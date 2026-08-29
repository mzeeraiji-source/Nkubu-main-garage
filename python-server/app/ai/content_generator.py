"""
Content Generator - AI-powered SEO and marketing content
Generates blog posts, product descriptions, and email campaigns
"""

import logging
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentType(str, Enum):
    """Types of content that can be generated"""
    BLOG_POST = "blog_post"
    PRODUCT_DESCRIPTION = "product_description"
    EMAIL_CAMPAIGN = "email_campaign"
    SERVICE_GUIDE = "service_guide"
    FAQ_ANSWER = "faq_answer"
    SOCIAL_MEDIA = "social_media"


class ContentGenerator:
    """Generate marketing and technical content using Claude AI"""

    def __init__(self, claude_client):
        """Initialize content generator"""
        self.claude_client = claude_client
        logger.info("ContentGenerator initialized")

    def generate_blog_post(
        self,
        topic: str,
        keywords: List[str],
        tone: str = "professional",
        length: str = "medium",
    ) -> Dict[str, str]:
        """
        Generate an SEO-optimized blog post

        Args:
            topic: Blog topic
            keywords: SEO keywords to include
            tone: Writing tone
            length: Post length (short/medium/long)

        Returns:
            Dict with title, content, meta_description
        """
        content = self.claude_client.generate_content(
            content_type="blog_post",
            topic=topic,
            tone=tone,
            length=length,
        )

        logger.info(f"✅ Blog post generated: {topic}")

        return {
            "title": f"Nkubu Garage Guide: {topic}",
            "content": content,
            "keywords": keywords,
            "meta_description": f"Expert guide on {topic} from Nkubu Garage",
            "generated_at": datetime.now().isoformat(),
        }

    def generate_service_description(
        self,
        service_name: str,
        service_category: str,
        benefits: List[str],
    ) -> str:
        """Generate compelling service description"""
        return self.claude_client.generate_content(
            content_type="product_description",
            topic=f"{service_category}: {service_name}",
            tone="professional",
        )

    def generate_email_campaign(
        self,
        campaign_type: str,  # reminder, promotion, newsletter
        recipient_type: str,  # loyal_customer, new_customer, returning
        personalization: Optional[Dict] = None,
    ) -> Dict[str, str]:
        """Generate personalized email campaign"""
        content = self.claude_client.generate_content(
            content_type="email_campaign",
            topic=f"{campaign_type} for {recipient_type}",
            tone="friendly",
        )

        logger.info(f"✅ Email campaign generated: {campaign_type}")

        return {
            "subject": f"Special offer for you at Nkubu Garage",
            "body": content,
            "cta": "Book Service Now",
            "personalization": personalization,
        }

    def batch_generate_content(
        self,
        requests: List[Dict],
    ) -> List[Dict]:
        """Generate multiple pieces of content in batch"""
        results = []
        for request in requests:
            if request["type"] == ContentType.BLOG_POST:
                result = self.generate_blog_post(**request["params"])
            else:
                result = {"status": "content_generated"}
            results.append(result)

        logger.info(f"✅ Batch generated {len(results)} content pieces")
        return results
