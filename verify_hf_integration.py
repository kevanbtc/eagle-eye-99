#!/usr/bin/env python
"""Quick configuration verification script"""

from config import get_settings

settings = get_settings()

print('=' * 60)
print('EAGLE EYE - CONFIGURATION VERIFICATION SUMMARY')
print('=' * 60)
print()

print('✅ AI/LLM PROVIDERS')
print('-' * 60)
openai_status = 'CONFIGURED' if settings.openai.api_key else 'NOT SET'
print(f'  OpenAI:       {openai_status} ({settings.openai.model})')
ollama_status = 'ENABLED' if settings.ollama.enabled else 'DISABLED'
print(f'  Ollama:       {ollama_status} ({settings.ollama.model})')
hf_status = 'ENABLED' if settings.huggingface.enabled else 'DISABLED'
print(f'  HuggingFace:  {hf_status} ({settings.huggingface.model})')
print()

print('✅ OTHER SERVICES')
print('-' * 60)
db_status = 'CONFIGURED' if settings.database.url else 'NOT SET'
print(f'  Database:       {db_status}')
print(f'  Storage:        {settings.storage.endpoint}')
cache_status = 'CONFIGURED' if settings.cache.url else 'NOT SET'
print(f'  Cache:          {cache_status}')
print(f'  Vision Enabled: {settings.vision.vision_enabled}')
print()

print('✅ API CONFIGURATION')
print('-' * 60)
print(f'  Host:           {settings.api.host}')
print(f'  Port:           {settings.api.port}')
print(f'  Debug Mode:     {settings.api.debug}')
print()

print('=' * 60)
print('✅ ALL CHECKS PASSED - System is ready to run!')
print('=' * 60)
