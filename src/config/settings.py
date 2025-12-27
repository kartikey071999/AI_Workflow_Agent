from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # ------------------------
    # TOPICS CONFIG
    # ------------------------
    topics: list[str] = Field(..., alias="TOPICS")
    # ------------------------
    # API KEYS
    # ------------------------
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    perplexity_api_key: str = Field(..., alias="PERPLEXITY_API_KEY")

    # ------------------------
    # TWILIO WHATSAPP CONFIG
    # ------------------------
    twilio_account_sid: str = Field(..., alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(..., alias="TWILIO_AUTH_TOKEN")
    twilio_whatsapp_number: str = Field(..., alias="TWILIO_WHATSAPP_NUMBER")
    my_whatsapp_number: str = Field(..., alias="MY_WHATSAPP_NUMBER")

    telegram_bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str = Field(..., alias="TELEGRAM_CHAT_ID")

    # ------------------------
    # FILE / REPORT CONFIG
    # ------------------------
    report_output_dir: str = Field("reports", alias="REPORT_OUTPUT_DIR")

    # ------------------------
    # APP SETTINGS
    # ------------------------
    environment: str = Field("development", alias="ENVIRONMENT")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    # ------------------------
    # Pydantic Config
    # ------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        json_loads_kwargs={"strict": False},
    )

    def create_directories(self):
        """
        Ensure required directories exist.
        Creates the 'reports' directory (or custom path from env) if it doesn't exist.
        This is where PDF reports will be saved.
        """
        Path(self.report_output_dir).mkdir(parents=True, exist_ok=True)
