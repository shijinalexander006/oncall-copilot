# 🚨 On-Call Copilot

A full-stack Incident Management Platform that helps engineers investigate production issues by collecting deployment and error events, correlating them, and generating AI-assisted incident analysis.

This project simulates how modern DevOps and Site Reliability Engineering (SRE) teams investigate production incidents.

---

## 📌 Features

- 📋 Incident Dashboard
- 📅 Incident Timeline
- 🔗 GitHub Deployment Webhook
- ⚠️ Sentry Error Webhook
- 🗄️ SQLite Database
- 🔍 Incident Correlation Engine
- 🤖 AI-Assisted Incident Analysis
- ⚡ FastAPI REST API
- 🌐 React Frontend

---

## 🏗️ Project Architecture

```
                GitHub
                   │
          Deployment Webhook
                   │
                   ▼
             FastAPI Backend
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    SQLite Database      Correlation Engine
                                 │
                                 ▼
                         AI Analysis Generator
                                 │
                                 ▼
                           React Dashboard
```

---

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- JavaScript
- HTML
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### Tools

- Git
- GitHub
- VS Code
- curl

---

## 📂 Project Structure

```
oncall-copilot
│
├── copilot-api
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── ...
│
├── copilot-web
│   ├── src
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   └── ...
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shijinalexander006/oncall-copilot.git
```

```
cd oncall-copilot
```

---

### 2. Backend Setup

```
cd copilot-api
```

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it

**Mac/Linux**

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn main:app --reload --port 8000
```

---

### 3. Frontend Setup

Open another terminal

```bash
cd copilot-web
```

Install dependencies

```bash
npm install
```

Run React

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

Backend

```
http://localhost:8000
```

---

## 📡 API Endpoints

### Health

```
GET /health
```

---

### List Incidents

```
GET /incidents
```

---

### Get Incident Details

```
GET /incidents/{id}
```

---

### GitHub Webhook

```
POST /webhooks/github
```

---

### Sentry Webhook

```
POST /webhooks/sentry
```

---

## 🧠 How It Works

1. GitHub sends a deployment webhook.
2. FastAPI stores the deployment event.
3. Sentry sends an error webhook.
4. FastAPI stores the error event.
5. The Correlation Engine compares deployment and error timestamps.
6. If an error occurs shortly after a deployment, an insight is generated.
7. The AI Analysis layer creates:
   - Summary
   - Possible Cause
   - Recommendation
8. React displays the incident timeline and AI analysis.

---

## 📸 Current Features

✅ Incident Dashboard

✅ Timeline View

✅ Deployment Correlation

✅ AI Analysis

✅ REST API

✅ SQLite Database

---

## 🚀 Future Improvements

- JWT Authentication
- PostgreSQL
- Docker
- Redis
- WebSockets
- Real GitHub Webhooks
- Real Sentry Integration
- OpenAI / Gemini Integration
- Slack Notifications
- Incident Severity Prediction
- Root Cause Analysis (LLM)
- Cloud Deployment (Render / AWS)

---

## 🎯 Learning Outcomes

This project demonstrates knowledge of:

- Full-Stack Development
- REST APIs
- FastAPI
- React
- SQLAlchemy ORM
- SQLite
- Git & GitHub
- Webhooks
- Event Correlation
- AI-Assisted Incident Analysis

---

## 👨‍💻 Author

**Shijin S Alexander**

GitHub:
https://github.com/shijinalexander006
