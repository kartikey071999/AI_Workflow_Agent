"""
WhatsApp Sender Service
Sends messages and files via Twilio WhatsApp API
"""

import logging
from pathlib import Path

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from src.config import settings

logger = logging.getLogger(__name__)


class WhatsAppSender:
    """Service for sending WhatsApp messages via Twilio."""

    def __init__(self):
        """Initialize Twilio client with credentials from settings."""
        self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

        # Ensure numbers contain ONLY digits and + prefix
        self.from_number = f"whatsapp:{settings.twilio_whatsapp_number}"
        self.to_number = f"whatsapp:{settings.my_whatsapp_number}"

        logger.info("WhatsApp sender initialized")

    def send_message(
        self,
        message: str = None,
        content_sid: str = None,
        content_variables: dict = None,
    ) -> bool:
        """
        Send a WhatsApp message using text or a Twilio Content Template.
        """

        try:
            if content_sid:
                # TEMPLATE MESSAGE
                logger.info("Sending WhatsApp template message...")

                payload = {
                    "from_": self.from_number,
                    "to": self.to_number,
                    "content_sid": content_sid,
                }

                if content_variables:
                    from json import dumps

                    payload["content_variables"] = dumps(content_variables)

            else:
                # NORMAL TEXT MESSAGE
                logger.info("Sending WhatsApp text message...")

                payload = {
                    "from_": self.from_number,
                    "to": self.to_number,
                    "body": message,
                }

            response = self.client.messages.create(**payload)

            logger.info(f"Message sent successfully. SID: {response.sid}")
            return True

        except TwilioRestException as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            return False

        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp message: {e}")
            return False

    def send_file(self, file_path: str, caption: str | None = None) -> bool:
        """
        Send a file via WhatsApp using a caption and media_url.
        """

        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"File not found: {file_path}")
                return False

            logger.warning(
                "Twilio requires a PUBLIC URL for media. "
                "Local paths cannot be sent directly."
            )

            message_params = {
                "from_": self.from_number,
                "to": self.to_number,
                "body": caption or "📎 File attached:",
            }

            response = self.client.messages.create(**message_params)

            logger.info(f"File notification sent. SID: {response.sid}")
            return True

        except Exception as e:
            logger.error(f"Unexpected error sending file: {e}")
            return False


def send_whatsapp_message(text: str):
    """Convenience wrapper"""
    sender = WhatsAppSender()
    return sender.send_message(message=text)


def send_whatsapp_template(content_sid: str, variables: dict):
    """Wrapper for template message"""
    sender = WhatsAppSender()
    return sender.send_message(content_sid=content_sid, content_variables=variables)


# Test message
send_whatsapp_message("WhatsApp sender service is up and running.")
