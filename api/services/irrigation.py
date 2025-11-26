"""
Irrigation calculation service.
Calculates water requirements based on crop type, growth stage, and weather.
"""
import logging
from typing import Dict

from core.constants import (
    CROP_COEFFICIENTS,
    WATERING_INTERVALS,
    URGENCY_LEVELS,
    MIN_IRRIGATION_LITERS,
    get_crop_name,
    get_growth_stage_name,
    get_crop_coefficient,
    get_watering_interval,
)

logger = logging.getLogger(__name__)


def calculate_irrigation(
    crop_code: str,
    growth_stage: str,
    weather_info: Dict,
    days_until_water: int
) -> Dict:
    """
    Calculate irrigation recommendation based on FAO-56 methodology.

    Args:
        crop_code: Crop identifier (e.g., "corn", "wheat")
        growth_stage: Current growth stage (e.g., "flowering")
        weather_info: Weather forecast data including ET0 and precipitation
        days_until_water: Days until irrigation date

    Returns:
        Dict with irrigation recommendation including water volume and urgency
    """
    logger.info(f"Calculating irrigation for {crop_code} ({growth_stage}), days={days_until_water}")

    # Get crop coefficient using helper function
    kc = get_crop_coefficient(crop_code, growth_stage)

    # Get ET0 (reference evapotranspiration) from weather
    et0 = weather_info.get("et0", 3.5)  # mm/day

    # Calculate crop evapotranspiration (ETc)
    etc_daily = kc * et0  # mm/day

    # Get expected precipitation
    precipitation = weather_info.get("precipitation_mm", 0)

    # Calculate net irrigation need (accounting for rainfall)
    net_irrigation_daily = max(0, etc_daily - precipitation)

    # Calculate total need for period until next watering
    next_watering_interval = get_watering_interval(growth_stage)
    total_irrigation_mm = net_irrigation_daily * next_watering_interval

    # Convert mm to liters per sotka (100 m²)
    # 1mm = 1 liter per m² = 100 liters per sotka
    liters_per_sotka = int(total_irrigation_mm * 100)

    # Ensure minimum amount
    if liters_per_sotka < MIN_IRRIGATION_LITERS:
        liters_per_sotka = MIN_IRRIGATION_LITERS

    # Determine urgency
    urgency = _calculate_urgency(days_until_water, growth_stage)

    # Generate recommendation messages
    messages = _generate_messages(
        crop_code,
        growth_stage,
        liters_per_sotka,
        urgency,
        days_until_water,
        weather_info
    )

    recommendation = {
        "liters_per_sotka": liters_per_sotka,
        "urgency": urgency,
        "urgency_display": URGENCY_LEVELS[urgency][1],  # Russian
        "next_watering_days": next_watering_interval,
        "message_ru": messages["ru"],
        "message_kg": messages["kg"],
        # Debug info (optional, useful for development)
        "debug": {
            "kc": kc,
            "et0": et0,
            "etc_daily": round(etc_daily, 2),
            "net_irrigation_daily": round(net_irrigation_daily, 2),
            "total_mm": round(total_irrigation_mm, 1)
        }
    }

    logger.info(f"Recommendation: {liters_per_sotka}L/sotka, urgency={urgency}")

    return recommendation


def _calculate_urgency(days_until_water: int, growth_stage: str) -> str:
    """
    Calculate irrigation urgency level.

    Args:
        days_until_water: Days until water availability
        growth_stage: Current growth stage

    Returns:
        Urgency level: critical, high, medium, low
    """
    # Flowering is always more critical
    if growth_stage == "flowering":
        if days_until_water <= 1:
            return "critical"
        elif days_until_water <= 3:
            return "high"
        else:
            return "medium"
    else:
        if days_until_water <= 0:
            return "critical"
        elif days_until_water <= 2:
            return "high"
        elif days_until_water <= 4:
            return "medium"
        else:
            return "low"


def _generate_messages(
    crop_code: str,
    growth_stage: str,
    liters: int,
    urgency: str,
    days_until_water: int,
    weather_info: Dict
) -> Dict[str, str]:
    """
    Generate personalized recommendation messages in Russian and Kyrgyz.

    Args:
        crop_code: Crop identifier
        growth_stage: Growth stage
        liters: Liters per sotka
        urgency: Urgency level
        days_until_water: Days until water
        weather_info: Weather information

    Returns:
        Dict with "ru" and "kg" localized messages
    """
    # Get localized crop and stage names using helper functions
    crop_ru = get_crop_name(crop_code, "ru").lower()
    crop_kg = get_crop_name(crop_code, "kg").lower()
    stage_ru = get_growth_stage_name(growth_stage, "ru")
    stage_kg = get_growth_stage_name(growth_stage, "kg")

    temp = weather_info.get("temp_avg", 12)
    precip = weather_info.get("precipitation_mm", 0)

    # Russian message
    if urgency == "critical":
        message_ru = (
            f"⚠️ Твоя {crop_ru} на {stage_ru} — критический период!\n\n"
            f"💧 Норма: {liters} литров на сотку\n"
            f"🌡️ Прогноз: {temp}°C, осадки {precip}мм\n\n"
            f"Когда дадут воду, полей обильно. Растения очень нуждаются в воде!"
        )
    elif urgency == "high":
        message_ru = (
            f"🔴 Твоя {crop_ru} на {stage_ru}.\n\n"
            f"💧 Норма: {liters} литров на сотку\n"
            f"🌡️ Прогноз: {temp}°C, осадки {precip}мм\n\n"
            f"Через {days_until_water} дня будет вода — этого достаточно."
        )
    elif urgency == "medium":
        message_ru = (
            f"🟡 Твоя {crop_ru} на {stage_ru}.\n\n"
            f"💧 Норма: {liters} литров на сотку\n"
            f"🌡️ Прогноз: {temp}°C, осадки {precip}мм\n\n"
            f"Все в порядке, вода подойдет вовремя."
        )
    else:
        message_ru = (
            f"🟢 Твоя {crop_ru} на {stage_ru}.\n\n"
            f"💧 Норма: {liters} литров на сотку\n"
            f"🌡️ Прогноз: {temp}°C, осадки {precip}мм\n\n"
            f"Растения чувствуют себя хорошо. Поливай по графику."
        )

    # Kyrgyz message
    if urgency == "critical":
        message_kg = (
            f"⚠️ Сенин {crop_kg} {stage_kg} — абдан маанилүү кезең!\n\n"
            f"💧 Норма: {liters} литр сотка үчүн\n"
            f"🌡️ Аба ырайы: {temp}°C, жаан {precip}мм\n\n"
            f"Суу келгенде көп суу бер. Өсүмдүктөр сууга муктаж!"
        )
    elif urgency == "high":
        message_kg = (
            f"🔴 Сенин {crop_kg} {stage_kg}.\n\n"
            f"💧 Норма: {liters} литр сотка үчүн\n"
            f"🌡️ Аба ырайы: {temp}°C, жаан {precip}мм\n\n"
            f"{days_until_water} күндөн кийин суу келет — бул жетиштүү."
        )
    elif urgency == "medium":
        message_kg = (
            f"🟡 Сенин {crop_kg} {stage_kg}.\n\n"
            f"💧 Норма: {liters} литр сотка үчүн\n"
            f"🌡️ Аба ырайы: {temp}°C, жаан {precip}мм\n\n"
            f"Бардыгы жакшы, суу убагында келет."
        )
    else:
        message_kg = (
            f"🟢 Сенин {crop_kg} {stage_kg}.\n\n"
            f"💧 Норма: {liters} литр сотка үчүн\n"
            f"🌡️ Аба ырайы: {temp}°C, жаан {precip}мм\n\n"
            f"Өсүмдүктөр жакшы абалда. Графикте суу бер."
        )

    return {
        "ru": message_ru,
        "kg": message_kg
    }


def validate_crop_code(crop_code: str) -> bool:
    """
    Validate if crop code is supported.

    Args:
        crop_code: Crop identifier to validate

    Returns:
        True if crop is supported, False otherwise
    """
    from core.constants import is_valid_crop
    return is_valid_crop(crop_code)


def validate_growth_stage(growth_stage: str) -> bool:
    """
    Validate if growth stage is valid.

    Args:
        growth_stage: Growth stage identifier to validate

    Returns:
        True if stage is valid, False otherwise
    """
    from core.constants import is_valid_growth_stage
    return is_valid_growth_stage(growth_stage)
