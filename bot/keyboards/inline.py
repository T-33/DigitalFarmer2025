"""
Inline keyboards for Telegram bot.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.language import get_text


def get_main_menu_keyboard(lang: str = "kg") -> InlineKeyboardMarkup:
    """
    Get main menu keyboard.

    Args:
        lang: Language code ('kg' or 'ru')

    Returns:
        InlineKeyboardMarkup: Main menu keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text("btn_new_check", lang),
            callback_data="new_check"
        )],
        [InlineKeyboardButton(
            text=get_text("btn_info", lang),
            callback_data="info"
        )],
        [InlineKeyboardButton(
            text=get_text("btn_change_lang", lang),
            callback_data="change_lang"
        )]
    ])
    return keyboard


def get_language_keyboard(lang: str = "kg") -> InlineKeyboardMarkup:
    """
    Get language selection keyboard.

    Args:
        lang: Language code ('kg' or 'ru')

    Returns:
        InlineKeyboardMarkup: Language selection keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="lang_kg")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(
            text=get_text("btn_back", lang),
            callback_data="back_to_menu"
        )]
    ])
    return keyboard


def get_quick_date_keyboard(lang: str = "kg") -> InlineKeyboardMarkup:
    """
    Get quick date selection keyboard.

    Args:
        lang: Language code ('kg' or 'ru')

    Returns:
        InlineKeyboardMarkup: Quick date selection keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_text("btn_today", lang),
                callback_data="date_today"
            ),
            InlineKeyboardButton(
                text=get_text("btn_tomorrow", lang),
                callback_data="date_tomorrow"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_day_after", lang),
                callback_data="date_day_after"
            ),
            InlineKeyboardButton(
                text=get_text("btn_this_week", lang),
                callback_data="date_this_week"
            )
        ],
        [InlineKeyboardButton(
            text=get_text("btn_custom", lang),
            callback_data="date_custom"
        )]
    ])
    return keyboard


def get_back_to_menu_keyboard(lang: str = "kg") -> InlineKeyboardMarkup:
    """
    Get back to menu keyboard.

    Args:
        lang: Language code ('kg' or 'ru')

    Returns:
        InlineKeyboardMarkup: Back to menu keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text("btn_back_to_menu", lang),
            callback_data="back_to_menu"
        )]
    ])
    return keyboard
