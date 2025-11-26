"""
Crop analysis endpoint.
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


class AnalyzeCropRequest(BaseModel):
    """Request model for crop analysis"""
    image_base64: str
    telegram_user_id: int


class CropInfo(BaseModel):
    """Crop information model"""
    name_ru: str
    name_kg: str
    name_code: str
    confidence: float
    growth_stage: str
    growth_stage_display: str
    water_need: str
    water_need_display: str


class AnalyzeCropResponse(BaseModel):
    """Response model for crop analysis"""
    success: bool
    crop: CropInfo = None
    error: str = None
    error_code: str = None


@router.post("/analyze-crop", response_model=AnalyzeCropResponse)
async def analyze_crop(request: AnalyzeCropRequest):
    """
    Analyze crop from photo.

    Args:
        request: Crop analysis request

    Returns:
        AnalyzeCropResponse: Crop analysis result
    """
    logger.info(f"Analyzing crop for user {request.telegram_user_id}")

    # TODO: Implement Plant.id API integration
    # For now, return mock response

    # Mock response for testing
    return {
        "success": True,
        "crop": {
            "name_ru": "Кукуруза",
            "name_kg": "Жүгөрү",
            "name_code": "corn",
            "confidence": 0.94,
            "growth_stage": "flowering",
            "growth_stage_display": "Цветение 🌸",
            "water_need": "high",
            "water_need_display": "🔴 Высокая"
        }
    }
