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
            "✍️ <b>Датаны жазыңыз</b>\n\n"
            "Мисалдар:\n"
            "• Бүгүн\n"
            "• Эртең\n"
            "• Шаршемби\n"
            "• 29 ноябрь\n"
            "• 2025-11-29",
            parse_mode="HTML"
        )
        return
    else:
        await callback.answer("Ката!")
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
            "❌ <b>Датаны түшүнбөдүм</b>\n\n"
            "Мисалдар:\n"
            "• Бүгүн\n"
            "• Эртең\n"
            "• Шаршемби\n"
            "• 29 ноябрь",
            parse_mode="HTML"
        )
        return

    # Check if date is not too far in future (max 7 days for weather forecast)
    days_diff = (parsed_date.date() - datetime.now().date()).days
    if days_diff > 7:
        await message.answer(
            "❌ <b>Дата өтө алыс</b>\n\n"
            "Аба ырайын 7 күнгө гана билем.\n"
            "Жакынкы датаны тандаңыз.",
            parse_mode="HTML"
        )
        return

    if days_diff < 0:
        await message.answer(
            "❌ <b>Дата өткөн</b>\n\n"
            "Келечектеги датаны тандаңыз.",
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
        # Get saved crop data
        data = await state.get_data()
        crop_code = data.get("crop_code")
        growth_stage = data.get("growth_stage")
        crop_name_kg = data.get("crop_name_kg")

        if not crop_code or not growth_stage:
            await message.answer(
                "❌ Ката: өсүмдүк маалыматы жок. /start баскычын басыңыз."
            )
            return

        # Send processing message
        processing_msg = await message.answer(
            "⏳ <b>Эсептеп жатам...</b>\n"
            "Аба ырайын текшерүүдө...",
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
            error_msg = result.get("error", "Белгисиз ката")
            await message.answer(
                f"❌ <b>Ката кетти</b>\n\n{error_msg}",
                parse_mode="HTML"
            )
            return

        # Extract recommendation
        water_date_display = result["water_date_display"]
        days_until = result["days_until_water"]
        weather = result["weather"]
        recommendation = result["recommendation"]

        # Format message
        response_text = (
            f"💧 <b>Суу берүү кеңеши</b>\n\n"
            f"🌱 <b>Өсүмдүк:</b> {crop_name_kg}\n"
            f"📅 <b>Суу күнү:</b> {water_date_display}\n"
            f"⏰ <b>Канча күн калды:</b> {days_until} күн\n\n"
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
            reply_markup=get_back_to_menu_keyboard(),
            parse_mode="HTML"
        )

        # Clear state
        await state.clear()

        logger.info(
            f"User {user_id} got recommendation for "
            f"{crop_name_kg} on {water_date}"
        )

    except Exception as e:
        logger.error(f"Error processing irrigation date: {e}", exc_info=True)
        await message.answer(
            "❌ <b>Ката кетти</b>\n\n"
            "Кеңешти алуу мүмкүн болбоду. Кайра аракет кылыңыз.",
            parse_mode="HTML"
        )
