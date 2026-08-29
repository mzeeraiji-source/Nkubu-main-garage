"""
Claude AI Client - Wrapper around Anthropic API
Handles all Claude interactions for Nkubu
"""

import logging
from typing import Optional, List, Dict, Any
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeClient:
    """
    Unified wrapper for Claude API interactions
    Manages model selection, token budgets, and prompt engineering
    """

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ):
        """
        Initialize Claude client

        Args:
            api_key: Anthropic API key
            model: Claude model to use
            max_tokens: Maximum tokens per response
            temperature: Sampling temperature (0-1)
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        logger.info(
            f"ClaudeClient initialized: model={model}, "
            f"max_tokens={max_tokens}, temperature={temperature}"
        )

    def call_claude(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Call Claude with a prompt and optional conversation history

        Args:
            prompt: User message
            system_prompt: System instruction (optional)
            conversation_history: Previous messages for context
            max_tokens: Override default token limit
            temperature: Override default temperature

        Returns:
            Claude's response text
        """
        messages = []

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current message
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                system=system_prompt or "",
                messages=messages,
            )

            result = response.content[0].text
            logger.debug(f"Claude response: {len(result)} characters")

            return result

        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise

    def diagnose_vehicle(self, symptoms: str, vehicle_info: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Use Claude to diagnose vehicle issues based on symptoms

        Args:
            symptoms: Description of vehicle symptoms
            vehicle_info: Optional dict with year, make, model, mileage

        Returns:
            Dict with probable causes, severity, and recommended services
        """
        vehicle_context = ""
        if vehicle_info:
            vehicle_context = (
                f"Vehicle: {vehicle_info.get('year', '')} "
                f"{vehicle_info.get('make', '')} {vehicle_info.get('model', '')} "
                f"({vehicle_info.get('mileage', 'unknown')} miles)"
            )

        system_prompt = """You are an expert automotive technician for Nkubu Garage.
        Analyze vehicle symptoms and provide:
        1. Most probable causes (ranked by likelihood)
        2. Severity assessment (critical/high/medium/low)
        3. Recommended services from our menu
        4. Estimated repair complexity
        5. Safety concerns if any
        
        Format as structured JSON."""

        prompt = f"""Please diagnose this vehicle issue:
        
        {vehicle_context}
        
        Symptoms: {symptoms}
        
        Provide a comprehensive diagnosis with probable causes, severity, and recommended services."""

        response = self.call_claude(prompt, system_prompt=system_prompt)

        logger.info(f"✅ Vehicle diagnosis completed for symptoms: {symptoms[:50]}...")

        return {
            "symptoms": symptoms,
            "vehicle_info": vehicle_info,
            "diagnosis": response,
        }

    def recommend_parts(
        self,
        service_type: str,
        vehicle_specs: Dict[str, str],
        budget_constraint: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Use Claude to recommend compatible parts

        Args:
            service_type: Type of service (brake service, oil change, etc.)
            vehicle_specs: Dict with year, make, model, engine, etc.
            budget_constraint: Optional budget limit in dollars

        Returns:
            Dict with recommended parts and links
        """
        system_prompt = """You are an expert parts recommender for Nkubu Garage.
        Based on vehicle specifications and service type, recommend compatible parts.
        Consider quality, compatibility, and value.
        Format as structured JSON with part names, part numbers, estimated costs, and where to source."""

        budget_note = f"Budget constraint: ${budget_constraint}" if budget_constraint else ""

        prompt = f"""Please recommend parts for:
        
        Service: {service_type}
        Vehicle: {vehicle_specs.get('year')} {vehicle_specs.get('make')} {vehicle_specs.get('model')}
        Engine: {vehicle_specs.get('engine', 'unknown')}
        {budget_note}
        
        Provide a list of recommended parts with part numbers, compatibility notes, and estimated costs."""

        response = self.call_claude(prompt, system_prompt=system_prompt)

        logger.info(f"✅ Parts recommendations generated for {service_type}")

        return {
            "service_type": service_type,
            "vehicle_specs": vehicle_specs,
            "recommendations": response,
        }

    def generate_content(
        self,
        content_type: str,
        topic: str,
        tone: str = "professional",
        length: str = "medium",
    ) -> str:
        """
        Use Claude to generate marketing/blog content

        Args:
            content_type: "blog_post", "product_description", "email_campaign", etc.
            topic: What to write about
            tone: "professional", "casual", "technical"
            length: "short", "medium", "long"

        Returns:
            Generated content
        """
        length_guidance = {
            "short": "200-300 words",
            "medium": "500-800 words",
            "long": "1000-1500 words",
        }

        system_prompt = f"""You are a professional content writer for Nkubu Garage.
        Write {content_type} in a {tone} tone.
        Target audience: car owners who value quality service.
        Include relevant keywords for SEO where appropriate."""

        prompt = f"""Please write a {content_type} about:
        
        Topic: {topic}
        Length: {length_guidance.get(length, 'medium')}
        Tone: {tone}
        
        Make it engaging, informative, and aligned with Nkubu Garage's brand."""

        response = self.call_claude(prompt, system_prompt=system_prompt)

        logger.info(f"✅ Content generated: {content_type} on '{topic}'")

        return response

    def analyze_customer_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze a customer message to extract intent and information

        Args:
            message: Customer message text

        Returns:
            Dict with extracted intent, entities, and suggested response
        """
        system_prompt = """You are a customer service AI for Nkubu Garage.
        Analyze customer messages to extract:
        1. Customer intent (booking, inquiry, complaint, feedback)
        2. Key information (vehicle type, issue, urgency)
        3. Sentiment (positive, neutral, negative)
        4. Suggested response type
        Format as structured JSON."""

        prompt = f"""Please analyze this customer message and extract key information:
        
        Message: "{message}"
        
        Identify intent, entities, sentiment, and suggest how our team should respond."""

        response = self.call_claude(prompt, system_prompt=system_prompt)

        return {
            "original_message": message,
            "analysis": response,
        }
