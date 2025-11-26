"""
Inline keyboards for Telegram bot.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Get main menu keyboard.

    Returns:
        InlineKeyboardMarkup: Main menu keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Жаңы талаа текшерүү", callback_data="new_check")],
        [InlineKeyboardButton(text="ℹ️ Маалымат", callback_data="info")],
        [InlineKeyboardButton(text="🌐 Тилди өзгөртүү", callback_data="change_lang")]
    ])
    return keyboard


def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Get language selection keyboard.

    Returns:
        InlineKeyboardMarkup: Language selection keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="lang_kg")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="⬅️ Артка", callback_data="back_to_menu")]
    ])
    return keyboard


def get_quick_date_keyboard() -> InlineKeyboardMarkup:
    """
    Get quick date selection keyboard.

    Returns:
        InlineKeyboardMarkup: Quick date selection keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Бүгүн", callback_data="date_today"),
            InlineKeyboardButton(text="Эртең", callback_data="date_tomorrow")
        ],
        [
            InlineKeyboardButton(text="Арада бир күн", callback_data="date_day_after"),
            InlineKeyboardButton(text="Ушул жумада", callback_data="date_this_week")
        ],
        [InlineKeyboardButton(text="✍️ Өзүм жазам", callback_data="date_custom")]
    ])
    return keyboard


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Get back to menu keyboard.

    Returns:
        InlineKeyboardMarkup: Back to menu keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Башкы менюга", callback_data="back_to_menu")]
    ])
    return keyboard
