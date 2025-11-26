# Tamchy AI - API Contract v1.0

**Base URL:** `http://localhost:8000/api/v1`

This document defines the contract between the Telegram Bot and Backend API services.

---

## 📋 Endpoints Overview

| Method | Endpoint | Description | Bot Usage |
|--------|----------|-------------|-----------|
| GET | `/health` | Health check | Startup verification |
| POST | `/analyze-crop` | Identify crop from photo | After user sends photo |
| POST | `/water-schedule` | Calculate irrigation plan | After user provides date |

---

## 1. GET /health

Health check endpoint to verify backend is running and external APIs are accessible.

### Request
No parameters required.

### Response 200 (Success)
```json
{
  "status": "ok",
  "plant_id_api": "connected",
  "weather_api": "connected"
}
```

### Response 503 (Service Unavailable)
```json
{
  "status": "error",
  "plant_id_api": "disconnected",
  "weather_api": "connected"
}
```

### Usage Example
```python
# Bot startup check
response = await http_client.get(f"{BACKEND_URL}/health")
if response.status_code != 200:
    logger.error("Backend is not healthy!")
```

---

## 2. POST /analyze-crop

Analyzes a crop photo using Plant.id API and returns crop information.

### Request Body
```json
{
  "image_base64": "string (base64 encoded image)",
  "telegram_user_id": 123456789
}
```

**Field Descriptions:**
- `image_base64` (required): Image encoded in base64 format (JPEG, PNG)
- `telegram_user_id` (required): Telegram user ID for analytics/logging

### Response 200 (Success)
```json
{
  "success": true,
  "crop": {
    "name_ru": "Кукуруза",
    "name_kg": "Жүгөрү",
    "name_code": "corn",
    "confidence": 0.94,
    "growth_stage": "flowering",
    "growth_stage_display": "Цветение 🌸",
    "water_need": "high",
    "water_need_display": "🔴 Высокая"
  }
}
```

**Field Descriptions:**
- `success`: Always `true` for successful identification
- `crop.name_ru`: Crop name in Russian
- `crop.name_kg`: Crop name in Kyrgyz
- `crop.name_code`: Internal crop code (e.g., "corn", "wheat", "cotton")
- `crop.confidence`: Identification confidence (0.0 to 1.0)
- `crop.growth_stage`: Internal stage code ("initial", "development", "flowering", "maturation")
- `crop.growth_stage_display`: Localized display text with emoji
- `crop.water_need`: Water need level ("low", "medium", "high")
- `crop.water_need_display`: Localized display text with emoji

### Response 400 (Plant Not Recognized)
```json
{
  "success": false,
  "error": "Could not identify plant",
  "error_code": "PLANT_NOT_RECOGNIZED"
}
```

### Response 400 (Unknown Crop)
```json
{
  "success": false,
  "error": "Plant identified but not a supported crop",
  "error_code": "UNSUPPORTED_CROP"
}
```

### Response 422 (Validation Error)
```json
{
  "detail": [
    {
      "loc": ["body", "image_base64"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Error Codes
- `PLANT_NOT_RECOGNIZED`: Plant.id could not identify anything in the image
- `UNSUPPORTED_CROP`: Plant identified but not in our crop database
- `PLANT_ID_API_ERROR`: External Plant.id API error
- `INVALID_IMAGE`: Image decoding failed

### Usage Example
```python
# Bot converts photo to base64 and sends
import base64

# Download photo from Telegram
photo_bytes = await bot.download(photo)
image_b64 = base64.b64encode(photo_bytes).decode()

# Call backend
response = await http_client.post(
    f"{BACKEND_URL}/analyze-crop",
    json={
        "image_base64": image_b64,
        "telegram_user_id": message.from_user.id
    }
)

data = response.json()
if data["success"]:
    crop_name = data["crop"]["name_kg"]
    await message.answer(f"Таанылды: {crop_name}")
else:
    await message.answer(f"Ката: {data['error']}")
```

---

## 3. POST /water-schedule

Calculates irrigation recommendation based on crop type, growth stage, and weather forecast.

### Request Body
```json
{
  "crop_code": "corn",
  "growth_stage": "flowering",
  "water_date": "2025-11-29",
  "telegram_user_id": 123456789
}
```

**Field Descriptions:**
- `crop_code` (required): Crop code from `/analyze-crop` response
- `growth_stage` (required): Growth stage from `/analyze-crop` response
- `water_date` (required): ISO date (YYYY-MM-DD) when water will be available
- `telegram_user_id` (required): Telegram user ID for analytics/logging

### Response 200 (Success)
```json
{
  "success": true,
  "water_date": "2025-11-29",
  "water_date_display": "Пятница, 29 ноября",
  "days_until_water": 3,
  "weather": {
    "temp_avg": 12.5,
    "precipitation_mm": 0,
    "condition": "Ясно ☀️"
  },
  "recommendation": {
    "liters_per_sotka": 650,
    "urgency": "critical",
    "urgency_display": "⚠️ Критично",
    "next_watering_days": 6,
    "message_ru": "Твоя кукуруза на стадии цветения — критический период! Когда дадут воду, полей обильно.",
    "message_kg": "Сенин жүгөрүң гүлдөө стадиясында — абдан маанилүү кезең! Суу келгенде көп суу бер."
  }
}
```

**Field Descriptions:**
- `success`: Always `true` for successful calculation
- `water_date`: Confirmed water date (ISO format)
- `water_date_display`: Localized date with day of week
- `days_until_water`: Number of days from today to water date
- `weather.temp_avg`: Average temperature on water date (°C)
- `weather.precipitation_mm`: Expected rainfall (millimeters)
- `weather.condition`: Weather summary with emoji
- `recommendation.liters_per_sotka`: Water amount per 100 m²
- `recommendation.urgency`: Urgency level ("low", "medium", "high", "critical")
- `recommendation.urgency_display`: Localized urgency with emoji
- `recommendation.next_watering_days`: Recommended days until next watering
- `recommendation.message_ru`: Complete recommendation text in Russian
- `recommendation.message_kg`: Complete recommendation text in Kyrgyz

### Response 400 (Invalid Date)
```json
{
  "success": false,
  "error": "Water date is too far in the future (max 7 days)",
  "error_code": "DATE_OUT_OF_RANGE"
}
```

### Response 400 (Invalid Crop)
```json
{
  "success": false,
  "error": "Unknown crop code",
  "error_code": "INVALID_CROP_CODE"
}
```

### Error Codes
- `DATE_OUT_OF_RANGE`: Date is beyond forecast window (>7 days)
- `DATE_IN_PAST`: Date is in the past
- `INVALID_CROP_CODE`: Crop code not recognized
- `WEATHER_API_ERROR`: External weather API error

### Usage Example
```python
# Bot sends irrigation date to backend
response = await http_client.post(
    f"{BACKEND_URL}/water-schedule",
    json={
        "crop_code": crop_code,  # Saved from analyze-crop
        "growth_stage": growth_stage,  # Saved from analyze-crop
        "water_date": "2025-11-29",  # Parsed from user input
        "telegram_user_id": message.from_user.id
    }
)

data = response.json()
if data["success"]:
    rec = data["recommendation"]
    await message.answer(
        f"💧 {rec['liters_per_sotka']} литр/сотка\n"
        f"{rec['urgency_display']}\n\n"
        f"{rec['message_kg']}"
    )
else:
    await message.answer(f"Ката: {data['error']}")
```

---

## 📝 General Notes

### Date Formats
- **API requests/responses**: ISO 8601 (YYYY-MM-DD)
- **Display to users**: Localized format via `*_display` fields

### Localization
- All user-facing text provided in both Russian (`*_ru`) and Kyrgyz (`*_kg`)
- Bot chooses which to display based on user language preference

### Error Handling
- **2xx**: Success, check `success` field in JSON
- **4xx**: Client error, check `error` and `error_code` fields
- **5xx**: Server error, retry with exponential backoff

### Rate Limiting
- No rate limiting for MVP
- Production: 100 requests/minute per user

### Timeouts
- Bot should set 30-second timeout for API calls
- Backend has 30-second timeout for external APIs

### Coordinates
- Default location: Bishkek (42.8746, 74.5698)
- Future: Accept location from bot

---

## 🔄 Typical Request Flow

```
User sends photo
    ↓
Bot downloads photo
    ↓
Bot encodes to base64
    ↓
Bot → POST /analyze-crop
    ↓
Backend → Plant.id API
    ↓
Backend ← Plant.id response
    ↓
Backend processes crop info
    ↓
Bot ← Success with crop data
    ↓
Bot saves crop_code & growth_stage
    ↓
Bot asks for irrigation date
    ↓
User types "эртең" (tomorrow)
    ↓
Bot parses to ISO date
    ↓
Bot → POST /water-schedule
    ↓
Backend → Weather API
    ↓
Backend calculates irrigation
    ↓
Bot ← Success with recommendation
    ↓
Bot displays to user in Kyrgyz
```

---

## 🧪 Testing

### Mock Responses for Development

**Successful crop analysis:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "...",
    "telegram_user_id": 123
  }'
```

**Successful water schedule:**
```bash
curl -X POST http://localhost:8000/api/v1/water-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "crop_code": "corn",
    "growth_stage": "flowering",
    "water_date": "2025-11-29",
    "telegram_user_id": 123
  }'
```

### Bot Mock Mode
Bot can run in mock mode (DEBUG=true) where it returns fake responses without calling backend.

### Backend Mock Mode
Backend can run with `MOCK_PLANT_ID=true` to skip external API calls during testing.

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-26 | Initial contract for hackathon MVP |

---

## 🤝 Contract Agreement

Both teams agree to:
1. Not change endpoint URLs without mutual agreement
2. Not remove required fields without versioning
3. Add new optional fields with backward compatibility
4. Communicate breaking changes immediately

---

**Last Updated:** November 26, 2025
**Status:** Active
**Next Review:** After MVP demo
