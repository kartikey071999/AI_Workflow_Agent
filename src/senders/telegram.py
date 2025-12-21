import requests
from src.config import settings


class TelegramClient:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{settings.telegram_bot_token}"
        self.chat_id = settings.telegram_chat_id

    def send(self, msg: str) -> None:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": msg,
            "parse_mode": "Markdown",
        }
        requests.post(url, json=payload)
