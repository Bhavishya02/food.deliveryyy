from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import order as order_crud, restaurant as restaurant_crud, rider as rider_crud
from app.schemas import order as order_schemas
from app.dependencies import get_db
from app.models import Order, OrderItem
from app.schemas.rider import Location
router = APIRouter()

@router.post("/create", response_model=order_schemas.OrderOut)
def create_order(order: order_schemas.OrderCreate, db: Session = Depends(get_db)):
    restaurant = restaurant_crud.get_restaurant_by_id(db, order.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    for item in order.items:
        menu_item = restaurant_crud.get_menu_item_by_id(db, item.menu_item_id)
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item {item.menu_item_id} not found")

    new_order = order_crud.create_order(db, order)
    return new_order

@router.get("/{order_id}", response_model=order_schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.get("/user/{user_id}", response_model=list[order_schemas.OrderOut])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = order_crud.get_orders_by_user(db, user_id)
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this user")
    return orders

@router.get("/restaurant/{restaurant_id}", response_model=list[order_schemas.OrderOut])
def get_orders_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    orders = order_crud.get_orders_by_restaurant(db, restaurant_id)
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this restaurant")
    return orders

@router.put("/{order_id}/status", response_model=order_schemas.OrderOut)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = order_crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    updated_order = order_crud.update_order_status(db, order_id, status)
    return updated_order

@router.put("/{order_id}/assign_rider", response_model=order_schemas.OrderOut)
def assign_rider_to_order(order_id: int, location: Location, db: Session = Depends(get_db)):
    order = order_crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    nearest_rider = rider_crud.get_nearest_rider(db, location)
    if not nearest_rider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No available riders found")
    
    updated_order = order_crud.assign_rider(db, order_id, nearest_rider.id)
    return updated_order