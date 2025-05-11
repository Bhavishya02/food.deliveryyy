from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models import order as models, restaurant as restaurant_models, menu as menu_models, rider as rider_models
from app.crud.rider import get_nearest_rider
from app.schemas import order as schemas
from app.models import Order, OrderItem
from app.schemas.rider import Location

from app.schemas import rider as rider_schemas

def create_order(db: Session, order: schemas.OrderCreate):
    restaurant = db.query(restaurant_models.Restaurant).filter_by(id=order.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    for item_id in order.menu_item_ids:
        item = db.query(menu_models.Menu).filter_by(id=item_id, restaurant_id=order.restaurant_id).first()
        if not item:
            raise HTTPException(status_code=400, detail=f"Menu item {item_id} is not valid for this restaurant")

    new_order = models.Order(
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        status="pending",
        delivery_address=order.delivery_address,
    )
    db.add(new_order)
    db.flush() 

    for item_id in order.menu_item_ids:
        db.add(models.OrderItem(order_id=new_order.id, menu_item_id=item_id))

    db.commit()
    db.refresh(new_order)
    return new_order

def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter_by(user_id=user_id).all()

def get_orders_by_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Order).filter_by(restaurant_id=restaurant_id).all()

def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(models.Order).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    return order

def assign_rider_to_order(db: Session, order_id: int, location: rider_schemas.Location):
    order = db.query(models.Order).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    rider = get_nearest_rider(db, location)
    if not rider:
        raise HTTPException(status_code=404, detail="No available rider found")
    order.rider_id = rider.id
    db.commit()
    return order
