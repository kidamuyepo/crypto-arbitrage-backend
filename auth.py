# backend/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # For form-data login
from sqlalchemy.orm import Session
from passlib.context import CryptContext # For password hashing
from jose import jwt # For JWT token creation
from datetime import datetime, timedelta

# Import models, schemas, and get_db from the 'backend' package
# This is correct when running `uvicorn backend.main:app` from the project root.
from backend import models, schemas
from backend.database import get_db

# Initialize the API Router.
# The `prefix="/auth"` is REMOVED from here, as it's defined in main.py.
router = APIRouter(tags=["auth"]) # <--- CRITICAL CHANGE: prefix="/auth" removed

# Password hashing context (for bcrypt algorithm)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key and algorithm (*** IMPORTANT: USE ENVIRONMENT VARIABLES FOR PRODUCTION! ***)
SECRET_KEY = "your-super-secret-key-that-should-be-in-env-var"
ALGORITHM = "HS256" # Hashing algorithm for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token expiration time

# Helper function to verify a plain password against a hashed one
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to hash a plain password
def hash_password(password: str):
    return pwd_context.hash(password)

# Helper function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire}) # Add expiration time to token payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Register new user endpoint
@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user: schemas.RegisterModel, db: Session = Depends(get_db)):
    # Check if username already exists
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    # Check if email already exists
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving
    hashed_password = hash_password(user.password)

    # Create a new User instance
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    # Add to database, commit, and refresh
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Refresh to get database-generated fields like 'id' and 'created_at'

    return new_user

# User login endpoint
# Uses OAuth2PasswordRequestForm for standard username/password form-data login
@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by username
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # Verify user existence and password
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create access token for the logged-in user
    access_token = create_access_token(data={"sub": user.username}) # Using username as subject

    # Return token response
    return {"access_token": access_token, "token_type": "bearer"}