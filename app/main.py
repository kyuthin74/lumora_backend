from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.api import auth, user, mood, alerts, charts, chatbot, emergency_contact, depression_test, depression_risk_result

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting Lumora Mental Health API...")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Lumora Mental Health API...")


def custom_openapi():
    """Custom OpenAPI schema to remove extra responses (422, etc.) from Swagger UI"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API for Lumora Mental Health Tracking Application",
        routes=app.routes,
    )
    
    # Remove 422 validation error responses from all endpoints
    for path in openapi_schema.get("paths", {}).values():
        for method in path.values():
            responses = method.get("responses", {})
            # Remove 422 Unprocessable Entity (validation error)
            responses.pop("422", None)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for Lumora Mental Health Tracking Application",
    lifespan=lifespan
)

# Override the default OpenAPI schema
app.openapi = custom_openapi

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )


# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(emergency_contact.router)
app.include_router(mood.router)
app.include_router(alerts.router)
app.include_router(charts.router)
app.include_router(chatbot.router)
app.include_router(depression_test.router)
app.include_router(depression_risk_result.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }


# Favicon endpoint to avoid 404s from browser requests
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204, media_type="image/x-icon")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


# API info endpoint
@app.get("/api/info")
async def api_info():
    """API information and available routes"""
    routes = []
    for route in app.routes:
        if hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "routes": routes
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
