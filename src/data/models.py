import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import JSON

from data.db import Base


class CarListing(Base):
    """
    Representation of a cryptocurrency ticker.
    """
    __tablename__ = "cars_ml_listing"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, unique=True)
    listing_url = Column(String)
    _avg_market_price = Column(String)
    body_type = Column(String)
    carfax_no_accidents = Column(Integer)
    carfax_one_owner = Column(Integer)
    cylinder = Column(Integer)
    description = Column(String)
    doors = Column(Integer)
    drivetrain = Column(String)
    engine = Column(String)
    fuel_city = Column(Float)
    fuel_combined = Column(Float)
    fuel_highway = Column(Float)
    fuel_type = Column(String)
    is_new = Column(Integer)
    is_private = Column(Integer)
    kms = Column(Integer)
    make = Column(String)
    model = Column(String)
    num_photos = Column(Integer)
    options = Column(JSON)
    price = Column(Integer)
    status = Column(String)
    transmission = Column(String)
    year = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
