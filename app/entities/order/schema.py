from decimal import Decimal

from pydantic import BaseModel


class OrderCreate(BaseModel):

    id: int
    user_id: int
    product_id: int
    amount: Decimal
    status: str


class OrderResponse(OrderCreate):
    pass