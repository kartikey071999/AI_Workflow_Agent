"""
Config module - handles all application settings and initialization.
Import settings from here: from config import settings
"""

from .settings import Settings

# Singleton-style global settings
settings = Settings()
settings.create_directories()

__all__ = ["settings"]
