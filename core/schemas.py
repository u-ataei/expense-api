from pydantic import BaseModel, Field


class ExpenseBaseSchema(BaseModel):
    description: str = Field(..., min_length=6, max_length=100)
    amount: float = Field(..., ge=0)


class ExpenseCreateSchema(ExpenseBaseSchema):
    id: int = Field(..., ge=0)


class ExpenseUpdateSchema(ExpenseBaseSchema):
    pass
