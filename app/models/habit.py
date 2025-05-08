from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.habit_day import HabitDay

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # if users exist
    # Relationship to track which days habit is marked
    days = relationship("HabitDay", back_populates="habit", cascade="all, delete")
