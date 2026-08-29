"""
Booking Engine - Core availability & scheduling algorithm
Handles bay availability, buffer times, holiday overrides, and conflict detection
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ServiceCategory(str, Enum):
    """Service types and their typical durations"""
    OIL_CHANGE = "oil_change"  # 30 min
    TIRE_SERVICE = "tire_service"  # 45 min
    BRAKE_SERVICE = "brake_service"  # 60 min
    DIAGNOSTIC = "diagnostic"  # 60 min
    TRANSMISSION = "transmission"  # 180 min
    ENGINE_REPAIR = "engine_repair"  # 240 min
    INSPECTION = "inspection"  # 30 min
    CUSTOM = "custom"  # Variable


SERVICE_DURATIONS = {
    ServiceCategory.OIL_CHANGE: 30,
    ServiceCategory.TIRE_SERVICE: 45,
    ServiceCategory.BRAKE_SERVICE: 60,
    ServiceCategory.DIAGNOSTIC: 60,
    ServiceCategory.TRANSMISSION: 180,
    ServiceCategory.ENGINE_REPAIR: 240,
    ServiceCategory.INSPECTION: 30,
    ServiceCategory.CUSTOM: 120,  # Default for custom
}


@dataclass
class Bay:
    """Represents a service bay/workstation"""
    id: str
    name: str
    specialization: str  # e.g., "brakes", "transmission", "general"
    is_active: bool = True


@dataclass
class Booking:
    """Represents a customer booking"""
    id: str
    customer_id: str
    vehicle_id: str
    bay_id: str
    service_category: ServiceCategory
    start_time: datetime
    duration_minutes: int
    status: str  # pending, confirmed, in_progress, completed, cancelled
    notes: Optional[str] = None


@dataclass
class AvailabilitySlot:
    """Represents an available time slot"""
    start_time: datetime
    end_time: datetime
    bay_id: str
    bay_name: str
    available_capacity: int


class BookingEngine:
    """
    Core booking availability engine
    Manages bay scheduling, conflict detection, and time slot generation
    """

    def __init__(
        self,
        buffer_minutes: int = 30,
        max_concurrent_bookings_per_bay: int = 1,
        booking_advance_days: int = 90,
        holiday_closures: Optional[List[str]] = None,
    ):
        """
        Initialize booking engine with business rules

        Args:
            buffer_minutes: Minimum time between bookings (cleanup, admin)
            max_concurrent_bookings_per_bay: Max simultaneous bookings per bay
            booking_advance_days: How many days in advance can customers book
            holiday_closures: List of ISO date strings when garage is closed
        """
        self.buffer_minutes = buffer_minutes
        self.max_concurrent_bookings_per_bay = max_concurrent_bookings_per_bay
        self.booking_advance_days = booking_advance_days
        self.holiday_closures = set(holiday_closures or [])

        logger.info(
            f"BookingEngine initialized: "
            f"buffer={buffer_minutes}min, "
            f"concurrency={max_concurrent_bookings_per_bay}, "
            f"advance={booking_advance_days}days"
        )

    def get_available_slots(
        self,
        service_category: ServiceCategory,
        date: datetime,
        bays: List[Bay],
        existing_bookings: List[Booking],
        working_hours: Tuple[int, int] = (9, 17),  # 9 AM - 5 PM
    ) -> List[AvailabilitySlot]:
        """
        Get all available time slots for a given service on a specific date

        Args:
            service_category: Type of service requested
            date: Requested date
            bays: List of available bays
            existing_bookings: List of existing bookings to check conflicts
            working_hours: Tuple of (open_hour, close_hour) in 24-hour format

        Returns:
            List of AvailabilitySlot objects sorted by start time
        """
        # Validate date
        if not self._is_bookable_date(date):
            logger.warning(f"Date {date} is not bookable (holiday or past date)")
            return []

        duration = SERVICE_DURATIONS.get(service_category, SERVICE_DURATIONS[ServiceCategory.CUSTOM])
        open_hour, close_hour = working_hours

        slots = []

        for bay in bays:
            if not bay.is_active:
                continue

            # Get all occupied time ranges for this bay on this date
            occupied_ranges = self._get_occupied_times(bay.id, date, existing_bookings)

            # Generate available slots by finding gaps
            bay_slots = self._generate_slots(
                bay=bay,
                date=date,
                occupied_ranges=occupied_ranges,
                service_duration=duration,
                open_hour=open_hour,
                close_hour=close_hour,
            )

            slots.extend(bay_slots)

        # Sort by start time
        slots.sort(key=lambda s: s.start_time)
        logger.info(f"Found {len(slots)} available slots for {service_category} on {date.date()}")

        return slots

    def _is_bookable_date(self, date: datetime) -> bool:
        """Check if date is valid for booking (not past, not holiday)"""
        now = datetime.now()

        # Check if date is in the past
        if date.date() < now.date():
            return False

        # Check if date is beyond advance booking window
        if (date.date() - now.date()).days > self.booking_advance_days:
            return False

        # Check if date is a holiday closure
        if date.date().isoformat() in self.holiday_closures:
            return False

        return True

    def _get_occupied_times(
        self,
        bay_id: str,
        date: datetime,
        bookings: List[Booking],
    ) -> List[Tuple[datetime, datetime]]:
        """
        Get all occupied time ranges for a bay on a specific date
        Includes buffer time before/after each booking
        """
        occupied = []

        for booking in bookings:
            if booking.bay_id != bay_id or booking.status == "cancelled":
                continue

            booking_date = booking.start_time.date()
            if booking_date != date.date():
                continue

            # Include buffer time
            start_with_buffer = booking.start_time - timedelta(minutes=self.buffer_minutes)
            end_with_buffer = booking.start_time + timedelta(
                minutes=booking.duration_minutes + self.buffer_minutes
            )

            occupied.append((start_with_buffer, end_with_buffer))

        # Merge overlapping ranges
        occupied.sort(key=lambda x: x[0])
        merged = []

        for start, end in occupied:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        return merged

    def _generate_slots(
        self,
        bay: Bay,
        date: datetime,
        occupied_ranges: List[Tuple[datetime, datetime]],
        service_duration: int,
        open_hour: int,
        close_hour: int,
    ) -> List[AvailabilitySlot]:
        """Generate available time slots for a bay"""
        slots = []

        # Start of business day
        business_start = date.replace(hour=open_hour, minute=0, second=0, microsecond=0)
        business_end = date.replace(hour=close_hour, minute=0, second=0, microsecond=0)

        current = business_start

        while current + timedelta(minutes=service_duration) <= business_end:
            slot_end = current + timedelta(minutes=service_duration)

            # Check if this slot conflicts with any occupied time
            is_available = True
            for occ_start, occ_end in occupied_ranges:
                if (current < occ_end) and (slot_end > occ_start):
                    is_available = False
                    break

            if is_available:
                slots.append(
                    AvailabilitySlot(
                        start_time=current,
                        end_time=slot_end,
                        bay_id=bay.id,
                        bay_name=bay.name,
                        available_capacity=self.max_concurrent_bookings_per_bay,
                    )
                )

            # Move to next 30-minute increment
            current += timedelta(minutes=30)

        return slots

    def check_availability(
        self,
        bay_id: str,
        start_time: datetime,
        duration_minutes: int,
        existing_bookings: List[Booking],
    ) -> bool:
        """Check if a specific time slot is available"""
        end_time = start_time + timedelta(minutes=duration_minutes)

        for booking in existing_bookings:
            if booking.bay_id != bay_id or booking.status == "cancelled":
                continue

            booking_end = booking.start_time + timedelta(minutes=booking.duration_minutes)

            # Check for conflicts with buffers
            buffer = timedelta(minutes=self.buffer_minutes)

            if (start_time - buffer < booking_end) and (end_time + buffer > booking.start_time):
                logger.warning(
                    f"Conflict detected for bay {bay_id}: "
                    f"requested {start_time}-{end_time}, "
                    f"existing {booking.start_time}-{booking_end}"
                )
                return False

        return True

    def create_booking(
        self,
        customer_id: str,
        vehicle_id: str,
        bay_id: str,
        service_category: ServiceCategory,
        start_time: datetime,
        existing_bookings: List[Booking],
        booking_id: Optional[str] = None,
    ) -> Optional[Booking]:
        """
        Create a new booking if availability allows

        Returns:
            Booking object if successful, None if conflict
        """
        duration = SERVICE_DURATIONS.get(service_category, SERVICE_DURATIONS[ServiceCategory.CUSTOM])

        if not self.check_availability(bay_id, start_time, duration, existing_bookings):
            logger.error(f"Cannot create booking: time slot not available")
            return None

        booking = Booking(
            id=booking_id or f"booking_{int(datetime.now().timestamp())}",
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            bay_id=bay_id,
            service_category=service_category,
            start_time=start_time,
            duration_minutes=duration,
            status="confirmed",
        )

        logger.info(
            f"✅ Booking created: {booking.id} for {service_category} "
            f"at {start_time} in bay {bay_id}"
        )

        return booking

    def reschedule_booking(
        self,
        booking: Booking,
        new_start_time: datetime,
        existing_bookings: List[Booking],
    ) -> bool:
        """Reschedule an existing booking to a new time"""
        # Remove current booking from conflicts check
        other_bookings = [b for b in existing_bookings if b.id != booking.id]

        if not self.check_availability(
            booking.bay_id,
            new_start_time,
            booking.duration_minutes,
            other_bookings,
        ):
            logger.error(f"Cannot reschedule booking {booking.id}: new time not available")
            return False

        booking.start_time = new_start_time
        logger.info(f"✅ Booking {booking.id} rescheduled to {new_start_time}")

        return True

    def cancel_booking(self, booking: Booking) -> bool:
        """Cancel an existing booking"""
        booking.status = "cancelled"
        logger.info(f"✅ Booking {booking.id} cancelled")
        return True
