"""
Central constants for MurabAI backend.
Eliminates code duplication and provides single source of truth.
"""
from typing import Dict, Tuple

# ============================================================================
# CROP INFORMATION
# ============================================================================

# Crop names in all supported languages
CROP_NAMES: Dict[str, Dict[str, str]] = {
    "corn": {"ru": "Кукуруза", "kg": "Жүгөрү", "en": "Corn"},
    "wheat": {"ru": "Пшеница", "kg": "Буудай", "en": "Wheat"},
    "cotton": {"ru": "Хлопок", "kg": "Пахта", "en": "Cotton"},
    "tomato": {"ru": "Помидор", "kg": "Помидор", "en": "Tomato"},
    "potato": {"ru": "Картофель", "kg": "Картошка", "en": "Potato"},
    "onion": {"ru": "Лук", "kg": "Пияз", "en": "Onion"},
    "carrot": {"ru": "Морковь", "kg": "Сабизи", "en": "Carrot"},
    "beet": {"ru": "Свекла", "kg": "Кызылча", "en": "Beet"},
    "cucumber": {"ru": "Огурец", "kg": "Бадыраң", "en": "Cucumber"},
    "pepper": {"ru": "Перец", "kg": "Калемпир", "en": "Pepper"},
}

# Growth stages with localized display names
GROWTH_STAGES: Dict[str, Dict[str, str]] = {
    "initial": {"ru": "Всходы 🌱", "kg": "Өнүү 🌱", "en": "Initial 🌱"},
    "development": {"ru": "Рост 🌿", "kg": "Өсүү 🌿", "en": "Development 🌿"},
    "flowering": {"ru": "Цветение 🌸", "kg": "Гүлдөө 🌸", "en": "Flowering 🌸"},
    "maturation": {"ru": "Созревание 🌾", "kg": "Бышуу 🌾", "en": "Maturation 🌾"},
}

# Stage names for use in sentences (genitive/locative case)
GROWTH_STAGE_NAMES: Dict[str, Dict[str, str]] = {
    "initial": {"ru": "всходах", "kg": "өнүү этабында"},
    "development": {"ru": "активном росте", "kg": "өсүү этабында"},
    "flowering": {"ru": "цветении", "kg": "гүлдөө этабында"},
    "maturation": {"ru": "созревании", "kg": "бышуу этабында"},
}

# Water need levels by growth stage
WATER_NEEDS: Dict[str, Dict[str, str]] = {
    "initial": {"level": "low", "ru": "🟢 Низкая", "kg": "🟢 Төмөн"},
    "development": {"level": "medium", "ru": "🟡 Средняя", "kg": "🟡 Орточо"},
    "flowering": {"level": "high", "ru": "🔴 Высокая", "kg": "🔴 Жогору"},
    "maturation": {"level": "medium", "ru": "🟡 Средняя", "kg": "🟡 Орточо"},
}

# Plant.id scientific name to crop code mapping
PLANT_ID_MAPPING: Dict[str, str] = {
    "Zea mays": "corn",
    "Triticum aestivum": "wheat",
    "Gossypium": "cotton",
    "Solanum lycopersicum": "tomato",
    "Solanum tuberosum": "potato",
    "Allium cepa": "onion",
    "Daucus carota": "carrot",
    "Beta vulgaris": "beet",
    "Cucumis sativus": "cucumber",
    "Capsicum annuum": "pepper",
}

# ============================================================================
# IRRIGATION CALCULATIONS (FAO-56)
# ============================================================================

# Crop coefficients (Kc) by crop and growth stage
# Based on FAO-56 guidelines for reference evapotranspiration
CROP_COEFFICIENTS: Dict[str, Dict[str, float]] = {
    "corn": {"initial": 0.3, "development": 0.7, "flowering": 1.2, "maturation": 0.6},
    "wheat": {"initial": 0.3, "development": 0.7, "flowering": 1.15, "maturation": 0.4},
    "cotton": {"initial": 0.35, "development": 0.7, "flowering": 1.15, "maturation": 0.7},
    "tomato": {"initial": 0.4, "development": 0.7, "flowering": 1.15, "maturation": 0.8},
    "potato": {"initial": 0.4, "development": 0.7, "flowering": 1.15, "maturation": 0.75},
    "onion": {"initial": 0.4, "development": 0.7, "flowering": 1.05, "maturation": 0.85},
    "carrot": {"initial": 0.4, "development": 0.7, "flowering": 1.05, "maturation": 0.95},
    "beet": {"initial": 0.4, "development": 0.75, "flowering": 1.05, "maturation": 0.95},
    "cucumber": {"initial": 0.4, "development": 0.7, "flowering": 1.0, "maturation": 0.9},
    "pepper": {"initial": 0.4, "development": 0.7, "flowering": 1.05, "maturation": 0.9},
}

# Watering intervals in days by growth stage
WATERING_INTERVALS: Dict[str, int] = {
    "initial": 8,
    "development": 7,
    "flowering": 5,
    "maturation": 7
}

# Urgency levels: (threshold_days, ru_display, kg_display)
URGENCY_LEVELS: Dict[str, Tuple[int, str, str]] = {
    "low": (5, "🟢 Нормально", "🟢 Жакшы"),
    "medium": (3, "🟡 Желательно", "🟡 Керек болсо"),
    "high": (1, "🔴 Важно", "🔴 Маанилүү"),
    "critical": (0, "⚠️ Критично", "⚠️ Абдан маанилүү")
}

# Minimum irrigation amount in liters per sotka (100 m²)
MIN_IRRIGATION_LITERS: int = 200

# ============================================================================
# LOCATION DEFAULTS
# ============================================================================

# Default location: Bishkek, Kyrgyzstan
DEFAULT_LATITUDE: float = 42.8746
DEFAULT_LONGITUDE: float = 74.5698

# ============================================================================
# API CONFIGURATION
# ============================================================================

# File size limits
MAX_PHOTO_SIZE_MB: int = 10
MAX_PHOTO_SIZE_BYTES: int = MAX_PHOTO_SIZE_MB * 1024 * 1024

# API timeouts (seconds)
DEFAULT_API_TIMEOUT: int = 30
PLANT_ID_TIMEOUT: int = 30
WEATHER_API_TIMEOUT: int = 10

# Weather forecast limits
MAX_FORECAST_DAYS: int = 7

# ============================================================================
# EXTERNAL API URLs
# ============================================================================

PLANT_ID_API_URL: str = "https://api.plant.id/v2/identify"
WEATHER_API_URL: str = "https://api.open-meteo.com/v1/forecast"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_crop_name(crop_code: str, lang: str = "ru") -> str:
    """
    Get localized crop name.

    Args:
        crop_code: Crop identifier (e.g., "corn")
        lang: Language code ("ru", "kg", "en")

    Returns:
        Localized crop name or crop_code if not found
    """
    return CROP_NAMES.get(crop_code, {}).get(lang, crop_code)


def get_growth_stage_display(stage: str, lang: str = "ru") -> str:
    """
    Get localized growth stage display name.

    Args:
        stage: Growth stage identifier
        lang: Language code

    Returns:
        Localized stage name with emoji
    """
    return GROWTH_STAGES.get(stage, {}).get(lang, stage)


def get_growth_stage_name(stage: str, lang: str = "ru") -> str:
    """
    Get localized growth stage name for use in sentences.

    Args:
        stage: Growth stage identifier
        lang: Language code

    Returns:
        Localized stage name in appropriate grammatical case
    """
    return GROWTH_STAGE_NAMES.get(stage, {}).get(lang, stage)


def is_valid_crop(crop_code: str) -> bool:
    """
    Check if crop code is valid.

    Args:
        crop_code: Crop identifier to validate

    Returns:
        True if crop is supported, False otherwise
    """
    return crop_code in CROP_NAMES


def is_valid_growth_stage(stage: str) -> bool:
    """
    Check if growth stage is valid.

    Args:
        stage: Growth stage identifier to validate

    Returns:
        True if stage is valid, False otherwise
    """
    return stage in GROWTH_STAGES


def get_crop_coefficient(crop_code: str, growth_stage: str) -> float:
    """
    Get crop coefficient for irrigation calculation.

    Args:
        crop_code: Crop identifier
        growth_stage: Growth stage

    Returns:
        Crop coefficient (Kc) or default value if not found
    """
    return CROP_COEFFICIENTS.get(crop_code, {}).get(growth_stage, 0.7)


def get_watering_interval(growth_stage: str) -> int:
    """
    Get recommended watering interval in days.

    Args:
        growth_stage: Growth stage

    Returns:
        Interval in days
    """
    return WATERING_INTERVALS.get(growth_stage, 7)
