from sqlalchemy.orm import Session
from app.models.menu import Menu

def get_menu_by_restaurant(db: Session, restaurant_id: int):
    return db.query(Menu).filter(Menu.restaurant_id == restaurant_id).all()