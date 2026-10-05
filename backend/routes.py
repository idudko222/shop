from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import get_db
from schemas import BalanceResponse, MessageResponse, AddResponse, WithdrawResponse

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/balance", description="Get wallet balance", response_model=BalanceResponse | MessageResponse)
def get_balance(wallet_name: str | None = None, db: Session = Depends(get_db)):
    if wallet_name is None:
        return {"message": "Wallet name is required"}

    wallet = crud.get_wallet(db, wallet_name)
    if wallet is None:
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}' not found")

    return {"balance": wallet.amount}


@router.post(
    "/wallet/add",
    description="Add money to wallet",
    response_model=AddResponse,
)
def add_money(name: str, amount: int, db: Session = Depends(get_db)):
    wallet = crud.add_money(db, name, amount)
    return {
        "message": f"Added {amount} to wallet",
        "wallet": wallet.name,
        "balance": wallet.amount,
    }

@router.post(
    "/wallet/withdraw",
    description="Withdraw money from wallet",
    response_model=WithdrawResponse,
)
def withdraw_money(name: str, amount: int, db: Session = Depends(get_db)):
    wallet = crud.withdraw_money(db, name, amount)
    return {
        "message": f"Withdraw {amount} from wallet",
        "wallet": name,
        "balance": amount,
    }
