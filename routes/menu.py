from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import menu as menu_crud
from app.schemas import menu as menu_schemas  
from app.dependencies import get_db

router = APIRouter()

@router.get("/{restaurant_id}", response_model=list[menu_schemas.MenuOut])
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    menu_items = menu_crud.get_menu_by_restaurant(db, restaurant_id)
    
    if not menu_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No menu items found for this restaurant"
        )
    
    return menu_items
