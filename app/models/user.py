# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.calendar_event import CalendarEvent

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    journal_entries = relationship("JournalEntry", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    events = relationship("CalendarEvent", back_populates="user", cascade="all, delete")
