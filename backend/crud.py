from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import WalletModel


def get_wallet(db: Session, name: str) -> WalletModel | None:
    return db.scalar(select(WalletModel).where(WalletModel.name == name))


def add_money(db: Session, name: str, amount: int) -> WalletModel:
    wallet = get_wallet(db, name)
    if wallet is None:
        wallet = WalletModel(name=name, amount=0)
        db.add(wallet)

    wallet.amount += amount
    db.commit()
    db.refresh(wallet)
    return wallet


def withdraw_money(db: Session, name: str, amount: int) -> WalletModel | None:
    wallet = get_wallet(db, name)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    elif wallet.amount < amount:
        raise HTTPException(status_code=404, detail="U don't have this this much")
    wallet.amount -= amount
    db.commit()
    db.refresh(wallet)
    return wallet
