"""
MurabAI - Backend API
FastAPI application entry point.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import health, crop, water

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MurabAI API",
    description="Backend API for MurabAI irrigation assistant",
    version="1.0.0",
    docs_url=f"/api/{settings.api_version}/docs",
    redoc_url=f"/api/{settings.api_version}/redoc",
    openapi_url=f"/api/{settings.api_version}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    health.router,
    prefix=f"/api/{settings.api_version}",
    tags=["health"]
)
app.include_router(
    crop.router,
    prefix=f"/api/{settings.api_version}",
    tags=["crop"]
)
app.include_router(
    water.router,
    prefix=f"/api/{settings.api_version}",
    tags=["water"]
)


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting MurabAI Backend API")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Mock Plant.id: {settings.mock_plant_id}")
    logger.info(f"Mock Weather: {settings.mock_weather}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down MurabAI Backend API")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MurabAI Backend API",
        "version": "1.0.0",
        "docs": f"/api/{settings.api_version}/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
