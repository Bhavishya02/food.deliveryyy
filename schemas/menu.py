from pydantic import BaseModel

class MenuOut(BaseModel):
    id: int
    name: str
    price: float
    restaurant_id: int

    model_config = {
        "from_attributes": True
    }