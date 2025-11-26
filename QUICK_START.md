# 🚀 MurabAI Quick Start Guide

Get MurabAI running in 5 minutes!

---

## Prerequisites

- Docker & Docker Compose installed
- Python 3.11+ (if running without Docker)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Plant.id API Key (optional for MVP, can use mock mode)

---

## Quick Start with Docker (Recommended)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd DigitalFarmer2025
```

### 2. Configure Environment

```bash
# Copy example files
cp .env.example .env
```

**Edit `.env` file:**

```bash
# Telegram Bot (Required)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # Get from @BotFather

# Plant.id API (Optional - use mock mode for testing)
PLANT_ID_API_KEY=                     # Leave empty for mock mode

# Application Settings
DEBUG=true
MOCK_PLANT_ID=true                    # Use mock data (no real API calls)
MOCK_WEATHER=true                     # Use mock weather data
```

### 3. Start Services

```bash
docker-compose up --build
```

**What starts:**
- 🔧 Backend API → `http://localhost:8000`
- 📚 API Docs → `http://localhost:8000/api/v1/docs`
- 🤖 Telegram Bot → Running and ready

### 4. Test the Bot

1. Open Telegram
2. Find your bot: `@YourBotUsername` (from @BotFather)
3. Send `/start`
4. Upload a crop photo (any plant photo works in mock mode)
5. Select "Эртең" (tomorrow)
6. Receive irrigation recommendation! 💧

---

## Manual Setup (Without Docker)

### Backend API

```bash
# Terminal 1
cd api
python -m venv venv
source venv/bin/activate      # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Telegram Bot

```bash
# Terminal 2
cd bot
python -m venv venv
source venv/bin/activate      # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Verification & Testing

### ✅ Check Backend Health

```bash
curl http://localhost:8000/api/v1/health
```

**Expected response:**
```json
{
  "status": "ok",
  "plant_id_api": "connected",
  "weather_api": "connected"
}
```

### ✅ Check Bot Commands

Open Telegram and test:

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message |
| `/help` | Display help information |
| `/stats` | View demo statistics |
| `/feedback` | Leave feedback rating |

### ✅ Test Full Flow

1. Send `/start`
2. Upload photo (corn, wheat, tomato work best)
3. Wait for AI recognition (~2-3 seconds)
4. Click "Эртең" (tomorrow) button
5. Receive detailed recommendation with:
   - Water volume (liters/sotka)
   - Urgency level
   - Weather forecast
   - Personalized advice

---

## Troubleshooting

### Problem: Bot doesn't respond

**Solutions:**
```bash
# Check bot logs
docker logs -f digitalfarmer2025_bot_1

# Verify token
echo $TELEGRAM_BOT_TOKEN

# Restart bot
docker-compose restart bot
```

### Problem: Backend returns errors

**Solutions:**
```bash
# Check API logs
docker logs -f digitalfarmer2025_api_1

# Test health endpoint
curl http://localhost:8000/api/v1/health

# Restart API
docker-compose restart api
```

### Problem: "Connection refused"

**Solutions:**
```bash
# Check running containers
docker ps

# Check port availability
netstat -an | grep 8000   # Linux/Mac
netstat -an | findstr 8000  # Windows

# Rebuild from scratch
docker-compose down
docker-compose up --build
```

### Problem: Images not recognized

**Check:**
- ✅ Image size < 10MB
- ✅ Image format: JPEG, PNG, GIF, BMP
- ✅ `MOCK_PLANT_ID=true` in .env (for testing)
- ✅ Plant is clearly visible in photo

---

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | From @BotFather |
| `PLANT_ID_API_KEY` | ❌ No | - | Plant.id API key |
| `MOCK_PLANT_ID` | ❌ No | true | Use mock plant recognition |
| `MOCK_WEATHER` | ❌ No | true | Use mock weather data |
| `DEBUG` | ❌ No | true | Enable debug logging |
| `HOST` | ❌ No | 0.0.0.0 | API host |
| `PORT` | ❌ No | 8000 | API port |
| `API_VERSION` | ❌ No | v1 | API version prefix |

### Docker Compose Ports

| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/api/v1/docs |
| Bot | - | Connects to Telegram |

---

## Production Deployment

### Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly deploy
```

### Environment Variables for Production

```bash
# Set in Railway/Fly.io dashboard
TELEGRAM_BOT_TOKEN=your_production_token
PLANT_ID_API_KEY=your_real_api_key
MOCK_PLANT_ID=false
MOCK_WEATHER=false
DEBUG=false
```

---

## Next Steps

### 1. Get Real API Keys (Production)

- **Plant.id:** https://web.plant.id/api-access-request/
  - Free tier: 100 requests/day
  - Paid: Unlimited

- **Open-Meteo:** https://open-meteo.com/
  - Free for non-commercial use

### 2. Read Documentation

- 📚 [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - Complete API reference
- 📋 [CONTRACT.md](./CONTRACT.md) - API contract specs
- 🎬 [DEMO.md](./DEMO.md) - Hackathon demo script
- 📝 [12H_PLAN.md](./12H_PLAN.md) - Development roadmap

### 3. Customize for Your Region

Edit `api/core/constants.py`:
```python
# Change default location
DEFAULT_LATITUDE = 42.8746  # Your latitude
DEFAULT_LONGITUDE = 74.5698  # Your longitude

# Add more crops
CROP_NAMES["apple"] = {"ru": "Яблоко", "kg": "Алма", "en": "Apple"}
```

---

## Development Workflow

### Running Tests

```bash
# Backend tests
cd api
pytest tests/ -v

# Bot tests
cd bot
pytest tests/ -v
```

### Code Formatting

```bash
# Format code
black .
isort .

# Lint
flake8 .
mypy .
```

### Database Migrations (Future)

```bash
# When database is added
alembic upgrade head
```

---

## Support & Resources

- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/murabai/issues)
- 💬 **Telegram:** @MurabAI_Support
- 📧 **Email:** support@murabai.kg
- 📖 **Docs:** http://localhost:8000/api/v1/docs

---

## FAQ

**Q: Do I need Plant.id API key for testing?**
A: No! Set `MOCK_PLANT_ID=true` to use mock data.

**Q: What crops are supported?**
A: Corn, wheat, cotton, tomato, potato, onion, carrot, beet, cucumber, pepper.

**Q: Can I add new languages?**
A: Yes! Edit `bot/utils/language.py` to add translations.

**Q: How accurate is the irrigation calculation?**
A: Based on FAO-56 standard. In mock mode, uses sample data.

**Q: Can I use this for other countries?**
A: Yes! Change coordinates in `api/core/constants.py`.

---

**Happy Coding! 🌾💻**

Last updated: November 26, 2025
