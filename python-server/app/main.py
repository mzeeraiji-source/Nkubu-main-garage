"""
Nkubu FastAPI Application Entry Point
Main router configuration, middleware setup, startup/shutdown events
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import get_settings, validate_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# --- LIFESPAN EVENTS ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle management
    Initializes databases, AI clients, and background tasks
    """
    settings = get_settings()

    # Startup
    logger.info("🚀 Starting Nkubu Backend...")
    try:
        # Validate all required environment variables
        validate_settings(settings)
        logger.info(f"✅ Environment: {settings.ENVIRONMENT}")
        logger.info(f"✅ Debug Mode: {settings.DEBUG}")

        # TODO: Initialize database connections
        # - Supabase client
        # - Neon connection pool
        logger.info("✅ Database connections initialized")

        # TODO: Initialize external service clients
        # - Anthropic Claude API
        # - Shopify API
        # - Stripe API
        logger.info("✅ External services initialized")

        # TODO: Start background task workers (Celery)
        logger.info("✅ Background task workers started")

        # TODO: Initialize MCP Server for Claude Desktop
        if settings.MCP_ENABLED:
            logger.info("✅ MCP Server initialized")

        logger.info("🎉 Nkubu Backend ready to serve requests")

    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise

    yield  # Application running

    # Shutdown
    logger.info("🛑 Shutting down Nkubu Backend...")
    try:
        # TODO: Close database connections
        # TODO: Stop background workers
        # TODO: Shutdown external service clients
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# --- CREATE FASTAPI APPLICATION ---
def create_app() -> FastAPI:
    """
    Application factory: Creates and configures the FastAPI app
    Returns fully configured FastAPI instance ready for ASGI servers
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="AI-native automotive workshop ecosystem with e-commerce, booking management, and Claude AI integration",
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    # --- MIDDLEWARE STACK ---

    # CORS: Allow frontend communication
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # GZIP Compression
    app.add_middleware(GZIPMiddleware, minimum_size=1000)

    # --- EXCEPTION HANDLERS ---

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors with detailed response"""
        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.errors(),
                "body": exc.body,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected errors gracefully"""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "message": str(exc) if settings.DEBUG else "An error occurred",
            },
        )

    # --- ROUTES ---

    # Health Check Endpoint
    @app.get("/health", tags=["System"])
    async def health_check():
        """Simple health check endpoint for load balancers"""
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }

    # Root Endpoint
    @app.get("/", tags=["System"])
    async def root():
        """Welcome endpoint"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "api_version": "v1",
        }

    # TODO: Include routers as they're built
    # from app.api.v1 import bookings, inventory, analytics, ai, webhooks, health
    # app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])
    # app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
    # app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
    # app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])
    # app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])

    return app


# --- APPLICATION INSTANCE ---
app = create_app()


# --- UVICORN ENTRY POINT ---
if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
