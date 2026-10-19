from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated
import joblib
import pandas as pd

from backend import crud
from backend.database import get_db
from backend.schemas import (BalanceResponse, MessageResponse, AddResponse,
                             WithdrawResponse, ScoreResponce, PredictionParams)

user_router = APIRouter(tags=['Wallet'])
wellcome_router = APIRouter(tags=['Hi!'], include_in_schema=False)
prediction_router = APIRouter(tags=['Prediction'])

PositiveAmount = Annotated[int, Query(gt=0)]

model = joblib.load('models/lr_model.pkl')

@wellcome_router.get("/")
async def root():
    return {"message": "Hello World"}


@user_router.get("/balance", description="Get wallet balance", response_model=BalanceResponse | MessageResponse)
def get_balance(wallet_name: str | None = None, db: Session = Depends(get_db)):
    if wallet_name is None:
        return {"message": "Wallet name is required"}

    wallet = crud.get_wallet(db, wallet_name)
    if wallet is None:
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}' not found")

    return {"balance": wallet.amount}


@user_router.post(
    "/wallet/add",
    description="Add money to wallet",
    response_model=AddResponse,
)
def add_money(name: str, amount: PositiveAmount, db: Session = Depends(get_db)):
    wallet = crud.add_money(db, name, amount)
    return {
        "message": f"Added {amount} to wallet",
        "wallet": wallet.name,
        "balance": wallet.amount,
    }


@user_router.post(
    "/wallet/withdraw",
    description="Withdraw money from wallet",
    response_model=WithdrawResponse,
)
def withdraw_money(name: str, amount: PositiveAmount, db: Session = Depends(get_db)):
    wallet = crud.withdraw_money(db, name, amount)
    return {
        "message": f"Withdraw {amount} from wallet",
        "wallet": wallet.name,
        "balance": wallet.amount
    }


@prediction_router.post(
    "/score",
    description="Прогноз дневной выручки",
    response_model=ScoreResponce,
)
def get_prediction(data: PredictionParams):
    features = pd.DataFrame([{
        "day_number": data.day_number,
        "Weekday": data.Weekday,
    }])

    money = float(model.predict(features)[0])

    return {"money": money}