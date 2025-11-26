"""
Handler for photo messages (crop identification).
"""
import logging
import base64
from io import BytesIO

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.irrigation import IrrigationStates
from services.api_client import api_client
from keyboards.inline import get_quick_date_keyboard
from utils.language import get_user_language

logger = logging.getLogger(__name__)

router = Router()


@router.message(IrrigationStates.waiting_for_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    """
    Handle crop photo from user.

    Args:
        message: Incoming message with photo
        state: FSM context
    """
    try:
        # Get user language
        user_lang = await get_user_language(state)

        # Send processing message
        processing_text = {
            "kg": "⏳ <b>Текшерүүдө...</b>\nСүрөттү анализдеп жатам...",
            "ru": "⏳ <b>Анализ...</b>\nАнализирую фото..."
        }
        processing_msg = await message.answer(
            processing_text.get(user_lang, processing_text["kg"]),
            parse_mode="HTML"
        )

        # Download photo (get highest quality)
        photo = message.photo[-1]

        # Check file size (Telegram Bot API limit is 20MB)
        MAX_SIZE = 10 * 1024 * 1024  # 10MB for safety
        if photo.file_size and photo.file_size > MAX_SIZE:
            await processing_msg.delete()
            error_text = {
                "kg": f"❌ <b>Сүрөт өтө чоң!</b>\n\nМаксимум өлчөм: 10MB\nСиздин сүрөт: {photo.file_size / 1024 / 1024:.1f}MB\n\nБашка сүрөт жөнөтүңүз же сапатын азайтыңыз.",
                "ru": f"❌ <b>Фото слишком большое!</b>\n\nМаксимальный размер: 10MB\nВаше фото: {photo.file_size / 1024 / 1024:.1f}MB\n\nОтправьте другое фото или уменьшите качество."
            }
            await message.answer(
                error_text.get(user_lang, error_text["kg"]),
                parse_mode="HTML"
            )
            return

        photo_file = await message.bot.download(
            photo.file_id,
            destination=BytesIO()
        )

        # Convert to base64
        photo_bytes = photo_file.getvalue()

        # Double-check actual size after download
        if len(photo_bytes) > MAX_SIZE:
            await processing_msg.delete()
            error_text = {
                "kg": "❌ <b>Сүрөт өтө чоң!</b>\n\nБашка сүрөт жөнөтүңүз же сапатын азайтыңыз.",
                "ru": "❌ <b>Фото слишком большое!</b>\n\nОтправьте другое фото или уменьшите качество."
            }
            await message.answer(
                error_text.get(user_lang, error_text["kg"]),
                parse_mode="HTML"
            )
            return

        image_base64 = base64.b64encode(photo_bytes).decode('utf-8')

        # Call backend API
        async with api_client:
            result = await api_client.analyze_crop(
                image_base64=image_base64,
                telegram_user_id=message.from_user.id
            )

        # Delete processing message
        await processing_msg.delete()

        # Check if successful
        if not result.get("success", False):
            error_msg = result.get("error", "Белгисиз ката")
            error_code = result.get("error_code", "UNKNOWN")

            if error_code == "PLANT_NOT_RECOGNIZED":
                await message.answer(
                    "❌ <b>Өсүмдүктү таный албадым</b>\n\n"
                    "Сураныч, башка сүрөт жөнөтүңүз:\n"
                    "• Өсүмдүк жакшы көрүнүш керек\n"
                    "• Жарык жетиштүү болуш керек\n"
                    "• Бир же бир нече өсүмдүк болуш керек",
                    parse_mode="HTML"
                )
            elif error_code == "UNSUPPORTED_CROP":
                await message.answer(
                    "❌ <b>Бул өсүмдүк менен иштебейм</b>\n\n"
                    f"Таанылды, бирок дагы колдоого алынган жок.\n\n"
                    "Колдоого алынган өсүмдүктөр:\n"
                    "🌾 Буудай\n"
                    "🌽 Жүгөрү\n"
                    "🥔 Картошка\n"
                    "🍅 Помидор",
                    parse_mode="HTML"
                )
            else:
                await message.answer(
                    f"❌ <b>Ката кетти</b>\n\n{error_msg}",
                    parse_mode="HTML"
                )
            return

        # Extract crop information
        crop = result["crop"]
        crop_name_kg = crop["name_kg"]
        crop_name_ru = crop["name_ru"]
        growth_stage_display = crop["growth_stage_display"]
        water_need_display = crop["water_need_display"]
        confidence = crop["confidence"]

        # Save crop data to state
        await state.update_data(
            crop_code=crop["name_code"],
            growth_stage=crop["growth_stage"],
            crop_name_kg=crop_name_kg,
            crop_name_ru=crop_name_ru
        )

        # Send result
        result_texts = {
            "kg": (
                f"✅ <b>Таанылды!</b>\n\n"
                f"🌱 <b>Өсүмдүк:</b> {crop_name_kg}\n"
                f"📊 <b>Этап:</b> {growth_stage_display}\n"
                f"💧 <b>Суу керектөө:</b> {water_need_display}\n"
                f"🎯 <b>Ишеним:</b> {int(confidence * 100)}%\n\n"
                f"<b>Качан суу келет?</b>\n"
                f"Суу берүү күнүн тандаңыз:"
            ),
            "ru": (
                f"✅ <b>Распознано!</b>\n\n"
                f"🌱 <b>Культура:</b> {crop_name_ru}\n"
                f"📊 <b>Стадия:</b> {growth_stage_display}\n"
                f"💧 <b>Потребность в воде:</b> {water_need_display}\n"
                f"🎯 <b>Уверенность:</b> {int(confidence * 100)}%\n\n"
                f"<b>Когда будет вода?</b>\n"
                f"Выберите дату полива:"
            )
        }
        await message.answer(
            result_texts.get(user_lang, result_texts["kg"]),
            reply_markup=get_quick_date_keyboard(user_lang),
            parse_mode="HTML"
        )

        # Move to next state
        await state.set_state(IrrigationStates.waiting_for_irrigation_date)

        logger.info(
            f"User {message.from_user.id} uploaded photo, "
            f"identified as {crop_name_kg}"
        )

    except Exception as e:
        logger.error(f"Error processing photo: {e}", exc_info=True)
        user_lang = await get_user_language(state)
        error_texts = {
            "kg": "❌ <b>Ката кетти</b>\n\nСүрөттү иштете албадым. Кайра аракет кылыңыз.",
            "ru": "❌ <b>Произошла ошибка</b>\n\nНе удалось обработать фото. Попробуйте еще раз."
        }
        await message.answer(
            error_texts.get(user_lang, error_texts["kg"]),
            parse_mode="HTML"
        )


@router.message(IrrigationStates.waiting_for_photo)
async def handle_non_photo(message: Message, state: FSMContext):
    """
    Handle non-photo messages when waiting for photo.

    Args:
        message: Incoming message
        state: FSM context
    """
    user_lang = await get_user_language(state)
    error_texts = {
        "kg": "📸 <b>Сүрөт жөнөтүңүз</b>\n\nТалаңыздын сүрөтүн жөнөтүш керек.",
        "ru": "📸 <b>Отправьте фото</b>\n\nНужно отправить фото вашего поля."
    }
    await message.answer(
        error_texts.get(user_lang, error_texts["kg"]),
        parse_mode="HTML"
    )
