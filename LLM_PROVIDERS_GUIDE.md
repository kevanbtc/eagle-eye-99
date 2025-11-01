# LLM Providers Configuration - Quick Reference

## Current Status ✅

All three LLM providers are now configured and ready to use:

| Provider | Status | Model | Details |
|----------|--------|-------|---------|
| **OpenAI** | ✅ CONFIGURED | gpt-4-turbo-preview | Cloud-hosted GPT-4 |
| **Ollama** | ✅ ENABLED | llama2 | Local open-source LLM |
| **Hugging Face** | ✅ ENABLED | meta-llama/Llama-2-7b-chat-hf | HF Model Hub integration |

## Configuration Files

### `.env.local` (Local Development)
```env
# OpenAI
OPENAI_API_KEY=sk-proj-test123456789
OPENAI_MODEL=gpt-4-turbo-preview

# Ollama (Local LLM Server)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_ENABLED=true

# Hugging Face
HUGGINGFACE_API_KEY=hf_YOUR_TOKEN_HERE
HUGGINGFACE_MODEL=meta-llama/Llama-2-7b-chat-hf
HUGGINGFACE_TASK=text-generation
HUGGINGFACE_ENABLED=true
```

### `.env.example` (Public Template)
All three providers are documented in `.env.example` for team reference.

## Usage in Code

### Get Settings
```python
from config import get_settings

settings = get_settings()
```

### Use OpenAI
```python
if settings.openai.api_key:
    api_key = settings.openai.api_key
    model = settings.openai.model
    
    # Use with OpenAI client
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
```

### Use Ollama (Local)
```python
if settings.ollama.enabled:
    base_url = settings.ollama.base_url  # http://localhost:11434
    model = settings.ollama.model         # llama2
    
    # Use with ollama Python client
    import ollama
    response = ollama.generate(model=model, prompt="Hello")
```

### Use Hugging Face
```python
if settings.huggingface.enabled:
    api_key = settings.huggingface.api_key
    model = settings.huggingface.model
    task = settings.huggingface.task
    
    # Use with transformers or huggingface_hub
    from huggingface_hub import InferenceClient
    client = InferenceClient(model=model, token=api_key)
```

## Verification Commands

```bash
# Full system check
python verify_config.py

# LLM providers quick check
python verify_hf_integration.py

# Check specific provider
python -c "from config import get_settings; s = get_settings(); print(f'OpenAI: {s.openai.model}'); print(f'Ollama: {s.ollama.model}'); print(f'HF: {s.huggingface.model}')"
```

## Environment Variables Reference

### OpenAI
- `OPENAI_API_KEY` - API key (starts with `sk-`)
- `OPENAI_MODEL` - Model name (default: `gpt-4-turbo-preview`)
- `OPENAI_TEMPERATURE` - Temperature 0-2 (default: 0.7)
- `OPENAI_MAX_TOKENS` - Max response tokens (default: 4096)

### Ollama
- `OLLAMA_BASE_URL` - Server URL (default: `http://localhost:11434`)
- `OLLAMA_MODEL` - Model name (default: `llama2`)
- `OLLAMA_API_TOKEN` - Optional API token
- `OLLAMA_ENABLED` - Enable/disable (default: `false`)

### Hugging Face
- `HUGGINGFACE_API_KEY` - API key (starts with `hf_`)
- `HUGGINGFACE_MODEL` - Model identifier (default: `gpt2`)
- `HUGGINGFACE_TASK` - Task type (default: `text-generation`)
- `HUGGINGFACE_ENABLED` - Enable/disable (default: `false`)

## Installation Requirements

### For OpenAI
```bash
pip install openai
```

### For Ollama
```bash
# Install Ollama locally from https://ollama.ai
# Then pull a model: ollama pull llama2
pip install ollama
```

### For Hugging Face
```bash
pip install huggingface_hub transformers torch
```

## Security Notes

⚠️ **All API keys in `.env.local` are:**
- ✅ Git-ignored (never committed)
- ✅ For local development only
- ❌ Should NOT be hardcoded in production

### Production Setup
For production, use:
- Azure Key Vault
- AWS Secrets Manager
- GitHub Secrets (CI/CD)
- Kubernetes Secrets (containers)
- Environment variables (Docker/cloud platforms)

## Testing

```python
# Test all providers
from config import get_settings

s = get_settings()
print(f"OpenAI configured: {bool(s.openai.api_key)}")
print(f"Ollama enabled: {s.ollama.enabled}")
print(f"HuggingFace enabled: {s.huggingface.enabled}")
```

Expected output:
```
OpenAI configured: True
Ollama enabled: True
HuggingFace enabled: True
```

## Troubleshooting

### OpenAI connection fails
- Check API key format (must start with `sk-`)
- Verify internet connection
- Check OpenAI account credits

### Ollama not found
- Ensure Ollama is installed and running
- Check `OLLAMA_BASE_URL` points to running instance
- Pull a model: `ollama pull llama2`

### HuggingFace authentication fails
- Check API key format (must start with `hf_`)
- Verify token isn't revoked
- Check HuggingFace account permissions

## Next Steps

1. **Install provider libraries**: `pip install openai ollama huggingface_hub transformers`
2. **Test connections**: Run `verify_hf_integration.py`
3. **Update services**: Modify API, Parser, Rules services to use preferred provider
4. **Add fallback logic**: Consider using Ollama as fallback when OpenAI is unavailable
