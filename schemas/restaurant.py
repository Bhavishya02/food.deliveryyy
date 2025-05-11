from pydantic import BaseModel, EmailStr

class Location(BaseModel):
    latitude: float
    longitude: float

class RestaurantBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    cuisine: str
    location: Location
    avg_delivery_time: int

class RestaurantCreate(RestaurantBase):
    password: str

class RestaurantLogin(BaseModel):
    email: EmailStr
    password: str

class RestaurantOut(RestaurantBase):
    id: int

    model_config = {
        "from_attributes": True
    }