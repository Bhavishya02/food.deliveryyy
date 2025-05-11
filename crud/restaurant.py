from sqlalchemy.orm import Session
from app.models import restaurant as restaurant_models
from app.schemas import restaurant as restaurant_schemas

def create_restaurant(db: Session, restaurant: restaurant_schemas.RestaurantCreate):
    db_restaurant = restaurant_models.Restaurant(
        name=restaurant.name,
        email=restaurant.email,
        address=restaurant.address,
        cuisine=restaurant.cuisine,
        location=restaurant.location,
        avg_delivery_time=restaurant.avg_delivery_time,
        password=restaurant.password
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def get_restaurant_by_id(db: Session, restaurant_id: int):
    return db.query(restaurant_models.Restaurant).filter(restaurant_models.Restaurant.id == restaurant_id).first()

def get_menu_items_by_restaurant(db: Session, restaurant_id: int):
    return db.query(restaurant_models.MenuItem).filter(restaurant_models.MenuItem.restaurant_id == restaurant_id).all()

def update_restaurant(db: Session, restaurant_id: int, restaurant: restaurant_schemas.RestaurantBase):
    db_restaurant = db.query(restaurant_models.Restaurant).filter(restaurant_models.Restaurant.id == restaurant_id).first()
    if db_restaurant:
        db_restaurant.name = restaurant.name
        db_restaurant.email = restaurant.email
        db_restaurant.address = restaurant.address
        db_restaurant.cuisine = restaurant.cuisine
        db_restaurant.location = restaurant.location
        db_restaurant.avg_delivery_time = restaurant.avg_delivery_time
        db.commit()
        db.refresh(db_restaurant)
    return db_restaurant
