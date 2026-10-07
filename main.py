from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)
app = FastAPI(title="가계부 API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/accounts", response_model=schemas.AccountRead, status_code=201)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_db)):
    account = models.Account(name=payload.name, balance=payload.balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@app.get("/accounts", response_model=list[schemas.AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return (
        db.execute(select(models.Account).order_by(models.Account.id))
        .scalars()
        .all()
    )


@app.get("/accounts/{account_id}", response_model=schemas.AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(models.Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="계좌를 찾을 수 없습니다")
    return account


@app.post("/transactions", response_model=schemas.TransactionRead, status_code=201)
def create_transaction(
    payload: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    if db.get(models.Account, payload.account_id) is None:
        raise HTTPException(status_code=404, detail="해당 계좌가 없습니다")
    transaction = models.Transaction(
        account_id=payload.account_id,
        category_id=payload.category_id,
        amount=payload.amount,
        memo=payload.memo,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@app.get(
    "/accounts/{account_id}/detail", response_model=schemas.AccountReadWithTx
)
def account_detail(account_id: int, db: Session = Depends(get_db)):
    account = db.get(models.Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="계좌를 찾을 수 없습니다")
    return account


@app.get("/stats/by-category")
def by_category(db: Session = Depends(get_db)):
    statement = (
        select(
            models.Category.name,
            func.sum(models.Transaction.amount),
            func.count(),
        )
        .join(
            models.Category,
            models.Transaction.category_id == models.Category.id,
            isouter=True,
        )
        .where(models.Transaction.amount < 0)
        .group_by(models.Category.name)
    )
    return [
        {"category": name, "total": total, "count": count}
        for name, total, count in db.execute(statement).all()
    ]