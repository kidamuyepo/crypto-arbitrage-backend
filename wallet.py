# backend/routes/wallet.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# You might need to import models, schemas, and get_db from the parent package (backend)
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/wallets", tags=["wallets"])

# Example endpoint: Get user's wallet (requires authentication in a real app)
@router.get("/{user_id}", response_model=schemas.WalletOut)
def get_user_wallet(user_id: int, db: Session = Depends(get_db)):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

# Example endpoint: Deposit funds (requires authentication)
@router.post("/deposit", response_model=schemas.DepositResponse)
def deposit_funds(deposit_request: schemas.DepositRequest, db: Session = Depends(get_db)):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == deposit_request.user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found for this user")

    wallet.balance += deposit_request.amount
    db.commit()
    db.refresh(wallet)
    return {
        "wallet_id": wallet.id,
        "wallet_address": wallet.wallet_address,
        "new_balance": wallet.balance,
        "message": f"Successfully deposited {deposit_request.amount} to wallet {wallet.wallet_address}"
    }