from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import restaurant as restaurant_crud
from app.schemas import restaurant as restaurant_schemas
from app.dependencies import get_db

router = APIRouter()

@router.post("/register", response_model=restaurant_schemas.RestaurantOut)
def register_restaurant(restaurant: restaurant_schemas.RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = restaurant_crud.create_restaurant(db, restaurant)
    return new_restaurant

@router.get("/{restaurant_id}", response_model=restaurant_schemas.RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = restaurant_crud.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return restaurant

@router.get("/{restaurant_id}/menu")
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    menu_items = restaurant_crud.get_menu_items_by_restaurant(db, restaurant_id)
    if not menu_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found for this restaurant")
    return menu_items

@router.put("/{restaurant_id}", response_model=restaurant_schemas.RestaurantOut)
def update_restaurant(restaurant_id: int, restaurant: restaurant_schemas.RestaurantBase, db: Session = Depends(get_db)):
    updated_restaurant = restaurant_crud.update_restaurant(db, restaurant_id, restaurant)
    if not updated_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return updated_restaurant
