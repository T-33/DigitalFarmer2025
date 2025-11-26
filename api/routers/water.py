"""
Water schedule endpoint.
"""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


class WaterScheduleRequest(BaseModel):
    """Request model for water schedule"""
    crop_code: str
    growth_stage: str
    water_date: str  # ISO format YYYY-MM-DD
    telegram_user_id: int


class WeatherInfo(BaseModel):
    """Weather information model"""
    temp_avg: float
    precipitation_mm: float
    condition: str


class RecommendationInfo(BaseModel):
    """Recommendation information model"""
    liters_per_sotka: int
    urgency: str
    urgency_display: str
    next_watering_days: int
    message_ru: str
    message_kg: str


class WaterScheduleResponse(BaseModel):
    """Response model for water schedule"""
    success: bool
    water_date: str = None
    water_date_display: str = None
    days_until_water: int = None
    weather: WeatherInfo = None
    recommendation: RecommendationInfo = None
    error: str = None
    error_code: str = None


@router.post("/water-schedule", response_model=WaterScheduleResponse)
async def get_water_schedule(request: WaterScheduleRequest):
    """
    Get irrigation schedule recommendation.

    Args:
        request: Water schedule request

    Returns:
        WaterScheduleResponse: Irrigation recommendation
    """
    logger.info(
        f"Getting water schedule for user {request.telegram_user_id}, "
        f"crop: {request.crop_code}, date: {request.water_date}"
    )

    # TODO: Implement weather API integration and calculations
    # For now, return mock response

    # Parse date
    try:
        water_date = datetime.fromisoformat(request.water_date).date()
        days_until = (water_date - datetime.now().date()).days
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Mock response for testing
    return {
        "success": True,
        "water_date": request.water_date,
        "water_date_display": "Пятница, 29 ноября",
        "days_until_water": days_until,
        "weather": {
            "temp_avg": 12.5,
            "precipitation_mm": 0,
            "condition": "Ясно ☀️"
        },
        "recommendation": {
            "liters_per_sotka": 650,
            "urgency": "critical",
            "urgency_display": "⚠️ Критично",
            "next_watering_days": 6,
            "message_ru": (
                "Твоя кукуруза на стадии цветения — критический период! "
                "Когда дадут воду, полей обильно."
            ),
            "message_kg": (
                "Сенин жүгөрүң гүлдөө стадиясында — абдан маанилүү кезең! "
                "Суу келгенде көп суу бер."
            )
        }
    }
