from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import Base
from datetime import datetime

class Coupon(Base):
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  
    discount_percent = Column(Float)
    active = Column(Boolean, default=True)
    expiry_date = Column(DateTime) 
    description = Column(String, nullable=True) 
    
    
    def is_expired(self):
        if self.expiry_date:
            return datetime.utcnow() > self.expiry_date
        return False  
