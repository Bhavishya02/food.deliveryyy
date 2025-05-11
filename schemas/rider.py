from pydantic import BaseModel, EmailStr

class Location(BaseModel):
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

class RiderCreate(BaseModel):
    name: str
    location: str 
    email: EmailStr
    availability: bool
    password: str

    class Config:
        from_attributes = True

class RiderOut(BaseModel):
    id: int
    name: str
    location: Location
    stars: float
    availability: bool

    class Config:
        from_attributes = True

class RiderLogin(BaseModel):
    email: EmailStr
    password: str