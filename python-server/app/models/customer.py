"""
Customer data models
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerCreate(BaseModel):
    """Create new customer"""
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    """Customer details response"""
    id: str
    email: str
    first_name: str
    last_name: str
    phone: str
    total_bookings: int = 0
    loyalty_points: int = 0
