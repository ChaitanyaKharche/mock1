import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def check_inventory(beds: int) -> str | None:
    # Stub function to simulate checking unit availability
    # In a real app, this would query a database
    if 1 <= beds <= 3:
        return f"UNIT-{beds}0{beds}"
    return None

def send_tour_confirmation_email(recipient_email: str, name: str, unit_id: str, property_address: str):
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT"))

    subject = "Your Tour Confirmation"
    body = f"""
    Hi {name},

    Your tour is confirmed!

    Property: {property_address}
    Unit: {unit_id}
    Suggested Tour Slot: Tuesday at 2:00 PM.

    Please let us know if you need to reschedule.

    Thanks,
    The Homewiz Team
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, recipient_email, msg.as_string())
            print(f"Email sent to {recipient_email}")
    except Exception as e:
        # In a real app, log this error properly
        print(f"Failed to send email: {e}")