# 📚 MurabAI API Documentation

## Overview

MurabAI Backend API - FastAPI-based REST API for crop analysis and irrigation recommendations.

**Base URL:** `http://localhost:8000/api/v1`

**Version:** 1.0.0

---

## 🔑 Authentication

Currently no authentication required (MVP stage). In production, implement JWT tokens.

---

## 📡 Endpoints

### 1. Health Check

**GET** `/health`

Check if backend services are operational.

**Response:**
```json
{
  "status": "ok",
  "plant_id_api": "connected",
  "weather_api": "connected",
  "timestamp": "2025-11-26T12:00:00Z"
}
```

**Status Codes:**
- `200` - All services operational
- `503` - One or more services unavailable

---

### 2. Analyze Crop

**POST** `/analyze-crop`

Identify crop from photo using Plant.id API.

**Request Body:**
```json
{
  "image_base64": "string (base64 encoded image)",
  "telegram_user_id": 123456789
}
```

**Validation:**
- `image_base64`: Must be valid base64 image (JPEG, PNG, GIF, BMP)
- `telegram_user_id`: Integer, required for logging

**Response (Success):**
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

**Response (Error):**
```json
{
  "success": false,
  "error": "Could not identify plant in the image",
  "error_code": "PLANT_NOT_RECOGNIZED"
}
```

**Error Codes:**
- `PLANT_NOT_RECOGNIZED` - No plant detected in image
- `UNSUPPORTED_CROP` - Plant identified but not a supported crop
- `INVALID_IMAGE_FORMAT` - Invalid base64 or unsupported image format
- `PLANT_ID_API_ERROR` - External Plant.id API error
- `ANALYSIS_ERROR` - Generic analysis error

**Status Codes:**
- `200` - Request processed (check `success` field)
- `400` - Invalid request data
- `500` - Internal server error

---

### 3. Water Schedule

**POST** `/water-schedule`

Calculate irrigation recommendation based on crop, date, and weather.

**Request Body:**
```json
{
  "crop_code": "corn",
  "growth_stage": "flowering",
  "water_date": "2025-11-29",
  "telegram_user_id": 123456789
}
```

**Validation:**
- `crop_code`: Must be valid crop (corn, wheat, cotton, tomato, potato, onion, carrot, beet, cucumber, pepper)
- `growth_stage`: Must be valid stage (initial, development, flowering, maturation)
- `water_date`: ISO format (YYYY-MM-DD), max 7 days in future
- `telegram_user_id`: Integer, required for logging

**Response (Success):**
```json
{
  "success": true,
  "water_date": "2025-11-29",
  "water_date_display": "Пятница, 29 ноября",
  "days_until_water": 3,
  "weather": {
    "temp_avg": 12.5,
    "temp_max": 18.0,
    "temp_min": 7.0,
    "precipitation_mm": 0.0,
    "et0": 3.8,
    "condition": "Ясно ☀️",
    "date": "2025-11-29"
  },
  "recommendation": {
    "liters_per_sotka": 650,
    "urgency": "critical",
    "urgency_display": "⚠️ Критично",
    "next_watering_days": 5,
    "message_ru": "⚠️ Твоя кукуруза на цветении — критический период!...",
    "message_kg": "⚠️ Сенин жүгөрүң гүлдөө этабында — абдан маанилүү кезең!...",
    "debug": {
      "kc": 1.2,
      "et0": 3.8,
      "etc_daily": 4.56,
      "net_irrigation_daily": 4.56,
      "total_mm": 22.8
    }
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Date out of range. Maximum 7 days",
  "error_code": "DATE_OUT_OF_RANGE"
}
```

**Error Codes:**
- `INVALID_CROP` - Unknown crop code
- `INVALID_GROWTH_STAGE` - Unknown growth stage
- `DATE_OUT_OF_RANGE` - Date more than 7 days in future
- `DATE_IN_PAST` - Date is in the past
- `WEATHER_API_ERROR` - Weather API unavailable
- `CALCULATION_ERROR` - Irrigation calculation failed

**Status Codes:**
- `200` - Request processed (check `success` field)
- `400` - Invalid request data
- `500` - Internal server error

---

## 🌾 Supported Crops

| Code | Russian | Kyrgyz | English |
|------|---------|--------|---------|
| corn | Кукуруза | Жүгөрү | Corn |
| wheat | Пшеница | Буудай | Wheat |
| cotton | Хлопок | Пахта | Cotton |
| tomato | Помидор | Помидор | Tomato |
| potato | Картофель | Картошка | Potato |
| onion | Лук | Пияз | Onion |
| carrot | Морковь | Сабизи | Carrot |
| beet | Свекла | Кызылча | Beet |
| cucumber | Огурец | Бадыраң | Cucumber |
| pepper | Перец | Калемпир | Pepper |

---

## 🌱 Growth Stages

| Code | Russian | Kyrgyz | Kc Range |
|------|---------|--------|----------|
| initial | Всходы 🌱 | Өнүү 🌱 | 0.3-0.4 |
| development | Рост 🌿 | Өсүү 🌿 | 0.7-0.75 |
| flowering | Цветение 🌸 | Гүлдөө 🌸 | 1.0-1.2 |
| maturation | Созревание 🌾 | Бышуү 🌾 | 0.4-0.95 |

---

## 💧 Irrigation Calculation (FAO-56)

### Formula

```
ETc = Kc × ET0
Net Irrigation = ETc - Precipitation
Total Volume = Net Irrigation × Days × Area
```

Where:
- **ETc** - Crop evapotranspiration (mm/day)
- **Kc** - Crop coefficient (depends on crop and stage)
- **ET0** - Reference evapotranspiration (from weather API)
- **Precipitation** - Expected rainfall (mm)
- **Area** - 100 m² (1 sotka)

### Urgency Levels

| Level | Days Until Water | Description |
|-------|------------------|-------------|
| 🟢 Low | 5+ | Normal, water on schedule |
| 🟡 Medium | 3-4 | Advisable to water |
| 🔴 High | 1-2 | Important to water |
| ⚠️ Critical | 0 | Water immediately |

**Note:** Flowering stage always has higher urgency.

---

## 🌐 External APIs

### Plant.id API

- **URL:** `https://api.plant.id/v2/identify`
- **Auth:** API Key in header
- **Rate Limit:** Depends on plan
- **Mock Mode:** Set `MOCK_PLANT_ID=true` for testing

### Open-Meteo Weather API

- **URL:** `https://api.open-meteo.com/v1/forecast`
- **Auth:** None (free API)
- **Data:** Temperature, precipitation, ET0 (FAO-56)
- **Forecast:** 7 days ahead
- **Mock Mode:** Set `MOCK_WEATHER=true` for testing

---

## 🐛 Error Handling

All endpoints return consistent error format:

```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE"
}
```

Common HTTP status codes:
- `200` - Success (check `success` field in body)
- `400` - Bad Request (invalid parameters)
- `422` - Validation Error (Pydantic)
- `500` - Internal Server Error
- `503` - Service Unavailable

---

## 🔧 Configuration

Environment variables (`.env`):

```bash
# Plant.id API
PLANT_ID_API_KEY=your_api_key_here

# Application
DEBUG=true
HOST=0.0.0.0
PORT=8000
API_VERSION=v1

# Mock mode (for testing without real APIs)
MOCK_PLANT_ID=true
MOCK_WEATHER=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 📦 Response Models (Pydantic)

### CropInfo
```python
class CropInfo(BaseModel):
    name_ru: str
    name_kg: str
    name_code: str
    confidence: float
    growth_stage: str
    growth_stage_display: str
    water_need: str
    water_need_display: str
```

### WeatherInfo
```python
class WeatherInfo(BaseModel):
    temp_avg: float
    temp_max: float
    temp_min: float
    precipitation_mm: float
    et0: float
    condition: str
    date: str
```

### IrrigationRecommendation
```python
class IrrigationRecommendation(BaseModel):
    liters_per_sotka: int
    urgency: str
    urgency_display: str
    next_watering_days: int
    message_ru: str
    message_kg: str
```

---

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Analyze crop (with mock data)
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "SGVsbG8gV29ybGQ=", "telegram_user_id": 123}'

# Water schedule
curl -X POST http://localhost:8000/api/v1/water-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "crop_code": "corn",
    "growth_stage": "flowering",
    "water_date": "2025-11-29",
    "telegram_user_id": 123
  }'
```

### Using Python requests

```python
import requests
import base64

# Analyze crop
with open("corn.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/v1/analyze-crop",
    json={
        "image_base64": image_b64,
        "telegram_user_id": 123456
    }
)

result = response.json()
if result["success"]:
    print(f"Identified: {result['crop']['name_ru']}")
    print(f"Confidence: {result['crop']['confidence']:.2%}")
```

---

## 📊 Interactive Documentation

- **Swagger UI:** http://localhost:8000/api/v1/docs
- **ReDoc:** http://localhost:8000/api/v1/redoc
- **OpenAPI JSON:** http://localhost:8000/api/v1/openapi.json

---

## 🚀 Production Considerations

1. **Authentication:** Add JWT or API key authentication
2. **Rate Limiting:** Implement rate limiting per user
3. **Caching:** Cache Plant.id results and weather data (Redis)
4. **Database:** Store user requests, crops, recommendations
5. **Monitoring:** Add Prometheus metrics, health checks
6. **Logging:** Structured logging with request IDs
7. **Validation:** Additional input sanitization
8. **HTTPS:** Use SSL/TLS in production
9. **Load Balancing:** Use multiple API instances
10. **Error Tracking:** Sentry or similar service

---

**Last Updated:** November 26, 2025
**Version:** 1.0.0
