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
from utils.language import get_user_language, get_text

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
        processing_msg = await message.answer(
            get_text("processing_photo", user_lang),
            parse_mode="HTML"
        )

        # Download photo (get highest quality)
        photo = message.photo[-1]

        # Check file size (Telegram Bot API limit is 20MB)
        MAX_SIZE = 10 * 1024 * 1024  # 10MB for safety
        if photo.file_size and photo.file_size > MAX_SIZE:
            await processing_msg.delete()
            file_size_mb = photo.file_size / 1024 / 1024
            from keyboards.inline import get_back_to_menu_keyboard
            await message.answer(
                get_text("photo_too_large_details", user_lang).format(size=file_size_mb),
                reply_markup=get_back_to_menu_keyboard(user_lang),
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
            from keyboards.inline import get_back_to_menu_keyboard
            await message.answer(
                get_text("photo_too_large", user_lang),
                reply_markup=get_back_to_menu_keyboard(user_lang),
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
            error_msg = result.get("error", get_text("error_unknown", user_lang))
            error_code = result.get("error_code", "UNKNOWN")

            from keyboards.inline import get_back_to_menu_keyboard

            if error_code == "PLANT_NOT_RECOGNIZED":
                await message.answer(
                    get_text("plant_not_recognized", user_lang),
                    reply_markup=get_back_to_menu_keyboard(user_lang),
                    parse_mode="HTML"
                )
            elif error_code == "UNSUPPORTED_CROP":
                await message.answer(
                    get_text("unsupported_crop", user_lang),
                    reply_markup=get_back_to_menu_keyboard(user_lang),
                    parse_mode="HTML"
                )
            else:
                await message.answer(
                    get_text("error_generic", user_lang).format(error=error_msg),
                    reply_markup=get_back_to_menu_keyboard(user_lang),
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
        crop_name = crop_name_kg if user_lang == "kg" else crop_name_ru
        await message.answer(
            get_text("crop_identified", user_lang).format(
                crop_name=crop_name,
                growth_stage=growth_stage_display,
                water_need=water_need_display,
                confidence=int(confidence * 100)
            ),
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
        from keyboards.inline import get_back_to_menu_keyboard
        await message.answer(
            get_text("error_processing_photo", user_lang),
            reply_markup=get_back_to_menu_keyboard(user_lang),
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
    await message.answer(
        get_text("need_photo", user_lang),
        parse_mode="HTML"
    )
