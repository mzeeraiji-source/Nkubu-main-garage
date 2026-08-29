"""
Pricing Engine - Dynamic pricing calculation
Handles service rates, parts markup, discounts, and invoice generation
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class DiscountType(str, Enum):
    """Types of discounts available"""
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    LOYALTY = "loyalty"
    SEASONAL = "seasonal"
    BULK = "bulk"


@dataclass
class PricingRule:
    """Represents a pricing rule or discount"""
    id: str
    name: str
    description: str
    discount_type: DiscountType
    discount_value: float
    min_amount: Optional[float] = None  # Minimum order amount to apply
    max_discount: Optional[float] = None  # Maximum discount cap
    active: bool = True


@dataclass
class LineItem:
    """Represents a line item in an invoice"""
    id: str
    description: str
    quantity: float
    unit_price: float
    total: float  # quantity * unit_price


@dataclass
class Invoice:
    """Complete invoice with all line items and totals"""
    id: str
    booking_id: str
    customer_id: str
    line_items: List[LineItem]
    subtotal: float
    tax_amount: float
    discounts: List[Dict]
    total: float
    created_at: datetime
    due_date: datetime
    status: str  # draft, sent, paid, overdue


class PricingEngine:
    """
    Dynamic pricing engine for service calculations
    Handles hourly rates, parts markup, discounts, and tax
    """

    def __init__(
        self,
        base_service_hour_rate: float = 50.0,
        parts_markup_percentage: float = 20.0,
        tax_rate: float = 0.1,  # 10% tax
    ):
        """
        Initialize pricing engine with base rates

        Args:
            base_service_hour_rate: Default hourly labor rate
            parts_markup_percentage: Markup on parts cost
            tax_rate: Sales tax rate (decimal, e.g., 0.1 for 10%)
        """
        self.base_service_hour_rate = base_service_hour_rate
        self.parts_markup_percentage = parts_markup_percentage
        self.tax_rate = tax_rate

        logger.info(
            f"PricingEngine initialized: "
            f"hourly_rate=${base_service_hour_rate}, "
            f"parts_markup={parts_markup_percentage}%, "
            f"tax_rate={tax_rate*100}%"
        )

    def calculate_service_labor_cost(
        self,
        duration_minutes: int,
        hourly_rate: Optional[float] = None,
        specialty_multiplier: float = 1.0,
    ) -> float:
        """
        Calculate labor cost based on service duration

        Args:
            duration_minutes: Service duration in minutes
            hourly_rate: Override base hourly rate (optional)
            specialty_multiplier: Multiplier for specialized services (e.g., 1.5 for transmission work)

        Returns:
            Total labor cost
        """
        rate = hourly_rate or self.base_service_hour_rate
        hours = duration_minutes / 60.0

        labor_cost = rate * hours * specialty_multiplier

        logger.debug(
            f"Labor cost calculated: {duration_minutes}min @ "
            f"${rate}/hr * {specialty_multiplier}x = ${labor_cost:.2f}"
        )

        return labor_cost

    def calculate_parts_cost_with_markup(
        self,
        parts_cost: float,
        markup_percentage: Optional[float] = None,
    ) -> Dict[str, float]:
        """
        Calculate parts cost with markup

        Args:
            parts_cost: Cost of parts to the garage
            markup_percentage: Override default markup (optional)

        Returns:
            Dict with cost, markup, and total
        """
        markup = markup_percentage or self.parts_markup_percentage
        markup_amount = parts_cost * (markup / 100.0)
        total = parts_cost + markup_amount

        return {
            "cost": parts_cost,
            "markup_percentage": markup,
            "markup_amount": markup_amount,
            "selling_price": total,
        }

    def apply_discount(
        self,
        amount: float,
        discount_rule: PricingRule,
    ) -> Dict[str, float]:
        """
        Apply a discount rule to an amount

        Args:
            amount: Amount to discount
            discount_rule: PricingRule with discount configuration

        Returns:
            Dict with original amount, discount amount, and final amount
        """
        # Check minimum amount requirement
        if discount_rule.min_amount and amount < discount_rule.min_amount:
            logger.debug(
                f"Discount {discount_rule.id} not applied: "
                f"${amount} < minimum ${discount_rule.min_amount}"
            )
            return {
                "original_amount": amount,
                "discount_amount": 0.0,
                "final_amount": amount,
                "discount_applied": False,
            }

        # Calculate discount
        if discount_rule.discount_type == DiscountType.PERCENTAGE:
            discount_amount = amount * (discount_rule.discount_value / 100.0)
        elif discount_rule.discount_type == DiscountType.FIXED_AMOUNT:
            discount_amount = discount_rule.discount_value
        else:
            # Handle other discount types (loyalty, seasonal, bulk)
            discount_amount = discount_rule.discount_value

        # Apply maximum discount cap if set
        if discount_rule.max_discount:
            discount_amount = min(discount_amount, discount_rule.max_discount)

        final_amount = max(0, amount - discount_amount)

        logger.info(
            f"Discount '{discount_rule.name}' applied: "
            f"${amount:.2f} - ${discount_amount:.2f} = ${final_amount:.2f}"
        )

        return {
            "original_amount": amount,
            "discount_amount": discount_amount,
            "final_amount": final_amount,
            "discount_applied": True,
            "discount_rule": discount_rule.id,
        }

    def calculate_invoice_total(
        self,
        line_items: List[LineItem],
        discount_rules: Optional[List[PricingRule]] = None,
    ) -> Dict:
        """
        Calculate complete invoice with all costs, discounts, and tax

        Args:
            line_items: List of line items (labor, parts, etc.)
            discount_rules: Optional list of discounts to apply

        Returns:
            Dict with subtotal, discounts, tax, and total
        """
        # Calculate subtotal
        subtotal = sum(item.total for item in line_items)

        # Apply discounts
        applied_discounts = []
        current_subtotal = subtotal

        if discount_rules:
            for rule in discount_rules:
                if not rule.active:
                    continue

                discount_result = self.apply_discount(current_subtotal, rule)
                if discount_result["discount_applied"]:
                    applied_discounts.append(discount_result)
                    current_subtotal = discount_result["final_amount"]

        # Calculate tax on discounted amount
        tax_amount = current_subtotal * self.tax_rate

        # Final total
        total = current_subtotal + tax_amount

        logger.info(
            f"Invoice calculated: "
            f"subtotal=${subtotal:.2f}, "
            f"discounts=${subtotal - current_subtotal:.2f}, "
            f"tax=${tax_amount:.2f}, "
            f"total=${total:.2f}"
        )

        return {
            "subtotal": subtotal,
            "applied_discounts": applied_discounts,
            "discount_total": subtotal - current_subtotal,
            "subtotal_after_discount": current_subtotal,
            "tax_rate": self.tax_rate,
            "tax_amount": tax_amount,
            "total": total,
            "line_items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total": item.total,
                }
                for item in line_items
            ],
        }

    def generate_invoice(
        self,
        booking_id: str,
        customer_id: str,
        line_items: List[LineItem],
        discount_rules: Optional[List[PricingRule]] = None,
        invoice_id: Optional[str] = None,
    ) -> Invoice:
        """
        Generate a complete invoice for a booking

        Args:
            booking_id: Associated booking ID
            customer_id: Customer ID
            line_items: List of line items
            discount_rules: Optional discounts
            invoice_id: Custom invoice ID (auto-generated if not provided)

        Returns:
            Complete Invoice object
        """
        # Calculate totals
        calculation = self.calculate_invoice_total(line_items, discount_rules)

        # Create invoice
        invoice = Invoice(
            id=invoice_id or f"INV-{int(datetime.now().timestamp())}",
            booking_id=booking_id,
            customer_id=customer_id,
            line_items=line_items,
            subtotal=calculation["subtotal"],
            tax_amount=calculation["tax_amount"],
            discounts=calculation["applied_discounts"],
            total=calculation["total"],
            created_at=datetime.now(),
            due_date=datetime.now() + __import__("datetime").timedelta(days=30),
            status="draft",
        )

        logger.info(f"✅ Invoice {invoice.id} generated for booking {booking_id}")

        return invoice

    def get_service_pricing_breakdown(
        self,
        service_name: str,
        duration_minutes: int,
        parts_list: List[Dict[str, float]],  # [{name, cost, quantity}]
        specialty_multiplier: float = 1.0,
    ) -> Dict:
        """
        Get complete pricing breakdown for a service

        Args:
            service_name: Name of service
            duration_minutes: Service duration
            parts_list: List of parts with costs
            specialty_multiplier: Multiplier for specialty work

        Returns:
            Detailed pricing breakdown
        """
        # Labor cost
        labor_cost = self.calculate_service_labor_cost(
            duration_minutes,
            specialty_multiplier=specialty_multiplier,
        )

        # Parts costs
        parts_total = 0.0
        parts_with_markup = []

        for part in parts_list:
            part_cost = part.get("cost", 0.0) * part.get("quantity", 1)
            marked_up = self.calculate_parts_cost_with_markup(part_cost)
            parts_with_markup.append({
                "name": part.get("name", "Part"),
                "quantity": part.get("quantity", 1),
                **marked_up,
            })
            parts_total += marked_up["selling_price"]

        # Subtotal
        subtotal = labor_cost + parts_total

        # Tax
        tax_amount = subtotal * self.tax_rate
        total = subtotal + tax_amount

        logger.info(
            f"Service '{service_name}' pricing: "
            f"labor=${labor_cost:.2f}, parts=${parts_total:.2f}, total=${total:.2f}"
        )

        return {
            "service_name": service_name,
            "duration_minutes": duration_minutes,
            "labor": {
                "hours": duration_minutes / 60.0,
                "hourly_rate": self.base_service_hour_rate,
                "specialty_multiplier": specialty_multiplier,
                "cost": labor_cost,
            },
            "parts": parts_with_markup,
            "subtotal": subtotal,
            "tax_rate": self.tax_rate,
            "tax_amount": tax_amount,
            "total": total,
        }
