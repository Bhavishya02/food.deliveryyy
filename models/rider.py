from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True) 
    password = Column(String, nullable=False)
    current_latitude = Column(Float, nullable=False)
    current_longitude = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    current_load = Column(Integer, default=0)
    stars = Column(Float, default=5.0)
