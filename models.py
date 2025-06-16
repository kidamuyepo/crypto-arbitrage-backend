# backend/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# Import Base from the database module.
# Since models.py is in the 'backend' package, and database.py is also in 'backend',
# we can use a direct import from the module name relative to the package.
from backend.database import Base

class User(Base):
    __tablename__ = "users" # Name of the database table

    # Define columns for the User table
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False) # Username must be unique and not null
    email = Column(String, unique=True, index=True, nullable=False)    # Email must be unique and not null
    password = Column(String, nullable=False) # Hashed password, cannot be null
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False) # Timestamp for user creation

    # Define a relationship with the Wallet model (one-to-one)
    # uselist=False indicates a one-to-one relationship.
    wallet = relationship("Wallet", back_populates="owner", uselist=False)

class Wallet(Base):
    __tablename__ = "wallets" # Name of the database table

    # Define columns for the Wallet table
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False) # Foreign key to user, unique for one-to-one
    wallet_address = Column(String, unique=True, nullable=False) # Unique wallet address
    balance = Column(Float, default=0.0, nullable=False) # Current balance, defaults to 0.0, not null
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False) # Timestamp for wallet creation

    # Define a relationship back to the User model
    owner = relationship("User", back_populates="wallet")