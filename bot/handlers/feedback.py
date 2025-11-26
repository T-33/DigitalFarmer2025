"""
Feedback collection handler.
Allows users to rate the bot and leave comments.
"""
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.language import get_user_language, get_text

logger = logging.getLogger(__name__)
router = Router()


class FeedbackStates(StatesGroup):
    """FSM states for feedback collection."""
    waiting_for_rating = State()
    waiting_for_comment = State()


@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    """
    Start feedback collection process.

    Args:
        message: Incoming message
        state: FSM context
    """
    user_lang = await get_user_language(state)

    # Create rating keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="rating_5"),
            InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data="rating_4")
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐", callback_data="rating_3"),
            InlineKeyboardButton(text="⭐⭐", callback_data="rating_2")
        ],
        [InlineKeyboardButton(text="⭐", callback_data="rating_1")]
    ])

    await message.answer(
        get_text("feedback_prompt", user_lang),
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await state.set_state(FeedbackStates.waiting_for_rating)

    logger.info(f"User {message.from_user.id} started feedback")


@router.callback_query(FeedbackStates.waiting_for_rating, F.data.startswith("rating_"))
async def handle_rating(callback: CallbackQuery, state: FSMContext):
    """
    Handle rating selection.

    Args:
        callback: Callback query
        state: FSM context
    """
    rating = int(callback.data.split("_")[1])
    await state.update_data(rating=rating)

    user_lang = await get_user_language(state)

    from keyboards.inline import get_feedback_skip_keyboard

    await callback.answer()
    await callback.message.edit_text(
        get_text("feedback_comment_prompt", user_lang).format(stars="⭐" * rating),
        reply_markup=get_feedback_skip_keyboard(user_lang),
        parse_mode="HTML"
    )

    await state.set_state(FeedbackStates.waiting_for_comment)


@router.callback_query(FeedbackStates.waiting_for_comment, F.data == "skip_feedback_comment")
async def skip_comment_callback(callback: CallbackQuery, state: FSMContext):
    """
    Skip comment and finish feedback (via callback button).

    Args:
        callback: Callback query
        state: FSM context
    """
    data = await state.get_data()
    rating = data.get("rating", 0)

    # Log feedback (in production, save to database)
    logger.info(
        f"Feedback from {callback.from_user.id}: {rating} stars, no comment"
    )

    user_lang = await get_user_language(state)

    from keyboards.inline import get_back_to_menu_keyboard

    await callback.answer()
    await callback.message.edit_text(
        get_text("feedback_thanks", user_lang),
        reply_markup=get_back_to_menu_keyboard(user_lang),
        parse_mode="HTML"
    )

    await state.clear()


@router.message(FeedbackStates.waiting_for_comment, Command("skip"))
async def skip_comment(message: Message, state: FSMContext):
    """
    Skip comment and finish feedback (via command).

    Args:
        message: Incoming message
        state: FSM context
    """
    data = await state.get_data()
    rating = data.get("rating", 0)

    # Log feedback (in production, save to database)
    logger.info(
        f"Feedback from {message.from_user.id}: {rating} stars, no comment"
    )

    user_lang = await get_user_language(state)

    from keyboards.inline import get_back_to_menu_keyboard

    await message.answer(
        get_text("feedback_thanks", user_lang),
        reply_markup=get_back_to_menu_keyboard(user_lang),
        parse_mode="HTML"
    )

    await state.clear()


@router.message(FeedbackStates.waiting_for_comment)
async def handle_comment(message: Message, state: FSMContext):
    """
    Handle feedback comment.

    Args:
        message: Incoming message
        state: FSM context
    """
    data = await state.get_data()
    rating = data.get("rating", 0)
    comment = message.text

    # Log feedback (in production, save to database)
    logger.info(
        f"Feedback from {message.from_user.id}: {rating} stars\n"
        f"Comment: {comment}"
    )

    user_lang = await get_user_language(state)

    from keyboards.inline import get_back_to_menu_keyboard

    await message.answer(
        get_text("feedback_thanks_detailed", user_lang),
        reply_markup=get_back_to_menu_keyboard(user_lang),
        parse_mode="HTML"
    )

    await state.clear()
