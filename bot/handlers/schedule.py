"""
Handler for irrigation schedule (date selection).
"""
import logging
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import dateparser

from states.irrigation import IrrigationStates
from services.api_client import api_client
from keyboards.inline import get_back_to_menu_keyboard
from utils.language import get_user_language, set_user_language, get_text

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(IrrigationStates.waiting_for_irrigation_date, F.data.startswith("date_"))
async def handle_quick_date(callback: CallbackQuery, state: FSMContext):
    """
    Handle quick date selection buttons.

    Args:
        callback: Callback query
        state: FSM context
    """
    # Get user language
    user_lang = await get_user_language(state)

    date_type = callback.data.split("_", 1)[1]  # e.g., "today", "tomorrow"

    today = datetime.now().date()

    if date_type == "today":
        selected_date = today
    elif date_type == "tomorrow":
        selected_date = today + timedelta(days=1)
    elif date_type == "day_after":
        selected_date = today + timedelta(days=2)
    elif date_type == "this_week":
        # Find next Friday (common water day)
        days_until_friday = (4 - today.weekday()) % 7
        if days_until_friday == 0:
            days_until_friday = 7
        selected_date = today + timedelta(days=days_until_friday)
    elif date_type == "custom":
        await callback.answer()
        await callback.message.edit_text(
            get_text("date_prompt_custom", user_lang),
            parse_mode="HTML"
        )
        return
    else:
        await callback.answer(get_text("date_error", user_lang))
        return

    await callback.answer()

    # Process the selected date
    await process_irrigation_date(
        callback.message,
        state,
        selected_date.strftime("%Y-%m-%d"),
        callback.from_user.id
    )


@router.message(IrrigationStates.waiting_for_irrigation_date)
async def handle_text_date(message: Message, state: FSMContext):
    """
    Handle text date input from user.

    Args:
        message: Incoming message
        state: FSM context
    """
    # Get user language
    user_lang = await get_user_language(state)

    user_text = message.text.strip()

    # Parse date using dateparser (supports Kyrgyz and Russian)
    parsed_date = dateparser.parse(
        user_text,
        languages=['kg', 'ru', 'en'],
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.now()
        }
    )

    if not parsed_date:
        await message.answer(
            get_text("date_invalid", user_lang),
            parse_mode="HTML"
        )
        return

    # Check if date is not too far in future (max 7 days for weather forecast)
    days_diff = (parsed_date.date() - datetime.now().date()).days
    if days_diff > 7:
        await message.answer(
            get_text("date_too_far", user_lang),
            parse_mode="HTML"
        )
        return

    if days_diff < 0:
        await message.answer(
            get_text("date_in_past", user_lang),
            parse_mode="HTML"
        )
        return

    # Process the date
    await process_irrigation_date(
        message,
        state,
        parsed_date.strftime("%Y-%m-%d"),
        message.from_user.id
    )


async def process_irrigation_date(
    message: Message,
    state: FSMContext,
    water_date: str,
    user_id: int
):
    """
    Process irrigation date and get recommendation from backend.

    Args:
        message: Message to reply to
        state: FSM context
        water_date: ISO date string (YYYY-MM-DD)
        user_id: Telegram user ID
    """
    try:
        # Get user language
        user_lang = await get_user_language(state)

        # Get saved crop data
        data = await state.get_data()
        crop_code = data.get("crop_code")
        growth_stage = data.get("growth_stage")
        crop_name_kg = data.get("crop_name_kg")
        crop_name_ru = data.get("crop_name_ru")

        if not crop_code or not growth_stage:
            await message.answer(
                get_text("error_no_crop_data", user_lang)
            )
            return

        # Send processing message
        processing_msg = await message.answer(
            get_text("processing_schedule", user_lang),
            parse_mode="HTML"
        )

        # Call backend API
        async with api_client:
            result = await api_client.get_water_schedule(
                crop_code=crop_code,
                growth_stage=growth_stage,
                water_date=water_date,
                telegram_user_id=user_id
            )

        # Delete processing message
        await processing_msg.delete()

        # Check if successful
        if not result.get("success", False):
            error_msg = result.get("error", get_text("error_unknown", user_lang))
            await message.answer(
                f"{get_text('error_occurred', user_lang)}\n\n{error_msg}",
                parse_mode="HTML"
            )
            return

        # Extract recommendation
        water_date_display = result["water_date_display"]
        days_until = result["days_until_water"]
        weather = result["weather"]
        recommendation = result["recommendation"]

        # Select crop name based on language
        crop_name = crop_name_kg if user_lang == "kg" else crop_name_ru

        # Format message in user's language
        if user_lang == "ru":
            response_text = (
                f"💧 <b>Рекомендация по поливу</b>\n\n"
                f"🌱 <b>Культура:</b> {crop_name}\n"
                f"📅 <b>День полива:</b> {water_date_display}\n"
                f"⏰ <b>Осталось дней:</b> {days_until}\n\n"
                f"🌡️ <b>Погода:</b>\n"
                f"• Температура: {weather['temp_avg']}°C\n"
                f"• Осадки: {weather['precipitation_mm']} мм\n"
                f"• {weather['condition']}\n\n"
                f"💦 <b>Объем воды:</b> {recommendation['liters_per_sotka']} литров/сотка\n"
                f"🚨 <b>Срочность:</b> {recommendation['urgency_display']}\n"
                f"🔄 <b>Следующий полив:</b> через {recommendation['next_watering_days']} дней\n\n"
                f"<b>Совет:</b>\n{recommendation['message_ru']}"
            )
        else:
            response_text = (
                f"💧 <b>Суу берүү кеңеши</b>\n\n"
                f"🌱 <b>Өсүмдүк:</b> {crop_name}\n"
                f"📅 <b>Суу күнү:</b> {water_date_display}\n"
                f"⏰ <b>Канча күн калды:</b> {days_until}\n\n"
                f"🌡️ <b>Аба ырайы:</b>\n"
                f"• Температура: {weather['temp_avg']}°C\n"
                f"• Жаан: {weather['precipitation_mm']} мм\n"
                f"• {weather['condition']}\n\n"
                f"💦 <b>Суу көлөмү:</b> {recommendation['liters_per_sotka']} литр/сотка\n"
                f"🚨 <b>Шашылыштык:</b> {recommendation['urgency_display']}\n"
                f"🔄 <b>Кийинки суу:</b> {recommendation['next_watering_days']} күндөн кийин\n\n"
                f"<b>Кеңеш:</b>\n{recommendation['message_kg']}"
            )

        await message.answer(
            response_text,
            reply_markup=get_back_to_menu_keyboard(user_lang),
            parse_mode="HTML"
        )

        # Clear state but preserve language
        await state.clear()
        await set_user_language(state, user_lang)

        logger.info(
            f"User {user_id} got recommendation for "
            f"{crop_name} on {water_date}"
        )

    except Exception as e:
        logger.error(f"Error processing irrigation date: {e}", exc_info=True)
        user_lang = await get_user_language(state)
        await message.answer(
            get_text("error_getting_recommendation", user_lang),
            parse_mode="HTML"
        )
