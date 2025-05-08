# app/crud/auth.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, PasswordChange
from fastapi import HTTPException




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the password before storing it
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password during login
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create a new user
def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by email (used for login and password reset)
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Change user password
def change_password(db: Session, email: str, current_password: str, new_password: str):
    db_user = get_user_by_email(db, email)
    if db_user and verify_password(current_password, db_user.password_hash):
        db_user.password_hash = hash_password(new_password)
        db.commit()
        db.refresh(db_user)
        return {"message": "Password updated successfully"}
    raise HTTPException(status_code=400, detail="Invalid credentials or current password")



# app/crud/auth.py
from fastapi import HTTPException
from app.models.user import User
import uuid  # For generating unique reset tokens

# Generate reset password token
def generate_reset_token():
    return str(uuid.uuid4())

# Store reset token in database (you would add this field to the User model)
def store_reset_token(db: Session, email: str, token: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        db_user.reset_token = token  # Assume we add reset_token field in User model
        db.commit()
        db.refresh(db_user)
        return db_user
    raise HTTPException(status_code=400, detail="User not found")

# Send the reset token via email (Simplified for now)
def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/reset-password/{token}"
    print(f"Send this link to {email}: {reset_link}")  # Simulate sending email
    return {"message": "Reset email sent"}


# app/auth.py

from fastapi import Depends, HTTPException
from app.db.database import get_db
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Use the token to get user information (e.g., JWT decoding or fetching from DB)
    # Example: Extract user from token (you can adjust according to your auth method)
    user = db.query(User).filter(User.token == token).first()  # Adjust to your auth logic
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
