# JanMitra AI – Government Welfare Assistant

JanMitra AI is an agentic AI and RAG-powered welfare discovery assistant for Indian citizens. It features dynamic multilingual interviews, structured profiling, precise criteria rules evaluation, document gap checklist calculations, and personalized step-by-step action roadmaps.

---

## Key Features

1. **Dynamic Interview Agent**: Conducts adaptive interviews (max 20 questions) and skips irrelevant nodes.
2. **Citizen Profiler Agent**: Extracts profile facts (income, age, landownership) from plain text.
3. **Retrieval Agent (RAG)**: Searches central and state policy FAQs using token-indexing.
4. **Welfare Eligibility Engine**: Ranks schemes into Highly Eligible, Eligible, and Potentially Eligible.
5. **Document Gap & Action Planner**: Creates custom guides to obtain missing certificates.
6. **Voice Integration**: Client-side speech synthesis (TTS) and recognition (STT) for Hindi and English.
7. **Report Exporter**: Generates customized welfare action plan PDFs.

---

## Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, React Router
- **Backend**: FastAPI, SQLite (SQLAlchemy)
- **Deployment**: Docker, docker-compose

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+

### Setup and Running (Using script)

We have provided a single PowerShell startup script at the root directory:

```powershell
.\start.ps1
```

This script will automatically:
1. Fire up the Python backend server (on `http://localhost:8000`)
2. Boot the Vite React developer server (on `http://localhost:5173`)
3. Open your default web browser to launch the interface.

---

## Manual Running

### 1. Backend Server Setup
```bash
# Navigate to project root
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start backend
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend Swagger documentation will be accessible at: `http://localhost:8000/docs`

### 2. Frontend Development
```bash
cd frontend
npm install
npm run dev
```

Frontend server will open on: `http://localhost:5173/`

---

## Folder Structure

```
JanMitra-AI/
├── backend/
│   ├── app/
│   │   ├── agents/          # Interview, Profiler, Eligibility, RAG, Action Plan Agents
│   │   ├── routes/          # Auth, Chat, Scheme CRUD endpoints
│   │   ├── utils/           # PDF compiler tools
│   │   ├── database.py      # SQLAlchemy sessions
│   │   ├── models.py        # Database entities
│   │   └── main.py          # Entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # VoiceButton, SchemeCard, ActionPlanView
│   │   ├── pages/           # Landing, Assessment, Results, Admin
│   │   └── index.css        # Theme variables & glassmorphism CSS
│   ├── Dockerfile
│   └── index.html           # SEO-optimized markup
├── docker-compose.yml
└── start.ps1
```
