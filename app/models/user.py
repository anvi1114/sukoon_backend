# # app/models/user.py
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from app.db.base import Base
# #from app.models.calendar_event import CalendarEvent


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     password_hash = Column(String)
#     journal_entries = relationship("Journal", back_populates="user")
#     tasks = relationship("Task", back_populates="user")
#     calendar_events = relationship("CalendarEvent", back_populates="user", lazy="selectin")


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # 🔐 For password reset functionality
    reset_token = Column(String, nullable=True)

    # 📒 Relationships
    journal_entries = relationship("Journal", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    calendar_events = relationship("CalendarEvent", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
