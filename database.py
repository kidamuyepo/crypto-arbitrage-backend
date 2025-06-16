# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL. It will create 'db.sqlite3' in your backend directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite to allow multiple threads
# to interact with the database, which is common in web servers like FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class to get a database session.
# autocommit=False ensures transactions are explicitly committed.
# autoflush=False prevents flushing pending changes before commit.
# bind=engine connects the session to our database engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your SQLAlchemy models.
Base = declarative_base()

# Dependency to get a database session.
# This function yields a session and ensures it's closed afterward,
# making it suitable for FastAPI's Dependency Injection.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()