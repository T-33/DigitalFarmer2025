"""
Backend API configuration module.
"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""

    def __init__(self):
        # Plant.id API
        self.plant_id_api_key: str = os.getenv("PLANT_ID_API_KEY", "")

        # Application
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.api_version: str = os.getenv("API_VERSION", "v1")

        # Database
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "sqlite+aiosqlite:///./murab.db"
        )

        # CORS
        allowed_origins_str = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:3000,http://localhost:8080"
        )
        self.allowed_origins: List[str] = [
            origin.strip() for origin in allowed_origins_str.split(",")
        ]

        # Mock mode for testing
        self.mock_plant_id: bool = os.getenv("MOCK_PLANT_ID", "false").lower() == "true"
        self.mock_weather: bool = os.getenv("MOCK_WEATHER", "false").lower() == "true"


# Global settings instance
settings = Settings()
