# 📧 Email Triage Agent
### Your inbox, handled. Automatically.

The average knowledge worker spends **2.5 hours per day on email**. This agent cuts that dramatically — autonomously reading, classifying, and drafting replies to your emails every morning, then asking for your approval before sending anything.

---

## 🚀 What It Does

- **Fetches** your last 20 unread emails via Gmail API
- **Classifies** each email as urgent / normal / newsletter / spam using Groq LLM
- **Drafts** professional replies for emails that need a response
- **Sends a WhatsApp digest** every morning at 8AM with a summary
- **Human-in-the-loop** — you approve or reject each draft before anything is sent

---

## 🎬 Live Demo

---

## 🧠 How It Works

```
Gmail API → Classify (Groq LLM) → Draft Replies → WhatsApp Digest → Human Review → Send
```

Built with **LangGraph** — a stateful agent framework that passes context through each step:

| Step | What Happens |
|------|-------------|
| `fetch_emails` | Pulls last 20 unread emails from Gmail |
| `classify_emails` | Groq LLM labels each: urgency + category + needs_reply |
| `draft_replies` | Groq LLM writes a professional reply for urgent/normal emails |
| `create_digest` | Summarizes everything into a human-readable report |
| `send_approved` | Sends only the drafts you approved via Gmail API |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | LangGraph |
| LLM | Groq (llama-3.3-70b-versatile) |
| Email | Gmail API + OAuth2 |
| Notifications | Twilio WhatsApp |
| Backend | FastAPI + APScheduler |
| Frontend | Next.js + Tailwind CSS |
| Deployment | Railway (backend) + Vercel (frontend) |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Gmail account with API access
- Groq API key (free tier works)
- Twilio account (sandbox is free)

### 1. Clone the repo

```bash
git clone https://github.com/Anushakashif/Email-triage-agent.git
cd Email-triage-agent
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Environment variables

Create `.env` in the `backend/` folder:

```env
GROQ_API_KEY=your_groq_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+your_number
FRONTEND_URL=http://localhost:3000
```

### 4. Gmail OAuth setup

- Go to [Google Cloud Console](https://console.cloud.google.com)
- Enable Gmail API
- Create OAuth credentials (Web Application)
- Download as `credentials.json` → place in `backend/`
- Run the backend once to authenticate via browser

### 5. Run the backend

```bash
cd backend
uvicorn main:app --reload
```

### 6. Frontend setup

```bash
cd frontend
npm install
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

```bash
npm run dev
```

---

## 📱 How To Use

1. **Automatic** — Agent runs every day at 8AM, sends WhatsApp digest
2. **Manual** — Hit `/run-agent` on the API to trigger anytime
3. **Review** — Open the frontend, approve/reject draft replies
4. **Send** — Click send → only approved emails go out

---

## 🏗️ Project Structure

```
email-triage-agent/
├── backend/
│   ├── agent/
│   │   ├── graph.py      # LangGraph pipeline
│   │   ├── nodes.py      # 5 agent nodes
│   │   └── state.py      # Shared state definition
│   ├── services/
│   │   ├── gmail.py      # Gmail API wrapper
│   │   └── twilio.py     # WhatsApp sender
│   ├── main.py           # FastAPI + scheduler
│   └── requirements.txt
└── frontend/
    └── app/
        └── page.tsx      # Review & approval UI
```

---

## 🔒 Security

- Gmail credentials never leave your machine
- `.env` and `token.json` are gitignored
- Human approval required before any email is sent
- No emails are stored — everything is in-memory

---

*Built to save 2.5 hours a day. One email at a time.*
