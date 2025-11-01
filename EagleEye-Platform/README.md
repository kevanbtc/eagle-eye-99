# EagleEye Platform Starter

**A minimal, production-ready scaffold for construction plan review and pricing.**

Manage CRM, upload plans, generate estimates, and use AI assistance — all in one stack.

---

## What's Included

- **PostgreSQL 16** — Relational database for accounts, contacts, projects, files, findings, and estimates
- **FastAPI Backend** — 6 REST endpoints (accounts, contacts, projects, files, estimates, assist)
- **Next.js 14 Frontend** — Dashboard, project creation, file upload, estimate generation, financing calculator
- **Financial Utilities** — Loan and lease payment calculators
- **AI Assistant** — Optional OpenAI integration for summarization (graceful fallback if no API key)

---

## Quick Start

### 1. Prerequisites

- Docker + Docker Compose
- (Optional) OpenAI API key for AI features

### 2. Clone or Copy

```powershell
cd EagleEye-Platform
```

### 3. Launch

```powershell
cd infra
docker compose up -d --build
```

Services will start:
- **Database**: PostgreSQL on port 5432
- **API**: FastAPI on [http://localhost:8000](http://localhost:8000)
- **Web**: Next.js on [http://localhost:3000](http://localhost:3000)

### 4. Access

- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Web UI**: [http://localhost:3000](http://localhost:3000)

---

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│  Next.js    │─────>│  FastAPI     │─────>│ PostgreSQL   │
│  (port 3000)│      │  (port 8000) │      │ (port 5432)  │
└─────────────┘      └──────────────┘      └──────────────┘
     Web UI             REST API              Database
```

### Database Schema

- **accounts** — Companies, GCs, subs, lenders, partners
- **contacts** — People linked to accounts
- **projects** — Plan review projects with jurisdiction and status
- **files** — Uploaded PDFs, drawings, specs
- **findings** — Code compliance issues (severity, discipline, citation, recommendation)
- **estimates** — Pricing data (base items, alternates, allowances, summary)

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/accounts` | Create account |
| GET | `/accounts` | List accounts |
| POST | `/contacts` | Create contact |
| GET | `/contacts` | List contacts |
| POST | `/projects` | Create project |
| GET | `/projects` | List projects |
| POST | `/files/{project_id}` | Upload file |
| POST | `/estimates/{project_id}/quick` | Generate quick estimate |
| GET | `/estimates/{project_id}` | Get latest estimate |
| GET | `/estimates/{project_id}/findings` | List findings |
| POST | `/assist/summarize` | AI summary helper |

---

## Usage Flow

1. **Create Account** — Add a company (owner, GC, sub, lender, partner)
2. **Create Project** — Link to account, set jurisdiction
3. **Upload Plans** — PDF drawings/specs
4. **Generate Estimate** — Click "Generate Quick Estimate" (placeholder logic for now)
5. **Review Findings** — See code compliance issues (sample IRC 2018 R703.4 finding)
6. **Calculate Financing** — Adjust APR and term to see monthly payment

---

## Configuration

### Environment Variables

Create `.env` file in `infra/` directory:

```env
# Optional: OpenAI API key for AI assistant
OPENAI_API_KEY=sk-...

# Database (defaults work for Docker Compose)
DATABASE_URL=postgresql+psycopg://eagle:eagle@db:5432/eagleeye

# Storage (local filesystem)
STORAGE_DIR=/app/storage
```

### Without OpenAI Key

The `/assist/summarize` endpoint falls back to a mock summary:
```
[Mock] Summary for: {text[:120]}...
```

---

## Development

### Run Tests

```powershell
docker compose exec api pytest app/tests/
```

### View Logs

```powershell
docker compose logs -f api
docker compose logs -f web
```

### Stop Services

```powershell
docker compose down
```

### Remove All Data

```powershell
docker compose down -v  # Removes database volume
```

---

## Extending the Platform

### Replace Placeholder Estimate Logic

The `quick_estimate()` function in `services/api/app/routers/estimates.py` returns hardcoded data:

```python
payload = {
  "base": [{"ee_code":"EE-RBL-DW-HANG-001","uom":"SF","qty":1000,"unit":1.75,"ext":1750}],
  "alternates": [{"name":"Standing seam roof","amount":12000}],
  "allowances": [{"name":"Inspections/Testing","amount":500}],
  "summary": {"subtotal":14250,"op":0.10,"cont":0.05,"total":16387.50}
}
```

**Next Steps:**
- Integrate with the comprehensive Eagle Eye pricing service
- Add regional factor adjustments
- Implement spec tier bundles
- Connect to Odoo/ERPNext for real costing data

### Add Code Compliance Rules

The platform creates a sample Finding for IRC 2018 R703.4 (pan flashing). To add real rules:

1. Import rule packs from main Eagle Eye system (IRC, IECC, NEC, Georgia amendments)
2. Implement PDF parsing for plan review
3. Add deterministic checks for code violations
4. Use LLM for last-mile polish and recommendation generation

### Enable BIM Quantity Takeoff

Integrate IfcOpenShell service:
```python
# services/api/app/routers/estimates.py
import requests
ifc_response = requests.post("http://ifcopenshell:9000/qto", files={"file": ifc_file})
quantities = ifc_response.json()
```

### Connect to ERP Systems

- **Odoo**: Use `integrations/odoo/odoo_connector.py` for XML-RPC integration
- **ERPNext**: Follow `integrations/erpnext/README.md` for REST API setup

---

## File Structure

```
EagleEye-Platform/
├── infra/
│   └── docker-compose.yml       # 3-service orchestration
├── services/
│   └── api/
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── storage/             # Uploaded files
│       └── app/
│           ├── main.py          # FastAPI app
│           ├── db.py            # Database connection
│           ├── models.py        # SQLAlchemy models
│           ├── schemas.py       # Pydantic schemas
│           ├── util_finance.py  # Loan/lease calculators
│           ├── routers/         # 6 API routers
│           └── tests/           # Unit tests
└── apps/
    └── web/
        ├── Dockerfile
        ├── package.json
        ├── next.config.js
        ├── tsconfig.json
        ├── app/                 # Next.js pages
        └── components/          # React components
```

---

## Why This Works

✅ **Clean separation** — API vs Web with Docker  
✅ **Real DB** — Postgres from day 1 (no SQLite hacks)  
✅ **Upload → Estimate → Financing** — One-click workflow  
✅ **AI helper** — Ready but not required  
✅ **Financial calcs** — Loan/lease payments built-in  
✅ **Extensible** — Replace placeholders with real services later  

---

## Troubleshooting

### Database Connection Error

```
FATAL: password authentication failed for user "eagle"
```

**Fix**: Wait for database healthcheck to pass (20 retries × 5s = 100s max)

### Port Already in Use

```
Error: port is already allocated
```

**Fix**: Change ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Web
  - "8001:8000"  # API
```

### Frontend Shows "Cannot connect to API"

**Fix**: Update `NEXT_PUBLIC_API_BASE` in `docker-compose.yml`:
```yaml
environment:
  - NEXT_PUBLIC_API_BASE=http://localhost:8001
```

---

## License

MIT

---

## Next Steps

1. **Test end-to-end** — Create account → project → upload → estimate
2. **Customize UI** — Replace inline styles with CSS modules
3. **Add authentication** — JWT tokens, user accounts
4. **Deploy to cloud** — Azure Container Apps, AWS ECS, or DigitalOcean App Platform
5. **Integrate with main Eagle Eye** — Connect to comprehensive pricing service, rule packs, and BIM tools

---

**Built with ❤️ for construction professionals**
