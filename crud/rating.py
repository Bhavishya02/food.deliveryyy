from sqlalchemy.orm import Session
from app.models.rating import Rating

def create_rating(db: Session, rating_data):
    db_rating = Rating(**rating_data.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings_for_rider(db: Session, rider_id: int):
    return db.query(Rating).filter(Rating.rider_id == rider_id).all()