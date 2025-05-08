# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, db
from app.crud.auth import get_user_by_email, change_password
from app.db.database import get_db
from app.schemas.auth import UserCreate, UserLogin, PasswordChange
from app.schemas import auth as schemas


router = APIRouter()

# Sign Up API
@router.post("/signup")
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Login API
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user and crud.verify_password(user.password, db_user.password_hash):
        return {"message": "Login successful"}  # You can add JWT token here
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Change Password API
@router.put("/change-password")
def change_password_api(
    email: str,
    password_data: schemas.PasswordChange,
    db: Session = Depends(get_db)
):
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    return change_password(db, email, password_data.current_password, password_data.new_password)

# Forgot Password API
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email)
    if db_user:
        token = generate_reset_token()
        store_reset_token(db, email, token)
        send_reset_email(email, token)
        return {"message": "Password reset link sent"}
    raise HTTPException(status_code=400, detail="Email not registered")
# In app/api/auth.py

def get_user_id(token: str):
    # Logic to get user ID from the token
    pass


# At the bottom of app/api/auth.py

from fastapi import Depends, HTTPException

def get_current_user():
    # Dummy example — replace with your actual JWT/token logic later
    return {"id": 1}  # Just a placeholder for now

def get_user_id(current_user: dict = Depends(get_current_user)):
    if current_user:
        return current_user['id']
    raise HTTPException(status_code=401, detail="User not authenticated")
