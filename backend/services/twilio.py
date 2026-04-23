import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp(message: str):
    """Send a WhatsApp message via Twilio."""
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_FROM"),
        to=os.getenv("TWILIO_WHATSAPP_TO"),
        body=message
    )

    print("✅ WhatsApp message sent")