"""
Crop analysis endpoint.
"""
import logging
from fastapi import APIRouter, HTTPException
from models.requests import AnalyzeCropRequest
from models.responses import AnalyzeCropResponse, CropInfo, ErrorResponse
from services import plant_id

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze-crop", response_model=AnalyzeCropResponse)
async def analyze_crop(request: AnalyzeCropRequest):
    """
    Analyze crop from photo using Plant.id API.

    Args:
        request: Crop analysis request with base64 image

    Returns:
        AnalyzeCropResponse: Crop identification result

    Raises:
        HTTPException: If analysis fails
    """
    logger.info(f"Analyzing crop for user {request.telegram_user_id}")

    try:
        # Call Plant.id service
        crop_data = await plant_id.identify_crop(request.image_base64)

        # Return success response
        return AnalyzeCropResponse(
            success=True,
            crop=CropInfo(**crop_data)
        )

    except Exception as e:
        error_message = str(e)
        logger.error(f"Crop analysis failed: {error_message}")

        # Parse error code
        if "PLANT_NOT_RECOGNIZED" in error_message:
            return AnalyzeCropResponse(
                success=False,
                error="Could not identify plant in the image",
                error_code="PLANT_NOT_RECOGNIZED"
            )
        elif "UNSUPPORTED_CROP" in error_message:
            return AnalyzeCropResponse(
                success=False,
                error="Plant identified but not a supported crop",
                error_code="UNSUPPORTED_CROP"
            )
        elif "PLANT_ID_API_ERROR" in error_message:
            return AnalyzeCropResponse(
                success=False,
                error="External Plant.id API error",
                error_code="PLANT_ID_API_ERROR"
            )
        else:
            return AnalyzeCropResponse(
                success=False,
                error="Failed to analyze crop image",
                error_code="ANALYSIS_ERROR"
            )
