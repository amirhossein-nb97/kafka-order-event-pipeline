from fastapi import APIRouter, status

from app.entities.order.schema import (
    OrderCreate,
    OrderResponse,
)

from kafka.producer import send_order


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(order: OrderCreate):

    order_data = order.model_dump()

    send_order(order_data)

    return order