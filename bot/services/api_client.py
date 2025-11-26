"""
Backend API client for MurabAI bot.
Handles HTTP communication with FastAPI backend.
"""
import logging
from typing import Optional
import httpx
from config import config

logger = logging.getLogger(__name__)


class APIClient:
    """Client for interacting with backend API"""

    def __init__(self, base_url: str = None, timeout: int = None):
        """
        Initialize API client.

        Args:
            base_url: Backend API base URL (defaults to config)
            timeout: Request timeout in seconds (defaults to config)
        """
        self.base_url = base_url or config.api.base_url
        self.timeout = timeout or config.api.timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client (singleton pattern)"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"},
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
            )
        return self._client

    async def close(self):
        """Close HTTP client"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - but don't close the client!"""
        pass  # Keep client alive for reuse

    async def health_check(self) -> dict:
        """
        Check backend health status.

        Returns:
            dict: Health status response

        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            client = await self.get_client()
            response = await client.get("/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise

    async def analyze_crop(
        self,
        image_base64: str,
        telegram_user_id: int
    ) -> dict:
        """
        Analyze crop from base64 image.

        Args:
            image_base64: Base64 encoded image string
            telegram_user_id: Telegram user ID

        Returns:
            dict: Crop analysis response
            {
                "success": true,
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

        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            client = await self.get_client()
            response = await client.post(
                "/analyze-crop",
                json={
                    "image_base64": image_base64,
                    "telegram_user_id": telegram_user_id
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Crop analysis failed: {e.response.text}")
            # Return error response from backend
            try:
                return e.response.json()
            except:
                return {"success": False, "error": str(e), "error_code": "HTTP_ERROR"}
        except Exception as e:
            logger.error(f"Crop analysis request failed: {e}")
            raise

    async def get_water_schedule(
        self,
        crop_code: str,
        growth_stage: str,
        water_date: str,
        telegram_user_id: int
    ) -> dict:
        """
        Get irrigation schedule recommendation.

        Args:
            crop_code: Crop code (e.g., "corn", "wheat")
            growth_stage: Growth stage (e.g., "flowering")
            water_date: ISO date string (YYYY-MM-DD)
            telegram_user_id: Telegram user ID

        Returns:
            dict: Water schedule response
            {
                "success": true,
                "water_date": "2025-11-29",
                "water_date_display": "Пятница, 29 ноября",
                "days_until_water": 3,
                "weather": {...},
                "recommendation": {...}
            }

        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            client = await self.get_client()
            response = await client.post(
                "/water-schedule",
                json={
                    "crop_code": crop_code,
                    "growth_stage": growth_stage,
                    "water_date": water_date,
                    "telegram_user_id": telegram_user_id
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Water schedule failed: {e.response.text}")
            # Return error response from backend
            try:
                return e.response.json()
            except:
                return {"success": False, "error": str(e), "error_code": "HTTP_ERROR"}
        except Exception as e:
            logger.error(f"Water schedule request failed: {e}")
            raise


# Global API client instance
api_client = APIClient()
