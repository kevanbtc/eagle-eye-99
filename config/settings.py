"""
Eagle Eye Configuration Settings
Centralized configuration management for all services
Supports: environment variables, .env files, and .env.local (git-ignored)
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from pathlib import Path
import os
from dotenv import load_dotenv

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent

# Load .env.local first (highest priority), then .env
env_local = PROJECT_ROOT / ".env.local"
env_file = PROJECT_ROOT / ".env"

if env_local.exists():
    load_dotenv(env_local, override=True)
elif env_file.exists():
    load_dotenv(env_file)


class DatabaseSettings(BaseModel):
    """Database configuration"""
    model_config = ConfigDict(populate_by_name=True)
    url: str = Field(
        default="postgresql+psycopg://eagle:eagle@localhost:5432/eagle",
        validation_alias="DATABASE_URL"
    )
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


class StorageSettings(BaseModel):
    """S3/MinIO storage configuration"""
    model_config = ConfigDict(populate_by_name=True)
    endpoint: str = Field(
        default="http://localhost:9000",
        validation_alias="S3_ENDPOINT"
    )
    access_key: str = Field(
        default="minio",
        validation_alias="S3_ACCESS_KEY"
    )
    secret_key: str = Field(
        default="minio123",
        validation_alias="S3_SECRET_KEY"
    )
    bucket: str = Field(
        default="eagle-files",
        validation_alias="S3_BUCKET"
    )
    region: str = "us-east-1"
    use_ssl: bool = False

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("S3_ENDPOINT must start with http:// or https://")
        return v


class CacheSettings(BaseModel):
    """Redis cache configuration"""
    model_config = ConfigDict(populate_by_name=True)
    url: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="REDIS_URL"
    )
    ttl_seconds: int = 3600  # 1 hour default


class OpenAISettings(BaseModel):
    """OpenAI API configuration"""
    model_config = ConfigDict(populate_by_name=True)
    api_key: Optional[str] = Field(
        default=None,
        validation_alias="OPENAI_API_KEY"
    )
    model: str = Field(
        default="gpt-4-turbo-preview",
        validation_alias="OPENAI_MODEL"
    )
    temperature: float = 0.7
    max_tokens: int = 4096

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v):
        if v and not v.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
        return v


class OllamaSettings(BaseModel):
    """Ollama local LLM configuration"""
    model_config = ConfigDict(populate_by_name=True)
    base_url: str = Field(
        default="http://localhost:11434",
        validation_alias="OLLAMA_BASE_URL"
    )
    model: str = Field(
        default="llama2",
        validation_alias="OLLAMA_MODEL"
    )
    api_token: Optional[str] = Field(
        default=None,
        validation_alias="OLLAMA_API_TOKEN"
    )
    enabled: bool = Field(
        default=False,
        validation_alias="OLLAMA_ENABLED"
    )


class HuggingFaceSettings(BaseModel):
    """Hugging Face API configuration"""
    model_config = ConfigDict(populate_by_name=True)

    api_key: Optional[str] = Field(
        default=None,
        validation_alias="HUGGINGFACE_API_KEY"
    )
    model: str = Field(
        default="gpt2",
        validation_alias="HUGGINGFACE_MODEL"
    )
    task: str = Field(
        default="text-generation",
        validation_alias="HUGGINGFACE_TASK"
    )
    enabled: bool = Field(
        default=False,
        validation_alias="HUGGINGFACE_ENABLED"
    )

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v):
        if v and not v.startswith("hf_"):
            raise ValueError("Invalid Hugging Face API key format (must start with 'hf_')")
        return v


class VisionSettings(BaseModel):
    """Vision/Image processing configuration"""
    model_config = ConfigDict(populate_by_name=True)
    vision_enabled: bool = Field(
        default=False,
        validation_alias="VISION_ENABLED"
    )
    sam_model: str = Field(
        default="sam_vit_h",
        validation_alias="SAM_MODEL"
    )
    grounding_dino_model: str = Field(
        default="groundingdino_swinb_cogcoor",
        validation_alias="GROUNDING_DINO_MODEL"
    )


class JurisdictionSettings(BaseModel):
    """Jurisdiction and code standards configuration"""
    model_config = ConfigDict(populate_by_name=True)
    default_state: str = Field(
        default="GA",
        validation_alias="DEFAULT_STATE"
    )
    code_set: str = Field(
        default="IRC2018_IECC2015_NEC2017_GA",
        validation_alias="CODE_SET"
    )
    supported_states: List[str] = ["GA", "CA", "TX", "NY", "FL"]


class APISettings(BaseModel):
    """API server configuration"""
    model_config = ConfigDict(populate_by_name=True)
    host: str = Field(
        default="0.0.0.0",
        validation_alias="API_HOST"
    )
    port: int = Field(
        default=8000,
        validation_alias="API_PORT"
    )
    debug: bool = Field(
        default=False,
        validation_alias="DEBUG"
    )
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5678",
        "http://localhost:8000"
    ]


class N8NSettings(BaseModel):
    """n8n workflow orchestration configuration"""
    model_config = ConfigDict(populate_by_name=True)
    webhook_url: str = Field(
        default="http://localhost:5678/webhook",
        validation_alias="N8N_WEBHOOK_URL"
    )
    api_url: str = Field(
        default="http://localhost:5678/api",
        validation_alias="N8N_API_URL"
    )
    api_key: Optional[str] = Field(
        default=None,
        validation_alias="N8N_API_KEY"
    )
    enabled: bool = Field(
        default=True,
        validation_alias="N8N_ENABLED"
    )


class LoggingSettings(BaseModel):
    """Logging configuration"""
    model_config = ConfigDict(populate_by_name=True)
    level: str = Field(
        default="INFO",
        validation_alias="LOG_LEVEL"
    )
    format: str = "json"  # json or text
    seq_enabled: bool = Field(
        default=False,
        validation_alias="SEQ_ENABLED"
    )
    seq_url: str = Field(
        default="http://localhost:5341",
        validation_alias="SEQ_URL"
    )


class Settings(BaseModel):
    """Main settings object - aggregates all subsettings"""
    model_config = ConfigDict(populate_by_name=True)
    app_name: str = "Eagle Eye"
    app_version: str = "0.1.0"
    environment: str = Field(
        default="development",
        validation_alias="ENVIRONMENT"
    )

    # Subsettings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    ollama: OllamaSettings = Field(default_factory=OllamaSettings)
    huggingface: HuggingFaceSettings = Field(default_factory=HuggingFaceSettings)
    vision: VisionSettings = Field(default_factory=VisionSettings)
    jurisdiction: JurisdictionSettings = Field(default_factory=JurisdictionSettings)
    api: APISettings = Field(default_factory=APISettings)
    n8n: N8NSettings = Field(default_factory=N8NSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v):
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v


# Singleton instance
_settings = None


def get_settings() -> Settings:
    """Get or create settings singleton"""
    global _settings
    if _settings is None:
        # Pass environment variables directly
        _settings = Settings(
            database=DatabaseSettings(
                url=os.getenv("DATABASE_URL", "postgresql+psycopg://eagle:eagle@localhost:5432/eagle")
            ),
            storage=StorageSettings(
                endpoint=os.getenv("S3_ENDPOINT", "http://localhost:9000"),
                access_key=os.getenv("S3_ACCESS_KEY", "minio"),
                secret_key=os.getenv("S3_SECRET_KEY", "minio123"),
                bucket=os.getenv("S3_BUCKET", "eagle-files"),
            ),
            cache=CacheSettings(
                url=os.getenv("REDIS_URL", "redis://localhost:6379/0")
            ),
            openai=OpenAISettings(
                api_key=os.getenv("OPENAI_API_KEY"),
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            ),
            ollama=OllamaSettings(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                model=os.getenv("OLLAMA_MODEL", "llama2"),
                api_token=os.getenv("OLLAMA_API_TOKEN"),
                enabled=os.getenv("OLLAMA_ENABLED", "false").lower() == "true",
            ),
            huggingface=HuggingFaceSettings(
                api_key=os.getenv("HUGGINGFACE_API_KEY"),
                model=os.getenv("HUGGINGFACE_MODEL", "gpt2"),
                task=os.getenv("HUGGINGFACE_TASK", "text-generation"),
                enabled=os.getenv("HUGGINGFACE_ENABLED", "false").lower() == "true",
            ),
            vision=VisionSettings(
                vision_enabled=os.getenv("VISION_ENABLED", "false").lower() == "true",
                sam_model=os.getenv("SAM_MODEL", "sam_vit_h"),
                grounding_dino_model=os.getenv("GROUNDING_DINO_MODEL", "groundingdino_swinb_cogcoor"),
            ),
            jurisdiction=JurisdictionSettings(
                default_state=os.getenv("DEFAULT_STATE", "GA"),
                code_set=os.getenv("CODE_SET", "IRC2018_IECC2015_NEC2017_GA"),
            ),
            api=APISettings(
                host=os.getenv("API_HOST", "0.0.0.0"),
                port=int(os.getenv("API_PORT", "8000")),
                debug=os.getenv("DEBUG", "false").lower() == "true",
            ),
            n8n=N8NSettings(
                webhook_url=os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook"),
                api_url=os.getenv("N8N_API_URL", "http://localhost:5678/api"),
                api_key=os.getenv("N8N_API_KEY"),
                enabled=os.getenv("N8N_ENABLED", "true").lower() == "true",
            ),
            logging=LoggingSettings(
                level=os.getenv("LOG_LEVEL", "INFO"),
                format=os.getenv("LOG_FORMAT", "json"),
                seq_enabled=os.getenv("SEQ_ENABLED", "false").lower() == "true",
                seq_url=os.getenv("SEQ_URL", "http://localhost:5341"),
            ),
        )
    return _settings


# Convenience accessors
def get_settings_dict() -> dict:
    """Get settings as dictionary (for debugging, excludes secrets)"""
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "environment": settings.environment,
        "database_url": "***" if settings.database.url else None,
        "storage_endpoint": settings.storage.endpoint,
        "cache_url": "***" if settings.cache.url else None,
        "openai_configured": bool(settings.openai.api_key),
        "ollama_enabled": settings.ollama.enabled,
        "vision_enabled": settings.vision.vision_enabled,
        "api_port": settings.api.port,
    }
