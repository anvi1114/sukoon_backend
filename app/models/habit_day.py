from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class HabitDay(Base):
    __tablename__ = "habit_days"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    day = Column(String, nullable=False)  # e.g., "S", "M", ...
    completed = Column(Boolean, default=False)

    habit = relationship("Habit", back_populates="days")
