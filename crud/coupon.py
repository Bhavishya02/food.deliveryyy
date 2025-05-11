from sqlalchemy.orm import Session
from app.models import coupon as coupon_models
from app.schemas import coupon as coupon_schemas

def create_coupon(db: Session, coupon: coupon_schemas.CouponCreate):
    db_coupon = coupon_models.Coupon(
        code=coupon.code,
        discount=coupon.discount,
        expiration_date=coupon.expiration_date
    )
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

def get_coupon_by_code(db: Session, coupon_code: str):
    return db.query(coupon_models.Coupon).filter(coupon_models.Coupon.code == coupon_code).first()

def update_coupon(db: Session, coupon_code: str, coupon: coupon_schemas.CouponUpdate):
    db_coupon = db.query(coupon_models.Coupon).filter(coupon_models.Coupon.code == coupon_code).first()
    if db_coupon:
        db_coupon.discount = coupon.discount
        db_coupon.expiration_date = coupon.expiration_date
        db.commit()
        db.refresh(db_coupon)
    return db_coupon

def apply_coupon_to_order(db: Session, order_id: int, coupon: coupon_models.Coupon):
    db_order = db.query(coupon_models.Order).filter(coupon_models.Order.id == order_id).first()
    if db_order:
        db_order.total_price -= (db_order.total_price * coupon.discount / 100)  
        db.commit()
        db.refresh(db_order)
    return db_order
