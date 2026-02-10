from fastapi import FastAPI, Query, HTTPException, status, Path, Body, Depends
from contextlib import asynccontextmanager
from .schemas import ExpenseCreateSchema, ExpenseUpdateSchema
from core.db import db_init, db_session, Expense
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_init()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/expenses", status_code=status.HTTP_200_OK)
def retrieve_expenses(expense_id: int | None = Query(None), db: Session = Depends(db_session)):
    existing_expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    expenses = db.query(Expense).all()
    if expense_id is not None:
        if existing_expense is not None:
            return existing_expense
        raise HTTPException(
            status_code=404, detail="Expense not found")
    return expenses


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreateSchema = Body(...), db: Session = Depends(db_session)):
    existing_expense = db.query(Expense).filter_by(id=expense.id).one_or_none()
    if existing_expense is not None:
        raise HTTPException(
            status_code=409, detail=f"Expense with this ID {expense.id} already exists.")

    new_expense = Expense(id=expense.id, description=expense.description, amount=expense.amount)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@app.put("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
def update_expense(expense_id: int = Path(...), expense: ExpenseUpdateSchema = Body(...),
                   db: Session = Depends(db_session)):
    existing_expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if existing_expense is None:
        raise HTTPException(
            status_code=404, detail="Expense not found")

    new_expense = {"description": expense.description, "amount": expense.amount}
    db.query(Expense).filter_by(id=expense_id).update(new_expense)
    db.commit()

    return new_expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int = Path(...), db: Session = Depends(db_session)):
    existing_expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if existing_expense is None:
        raise HTTPException(
            status_code=404, detail="Expense not found")

    db.query(Expense).filter_by(id=expense_id).delete()
    db.commit()

    return None
