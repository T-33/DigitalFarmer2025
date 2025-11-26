# 🌱 Tamchy AI - Smart Irrigation Assistant

> **Tamchy** (Тамчы) means "drop" in Kyrgyz — every drop counts!

An intelligent Telegram bot that helps Kyrgyz farmers save water and increase yields through AI-powered crop recognition and weather-based irrigation recommendations.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![aiogram](https://img.shields.io/badge/aiogram-3.3-orange.svg)](https://docs.aiogram.dev/)

---

## 🎯 Problem & Solution

### The Problem
- **65%** of water in Kyrgyzstan is used inefficiently
- Farmers irrigate "by eye" without data
- Water schedules (AVP) don't match actual crop needs

### Our Solution
An AI agronomist in your pocket that:
1. 📸 **Sees** your field through photos (Plant.id)
2. 🌤️ **Knows** weather for the week ahead
3. 💧 **Calculates** exact water requirements
4. ⏰ **Accounts** for your irrigation schedule

### Impact
- 💧 **30% water savings**
- 📈 **15% yield increase**
- 👨‍🌾 **350,000 farmers** in Kyrgyzstan
- 🌍 Supports UN SDGs #2, #6, #13

---

## 🏗️ Architecture

This project uses a **microservices architecture** with two independent services:

```
┌─────────────────┐         API Contract         ┌─────────────────┐
│                 │  ◄─────────────────────────► │                 │
│   TELEGRAM BOT  │                              │   BACKEND API   │
│                 │   POST /analyze-crop         │                 │
│  (User Interface)   POST /water-schedule       │ (Business Logic)│
│                 │   GET  /health               │                 │
│   Port: 3000    │                              │   Port: 8000    │
└─────────────────┘                              └─────────────────┘
      │                                                  │
      │                                                  │
      ▼                                                  ▼
  Telegram API                                   Plant.id + Weather
```

### Why Separated?

- ✅ **Parallel development** — Backend and Bot teams work independently
- ✅ **Clear contracts** — API-first approach
- ✅ **Easier testing** — Mock either service
- ✅ **Scalability** — Deploy and scale separately

---

## 📁 Project Structure

```
FarmersHackathon/
│
├── CONTRACT.md              # 🤝 API contract (READ THIS FIRST!)
├── API.md                   # 📚 Backend API documentation
├── CLAUDE.md                # 📖 Full project documentation
├── PLAN.md                  # 📋 48-hour development plan
├── README.md                # 👋 You are here
├── docker-compose.yml       # 🐳 Run both services
│
├── bot/                     # 🤖 Telegram Bot Service
│   ├── main.py
│   ├── config.py
│   ├── handlers/            # Command handlers
│   ├── states/              # FSM states
│   ├── services/            # API client
│   ├── requirements.txt
│   └── .env.example
│
├── api/                     # 🔧 Backend API Service
│   ├── main.py
│   ├── core/                # Configuration
│   ├── routers/             # FastAPI endpoints
│   ├── services/            # Business logic
│   │   ├── plant_id.py
│   │   ├── weather.py
│   │   └── irrigation.py
│   ├── models/              # Pydantic models
│   ├── requirements.txt
│   └── .env.example
│
└── tests/                   # 🧪 Tests
    ├── bot/
    └── api/
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional but recommended)
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Plant.id API Key ([get here](https://web.plant.id/))

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd FarmersHackathon

# 2. Create environment files
cp bot/.env.example bot/.env
cp api/.env.example api/.env

# 3. Edit .env files with your API keys
# bot/.env: Add TELEGRAM_BOT_TOKEN
# api/.env: Add PLANT_ID_API_KEY

# 4. Run both services
docker-compose up --build
```

**Services will be available at:**
- Backend API: http://localhost:8000/api/docs
- Telegram Bot: Running and polling

### Option 2: Manual Setup

**Terminal 1 (Backend):**
```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Plant.id API key
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Bot):**
```bash
cd bot
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Telegram bot token
python main.py
```

---

## 💬 How to Use

1. **Start the bot** on Telegram: `/start`
2. **Send a photo** of your crop
3. **Bot identifies** the plant: "Identified: Corn 🌽"
4. **Tell when water comes**: "эртең" (tomorrow) or "2 дан кийин" (in 2 days)
5. **Get recommendation**: "650 liters per sotka ⚠️ Critical"

### Example Conversation (Kyrgyz)

```
👤: /start
🤖: 🌱 Тамчы AI'га кош келиңиз!
    Талаңыздын сүрөтүн жөнөтүңүз 📸

👤: [sends photo of corn field]
🤖: ✅ Таанылды: Жүгөрү
    🌸 Өсүү этабы: Цветение
    🔴 Суу керектиги: Жогору

    Качан суу келет?

👤: эртең
🤖: 💧 СУУ БЕРҮҮ КЕҢЕШИ

    📅 Дата: 27.11.2025 (Бейшемби)
    🌡️ Аба ырайы: 12°C
    🌧️ Жамгыр: 0 мм

    💦 Суу көлөмү: 650 л/сотка
    ⚠️ Критично

    Сенин жүгөрүң гүлдөө стадиясында — абдан маанилүү кезең!
```

---

## 🧪 Testing

### Backend Tests
```bash
cd api
pytest tests/ -v --cov
```

### Bot Tests
```bash
cd bot
pytest tests/ -v
```

### Manual API Testing
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Test with sample image (requires base64)
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d @tests/sample_request.json
```

---

## 📚 Documentation

- **[CONTRACT.md](CONTRACT.md)** — API contract between Bot and Backend
- **[API.md](API.md)** — Backend API reference
- **[CLAUDE.md](CLAUDE.md)** — Complete project documentation
- **[PLAN.md](PLAN.md)** — 48-hour hackathon development plan

---

## 🛠️ Tech Stack

### Backend API
- **Framework:** FastAPI
- **Plant Recognition:** Plant.id API
- **Weather Data:** Open-Meteo API (free!)
- **Database:** SQLite + SQLAlchemy
- **Validation:** Pydantic

### Telegram Bot
- **Framework:** aiogram 3.3
- **HTTP Client:** httpx
- **Date Parsing:** dateparser
- **State Management:** FSM (Finite State Machine)

### Infrastructure
- **Containerization:** Docker + docker-compose
- **Deployment:** Railway / Fly.io
- **CI/CD:** GitHub Actions (planned)

---

## 🌍 Supported Crops

- 🌽 **Corn** (Кукуруза / Жүгөрү)
- 🌾 **Wheat** (Пшеница / Буудай)
- ☁️ **Cotton** (Хлопок / Мамык)
- 🥕 **Vegetables** (various)

*More crops coming soon!*

---

## 🔮 Roadmap

### Phase 1: MVP (Hackathon - 48 hours) ✅
- [x] Telegram bot interface
- [x] Plant.id crop recognition
- [x] Weather-based recommendations
- [x] Kyrgyz language support

### Phase 2: Post-Hackathon
- [ ] AVP (water distribution) system integration
- [ ] Sentinel-2 satellite imagery
- [ ] Voice message input
- [ ] SMS fallback (no internet)
- [ ] Field area estimation

### Phase 3: Scale
- [ ] Mobile app (Flutter)
- [ ] Multi-language (Kyrgyz, Russian, Uzbek)
- [ ] Farmer community features
- [ ] Government reporting dashboard
- [ ] Soil moisture sensor integration

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Code Style:**
- Python: Black formatter, type hints
- Conventional Commits
- Tests for new features

---

## 📄 License

[To be determined after hackathon]

---

## 👥 Team

Built with ❤️ for Kyrgyz farmers during [Hackathon Name]

- **Backend Developer:** [Your Name]
- **Bot Developer:** [Friend's Name]
- **Presentation:** [Team Member]

---

## 📞 Contact

- **Issues:** [GitHub Issues](your-repo-url/issues)
- **Telegram:** [@your_username](https://t.me/your_username)
- **Email:** your@email.com

---

## 🙏 Acknowledgments

- Plant.id for crop recognition API
- Open-Meteo for free weather data
- FAO for irrigation calculation methodology
- Kyrgyz farmers for inspiration

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/tamchy-ai)
![GitHub forks](https://img.shields.io/github/forks/yourusername/tamchy-ai)
![GitHub issues](https://img.shields.io/github/issues/yourusername/tamchy-ai)

---

**Кыргыз дыйкандары үчүн ❤️ менен жасалган**
**Built with ❤️ for Kyrgyz farmers**
