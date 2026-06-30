from sqlalchemy import Column, Integer, Float, String, ForeignKey
from database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    days = Column(Integer)

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    name = Column(String)
    lat = Column(Float)
    lng = Column(Float)