from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("riders.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Float)