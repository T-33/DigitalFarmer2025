# Tamchy AI - Development Plan

## 🎯 Project Goal
Build a functional Telegram bot MVP in 48 hours that helps Kyrgyz farmers optimize irrigation through AI crop recognition and weather forecasting.

---

## 📋 High-Level Timeline

| Phase | Duration | Objective |
|-------|----------|-----------|
| **Setup & Infrastructure** | Hours 1-6 | Project scaffolding, API keys, basic bot |
| **Core Integration** | Hours 6-24 | Plant.id + Weather APIs + FSM |
| **Business Logic** | Hours 24-36 | Irrigation calculations + UI polish |
| **Deploy & Demo** | Hours 36-48 | Railway deployment + presentation |

---

## 🏗️ Detailed Implementation Plan

### Phase 1: Setup & Infrastructure (Hours 1-6)

#### Step 1.1: Project Structure Creation

**Root level files:**
```
FarmersHackathon/
├── CONTRACT.md              # API contract (CREATE FIRST!)
├── API.md                   # Backend API documentation
├── README.md
├── docker-compose.yml       # Both services orchestration
├── .gitignore
```

**Backend API structure:**
```
api/
├── main.py                  # FastAPI entry point
├── core/
│   ├── __init__.py
│   └── config.py            # API settings
├── routers/
│   ├── __init__.py
│   ├── health.py            # GET /health
│   ├── crop.py              # POST /analyze-crop
│   └── water.py             # POST /water-schedule
├── services/
│   ├── __init__.py
│   ├── plant_id.py          # Plant.id integration
│   ├── weather.py           # Open-Meteo integration
│   └── irrigation.py        # Irrigation calculations
├── models/
│   ├── __init__.py
│   ├── requests.py          # Pydantic request schemas
│   ├── responses.py         # Pydantic response schemas
│   └── database.py          # SQLAlchemy models
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

**Telegram Bot structure:**
```
bot/
├── main.py                  # Bot entry point
├── config.py                # Bot settings
├── handlers/
│   ├── __init__.py
│   ├── start.py             # /start command
│   ├── photo.py             # Photo upload handler
│   └── schedule.py          # Irrigation date handler
├── keyboards/
│   ├── __init__.py
│   └── inline.py            # Inline keyboards
├── states/
│   ├── __init__.py
│   └── irrigation.py        # FSM states
├── services/
│   ├── __init__.py
│   └── api_client.py        # Backend API HTTP client
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

**Tests structure:**
```
tests/
├── api/
│   ├── test_crop_analysis.py
│   ├── test_water_schedule.py
│   └── test_services.py
└── bot/
    └── test_handlers.py
```

#### Step 1.2: API Contract Definition (CRITICAL!)
**File: `CONTRACT.md`**

This is the **single source of truth** for both teams. Create this FIRST!

```markdown
# Tamchy AI - API Contract v1.0

Base URL: `http://localhost:8000/api/v1`

## Endpoints

### 1. GET /health
Health check endpoint.

**Response 200:**
{
  "status": "ok",
  "plant_id_api": "connected",
  "weather_api": "connected"
}

### 2. POST /analyze-crop
Analyze crop photo.

**Request:**
{
  "image_base64": "string",
  "telegram_user_id": 123456789
}

**Response 200:**
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

**Response 400:**
{
  "success": false,
  "error": "Could not identify plant",
  "error_code": "PLANT_NOT_RECOGNIZED"
}

### 3. POST /water-schedule
Calculate irrigation schedule.

**Request:**
{
  "crop_code": "corn",
  "growth_stage": "flowering",
  "water_date": "2025-11-29",
  "telegram_user_id": 123456789
}

**Response 200:**
{
  "success": true,
  "water_date": "2025-11-29",
  "water_date_display": "Пятница, 29 ноября",
  "days_until_water": 3,
  "weather": {
    "temp_avg": 12,
    "precipitation_mm": 0,
    "condition": "Ясно ☀️"
  },
  "recommendation": {
    "liters_per_sotka": 650,
    "urgency": "critical",
    "urgency_display": "⚠️ Критично",
    "next_watering_days": 6,
    "message_ru": "Твоя кукуруза на стадии цветения — критический период!",
    "message_kg": "Сенин жүгөрүң гүлдөө стадиясында — абдан маанилүү!"
  }
}
```

#### Step 1.3: Configuration Setup

**File: `api/core/config.py`** (Backend)
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    plant_id_api_key: str
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    api_version: str = "v1"
    database_url: str = "sqlite+aiosqlite:///./tamchy.db"
    allowed_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()
```

**File: `bot/config.py`** (Bot)
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_bot_token: str
    backend_api_url: str = "http://localhost:8000/api/v1"
    api_timeout: int = 30
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
```

#### Step 1.3: FastAPI Application
**File: `src/main.py`**
- Create FastAPI app instance
- Health check endpoint (`GET /health`)
- Webhook endpoint for Telegram (future use)
- CORS middleware
- Uvicorn server configuration

#### Step 1.4: Docker Compose Setup
**File: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  backend:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - PLANT_ID_API_KEY=${PLANT_ID_API_KEY}
      - DEBUG=true
    volumes:
      - ./api:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  bot:
    build: ./bot
    depends_on:
      - backend
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - BACKEND_API_URL=http://backend:8000/api/v1
      - DEBUG=true
    volumes:
      - ./bot:/app
    command: python main.py
```

#### Step 1.5: Telegram Bot Setup
**Actions:**
1. Create bot via @BotFather → Get token
2. Set bot commands:
   - `/start` - Баштоо (Start)
   - `/help` - Жардам (Help)

#### Step 1.6: Dependencies Files

**File: `api/requirements.txt`** (Backend)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
httpx==0.26.0
sqlalchemy==2.0.25
aiosqlite==0.19.0
python-dotenv==1.0.0
```

**File: `bot/requirements.txt`** (Bot)
```
aiogram==3.3.0
httpx==0.26.0
dateparser==1.2.0
python-dotenv==1.0.0
pydantic==2.5.3
```

#### Step 1.7: Initial Testing

**Test Backend:**
```bash
cd api
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Should see: "Uvicorn running on http://127.0.0.1:8000"
```

**Test Bot (in separate terminal):**
```bash
cd bot
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
# Should see: "Bot started"
```

---

### Phase 2: Parallel Development (Hours 6-24)

**IMPORTANT:** Backend and Bot teams work **simultaneously** on their respective folders!

---

## 🔧 BACKEND DEVELOPMENT (api/ folder)

#### Step 2.1: FastAPI Application Setup
**File: `api/main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import health, crop, water

app = FastAPI(
    title="Tamchy AI Backend",
    version="1.0.0",
    docs_url="/api/docs"
)

# CORS for bot communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(crop.router, prefix="/api/v1", tags=["crop"])
app.include_router(water.router, prefix="/api/v1", tags=["water"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
```

#### Step 2.2: Pydantic Models (Request/Response)
**File: `api/models/requests.py`**
```python
from pydantic import BaseModel, Field

class CropAnalysisRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image")
    telegram_user_id: int = Field(..., description="Telegram user ID")

class WaterScheduleRequest(BaseModel):
    crop_code: str = Field(..., description="Crop code (e.g., 'corn')")
    growth_stage: str = Field(..., description="Growth stage")
    water_date: str = Field(..., description="ISO date (YYYY-MM-DD)")
    telegram_user_id: int
```

**File: `api/models/responses.py`**
```python
from pydantic import BaseModel

class CropInfo(BaseModel):
    name_ru: str
    name_kg: str
    name_code: str
    confidence: float
    growth_stage: str
    growth_stage_display: str
    water_need: str
    water_need_display: str

class CropAnalysisResponse(BaseModel):
    success: bool
    crop: CropInfo | None = None
    error: str | None = None
    error_code: str | None = None

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

class WaterScheduleResponse(BaseModel):
    success: bool
    water_date: str | None = None
    water_date_display: str | None = None
    days_until_water: int | None = None
    weather: WeatherInfo | None = None
    recommendation: RecommendationInfo | None = None
    error: str | None = None
```

#### Step 2.3: Plant.id Service
**File: `api/services/plant_id.py`**

```python
import httpx
import base64
from core.config import settings

PLANT_ID_URL = "https://api.plant.id/v2/identify"

CROP_NAME_MAPPING = {
    "zea mays": {"ru": "Кукуруза", "kg": "Жүгөрү", "code": "corn"},
    "triticum": {"ru": "Пшеница", "kg": "Буудай", "code": "wheat"},
    "gossypium": {"ru": "Хлопок", "kg": "Мамык", "code": "cotton"},
    # Add more crops
}

async def identify_plant(image_base64: str) -> dict:
    """Call Plant.id API to identify crop."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            PLANT_ID_URL,
            json={
                "images": [image_base64],
                "modifiers": ["crops", "similar_images"],
                "plant_language": "ru",
                "plant_details": ["common_names", "taxonomy"]
            },
            headers={"Api-Key": settings.plant_id_api_key}
        )
        response.raise_for_status()
        return response.json()

def extract_crop_info(plant_response: dict) -> dict:
    """Extract crop information from Plant.id response."""
    if not plant_response.get("suggestions"):
        raise ValueError("No plant identified")

    top_suggestion = plant_response["suggestions"][0]
    plant_name = top_suggestion["plant_name"].lower()
    confidence = top_suggestion["probability"]

    # Map to known crops
    crop_data = None
    for key, value in CROP_NAME_MAPPING.items():
        if key in plant_name:
            crop_data = value
            break

    if not crop_data:
        raise ValueError(f"Unknown crop: {plant_name}")

    # Infer growth stage (simplified for MVP)
    growth_stage = infer_growth_stage(plant_name, confidence)

    return {
        "name_ru": crop_data["ru"],
        "name_kg": crop_data["kg"],
        "name_code": crop_data["code"],
        "confidence": confidence,
        "growth_stage": growth_stage,
        "growth_stage_display": GROWTH_STAGES[growth_stage],
        "water_need": get_water_need(growth_stage),
        "water_need_display": WATER_NEED_DISPLAY[get_water_need(growth_stage)]
    }

def infer_growth_stage(plant_name: str, confidence: float) -> str:
    """Infer growth stage (simplified - use ML in production)."""
    # For MVP, return based on common patterns
    # In production, analyze image features
    return "flowering"  # Default for demo

GROWTH_STAGES = {
    "initial": "Всходы 🌱",
    "development": "Рост 🌿",
    "flowering": "Цветение 🌸",
    "maturation": "Созревание 🌾"
}

WATER_NEED_DISPLAY = {
    "low": "🟢 Низкая",
    "medium": "🟡 Средняя",
    "high": "🔴 Высокая"
}

def get_water_need(growth_stage: str) -> str:
    mapping = {
        "initial": "low",
        "development": "medium",
        "flowering": "high",
        "maturation": "medium"
    }
    return mapping.get(growth_stage, "medium")
```

#### Step 2.4: Weather Service
**File: `api/services/weather.py`**

```python
import httpx
from datetime import datetime

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_LOCATION = (42.8746, 74.5698)  # Bishkek

async def get_weather_forecast(
    lat: float = DEFAULT_LOCATION[0],
    lon: float = DEFAULT_LOCATION[1],
    days: int = 7
) -> dict:
    """Fetch weather forecast from Open-Meteo."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration",
                "timezone": "Asia/Bishkek",
                "forecast_days": days
            }
        )
        response.raise_for_status()
        return response.json()

def get_weather_for_date(weather_data: dict, target_date: str) -> dict:
    """Extract weather for specific date."""
    daily = weather_data["daily"]
    try:
        idx = daily["time"].index(target_date)
        temp_avg = (daily["temperature_2m_max"][idx] + daily["temperature_2m_min"][idx]) / 2
        precipitation = daily["precipitation_sum"][idx]
        et0 = daily["et0_fao_evapotranspiration"][idx]

        # Determine condition
        if precipitation > 10:
            condition = "Дождь 🌧️"
        elif precipitation > 0:
            condition = "Облачно ☁️"
        else:
            condition = "Ясно ☀️"

        return {
            "temp_avg": round(temp_avg, 1),
            "precipitation_mm": precipitation,
            "condition": condition,
            "et0": et0
        }
    except (ValueError, IndexError):
        # Date not in forecast
        return None
```

#### Step 2.4: Date Parsing
**File: `src/services/irrigation.py` (helper function)**

```python
import dateparser
from datetime import datetime, timedelta

def parse_irrigation_date(user_input: str) -> datetime | None:
    """
    Parse Kyrgyz/Russian date phrases:
    - "бүгүн", "сегодня" → today
    - "эртең", "завтра" → tomorrow
    - "шаршемби" → next Wednesday
    - "3 күн" → in 3 days
    """
    settings = {
        'TIMEZONE': 'Asia/Bishkek',
        'RETURN_AS_TIMEZONE_AWARE': True,
        'LANGUAGES': ['ru', 'ky']
    }
    return dateparser.parse(user_input, settings=settings)
```

#### Step 2.5: Bot Conversation Flow
**File: `src/bot/handlers.py` (expanded)**

**Handler 1: Start**
```python
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "🌱 Тамчы AI'га кош келиңиз!\n\n"
        "Талаңыздын сүрөтүн жөнөтүңүз 📸"
    )
    await state.set_state(IrrigationStates.waiting_for_photo)
```

**Handler 2: Photo Processing**
```python
@router.message(IrrigationStates.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    # 1. Download photo
    # 2. Send to Plant.id
    # 3. Store crop info in state
    # 4. Ask for irrigation date
    await state.set_state(IrrigationStates.waiting_for_irrigation_date)
```

**Handler 3: Date Processing**
```python
@router.message(IrrigationStates.waiting_for_irrigation_date, F.text)
async def process_date(message: Message, state: FSMContext):
    # 1. Parse date
    # 2. Get weather forecast
    # 3. Calculate irrigation recommendation
    # 4. Send formatted result
    # 5. Clear state
```

---

### Phase 3: Business Logic (Hours 24-36)

#### Step 3.1: Crop Coefficient Database
**File: `src/services/irrigation.py`**

```python
# Crop coefficients by growth stage (Kc)
CROP_COEFFICIENTS = {
    "corn": {
        "initial": 0.3,      # Seedling
        "development": 0.7,  # Vegetative
        "mid": 1.2,          # Flowering/grain filling
        "late": 0.6          # Maturation
    },
    "wheat": {
        "initial": 0.3,
        "development": 0.7,
        "mid": 1.15,
        "late": 0.4
    },
    "cotton": {
        "initial": 0.35,
        "development": 0.7,
        "mid": 1.15,
        "late": 0.7
    },
    # Add more crops
}

# Stage duration (days) - rough estimates
GROWTH_STAGES_DURATION = {
    "corn": {"initial": 25, "development": 40, "mid": 45, "late": 30},
    "wheat": {"initial": 20, "development": 30, "mid": 60, "late": 30},
}
```

#### Step 3.2: Irrigation Calculation Algorithm
**File: `src/services/irrigation.py`**

```python
def calculate_irrigation_need(
    crop_name: str,
    growth_stage: str,
    et0: float,  # mm/day
    expected_rainfall: float,  # mm
    days_until_irrigation: int,
    field_area_ha: float = 1.0  # Default 1 hectare
) -> dict:
    """
    Calculate irrigation water requirement.

    Returns:
        {
            "liters_per_hectare": int,
            "total_liters": int,
            "daily_et": float,
            "rainfall_offset": float,
            "recommendation": str
        }
    """
    # Get crop coefficient
    kc = CROP_COEFFICIENTS.get(crop_name, {}).get(growth_stage, 0.8)

    # Calculate crop evapotranspiration (ETc)
    etc_daily = et0 * kc  # mm/day

    # Total ET over period
    total_etc = etc_daily * days_until_irrigation

    # Subtract expected rainfall
    net_irrigation_need = max(0, total_etc - expected_rainfall)

    # Convert mm to liters per hectare (1mm = 10,000 L/ha)
    liters_per_ha = net_irrigation_need * 10000
    total_liters = liters_per_ha * field_area_ha

    # Generate recommendation
    if net_irrigation_need < 10:
        recommendation = "🌧️ Жамгыр болот, суу берүүнүн кереги жок"
    elif net_irrigation_need < 30:
        recommendation = "💧 Аз суу берүү керек"
    elif net_irrigation_need < 50:
        recommendation = "💦 Орточо суу берүү"
    else:
        recommendation = "🌊 Көп суу берүү керек"

    return {
        "liters_per_hectare": int(liters_per_ha),
        "total_liters": int(total_liters),
        "daily_et": round(etc_daily, 2),
        "rainfall_offset": expected_rainfall,
        "recommendation": recommendation,
        "crop_coefficient": kc
    }
```

#### Step 3.3: Message Formatting
**File: `src/bot/keyboards.py`**

```python
def format_irrigation_message(
    crop_info: CropInfo,
    irrigation_date: datetime,
    weather: WeatherForecast,
    calculation: dict
) -> str:
    """Format the final recommendation message."""

    date_str = irrigation_date.strftime("%d.%m.%Y (%A)")

    # Find weather for irrigation date
    target_weather = next(
        (d for d in weather.days if d.date == irrigation_date.date().isoformat()),
        None
    )

    msg = f"""
✅ Таанылды: {crop_info.name_ky} ({crop_info.confidence:.0%})
🌾 Өсүү этабы: {crop_info.growth_stage or 'Аныкталбады'}

💧 **СУУ БЕРҮҮ КЕҢЕШИ**

📅 Дата: {date_str}
🌡️ Аба ырайы: {target_weather.temp_max}°C / {target_weather.temp_min}°C
🌧️ Жамгыр: {target_weather.precipitation} мм

💦 Суу көлөмү: **{calculation['liters_per_hectare']:,} л/га**
📊 Күндүк жоготуу: {calculation['daily_et']} мм

{calculation['recommendation']}
"""

    # Add warning if needed
    if target_weather.precipitation > 30:
        msg += "\n⚠️ Көп жамгыр күтүлүүдө, суу берүүнү кийинкиге калтырыңыз!"

    return msg.strip()
```

#### Step 3.4: Error Handling & Edge Cases
**Scenarios to handle:**
1. Plant.id doesn't recognize crop → Ask for manual input
2. Date parsing fails → Show examples
3. Weather API unavailable → Use default ET0 values
4. Photo quality too low → Ask for retake

**File: `src/bot/handlers.py` (add error handlers)**

```python
@router.error()
async def error_handler(event: ErrorEvent):
    logging.error(f"Error: {event.exception}")
    if event.update.message:
        await event.update.message.answer(
            "❌ Ката кетти. Кайра аракет кылыңыз же /start басыңыз"
        )
```

#### Step 3.5: Database Models (Optional for MVP)
**File: `src/models/database.py`**

```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class IrrigationQuery(Base):
    __tablename__ = "irrigation_queries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    crop_name = Column(String)
    irrigation_date = Column(DateTime)
    liters_recommended = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Note:** Can be skipped for hackathon MVP if time is tight.

---

### Phase 4: Deploy & Demo (Hours 36-48)

#### Step 4.1: Testing with Real Photos
**Prepare test dataset:**
- 3-5 corn photos (different growth stages)
- 3-5 wheat photos
- 2-3 vegetable photos
- 1-2 edge cases (unclear crops)

**Test scenarios:**
1. Happy path: corn → "tomorrow" → valid recommendation
2. Rainy day: any crop → date with heavy rain → warning
3. Far future date: any crop → "in 7 days" → forecast limit
4. Invalid crop: photo of animal → error handling

#### Step 4.2: Railway Deployment
**Files needed:**
- `Procfile`: `web: uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- `runtime.txt`: `python-3.11.7`

**Steps:**
1. Create Railway account
2. New project → Deploy from GitHub
3. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `PLANT_ID_API_KEY`
4. Set webhook URL: `https://your-app.railway.app/webhook`
5. Test deployment

**Alternative (if Railway issues):** Use polling mode locally for demo

#### Step 4.3: Presentation Preparation
**Slide structure (10 slides max):**

1. **Title Slide**
   - Tamchy AI - Акылдуу суу берүү
   - Team name + logo

2. **Problem** (with stats)
   - 65% water waste in Kyrgyzstan
   - Manual irrigation = crop loss

3. **Solution Overview**
   - AI crop recognition + Weather forecast
   - Works via Telegram (350K users)

4. **Live Demo** (video backup)
   - Show bot conversation flow
   - Real recommendation output

5. **Technical Architecture**
   - FastAPI + aiogram + Plant.id + Open-Meteo
   - Diagram

6. **Irrigation Algorithm**
   - Crop coefficients
   - Weather adjustments
   - Formula visualization

7. **Impact Potential**
   - 30% water savings × 350K farmers
   - SDG alignment

8. **Next Steps**
   - AVP integration
   - Satellite imagery
   - Voice input

9. **Business Model** (brief)
   - Freemium: Basic free, Pro with sensors
   - B2B: Government reporting

10. **Thank You + Demo**
    - QR code to try bot
    - Contact info

#### Step 4.4: Demo Script
**Duration: 4 minutes**

**Minute 1: Hook**
> "Сиз азык-түлүктү өстүрөсүз. Күнүгө суу берүү керек, бирок канча суу керектигин ким билет? Kyrgyzстанда фермерлер жылына 2 миллиард литр сууну текке кетиришет. Биз бул маселени чечебиз."

**Minute 2: Demo Part 1**
- Open Telegram on phone (screen mirrored)
- Send `/start` → Show Kyrgyz interface
- Send pre-saved corn photo
- Bot responds with crop identification

**Minute 3: Demo Part 2**
- Type "эртең" (tomorrow)
- Bot calculates and shows recommendation
- Highlight: weather integration, specific liter amount

**Minute 4: Impact & Next Steps**
- Show second quick demo (wheat photo)
- Explain next features (AVP, satellite)
- Show final slide with QR code to try bot

**Backup plan:** Pre-recorded video if live demo fails

---

## 🔧 Development Commands

### Setup
```bash
# Clone/navigate to project
cd C:\Users\Amin_stors\Desktop\FarmersHackathon

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env with actual API keys
```

### Run Locally
```bash
# Start FastAPI + Bot
python src/main.py

# Or with hot reload
uvicorn src.main:app --reload
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_plant_id.py -v
```

### Deployment
```bash
# Push to GitHub
git add .
git commit -m "feat: complete MVP"
git push origin main

# Railway auto-deploys from main branch
```

---

## 📦 File Creation Priority

### Critical (Must have for basic demo)
1. ✅ `src/config.py`
2. ✅ `src/main.py`
3. ✅ `src/bot/handlers.py`
4. ✅ `src/bot/states.py`
5. ✅ `src/services/plant_id.py`
6. ✅ `src/services/weather.py`
7. ✅ `src/services/irrigation.py`
8. ✅ `.env.example`
9. ✅ `.gitignore`

### Important (Makes demo polished)
10. ⭐ `src/bot/keyboards.py`
11. ⭐ `tests/test_irrigation.py`
12. ⭐ `README.md` (with setup instructions)

### Nice to have (If time permits)
13. 💡 `src/models/database.py`
14. 💡 `tests/test_plant_id.py`
15. 💡 `Procfile` (for Railway)

---

## ⚠️ Risk Mitigation

| Risk | Probability | Mitigation |
|------|------------|------------|
| Plant.id API rate limit | Medium | Cache common crops, manual fallback |
| Weather API downtime | Low | Hardcode default ET0 values |
| Photo quality issues | High | Add quality check, ask for retake |
| Date parsing fails | Medium | Provide date picker keyboard |
| Deployment issues | Medium | Prepare local polling mode demo |
| Demo internet failure | Low | Pre-record video backup |

---

## 🎯 Success Criteria

### Minimum Viable Product (Must have)
- [ ] Bot responds to `/start`
- [ ] Accepts photo and identifies crop
- [ ] Parses "tomorrow" in Kyrgyz/Russian
- [ ] Shows water recommendation in liters
- [ ] Works end-to-end at least once

### Good Demo (Should have)
- [ ] Works with 3+ different crops
- [ ] Handles rainy day scenario
- [ ] Kyrgyz language throughout
- [ ] Deployed and accessible via QR code
- [ ] Clean error messages

### Impressive Demo (Nice to have)
- [ ] Handles 5+ crops accurately
- [ ] Beautiful message formatting
- [ ] Voice message support
- [ ] Works with AVP schedule input
- [ ] Analytics dashboard

---

## 📞 Pre-Hackathon Preparation Checklist

### Week Before
- [ ] Register at https://plant.id/ → Get API key (250 free IDs)
- [ ] Create Telegram bot via @BotFather
- [ ] Test Plant.id API with sample photos
- [ ] Test Open-Meteo API (no key needed)
- [ ] Prepare 10 test crop photos

### Day Before
- [ ] Review FastAPI docs
- [ ] Review aiogram 3.x docs (note: breaking changes from 2.x)
- [ ] Set up Railway account
- [ ] Prepare laptop (charger, hotspot backup)
- [ ] Print one-page cheat sheet with API endpoints

### Morning Of
- [ ] Coffee ☕
- [ ] Clone starter template
- [ ] Verify all API keys work
- [ ] Set timer for phase checkpoints

---

## 🚀 Execution Strategy

### Time Management
- **Set 6-hour alarms** to force phase transitions
- **No gold-plating**: Finish core features first
- **Commit often**: Every 30 minutes or after feature completion
- **Demo-first mindset**: If it doesn't show in demo, it's optional

### Team Coordination (if applicable)
- Person 1: Backend (FastAPI + APIs)
- Person 2: Bot logic (handlers + FSM)
- Person 3: Business logic (irrigation calc) + Demo prep

### Red Flags (Stop and pivot if...)
- Hour 12: No working bot interaction
- Hour 24: No Plant.id response
- Hour 36: No irrigation calculation working

---

## 📚 Key Resources

### Documentation
- [aiogram 3.x docs](https://docs.aiogram.dev/en/latest/)
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Plant.id API](https://web.plant.id/plant-identification-api/)
- [Open-Meteo API](https://open-meteo.com/en/docs)

### Code References
- [aiogram FSM example](https://github.com/aiogram/aiogram/tree/dev-3.x/examples)
- [FAO Crop ET calculator](http://www.fao.org/3/x0490e/x0490e00.htm)

### Kyrgyz Resources
- Kyrgyz crop names dictionary (to be prepared)
- Common date phrases in Kyrgyz

---

## ✅ Definition of Done

**This project is complete when:**
1. A judge can scan QR code → Open bot
2. Judge sends crop photo → Gets crop name
3. Judge types "tomorrow" → Gets liter recommendation
4. All above happens in Kyrgyz language
5. Presentation clearly shows water savings impact

**Stretch goal:**
Judge tries 3 different crops → All work correctly

---

## 🎬 Final Deliverables

1. **GitHub Repository**
   - Clean commit history
   - README with setup instructions
   - All code documented

2. **Live Bot**
   - Deployed on Railway
   - QR code printed on presentation

3. **Presentation**
   - 10 slides (PDF + Keynote)
   - Demo video backup (MP4)

4. **Demo Materials**
   - 5 test photos on phone
   - Printed cheat sheet (date phrases)
   - Backup hotspot device

---

**Approval Needed:**
👉 Please review this plan and confirm:
1. Overall structure makes sense
2. 48-hour timeline is realistic
3. Any specific features to add/remove
4. Any Kyrgyz-specific requirements I missed

After approval, I'll start creating files in order of priority! 🚀
