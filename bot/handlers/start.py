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
    get_language_keyboard
)
from states.irrigation import IrrigationStates

logger = logging.getLogger(__name__)

router = Router()


WELCOME_MESSAGE_KG = """
🌱 <b>MurabAI'га кош келиңиз!</b>

Мен сиздин талаңызга карап, канча суу керектигин айтып берем.

<b>Мен кандай жардам бере алам:</b>
✅ Өсүмдүктү таанып алам (фото боюнча)
✅ Аба ырайын текшерем
✅ Суу көлөмүн эсептейм
✅ Кеңештерди беремин

<b>Баштоо үчүн талаңыздын сүрөтүн жөнөтүңүз 📸</b>
"""

WELCOME_MESSAGE_RU = """
🌱 <b>Добро пожаловать в MurabAI!</b>

Я помогу определить, сколько воды нужно вашему полю.

<b>Что я умею:</b>
✅ Распознаю культуры по фото
✅ Проверяю прогноз погоды
✅ Рассчитываю объем воды
✅ Даю рекомендации

<b>Отправьте фото вашего поля, чтобы начать 📸</b>
"""

INFO_MESSAGE_KG = """
ℹ️ <b>MurabAI жөнүндө</b>

<b>Биздин максат:</b>
Кыргызстандагы дыйкандарга сууну үнөмдөөгө жана түшүмдүүлүктү жогорулатууга жардам берүү.

<b>Кантип иштейт:</b>
1. Талаңыздын сүрөтүн жөнөтөсүз
2. Биз өсүмдүктү таанып алабыз
3. Сиз суу качан келерин айтасыз
4. Биз аба ырайын текшерип, кеңеш беребиз

<b>Артыкчылыктар:</b>
💧 30%га чейин суу үнөмдөө
📈 15%га чейин түшүмдүүлүктү жогорулатуу
🌍 Экологияга пайда

Долбоор: Farmers Hackathon 2025
"""


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    Handle /start command.

    Args:
        message: Incoming message
        state: FSM context
    """
    await state.clear()

    # TODO: Get user language preference from database
    # For now, default to Kyrgyz
    user_lang = "kg"

    welcome_text = WELCOME_MESSAGE_KG if user_lang == "kg" else WELCOME_MESSAGE_RU

    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
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

    await callback.message.edit_text(
        "📸 <b>Талаңыздын сүрөтүн жөнөтүңүз</b>\n\n"
        "Өсүмдүктөр жакшы көрүнүш керек.",
        parse_mode="HTML"
    )

    await state.set_state(IrrigationStates.waiting_for_photo)


@router.callback_query(F.data == "info")
async def callback_info(callback: CallbackQuery):
    """
    Handle 'Info' button.

    Args:
        callback: Callback query
    """
    await callback.answer()

    from keyboards.inline import get_back_to_menu_keyboard

    await callback.message.edit_text(
        INFO_MESSAGE_KG,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "change_lang")
async def callback_change_lang(callback: CallbackQuery):
    """
    Handle 'Change language' button.

    Args:
        callback: Callback query
    """
    await callback.answer()

    await callback.message.edit_text(
        "🌐 <b>Тилди тандаңыз / Выберите язык:</b>",
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("lang_"))
async def callback_set_language(callback: CallbackQuery):
    """
    Handle language selection.

    Args:
        callback: Callback query
    """
    lang = callback.data.split("_")[1]  # Extract 'kg' or 'ru'

    # TODO: Save language preference to database

    await callback.answer(
        "✅ Тил өзгөртүлдү!" if lang == "kg" else "✅ Язык изменён!",
        show_alert=True
    )

    # Return to main menu
    welcome_text = WELCOME_MESSAGE_KG if lang == "kg" else WELCOME_MESSAGE_RU

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "back_to_menu")
async def callback_back_to_menu(callback: CallbackQuery, state: FSMContext):
    """
    Handle 'Back to menu' button.

    Args:
        callback: Callback query
        state: FSM context
    """
    await callback.answer()

    # Clear state
    await state.clear()

    # TODO: Get user language
    user_lang = "kg"
    welcome_text = WELCOME_MESSAGE_KG if user_lang == "kg" else WELCOME_MESSAGE_RU

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )

    # Set state back to waiting for photo
    await state.set_state(IrrigationStates.waiting_for_photo)
