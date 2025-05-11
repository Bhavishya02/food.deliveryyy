from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import coupon as coupon_crud
from app.schemas import coupon as coupon_schemas
from app.dependencies import get_db

router = APIRouter()

@router.post("/create", response_model=coupon_schemas.CouponOut)
def create_coupon(coupon: coupon_schemas.CouponCreate, db: Session = Depends(get_db)):
    new_coupon = coupon_crud.create_coupon(db, coupon)
    return new_coupon

@router.get("/{coupon_code}", response_model=coupon_schemas.CouponOut)
def get_coupon(coupon_code: str, db: Session = Depends(get_db)):
    coupon = coupon_crud.get_coupon_by_code(db, coupon_code)
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    return coupon

@router.put("/{coupon_code}", response_model=coupon_schemas.CouponOut)
def update_coupon(coupon_code: str, coupon: coupon_schemas.CouponUpdate, db: Session = Depends(get_db)):
    updated_coupon = coupon_crud.update_coupon(db, coupon_code, coupon)
    if not updated_coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    return updated_coupon

@router.put("/{order_id}/apply_coupon", response_model=coupon_schemas.OrderOut)
def apply_coupon_to_order(order_id: int, coupon_code: str, db: Session = Depends(get_db)):
    coupon = coupon_crud.get_coupon_by_code(db, coupon_code)
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    
    order = coupon_crud.apply_coupon_to_order(db, order_id, coupon)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found or coupon application failed")
    
    return order
