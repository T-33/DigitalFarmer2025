"""
Water schedule endpoint.
"""
import logging
from datetime import datetime, date
from fastapi import APIRouter, HTTPException
from models.requests import WaterScheduleRequest
from models.responses import WaterScheduleResponse, WeatherInfo, IrrigationRecommendation
from services import weather, irrigation

logger = logging.getLogger(__name__)

router = APIRouter()

# Russian month names for date display
MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

# Russian day names
DAYS_RU = {
    0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг",
    4: "Пятница", 5: "Суббота", 6: "Воскресенье"
}


@router.post("/water-schedule", response_model=WaterScheduleResponse)
async def get_water_schedule(request: WaterScheduleRequest):
    """
    Get irrigation schedule recommendation based on crop, weather, and date.

    Args:
        request: Water schedule request with crop info and water date

    Returns:
        WaterScheduleResponse: Irrigation recommendation

    Raises:
        HTTPException: If validation or API calls fail
    """
    logger.info(
        f"Getting water schedule for user {request.telegram_user_id}, "
        f"crop: {request.crop_code}, stage: {request.growth_stage}, date: {request.water_date}"
    )

    try:
        # Validate crop and growth stage
        if not irrigation.validate_crop_code(request.crop_code):
            return WaterScheduleResponse(
                success=False,
                error=f"Unknown crop code: {request.crop_code}",
                error_code="INVALID_CROP_CODE"
            )

        if not irrigation.validate_growth_stage(request.growth_stage):
            return WaterScheduleResponse(
                success=False,
                error=f"Invalid growth stage: {request.growth_stage}",
                error_code="INVALID_GROWTH_STAGE"
            )

        # Parse water date
        try:
            water_date = datetime.fromisoformat(request.water_date).date()
        except ValueError:
            return WaterScheduleResponse(
                success=False,
                error="Invalid date format. Use YYYY-MM-DD",
                error_code="INVALID_DATE_FORMAT"
            )

        # Calculate days until water
        days_until_water = (water_date - date.today()).days

        # Validate date range
        if days_until_water < 0:
            return WaterScheduleResponse(
                success=False,
                error="Water date is in the past",
                error_code="DATE_IN_PAST"
            )

        if days_until_water > 7:
            return WaterScheduleResponse(
                success=False,
                error="Water date is too far in the future (max 7 days)",
                error_code="DATE_OUT_OF_RANGE"
            )

        # Get weather forecast
        weather_info = await weather.get_weather_forecast(
            latitude=request.latitude,
            longitude=request.longitude,
            target_date=water_date
        )

        # Calculate irrigation recommendation
        recommendation_data = irrigation.calculate_irrigation(
            crop_code=request.crop_code,
            growth_stage=request.growth_stage,
            weather_info=weather_info,
            days_until_water=days_until_water
        )

        # Format date display
        day_name = DAYS_RU[water_date.weekday()]
        month_name = MONTHS_RU[water_date.month]
        water_date_display = f"{day_name}, {water_date.day} {month_name}"

        # Build response
        return WaterScheduleResponse(
            success=True,
            water_date=request.water_date,
            water_date_display=water_date_display,
            days_until_water=days_until_water,
            weather=WeatherInfo(
                temp_avg=weather_info["temp_avg"],
                precipitation_mm=weather_info["precipitation_mm"],
                condition=weather_info["condition"]
            ),
            recommendation=IrrigationRecommendation(**recommendation_data)
        )

    except Exception as e:
        error_message = str(e)
        logger.error(f"Water schedule calculation failed: {error_message}")

        # Parse error codes
        if "DATE_OUT_OF_RANGE" in error_message:
            return WaterScheduleResponse(
                success=False,
                error="Water date is beyond forecast window (max 7 days)",
                error_code="DATE_OUT_OF_RANGE"
            )
        elif "DATE_IN_PAST" in error_message:
            return WaterScheduleResponse(
                success=False,
                error="Water date is in the past",
                error_code="DATE_IN_PAST"
            )
        elif "WEATHER_API_ERROR" in error_message:
            return WaterScheduleResponse(
                success=False,
                error="Failed to fetch weather forecast",
                error_code="WEATHER_API_ERROR"
            )
        else:
            return WaterScheduleResponse(
                success=False,
                error="Failed to calculate irrigation schedule",
                error_code="CALCULATION_ERROR"
            )
