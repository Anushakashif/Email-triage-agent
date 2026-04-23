import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from agent.graph import email_graph
from apscheduler.schedulers.background import BackgroundScheduler
from services.twilio import send_whatsapp

load_dotenv()

app = FastAPI()

# Allow Next.js frontend to talk to our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store state in memory for now
current_state = {}

def run_daily_agent():
    """Run agent and send digest to WhatsApp."""
    print("⏰ Running scheduled email triage...")
    
    result = email_graph.invoke({
        "raw_emails": [],
        "classified": [],
        "drafts": [],
        "digest": "",
        "human_approved": False,
        "emails_to_send": []
    })
    
    global current_state
    current_state = result
    
    send_whatsapp(result["digest"])
    print("✅ Daily digest sent to WhatsApp")

# Start scheduler AFTER function is defined
scheduler = BackgroundScheduler()
scheduler.add_job(run_daily_agent, 'cron', hour=8, minute=0)
scheduler.start()

@app.get("/")
def root():
    return {"status": "Email Triage Agent Running"}

@app.post("/run-agent")
async def run_agent():
    global current_state
    result = email_graph.invoke({
        "raw_emails": [],
        "classified": [],
        "drafts": [],
        "digest": "",
        "human_approved": False,
        "emails_to_send": []
    })
    current_state = result
    return {"status": "done", "digest": result["digest"]}

@app.get("/digest")
def get_digest():
    return {"digest": current_state.get("digest", "No digest yet. Run agent first.")}

@app.get("/drafts")
def get_drafts():
    return {"drafts": current_state.get("drafts", [])}

@app.post("/approve")
def approve_and_send(approved_ids: list[str]):
    global current_state
    approved_drafts = [
        d for d in current_state.get("drafts", [])
        if d["id"] in approved_ids
    ]
    current_state["human_approved"] = True
    current_state["emails_to_send"] = approved_drafts
    from agent.nodes import send_approved_node
    send_approved_node(current_state)
    return {"status": "sent", "count": len(approved_drafts)}