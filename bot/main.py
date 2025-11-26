"""
MurabAI - Telegram Bot
Main entry point for the bot.
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import config
from handlers import start, photo, schedule, stats, help, feedback, region

# Configure logging
logging.basicConfig(
    level=logging.INFO if not config.bot.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    """
    Set bot commands menu for different languages.

    Args:
        bot: Bot instance
    """
    # Commands for Kyrgyz language
    commands_kg = [
        BotCommand(command="start", description="🌱 Башынан баштоо"),
        BotCommand(command="help", description="❓ Жардам"),
        BotCommand(command="stats", description="📊 Статистика"),
        BotCommand(command="feedback", description="💬 Пикир калтыруу"),
        BotCommand(command="language", description="🌐 Тилди өзгөртүү"),
    ]

    # Commands for Russian language
    commands_ru = [
        BotCommand(command="start", description="🌱 Начать заново"),
        BotCommand(command="help", description="❓ Помощь"),
        BotCommand(command="stats", description="📊 Статистика"),
        BotCommand(command="feedback", description="💬 Оставить отзыв"),
        BotCommand(command="language", description="🌐 Сменить язык"),
    ]

    # Set default commands (Kyrgyz as default)
    await bot.set_my_commands(commands_kg, scope=BotCommandScopeDefault())

    logger.info("Bot commands menu set successfully!")


async def main():
    """Main bot function"""

    # Initialize bot and dispatcher
    bot = Bot(token=config.bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register routers (order matters - more specific handlers first)
    dp.include_router(start.router)
    dp.include_router(region.router)
    dp.include_router(help.router)
    dp.include_router(feedback.router)
    dp.include_router(stats.router)
    dp.include_router(photo.router)
    dp.include_router(schedule.router)

    # Set bot commands menu
    await set_bot_commands(bot)

    logger.info("Bot started successfully!")
    logger.info(f"Backend API URL: {config.api.base_url}")

    try:
        # Start polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Error during polling: {e}", exc_info=True)
    finally:
        # Close API client
        from services.api_client import api_client
        await api_client.close()
        # Close bot session
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
