from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import auth, journal, task, habit 
from app.db.database import engine, get_db
from app.models import journal as journal_models  
from app.api import calendar_event
from app.db.base import Base
from app.api import auth
import app.models

app = FastAPI()

# ✅ Create all database tables
Base.metadata.create_all(bind=engine)

# ✅ Include all routers
app.include_router(auth.router, prefix="/auth")
app.include_router(journal.router)
app.include_router(task.router)
app.include_router(habit.router, prefix="/api", tags=["Habit Tracker"])  # ✅ Correctly placed
app.include_router(calendar_event.router, prefix="/api", tags=["Calendar"])

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to Sukoon Backend!"}

# ✅ About route
@app.get("/about")
def read_about():
    return {"about": "Sukoon is your personal self-care app. Stay calm, stay balanced!"}

# ✅ DB connection test
@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"message": "Connected to the database successfully!"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}
    

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth.login_user(db, form_data)