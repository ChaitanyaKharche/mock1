import re
from .models import ConversationState
from .database import get_session, save_session
from .services import check_inventory, send_tour_confirmation_email
from pydantic import validate_email

def process_message(session_id: str, message: str) -> str:
    session = get_session(session_id)
    if not session:
        session = ConversationState(session_id=session_id)

    # Allow booking at any point if we have enough info
    if "book" in message.lower() and session.state == "COMPLETED":
        unit_id = check_inventory(session.beds)
        if unit_id and session.email:
            send_tour_confirmation_email(
                recipient_email=session.email,
                name=session.name,
                unit_id=unit_id,
                property_address="123 Main St, Anytown, USA"
            )
            return f"Great! I've sent a tour confirmation for unit {unit_id} to {session.email}. See you soon!"
        else:
            return "Something went wrong. I couldn't find a unit or your email is missing."

    response = ""
    current_state = session.state

    if current_state == "AWAITING_NAME":
        session.name = message.strip()
        session.state = "AWAITING_EMAIL"
        response = f"Thanks, {session.name}. What is your email address?"
    
    elif current_state == "AWAITING_EMAIL":
        try:
            validate_email(message.strip())
            session.email = message.strip()
            session.state = "AWAITING_PHONE"
            response = "Got it. And your phone number?"
        except ValueError:
            response = "That doesn't look like a valid email. Please try again."

    elif current_state == "AWAITING_PHONE":
        # Simple regex for phone format validation
        phone_match = re.match(r"^\+?1?\d{9,15}$", message.strip().replace(" ", ""))
        if phone_match:
            session.phone = message.strip()
            session.state = "AWAITING_MOVE_IN_DATE"
            response = "Perfect. When are you looking to move in? (e.g., 'August 1st', '2025-08-01')"
        else:
            response = "Please provide a valid phone number."

    elif current_state == "AWAITING_MOVE_IN_DATE":
        session.move_in_date = message.strip()
        session.state = "AWAITING_BEDS"
        response = "Thanks. How many bedrooms are you looking for?"

    elif current_state == "AWAITING_BEDS":
        try:
            beds = int(re.search(r'\d+', message).group())
            if 1 <= beds <= 5:
                session.beds = beds
                session.state = "COMPLETED"
                unit_id = check_inventory(beds)
                if unit_id:
                    response = f"Excellent! We have a {beds}-bedroom unit available: {unit_id}. You can say 'book' to schedule a tour, or ask something else."
                else:
                    response = f"I'm sorry, we don't have any {beds}-bedroom units available right now."
            else:
                response = "We only offer units with 1 to 5 bedrooms. Please choose a number in that range."
        except (ValueError, AttributeError):
            response = "Please enter a valid number for the bedrooms."
    
    else: # COMPLETED state
        response = "I have all your details. Just say 'book' to schedule the tour."

    save_session(session)
    return response