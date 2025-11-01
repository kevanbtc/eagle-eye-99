# Eagle Eye Secrets & Configuration Management Guide

## Overview

This guide explains how to safely manage secrets and configuration for the Eagle Eye project across all services.

**Key Principle**: Sensitive data (API keys, database passwords) should NEVER be committed to Git.

---

## Quick Start (5 minutes)

### Step 1: Copy the Template
```powershell
# From the project root directory
Copy-Item .env.example .env.local
```

### Step 2: Edit with Your Values
```powershell
# Open in your editor
code .env.local
```

Add your real API keys:
```bash
OPENAI_API_KEY=sk-proj-YOUR_KEY_FROM_OPENAI
DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/eagle
# ... other values
```

### Step 3: Verify .gitignore
Ensure `.env.local` is in `.gitignore`:
```bash
# ✅ Should see this line:
cat .gitignore | grep ".env.local"
```

### Step 4: Use in Your Service

**For Python (FastAPI):**
```python
from config.settings import get_settings

settings = get_settings()
api_key = settings.openai.api_key
db_url = settings.database.url
```

**For .NET (C#):**
```csharp
var settings = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddUserSecrets<Program>()
    .AddEnvironmentVariables()
    .Build();

var openaiKey = settings["OpenAI:ApiKey"];
```

---

## File Structure

```
eagle-eye-2/
├── .env.example          ← Public template (commit to Git)
├── .env.local            ← YOUR local secrets (git-ignored, NEVER commit)
├── .env.local.template   ← Reference/backup template
├── .gitignore            ← Must include .env.local
└── config/
    └── settings.py       ← Centralized settings (pydantic)
```

### .env.example
- **Committed to Git** ✅
- Shows structure and defaults
- Contains placeholder values
- **Does NOT contain real secrets** ✅

### .env.local
- **Git-ignored** ✅
- Contains your actual API keys
- Created locally by each developer
- **NEVER commit this file** ⚠️

---

## Configuration by Environment

### Development (Local Machine)

1. **Create .env.local:**
```bash
cp .env.example .env.local
```

2. **Fill in local values:**
```bash
ENVIRONMENT=development
DEBUG=true
OPENAI_API_KEY=sk-proj-YOUR_DEV_KEY
DATABASE_URL=postgresql+psycopg://eagle:eagle@localhost:5432/eagle
```

3. **Run services:**
```bash
# Services auto-load .env.local
cd services/api && python main.py
```

### Staging/Production

**Do NOT use .env.local in production!** ⚠️

Instead, use:

#### Option A: Azure Key Vault (Recommended for .NET)
```csharp
var keyVaultUrl = new Uri("https://my-vault.vault.azure.net/");
var credential = new DefaultAzureCredential();
var client = new SecretClient(keyVaultUrl, credential);
builder.Configuration.AddAzureKeyVault(client);
```

#### Option B: GitHub Secrets (For CI/CD)
```yaml
# .github/workflows/deploy.yml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

#### Option C: Environment Variables (Docker/K8s)
```dockerfile
# Dockerfile
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV DATABASE_URL=${DATABASE_URL}
```

#### Option D: Managed Secrets (Python)
```python
# Use python-dotenv only in development
from dotenv import load_dotenv
import os

# Only loads .env.local in development
if os.getenv("ENVIRONMENT") == "development":
    load_dotenv(".env.local")
```

---

## Security Best Practices

### ✅ DO

- ✅ Store secrets in .env.local (local dev only)
- ✅ Use Azure Key Vault for production
- ✅ Rotate API keys every 90 days
- ✅ Use strong database passwords (20+ chars)
- ✅ Check .gitignore includes .env.local
- ✅ Use different keys for dev/prod
- ✅ Log configuration on startup (with secrets masked)

### ❌ DON'T

- ❌ Commit .env.local to Git
- ❌ Paste API keys in chat/Slack/email
- ❌ Share .env.local files
- ❌ Use same API key for dev and prod
- ❌ Leave secrets in commit messages (even deleted)
- ❌ Log actual secret values
- ❌ Store secrets in comments

---

## Checking for Leaked Secrets

### Before Committing

```bash
# Scan for common patterns
git diff HEAD | grep -E "(sk-|password|secret|key)" | grep -v ".env.example"

# Check staged files
git diff --cached | grep -iE "api.key|password|secret"
```

### If You Accidentally Committed a Secret

**IMMEDIATELY:**

1. **Create new API key** (old one is compromised)
2. **Rotate in the service** (OpenAI, etc.)
3. **Check git history:**
```bash
# Find commits containing the key
git log -S "sk-proj-" --all --source -- '*.py' '*.env'

# Rewrite history (careful operation)
git filter-branch --tree-filter 'grep -r "sk-proj-" | cut -d: -f1 | xargs sed -i "s/sk-proj-[^ ]*/***/g"' -- --all
```

4. **Force push if absolutely necessary** (only for small teams):
```bash
git push origin --force-with-lease
```

---

## Python Services Setup

### Install pydantic-settings
```bash
pip install pydantic-settings python-dotenv
```

### Using Settings in Your Service

```python
# services/api/main.py
from fastapi import FastAPI, Depends
from config.settings import get_settings, Settings

app = FastAPI()

# Route-level dependency injection
@app.get("/api/status")
async def status(settings: Settings = Depends(get_settings)):
    return {
        "openai_configured": bool(settings.openai.api_key),
        "db": settings.database.url.split('@')[1] if '@' in settings.database.url else "***"
    }

# Initialize with settings
if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(app, host=settings.api.host, port=settings.api.port)
```

---

## C# / .NET Services Setup

### Using User Secrets (Development)

```bash
# Initialize secrets store
dotnet user-secrets init --project src/EagleEye.Api

# Set secrets
dotnet user-secrets set "OpenAI:ApiKey" "sk-proj-YOUR_KEY" --project src/EagleEye.Api
dotnet user-secrets set "Database:ConnectionString" "Server=..." --project src/EagleEye.Api

# List all secrets
dotnet user-secrets list --project src/EagleEye.Api
```

### Using appsettings

```json
// appsettings.Development.json (git-ignored)
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  },
  "OpenAI": {
    "ApiKey": "sk-proj-YOUR_DEV_KEY"
  },
  "Database": {
    "ConnectionString": "Server=localhost;Database=eagle;..."
  }
}
```

### Using Azure Key Vault (Production)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Add Azure Key Vault
var keyVaultEndpoint = new Uri(builder.Configuration["KeyVault:VaultUri"]);
var credential = new DefaultAzureCredential();
builder.Configuration.AddAzureKeyVault(keyVaultEndpoint, credential);

var app = builder.Build();

// Access secrets
var apiKey = app.Configuration["OpenAI--ApiKey"];
```

---

## Docker Compose Setup

### Local Development with Docker

```yaml
# infra/docker-compose.yml
version: '3.8'

services:
  api:
    build: ../services/api
    ports:
      - "8000:8000"
    env_file: ../.env.local  # ← Loads from .env.local
    environment:
      ENVIRONMENT: development
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: eagle
      POSTGRES_PASSWORD: ${DB_PASSWORD:-eagle}  # From .env.local
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Production Deployment

**DO NOT use env_file in production!**

Instead:
```yaml
# Use Docker secrets or orchestration secrets
services:
  api:
    # No env_file!
    environment:
      OPENAI_API_KEY: /run/secrets/openai_key  # Read from secret file
```

---

## Troubleshooting

### Issue: "Configuration key not found"

**Solution:**
```python
# Check if settings are loading
from config.settings import get_settings
settings = get_settings()
print(settings.openai.api_key)  # Should print value or None
```

### Issue: .env.local changes not reflected

**Solution:**
```bash
# Restart the service
# The settings are cached as a singleton
# Kill and restart Python process

# For development:
# - Ctrl+C in terminal
# - Run service again
```

### Issue: "OpenAI API key not configured"

**Solution:**
```bash
# 1. Check .env.local exists
ls -la .env.local

# 2. Verify key is set
cat .env.local | grep OPENAI_API_KEY

# 3. Verify format (should start with sk-proj-)
# If not, get new key from https://platform.openai.com/api-keys
```

### Issue: Git keeps trying to commit .env.local

**Solution:**
```bash
# 1. Verify .gitignore has .env.local
cat .gitignore | grep ".env.local"

# 2. If already committed, remove from tracking
git rm --cached .env.local
git commit -m "Stop tracking .env.local"

# 3. Verify removed
git status
```

---

## Environment Variables Reference

| Variable | Purpose | Example | Required |
|----------|---------|---------|----------|
| `ENVIRONMENT` | App environment | `development` / `production` | ✓ |
| `OPENAI_API_KEY` | OpenAI API access | `sk-proj-...` | For LLM features |
| `DATABASE_URL` | PostgreSQL connection | `postgresql+psycopg://...` | ✓ |
| `S3_ENDPOINT` | MinIO/S3 endpoint | `http://localhost:9000` | ✓ |
| `S3_ACCESS_KEY` | S3 access key | `minio` | ✓ |
| `S3_SECRET_KEY` | S3 secret key | `minio123` | ✓ |
| `REDIS_URL` | Redis cache URL | `redis://localhost:6379/0` | ✓ |
| `OLLAMA_ENABLED` | Enable local LLM | `false` / `true` | Optional |
| `OLLAMA_API_TOKEN` | Ollama auth token | `abc123...` | If Ollama enabled |
| `N8N_API_KEY` | n8n automation key | `n_...` | For workflows |
| `SEQ_ENABLED` | Enable Seq logging | `false` / `true` | Optional |

---

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and paste into .env.local
4. **Keep it secret!**

### n8n API Key
1. Open n8n UI (http://localhost:5678)
2. Go to Settings → API Keys
3. Click "Generate API Key"
4. Add to .env.local

### Azure Key Vault (Production)
1. Go to Azure Portal → Key Vaults
2. Create vault or use existing
3. Add secrets for each environment variable
4. Grant app's managed identity access

---

## Monitoring & Logging

### Check Configuration on Startup

```python
# services/api/main.py
import logging
from config.settings import get_settings_dict

logger = logging.getLogger(__name__)

# Log configuration (with secrets masked)
config = get_settings_dict()
logger.info(f"Configuration loaded: {config}")
# Output: Configuration loaded: {'openai_configured': True, 'database_url': '***', ...}
```

### Detect Missing Secrets

```python
from config.settings import get_settings

settings = get_settings()

required = {
    "openai": settings.openai.api_key,
    "database": settings.database.url,
    "s3": settings.storage.access_key
}

missing = [k for k, v in required.items() if not v]
if missing:
    logger.error(f"Missing required configuration: {missing}")
    raise RuntimeError(f"Missing: {missing}")
```

---

## Summary Checklist

- [ ] Created `.env.local` from `.env.example`
- [ ] Added real API keys to `.env.local`
- [ ] Verified `.env.local` in `.gitignore`
- [ ] Tested settings load successfully (`get_settings()`)
- [ ] Checked git log for accidentally committed secrets
- [ ] Set up backup/recovery plan for keys
- [ ] Documented secrets location for team
- [ ] Set rotation reminder (every 90 days)
- [ ] Tested with actual services

---

**Questions?** See specific service documentation:
- Python services: `services/api/README.md`
- C# services: `EagleEye.NET/README.md`
- Docker setup: `infra/docker-compose.yml`
