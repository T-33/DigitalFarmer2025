# 🚀 Tamchy AI - Quick Start Guide

This guide will help you get Tamchy AI up and running in under 10 minutes!

---

## 📋 Prerequisites

Before starting, make sure you have:

- [ ] **Python 3.11+** installed ([Download](https://www.python.org/downloads/))
- [ ] **Git** installed
- [ ] **Telegram Bot Token** from [@BotFather](https://t.me/botfather)
- [ ] **Plant.id API Key** from [web.plant.id](https://web.plant.id/)

**Optional but Recommended:**
- [ ] **Docker Desktop** for containerized deployment ([Download](https://www.docker.com/products/docker-desktop))

---

## 🎯 Choose Your Path

### **Option A: Manual Setup** (Recommended for Development) ⚡
Best for: Active development, debugging, faster iteration

### **Option B: Docker Setup** 🐳
Best for: Production-like environment, team consistency

---

# Option A: Manual Setup ⚡

## Step 1: Clone and Setup Environment

```bash
# Navigate to project
cd FarmersHackathon

# Create .env files from templates
cp api/.env.example api/.env
cp bot/.env.example bot/.env
```

## Step 2: Configure API Keys

### Edit `api/.env`:
```env
PLANT_ID_API_KEY=your_actual_plant_id_key_here
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### Edit `bot/.env`:
```env
TELEGRAM_BOT_TOKEN=your_actual_telegram_token_here
BACKEND_API_URL=http://localhost:8000/api/v1
DEBUG=true
```

## Step 3: Setup Backend API

**Open Terminal 1:**

```bash
# Navigate to API folder
cd api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **Backend is running at http://localhost:8000**

## Step 4: Setup Telegram Bot

**Open Terminal 2 (keep Terminal 1 running!):**

```bash
# Navigate to Bot folder
cd bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

**Expected Output:**
```
INFO: Bot started successfully
INFO: Polling for updates...
```

✅ **Bot is running and listening for Telegram messages**

---

# Option B: Docker Setup 🐳

## Step 1: Prepare Environment

```bash
# Navigate to project root
cd FarmersHackathon

# Create root .env file for docker-compose
cp .env.example .env
```

**Edit `.env` (root level):**
```env
TELEGRAM_BOT_TOKEN=your_actual_telegram_token_here
PLANT_ID_API_KEY=your_actual_plant_id_key_here
DEBUG=true
```

## Step 2: Build and Start Services

```bash
# Build and start all services
docker-compose up --build
```

**Expected Output:**
```
[+] Building 45.2s (20/20) FINISHED
[+] Running 3/3
 ✔ Network tamchy-network     Created
 ✔ Container tamchy-backend   Started
 ✔ Container tamchy-bot       Started
```

**Alternative Commands:**

```bash
# Run in background (detached mode)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

✅ **Both services running in Docker**

---

# 🧪 Testing Your Setup

## Test 1: Backend Health Check

### Manual Setup:
```bash
curl http://localhost:8000/api/v1/health
```

### Docker Setup:
```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "plant_id_api": "connected",
  "weather_api": "connected"
}
```

✅ If you see this, backend is working!

---

## Test 2: API Documentation

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

You should see interactive API documentation.

✅ If you see the docs, FastAPI is configured correctly!

---

## Test 3: Telegram Bot

1. **Open Telegram**
2. **Search for your bot** (name you gave it in @BotFather)
3. **Send `/start` command**

**Expected Response from Bot:**
```
🌱 Тамчы AI'га кош келиңиз!

Мен сиздин талаңызга карап, канча суу керектигин айтып берем.

Баштоо үчүн талаңыздын сүрөтүн жөнөтүңүз 📸
```

✅ If you see this, bot is working!

---

## Test 4: End-to-End Flow (Mock Test)

**Test Crop Analysis Endpoint:**

```bash
# Create a test request file
cat > test_crop.json << 'EOF'
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
  "telegram_user_id": 123456789
}
EOF

# Test the endpoint
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d @test_crop.json
```

**Expected Response (or error if Plant.id needs real image):**
```json
{
  "success": true,
  "crop": {
    "name_ru": "Кукуруза",
    "name_kg": "Жүгөрү",
    "name_code": "corn",
    ...
  }
}
```

---

## Test 5: Water Schedule Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/water-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "crop_code": "corn",
    "growth_stage": "flowering",
    "water_date": "2025-11-30",
    "telegram_user_id": 123456789
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "water_date": "2025-11-30",
  "days_until_water": 4,
  "weather": {...},
  "recommendation": {...}
}
```

✅ If you get JSON response, irrigation logic is working!

---

# 🐛 Troubleshooting

## Problem: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your terminal prompt

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## Problem: Backend won't start - "Address already in use"

**Solution:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000

# Mac/Linux:
lsof -i :8000

# Kill the process (use PID from above)
# Windows:
taskkill /PID <PID> /F

# Mac/Linux:
kill -9 <PID>

# Or use a different port
uvicorn main:app --reload --port 8001
# Then update bot/.env: BACKEND_API_URL=http://localhost:8001/api/v1
```

---

## Problem: Bot not responding

**Checklist:**
1. ✅ Is backend running? Check http://localhost:8000/api/v1/health
2. ✅ Is bot process running without errors?
3. ✅ Is TELEGRAM_BOT_TOKEN correct in bot/.env?
4. ✅ Did you actually send `/start` to the bot in Telegram?
5. ✅ Is BACKEND_API_URL pointing to correct address?

**Debug Mode:**
```bash
# Enable debug logging in bot
cd bot
DEBUG=true python main.py
```

---

## Problem: Plant.id API errors

**Solution:**
```bash
# Check your API key is valid
# Log into https://web.plant.id/
# Verify key in api/.env

# Check quota (free tier: 250 IDs/month)
# If exceeded, wait or upgrade plan

# For testing without Plant.id:
# Edit api/.env:
MOCK_PLANT_ID=true
```

---

## Problem: Docker container won't start

**Solution:**
```bash
# View detailed logs
docker-compose logs backend
docker-compose logs bot

# Rebuild completely
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check if ports are available
# Make sure nothing is using port 8000
```

---

## Problem: "CORS error" in browser

**Solution:**

This is expected! The API is meant for bot, not browser.
- Bot → Backend: ✅ Works (no CORS)
- Browser → Backend: ❌ CORS blocked (by design)

If you need browser access, edit `api/.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:5173
```

---

# 📊 Verify Everything Works

Run this checklist:

### Backend Checklist
- [ ] `curl http://localhost:8000/api/v1/health` returns `{"status": "ok"}`
- [ ] http://localhost:8000/api/docs shows Swagger UI
- [ ] No errors in terminal/logs

### Bot Checklist
- [ ] Bot responds to `/start` in Telegram
- [ ] No errors in terminal/logs
- [ ] Bot can reach backend (check logs)

### Integration Checklist
- [ ] Send photo to bot (if handlers implemented)
- [ ] Bot forwards to backend
- [ ] Backend returns crop info
- [ ] Bot displays result

---

# 🎯 Next Steps

Once everything is working:

1. **For Backend Developer:**
   - Start implementing `api/main.py`
   - Follow `PLAN.md` Phase 2 (Backend)
   - Reference `API.md` for details

2. **For Bot Developer:**
   - Start implementing `bot/main.py`
   - Follow `PLAN.md` Phase 2 (Bot)
   - Reference `CONTRACT.md` for API contract

3. **For Both:**
   - Keep services running while developing
   - Changes auto-reload (--reload flag)
   - Test frequently with curl/Telegram

---

# 📚 Useful Commands Reference

## Manual Setup

### Backend
```bash
cd api
.\venv\Scripts\activate          # Windows
source venv/bin/activate         # Mac/Linux
uvicorn main:app --reload --port 8000
```

### Bot
```bash
cd bot
.\venv\Scripts\activate          # Windows
source venv/bin/activate         # Mac/Linux
python main.py
```

### Run Tests
```bash
# Backend tests
cd api
pytest tests/ -v

# Bot tests
cd bot
pytest tests/ -v
```

---

## Docker Setup

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs backend
docker-compose logs bot

# Stop services
docker-compose down

# Rebuild
docker-compose build --no-cache
docker-compose up --build

# Enter container shell
docker-compose exec backend bash
docker-compose exec bot bash

# Remove everything
docker-compose down -v
```

---

## Testing Commands

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Test with Pretty JSON
curl http://localhost:8000/api/v1/health | python -m json.tool

# Test crop analysis
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d @test_request.json

# Test water schedule
curl -X POST http://localhost:8000/api/v1/water-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "crop_code": "corn",
    "growth_stage": "flowering",
    "water_date": "2025-11-30",
    "telegram_user_id": 123
  }'
```

---

# ⚡ Pro Tips

1. **Use tmux or screen** to manage multiple terminals
2. **Enable auto-reload** (already default with --reload)
3. **Keep API docs open** (http://localhost:8000/api/docs)
4. **Use Postman/Insomnia** for API testing (easier than curl)
5. **Check logs frequently** - errors show up there first
6. **Use DEBUG=true** during development
7. **Commit often** - every feature that works

---

# 🆘 Still Having Issues?

1. Check `PLAN.md` for detailed implementation steps
2. Review `CONTRACT.md` for API contract
3. Read `CLAUDE.md` for architecture details
4. Check `PROJECT_STRUCTURE.md` for file locations

---

**Good luck! 🚀 Кыргыз дыйкандары үчүн!**

---

**Last Updated:** November 26, 2025
**Status:** Ready for Development
