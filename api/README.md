# Tamchy AI - Backend API

This is the backend API service for Tamchy AI. It handles crop identification and irrigation calculations.

## Setup

### 1. Install Dependencies

```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your PLANT_ID_API_KEY
```

Get your Plant.id API key from [web.plant.id](https://web.plant.id/).

### 3. Run the Server

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Project Structure

```
api/
├── main.py              # FastAPI application entry point
├── core/
│   └── config.py       # Configuration settings
├── routers/             # API endpoints
│   ├── health.py       # GET /health
│   ├── crop.py         # POST /analyze-crop
│   └── water.py        # POST /water-schedule
├── services/            # Business logic
│   ├── plant_id.py     # Plant.id API integration
│   ├── weather.py      # Open-Meteo API integration
│   └── irrigation.py   # Irrigation calculations
└── models/              # Data models
    ├── requests.py     # Pydantic request schemas
    ├── responses.py    # Pydantic response schemas
    └── database.py     # SQLAlchemy models
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API Endpoints

### GET /api/v1/health
Health check endpoint.

### POST /api/v1/analyze-crop
Identify crop from photo (base64 encoded).

### POST /api/v1/water-schedule
Calculate irrigation recommendation.

See [CONTRACT.md](../CONTRACT.md) for full API specification.

## Development

### Running Tests

```bash
pytest tests/ -v --cov
```

### Manual Testing

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Test crop analysis (requires valid base64 image)
curl -X POST http://localhost:8000/api/v1/analyze-crop \
  -H "Content-Type: application/json" \
  -d @tests/sample_request.json
```

## Environment Variables

- `PLANT_ID_API_KEY` - Your Plant.id API key (required)
- `DEBUG` - Enable debug mode (default: false)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DATABASE_URL` - Database connection string
- `ALLOWED_ORIGINS` - CORS allowed origins (comma-separated)
- `MOCK_PLANT_ID` - Use mock responses for Plant.id (testing only)
- `MOCK_WEATHER` - Use mock responses for weather (testing only)

## External APIs

### Plant.id API
- **Docs**: https://web.plant.id/plant-identification-api/
- **Free tier**: 250 identifications/month

### Open-Meteo API
- **Docs**: https://open-meteo.com/en/docs
- **Free**: No API key required

## Team Responsibilities

Backend developer is responsible for:
- Plant.id API integration
- Weather API integration
- Irrigation calculation logic
- Crop coefficient database
- API endpoint implementation
- Data validation (Pydantic)

See [API.md](../API.md) for detailed API documentation.
