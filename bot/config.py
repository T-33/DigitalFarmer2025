"""
Bot configuration module.
Loads settings from environment variables.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class BotConfig:
    """Telegram Bot Configuration"""
    token: str
    debug: bool = False


@dataclass
class APIConfig:
    """Backend API Configuration"""
    base_url: str
    timeout: int = 30


@dataclass
class Config:
    """Main configuration class"""
    bot: BotConfig
    api: APIConfig


def load_config() -> Config:
    """
    Load configuration from environment variables.

    Returns:
        Config: Configuration object

    Raises:
        ValueError: If required environment variables are missing
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is not set. "
            "Please create .env file with your bot token."
        )

    backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
    api_timeout = int(os.getenv("API_TIMEOUT", "30"))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    return Config(
        bot=BotConfig(
            token=bot_token,
            debug=debug
        ),
        api=APIConfig(
            base_url=backend_url,
            timeout=api_timeout
        )
    )


# Global config instance (loaded on import)
config = load_config()
