import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Incident, Event

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="On-call Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "oncall-copilot-api"}


@app.post("/webhooks/sentry")
async def sentry_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    issue = body.get("data", {}).get("issue", {})
    title = issue.get("title", "Unknown Sentry error")
    occurred_at = datetime.utcnow()

    incident = Incident(title=title, status="open")
    db.add(incident)
    db.flush()

    event = Event(
        incident_id=incident.id,
        type="error_spike",
        source="sentry",
        title=title,
        payload=body,
        occurred_at=occurred_at,
    )

    db.add(event)
    db.commit()

    return {"ok": True, "incident_id": incident.id}


@app.post("/webhooks/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    if body.get("zen"):
        return {"ok": True, "message": "github ping received"}

    workflow = body.get("workflow_run", {})
    title = f"Deploy: {workflow.get('name', 'workflow')} ({workflow.get('conclusion', 'unknown')})"

    occurred_at = datetime.utcnow()

    incident = Incident(title=title, status="open")
    db.add(incident)
    db.flush()

    event = Event(
        incident_id=incident.id,
        type="deploy",
        source="github",
        title=title,
        payload=body,
        occurred_at=occurred_at,
    )

    db.add(event)
    db.commit()

    return {"ok": True, "incident_id": incident.id}


@app.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(
        Incident.started_at.desc()
    ).all()


@app.get("/incidents/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        return {"error": "not found"}

    events = (
        db.query(Event)
        .filter(Event.incident_id == incident_id)
        .order_by(Event.occurred_at.asc())
        .all()
    )

    insights = []

    all_events = (
        db.query(Event)
        .order_by(Event.occurred_at.asc())
        .all()
    )

    current_error = next(
        (e for e in events if e.type == "error_spike"),
        None
    )

    if current_error:

        recent_deploy = None

        for event in reversed(all_events):

            if event.type == "deploy":

                delta = (
                    current_error.occurred_at
                    - event.occurred_at
                )

                if timedelta(0) <= delta <= timedelta(minutes=15):
                    recent_deploy = event
                    break

        if recent_deploy:

            minutes = int(
                (
                    current_error.occurred_at
                    - recent_deploy.occurred_at
                ).total_seconds() // 60
            )

            insights.append({
                "type": "insight",
                "title": f"Possible cause: error started {minutes} min after deployment"
            })

    # AI Analysis Layer
    ai_analysis = {
        "summary": "No analysis available",
        "possible_cause": "Unknown",
        "recommendation": "Investigate manually"
    }

    if insights:
        ai_analysis = {
            "summary": incident.title,
            "possible_cause": insights[0]["title"],
            "recommendation":
                "Review deployment changes and inspect recent commits."
        }

    return {
        "incident": incident,
        "events": events,
        "insights": insights,
        "ai_analysis": ai_analysis,
    }