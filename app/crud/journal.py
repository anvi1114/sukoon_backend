from sqlalchemy.orm import Session
from app.models.journal import Journal
from app.schemas.journal import JournalCreate

def create_journal_entry(db: Session, entry: JournalCreate):
    journal = Journal(**entry.dict())
    db.add(journal)
    db.commit()
    db.refresh(journal)
    return journal

def get_journals_by_user(db: Session, user_id: int):
    return db.query(Journal).filter(Journal.user_id == user_id).all()

