"""
Inline keyboards for Telegram bot.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.language import get_text
from utils.regions import REGIONS, get_region_display_name


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
        [
            InlineKeyboardButton(
                text=get_text("btn_change_lang", lang),
                callback_data="change_lang"
            ),
            InlineKeyboardButton(
                text=get_text("btn_change_region", lang),
                callback_data="change_region"
            )
        ]
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
        )],
        [InlineKeyboardButton(
            text=get_text("btn_back_to_menu", lang),
            callback_data="back_to_menu"
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


def get_feedback_skip_keyboard(lang: str = "kg") -> InlineKeyboardMarkup:
    """
    Get keyboard for skipping feedback comment.

    Args:
        lang: Language code ('kg' or 'ru')

    Returns:
        InlineKeyboardMarkup: Feedback skip keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text("btn_skip_comment", lang),
            callback_data="skip_feedback_comment"
        )],
        [InlineKeyboardButton(
            text=get_text("btn_back_to_menu", lang),
            callback_data="back_to_menu"
        )]
    ])
    return keyboard


def get_region_keyboard(lang: str = "kg") -> InlineKeyboardMarkup:
    """
    Get region selection keyboard.

    Args:
        lang: Language code ('kg' or 'ru')

    Returns:
        InlineKeyboardMarkup: Region selection keyboard
    """
    # Create buttons for each region (2 per row)
    buttons = []
    region_list = list(REGIONS.keys())

    for i in range(0, len(region_list), 2):
        row = []
        for j in range(2):
            if i + j < len(region_list):
                region_code = region_list[i + j]
                region_info = REGIONS[region_code]
                display_name = get_region_display_name(region_code, lang)
                emoji = region_info.get("emoji", "")

                row.append(InlineKeyboardButton(
                    text=f"{emoji} {display_name}",
                    callback_data=f"region_{region_code}"
                ))
        buttons.append(row)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
