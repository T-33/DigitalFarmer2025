"""
Plant.id API integration service.
Identifies crops from images using Plant.id API.
"""
import logging
import httpx
import base64
import binascii
from typing import Dict, Optional

from core.config import settings
from core.constants import (
    PLANT_ID_API_URL,
    PLANT_ID_MAPPING,
    PLANT_ID_TIMEOUT,
    get_crop_name,
    get_growth_stage_display,
    WATER_NEEDS,
)

logger = logging.getLogger(__name__)


def validate_base64_image(image_base64: str) -> bool:
    """
    Validate that base64 string is a valid image.

    Args:
        image_base64: Base64 encoded string

    Returns:
        True if valid image format, False otherwise
    """
    try:
        # Try to decode
        image_bytes = base64.b64decode(image_base64)

        # Check magic bytes for common image formats
        if image_bytes[:2] == b'\xff\xd8':  # JPEG
            return True
        elif image_bytes[:4] == b'\x89PNG':  # PNG
            return True
        elif image_bytes[:6] in [b'GIF87a', b'GIF89a']:  # GIF
            return True
        elif image_bytes[:2] in [b'BM', b'BA']:  # BMP
            return True

        return False
    except (binascii.Error, ValueError):
        return False


async def identify_crop(image_base64: str) -> Dict:
    """
    Identify crop from base64 encoded image using Plant.id API.

    Args:
        image_base64: Base64 encoded image string

    Returns:
        Dict with crop information

    Raises:
        Exception: If API call fails or image is invalid
    """
    # Validate base64 image
    if not validate_base64_image(image_base64):
        logger.error("Invalid base64 image format")
        raise Exception("INVALID_IMAGE_FORMAT")

    # Mock mode for testing
    if settings.mock_plant_id:
        logger.info("Using mock Plant.id response")
        return _get_mock_response()

    try:
        # Prepare request payload
        payload = {
            "images": [f"data:image/jpeg;base64,{image_base64}"],
            "modifiers": ["crops", "similar_images"],
            "plant_language": "ru",
            "plant_details": ["common_names", "taxonomy", "url"]
        }

        headers = {
            "Content-Type": "application/json",
            "Api-Key": settings.plant_id_api_key
        }

        logger.info("Calling Plant.id API...")

        async with httpx.AsyncClient(timeout=float(PLANT_ID_TIMEOUT)) as client:
            response = await client.post(
                PLANT_ID_API_URL,
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            data = response.json()

            logger.info("Plant.id API response received")

            # Parse response
            return _parse_plant_id_response(data)

    except httpx.HTTPStatusError as e:
        logger.error(f"Plant.id API HTTP error: {e.response.status_code}")
        raise Exception(f"PLANT_ID_API_ERROR: {e.response.status_code}")
    except httpx.TimeoutException:
        logger.error("Plant.id API timeout")
        raise Exception("PLANT_ID_API_TIMEOUT")
    except Exception as e:
        logger.error(f"Plant.id API error: {str(e)}")
        raise


def _parse_plant_id_response(data: Dict) -> Dict:
    """
    Parse Plant.id API response and extract crop information.

    Args:
        data: Raw API response

    Returns:
        Dict with parsed crop data
    """
    suggestions = data.get("suggestions", [])

    if not suggestions:
        raise Exception("PLANT_NOT_RECOGNIZED")

    # Get top suggestion
    top_suggestion = suggestions[0]
    plant_name = top_suggestion.get("plant_name", "")
    probability = top_suggestion.get("probability", 0)

    logger.info(f"Top suggestion: {plant_name} (confidence: {probability:.2f})")

    # Map to our crop codes
    crop_code = _map_to_crop_code(plant_name)

    if not crop_code:
        raise Exception("UNSUPPORTED_CROP")

    # Infer growth stage (simplified - in production, use more sophisticated analysis)
    growth_stage = _infer_growth_stage(probability)

    # Build response
    crop_info = {
        "name_ru": get_crop_name(crop_code, "ru"),
        "name_kg": get_crop_name(crop_code, "kg"),
        "name_code": crop_code,
        "confidence": round(probability, 2),
        "growth_stage": growth_stage,
        "growth_stage_display": get_growth_stage_display(growth_stage, "ru"),
        "water_need": WATER_NEEDS[growth_stage]["level"],
        "water_need_display": WATER_NEEDS[growth_stage]["ru"]
    }

    return crop_info


def _map_to_crop_code(plant_name: str) -> Optional[str]:
    """
    Map Plant.id scientific name to our crop code.

    Args:
        plant_name: Scientific name from Plant.id

    Returns:
        Crop code or None if not found
    """
    # Direct mapping
    if plant_name in PLANT_ID_MAPPING:
        return PLANT_ID_MAPPING[plant_name]

    # Partial matching (for genus-level matches)
    for scientific_name, crop_code in PLANT_ID_MAPPING.items():
        if plant_name.startswith(scientific_name.split()[0]):
            return crop_code

    return None


def _infer_growth_stage(confidence: float) -> str:
    """
    Infer growth stage from image analysis.
    Simplified version - uses confidence as proxy.
    In production, use Plant.id health assessment or custom CV model.

    Args:
        confidence: Identification confidence

    Returns:
        Growth stage code
    """
    # Simplified logic for MVP
    # In reality, you'd analyze plant size, leaves, flowers, etc.
    if confidence > 0.9:
        return "flowering"  # High confidence → mature plant
    elif confidence > 0.7:
        return "development"  # Medium confidence → growing
    else:
        return "initial"  # Lower confidence → young plant


def _get_mock_response() -> Dict:
    """
    Return mock crop identification for testing.

    Returns:
        Mock crop data
    """
    return {
        "name_ru": "Кукуруза",
        "name_kg": "Жүгөрү",
        "name_code": "corn",
        "confidence": 0.94,
        "growth_stage": "flowering",
        "growth_stage_display": "Цветение 🌸",
        "water_need": "high",
        "water_need_display": "🔴 Высокая"
    }


async def check_api_health() -> bool:
    """
    Check if Plant.id API is accessible.

    Returns:
        True if API is healthy, False otherwise
    """
    if settings.mock_plant_id:
        return True

    # Plant.id doesn't have a /health endpoint, so we just check if we have an API key
    # The actual /identify endpoint will work if the key is valid
    if settings.plant_id_api_key and len(settings.plant_id_api_key) > 20:
        return True

    return False
