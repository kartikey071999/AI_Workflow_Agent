import requests

from src.config import settings


class TelegramSendError(Exception):
    """Raised when Telegram message sending fails."""


class TelegramClient:
    def __init__(self, timeout: int = 10):
        if not settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not configured")
        if not settings.telegram_chat_id:
            raise ValueError("TELEGRAM_CHAT_ID is not configured")

        self.base_url = f"https://api.telegram.org/bot{settings.telegram_bot_token}"
        self.chat_id = settings.telegram_chat_id
        self.timeout = timeout

    def send(self, msg: str) -> None:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": msg,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()

        except requests.exceptions.Timeout as exc:
            raise TelegramSendError("Telegram API request timed out") from exc

        except requests.exceptions.RequestException as exc:
            raise TelegramSendError(f"Telegram API request failed: {exc}") from exc

        # Telegram returns 200 even for logical errors
        data = response.json()
        if not data.get("ok", False):
            description = data.get("description", "Unknown Telegram API error")
            raise TelegramSendError(f"Telegram API error: {description}")
