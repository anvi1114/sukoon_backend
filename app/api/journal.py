from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import journal as journal_schema
from app.crud import journal as journal_crud
from app.db.database import get_db

router = APIRouter(
    prefix="/journal",
    tags=["Journal"]
)

@router.post("/", response_model=journal_schema.JournalOut)
def create_journal(entry: journal_schema.JournalCreate, db: Session = Depends(get_db)):
    # Calls the CRUD function to create a journal entry
    return journal_crud.create_journal_entry(db, entry)

@router.get("/user/{user_id}", response_model=list[journal_schema.JournalOut])
def get_user_journals(user_id: int, db: Session = Depends(get_db)):
    # Fetch journals by user_id from CRUD
    return journal_crud.get_journals_by_user(db, user_id)
