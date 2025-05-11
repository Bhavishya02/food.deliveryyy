from pydantic import BaseModel
from typing import List

class OrderItemCreate(BaseModel):
    item_name: str
    quantity: int

class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    items: List[OrderItemCreate]
    total_price: float

class OrderItemOut(OrderItemCreate):
    id: int
    model_config = {
        "from_attributes": True
    }
class OrderOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    total_price: float
    status: str
    items: List[OrderItemOut]

    model_config = {
        "from_attributes": True
    }