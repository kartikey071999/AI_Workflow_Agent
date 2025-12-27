## Local Lint & Format Pipeline

You can run code quality checks locally at any time. This is optional and does not run automatically—it's for developer convenience.

### One-liner (using Makefile)

```powershell
make check
```

Or run manually:

```powershell
ruff check src/
black --check src/
```

To auto-format with black:

```powershell
black src/
```

> **Tip:** These checks are fast and only run if you choose to. No CI/CD or pre-commit hooks are enforced by default.


# AI Workflow Agent

Automated workflow for collecting AI news, summarizing content, and sending updates via Telegram (primary) and WhatsApp (optional). Designed for scheduled GitHub Actions pipeline runs, but can be run locally for development and testing.

## Features

- 📰 **AI News Collection** - Fetches the latest AI news using Perplexity API
- 🤖 **Summarization** - (Stub/optional) Summarize content with OpenAI/Gemini
- 📄 **PDF Generation** - (Stub/optional) Generate PDF reports (not active by default)
- 📲 **Telegram Delivery** - Send updates via Telegram bot (robust, error-handled)
- 📱 **WhatsApp Delivery** - (Optional) Send messages via Twilio WhatsApp API
- ⏰ **Automated Pipeline** - Runs as a scheduled GitHub Actions cron job (see .github/workflows/daily-tech-updates.yml)
- 🧑‍💻 **Local Dev Tools** - Fast, optional ruff/black checks via Makefile

> **Note:** Some features (PDF, WhatsApp, Summarizer) are present but not actively maintained or may be stubbed. Telegram and pipeline delivery are the main focus.

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


### 5. Run the Application (Locally or in CI)

```powershell
# Make sure virtual environment is activated
python src/main.py
```

Or let the GitHub Actions pipeline run it automatically on schedule (see .github/workflows/daily-tech-updates.yml).


## Project Structure

```
AI_Workflow_Agent/
├── src/
│   ├── main.py                    # Main pipeline entry point (Telegram, cron)
│   ├── config/
│   │   └── settings.py            # Configuration and environment variables
│   ├── senders/
│   │   └── telegram.py            # Telegram client (robust)
│   ├── services/
│   │   ├── collect_ai_news.py     # AI news collection service
│   │   ├── summarizer.py          # (Stub/optional)
│   │   ├── pdf_generator.py       # (Stub/optional)
│   │   └── whatsapp_sender.py     # WhatsApp messaging service (optional)
│   └── utils/
│       └── logger.py              # Logging utilities
├── jobs/                          # (Reserved for future jobs)
├── reports/                       # (Optional) Generated PDF reports
├── .env                           # Environment variables (not in git)
├── .env.example                   # Example environment file
├── Makefile                       # Local dev lint/format commands
├── pyproject.toml                 # Project dependencies & config
├── .github/
│   └── workflows/
│       └── daily-tech-updates.yml # GitHub Actions pipeline (cron job)
└── README.md                      # This file
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


## Development & Local Checks

### Install Dev Dependencies

```powershell
uv pip install -e ".[dev]"
```

### Lint & Format (Optional, Fast)

```powershell
make check   # ruff + black --check
make format  # auto-format with black
```

Or run manually:

```powershell
ruff check src/
black --check src/
```

### Type Checking (Optional)

```powershell
mypy src/
```


## GitHub Actions Pipeline

The project is designed to run as a scheduled pipeline (see .github/workflows/daily-tech-updates.yml). All secrets should be uploaded to GitHub Secrets. The pipeline will fail if any topic fails to process.

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
