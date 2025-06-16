import uuid
from sqlalchemy.orm import Session
from . import models

def get_or_create_wallet(db: Session, user_id: int):
    wallet = db.query(models.Wallet).filter_by(user_id=user_id).first()
    if not wallet:
        wallet_address = str(uuid.uuid4())
        wallet = models.Wallet(user_id=user_id, wallet_address=wallet_address)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet

def deposit_to_wallet(db: Session, user_id: int, amount: float):
    wallet = db.query(models.Wallet).filter_by(user_id=user_id).first()
    if not wallet:
        return None, "Wallet not found"

    wallet.balance += amount
    db.commit()
    db.refresh(wallet)
    return wallet, "Deposit successful"
