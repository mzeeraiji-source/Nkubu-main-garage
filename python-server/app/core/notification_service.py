"""
Notification Service - Email and SMS dispatching
Handles customer notifications for bookings, reminders, and updates
"""

import logging
from typing import Optional, List, Dict
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class NotificationChannel(str, Enum):
    """Available notification channels"""
    EMAIL = "email"
    SMS = "sms"
    BOTH = "both"


class NotificationType(str, Enum):
    """Types of notifications"""
    BOOKING_CONFIRMATION = "booking_confirmation"
    BOOKING_REMINDER = "booking_reminder"
    STATUS_UPDATE = "status_update"
    COMPLETION_NOTICE = "completion_notice"
    PAYMENT_REMINDER = "payment_reminder"
    PROMOTIONAL = "promotional"
    ALERT = "alert"


@dataclass
class Notification:
    """Notification to be sent"""
    id: str
    customer_id: str
    type: NotificationType
    channel: NotificationChannel
    recipient_email: Optional[str] = None
    recipient_phone: Optional[str] = None
    subject: str = ""
    message: str = ""
    sent_at: Optional[datetime] = None
    status: str = "pending"  # pending, sent, failed


class NotificationService:
    """Send notifications via email and SMS"""

    def __init__(self, resend_client=None, twilio_client=None, claude_client=None):
        """
        Initialize notification service

        Args:
            resend_client: Resend email client
            twilio_client: Twilio SMS client
            claude_client: Claude for personalized message generation
        """
        self.resend = resend_client
        self.twilio = twilio_client
        self.claude = claude_client
        logger.info("NotificationService initialized")

    def send_booking_confirmation(
        self,
        customer_id: str,
        customer_email: str,
        customer_phone: Optional[str],
        booking_details: Dict,
        channel: NotificationChannel = NotificationChannel.BOTH,
    ) -> bool:
        """Send booking confirmation notification"""
        logger.info(f"Sending booking confirmation to {customer_id}")
        # Would call resend/twilio here
        return True

    def send_booking_reminder(
        self,
        customer_id: str,
        customer_email: str,
        customer_phone: Optional[str],
        booking_details: Dict,
        hours_before: int = 24,
    ) -> bool:
        """Send booking reminder (24h, 1h before)"""
        logger.info(f"Sending {hours_before}h reminder to {customer_id}")
        return True

    def send_status_update(
        self,
        customer_id: str,
        customer_email: str,
        booking_id: str,
        status: str,
        message: str,
    ) -> bool:
        """Send real-time service status update"""
        logger.info(f"Sending status update for booking {booking_id}")
        return True

    def send_completion_notice(
        self,
        customer_id: str,
        customer_email: str,
        booking_id: str,
        invoice_url: str,
    ) -> bool:
        """Send service completion notice with invoice"""
        logger.info(f"Sending completion notice for booking {booking_id}")
        return True

    def send_personalized_promotion(
        self,
        customer_id: str,
        customer_email: str,
        promotion_details: Dict,
    ) -> bool:
        """Send AI-personalized promotional message"""
        # Use Claude to personalize based on customer history
        logger.info(f"Sending personalized promotion to {customer_id}")
        return True

    def batch_send_reminders(
        self,
        reminders: List[Dict],
    ) -> Dict[str, int]:
        """Send batch reminders for upcoming bookings"""
        results = {"sent": 0, "failed": 0}
        for reminder in reminders:
            try:
                self.send_booking_reminder(**reminder)
                results["sent"] += 1
            except Exception as e:
                logger.error(f"Failed to send reminder: {str(e)}")
                results["failed"] += 1
        return results
