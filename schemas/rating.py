from pydantic import BaseModel
from typing import Optional

class RatingCreate(BaseModel):
    rider_id: int
    user_id: int
    score: int
    comment: Optional[str] = None


class RatingOut(RatingCreate):
    id: int
    model_config = {
        "from_attributes": True
    }