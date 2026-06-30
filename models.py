from sqlalchemy import Column, Integer, String
from database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    days = Column(Integer)