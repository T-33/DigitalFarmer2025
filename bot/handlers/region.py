"""
Handler for region selection.
Allows users to select their region (oblast) in Kyrgyzstan.
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.language import get_user_language, get_text
from utils.regions import (
    REGIONS,
    get_region_info,
    get_region_display_name,
    get_region_stats
)
from keyboards.inline import get_region_keyboard, get_back_to_menu_keyboard

logger = logging.getLogger(__name__)
router = Router()


async def ask_region(message: Message, state: FSMContext):
    """
    Ask user to select their region.

    Args:
        message: Message to reply to
        state: FSM context
    """
    user_lang = await get_user_language(state)

    await message.answer(
        get_text("select_region", user_lang),
        reply_markup=get_region_keyboard(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("region_"))
async def handle_region_selection(callback: CallbackQuery, state: FSMContext):
    """
    Handle region selection.

    Args:
        callback: Callback query
        state: FSM context
    """
    region_code = callback.data.split("_", 1)[1]

    # Validate region code
    if region_code not in REGIONS:
        await callback.answer("Invalid region")
        return

    # Save region to state
    await state.update_data(region=region_code)

    user_lang = await get_user_language(state)
    region_name = get_region_display_name(region_code, user_lang)
    region_info = get_region_info(region_code)

    # Get region stats
    stats = get_region_stats(region_code)

    # Acknowledge selection
    await callback.answer(
        get_text("region_selected", user_lang).format(region=region_name)
    )

    # Show region info with statistics
    response_text = get_text("region_info", user_lang).format(
        emoji=region_info["emoji"],
        region=region_name,
        elevation=region_info["elevation"],
        users=stats["users"],
        analyses=stats["analyses"],
        water_saved=stats["water_saved_m3"]
    )

    await callback.message.edit_text(
        response_text,
        parse_mode="HTML"
    )

    # Ask for photo
    await callback.message.answer(
        get_text("send_photo", user_lang),
        parse_mode="HTML"
    )

    logger.info(f"User {callback.from_user.id} selected region: {region_code}")


@router.callback_query(F.data == "change_region")
async def handle_change_region(callback: CallbackQuery, state: FSMContext):
    """
    Handle region change request.

    Args:
        callback: Callback query
        state: FSM context
    """
    await callback.answer()

    user_lang = await get_user_language(state)

    await callback.message.edit_text(
        get_text("select_region", user_lang),
        reply_markup=get_region_keyboard(user_lang),
        parse_mode="HTML"
    )
