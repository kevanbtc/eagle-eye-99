"""
Eagle Eye Configuration Module

Centralized configuration management for all services.

Usage:
    from config.settings import get_settings
    
    settings = get_settings()
    api_key = settings.openai.api_key
    db_url = settings.database.url
"""

from .settings import (
    get_settings,
    get_settings_dict,
    Settings,
    DatabaseSettings,
    StorageSettings,
    CacheSettings,
    OpenAISettings,
    OllamaSettings,
    HuggingFaceSettings,
    VisionSettings,
    JurisdictionSettings,
    APISettings,
    N8NSettings,
    LoggingSettings,
)

__all__ = [
    "get_settings",
    "get_settings_dict",
    "Settings",
    "DatabaseSettings",
    "StorageSettings",
    "CacheSettings",
    "OpenAISettings",
    "OllamaSettings",
    "HuggingFaceSettings",
    "VisionSettings",
    "JurisdictionSettings",
    "APISettings",
    "N8NSettings",
    "LoggingSettings",
]

__version__ = "0.1.0"
