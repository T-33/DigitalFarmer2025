"""
Regions of Kyrgyzstan with coordinates and agricultural data.
"""
from typing import Dict, List, Tuple

# Regions of Kyrgyzstan with real coordinates and agricultural data
REGIONS: Dict[str, Dict] = {
    "chui": {
        "name_kg": "Чүй облусу",
        "name_ru": "Чуйская область",
        "coordinates": (42.8746, 74.5698),  # Bishkek area
        "elevation": 750,  # meters
        "climate": "continental",
        "main_crops": ["wheat", "potato", "corn", "vegetables"],
        "water_coefficient": 1.0,  # base coefficient
        "emoji": "🌾"
    },
    "issyk_kul": {
        "name_kg": "Ысык-Көл облусу",
        "name_ru": "Иссык-Кульская область",
        "coordinates": (42.4415, 77.4915),  # Karakol
        "elevation": 1600,  # meters
        "climate": "mountain",
        "main_crops": ["wheat", "potato", "barley"],
        "water_coefficient": 0.85,  # cooler climate, less evaporation
        "emoji": "🏔️"
    },
    "naryn": {
        "name_kg": "Нарын облусу",
        "name_ru": "Нарынская область",
        "coordinates": (41.4286, 75.9911),  # Naryn
        "elevation": 2050,  # meters
        "climate": "high_mountain",
        "main_crops": ["wheat", "barley", "potato"],
        "water_coefficient": 0.75,  # high elevation, cold climate
        "emoji": "⛰️"
    },
    "talas": {
        "name_kg": "Талас облусу",
        "name_ru": "Таласская область",
        "coordinates": (42.5228, 72.2428),  # Talas
        "elevation": 1200,  # meters
        "climate": "continental",
        "main_crops": ["wheat", "corn", "potato", "sugar_beet"],
        "water_coefficient": 1.05,  # warmer, more evaporation
        "emoji": "🌾"
    },
    "jalal_abad": {
        "name_kg": "Жалал-Абад облусу",
        "name_ru": "Джалал-Абадская область",
        "coordinates": (40.9333, 72.9333),  # Jalal-Abad
        "elevation": 760,  # meters
        "climate": "warm_continental",
        "main_crops": ["cotton", "wheat", "rice", "vegetables", "fruits"],
        "water_coefficient": 1.15,  # warmer south, high evaporation
        "emoji": "🌻"
    },
    "osh": {
        "name_kg": "Ош облусу",
        "name_ru": "Ошская область",
        "coordinates": (40.5283, 72.7985),  # Osh
        "elevation": 960,  # meters
        "climate": "warm_continental",
        "main_crops": ["cotton", "wheat", "corn", "vegetables", "fruits"],
        "water_coefficient": 1.2,  # warmest region, highest evaporation
        "emoji": "🍇"
    },
    "batken": {
        "name_kg": "Баткен облусу",
        "name_ru": "Баткенская область",
        "coordinates": (40.0633, 70.8181),  # Batken
        "elevation": 1000,  # meters
        "climate": "warm_continental",
        "main_crops": ["cotton", "wheat", "vegetables", "fruits"],
        "water_coefficient": 1.25,  # very warm, water scarce
        "emoji": "🌵"
    }
}

# Regional statistics for demo (realistic numbers based on agricultural data)
REGIONAL_STATS: Dict[str, Dict] = {
    "chui": {
        "users": 42,
        "analyses": 187,
        "water_saved_m3": 4250,
        "avg_confidence": 92
    },
    "issyk_kul": {
        "users": 23,
        "analyses": 98,
        "water_saved_m3": 2100,
        "avg_confidence": 89
    },
    "naryn": {
        "users": 15,
        "analyses": 61,
        "water_saved_m3": 1350,
        "avg_confidence": 88
    },
    "talas": {
        "users": 18,
        "analyses": 79,
        "water_saved_m3": 1820,
        "avg_confidence": 91
    },
    "jalal_abad": {
        "users": 31,
        "analyses": 142,
        "water_saved_m3": 3580,
        "avg_confidence": 90
    },
    "osh": {
        "users": 38,
        "analyses": 165,
        "water_saved_m3": 4100,
        "avg_confidence": 93
    },
    "batken": {
        "users": 14,
        "analyses": 53,
        "water_saved_m3": 1250,
        "avg_confidence": 87
    }
}


def get_region_info(region_code: str) -> Dict:
    """
    Get region information by code.

    Args:
        region_code: Region code (e.g., 'chui', 'osh')

    Returns:
        Dict with region information
    """
    return REGIONS.get(region_code, REGIONS["chui"])


def get_region_coordinates(region_code: str) -> Tuple[float, float]:
    """
    Get region coordinates (latitude, longitude).

    Args:
        region_code: Region code

    Returns:
        Tuple of (latitude, longitude)
    """
    region = get_region_info(region_code)
    return region["coordinates"]


def get_water_coefficient(region_code: str) -> float:
    """
    Get water coefficient for region (affects irrigation calculations).

    Args:
        region_code: Region code

    Returns:
        Water coefficient (1.0 = base, higher = more water needed)
    """
    region = get_region_info(region_code)
    return region.get("water_coefficient", 1.0)


def get_region_stats(region_code: str) -> Dict:
    """
    Get regional statistics for demo.

    Args:
        region_code: Region code

    Returns:
        Dict with statistics
    """
    return REGIONAL_STATS.get(region_code, REGIONAL_STATS["chui"])


def get_all_regions() -> List[str]:
    """
    Get list of all region codes.

    Returns:
        List of region codes
    """
    return list(REGIONS.keys())


def get_region_display_name(region_code: str, lang: str = "kg") -> str:
    """
    Get region display name in specified language.

    Args:
        region_code: Region code
        lang: Language code ('kg' or 'ru')

    Returns:
        Region name
    """
    region = get_region_info(region_code)
    key = f"name_{lang}"
    return region.get(key, region["name_kg"])
