# backend/schemas.py
from pydantic import BaseModel, EmailStr

# --- User schemas ---

# Schema for user registration request body
class RegisterModel(BaseModel):
    username: str
    email: EmailStr # Uses Pydantic's EmailStr for email format validation
    password: str

# Schema for user login request body (basic, often OAuth2PasswordRequestForm is used with form data)
class LoginModel(BaseModel):
    username: str
    password: str

# Schema for user data returned in responses (e.g., after registration)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    # Pydantic's Config class to enable ORM mode.
    # This allows Pydantic to read data directly from SQLAlchemy model instances.
    class Config:
        from_attributes = True # Pydantic v2.x, use orm_mode = True for older versions

# --- Token response schema ---

# Schema for the JWT token response after successful login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer" # Standard token type

# --- Wallet schemas ---

# Schema for wallet data returned in responses
class WalletOut(BaseModel):
    id: int
    user_id: int
    wallet_address: str
    balance: float

    class Config:
        from_attributes = True # Pydantic v2.x, use orm_mode = True for older versions

# Schema for deposit request body
class DepositRequest(BaseModel):
    user_id: int
    amount: float

# Schema for deposit response
class DepositResponse(BaseModel):
    wallet_id: int
    wallet_address: str
    new_balance: float
    message: str