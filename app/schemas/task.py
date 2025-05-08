# app/schemas/task.py
from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    name: str

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    status: bool
    user_id: int

    class Config:
        orm_mode = True
