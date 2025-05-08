# # app/db/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from .config import DATABASE_URL

# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Make sure this line exists

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


# # Database connection URL (Make sure to replace 'username' and 'password' with your PostgreSQL credentials)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:anvi1234@localhost:5432/sukoon_db"

# # Create an engine for connecting to the database
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# # SessionLocal will be used to interact with the database
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for all SQLAlchemy models
# Base = declarative_base()

# # Dependency function to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Get DB URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
