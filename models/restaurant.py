from sqlalchemy import Column, Integer, String
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    location = Column(String, nullable=False)
    avg_delivery_time = Column(Integer, nullable=False)
