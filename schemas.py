from datetime import datetime

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    name: str
    balance: int = 0


class AccountRead(BaseModel):
    id: int
    name: str
    balance: int
    model_config = {"from_attributes": True}


class TransactionCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    amount: int
    memo: str | None = None


class TransactionRead(BaseModel):
    id: int
    account_id: int
    category_id: int | None
    amount: int
    memo: str | None
    occurred_at: datetime
    model_config = {"from_attributes": True}


class AccountReadWithTx(BaseModel):
    id: int
    name: str
    balance: int
    transactions: list[TransactionRead] = Field(default_factory=list)
    model_config = {"from_attributes": True}