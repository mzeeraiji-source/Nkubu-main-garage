"""
Vehicle Diagnosis Engine - AI-powered symptom analysis
Uses Claude to provide intelligent diagnostics and recommendations
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class SeverityLevel(str, Enum):
    """Severity levels for vehicle issues"""
    CRITICAL = "critical"  # Safety risk, stop driving
    HIGH = "high"  # Needs urgent attention
    MEDIUM = "medium"  # Schedule soon
    LOW = "low"  # Routine maintenance


@dataclass
class DiagnosisResult:
    """Result of vehicle diagnosis"""
    symptoms: str
    probable_causes: List[str]
    severity: SeverityLevel
    recommended_services: List[str]
    estimated_cost_range: tuple  # (min, max)
    safety_concerns: Optional[List[str]] = None
    urgency_description: str = ""


class DiagnosisEngine:
    """
    Vehicle diagnosis using Claude AI
    Analyzes symptoms and provides intelligent recommendations
    """

    def __init__(self, claude_client):
        """
        Initialize diagnosis engine

        Args:
            claude_client: ClaudeClient instance for AI calls
        """
        self.claude_client = claude_client
        logger.info("DiagnosisEngine initialized")

    def diagnose_symptoms(
        self,
        symptoms: str,
        vehicle_year: int,
        vehicle_make: str,
        vehicle_model: str,
        mileage: int,
        additional_context: Optional[str] = None,
    ) -> DiagnosisResult:
        """
        Diagnose vehicle based on symptoms

        Args:
            symptoms: Description of symptoms
            vehicle_year: Vehicle year
            vehicle_make: Vehicle make
            vehicle_model: Vehicle model
            mileage: Current mileage
            additional_context: Any other relevant info

        Returns:
            DiagnosisResult with findings and recommendations
        """
        vehicle_info = {
            "year": vehicle_year,
            "make": vehicle_make,
            "model": vehicle_model,
            "mileage": mileage,
        }

        # Call Claude for diagnosis
        diagnosis_response = self.claude_client.diagnose_vehicle(
            symptoms=symptoms,
            vehicle_info=vehicle_info,
        )

        # Parse Claude's response and extract structured data
        logger.info(f"✅ Diagnosis completed for {vehicle_year} {vehicle_make} {vehicle_model}")

        return DiagnosisResult(
            symptoms=symptoms,
            probable_causes=self._extract_causes(diagnosis_response["diagnosis"]),
            severity=self._assess_severity(diagnosis_response["diagnosis"]),
            recommended_services=self._extract_services(diagnosis_response["diagnosis"]),
            estimated_cost_range=self._estimate_cost(diagnosis_response["diagnosis"]),
            safety_concerns=self._extract_safety_concerns(diagnosis_response["diagnosis"]),
        )

    def _extract_causes(self, diagnosis_text: str) -> List[str]:
        """Extract probable causes from Claude response"""
        # Placeholder - in production, parse Claude's structured response
        return ["Primary cause", "Secondary possibility", "Less likely cause"]

    def _assess_severity(self, diagnosis_text: str) -> SeverityLevel:
        """Assess severity from diagnosis"""
        # Placeholder - in production, parse Claude's assessment
        return SeverityLevel.MEDIUM

    def _extract_services(self, diagnosis_text: str) -> List[str]:
        """Extract recommended services"""
        # Placeholder - in production, parse Claude's recommendations
        return ["Diagnostic scan", "Component inspection"]

    def _estimate_cost(self, diagnosis_text: str) -> tuple:
        """Estimate cost range"""
        # Placeholder - in production, estimate based on services
        return (150.0, 500.0)

    def _extract_safety_concerns(self, diagnosis_text: str) -> Optional[List[str]]:
        """Extract any safety concerns"""
        # Placeholder - in production, identify safety issues
        return None

    def get_service_menu_recommendation(
        self,
        diagnosis_result: DiagnosisResult,
    ) -> List[Dict[str, Any]]:
        """
        Convert diagnosis to recommended services from our menu

        Args:
            diagnosis_result: DiagnosisResult from diagnosis

        Returns:
            List of recommended services with pricing
        """
        # This would query the database for actual service details
        recommendations = []

        for service_name in diagnosis_result.recommended_services:
            recommendations.append({
                "service_name": service_name,
                "estimated_duration": "1-2 hours",  # Would come from DB
                "estimated_cost": diagnosis_result.estimated_cost_range,
                "urgency": diagnosis_result.severity.value,
            })

        return recommendations
