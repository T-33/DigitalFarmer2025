"""
Help command handler.
Displays usage instructions and available commands.
"""
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.language import get_user_language, get_text

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    """
    Show help information.

    Args:
        message: Incoming message
        state: FSM context
    """
    user_lang = await get_user_language(state)

    help_text = get_text("help", user_lang)

    await message.answer(help_text, parse_mode="HTML")

    logger.info(f"User {message.from_user.id} requested help")
