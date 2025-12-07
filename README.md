# AI Workflow Agent

Automated workflow for collecting AI news, summarizing content, generating PDF reports, and sending them via WhatsApp.

## Features

- 📰 **AI News Collection** - Fetch latest AI news using Perplexity API
- 🤖 **Smart Summarization** - Summarize content with OpenAI/Gemini
- 📄 **PDF Generation** - Create professional PDF reports
- 📱 **WhatsApp Delivery** - Send reports via Twilio WhatsApp API

## Setup Instructions

### 1. Install uv (if not already installed)

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create Virtual Environment

```powershell
# Navigate to project directory
cd c:\Users\karti\OneDrive\Documents\GitHub\AI_Workflow_Agent

# Create virtual environment with uv
uv venv

# Activate the virtual environment
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
# Install all project dependencies
uv pip install -e .

# Or install with dev dependencies
uv pip install -e ".[dev]"
```

### 4. Configure Environment Variables

```powershell
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual credentials
notepad .env
```

Required API keys:
- **OpenAI API Key** - Get from https://platform.openai.com/api-keys
- **Gemini API Key** - Get from https://aistudio.google.com/app/apikey
- **Perplexity API Key** - Get from https://www.perplexity.ai/settings/api
- **Twilio Account SID & Auth Token** - Get from https://www.twilio.com/console
- **Twilio WhatsApp Number** - Set up at https://www.twilio.com/console/sms/whatsapp/sandbox

### 5. Run the Application

```powershell
# Make sure virtual environment is activated
python src/main.py
```

## Project Structure

```
AI_Workflow_Agent/
├── src/
│   ├── main.py                    # Main application entry point
│   ├── config/
│   │   └── settings.py            # Configuration and environment variables
│   ├── services/
│   │   ├── collect_ai_news.py     # AI news collection service
│   │   ├── summarizer.py          # Content summarization service
│   │   ├── pdf_generator.py       # PDF report generation
│   │   └── whatsapp_sender.py     # WhatsApp messaging service
│   └── utils/
│       └── logger.py              # Logging utilities
├── reports/                       # Generated PDF reports
├── .env                          # Environment variables (not in git)
├── .env.example                  # Example environment file
├── pyproject.toml                # Project dependencies
└── README.md                     # This file
```

## Quick Start with uv

```powershell
# One-liner setup (after installing uv)
uv venv && .venv\Scripts\Activate.ps1 && uv pip install -e . && cp .env.example .env
```

Then edit `.env` with your API keys and run:

```powershell
python src/main.py
```

## Development

### Install Dev Dependencies

```powershell
uv pip install -e ".[dev]"
```

### Code Formatting

```powershell
black src/
```

### Linting

```powershell
ruff check src/
```

### Type Checking

```powershell
mypy src/
```

## Troubleshooting

### Virtual Environment Not Activating

```powershell
# If execution policy prevents activation
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.venv\Scripts\Activate.ps1
```

### Missing Dependencies

```powershell
# Reinstall all dependencies
uv pip install -e . --force-reinstall
```

## License

MIT License
