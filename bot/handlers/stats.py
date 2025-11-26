"""Statistics command for demo."""
import logging
from datetime import datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.language import get_user_language, get_text

logger = logging.getLogger(__name__)
router = Router()

# Fake stats for demo (replace with DB later)
DEMO_STATS = {
    "total_users": 127,
    "total_analyses": 456,
    "water_saved_m3": 12450,
    "avg_confidence": 0.91,
    "top_crops": {
        "kg": [
            ("🌽 Жүгөрү", 182),
            ("🌾 Буудай", 145),
            ("🍅 Помидор", 89),
            ("🥔 Картошка", 40)
        ],
        "ru": [
            ("🌽 Кукуруза", 182),
            ("🌾 Пшеница", 145),
            ("🍅 Помидор", 89),
            ("🥔 Картофель", 40)
        ]
    }
}

@router.message(Command("stats"))
async def cmd_stats(message: Message, state: FSMContext):
    """Show demo statistics."""
    # Get user language
    user_lang = await get_user_language(state)
    stats = DEMO_STATS

    response = (
        get_text("stats_title", user_lang) + "\n\n" +
        get_text("stats_users", user_lang).format(count=stats['total_users']) + "\n" +
        get_text("stats_analyses", user_lang).format(count=stats['total_analyses']) + "\n" +
        get_text("stats_water_saved", user_lang).format(amount=stats['water_saved_m3']) + "\n" +
        get_text("stats_accuracy", user_lang).format(percent=int(stats['avg_confidence'] * 100)) + "\n\n" +
        get_text("stats_popular_crops", user_lang) + "\n"
    )

    for crop, count in stats["top_crops"][user_lang]:
        response += f"{crop}: {count} " + get_text("stats_analysis_count", user_lang).format(count=count) + "\n"

    response += get_text("stats_footer", user_lang).format(tons=stats['water_saved_m3'] / 1000)

    await message.answer(response, parse_mode="HTML")


# Admin-only detailed stats
@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message, state: FSMContext):
    """Admin statistics (for your own viewing during demo)."""
    # Add your Telegram ID here for security
    # Get it by sending /start and checking logs
    # For demo, allow everyone

    # Get user language
    user_lang = await get_user_language(state)

    response = (
        get_text("admin_stats_title", user_lang) + "\n\n" +
        get_text("admin_system_health", user_lang) + "\n" +
        get_text("admin_backend_online", user_lang) + "\n" +
        get_text("admin_bot_running", user_lang) + "\n" +
        get_text("admin_mock_mode", user_lang) + "\n\n" +
        get_text("admin_quick_stats", user_lang) + "\n" +
        get_text("admin_your_id", user_lang).format(user_id=message.from_user.id) + "\n" +
        get_text("admin_your_name", user_lang).format(name=message.from_user.full_name) + "\n\n" +
        get_text("admin_next_steps", user_lang) + "\n" +
        get_text("admin_steps_list", user_lang)
    )

    await message.answer(response, parse_mode="HTML")
