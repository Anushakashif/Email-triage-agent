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

    MAX_LENGTH = 1500
    chunks = [message[i:i+MAX_LENGTH] for i in range(0, len(message), MAX_LENGTH)]

    for i, chunk in enumerate(chunks):
        client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP_FROM"),
            to=os.getenv("TWILIO_WHATSAPP_TO"),
            body=f"({i+1}/{len(chunks)}) {chunk}"
        )

    print(f"✅ WhatsApp message sent in {len(chunks)} part(s)")