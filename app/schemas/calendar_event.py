# app/schemas/calendar_event.py
from pydantic import BaseModel
from datetime import date

class CalendarEventBase(BaseModel):
    title: str
    event_date: date
    description: str | None = None

class CalendarEventCreate(CalendarEventBase):
    pass

class CalendarEvent(CalendarEventBase):
    id: int
    class Config:
        orm_mode = True
