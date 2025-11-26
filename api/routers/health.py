"""
Health check endpoint.
"""
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    # TODO: Check external API connectivity
    return {
        "status": "ok",
        "plant_id_api": "not_implemented",
        "weather_api": "not_implemented"
    }
