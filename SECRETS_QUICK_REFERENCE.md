# 🔐 Eagle Eye Secrets Management - Visual Quick Reference

## File Map

```
eagle-eye-2/
│
├── 📄 .env.example (COMMIT this)
│   └─ ✅ Public template with all variables
│
├── 📄 .env.local (git-ignored - CREATE THIS)
│   └─ 🔒 Your actual API keys (NEVER commit)
│
├── 🔧 config/
│   ├── settings.py (Centralized config - Pydantic)
│   ├── __init__.py (Clean exports)
│   └── requirements.txt (Dependencies)
│
├── 📚 SECRETS_CONFIGURATION_GUIDE.md ← START HERE!
├── 📚 SECRETS_SETUP_COMPLETE.md
├── 📚 SECRETS_SUMMARY.md (THIS FILE)
├── .github/SECRETS_GITHUB_ACTIONS.md (CI/CD setup)
│
├── 🔍 verify_config.py (Configuration checker)
│
└── services/api/
    └── example_settings_usage.py (Code examples)
```

---

## 🚀 5-Minute Setup

```
1. Copy Template
   $ Copy-Item .env.example .env.local

2. Add Your Keys
   $ code .env.local
   # Edit: OPENAI_API_KEY=sk-proj-YOUR_KEY

3. Verify Setup
   $ python verify_config.py
   ✓ All checks passed!

4. Done! Use It
   from config.settings import get_settings
   settings = get_settings()
   api_key = settings.openai.api_key
```

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  DEVELOPMENT MACHINE                                        │
│  ─────────────────────────────────────────────────────      │
│                                                             │
│  .env.local ──────────────┐                                │
│  (git-ignored)            │                                │
│  sk-proj-YOUR_KEY         │                                │
│  postgresql://            │                                │
│  etc...                   ↓                                │
│                    config/settings.py                      │
│                    (Pydantic loader)                       │
│                           ↓                                │
│                    FastAPI/Python Services                │
│                    (Access via settings)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PRODUCTION                                                 │
│  ─────────────────────────────────────────────────────      │
│                                                             │
│  GitHub Secrets ──────────┐                                │
│  (encrypted)              │                                │
│  OPENAI_API_KEY           │                                │
│  DATABASE_URL             ↓                                │
│  S3_ACCESS_KEY     GitHub Actions                          │
│  etc...            (CI/CD workflow)                        │
│                           ↓                                │
│                    Docker Container                        │
│                    (Environment variables)                 │
│                           ↓                                │
│                    Production Services                     │
│                           ↓                                │
│  Azure Key Vault (C#/.NET services)                       │
│  (Managed Identity access)                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Configuration Reference

### All Available Variables

```bash
# Application
ENVIRONMENT=development              # development | staging | production
DEBUG=false                           # true | false
LOG_LEVEL=INFO                        # DEBUG | INFO | WARNING | ERROR

# Database
DATABASE_URL=postgresql+psycopg://    # PostgreSQL connection string

# Storage (MinIO/S3)
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minio
S3_SECRET_KEY=minio123
S3_BUCKET=eagle-files

# Cache (Redis)
REDIS_URL=redis://localhost:6379/0

# Language Models
OPENAI_API_KEY=sk-proj-...            # OpenAI API key
OLLAMA_ENABLED=false                  # Enable local LLM
OLLAMA_API_TOKEN=...                  # Ollama authentication

# Orchestration
N8N_ENABLED=true
N8N_API_KEY=...

# Jurisdiction
DEFAULT_STATE=GA
CODE_SET=IRC2018_IECC2015_NEC2017_GA
```

---

## 💾 Loading Priority

```
1. Environment Variables (HIGHEST priority)
   └─ Overrides everything

2. .env.local file
   └─ Your local/development secrets

3. .env file
   └─ Shared development defaults

4. Code defaults (LOWEST priority)
   └─ Built-in fallback values
```

**Example:**
```python
# In code
api_key_default = "default"

# In .env
OPENAI_API_KEY=from_env_file

# In .env.local
OPENAI_API_KEY=from_local_file

# In environment
export OPENAI_API_KEY=from_environment

# Result: from_environment (highest priority wins)
```

---

## ✅ Pre-Launch Checklist

### Local Setup
```
☐ Created .env.local from .env.example
☐ Added OPENAI_API_KEY to .env.local
☐ Added DATABASE_URL to .env.local
☐ Added S3_* credentials to .env.local
☐ Ran: python verify_config.py
☐ All checks passed ✓
☐ Verified .env.local is in .gitignore
☐ Verified .env.local is not in git: git status
```

### Python Services
```
☐ Installed: pip install -r config/requirements.txt
☐ Imported: from config.settings import get_settings
☐ Tested: settings = get_settings()
☐ Works: settings.openai.api_key is not None
```

### .NET Services
```
☐ Initialized secrets: dotnet user-secrets init
☐ Set secrets: dotnet user-secrets set "OpenAI:ApiKey" "sk-proj-..."
☐ Configured: Added to Program.cs
☐ Tested: Can read configuration values
```

### CI/CD
```
☐ Added secrets to GitHub: Settings → Secrets and variables → Actions
☐ Updated workflow to use: ${{ secrets.OPENAI_API_KEY }}
☐ Tested: Workflow runs successfully
```

### Team
```
☐ Shared .env.example with team
☐ Explained local setup process
☐ Provided list of required API keys
☐ Added to onboarding documentation
☐ Scheduled 90-day key rotation
```

---

## 🆘 Troubleshooting Decision Tree

```
Problem: "ImportError: No module named config"
├─ Solution: pip install -r config/requirements.txt
└─ Test: python -c "from config.settings import get_settings"

Problem: "Settings failed to load"
├─ Check: python verify_config.py
├─ Check: Does .env.local exist?
└─ Check: Is it in project root (not subdirectory)?

Problem: "OpenAI API key is None"
├─ Check: cat .env.local | grep OPENAI_API_KEY
├─ Check: Does value start with "sk-proj-"?
├─ Check: No spaces before/after value?
└─ Fix: Edit .env.local with correct value

Problem: "Changes to .env.local don't take effect"
├─ Cause: Settings is cached (singleton)
├─ Fix: Restart Python process
├─ In development: Stop and restart service
└─ In tests: Use fixture to reload settings

Problem: ".env.local was accidentally committed"
├─ Danger: Your secrets are exposed!
├─ Immediate: Create new API keys
├─ Clean git history: git filter-branch (complex)
├─ Update GitHub: Use new keys
└─ Secure: Consider rotating all secrets
```

---

## 🔑 Getting API Keys

### OpenAI
```
1. Go: https://platform.openai.com/api-keys
2. Click: "Create new secret key"
3. Copy: sk-proj-... (save somewhere safe)
4. Add to .env.local: OPENAI_API_KEY=sk-proj-...
```

### n8n
```
1. Open: http://localhost:5678 (or your n8n URL)
2. Go: Settings → API Keys
3. Click: "Generate API Key"
4. Copy: n_... (save somewhere safe)
5. Add to .env.local: N8N_API_KEY=n_...
```

### Database (PostgreSQL)
```
1. Create user: createuser -P eagle
2. Create DB: createdb -O eagle eagle
3. Connection: postgresql+psycopg://eagle:password@localhost:5432/eagle
4. Add to .env.local: DATABASE_URL=postgresql+psycopg://...
```

### AWS / Azure Keys
```
1. AWS: IAM → Users → Create Access Key
2. Azure: Subscriptions → Access Control → Create Service Principal
3. Copy credentials to .env.local
4. Use in workflow: ${{ secrets.AWS_ACCESS_KEY }}
```

---

## 🛡️ Security Dos & Don'ts

### ✅ DO
```
✅ Keep .env.local in .gitignore
✅ Treat .env.local as confidential
✅ Use different keys per environment
✅ Rotate keys every 90 days
✅ Store production secrets in vaults
✅ Verify .env.local isn't in git
✅ Use strong passwords (20+ chars)
✅ Audit secret usage regularly
✅ Document access controls
✅ Monitor API usage for anomalies
```

### ❌ DON'T
```
❌ Commit .env.local to Git
❌ Share .env.local files
❌ Paste secrets in chat/email
❌ Log actual secret values
❌ Use same key for dev+prod
❌ Store secrets in comments
❌ Hardcode secrets in code
❌ Expose in error messages
❌ Use weak passwords
❌ Ignore rotation deadlines
```

---

## 📞 Need Help?

1. **Basic setup:** Read `SECRETS_CONFIGURATION_GUIDE.md`
2. **Specific issue:** Run `python verify_config.py`
3. **Code examples:** See `services/api/example_settings_usage.py`
4. **CI/CD setup:** Check `.github/SECRETS_GITHUB_ACTIONS.md`
5. **Full checklist:** Review `SECRETS_SETUP_COMPLETE.md`

---

## 🎯 You Are Here

```
🟢 DONE ✓
   ├─ Created config/settings.py
   ├─ Created .env.example
   ├─ Created verification script
   ├─ Created documentation
   └─ Created this quick reference

🟡 TODO
   ├─ Create .env.local (copy from .env.example)
   ├─ Add your API keys to .env.local
   ├─ Run python verify_config.py
   ├─ Share .env.example with team
   └─ Set up GitHub Secrets for CI/CD
```

---

## 🚀 Next: Run the Verification

```powershell
python verify_config.py
```

Expected output:
```
✓ All checks passed!
Eagle Eye is ready to run.
```

---

**Your Eagle Eye project is secure! 🔐**
