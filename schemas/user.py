from pydantic import BaseModel,  EmailStr 
from typing import Optional
class UserCreate(BaseModel):
    name: str
    address: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id : int
    name: str
    address: Optional[str]

    model_config = {
        "from_attributes": True
    }