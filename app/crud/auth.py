# # app/crud/auth.py
# from sqlalchemy.orm import Session
# from passlib.context import CryptContext
# from app.models.user import User
# from app.schemas.auth import UserCreate, UserLogin, PasswordChange
# from fastapi import HTTPException




# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Hash the password before storing it
# def hash_password(password: str):
#     return pwd_context.hash(password)

# # Verify password during login
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # Create a new user
# def create_user(db: Session, user: UserCreate):
#     db_user = User(name=user.name, email=user.email, password_hash=hash_password(user.password))
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # Get user by email (used for login and password reset)
# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()

# # Change user password
# def change_password(db: Session, email: str, current_password: str, new_password: str):
#     db_user = get_user_by_email(db, email)
#     if db_user and verify_password(current_password, db_user.password_hash):
#         db_user.password_hash = hash_password(new_password)
#         db.commit()
#         db.refresh(db_user)
#         return {"message": "Password updated successfully"}
#     raise HTTPException(status_code=400, detail="Invalid credentials or current password")



# # app/crud/auth.py
# from fastapi import HTTPException
# from app.models.user import User
# import uuid  # For generating unique reset tokens

# # Generate reset password token
# def generate_reset_token():
#     return str(uuid.uuid4())

# # Store reset token in database (you would add this field to the User model)
# def store_reset_token(db: Session, email: str, token: str):
#     db_user = db.query(User).filter(User.email == email).first()
#     if db_user:
#         db_user.reset_token = token  # Assume we add reset_token field in User model
#         db.commit()
#         db.refresh(db_user)
#         return db_user
#     raise HTTPException(status_code=400, detail="User not found")

# # Send the reset token via email (Simplified for now)
# def send_reset_email(email: str, token: str):
#     reset_link = f"http://localhost:8000/reset-password/{token}"
#     print(f"Send this link to {email}: {reset_link}")  # Simulate sending email
#     return {"message": "Reset email sent"}


# # app/auth.py

# from fastapi import Depends, HTTPException
# from app.db.database import get_db
# from app.models.user import User
# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     # Use the token to get user information (e.g., JWT decoding or fetching from DB)
#     # Example: Extract user from token (you can adjust according to your auth method)
#     user = db.query(User).filter(User.token == token).first()  # Adjust to your auth logic
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return user


from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.auth import UserCreate
from app.db.database import get_db
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uuid

# ================================ #
# 🔐 AUTH CONFIGURATION
# ================================ #

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_super_secret_key"  # use a secure env variable in real apps
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ================================ #
# 🔑 UTILITY FUNCTIONS
# ================================ #

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ================================ #
# 👤 USER CRUD OPERATIONS
# ================================ #

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def change_password(db: Session, email: str, current_password: str, new_password: str):
    db_user = get_user_by_email(db, email)
    if db_user and verify_password(current_password, db_user.password_hash):
        db_user.password_hash = hash_password(new_password)
        db.commit()
        db.refresh(db_user)
        return {"message": "Password updated successfully"}
    raise HTTPException(status_code=400, detail="Invalid credentials or current password")


# ================================ #
# 🔐 GET CURRENT USER
# ================================ #

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token payload invalid")
    
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


# ================================ #
# 🔁 PASSWORD RESET
# ================================ #

def generate_reset_token():
    return str(uuid.uuid4())

def store_reset_token(db: Session, email: str, token: str):
    db_user = get_user_by_email(db, email)
    if db_user:
        db_user.reset_token = token
        db.commit()
        db.refresh(db_user)
        return db_user
    raise HTTPException(status_code=400, detail="User not found")

def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/reset-password/{token}"
    print(f"Send this link to {email}: {reset_link}")
    return {"message": "Reset email sent"}


# ================================ #
# 🔓 LOGIN ROUTE HANDLER
# ================================ #

def login_user(db: Session, form_data: OAuth2PasswordRequestForm):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
