"""
Irrigation calculation service.
Calculates water requirements based on crop type, growth stage, and weather.
"""
import logging
from typing import Dict
from datetime import date, datetime

logger = logging.getLogger(__name__)

# Crop coefficients (Kc) by crop and growth stage
# Based on FAO-56 guidelines
CROP_COEFFICIENTS = {
    "corn": {
        "initial": 0.3,
        "development": 0.7,
        "flowering": 1.2,
        "maturation": 0.6
    },
    "wheat": {
        "initial": 0.3,
        "development": 0.7,
        "flowering": 1.15,
        "maturation": 0.4
    },
    "cotton": {
        "initial": 0.35,
        "development": 0.7,
        "flowering": 1.15,
        "maturation": 0.7
    },
    "tomato": {
        "initial": 0.4,
        "development": 0.7,
        "flowering": 1.15,
        "maturation": 0.8
    },
    "potato": {
        "initial": 0.4,
        "development": 0.7,
        "flowering": 1.15,
        "maturation": 0.75
    },
    "onion": {
        "initial": 0.4,
        "development": 0.7,
        "flowering": 1.05,
        "maturation": 0.85
    },
    "carrot": {
        "initial": 0.4,
        "development": 0.7,
        "flowering": 1.05,
        "maturation": 0.95
    },
    "beet": {
        "initial": 0.4,
        "development": 0.75,
        "flowering": 1.05,
        "maturation": 0.95
    },
    "cucumber": {
        "initial": 0.4,
        "development": 0.7,
        "flowering": 1.0,
        "maturation": 0.9
    },
    "pepper": {
        "initial": 0.4,
        "development": 0.7,
        "flowering": 1.05,
        "maturation": 0.9
    }
}

# Watering intervals (days) by growth stage
WATERING_INTERVALS = {
    "initial": 8,
    "development": 7,
    "flowering": 5,
    "maturation": 7
}

# Urgency thresholds (days until water)
URGENCY_LEVELS = {
    "low": (5, "🟢 Нормально", "🟢 Жакшы"),
    "medium": (3, "🟡 Желательно", "🟡 Керек болсо"),
    "high": (1, "🔴 Важно", "🔴 Маанилүү"),
    "critical": (0, "⚠️ Критично", "⚠️ Абдан маанилүү")
}


def calculate_irrigation(
    crop_code: str,
    growth_stage: str,
    weather_info: Dict,
    days_until_water: int
) -> Dict:
    """
    Calculate irrigation recommendation.

    Args:
        crop_code: Crop identifier
        growth_stage: Current growth stage
        weather_info: Weather forecast data
        days_until_water: Days until irrigation date

    Returns:
        Dict with irrigation recommendation
    """
    logger.info(f"Calculating irrigation for {crop_code} ({growth_stage}), days={days_until_water}")

    # Get crop coefficient
    kc = CROP_COEFFICIENTS.get(crop_code, {}).get(growth_stage, 0.7)

    # Get ET0 (reference evapotranspiration) from weather
    et0 = weather_info.get("et0", 3.5)  # mm/day

    # Calculate crop evapotranspiration (ETc)
    etc_daily = kc * et0  # mm/day

    # Get expected precipitation
    precipitation = weather_info.get("precipitation_mm", 0)

    # Calculate net irrigation need (accounting for rainfall)
    net_irrigation_daily = max(0, etc_daily - precipitation)

    # Calculate total need for period until next watering
    next_watering_interval = WATERING_INTERVALS.get(growth_stage, 7)
    total_irrigation_mm = net_irrigation_daily * next_watering_interval

    # Convert mm to liters per sotka (100 m²)
    # 1mm = 1 liter per m² = 100 liters per sotka
    liters_per_sotka = int(total_irrigation_mm * 100)

    # Ensure minimum amount
    if liters_per_sotka < 200:
        liters_per_sotka = 200

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
        # Debug info (optional)
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
    Generate recommendation messages in Russian and Kyrgyz.

    Args:
        crop_code: Crop identifier
        growth_stage: Growth stage
        liters: Liters per sotka
        urgency: Urgency level
        days_until_water: Days until water
        weather_info: Weather information

    Returns:
        Dict with "ru" and "kg" messages
    """
    # Crop names
    crop_names = {
        "corn": {"ru": "кукуруза", "kg": "жүгөрү"},
        "wheat": {"ru": "пшеница", "kg": "буудай"},
        "cotton": {"ru": "хлопок", "kg": "пахта"},
        "tomato": {"ru": "помидоры", "kg": "помидор"},
        "potato": {"ru": "картофель", "kg": "картошка"},
        "onion": {"ru": "лук", "kg": "пияз"},
        "carrot": {"ru": "морковь", "kg": "сабизи"},
        "beet": {"ru": "свекла", "kg": "кызылча"},
        "cucumber": {"ru": "огурцы", "kg": "бадыраң"},
        "pepper": {"ru": "перец", "kg": "калемпир"},
    }

    # Stage descriptions
    stage_names = {
        "initial": {"ru": "всходах", "kg": "өнүү этабында"},
        "development": {"ru": "активном росте", "kg": "өсүү этабында"},
        "flowering": {"ru": "цветении", "kg": "гүлдөө этабында"},
        "maturation": {"ru": "созревании", "kg": "бышуу этабында"},
    }

    crop_ru = crop_names.get(crop_code, {}).get("ru", "культура")
    crop_kg = crop_names.get(crop_code, {}).get("kg", "өсүмдүк")
    stage_ru = stage_names.get(growth_stage, {}).get("ru", "развитии")
    stage_kg = stage_names.get(growth_stage, {}).get("kg", "өсүү этабында")

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
        crop_code: Crop identifier

    Returns:
        True if valid, False otherwise
    """
    return crop_code in CROP_COEFFICIENTS


def validate_growth_stage(growth_stage: str) -> bool:
    """
    Validate if growth stage is valid.

    Args:
        growth_stage: Growth stage identifier

    Returns:
        True if valid, False otherwise
    """
    return growth_stage in ["initial", "development", "flowering", "maturation"]
