import os
import json
from groq import Groq
from dotenv import load_dotenv
from services.gmail import fetch_unread_emails
from agent.state import EmailState
from services.gmail import fetch_unread_emails, get_gmail_service

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def fetch_emails_node(state: EmailState) -> EmailState:
    """Node 1 - Fetch unread emails from Gmail."""
    print("📧 Fetching unread emails...")
    
    emails = fetch_unread_emails(max_results=20)
    
    print(f"✅ Fetched {len(emails)} unread emails")
    
    return {"raw_emails": emails}

def classify_emails_node(state: EmailState) -> EmailState:
    """Node 2 - Classify each email by urgency and category."""
    print("🔍 Classifying emails...")
    
    classified = []
    
    for email in state["raw_emails"]:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"""Classify this email:
From: {email['from']}
Subject: {email['subject']}
Preview: {email['snippet']}

Reply with JSON only, no explanation:
{{"urgency": "urgent|normal|low", "category": "work|newsletter|spam|personal", "needs_reply": true|false}}"""
                }
            ]
        )
        
        try:
            classification = json.loads(response.choices[0].message.content)
        except:
            classification = {"urgency": "normal", "category": "work", "needs_reply": False}
        
        classified.append({**email, **classification})
    
    print(f"✅ Classified {len(classified)} emails")
    
    return {"classified": classified}

def draft_replies_node(state: EmailState) -> EmailState:
    """Node 3 - Draft replies for urgent and normal emails."""
    print("✍️ Drafting replies...")
    
    drafts = []
    
    for email in state["classified"]:
        # Only draft replies for urgent and normal emails that need reply
        if email["urgency"] in ["urgent", "normal"] and email["needs_reply"]:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Draft a professional reply for this email:
From: {email['from']}
Subject: {email['subject']}
Preview: {email['snippet']}

Rules:
- Keep it short and professional
- Don't make up specific details
- End with: Best regards

Reply with the email body only, no subject line."""
                    }
                ]
            )
            
            draft_body = response.choices[0].message.content
            
            drafts.append({
                **email,
                "draft": draft_body
            })
    
    print(f"✅ Drafted {len(drafts)} replies")
    
    return {"drafts": drafts}

def create_digest_node(state: EmailState) -> EmailState:
    """Node 4 - Create a summary digest for the human."""
    print("📋 Creating digest...")

    total = len(state["classified"])
    urgent = [e for e in state["classified"] if e["urgency"] == "urgent"]
    normal = [e for e in state["classified"] if e["urgency"] == "normal"]
    low = [e for e in state["classified"] if e["urgency"] == "low"]
    drafts = state["drafts"]

    digest = f"""
📧 EMAIL DIGEST
═══════════════════════════════
Total Unread: {total}
🔴 Urgent: {len(urgent)}
🟡 Normal: {len(normal)}
🟢 Low: {len(low)}
✍️ Drafts Ready: {len(drafts)}

🔴 URGENT EMAILS:
"""
    for email in urgent:
        digest += f"""
- From: {email['from']}
  Subject: {email['subject']}
"""

    digest += "\n🟡 NORMAL EMAILS:\n"
    for email in normal:
        digest += f"""
- From: {email['from']}
  Subject: {email['subject']}
"""

    digest += "\n✍️ DRAFTS PREPARED:\n"
    for draft in drafts:
        digest += f"""
- Subject: {draft['subject']}
  Draft: {draft['draft'][:100]}...
"""

    digest += "\n═══════════════════════════════"
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    digest += f"\nGo to {frontend_url} to approve and send"

    print("✅ Digest created")

    return {"digest": digest}

def send_approved_node(state: EmailState) -> EmailState:
    """Node 5 - Send approved email drafts via Gmail."""
    print("📤 Sending approved emails...")

    if not state["human_approved"]:
        print("❌ Human did not approve. Nothing sent.")
        return {"emails_to_send": []}

    service = get_gmail_service()
    sent = []

    for draft in state["emails_to_send"]:
        try:
            import base64
            from email.mime.text import MIMEText

            message = MIMEText(draft["draft"])
            message["to"] = draft["from"]
            message["subject"] = f"Re: {draft['subject']}"

            raw = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode("utf-8")

            service.users().messages().send(
                userId="me",
                body={"raw": raw}
            ).execute()

            sent.append(draft)
            print(f"✅ Sent reply to {draft['from']}")

        except Exception as e:
            print(f"❌ Failed to send to {draft['from']}: {e}")

    print(f"✅ Sent {len(sent)} emails")
    return {"emails_to_send": sent}