"""
Open-Meteo weather API integration service.
Fetches weather forecasts for irrigation planning.
"""
import logging
import httpx
from typing import Dict
from datetime import date, timedelta

from core.config import settings
from core.constants import (
    WEATHER_API_URL,
    WEATHER_API_TIMEOUT,
    MAX_FORECAST_DAYS,
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE,
)

logger = logging.getLogger(__name__)

# Weather condition emojis
WEATHER_CONDITIONS = {
    "clear": "☀️",
    "partly_cloudy": "⛅",
    "cloudy": "☁️",
    "rain": "🌧️",
    "snow": "🌨️",
}


async def get_weather_forecast(
    latitude: float = DEFAULT_LATITUDE,
    longitude: float = DEFAULT_LONGITUDE,
    target_date: date = None
) -> Dict:
    """
    Get weather forecast for a specific location and date.

    Args:
        latitude: Location latitude (defaults to Bishkek)
        longitude: Location longitude (defaults to Bishkek)
        target_date: Target date for forecast (defaults to today)

    Returns:
        Dict with weather information including temperature, precipitation, and ET0

    Raises:
        Exception: If API call fails or date out of range
    """
    # Use today if target_date not specified
    if target_date is None:
        target_date = date.today()

    # Mock mode for testing
    if settings.mock_weather:
        logger.info("Using mock weather response")
        return _get_mock_weather()

    try:
        # Validate date range
        days_ahead = (target_date - date.today()).days
        if days_ahead > MAX_FORECAST_DAYS:
            raise Exception(f"DATE_OUT_OF_RANGE: Maximum {MAX_FORECAST_DAYS} days")
        if days_ahead < 0:
            raise Exception("DATE_IN_PAST")

        # Prepare API request
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration",
            "timezone": "Asia/Bishkek",
            "forecast_days": MAX_FORECAST_DAYS
        }

        logger.info(f"Fetching weather for {latitude}, {longitude} on {target_date}")

        async with httpx.AsyncClient(timeout=float(WEATHER_API_TIMEOUT)) as client:
            response = await client.get(WEATHER_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            logger.info("Weather API response received")

            # Parse response for target date
            return _parse_weather_response(data, target_date)

    except httpx.HTTPStatusError as e:
        logger.error(f"Weather API HTTP error: {e.response.status_code}")
        raise Exception(f"WEATHER_API_ERROR: {e.response.status_code}")
    except httpx.TimeoutException:
        logger.error("Weather API timeout")
        raise Exception("WEATHER_API_TIMEOUT")
    except Exception as e:
        if str(e).startswith("DATE_"):
            raise
        logger.error(f"Weather API error: {str(e)}")
        raise Exception(f"WEATHER_API_ERROR: {str(e)}")


def _parse_weather_response(data: Dict, target_date: date) -> Dict:
    """
    Parse Open-Meteo API response for target date.

    Args:
        data: Raw API response
        target_date: Target date to extract

    Returns:
        Dict with parsed weather data
    """
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    temps_max = daily.get("temperature_2m_max", [])
    temps_min = daily.get("temperature_2m_min", [])
    precipitation = daily.get("precipitation_sum", [])
    et0 = daily.get("et0_fao_evapotranspiration", [])

    # Find index for target date
    target_date_str = target_date.isoformat()
    if target_date_str not in dates:
        raise Exception("DATE_NOT_IN_FORECAST")

    idx = dates.index(target_date_str)

    # Extract data
    temp_max = temps_max[idx] if idx < len(temps_max) else 20
    temp_min = temps_min[idx] if idx < len(temps_min) else 10
    precip = precipitation[idx] if idx < len(precipitation) else 0
    evapotranspiration = et0[idx] if idx < len(et0) else 3.5

    temp_avg = (temp_max + temp_min) / 2

    # Determine weather condition
    condition = _get_weather_condition(precip, temp_avg)

    weather_info = {
        "temp_avg": round(temp_avg, 1),
        "temp_max": round(temp_max, 1),
        "temp_min": round(temp_min, 1),
        "precipitation_mm": round(precip, 1),
        "et0": round(evapotranspiration, 2),
        "condition": condition,
        "date": target_date_str
    }

    logger.info(f"Weather parsed: {temp_avg}°C, {precip}mm rain, ET0={evapotranspiration}")

    return weather_info


def _get_weather_condition(precipitation: float, temp_avg: float) -> str:
    """
    Determine weather condition with emoji.

    Args:
        precipitation: Precipitation in mm
        temp_avg: Average temperature in °C

    Returns:
        Weather condition string with emoji
    """
    if precipitation > 10:
        return "Дождь 🌧️"
    elif precipitation > 2:
        return "Переменная облачность ⛅"
    elif precipitation > 0:
        return "Облачно ☁️"
    elif temp_avg > 25:
        return "Жарко и ясно ☀️"
    else:
        return "Ясно ☀️"


def _get_mock_weather() -> Dict:
    """
    Return mock weather data for testing.

    Returns:
        Mock weather data
    """
    return {
        "temp_avg": 12.5,
        "temp_max": 18.0,
        "temp_min": 7.0,
        "precipitation_mm": 0.0,
        "et0": 3.8,
        "condition": "Ясно ☀️",
        "date": (date.today() + timedelta(days=3)).isoformat()
    }


async def get_weekly_forecast(
    latitude: float = DEFAULT_LATITUDE,
    longitude: float = DEFAULT_LONGITUDE
) -> Dict:
    """
    Get 7-day weather forecast.

    Args:
        latitude: Location latitude (defaults to Bishkek)
        longitude: Location longitude (defaults to Bishkek)

    Returns:
        Dict with weekly forecast data

    Raises:
        Exception: If API call fails
    """
    if settings.mock_weather:
        return {"forecast": [_get_mock_weather() for _ in range(MAX_FORECAST_DAYS)]}

    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration",
            "timezone": "Asia/Bishkek",
            "forecast_days": MAX_FORECAST_DAYS
        }

        async with httpx.AsyncClient(timeout=float(WEATHER_API_TIMEOUT)) as client:
            response = await client.get(WEATHER_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            return data.get("daily", {})

    except Exception as e:
        logger.error(f"Weekly forecast error: {e}")
        raise


async def check_api_health() -> bool:
    """
    Check if Weather API is accessible.

    Returns:
        True if API is healthy, False otherwise
    """
    if settings.mock_weather:
        return True

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Test request for default location (Bishkek)
            params = {
                "latitude": DEFAULT_LATITUDE,
                "longitude": DEFAULT_LONGITUDE,
                "daily": "temperature_2m_max",
                "forecast_days": 1
            }
            response = await client.get(WEATHER_API_URL, params=params)
            return response.status_code == 200
    except Exception as e:
        logger.error(f"Weather API health check failed: {e}")
        return False
