"""
Pydantic request models for API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class AnalyzeCropRequest(BaseModel):
    """Request model for POST /analyze-crop endpoint"""
    image_base64: str = Field(
        ...,
        description="Base64 encoded image (JPEG, PNG)",
        min_length=100
    )
    telegram_user_id: int = Field(
        ...,
        description="Telegram user ID for analytics",
        gt=0
    )

    class Config:
        json_schema_extra = {
            "example": {
                "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                "telegram_user_id": 123456789
            }
        }


class WaterScheduleRequest(BaseModel):
    """Request model for POST /water-schedule endpoint"""
    crop_code: str = Field(
        ...,
        description="Crop code from analyze-crop response",
        min_length=2,
        max_length=50
    )
    growth_stage: str = Field(
        ...,
        description="Growth stage from analyze-crop response",
        min_length=2,
        max_length=50
    )
    water_date: str = Field(
        ...,
        description="ISO date (YYYY-MM-DD) when water will be available",
        pattern=r'^\d{4}-\d{2}-\d{2}$'
    )
    telegram_user_id: int = Field(
        ...,
        description="Telegram user ID for analytics",
        gt=0
    )
    latitude: Optional[float] = Field(
        default=42.8746,
        description="Latitude for weather forecast (default: Bishkek)",
        ge=-90,
        le=90
    )
    longitude: Optional[float] = Field(
        default=74.5698,
        description="Longitude for weather forecast (default: Bishkek)",
        ge=-180,
        le=180
    )

    class Config:
        json_schema_extra = {
            "example": {
                "crop_code": "corn",
                "growth_stage": "flowering",
                "water_date": "2025-11-29",
                "telegram_user_id": 123456789,
                "latitude": 42.8746,
                "longitude": 74.5698
            }
        }
