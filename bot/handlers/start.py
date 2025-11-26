"""
Handler for /start command and main menu.
"""
import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import (
    get_main_menu_keyboard,
    get_language_keyboard,
    get_back_to_menu_keyboard
)
from states.irrigation import IrrigationStates
from utils.language import get_user_language, set_user_language, get_text

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    Handle /start command.

    Args:
        message: Incoming message
        state: FSM context
    """
    await state.clear()

    # Get user language (defaults to 'kg' if not set)
    user_lang = await get_user_language(state)

    # Set language if not set yet
    if not await state.get_data():
        await set_user_language(state, "kg")
        user_lang = "kg"

    welcome_text = get_text("welcome", user_lang)

    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard(user_lang),
        parse_mode="HTML"
    )

    # Set state to waiting for photo
    await state.set_state(IrrigationStates.waiting_for_photo)

    logger.info(f"User {message.from_user.id} started the bot")


@router.callback_query(F.data == "new_check")
async def callback_new_check(callback: CallbackQuery, state: FSMContext):
    """
    Handle 'New check' button.

    Args:
        callback: Callback query
        state: FSM context
    """
    await callback.answer()

    # Get user language
    user_lang = await get_user_language(state)

    await callback.message.edit_text(
        get_text("send_photo", user_lang),
        parse_mode="HTML"
    )

    await state.set_state(IrrigationStates.waiting_for_photo)


@router.callback_query(F.data == "info")
async def callback_info(callback: CallbackQuery, state: FSMContext):
    """
    Handle 'Info' button.

    Args:
        callback: Callback query
        state: FSM context
    """
    await callback.answer()

    # Get user language
    user_lang = await get_user_language(state)

    await callback.message.edit_text(
        get_text("info", user_lang),
        reply_markup=get_back_to_menu_keyboard(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "change_lang")
async def callback_change_lang(callback: CallbackQuery, state: FSMContext):
    """
    Handle 'Change language' button.

    Args:
        callback: Callback query
        state: FSM context
    """
    await callback.answer()

    # Get current language
    user_lang = await get_user_language(state)

    await callback.message.edit_text(
        get_text("select_language", user_lang),
        reply_markup=get_language_keyboard(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("lang_"))
async def callback_set_language(callback: CallbackQuery, state: FSMContext):
    """
    Handle language selection.

    Args:
        callback: Callback query
        state: FSM context
    """
    lang = callback.data.split("_")[1]  # Extract 'kg' or 'ru'

    # Save language preference to state
    await set_user_language(state, lang)

    await callback.answer(
        get_text("language_changed", lang),
        show_alert=True
    )

    # Return to main menu with new language
    welcome_text = get_text("welcome", lang)

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML"
    )

    # Keep state as waiting for photo
    await state.set_state(IrrigationStates.waiting_for_photo)


@router.callback_query(F.data == "back_to_menu")
async def callback_back_to_menu(callback: CallbackQuery, state: FSMContext):
    """
    Handle 'Back to menu' button.

    Args:
        callback: Callback query
        state: FSM context
    """
    await callback.answer()

    # Get user language BEFORE clearing
    user_lang = await get_user_language(state)

    # Clear state but preserve language
    await state.clear()
    await set_user_language(state, user_lang)

    welcome_text = get_text("welcome", user_lang)

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(user_lang),
        parse_mode="HTML"
    )

    # Set state back to waiting for photo
    await state.set_state(IrrigationStates.waiting_for_photo)
