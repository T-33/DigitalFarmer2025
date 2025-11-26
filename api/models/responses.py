"""
Pydantic response models for API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    """Response model for GET /health endpoint"""
    status: str = Field(..., description="Status: 'ok' or 'error'")
    plant_id_api: str = Field(..., description="Plant.id API status: 'connected' or 'disconnected'")
    weather_api: str = Field(..., description="Weather API status: 'connected' or 'disconnected'")


class CropInfo(BaseModel):
    """Crop information model"""
    name_ru: str = Field(..., description="Crop name in Russian")
    name_kg: str = Field(..., description="Crop name in Kyrgyz")
    name_code: str = Field(..., description="Internal crop code")
    confidence: float = Field(..., description="Identification confidence (0.0 to 1.0)", ge=0, le=1)
    growth_stage: str = Field(..., description="Growth stage code")
    growth_stage_display: str = Field(..., description="Localized growth stage with emoji")
    water_need: str = Field(..., description="Water need level: low, medium, high, critical")
    water_need_display: str = Field(..., description="Localized water need with emoji")


class AnalyzeCropResponse(BaseModel):
    """Response model for POST /analyze-crop endpoint"""
    success: bool = Field(..., description="Operation success status")
    crop: Optional[CropInfo] = Field(None, description="Crop information")
    error: Optional[str] = Field(None, description="Error message if failed")
    error_code: Optional[str] = Field(None, description="Error code if failed")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class WeatherInfo(BaseModel):
    """Weather information model"""
    temp_avg: float = Field(..., description="Average temperature (°C)")
    precipitation_mm: float = Field(..., description="Expected precipitation (mm)")
    condition: str = Field(..., description="Weather condition with emoji")


class IrrigationRecommendation(BaseModel):
    """Irrigation recommendation model"""
    liters_per_sotka: int = Field(..., description="Water amount per 100 m² (sotka)")
    urgency: str = Field(..., description="Urgency level: low, medium, high, critical")
    urgency_display: str = Field(..., description="Localized urgency with emoji")
    next_watering_days: int = Field(..., description="Recommended days until next watering", ge=1)
    message_ru: str = Field(..., description="Complete recommendation in Russian")
    message_kg: str = Field(..., description="Complete recommendation in Kyrgyz")


class WaterScheduleResponse(BaseModel):
    """Response model for POST /water-schedule endpoint"""
    success: bool = Field(..., description="Operation success status")
    water_date: Optional[str] = Field(None, description="Confirmed water date (ISO format)")
    water_date_display: Optional[str] = Field(None, description="Localized date display")
    days_until_water: Optional[int] = Field(None, description="Days from today to water date")
    weather: Optional[WeatherInfo] = Field(None, description="Weather information")
    recommendation: Optional[IrrigationRecommendation] = Field(None, description="Irrigation recommendation")
    error: Optional[str] = Field(None, description="Error message if failed")
    error_code: Optional[str] = Field(None, description="Error code if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "water_date": "2025-11-29",
                "water_date_display": "Пятница, 29 ноября",
                "days_until_water": 3,
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
                    "message_ru": "Твоя кукуруза на стадии цветения — критический период!",
                    "message_kg": "Сенин жүгөрүң гүлдөө стадиясында — абдан маанилүү кезең!"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Generic error response model"""
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
