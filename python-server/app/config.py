"""
Configuration & Environment Variables for Nkubu Backend
Manages all settings: database, APIs, auth, features
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Core application settings loaded from environment variables"""

    # Application Metadata
    APP_NAME: str = "Nkubu Garage"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")  # dev, staging, prod
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "https://nkubu.vercel.app"]

    # --- DATABASE CONFIGURATION ---
    # Supabase (Primary - Realtime, Auth, Storage)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")

    # Neon (Analytics, Vector DB, Read Replicas)
    NEON_DATABASE_URL: str = os.getenv("NEON_DATABASE_URL", "")
    NEON_POOLER_URL: str = os.getenv("NEON_POOLER_URL", "")

    # PostgreSQL Connection Pooling
    DB_POOL_MIN_SIZE: int = int(os.getenv("DB_POOL_MIN_SIZE", "5"))
    DB_POOL_MAX_SIZE: int = int(os.getenv("DB_POOL_MAX_SIZE", "20"))

    # --- ANTHROPIC / CLAUDE AI ---
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "2048"))
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))

    # MCP Server Configuration (Claude Desktop Integration)
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "3001"))
    MCP_ENABLED: bool = os.getenv("MCP_ENABLED", "true").lower() == "true"

    # --- SHOPIFY INTEGRATION ---
    SHOPIFY_STORE_NAME: str = os.getenv("SHOPIFY_STORE_NAME", "")
    SHOPIFY_ACCESS_TOKEN: str = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
    SHOPIFY_API_VERSION: str = os.getenv("SHOPIFY_API_VERSION", "2024-01")
    SHOPIFY_WEBHOOK_SECRET: str = os.getenv("SHOPIFY_WEBHOOK_SECRET", "")

    # --- PAYMENT PROCESSING (STRIPE) ---
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # --- NOTIFICATIONS ---
    # Twilio (SMS)
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    # Resend (Transactional Email)
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    SUPPORT_EMAIL: str = os.getenv("SUPPORT_EMAIL", "support@nkubu.garage")
    NOREPLY_EMAIL: str = os.getenv("NOREPLY_EMAIL", "noreply@nkubu.garage")

    # --- AUTHENTICATION ---
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    REFRESH_TOKEN_EXPIRATION_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRATION_DAYS", "7"))

    # OAuth (Google)
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")

    # --- BUSINESS RULES ---
    # Booking Engine
    BOOKING_BUFFER_MINUTES: int = int(os.getenv("BOOKING_BUFFER_MINUTES", "30"))
    MAX_CONCURRENT_BOOKINGS_PER_BAY: int = int(os.getenv("MAX_CONCURRENT_BOOKINGS_PER_BAY", "1"))
    BOOKING_ADVANCE_DAYS: int = int(os.getenv("BOOKING_ADVANCE_DAYS", "90"))
    HOLIDAY_CLOSURES: list = os.getenv("HOLIDAY_CLOSURES", "").split(",") if os.getenv("HOLIDAY_CLOSURES") else []

    # Pricing
    BASE_SERVICE_HOUR_RATE: float = float(os.getenv("BASE_SERVICE_HOUR_RATE", "50.00"))
    PARTS_MARKUP_PERCENTAGE: float = float(os.getenv("PARTS_MARKUP_PERCENTAGE", "20.0"))

    # Notifications
    BOOKING_REMINDER_HOURS: int = int(os.getenv("BOOKING_REMINDER_HOURS", "24"))
    ENABLE_SMS_NOTIFICATIONS: bool = os.getenv("ENABLE_SMS_NOTIFICATIONS", "true").lower() == "true"
    ENABLE_EMAIL_NOTIFICATIONS: bool = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "true").lower() == "true"

    # --- CELERY (BACKGROUND JOBS) ---
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
    CELERY_TIMEZONE: str = "UTC"

    # Sync Intervals (in seconds)
    SHOPIFY_SYNC_INTERVAL: int = int(os.getenv("SHOPIFY_SYNC_INTERVAL", "3600"))  # 1 hour
    ANALYTICS_BATCH_INTERVAL: int = int(os.getenv("ANALYTICS_BATCH_INTERVAL", "300"))  # 5 minutes

    # --- LOGGING & MONITORING ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN", None)

    # --- API RATE LIMITING ---
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

    # --- VERCEL DEPLOYMENT ---
    VERCEL_ENV: str = os.getenv("VERCEL_ENV", "development")
    VERCEL_URL: str = os.getenv("VERCEL_URL", "http://localhost:8000")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Singleton pattern: Returns cached settings instance
    Used throughout the app via dependency injection
    """
    return Settings()


# Validate critical settings on startup
def validate_settings(settings: Settings) -> None:
    """Ensure all required environment variables are configured"""
    required_fields = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "NEON_DATABASE_URL",
        "ANTHROPIC_API_KEY",
        "SHOPIFY_STORE_NAME",
        "SHOPIFY_ACCESS_TOKEN",
    ]

    missing = [field for field in required_fields if not getattr(settings, field)]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            f"Please configure these in your .env file"
        )
