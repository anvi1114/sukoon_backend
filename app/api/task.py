# app/api/task.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import task as task_schema
from app.crud import task as task_crud
from app.db.database import get_db
# app/api/task.py
from app.api.auth import get_user_id  # Import the function

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=task_schema.TaskOut)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    return task_crud.create_task(db, task, user_id)

@router.get("/", response_model=list[task_schema.TaskOut])
def get_user_tasks(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    return task_crud.get_tasks_by_user(db, user_id)

@router.patch("/{task_id}", response_model=task_schema.TaskOut)
def update_task_status(task_id: int, status: bool, db: Session = Depends(get_db)):
    return task_crud.update_task_status(db, task_id, status)

@router.delete("/{task_id}", response_model=task_schema.TaskOut)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return task_crud.delete_task(db, task_id)


# app/api/task.py

from fastapi import Depends, HTTPException
from app.api.auth import get_current_user  # Assuming this function is defined in your auth module

def get_user_id(current_user: dict = Depends(get_current_user)):
    # Assuming 'current_user' contains user information (such as user_id)
    if current_user:
        return current_user['id']
    raise HTTPException(status_code=401, detail="User not authenticated")
