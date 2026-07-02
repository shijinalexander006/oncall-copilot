from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    status = Column(String, default="open")
    started_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("Event", back_populates="incident")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    type = Column(String)
    source = Column(String)
    title = Column(String)
    payload = Column(JSON)
    occurred_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="events")