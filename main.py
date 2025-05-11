import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends
from app.database import Base, engine, Session, get_db  
from app import models
from app.routes import user, restaurant, menu, order, rider, coupon, rating
from app.schemas.rider import Location  
import sqlite3
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Delivery App")

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(restaurant.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(rider.router, prefix="/riders", tags=["Riders"])
app.include_router(coupon.router, prefix="/coupons", tags=["Coupons"])
app.include_router(rating.router, prefix="/ratings", tags=["Ratings"])

@app.post("/assign_rider_to_order/{order_id}")
def assign_rider_to_order(order_id: int, location: Location, db: Session = Depends(get_db)):
    from app.crud import assign_rider_to_order as assign_rider 

    return assign_rider(db=db, order_id=order_id, location=location)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


conn = sqlite3.connect("food_delivery.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
