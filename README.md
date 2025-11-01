# Eagle Eye – CRM + Senior Review + Pricing + One‑Click Proposal

> **Goal:** Drop‑in monorepo scaffold (API + Plan Ingest + Rules/PE checks + Pricing + Reports + MCP agents + n8n flow) that turns plan PDFs into a code‑cited risk report, priced estimate, and a lender/GC proposal in **minutes**.

## Architecture

### Frontend
- **apps/web**: Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
  - Upload page with drag-drop
  - Live review page with findings, quantities, pricing
  - One-click PDF/CSV generation

### Backend Services
- **services/api**: FastAPI - CRM, Projects, Findings, Estimates
- **services/parser**: pdfplumber/Tesseract + optional SAM/GroundingDINO
- **services/rules**: Deterministic code checks (IRC/IECC/NEC + GA)
- **services/pricing**: TradeBase catalog + regional factors engine
- **services/reports**: Jinja2 → PDF/DOCX/CSV generation

### Orchestration
- **agents/mcp-server**: MCP (stdio) tools for pipeline orchestration
- **workflows/n8n**: Automated flow (upload→parse→rules→price→render→email)

### Infrastructure
- PostgreSQL 16 (database)
- MinIO (S3-compatible storage)
- Redis (cache/queue)
- Docker Compose for local development

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for service development)

### Setup

```bash
# 1. Clone and navigate
cd eagle-eye

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
make up

# 4. Seed database with schema + pricing data
make seed

# 5. Access services
# - API: http://localhost:8000/docs
# - Web: http://localhost:3000
# - n8n: http://localhost:5678
# - MinIO Console: http://localhost:9001
```

### Development Workflow

```bash
# View logs
make logs

# Reset everything (caution: deletes data)
make reset

# Develop frontend locally
make dev-web

# Install dependencies
make install
```

## Key Features

### 1. Plan Ingestion & Parsing
- Upload construction plan PDFs
- Extract schedules (windows, doors, equipment)
- Build plan graph with sheet references

### 2. Code Compliance Checks
- Deterministic rules engine for IRC 2018, IECC 2015, NEC 2017, Georgia amendments
- Red/Orange/Yellow severity findings
- Code citations with sheet/location references
- PE-level structural focus

### 3. Pricing Engine
- TradeBase catalog with regional labor/material factors
- Base estimate + alternates + allowances
- O&P slider, permit/demo adjustments
- Xactimate-compatible CSV export

### 4. One-Click Deliverables
- **Eagle Eye Proposal (PDF)**: A–I sections with risk table, code cites, pricing, draw schedule
- **Lender Summary (PDF/XLSX)**: Subtotals, O&P, risk assessment, draws
- **Owner/GC Proposal (PDF)**: Scope with alternates and payment schedule
- **Xactimate CSV**: WBS/assemblies/line items

## Project Structure

```
eagle-eye/
├── apps/
│   └── web/                 # Next.js frontend
├── services/
│   ├── api/                 # FastAPI main API
│   ├── parser/              # PDF parsing service
│   ├── rules/               # Code compliance engine
│   ├── pricing/             # Pricing calculator
│   └── reports/             # Report generation
├── agents/
│   └── mcp-server/          # MCP orchestration tools
├── workflows/
│   └── n8n/                 # n8n automation flows
├── infra/
│   ├── docker-compose.yml   # Container orchestration
│   ├── db/                  # Database schema & seeds
│   └── seeds/               # Regional factors & trade base
├── templates/               # Jinja2 templates for PDFs
├── packages/
│   └── shared/              # Shared Pydantic/TS models
└── README.md
```

## OSS Estimating Integrations

Eagle Eye can integrate with existing open-source estimating/takeoff tools:

### 🚀 Odoo (Fastest)
Pre-built UI for estimating + quoting. Eagle Eye adds PE-grade code review to Odoo Construction Estimator quotes.

```bash
cd integrations/odoo && docker-compose up -d
# See: integrations/QUICKSTART.md
```

### 🏗️ ERPNext (Full Control)
100% OSS CRM + job costing + accounting. Custom doctypes for seamless Eagle Eye integration.

```bash
# See detailed guide: integrations/erpnext/README.md
```

### 📐 IfcOpenShell (BIM Workflows)
Auto-extract quantities from IFC models (Revit, ArchiCAD). High-confidence takeoffs feed directly into Eagle Eye pricing.

```bash
cd integrations/ifcopenshell && docker-compose up -d
curl -X POST http://localhost:5001/qto -F "file=@model.ifc"
```

**→ Full guide:** [integrations/QUICKSTART.md](./integrations/QUICKSTART.md)

---

## API Endpoints

### Projects
- `POST /projects` - Create new project
- `GET /projects/{id}` - Get project details
- `POST /projects/{id}/files` - Upload plan files
- `POST /projects/{id}/run` - Execute pipeline (parse→rules→price→render)

### Findings & Estimates
- `GET /projects/{id}/findings` - Get code compliance findings
- `GET /projects/{id}/estimate` - Get pricing estimate
- `GET /projects/{id}/reports` - Download generated reports

### Integration Endpoints
- `POST /api/estimates/process` - Process estimate from external source (Odoo/ERPNext/IFC)
- `GET /api/integrations/health` - Check integration service status

## OpenAI Integration

OpenAI is used strategically for:
- **Narrative polish**: Converting technical findings into client-friendly prose
- **Proposal sections**: Executive summaries and explanations
- **NOT used for**: Core compliance math, code citations, or pricing calculations

## Quality & Governance

- Deterministic rules first, LLM last-mile only
- Versioned plan graphs, findings, and estimates
- RBAC + audit logging
- Unit tests for rules engine
- Golden-file tests for templates

## Next Steps (Optional)

- Vision upgrade: SAM/GroundingDINO for wall/door/window segmentation
- Cost plugins: RSMeans overlay or vendor live quotes
- Client portal: E-signature, deposits, submittal uploads
- Inspector view: Read-only risk dashboard with photo logs

## License

Proprietary - Eagle Eye AI

## Support

Contact: support@eagleeye.ai
