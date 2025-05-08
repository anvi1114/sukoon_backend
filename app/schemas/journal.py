from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class MoodEnum(str, Enum):
    happy = "happy"
    sad = "sad"
    neutral = "neutral"

class JournalCreate(BaseModel):
    user_id: int
    content: str
    photo_url: Optional[str] = None
    date: date
    mood: MoodEnum

class JournalOut(JournalCreate):
    id: int

    class Config:
        orm_mode = True
