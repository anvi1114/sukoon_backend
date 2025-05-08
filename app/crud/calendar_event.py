# app/crud/calendar_event.py
from sqlalchemy.orm import Session
from app.models.calendar_event import CalendarEvent
from app.schemas.calendar_event import CalendarEventCreate

def create_event(db: Session, event: CalendarEventCreate, user_id: int):
    db_event = CalendarEvent(**event.dict(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events_by_user(db: Session, user_id: int):
    return db.query(CalendarEvent).filter(CalendarEvent.user_id == user_id).all()
