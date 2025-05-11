from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import rider as rider_crud
from app.schemas import rider as rider_schemas
from app.dependencies import get_db
from app.models import rider as rider_models

router = APIRouter()


@router.post("/register", response_model=rider_schemas.RiderOut)
def register_rider(rider: rider_schemas.RiderCreate, db: Session = Depends(get_db)):
    new_rider = rider_crud.create_rider(db, rider)
    return new_rider


@router.post("/login")
def login_rider(login_data: rider_schemas.RiderLogin, db: Session = Depends(get_db)):
    rider = db.query(rider_models.Rider).filter_by(email=login_data.email).first()
    if rider is None or rider.password != login_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {"message": "Login successful", "rider_id": rider.id}


@router.get("/nearest", response_model=rider_schemas.RiderOut)
def find_nearest_rider(location: rider_schemas.Location, db: Session = Depends(get_db)):
    rider = rider_crud.get_nearest_rider(db, location)
    if not rider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No available riders found")
    return rider


@router.get("/{rider_id}", response_model=rider_schemas.RiderOut)
def get_rider(rider_id: int, db: Session = Depends(get_db)):
    rider = rider_crud.get_rider_by_id(db, rider_id)
    if not rider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rider not found")
    return rider


@router.put("/{rider_id}/availability", response_model=rider_schemas.RiderOut)
def update_rider_availability(rider_id: int, is_available: bool, db: Session = Depends(get_db)):
    rider = rider_crud.update_availability(db, rider_id, is_available)
    if not rider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rider not found")
    return rider
