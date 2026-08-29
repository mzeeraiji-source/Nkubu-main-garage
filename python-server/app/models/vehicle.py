"""
Vehicle data models
"""

from pydantic import BaseModel
from typing import Optional


class VehicleCreate(BaseModel):
    """Create new vehicle"""
    customer_id: str
    year: int
    make: str
    model: str
    trim: Optional[str] = None
    vin: str
    color: Optional[str] = None
    mileage: int
    engine_type: Optional[str] = None
    license_plate: str


class VehicleResponse(BaseModel):
    """Vehicle details response"""
    id: str
    customer_id: str
    year: int
    make: str
    model: str
    vin: str
    mileage: int
    license_plate: str
