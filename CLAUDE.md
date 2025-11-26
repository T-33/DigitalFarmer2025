# Tamchy AI - Irrigation Assistant Bot

## 📋 Project Overview

**Tamchy AI** is an intelligent Telegram bot that helps farmers in Kyrgyzstan optimize water usage through AI-powered crop recognition and weather-based irrigation recommendations.

### Problem Statement
- 65% of water in Kyrgyzstan is used inefficiently
- Farmers irrigate "by eye" without considering weather and crop growth stages
- Water distribution schedules (AVP) are not synchronized with actual needs

### Solution
An AI agronomist in your pocket that:
1. **Sees** the field through photos (Plant.id API)
2. **Knows** weather forecast for the week ahead (Open-Meteo API)
3. **Calculates** precise water requirements
4. **Accounts** for the AVP irrigation schedule

## 🎯 Business Impact

| Metric | Value |
|---------|-------|
| 💧 Water Savings | up to 30% |
| 📈 Yield Increase | up to 15% |
| 👨‍🌾 Target Audience | 350,000 farmers in Kyrgyzstan |
| 🌍 SDG Goals | #2 (Zero Hunger), #6 (Clean Water), #13 (Climate Action) |

## 🏗️ Technical Architecture

### Architecture Overview
The system is split into **two independent services** communicating via REST API:

```
┌─────────────────┐         API Contract         ┌─────────────────┐
│                 │  ◄─────────────────────────► │                 │
│   TELEGRAM BOT  │                              │   BACKEND API   │
│                 │   POST /analyze-crop         │                 │
│   (User Interface)   POST /water-schedule      │   (Business Logic)
│                 │   GET  /health               │                 │
│   Port: 3000    │                              │   Port: 8000    │
└─────────────────┘                              └─────────────────┘
      │                                                  │
      │                                                  │
      ▼                                                  ▼
  Telegram API                                   Plant.id + Weather APIs
```

### Technology Stack

**Backend API (FastAPI)**
- Framework: FastAPI
- Plant Recognition: Plant.id API
- Weather Data: Open-Meteo API
- Database: SQLAlchemy + aiosqlite
- Validation: Pydantic

**Telegram Bot (aiogram)**
- Bot Framework: aiogram 3.3.0
- HTTP Client: httpx (for API calls)
- Date Parsing: dateparser
- State Management: aiogram FSM

**Infrastructure**
- Containerization: Docker + docker-compose
- Deployment: Railway / Fly.io
- Environment: python-dotenv

### Project Structure
```
FarmersHackathon/
│
├── CONTRACT.md              # 🤝 API contract specification
├── API.md                   # 📚 Backend API documentation
├── README.md                # Project overview
├── docker-compose.yml       # Run both services together
├── .gitignore
│
├── bot/                     # 🤖 TELEGRAM BOT (Independent service)
│   ├── main.py             # Bot entry point
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py        # /start command
│   │   ├── photo.py        # Photo handling
│   │   └── schedule.py     # Irrigation date input
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── inline.py       # Inline keyboards
│   ├── states/
│   │   ├── __init__.py
│   │   └── irrigation.py   # FSM states
│   ├── services/
│   │   ├── __init__.py
│   │   └── api_client.py   # Backend API client
│   ├── config.py           # Bot configuration
│   ├── requirements.txt    # Bot dependencies
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md           # Bot-specific docs
│
├── api/                     # 🔧 BACKEND API (Independent service)
│   ├── main.py             # FastAPI application
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── crop.py         # POST /analyze-crop
│   │   ├── water.py        # POST /water-schedule
│   │   └── health.py       # GET /health
│   ├── services/
│   │   ├── __init__.py
│   │   ├── plant_id.py     # Plant.id integration
│   │   ├── weather.py      # Open-Meteo integration
│   │   └── irrigation.py   # Irrigation calculations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py     # Pydantic request models
│   │   ├── responses.py    # Pydantic response models
│   │   └── database.py     # SQLAlchemy models
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py       # API configuration
│   ├── requirements.txt    # API dependencies
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md           # API-specific docs
│
└── tests/                   # 🧪 Tests for both services
    ├── bot/
    │   └── test_handlers.py
    └── api/
        ├── test_crop_analysis.py
        ├── test_water_schedule.py
        └── test_services.py
```

## 🔑 Environment Variables

### Backend API (`api/.env`)
```env
# Plant.id API
PLANT_ID_API_KEY=your_plant_id_api_key

# Application
DEBUG=true
HOST=0.0.0.0
PORT=8000
API_VERSION=v1

# Database
DATABASE_URL=sqlite+aiosqlite:///./tamchy.db

# CORS (for bot communication)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Telegram Bot (`bot/.env`)
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# Backend API
BACKEND_API_URL=http://localhost:8000/api/v1
API_TIMEOUT=30

# Application
DEBUG=true
PORT=3000
```

## 🤖 Bot Conversation Flow

### User Journey
1. **Start**: User sends `/start` command
2. **Photo Upload**: User sends a photo of their crop
3. **API Call**: Bot → Backend `/analyze-crop` endpoint
4. **Recognition**: Backend identifies plant via Plant.id
5. **Irrigation Date**: Bot asks when water will be available (AVP schedule)
6. **API Call**: Bot → Backend `/water-schedule` endpoint
7. **Weather Check**: Backend fetches forecast and calculates
8. **Recommendation**: Bot displays formatted recommendation to user

### FSM States (Bot Side)
```python
class IrrigationStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_irrigation_date = State()
```

### API Endpoints (Backend Side)

#### 1. POST `/api/v1/analyze-crop`
Analyzes crop photo and returns identification.

**Request:**
```json
{
  "image_base64": "string (base64 encoded image)",
  "telegram_user_id": 123456789
}
```

**Response:**
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

#### 2. POST `/api/v1/water-schedule`
Calculates irrigation recommendation based on crop and date.

**Request:**
```json
{
  "crop_code": "corn",
  "growth_stage": "flowering",
  "water_date": "2025-11-29",
  "telegram_user_id": 123456789
}
```

**Response:**
```json
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
    "message_ru": "Твоя кукуруза на стадии цветения...",
    "message_kg": "Сенин жүгөрүң гүлдөө стадиясында..."
  }
}
```

#### 3. GET `/api/v1/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "plant_id_api": "connected",
  "weather_api": "connected"
}
```

## 📊 Irrigation Calculation Logic

### Inputs
1. Crop type (from Plant.id)
2. Growth stage (inferred from photo analysis)
3. Weather forecast (temperature, precipitation, humidity)
4. Planned irrigation date
5. Field location (coordinates)

### Formula (Simplified MVP)
```
Base water need = crop_coefficient × reference_evapotranspiration
Adjusted need = base_need - expected_rainfall
Daily recommendation = adjusted_need × area
```

### Crop Coefficients (Kc) for Kyrgyzstan
- Wheat: 0.3-1.15 (by stage)
- Corn: 0.3-1.20 (by stage)
- Cotton: 0.35-1.15 (by stage)
- Vegetables: 0.45-1.05 (by stage)

## 🌐 External API Integration Details (Backend Only)

### Plant.id API
**Endpoint:** `POST https://api.plant.id/v2/identify`

**Headers:**
```
Content-Type: application/json
Api-Key: {PLANT_ID_API_KEY}
```

**Request Body:**
```json
{
  "images": ["base64_encoded_image"],
  "modifiers": ["crops", "similar_images"],
  "plant_language": "ru",
  "plant_details": ["common_names", "taxonomy", "url"]
}
```

**Used by:** `api/services/plant_id.py`

### Open-Meteo API
**Endpoint:** `GET https://api.open-meteo.com/v1/forecast`

**Query Parameters:**
```
latitude=42.8746
longitude=74.5698
daily=temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration
timezone=Asia/Bishkek
forecast_days=7
```

**Used by:** `api/services/weather.py`

## 🎨 User Interface (Telegram)

### Message Templates (Kyrgyz Language)
```
🌱 Тамчы AI'га кош келиңиз!

Мен сиздин талаңызга карап, канча суу керектигин айтып берем.

Баштоо үчүн талаңыздын сүрөтүн жөнөтүңүз 📸
```

```
✅ Таанылды: {crop_name}
🌾 Өсүү этабы: {growth_stage}

Качан суу келет? (мисалы: "бүгүн", "эртең", "шаршемби")
```

```
💧 Суу берүү кеңеши:

📅 Дата: {date}
🌡️ Аба ырайы: {weather_summary}
💦 Суу көлөмү: {liters} литр/га

⚠️ {warning_if_any}
```

## 📱 Demo Scenario for Judges

1. **Problem Introduction** (30 sec)
   - "In Kyrgyzstan, 65% of water is lost due to improper irrigation"

2. **Live Demo** (2 min)
   - Open Telegram bot
   - Send pre-prepared corn photo
   - Bot responds: "Identified: Corn, flowering stage..."
   - Type "on Friday"
   - Bot provides recommendation with liters and forecast

3. **Second Example** (1 min)
   - Send wheat photo
   - Quick response demonstrating versatility

4. **Next Steps** (30 sec)
   - AVP system integration
   - Sentinel-2 satellite imagery
   - Voice input support

## 🚀 Development Checklist (48 Hours)

### Phase 1: Setup & Contract (Hours 1-6)
- [ ] Create project structure (bot/ and api/ folders)
- [ ] Write CONTRACT.md with API specification
- [ ] Set up Telegram bot via @BotFather
- [ ] Obtain Plant.id API key
- [ ] Configure docker-compose.yml
- [ ] Create .env.example for both services

### Phase 2: Parallel Development (Hours 6-24)

**Backend Team:**
- [ ] FastAPI application setup
- [ ] `/health` endpoint
- [ ] Plant.id service integration
- [ ] Open-Meteo service integration
- [ ] `/analyze-crop` endpoint
- [ ] `/water-schedule` endpoint
- [ ] Pydantic models for validation

**Bot Team:**
- [ ] aiogram bot setup
- [ ] `/start` command handler
- [ ] FSM states definition
- [ ] Photo handler + API client
- [ ] Date parsing with dateparser
- [ ] Irrigation date handler + API client
- [ ] Message formatting

### Phase 3: Integration & Testing (Hours 24-36)
- [ ] Connect bot to backend API
- [ ] End-to-end testing
- [ ] Error handling (both services)
- [ ] Kyrgyz language messages
- [ ] Crop coefficient tuning
- [ ] Weather-based adjustments

### Phase 4: Deploy & Demo (Hours 36-48)
- [ ] Docker images build
- [ ] Deploy backend to Railway
- [ ] Deploy bot to Railway
- [ ] Test with real crop photos
- [ ] Prepare demo scenario
- [ ] Create presentation slides
- [ ] Record backup demo video

## 🧪 Testing Strategy

### Unit Tests
- Plant.id API response parsing
- Weather data processing
- Irrigation calculations
- Date parsing edge cases

### Integration Tests
- End-to-end bot conversation flow
- API error handling
- Database operations

### Manual Testing
- Real crop photos from Kyrgyzstan
- Various date input formats
- Different weather conditions

## 📈 Future Enhancements

### Phase 2 (Post-Hackathon)
- AVP (water distribution) system integration
- Sentinel-2 satellite imagery analysis
- Voice message input (Kyrgyz language)
- SMS fallback for areas without internet
- Field area estimation from photos
- Soil moisture sensor integration

### Phase 3 (Scale)
- Mobile app (Flutter)
- Multi-language support (Kyrgyz, Russian, Uzbek)
- Community features (farmer network)
- Marketplace integration
- Government reporting dashboard

## 🔄 Development Workflow

### Contract-First Approach
1. **Define API contract** in `CONTRACT.md`
2. **Agree on request/response formats**
3. **Work independently** on bot and backend
4. **Integrate** when both are ready

### Running Locally

**Option 1: Docker Compose (Recommended)**
```bash
docker-compose up --build
```
- Backend runs on `http://localhost:8000`
- Bot connects to backend automatically

**Option 2: Separate Terminals**

Terminal 1 (Backend):
```bash
cd api
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Terminal 2 (Bot):
```bash
cd bot
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### Testing Backend Without Bot
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Test crop analysis (with sample base64 image)
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "...", "telegram_user_id": 123}'
```

### Testing Bot Without Backend
Use mock responses in `bot/services/api_client.py`:
```python
if os.getenv("DEBUG") == "true":
    return MockResponse(...)
```

## 🤝 Team Collaboration

### Bot Developer Responsibilities
- Telegram user interface (messages, keyboards)
- FSM state management
- Date parsing (natural language → ISO format)
- Formatting backend responses for display
- Error handling (user-facing messages)

### Backend Developer Responsibilities
- Plant.id API integration
- Weather API integration
- Irrigation calculation logic
- Crop coefficient database
- API endpoint implementation
- Data validation (Pydantic)

### Shared Responsibilities
- API contract definition
- Integration testing
- Demo preparation
- Documentation

## 📄 License

[To be determined after hackathon]

---

**Built with ❤️ for Kyrgyz farmers**
**Кыргыз дыйкандары үчүн ❤️ менен жасалган**
