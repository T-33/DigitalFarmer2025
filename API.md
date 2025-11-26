# Tamchy AI - Backend API Documentation

## 📋 Overview

The Tamchy AI Backend API is a FastAPI-based service that provides crop identification and irrigation recommendations for farmers in Kyrgyzstan.

**Technology Stack:**
- Framework: FastAPI 0.109.0
- Python: 3.11+
- External APIs: Plant.id, Open-Meteo
- Database: SQLite (aiosqlite)

**Base URL (Local):** `http://localhost:8000`
**API Version:** v1
**API Prefix:** `/api/v1`

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│         FastAPI Application              │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │         Routers                    │  │
│  │  • /health  • /analyze-crop        │  │
│  │  • /water-schedule                 │  │
│  └────────────────────────────────────┘  │
│                  ↓                       │
│  ┌────────────────────────────────────┐  │
│  │         Services                   │  │
│  │  • plant_id.py  • weather.py       │  │
│  │  • irrigation.py                   │  │
│  └────────────────────────────────────┘  │
│                  ↓                       │
│  ┌────────────────────────────────────┐  │
│  │      External APIs                 │  │
│  │  • Plant.id  • Open-Meteo          │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Installation

```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Setup

Create `api/.env`:
```env
PLANT_ID_API_KEY=your_api_key_here
DEBUG=true
HOST=0.0.0.0
PORT=8000
API_VERSION=v1
DATABASE_URL=sqlite+aiosqlite:///./tamchy.db
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Running the Server

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

---

## 📡 API Endpoints

### Health Check

**GET** `/api/v1/health`

Returns backend health status and external API connectivity.

**Response 200:**
```json
{
  "status": "ok",
  "plant_id_api": "connected",
  "weather_api": "connected"
}
```

---

### Analyze Crop

**POST** `/api/v1/analyze-crop`

Identifies crop type and growth stage from a photo.

**Request Body:**
```json
{
  "image_base64": "string",
  "telegram_user_id": 123456789
}
```

**Response 200:**
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

**Error Responses:**
- 400: Plant not recognized
- 422: Validation error
- 500: Server error

---

### Water Schedule

**POST** `/api/v1/water-schedule`

Calculates irrigation recommendation based on crop, weather, and irrigation date.

**Request Body:**
```json
{
  "crop_code": "corn",
  "growth_stage": "flowering",
  "water_date": "2025-11-29",
  "telegram_user_id": 123456789
}
```

**Response 200:**
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
    "message_ru": "Твоя кукуруза на стадии цветения...",
    "message_kg": "Сенин жүгөрүң гүлдөө стадиясында..."
  }
}
```

---

## 🔧 Service Layer

### Plant.id Service (`services/plant_id.py`)

**Functions:**
- `identify_plant(image_base64: str) -> dict`: Call Plant.id API
- `extract_crop_info(plant_response: dict) -> dict`: Parse response

**Supported Crops:**
- Corn (Кукуруза / Жүгөрү)
- Wheat (Пшеница / Буудай)
- Cotton (Хлопок / Мамык)
- Vegetables (various)

### Weather Service (`services/weather.py`)

**Functions:**
- `get_weather_forecast(lat, lon, days) -> dict`: Fetch forecast
- `get_weather_for_date(weather_data, target_date) -> dict`: Extract specific date

**Data Sources:**
- Open-Meteo API (free, no key required)
- Default location: Bishkek (42.8746, 74.5698)

### Irrigation Service (`services/irrigation.py`)

**Functions:**
- `calculate_irrigation(crop, stage, weather, date) -> dict`: Main logic
- `get_crop_coefficient(crop, stage) -> float`: Kc values
- `calculate_et(kc, et0) -> float`: Evapotranspiration

**Calculation Method:**
- FAO Penman-Monteith (simplified)
- Crop coefficients by growth stage
- Weather-adjusted recommendations

---

## 📊 Data Models

### Request Models (`models/requests.py`)

```python
class CropAnalysisRequest(BaseModel):
    image_base64: str
    telegram_user_id: int

class WaterScheduleRequest(BaseModel):
    crop_code: str
    growth_stage: str
    water_date: str  # ISO format YYYY-MM-DD
    telegram_user_id: int
```

### Response Models (`models/responses.py`)

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

class WeatherInfo(BaseModel):
    temp_avg: float
    precipitation_mm: float
    condition: str

class RecommendationInfo(BaseModel):
    liters_per_sotka: int
    urgency: str
    urgency_display: str
    next_watering_days: int
    message_ru: str
    message_kg: str
```

---

## 🧪 Testing

### Unit Tests

```bash
cd api
pytest tests/ -v
```

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Analyze crop (requires valid base64 image)
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d @test_crop_request.json

# Water schedule
curl -X POST http://localhost:8000/api/v1/water-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "crop_code": "corn",
    "growth_stage": "flowering",
    "water_date": "2025-11-30",
    "telegram_user_id": 123
  }'
```

### Test Coverage

```bash
pytest --cov=. --cov-report=html
```

---

## 🔐 Security

### CORS Configuration
- Configured in `main.py`
- Allows bot origin (localhost:3000)
- Production: Restrict to deployed bot URL

### API Key Management
- Plant.id key stored in environment variables
- Never commit `.env` to Git
- Use `.env.example` as template

### Input Validation
- Pydantic validates all requests
- Base64 image size limits (future)
- Rate limiting (future)

---

## 📈 Performance

### Caching Strategy (Future)
- Redis for weather data (1 hour TTL)
- Crop identification cache (for same photos)

### Response Times (Target)
- Health check: <50ms
- Crop analysis: <3 seconds
- Water schedule: <1 second

### Monitoring
- FastAPI built-in metrics
- Logging with Python `logging` module
- Production: Sentry for error tracking

---

## 🚢 Deployment

### Docker

```bash
cd api
docker build -t tamchy-api .
docker run -p 8000:8000 --env-file .env tamchy-api
```

### Railway

1. Connect GitHub repository
2. Select `api` folder as root
3. Add environment variables
4. Deploy

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 📝 Development Notes

### Adding New Crops

1. Update `CROP_NAME_MAPPING` in `services/plant_id.py`
2. Add crop coefficient in `services/irrigation.py`
3. Update tests

### Changing Calculation Logic

- Edit `services/irrigation.py`
- Maintain backward compatibility in API responses
- Update CONTRACT.md if response structure changes

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Processing crop analysis")
logger.error("Plant.id API error", exc_info=True)
```

---

## 🐛 Common Issues

### Plant.id API Key Error
```
HTTPStatusError: 401 Unauthorized
```
**Solution:** Check `PLANT_ID_API_KEY` in `.env`

### Weather API Timeout
```
ReadTimeout
```
**Solution:** Increase timeout in `httpx.AsyncClient(timeout=60.0)`

### CORS Error from Bot
```
Access to fetch at 'http://localhost:8000' blocked by CORS
```
**Solution:** Add bot origin to `ALLOWED_ORIGINS` in `.env`

---

## 📚 External API Documentation

- **Plant.id:** https://web.plant.id/plant-identification-api/
- **Open-Meteo:** https://open-meteo.com/en/docs

---

## 🤝 Contributing

See main `PLAN.md` for development workflow.

**Code Style:**
- Black formatter
- Type hints (Python 3.11+)
- Async/await where possible

---

**Maintained by:** Backend Team
**Last Updated:** November 26, 2025
**Version:** 1.0.0
