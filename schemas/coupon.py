from pydantic import BaseModel
from typing import Optional
from app.schemas import order as order_schemas

class CouponCreate(BaseModel):
    code: str
    discount_percentage: float
    expiry_date: str 
    description: Optional[str] = None  

class CouponUpdate(BaseModel):
    discount_percentage: Optional[float] = None
    expiry_date: Optional[str] = None 
    description: Optional[str] = None

class CouponOut(CouponCreate):
    id: int 

    model_config = {
        "from_attributes": True
    }

class OrderOut(order_schemas.OrderOut): 
    coupon_code: str 

    model_config = {
        "from_attributes": True
    }