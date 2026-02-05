from fastapi import FastAPI, Query, HTTPException, status, Path, Body
from typing import Dict
from .schemas import ExpenseCreateSchema, ExpenseUpdateSchema, ExpenseResponseSchema

app = FastAPI()


expenses_db: Dict[int, Dict] = {
    0: {"id": 0, "description": "Cinema", "amount": 5.00},
    1: {"id": 1, "description": "Hotel", "amount": 120.00}
}


@app.get("/expenses", status_code=status.HTTP_200_OK)
def retrieve_expenses(id: int | None = Query(None)):
    if id is not None:
        if id in expenses_db:
            return expenses_db[id]
        raise HTTPException(
            status_code=404, detail="Expense not found")
    return expenses_db


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(create_expense: ExpenseCreateSchema = Body(...)):
    if create_expense.id in expenses_db:
        raise HTTPException(
            status_code=409, detail=f"Expense with this ID {create_expense.id} already exists.")

    expenses_db[create_expense.id] = {
        "id": create_expense.id,
        "description": create_expense.description,
        "amount": create_expense.amount
    }

    return expenses_db[create_expense.id]


@app.put("/expenses/{id}", status_code=status.HTTP_200_OK)
def update_expense(id: int = Path(...), update_expense: ExpenseUpdateSchema = Body(...)):
    if not id in expenses_db:
        raise HTTPException(
            status_code=404, detail="Expense not found")

    expenses_db[id]["description"] = update_expense.description
    expenses_db[id]["amount"] = update_expense.amount

    return expenses_db[id]


@app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int = Path(...)):
    if not id in expenses_db:
        raise HTTPException(
            status_code=404, detail="Expense not found")

    del expenses_db[id]

    return None
