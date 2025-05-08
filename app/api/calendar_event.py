# app/api/calendar_event.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.calendar_event import CalendarEvent, CalendarEventCreate
from app.crud import calendar_event
from app.db.database import get_db

router = APIRouter()

@router.post("/events/", response_model=CalendarEvent)
def add_event(event: CalendarEventCreate, db: Session = Depends(get_db)):
    return calendar_event.create_event(db, event, user_id=1)  # Replace with actual user_id

@router.get("/events/", response_model=list[CalendarEvent])
def list_events(db: Session = Depends(get_db)):
    return calendar_event.get_events_by_user(db, user_id=1)  # Replace with actual user_id
