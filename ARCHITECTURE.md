# Eagle Eye Architecture

Complete system architecture for Eagle Eye plan review + pricing system with OSS integrations.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SOURCES                            │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │  Odoo    │    │ ERPNext  │    │   IFC    │    │   PDF    │     │
│  │Community │    │  (CRM)   │    │  Models  │    │  Plans   │     │
│  │Estimator │    │          │    │ (Revit)  │    │          │     │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘     │
└───────┼──────────────┼───────────────┼──────────────┼─────────────┘
        │              │               │              │
        │ XML-RPC      │ Frappe API    │ Upload       │ Upload
        ▼              ▼               ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INTEGRATION LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │ Odoo Connector │  │ ERPNext Bridge │  │IfcOpenShell QTO│       │
│  │   (Flask)      │  │   (n8n node)   │  │   (Flask)      │       │
│  │   :5002        │  │                │  │   :5001        │       │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘       │
│           │                   │                   │                │
│           └───────────────────┼───────────────────┘                │
│                               │                                    │
│                        Normalized JSON                             │
│                      (Eagle Eye Schema)                            │
└───────────────────────────────┼─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                       n8n Workflow Engine                     │  │
│  │                           :5678                               │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  Webhook → Route by Source → Fetch → Normalize → Process    │  │
│  │  → Generate Reports → Push Back to Source → Notify          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    MCP Server (stdio)                         │  │
│  │                 agents/mcp-server                             │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  Tools: parse_plan, check_code, calculate_price,            │  │
│  │         generate_proposal, manage_project                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┼─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    API Service (FastAPI)                     │  │
│  │                          :8000                               │  │
│  ├─────────────────────────────────────────────────────────────┤  │
│  │  • CRM (Clients, Contacts, Jobs)                            │  │
│  │  • Projects (Properties, Plans, Tasks)                      │  │
│  │  • Findings (Code violations, Deficiencies)                 │  │
│  │  • Estimates (Line items, Pricing, Alternates)              │  │
│  │  • Reports (PDF/CSV generation triggers)                    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Parser  │  │  Rules   │  │ Pricing  │  │ Reports  │          │
│  │  :8001   │  │  :8002   │  │  :8003   │  │  :8004   │          │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘          │
│        │             │             │             │                 │
│        │             │             │             │                 │
│   ┌────▼─────┐  ┌───▼────┐  ┌─────▼────┐  ┌─────▼─────┐          │
│   │pdfplumber│  │IRC 2018│  │TradeBase │  │  Jinja2   │          │
│   │ Tesseract│  │IECC2015│  │Regional  │  │ WeasyPrint│          │
│   │  SAM/    │  │NEC 2017│  │  Factors │  │  Xactimate│          │
│   │Grounding │  │GA Amend│  │SpecTiers │  │   CSV     │          │
│   │  DINO    │  │        │  │          │  │           │          │
│   └──────────┘  └────────┘  └──────────┘  └───────────┘          │
│                                                                     │
└───────────────────────────────┼─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │               PostgreSQL 16 (Primary Database)                │  │
│  │                          :5432                                │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  • clients, contacts, jobs (CRM)                             │  │
│  │  • projects, properties, plans, plan_sheets                  │  │
│  │  • findings, finding_evidence                                │  │
│  │  • estimates, line_items, alternates, allowances             │  │
│  │  • catalog_items, regional_factors, spec_tier_bundles        │  │
│  │  • submittals, deficiencies, draw_schedule                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌────────────────────────┐    ┌──────────────────────────────┐   │
│  │  MinIO (Object Store)  │    │      Redis (Cache/Queue)     │   │
│  │        :9000           │    │          :6379               │   │
│  ├────────────────────────┤    ├──────────────────────────────┤   │
│  │  • PDF plans           │    │  • Job queue (Celery)        │   │
│  │  • IFC models          │    │  • Session cache             │   │
│  │  • Generated reports   │    │  • Rate limiting             │   │
│  │  • Photos/evidence     │    │  • Parsed plan graph cache   │   │
│  └────────────────────────┘    └──────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Next.js 14 Frontend (SSR + SSG)                  │  │
│  │                          :3000                                │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  Pages:                                                       │  │
│  │    • /dashboard - Project overview, active reviews           │  │
│  │    • /projects/[id] - Upload plans, run pipeline             │  │
│  │    • /review/[id] - Findings viewer (red/orange/yellow)      │  │
│  │    • /estimate/[id] - Pricing breakdown with alternates      │  │
│  │    • /proposal/[id] - Preview & download deliverables        │  │
│  │    • /clients - CRM management                               │  │
│  │                                                               │  │
│  │  Components (shadcn/ui):                                      │  │
│  │    • FileUploadZone, FindingsTable, PricingGrid              │  │
│  │    • ProposalPreview, DrawScheduleTable                      │  │
│  │                                                               │  │
│  │  State: React Query + Zustand                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Scenario 1: PDF Plan Upload (Direct)

```
User uploads PDF
     ↓
Next.js Frontend
     ↓ POST /projects/{id}/files
FastAPI API Service
     ↓ Store blob
MinIO (S3)
     ↓ Trigger pipeline
n8n Workflow
     ↓ HTTP POST /api/parser/process
Parser Service
     ↓ pdfplumber + Tesseract
Extract schedules, quantities
     ↓ Return plan_graph JSON
     ↓ POST /api/rules/check
Rules Service
     ↓ IRC/IECC/NEC/GA checks
Generate findings with citations
     ↓ Return findings[] JSON
     ↓ POST /api/pricing/estimate
Pricing Service
     ↓ TradeBase + regional factors
Calculate line items + alternates
     ↓ Return estimate JSON
     ↓ POST /api/reports/proposal
Reports Service
     ↓ Jinja2 + WeasyPrint
Render comprehensive proposal PDF
     ↓ Store in MinIO
     ↓ Notify user
Email + UI notification
```

### Scenario 2: Odoo Integration (Bidirectional Sync)

```
User creates estimate in Odoo
     ↓
Odoo triggers webhook
     ↓ POST /sync/odoo-to-eagle
Odoo Connector Service
     ↓ XML-RPC: read estimate lines
Fetch from Odoo
     ↓ Map fields to Eagle Eye schema
     ↓ POST /api/estimates/process
Eagle Eye API
     ↓ Store in PostgreSQL
     ↓ Trigger n8n workflow
n8n Multi-Source Pipeline
     ↓ (Skip Parser - already have quantities)
     ↓ POST /api/rules/check
Rules Service
     ↓ Code compliance checks
Findings generated
     ↓ POST /api/pricing/estimate
Pricing Service
     ↓ Regional adjustments + spec tier pricing
Enhanced estimate
     ↓ POST /api/reports/proposal
Reports Service
     ↓ Generate comprehensive proposal
PDF + Xactimate CSV
     ↓ POST /sync/eagle-to-odoo
Odoo Connector
     ↓ XML-RPC: update estimate
Push findings as internal notes
     ↓ Update pricing
Odoo estimate enhanced with code review
```

### Scenario 3: IFC/BIM Workflow

```
User uploads IFC model
     ↓ POST /qto (multipart file)
IfcOpenShell Service
     ↓ IfcOpenShell library
Parse IFC elements (walls, windows, doors, slabs, roofs)
     ↓ Extract quantities (IfcQuantityArea, etc.)
     ↓ Convert metric → imperial
     ↓ Map to Eagle Eye schema
Quantities JSON with WBS codes
     ↓ Return to n8n workflow
     ↓ POST /api/estimates/process
Eagle Eye API
     ↓ Store quantities (High confidence)
     ↓ Trigger rules/pricing pipeline
Same as PDF flow
     ↓
Generate proposal with BIM-sourced quantities
```

## Technology Stack

### Frontend

- **Framework**: Next.js 14.2.5 (React 18)
- **Language**: TypeScript 5.3.3
- **Styling**: Tailwind CSS 3.4 + shadcn/ui components
- **State**: React Query (server state) + Zustand (client state)
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts for pricing visualizations

### Backend Services

- **API Framework**: FastAPI 0.109.0 (Python 3.11)
- **Validation**: Pydantic 2.x
- **ORM**: SQLAlchemy 2.x (async)
- **Migrations**: Alembic
- **Auth**: JWT tokens (future: Clerk/Auth0)

### Data Processing

- **PDF Parsing**: pdfplumber 0.11 + pytesseract 0.3
- **Vision (optional)**: SAM + GroundingDINO for segmentation
- **IFC Parsing**: IfcOpenShell 0.7.0
- **Code Checks**: Custom deterministic rule engine

### Pricing & Templates

- **Pricing**: pandas for regional factor calculations
- **Templates**: Jinja2 3.1
- **PDF Generation**: WeasyPrint 60
- **CSV Export**: Xactimate-compatible format

### Infrastructure

- **Database**: PostgreSQL 16-alpine
- **Cache**: Redis 7-alpine
- **Storage**: MinIO (S3-compatible)
- **Orchestration**: n8n 1.68.0 + MCP stdio server
- **Containers**: Docker 24+ with Compose v2

### Integrations

- **Odoo**: XML-RPC bridge (Flask)
- **ERPNext**: Frappe API (custom doctypes)
- **IfcOpenShell**: Flask service for BIM QTO

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Network Layer                                           │
│     • Nginx reverse proxy with SSL (Let's Encrypt)         │
│     • UFW firewall (ports 80, 443, 22 only)                │
│     • Fail2Ban for SSH brute-force protection              │
│     • IP whitelisting for admin interfaces                 │
│                                                             │
│  2. Application Layer                                       │
│     • JWT authentication (future)                          │
│     • RBAC with role-based permissions                     │
│     • Input validation (Pydantic schemas)                  │
│     • SQL injection prevention (parameterized queries)     │
│     • XSS protection (CSP headers)                         │
│                                                             │
│  3. Data Layer                                              │
│     • PostgreSQL row-level security (RLS)                  │
│     • Encrypted passwords (bcrypt)                         │
│     • API keys stored in environment variables             │
│     • MinIO access keys rotated quarterly                  │
│                                                             │
│  4. Audit Layer                                             │
│     • All API requests logged                              │
│     • Database audit trail for quantity/price changes      │
│     • File upload/download tracking                        │
│     • User action logging (who/what/when)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

### Development

```
Local Machine
├── docker-compose up (all services)
├── PostgreSQL :5432
├── MinIO :9000
├── Redis :6379
├── API :8000
├── Parser/Rules/Pricing/Reports :8001-8004
├── n8n :5678
├── Odoo :8069
├── IfcOpenShell :5001
└── Next.js dev server :3000
```

### Production

```
Cloud Server (AWS/Azure/DO)
├── Nginx (reverse proxy)
│   ├── yourdomain.com → :3000 (Next.js)
│   ├── api.yourdomain.com → :8000 (FastAPI)
│   ├── n8n.yourdomain.com → :5678 (n8n - IP restricted)
│   └── odoo.yourdomain.com → :8069 (Odoo - optional)
│
├── Docker Compose (production mode)
│   ├── PostgreSQL (internal :5432)
│   ├── MinIO (internal :9000)
│   ├── Redis (internal :6379)
│   ├── API + microservices
│   └── Integration services
│
├── Backups
│   ├── PostgreSQL dump (daily 2 AM)
│   ├── MinIO data sync (daily 3 AM)
│   └── 7-day retention
│
└── Monitoring
    ├── Docker health checks
    ├── External uptime monitoring (Uptime Robot)
    └── Log aggregation (Promtail + Loki - optional)
```

## Performance Characteristics

### Expected Throughput

- **PDF parsing**: 1-2 minutes for 50-page plan set
- **Code checks**: 5-10 seconds for 100 line items
- **Pricing calculation**: 2-3 seconds for 500 assemblies
- **PDF generation**: 10-15 seconds for comprehensive proposal
- **IFC parsing**: 30-60 seconds for medium complexity model

### Resource Usage

- **API Service**: 512MB RAM, 1 CPU
- **Parser Service**: 2GB RAM, 2 CPU (Tesseract OCR)
- **Rules Service**: 256MB RAM, 1 CPU
- **Pricing Service**: 512MB RAM, 1 CPU
- **Reports Service**: 1GB RAM, 1 CPU (WeasyPrint)
- **PostgreSQL**: 4GB RAM, 2 CPU
- **MinIO**: 1GB RAM, 1 CPU
- **n8n**: 512MB RAM, 1 CPU

**Total minimum**: 8 CPU cores, 16GB RAM for comfortable performance

### Scalability Limits

- **Concurrent users**: 50-100 (single server)
- **Projects**: Unlimited (database-limited)
- **File size**: 100MB per PDF (configurable)
- **IFC size**: 500MB per model (configurable)
- **Storage**: Unlimited (MinIO scales horizontally)

## Development Workflow

```
Feature Development
     ↓
1. Create feature branch
     ↓
2. Develop locally (make up)
     ↓
3. Test with sample plans
     ↓
4. Run unit tests (pytest)
     ↓
5. Test integration flow
     ↓
6. PR to main branch
     ↓
7. Code review
     ↓
8. Merge to main
     ↓
9. Deploy to staging
     ↓
10. QA testing
     ↓
11. Deploy to production
     ↓
12. Monitor logs/metrics
```

## Extension Points

### Adding New Code Standards

```python
# services/rules/ibc_2024.py
from typing import List
from packages.shared.models import Finding

def check_ibc_2024(quantities: dict, plan_graph: dict) -> List[Finding]:
    findings = []
    
    # Implement IBC 2024 checks
    # ...
    
    return findings
```

### Custom Pricing Catalogs

```sql
-- infra/seeds/custom_catalog.sql
INSERT INTO catalog_items (wbs, assembly, item, uom, base_unit_cost, region)
VALUES
  ('03.01', 'Standing Seam Metal Roof', '24ga Galvalume', 'SF', 12.50, 'Southeast'),
  ('04.01', 'Impact Windows', 'Vinyl DP50+', 'EA', 850.00, 'Florida');
```

### External API Integration

```python
# services/pricing/vendors/acme_supply.py
import requests

def get_live_quote(item_code: str, quantity: int) -> float:
    """Fetch live pricing from vendor API"""
    response = requests.post(
        "https://api.acmesupply.com/quote",
        json={"item": item_code, "qty": quantity}
    )
    return response.json()["unit_price"]
```

---

**Architecture designed for**:

- ✅ Modularity (swap parsers, add rule packs, integrate pricing sources)
- ✅ Scalability (horizontal scaling for API/workers)
- ✅ Reliability (health checks, backups, rollback procedures)
- ✅ Extensibility (OSS integrations, custom catalogs, new code standards)
- ✅ Maintainability (clear separation of concerns, documented APIs)
