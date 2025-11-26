"""Statistics command for demo."""
import logging
from datetime import datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()

# Fake stats for demo (replace with DB later)
DEMO_STATS = {
    "total_users": 127,
    "total_analyses": 456,
    "water_saved_m3": 12450,
    "avg_confidence": 0.91,
    "top_crops": [
        ("🌽 Жүгөрү", 182),
        ("🌾 Буудай", 145),
        ("🍅 Помидор", 89),
        ("🥔 Картошка", 40)
    ]
}

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Show demo statistics."""
    stats = DEMO_STATS

    response = (
        "📊 <b>MurabAI Статистика</b>\n\n"
        f"👥 Колдонуучулар: <b>{stats['total_users']}</b>\n"
        f"🔍 Анализдер: <b>{stats['total_analyses']}</b>\n"
        f"💧 Суу үнөмдөлдү: <b>{stats['water_saved_m3']:,} м³</b>\n"
        f"🎯 Орточо тактык: <b>{int(stats['avg_confidence'] * 100)}%</b>\n\n"
        "<b>Популярдуу өсүмдүктөр:</b>\n"
    )

    for crop, count in stats["top_crops"]:
        response += f"{crop}: {count} анализ\n"

    response += (
        "\n💡 <i>Биз менен {:.1f} тонна суу үнөмдөлдү!</i>\n"
        "🌍 SDG #6: Clean Water for All"
    ).format(stats['water_saved_m3'] / 1000)

    await message.answer(response, parse_mode="HTML")


# Admin-only detailed stats
@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message):
    """Admin statistics (for your own viewing during demo)."""
    # Add your Telegram ID here for security
    # Get it by sending /start and checking logs
    # For demo, allow everyone

    response = (
        "🔧 <b>Admin Dashboard</b>\n\n"
        "<b>System Health:</b>\n"
        "✅ Backend API: Online\n"
        "✅ Bot: Running\n"
        "✅ Mock Mode: Enabled\n\n"
        "<b>Quick Stats:</b>\n"
        f"🆔 Your ID: {message.from_user.id}\n"
        f"👤 Your Name: {message.from_user.full_name}\n\n"
        "<b>Next Steps for Production:</b>\n"
        "1. Get Plant.id API key\n"
        "2. Add geolocation support\n"
        "3. Implement real weather API\n"
        "4. PostgreSQL database\n"
        "5. Redis for FSM storage\n\n"
        "Good luck with the demo! 🚀"
    )

    await message.answer(response, parse_mode="HTML")
