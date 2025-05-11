from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.rating import RatingCreate, RatingOut
from app.crud import rating as rating_crud
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=RatingOut)
def rate_rider(rating: RatingCreate, db: Session = Depends(get_db)):
    try:
        return rating_crud.create_rating(db, rating)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/rider/{rider_id}", response_model=List[RatingOut])
def get_rider_ratings(rider_id: int, db: Session = Depends(get_db)):
    return rating_crud.get_ratings_for_rider(db, rider_id)
