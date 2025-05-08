# app/crud/task.py
from sqlalchemy.orm import Session
from app.models import task as task_models
from app.schemas import task as task_schema

def create_task(db: Session, task: task_schema.TaskCreate, user_id: int):
    db_task = task_models.Task(name=task.name, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(task_models.Task).filter(task_models.Task.user_id == user_id).all()

def update_task_status(db: Session, task_id: int, status: bool):
    task = db.query(task_models.Task).filter(task_models.Task.id == task_id).first()
    if task:
        task.status = status  # Update the status based on checkbox action
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(task_models.Task).filter(task_models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
