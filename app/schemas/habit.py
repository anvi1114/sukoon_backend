from pydantic import BaseModel
from typing import List, Optional

class HabitDayBase(BaseModel):
    day: str
    completed: bool

class HabitDayCreate(HabitDayBase):
    pass

class HabitDay(HabitDayBase):
    id: int
    class Config:
        orm_mode = True

class HabitBase(BaseModel):
    name: str

class HabitCreate(HabitBase):
    days: List[HabitDayCreate]

class Habit(HabitBase):
    id: int
    days: List[HabitDay] = []

    class Config:
        orm_mode = True
