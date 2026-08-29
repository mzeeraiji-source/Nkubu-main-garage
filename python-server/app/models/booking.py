"""
Booking data models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ServiceCategory(str, Enum):
    OIL_CHANGE = "oil_change"
    TIRE_SERVICE = "tire_service"
    BRAKE_SERVICE = "brake_service"
    DIAGNOSTIC = "diagnostic"
    TRANSMISSION = "transmission"
    ENGINE_REPAIR = "engine_repair"
    INSPECTION = "inspection"


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BookingRequest(BaseModel):
    """Request to create a new booking"""
    customer_id: str
    vehicle_id: str
    service_category: ServiceCategory
    preferred_date: datetime
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    """Response with booking details"""
    id: str
    customer_id: str
    vehicle_id: str
    bay_id: str
    service_category: ServiceCategory
    start_time: datetime
    duration_minutes: int
    status: BookingStatus
    created_at: datetime


class AvailabilityRequest(BaseModel):
    """Request for available time slots"""
    service_category: ServiceCategory
    date: datetime
    vehicle_id: str


class AvailabilitySlotResponse(BaseModel):
    """Available time slot"""
    start_time: datetime
    end_time: datetime
    bay_id: str
    bay_name: str
    available: bool = True
