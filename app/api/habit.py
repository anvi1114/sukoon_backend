from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.habit import HabitCreate, Habit
from app.crud import habit as crud_habit
from typing import List

router = APIRouter()

@router.post("/habits/", response_model=Habit)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db), user_id: int = 1):
    return crud_habit.create_habit(db=db, habit=habit, user_id=user_id)

@router.get("/habits/", response_model=List[Habit])
def get_habits(db: Session = Depends(get_db), user_id: int = 1):
    return crud_habit.get_user_habits(db=db, user_id=user_id)

@router.put("/habits/day/{day_id}")
def update_day(day_id: int, completed: bool, db: Session = Depends(get_db)):
    return crud_habit.update_day_status(db=db, habit_day_id=day_id, completed=completed)
