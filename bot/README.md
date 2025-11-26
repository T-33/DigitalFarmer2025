# Tamchy AI - Telegram Bot

This is the Telegram bot service for Tamchy AI. It handles user interactions and communicates with the backend API.

## Setup

### 1. Install Dependencies

```bash
cd bot
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN
```

Get your bot token from [@BotFather](https://t.me/botfather).

### 3. Run the Bot

```bash
python main.py
```

## Project Structure

```
bot/
├── main.py              # Bot entry point
├── config.py            # Configuration settings
├── handlers/            # Message and command handlers
│   ├── start.py        # /start command
│   ├── photo.py        # Photo upload handler
│   └── schedule.py     # Irrigation date handler
├── keyboards/           # Telegram keyboards
│   └── inline.py       # Inline keyboards
├── states/              # FSM states
│   └── irrigation.py   # Irrigation flow states
└── services/            # Backend API client
    └── api_client.py   # HTTP client for backend
```

## Bot Commands

- `/start` - Start the bot and get instructions
- `/help` - Get help information

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Mock Mode

For testing without backend:

```bash
DEBUG=true python main.py
```

## Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather (required)
- `BACKEND_API_URL` - Backend API base URL (default: http://localhost:8000/api/v1)
- `API_TIMEOUT` - API request timeout in seconds (default: 30)
- `DEBUG` - Enable debug mode (default: false)

## Team Responsibilities

Bot developer is responsible for:
- Telegram user interface (messages, keyboards)
- FSM state management
- Date parsing (natural language → ISO format)
- Formatting backend responses for display
- Error handling (user-facing messages)

See [CONTRACT.md](../CONTRACT.md) for API contract with backend.
