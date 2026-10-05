from pydantic import BaseModel, ConfigDict


class Wallet(BaseModel):
    name: str | None = None
    amount: int | float

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class BalanceResponse(BaseModel):
    balance: int | float

class MoneyTransferResponse(BaseModel):
    message: str
    wallet: str
    balance: int | float


class AddResponse(MoneyTransferResponse):
    pass

class WithdrawResponse(MoneyTransferResponse):
    pass