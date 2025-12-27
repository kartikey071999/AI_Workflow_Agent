import re
from urllib.parse import urlparse

from src.config import settings
from src.senders import TelegramClient
from src.services.collect_ai_news import PerplexityClient


def format_update_for_telegram(topic: str, response: str, citations: list[str]) -> str:
    lines = response.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove citation markers like [1][4][5]
        line = re.sub(r"\[\d+\]", "", line)

        # Ensure line ends with a full stop
        if not line.endswith("."):
            line += "."

        cleaned_lines.append(line)

    # Format citations nicely
    formatted_sources = []
    for i, url in enumerate(citations, start=1):
        domain = urlparse(url).netloc.replace("www.", "")
        formatted_sources.append(f"{i}. {domain}")

    message = (
        f"**📰 Daily Update on {topic}**\n\n"
        + "\n\n".join(cleaned_lines)
        + "\n\n📚 **Sources:**\n"
        + "\n".join(formatted_sources)
    )

    return message


def get_topics():
    # Use topics from settings (config module)
    return settings.topics


if __name__ == "__main__":
    import sys

    client = PerplexityClient()
    topics = get_topics()

    telegram_client = TelegramClient()
    errors = []
    for topic in topics:
        try:
            update = client.get_update(topic)
            msg = format_update_for_telegram(
                topic, update["response"], update["citations"]
            )
            telegram_client.send(msg)
        except Exception as e:
            error_msg = f"::error title=Failed for topic::{topic} error={e}"
            print(error_msg)
            errors.append(error_msg)
            continue
    if errors:
        print("::group::Summary of failures")
        for err in errors:
            print(err)
        print("::endgroup::")
        sys.exit(1)
