import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

def check_inventory(beds: int) -> str | None:
    """Stub function to simulate checking unit availability."""
    if 1 <= beds <= 3:
        return f"UNIT-{beds}0{beds}"
    return None

def send_tour_confirmation_email(recipient_email: str, name: str, unit_id: str, property_address: str):
    """Sends a confirmation email using the SendGrid API."""
    message = Mail(
        from_email=os.getenv("VERIFIED_SENDER_EMAIL"), # IMPORTANT: Use an email from a domain you verified on SendGrid
        to_emails=recipient_email,
        subject="Your Tour Confirmation",
        html_content=f"""
        <p>Hi {name},</p>
        <p>Your tour is confirmed!</p>
        <ul>
            <li><strong>Property:</strong> {property_address}</li>
            <li><strong>Unit:</strong> {unit_id}</li>
            <li><strong>Suggested Tour Slot:</strong> Tuesday at 2:00 PM.</li>
        </ul>
        <p>Please let us know if you need to reschedule.</p>
        <p>Thanks,<br>The Homewiz Team</p>
        """
    )
    try:
        sendgrid_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sendgrid_client.send(message)
        print(f"Email sent to {recipient_email} via SendGrid, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email via SendGrid: {e}")

def send_tour_confirmation_sms(recipient_phone: str, name: str, unit_id: str):
    """Sends a confirmation SMS using the Twilio API."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    
    if not all([account_sid, auth_token, twilio_number]):
        print("Twilio credentials are not fully configured.")
        return

    client = Client(account_sid, auth_token)

    try:
        # Ensure phone number is in E.164 format for Twilio
        formatted_phone = recipient_phone if recipient_phone.startswith('+') else f'+{recipient_phone}'
        
        message = client.messages.create(
            body=f"Hi {name}, your tour for unit {unit_id} is confirmed! See you Tuesday at 2:00 PM. -Homewiz Team",
            from_=twilio_number,
            to=formatted_phone
        )
        print(f"SMS sent to {formatted_phone} via Twilio, SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS via Twilio: {e}")