# app/models/journal.py
from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class MoodEnum(enum.Enum):
    happy = "happy"
    sad = "sad"
    neutral = "neutral"

class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    photo_url = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    mood = Column(Enum(MoodEnum), default=MoodEnum.neutral)
   
   
    user = relationship("User", back_populates="journal_entries")

