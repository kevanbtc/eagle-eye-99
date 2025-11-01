"""
Example: Using Eagle Eye Settings in FastAPI Services

This file shows how to use the centralized settings across all services.
"""

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import logging
from pathlib import Path
import sys

# Add config to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import get_settings, Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context for app startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup and shutdown events"""
    settings = get_settings()
    logger.info(f"🚀 Starting Eagle Eye API (v{settings.app_version})")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database: {settings.database.url.split('@')[1] if '@' in settings.database.url else '***'}")
    
    # Startup
    yield
    
    # Shutdown
    logger.info("Shutting down Eagle Eye API")


# Create FastAPI app
app = FastAPI(
    title="Eagle Eye API",
    description="Construction Plan Review & Pricing System",
    lifespan=lifespan
)


# Dependency: Inject settings into routes
async def get_app_settings() -> Settings:
    """FastAPI dependency for accessing settings in route handlers"""
    return get_settings()


# EXAMPLE 1: Access settings in route handler
@app.get("/health")
async def health_check(settings: Settings = Depends(get_app_settings)):
    """Health check endpoint that uses settings"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


# EXAMPLE 2: OpenAI integration with settings
@app.post("/ai/analyze")
async def analyze_plan(text: str, settings: Settings = Depends(get_app_settings)):
    """Example endpoint using OpenAI settings"""
    
    if not settings.openai.api_key:
        return {"error": "OpenAI API key not configured"}
    
    try:
        import openai
        openai.api_key = settings.openai.api_key
        
        response = openai.ChatCompletion.create(
            model=settings.openai.model,
            messages=[{"role": "user", "content": text}],
            temperature=settings.openai.temperature,
            max_tokens=settings.openai.max_tokens,
        )
        
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}


# EXAMPLE 3: Database connection with settings
@app.get("/db/status")
async def database_status(settings: Settings = Depends(get_app_settings)):
    """Example showing database settings usage"""
    
    db_url = settings.database.url
    # Hide credentials in response
    sanitized_url = db_url.replace(
        db_url.split("://")[1].split("@")[0],
        "***"
    ) if "@" in db_url else db_url
    
    return {
        "database": sanitized_url,
        "pool_size": settings.database.pool_size,
        "max_overflow": settings.database.max_overflow,
        "echo": settings.database.echo
    }


# EXAMPLE 4: S3 storage initialization
@app.get("/storage/info")
async def storage_info(settings: Settings = Depends(get_app_settings)):
    """Show storage configuration (without secrets)"""
    return {
        "endpoint": settings.storage.endpoint,
        "bucket": settings.storage.bucket,
        "region": settings.storage.region,
        "ssl": settings.storage.use_ssl
    }


# EXAMPLE 5: Redis cache setup
from redis.asyncio import Redis

_redis_client = None

async def get_redis(settings: Settings = Depends(get_app_settings)) -> Redis:
    """Dependency: Get Redis client initialized with settings"""
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(settings.cache.url, decode_responses=True)
    return _redis_client


@app.get("/cache/ping")
async def cache_ping(redis: Redis = Depends(get_redis)):
    """Test Redis connection"""
    try:
        pong = await redis.ping()
        return {"redis": "connected", "pong": pong}
    except Exception as e:
        return {"error": str(e)}


# EXAMPLE 6: Using settings in async initialization
async def initialize_services(settings: Settings):
    """Initialize all external services based on settings"""
    
    # Initialize database
    logger.info(f"Initializing database: {settings.database.url}")
    
    # Initialize S3
    logger.info(f"Initializing S3 storage: {settings.storage.endpoint}")
    
    # Initialize OpenAI
    if settings.openai.api_key:
        logger.info("OpenAI API configured")
    else:
        logger.warning("OpenAI API key not configured")
    
    # Initialize Ollama if enabled
    if settings.ollama.enabled:
        logger.info(f"Ollama enabled: {settings.ollama.model}")
    
    # Initialize n8n webhooks if enabled
    if settings.n8n.enabled:
        logger.info(f"n8n orchestration enabled: {settings.n8n.api_url}")


# EXAMPLE 7: Configuration endpoint (for debugging, hides secrets)
@app.get("/config/status")
async def config_status(settings: Settings = Depends(get_app_settings)):
    """Show current configuration status (secrets masked)"""
    from config.settings import get_settings_dict
    return get_settings_dict()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.api.host,
        port=settings.api.port,
        debug=settings.api.debug
    )
