from sqlalchemy import Column, String, Float
from ..database import Base
from pydantic import BaseModel

class StowLocation(Base):
    __tablename__ = "locations"

    location_id = Column(String, primary_key=True, index=True)
    available_length_cm = Column(Float, nullable=False)
    available_width_cm = Column(Float, nullable=False)
    available_height_cm = Column(Float, nullable=False)
    weight_capacity_kg = Column(Float, nullable=False)
    occupied_volume_cm3 = Column(Float, default=0.0)
    status = Column(String, default="AVAILABLE")

class LocationResponse(BaseModel):
    location_id: str
    available_length_cm: float
    available_width_cm: float
    available_height_cm: float
    weight_capacity_kg: float
    occupied_volume_cm3: float
    status: str

    class Config:
        from_attributes = True
