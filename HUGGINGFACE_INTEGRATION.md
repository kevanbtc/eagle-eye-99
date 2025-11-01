# Hugging Face Integration Guide

## Quick Setup

### 1. Get Your Hugging Face API Token

1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it (e.g., "Eagle Eye")
4. Choose "Read" scope (for inference)
5. Copy the token (starts with `hf_...`)

### 2. Add to `.env.local`

```bash
HUGGINGFACE_ENABLED=true
HUGGINGFACE_API_KEY=hf_YOUR_TOKEN_HERE
HUGGINGFACE_MODEL=gpt2
HUGGINGFACE_TASK=text-generation
```

### 3. Verify Configuration

```powershell
python verify_config.py
# Should show: ✓ All checks passed!
```

---

## Using in Your Code

### Python Example

```python
from config.settings import get_settings

settings = get_settings()

if settings.huggingface.enabled:
    api_key = settings.huggingface.api_key
    model = settings.huggingface.model
    
    # Use with Hugging Face transformers library
    from transformers import pipeline
    
    classifier = pipeline("sentiment-analysis", model=model)
    result = classifier("I love Eagle Eye!")
    print(result)
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from config.settings import Settings, get_settings

app = FastAPI()

@app.get("/ai/hf-status")
async def hf_status(settings: Settings = Depends(get_settings)):
    return {
        "huggingface_enabled": settings.huggingface.enabled,
        "model": settings.huggingface.model,
        "task": settings.huggingface.task,
        "configured": bool(settings.huggingface.api_key)
    }

@app.post("/ai/analyze-text")
async def analyze_text(
    text: str,
    settings: Settings = Depends(get_settings)
):
    if not settings.huggingface.enabled:
        return {"error": "Hugging Face not enabled"}
    
    from transformers import pipeline
    
    classifier = pipeline(
        settings.huggingface.task,
        model=settings.huggingface.model,
        token=settings.huggingface.api_key
    )
    
    result = classifier(text)
    return {"result": result}
```

---

## Available Models

### For Text Generation
- `gpt2` - GPT-2 small model
- `distilgpt2` - Smaller, faster version
- `meta-llama/Llama-2-7b` - Llama 2 (requires approval)
- `bigcode/starcoder` - Code generation
- See more: https://huggingface.co/models?task=text-generation

### For Classification
- `distilbert-base-uncased-finetuned-sst-2-english` - Sentiment analysis
- `bert-base-multilingual-uncased` - Multi-language
- See more: https://huggingface.co/models?task=text-classification

### For Question Answering
- `distilbert-base-cased-distilled-squad` - QA model
- See more: https://huggingface.co/models?task=question-answering

### For Named Entity Recognition
- `dbmdz/bert-large-cased-finetuned-conll03-english` - NER
- See more: https://huggingface.co/models?task=token-classification

---

## Configuration Options

### Settings Fields

```python
settings.huggingface.enabled       # bool - Enable/disable
settings.huggingface.api_key       # str - API token (hf_...)
settings.huggingface.model         # str - Model name
settings.huggingface.task          # str - Task type
```

### Available Tasks

- `text-generation` - Generate text
- `text-classification` - Classify text
- `token-classification` - Name entity recognition
- `question-answering` - Q&A
- `summarization` - Summarize text
- `translation` - Translate text
- `sentiment-analysis` - Sentiment analysis
- See all: https://huggingface.co/tasks

---

## Production Deployment

### GitHub Actions

Add to `.github/workflows/deploy.yml`:

```yaml
env:
  HUGGINGFACE_API_KEY: ${{ secrets.HUGGINGFACE_API_KEY }}
  HUGGINGFACE_MODEL: gpt2
  HUGGINGFACE_ENABLED: true
```

### Docker

```dockerfile
FROM python:3.11
ENV HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
ENV HUGGINGFACE_ENABLED=true
COPY requirements.txt .
RUN pip install -r requirements.txt
```

### Azure Key Vault

```csharp
// For .NET services
var kvUri = new Uri("https://my-vault.vault.azure.net/");
var credential = new DefaultAzureCredential();
var client = new SecretClient(kvUri, credential);

var huggingfaceKey = client.GetSecret("huggingface-api-key");
```

---

## Common Issues

### Issue: "API token is invalid"
- **Solution:** Make sure token starts with `hf_`
- **Check:** Copy token from https://huggingface.co/settings/tokens
- **Test:** Run `python verify_config.py`

### Issue: "Model not found"
- **Solution:** Check model name on https://huggingface.co/models
- **Example:** Use `gpt2` not `GPT-2` or `gpt2-medium`
- **Test:** Try downloading model: `python -c "from transformers import AutoModel; AutoModel.from_pretrained('gpt2')"`

### Issue: "Authentication required"
- **Solution:** Some models require approval on Hugging Face
- **Fix:** Go to model page, click "Request Access"
- **Wait:** Approval can take hours or days
- **Alternative:** Use public models that don't require approval

### Issue: "Rate limit exceeded"
- **Solution:** Hugging Face has rate limits on free tier
- **Fix:** Upgrade to Pro: https://huggingface.co/pricing
- **Alternative:** Use smaller models (distilgpt2, distilbert, etc.)

### Issue: "Out of memory"
- **Solution:** Large models require lots of memory
- **Fix:** Use smaller models (distil-* variants)
- **Example:** Use `distilgpt2` instead of `gpt2-large`

---

## Troubleshooting

### Check Configuration
```powershell
python verify_config.py
```

### Test API Connection
```python
from config.settings import get_settings
settings = get_settings()
print(f"Hugging Face enabled: {settings.huggingface.enabled}")
print(f"API key set: {bool(settings.huggingface.api_key)}")
print(f"Model: {settings.huggingface.model}")
```

### Test Model Loading
```python
from transformers import AutoModel

model_name = "gpt2"
try:
    model = AutoModel.from_pretrained(model_name)
    print(f"✓ Model '{model_name}' loaded successfully")
except Exception as e:
    print(f"✗ Failed to load model: {e}")
```

### Test Pipeline
```python
from transformers import pipeline
from config.settings import get_settings

settings = get_settings()

try:
    pipe = pipeline(
        settings.huggingface.task,
        model=settings.huggingface.model,
        token=settings.huggingface.api_key
    )
    result = pipe("test text")
    print(f"✓ Pipeline works: {result}")
except Exception as e:
    print(f"✗ Pipeline failed: {e}")
```

---

## Dependencies

### Install Transformers

```bash
pip install transformers torch
```

### Full Requirements

```bash
# Core
transformers==4.34.0
torch==2.0.1
huggingface-hub==0.17.3

# Optional (for specific models)
sentencepiece              # For some models
protobuf                   # For some models
tokenizers                 # Fast tokenizers
accelerate                 # GPU support
```

### Update `services/api/requirements.txt`

```txt
# Existing
fastapi
uvicorn
pydantic
pydantic-settings
python-dotenv

# Add these for Hugging Face
transformers>=4.34.0
torch>=2.0.1
huggingface-hub>=0.17.3
```

---

## Security Best Practices

✅ **DO:**
- Keep API token in `.env.local` (git-ignored)
- Use tokens with "Read" scope only
- Rotate tokens annually
- Don't share tokens in chat/email
- Use environment variables in production

❌ **DON'T:**
- Commit `.env.local` with token
- Paste token in code
- Share token across projects
- Use old/test tokens
- Log token values

---

## Performance Tips

### 1. Use Smaller Models
```python
# Fast & lightweight
model = "distilgpt2"              # 82M parameters
model = "distilbert-base"         # 66M parameters
model = "tiny-random-GPTModel"    # 124K parameters (demo)

# Slower but powerful
model = "gpt2-medium"             # 355M parameters
model = "gpt2-large"              # 774M parameters
```

### 2. Cache Models
```python
from transformers import pipeline

# Models are downloaded once and cached
pipe = pipeline("text-generation", model="gpt2")
# Second time will load from cache instantly
```

### 3. Batch Processing
```python
from transformers import pipeline

pipe = pipeline("sentiment-analysis")

# Better than looping with single inputs
texts = ["text1", "text2", "text3"]
results = pipe(texts)
```

### 4. Use GPU
```python
import torch
from transformers import pipeline

device = 0 if torch.cuda.is_available() else -1
pipe = pipeline("text-generation", model="gpt2", device=device)
```

---

## Resources

- **Hugging Face Hub:** https://huggingface.co/
- **Models:** https://huggingface.co/models
- **Transformers Docs:** https://huggingface.co/docs/transformers
- **API Tokens:** https://huggingface.co/settings/tokens
- **Model Cards:** https://huggingface.co/model-hub

---

## Next Steps

1. Get API token from Hugging Face
2. Add to `.env.local` (HUGGINGFACE_API_KEY)
3. Choose a model from https://huggingface.co/models
4. Update `.env.local` with model name
5. Run `python verify_config.py`
6. Test with example code above

---

**Questions?** See the main secrets documentation or the Eagle Eye README.
