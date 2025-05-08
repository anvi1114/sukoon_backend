from sqlalchemy.orm import Session
from app.models.habit import Habit
from app.models.habit_day import HabitDay
from app.schemas.habit import HabitCreate

def create_habit(db: Session, habit: HabitCreate, user_id: int):
    db_habit = Habit(name=habit.name, user_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)

    for day in habit.days:
        db_day = HabitDay(day=day.day, completed=day.completed, habit_id=db_habit.id)
        db.add(db_day)

    db.commit()
    db.refresh(db_habit)
    return db_habit

def get_user_habits(db: Session, user_id: int):
    return db.query(Habit).filter(Habit.user_id == user_id).all()

def update_day_status(db: Session, habit_day_id: int, completed: bool):
    day = db.query(HabitDay).filter(HabitDay.id == habit_day_id).first()
    if day:
        day.completed = completed
        db.commit()
    return day
