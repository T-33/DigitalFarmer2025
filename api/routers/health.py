"""
Health check endpoint.
"""
import logging
from fastapi import APIRouter
from models.responses import HealthResponse
from services import plant_id, weather

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Verifies backend is running and external APIs are accessible.

    Returns:
        HealthResponse: Health status of all services
    """
    logger.info("Health check requested")

    # Check Plant.id API
    plant_id_status = "connected" if await plant_id.check_api_health() else "disconnected"

    # Check Weather API
    weather_status = "connected" if await weather.check_api_health() else "disconnected"

    # Overall status
    overall_status = "ok" if plant_id_status == "connected" and weather_status == "connected" else "degraded"

    return HealthResponse(
        status=overall_status,
        plant_id_api=plant_id_status,
        weather_api=weather_status
    )
