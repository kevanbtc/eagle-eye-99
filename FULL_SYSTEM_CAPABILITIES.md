# 🦅 Eagle Eye - Complete System Architecture & Capabilities

## Executive Summary

**Eagle Eye** is an enterprise-grade construction plan review and pricing system that combines:

1. **Deterministic Code Compliance Engine** (Rules, Findings)
2. **AI Vision Pipeline** (Plan parsing, quantity extraction)
3. **Intelligent Pricing System** (Regional factors, spec tiers, contingency)
4. **Agentic Orchestration** (MCP + n8n + AI Swarm)
5. **Enterprise Integration** (Odoo, ERPNext, IFC models, custom APIs)
6. **Production-Ready Infrastructure** (.NET Clean Architecture, FastAPI services)

**Full workflow**: Upload PDF plan → Parse & extract quantities → Run compliance checks → Generate pricing estimate → Produce PDF proposal → Send to client/CRM

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EAGLE EYE FULL STACK                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER 1: USER INTERFACES                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📱 Next.js Web Portal              🚀 EagleEye.NET (C# API)               │
│  ├─ Upload → Review → Estimate      ├─ Clean Architecture                 │
│  ├─ Live pricing dashboard          ├─ Domain/App/Infrastructure          │
│  ├─ PDF/CSV export                  ├─ Modular (Estimating, etc.)        │
│  ├─ Proposal generation             ├─ Async jobs (Hangfire-ready)       │
│  └─ Client portal (future)          └─ Health checks, structured logging  │
│                                                                              │
│  🔗 Integration Portals                                                    │
│  ├─ Odoo (CRM sync)                                                        │
│  ├─ ERPNext (ERP sync)                                                     │
│  └─ IFC Viewer (BIM models)                                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER 2: ORCHESTRATION LAYER (The Swarm)                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🤖 AI SWARM (smolagents + Claude/GPT-4 Orchestration)                    │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │ MCP SERVER (Model Context Protocol - stdio)              │           │
│  │ ├─ Coordinator Agent (mission planning & oversight)     │           │
│  │ ├─ Parser Agent (PDF → structured data)                 │           │
│  │ ├─ Compliance Agent (IRC/IECC/NEC rule checks)         │           │
│  │ ├─ Pricing Agent (cost calculation + adjustments)      │           │
│  │ ├─ Render Agent (proposal templates + export)          │           │
│  │ ├─ Vision Agent (SAM/Grounding DINO image analysis)   │           │
│  │ ├─ Integration Agent (Odoo/ERPNext sync)              │           │
│  │ └─ Quality Agent (confidence scoring & RFI flagging)  │           │
│  └────────────────────────────────────────────────────────────┘           │
│                                                                              │
│  🔄 WORKFLOW ENGINE (n8n)                                                  │
│  └─ Automated pipelines: Upload → Parse → Rules → Price → Render → Email  │
│                                                                              │
│  📊 STATE MANAGEMENT                                                       │
│  ├─ Redis (session, cache, queuing)                                       │
│  ├─ PostgreSQL (projects, findings, estimates - versioned)                │
│  └─ MinIO S3 (PDFs, plans, exports)                                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER 3: MICROSERVICES LAYER                                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🔵 API Service (FastAPI)           🟢 EagleEye.Api (ASP.NET Core)        │
│  ├─ Project CRUD                    ├─ Same domain logic (multiplatform)  │
│  ├─ File upload/download            ├─ REST endpoints                     │
│  ├─ Pipeline orchestration          ├─ OpenAPI/Swagger                   │
│  └─ Health checks                   └─ Health checks at /health          │
│                                                                              │
│  📄 Parser Service (pdfplumber)     🏗️ EagleEye.Infrastructure (EF Core) │
│  ├─ PDF extraction                  ├─ AppDbContext                       │
│  ├─ OCR (Tesseract)                 ├─ EF migrations                      │
│  ├─ Plan graph builder              └─ DbSets for all domains            │
│  └─ Confidence scoring                                                     │
│                                                                              │
│  ✅ Rules Service (Deterministic)   💰 Pricing Service (Calculations)    │
│  ├─ IRC 2018 checks                 ├─ TradeBase lookup                   │
│  ├─ IECC 2015 checks                ├─ Regional factors                   │
│  ├─ NEC 2017 checks                 ├─ Spec tier matrices                │
│  ├─ Georgia amendments              ├─ OH&P policy engine                 │
│  └─ Finding generation              └─ Contingency scoring               │
│                                                                              │
│  📋 Reports Service (Template)       🎨 Vision Service (Optional)        │
│  ├─ Jinja2 rendering                ├─ SAM (Segment Anything)            │
│  ├─ PDF generation                  ├─ Grounding DINO (detection)        │
│  ├─ CSV/DOCX export                 ├─ Donut (document analysis)         │
│  └─ Xactimate format                └─ LayoutLMv3 (form extraction)      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER 4: DATA & INTEGRATION LAYER                                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🐘 PostgreSQL 16                   🔑 Redis 7 (Cache & Queue)           │
│  ├─ Projects table                  ├─ Session storage                    │
│  ├─ Findings (versioned)            ├─ Rate limiting                      │
│  ├─ Estimates (versioned)           ├─ Job queue (async tasks)           │
│  ├─ Regional factors                ├─ Plan graph cache                  │
│  ├─ Rate catalogs                   └─ Contractor recommendations         │
│  ├─ Spec tier bundles                                                      │
│  └─ Audit logs                      📦 MinIO S3-Compatible               │
│                                       ├─ Plan PDFs                         │
│                                       ├─ Parsed outputs                    │
│                                       ├─ Generated proposals               │
│                                       └─ Audit trail (immutable)          │
│                                                                              │
│  🔗 Integration Connectors          📐 IFC + BIM Support                  │
│  ├─ Odoo ERP (CRM, quotes, invoices)├─ IfcOpenShell (QTO extraction)   │
│  ├─ ERPNext (multi-tenant)          ├─ Model geometry analysis           │
│  ├─ QuickBooks (accounting)         ├─ Property extraction              │
│  ├─ Procore (project mgmt)          └─ Cost correlation                 │
│  └─ Buildertrend (scheduling)                                            │
│                                                                              │
│  🧠 External AI Services            📊 External Data Sources            │
│  ├─ OpenAI GPT-4 (narrative polish) ├─ RSMeans (pricing - future)      │
│  ├─ Claude (optional fallback)      ├─ Vendor APIs (live quotes)        │
│  ├─ Anthropic Batch API (scale)     └─ Market indices (lumber, steel)  │
│  └─ Hugging Face (local vision)                                         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Swarm Architecture (smolagents + MCP)

### Overview

The **AI Swarm** is a multi-agent orchestration system using:
- **smolagents** (Hugging Face agentic framework)
- **Model Context Protocol (MCP)** (Claude/OpenAI interface)
- **n8n** (workflow automation)
- **Redis** (task queue + state sharing)

### Agent Roles & Responsibilities

```
┌──────────────────────────────────────────────────────────────────┐
│ AI SWARM AGENTS                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1️⃣ COORDINATOR AGENT (Agentic Mission Planner)               │
│  ├─ Role: Mission & context awareness                           │
│  ├─ Triggers: Project upload, pipeline execution               │
│  ├─ Responsibilities:                                           │
│  │  ├─ Parse user intent (mode: parse, rules, price, etc.)    │
│  │  ├─ Delegate tasks to specialist agents                    │
│  │  ├─ Monitor agent progress & retries                       │
│  │  ├─ Aggregate results & quality checks                     │
│  │  └─ Handle errors & human escalation                       │
│  ├─ Tools Available:                                            │
│  │  ├─ mcp_get_project_context (fetch jurisdiction, spec_tier)│
│  │  ├─ mcp_dispatch_agent_task (enqueue agent jobs)          │
│  │  ├─ mcp_poll_agent_status (check progress)                │
│  │  └─ mcp_escalate_to_human (flag issues)                   │
│  └─ Example Flow:                                              │
│     "Parse plan, check codes for GA, price Luxury, then render"│
│                                                                  │
│────────────────────────────────────────────────────────────────│
│                                                                  │
│  2️⃣ PARSER AGENT (Vision + PDF Extraction)                    │
│  ├─ Role: Plan ingestion & quantity extraction                 │
│  ├─ Input: PDF file (binary) + metadata (jurisdiction, type)  │
│  ├─ Process:                                                    │
│  │  ├─ pdfplumber extraction (text, tables, coordinates)      │
│  │  ├─ Tesseract OCR (scanned schedules)                      │
│  │  ├─ Optional: SAM/Grounding DINO (wall/door detection)    │
│  │  ├─ Build plan graph (sheets, schedules, dependencies)     │
│  │  └─ Confidence scoring (High/Medium/Low per item)         │
│  ├─ Output:                                                     │
│  │  ├─ Structured quantities (doors, windows, linoleum, etc.) │
│  │  ├─ Plan graph (sheets, cross-references, metadata)       │
│  │  ├─ Confidence scores & RFI flags                         │
│  │  └─ Extracted text (for compliance checks)                │
│  ├─ Tools:                                                      │
│  │  ├─ mcp_parse_pdf (pdfplumber wrapper)                    │
│  │  ├─ mcp_ocr_image (Tesseract)                             │
│  │  ├─ mcp_segment_image (SAM - optional)                    │
│  │  └─ mcp_detect_objects (Grounding DINO - optional)       │
│  └─ Example Flow:                                              │
│     "Extract 12 windows, 4 doors, 2500 SF flooring from plan"  │
│                                                                  │
│────────────────────────────────────────────────────────────────│
│                                                                  │
│  3️⃣ COMPLIANCE AGENT (Code Rule Engine)                       │
│  ├─ Role: Deterministic code compliance checking              │
│  ├─ Input: Extracted plan data + jurisdiction (e.g., GA)     │
│  ├─ Process:                                                    │
│  │  ├─ Load IRC 2018, IECC 2015, NEC 2017, GA amendments    │
│  │  ├─ Run deterministic rules (wall height, setback, etc.)  │
│  │  ├─ Cross-reference with extracted items                 │
│  │  ├─ Generate findings with severity (Critical/Major/Info) │
│  │  └─ Cite code sections & requirement links               │
│  ├─ Output:                                                     │
│  │  ├─ Findings list (violation, reference, remediation)     │
│  │  ├─ Compliance score (pass/fail per code)                │
│  │  ├─ RFI recommendations (ask client to clarify)          │
│  │  └─ Remediation cost estimates                           │
│  ├─ Tools:                                                      │
│  │  ├─ mcp_load_code_rules (IRC/IECC/NEC from service)      │
│  │  ├─ mcp_check_rule (evaluate single rule)                │
│  │  ├─ mcp_generate_finding (create formatted finding)      │
│  │  └─ mcp_cite_code (retrieve authoritative reference)    │
│  └─ Example Flow:                                              │
│     "Found 3 findings: Windows not tempered (NEC 2017), walls│
│      exceeding setback (GA Amendment), flooring not rated"    │
│                                                                  │
│────────────────────────────────────────────────────────────────│
│                                                                  │
│  4️⃣ PRICING AGENT (Cost Calculation Engine)                  │
│  ├─ Role: Estimate generation with OH&P & contingency        │
│  ├─ Input: Quantities + spec_tier + regional_factors         │
│  ├─ Process:                                                    │
│  │  ├─ Lookup TradeBase catalog (material/labor rates)       │
│  │  ├─ Apply regional factors (GA multiplier)                │
│  │  ├─ Match spec tier (Standard/Premium/Luxury)            │
│  │  ├─ Calculate Overhead & Profit (trade-specific %)       │
│  │  ├─ Apply risk contingency (low-conf items = +%)         │
│  │  └─ Generate alternate pricing (budget-friendly options)  │
│  ├─ Output:                                                     │
│  │  ├─ Line items (qty, unit cost, extended)                │
│  │  ├─ Subtotal + OH&P breakdown                            │
│  │  ├─ Contingency (risk-based)                             │
│  │  ├─ Grand total                                           │
│  │  └─ Alternates list                                       │
│  ├─ Tools:                                                      │
│  │  ├─ mcp_lookup_rate (TradeBase + region + tier)          │
│  │  ├─ mcp_apply_regional_factors (region adjustments)      │
│  │  ├─ mcp_calculate_ohp (overhead/profit policy)           │
│  │  ├─ mcp_score_contingency (risk → contingency %)         │
│  │  └─ mcp_generate_alternate (budget/deluxe options)       │
│  └─ Example Flow:                                              │
│     "12 windows × $450 (GA premium) + labor × 1.1 OH&P        │
│      + 5% contingency (low-conf items) = $7,425 est."         │
│                                                                  │
│────────────────────────────────────────────────────────────────│
│                                                                  │
│  5️⃣ RENDER AGENT (Template & Export Generation)              │
│  ├─ Role: Proposal creation (PDF, CSV, DOCX)                │
│  ├─ Input: Findings + Estimate + Project metadata           │
│  ├─ Process:                                                    │
│  │  ├─ Select Jinja2 template (proposal style)             │
│  │  ├─ Populate template with findings, costs, terms        │
│  │  ├─ Optional: Use GPT-4 for narrative polish (exec summary)│
│  │  ├─ Generate PDF via WeasyPrint                          │
│  │  ├─ Export CSV for Xactimate/accounting                 │
│  │  └─ Archive original PDF in MinIO                        │
│  ├─ Output:                                                     │
│  │  ├─ Proposal PDF (branded, professional)                 │
│  │  ├─ CSV export (for Xactimate, QBO)                     │
│  │  ├─ HTML (for email, portal)                            │
│  │  └─ Archive metadata (audit trail)                       │
│  ├─ Tools:                                                      │
│  │  ├─ mcp_render_jinja2 (Jinja2 → HTML)                   │
│  │  ├─ mcp_pdf_from_html (WeasyPrint)                       │
│  │  ├─ mcp_polish_narrative (GPT-4 → client-friendly)      │
│  │  ├─ mcp_export_csv (Xactimate format)                    │
│  │  └─ mcp_archive_to_minio (S3 upload)                     │
│  └─ Example Flow:                                              │
│     "Created proposal.pdf (3 findings, $7.4K est), exported   │
│      to CSV for QBO, archived with audit trail"               │
│                                                                  │
│────────────────────────────────────────────────────────────────│
│                                                                  │
│  6️⃣ VISION AGENT (Advanced Image Analysis - Optional)        │
│  ├─ Role: Deep image understanding for plan details         │
│  ├─ Models Used:                                               │
│  │  ├─ SAM (Segment Anything Model) → wall/door/window masks │
│  │  ├─ Grounding DINO → object detection (label-free)       │
│  │  ├─ Donut → document understanding (forms, schedules)    │
│  │  └─ LayoutLMv3 → structured form extraction             │
│  ├─ Triggers:                                                   │
│  │  ├─ Auto: Low OCR confidence in Parser                  │
│  │  ├─ Manual: User requests "smart extraction"            │
│  │  └─ Workflow: After pdfplumber fails on handwritten items│
│  ├─ Output:                                                     │
│  │  ├─ Pixel-level segmentation masks                       │
│  │  ├─ Bounding boxes for geometry (walls, openings)       │
│  │  ├─ Extracted form fields (schedules, notes)           │
│  │  └─ High-confidence annotations for manual review       │
│  ├─ Tools:                                                      │
│  │  ├─ mcp_segment_image (SAM)                             │
│  │  ├─ mcp_detect_objects (Grounding DINO)                │
│  │  ├─ mcp_analyze_document (Donut)                        │
│  │  └─ mcp_extract_forms (LayoutLMv3)                      │
│  └─ Example Flow:                                              │
│     "Plan has handwritten notes → Vision Agent → detects      │
│      'kitchen renovation 12x14' + segmentation mask"         │
│                                                                  │
│────────────────────────────────────────────────────────────────│
│                                                                  │
│  7️⃣ INTEGRATION AGENT (CRM & ERP Sync)                       │
│  ├─ Role: Two-way data sync with external systems           │
│  ├─ Supports:                                                   │
│  │  ├─ Odoo (CRM, quotes, projects, invoicing)             │
│  │  ├─ ERPNext (multi-tenant ERP, GL posting)              │
│  │  ├─ QuickBooks (accounting, customer management)        │
│  │  ├─ Procore (project management, submittals)            │
│  │  └─ Buildertrend (scheduling, task coordination)        │
│  ├─ Process:                                                    │
│  │  ├─ Authenticate with external system                    │
│  │  ├─ Map Eagle Eye entities → CRM/ERP models             │
│  │  ├─ Bi-directional sync (create, update, retrieve)      │
│  │  ├─ Handle versioning & conflicts                        │
│  │  └─ Log all sync operations (audit trail)               │
│  ├─ Output:                                                     │
│  │  ├─ Created quote in Odoo                                │
│  │  ├─ Updated project status in ERPNext                   │
│  │  ├─ Posted journal entry in QB                          │
│  │  └─ Sync status (success/pending/failed)               │
│  ├─ Tools:                                                      │
│  │  ├─ mcp_odoo_api (Odoo xmlrpc wrapper)                 │
│  │  ├─ mcp_erpnext_api (ERPNext frappe wrapper)            │
│  │  ├─ mcp_quickbooks_api (QB OAuth + QBXML)              │
│  │  └─ mcp_sync_status (track sync state)                  │
│  └─ Example Flow:                                              │
│     "Proposal generated → create Odoo quote → link to project │
│      → post AR entry in QB → log sync in audit trail"        │
│                                                                  │
│────────────────────────────────────────────────────────────────│
│                                                                  │
│  8️⃣ QUALITY AGENT (Confidence Scoring & RFI)                 │
│  ├─ Role: QA / variance detection / escalation               │
│  ├─ Monitors:                                                   │
│  │  ├─ Parsing confidence (OCR quality, table extraction)   │
│  │  ├─ Code compliance mismatches (multiple violations)     │
│  │  ├─ Pricing outliers (unusually high/low costs)          │
│  │  ├─ Missing data (fields not extracted)                  │
│  │  └─ Agent loop detection (infinite retries)             │
│  ├─ Process:                                                    │
│  │  ├─ Calculate aggregate confidence score                 │
│  │  ├─ Flag low-confidence items as RFI                    │
│  │  ├─ Suggest manual review / human intervention          │
│  │  ├─ Recommend re-parsing with Vision Agent             │
│  │  └─ Generate quality report                             │
│  ├─ Output:                                                     │
│  │  ├─ Confidence score (0-100%)                           │
│  │  ├─ RFI list (questions for client/GC)                 │
│  │  ├─ Manual review checklist                             │
│  │  └─ Recommended actions (reparse, escalate, etc.)      │
│  ├─ Tools:                                                      │
│  │  ├─ mcp_calculate_confidence (aggregator)               │
│  │  ├─ mcp_generate_rfi (create RFI questions)             │
│  │  ├─ mcp_flag_for_review (human escalation)              │
│  │  └─ mcp_suggest_actions (remediation steps)             │
│  └─ Example Flow:                                              │
│     "Parser confidence 65% (handwritten schedule) → flag for  │
│      vision analysis → RFI: 'Clarify kitchen dimensions?' →  │
│      Manual review recommended"                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Agent Communication & State Management

```
┌──────────────────────────────────────────────────────────────────┐
│ AGENT COMMUNICATION FLOW                                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  REQUEST FLOW:                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. User uploads plan PDF → API /projects/{id}/files     │  │
│  │ 2. API stores file in MinIO, creates Job in Redis      │  │
│  │ 3. n8n webhook triggers → Coordinator Agent spawns     │  │
│  │ 4. Coordinator reads job params (jurisdiction, modes)  │  │
│  │ 5. Coordinator dispatches Parser → Compliance → Price  │  │
│  │ 6. Each agent uses MCP tools (stdio communication)     │  │
│  │ 7. Results stored in PostgreSQL & Redis cache          │  │
│  │ 8. Coordinator aggregates → Render Agent creates PDF   │  │
│  │ 9. Final proposal uploaded to MinIO + sent to user    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  STATE SHARING (Redis):                                         │
│  ├─ job:{project_id}:status → "parsing" / "pricing" / "done"  │
│  ├─ plan:{project_id}:graph → {sheets, quantities, metadata}  │
│  ├─ findings:{project_id}:{version} → [Finding, ...]         │
│  ├─ estimate:{project_id}:{version} → {lines, summary, ...}  │
│  └─ agent_queue:{coordinator,parser,compliance} → [Job, ...]  │
│                                                                  │
│  ERROR HANDLING:                                                 │
│  ├─ Agent fails → Quality Agent triggered                       │
│  ├─ Quality Agent flags RFI → Escalate to human               │
│  ├─ Human corrects data → Coordinator retries downstream       │
│  ├─ Timeout (>5min) → escalate to ops team                    │
│  └─ All errors logged in PostgreSQL audit_log table           │
│                                                                  │
│  RETRY LOGIC:                                                    │
│  ├─ Parser fails → optionally try Vision Agent                │
│  ├─ Rules fails → log finding + continue                      │
│  ├─ Pricing fails → use regional default + flag              │
│  ├─ Max retries: 3 (per agent) before escalation             │
│  └─ Exponential backoff (1s, 2s, 4s)                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📊 What the System Can Do (Complete Capabilities)

### 1. **Plan Ingestion & Parsing**

#### Deterministic (Default)
- ✅ PDF upload (drag-drop or API)
- ✅ pdfplumber text/table extraction
- ✅ Tesseract OCR for scanned schedules
- ✅ Schedule parsing (windows, doors, flooring, etc.)
- ✅ Plan graph builder (sheets, cross-references)
- ✅ Confidence scoring per line item
- ✅ RFI flagging (low-confidence items)
- ✅ Archive in MinIO with metadata

#### Advanced (Optional - Vision Agent)
- ✅ Wall/door/window detection (Grounding DINO)
- ✅ Pixel-level segmentation (SAM)
- ✅ Form extraction from schedules (Donut + LayoutLMv3)
- ✅ Handwritten note recognition
- ✅ Automatic fallback when OCR fails

**Output**: Structured quantities (12 windows, 4 doors, 2500 SF), plan graph, confidence scores

---

### 2. **Code Compliance Checking**

#### Supported Code Standards
- ✅ **IRC 2018** (International Residential Code)
- ✅ **IECC 2015** (International Energy Conservation Code)
- ✅ **NEC 2017** (National Electrical Code)
- ✅ **Georgia Amendments** (state-specific overrides)
- 🔄 **IBC, UBC, Canada NBC** (roadmap Q4 2025)

#### Finding Generation
- ✅ Deterministic rule evaluation (no ML randomness)
- ✅ Finding with violation description
- ✅ Code section citation (e.g., "IRC 2018 §302.1.1")
- ✅ Severity classification (Critical/Major/Info)
- ✅ Remediation guidance
- ✅ Photo/reference links
- ✅ Versioned history (track changes)

#### Output
```json
{
  "id": "finding-uuid",
  "project_id": "project-uuid",
  "code": "IRC_2018",
  "violation": "Windows not tempered safety glass",
  "section": "2406.1",
  "severity": "Critical",
  "remediation": "Install tempered glass or protective bars",
  "url": "https://codes.iccsafe.org/content/IRC2018/...",
  "quantity_affected": 12,
  "estimated_cost": 1200
}
```

---

### 3. **Intelligent Pricing & Estimation**

#### Data Sources
- ✅ **TradeBase Catalog** (materials, labor, equipment)
- ✅ **Regional Factors** (GA multiplier: 0.95-1.15 depending on market)
- ✅ **Spec Tier Matrices** (Standard/Premium/Luxury)
- ✅ **Trade-Specific Rules** (electrical OH&P ≠ carpentry OH&P)
- ✅ **Risk Contingency** (low-confidence items = +%)
- 🔄 **RSMeans Integration** (roadmap Q3 2025)
- 🔄 **Live Vendor Quotes** (roadmap Q3 2025)

#### Pricing Features
- ✅ Line-item detail (qty, unit, unit cost, extended)
- ✅ Overhead & Profit calculation (per trade)
- ✅ Contingency scoring based on confidence
- ✅ Alternate pricing (budget/deluxe options)
- ✅ Allowances & contingency buildup
- ✅ Multi-currency support (future)
- ✅ Version history (audit trail)

#### Output
```json
{
  "id": "estimate-uuid",
  "project_id": "project-uuid",
  "lines": [
    {
      "assembly": "Windows - Vinyl Double",
      "qty": 12,
      "unit": "EA",
      "unit_cost": 450,
      "extended": 5400
    },
    { "assembly": "Doors - Exterior", "qty": 4, "unit": "EA", "unit_cost": 850, "extended": 3400 }
  ],
  "subtotal": 8800,
  "overhead_pct": 10.0,
  "overhead_amt": 880,
  "profit_pct": 10.0,
  "profit_amt": 968,
  "contingency_pct": 5.0,
  "contingency_amt": 440,
  "total": 11088
}
```

---

### 4. **Proposal Generation & Export**

#### Formats
- ✅ **PDF** (branded, professional proposal)
- ✅ **CSV** (Xactimate-compatible format)
- ✅ **DOCX** (Word document for editing)
- ✅ **HTML** (for email, portal display)
- ✅ **JSON** (API consumption)

#### Template Features
- ✅ Custom branding (logos, colors, footers)
- ✅ Multi-page layouts (cover, findings, pricing, terms)
- ✅ Conditional sections (show findings only if > severity threshold)
- ✅ Dynamic calculations (subtotals, taxes, discounts)
- ✅ Jinja2 templating (advanced: loops, filters)
- ✅ Optional narrative polish (GPT-4 for executive summary)

#### Export Options
- ✅ One-click PDF download
- ✅ Email proposal to client
- ✅ Post to project portal (read-only)
- ✅ Archive with audit trail (MinIO)
- ✅ Webhook to external system (n8n)

---

### 5. **CRM & ERP Integration**

#### Odoo Integration
- ✅ Create/update CRM leads & opportunities
- ✅ Link estimates to quotations
- ✅ Sync projects & invoicing
- ✅ Post revenue to GL
- ✅ Two-way sync (updates flow both directions)

#### ERPNext Integration
- ✅ Multi-tenant support (different companies)
- ✅ Create sales orders from estimates
- ✅ Link to projects & billing
- ✅ Post journal entries (AR, revenue, COGS)
- ✅ Sync inventory (if materials come from ERP)

#### QuickBooks Integration (Future)
- 🔄 Post invoice & AR entry
- 🔄 Customer management sync
- 🔄 Trial balance sync

#### Procore/Buildertrend (Future)
- 🔄 Sync RFIs & submittals
- 🔄 Update project schedule
- 🔄 Lien document generation

**Example Workflow**: Upload plan → Parse → Generate estimate → Create Odoo quotation → Post AR in QB

---

### 6. **BIM & IFC Model Support**

#### IfcOpenShell Integration
- ✅ Upload IFC model (3D building information model)
- ✅ Automatic Quantity Takeoff (QTO) extraction
- ✅ Property extraction (U-factor, fire rating, materials)
- ✅ Geometry analysis (wall lengths, floor areas)
- ✅ High-confidence quantities (explicit model data)

#### Process
1. Upload .ifc file
2. IfcOpenShell service extracts geometry & properties
3. QTO feed into Parser Agent (bypass PDF parsing)
4. Generate estimate with model-derived quantities
5. Same compliance checks & pricing as PDF workflow

**Use Case**: General contractors with BIM models get instant estimates from floor plans + schedules

---

### 7. **Project Management & Versioning**

#### Projects
- ✅ Create project (name, address, jurisdiction, spec_tier)
- ✅ Upload multiple plan files (revisions)
- ✅ Track project status (draft → submitted → approved → invoiced)
- ✅ Add project metadata (client, general contractor, architect)
- ✅ RBAC (role-based access control)

#### Versioning & History
- ✅ Findings versioned (v1, v2, v3 on revisions)
- ✅ Estimates versioned (track price changes)
- ✅ Plan graphs cached (avoid re-parsing)
- ✅ Audit trail (who changed what, when)
- ✅ Comparison view (show deltas between versions)

#### Status Workflow
```
Draft → Submitted → In Review → Approved → Invoiced → Completed
  ↑                    ↓
  └──── Revisions ────┘
```

---

### 8. **User Interfaces**

#### Next.js Web Portal
- ✅ Project dashboard (list, create, filter)
- ✅ Upload page (drag-drop PDFs, IFC files)
- ✅ Live review (see findings as they generate)
- ✅ Pricing dashboard (interactive estimates)
- ✅ Proposal preview (before download)
- ✅ CSV export
- ✅ Client portal (read-only view, e-signature - future)

#### EagleEye.NET REST API
- ✅ All CRUD operations via HTTP
- ✅ OpenAPI/Swagger documentation
- ✅ Health checks (`GET /health`)
- ✅ Async job submission
- ✅ Webhook callbacks (plan ready, estimate ready, proposal ready)

#### Admin Interfaces
- ✅ Pricing management (TradeBase, regional factors, spec tiers)
- ✅ Code rule editor (custom GA amendments)
- ✅ Template management (Jinja2 proposals)
- ✅ Integration settings (Odoo, ERPNext credentials)
- ✅ User & team management

---

### 9. **Advanced Features (Optional/Roadmap)**

#### AI-Powered Enhancements
- 🔄 **Narrative Generation** (GPT-4 executive summary)
- 🔄 **Predictive Analytics** (cost overrun detection)
- 🔄 **Recommendation Engine** (suggest spec tier upgrades)
- 🔄 **Risk Scoring** (identify high-risk compliance areas)

#### Data Integrations
- 🔄 **RSMeans Overlay** (licensed pricing data)
- 🔄 **Vendor Live Quotes** (real-time material pricing)
- 🔄 **Market Index** (lumber futures, steel prices)
- 🔄 **Historical Database** (past project costs for benchmarking)

#### User Features
- 🔄 **Client Portal** (read-only, e-signature)
- 🔄 **Mobile App** (iOS/Android for site inspections)
- 🔄 **Draw Request Workflow** (GC submits, lender approves)
- 🔄 **Photo Log** (document deficiencies)
- 🔄 **Marketplace** (user-contributed rule packs)

---

## 🏗️ Full Infrastructure Stack

### Deployment Architecture

```yaml
Production Deployment (AWS Example):
  
  Load Balancer (ALB)
    ├─ NextJS Frontend (ECS Fargate)
    ├─ FastAPI API (ECS Fargate, auto-scale)
    ├─ Parser Service (ECS Fargate, GPU-enabled for Vision)
    ├─ Rules Service (ECS Fargate)
    ├─ Pricing Service (ECS Fargate)
    ├─ Reports Service (ECS Fargate)
    ├─ EagleEye.API (ECS Fargate)
    └─ MCP Server (ECS Fargate, long-running)
  
  Data Layer:
    ├─ PostgreSQL RDS (Multi-AZ)
    ├─ Redis ElastiCache (Multi-AZ)
    ├─ S3 (MinIO replacement in cloud)
    └─ SQS (job queue)
  
  Integrations:
    ├─ Odoo (self-hosted or cloud)
    ├─ ERPNext (self-hosted or cloud)
    └─ External APIs (RSMeans, vendors, markets)
  
  Monitoring:
    ├─ CloudWatch (logs, metrics)
    ├─ Datadog (optional, APM)
    ├─ Sentry (error tracking)
    └─ Health checks every 30s
```

### Docker Compose (Local Development)

```bash
docker compose up -d --build

Services:
  ✅ PostgreSQL (database)
  ✅ Redis (cache, queue)
  ✅ MinIO (S3-compatible storage)
  ✅ FastAPI (main API service)
  ✅ Parser Service (PDF → structured data)
  ✅ Rules Service (compliance checks)
  ✅ Pricing Service (cost calculations)
  ✅ Reports Service (PDF/CSV generation)
  ✅ MCP Server (agent orchestration)
  ✅ n8n (workflow automation)
  ✅ Next.js (frontend)
  ✅ Odoo (CRM - optional)
  ✅ IfcOpenShell (BIM QTO - optional)
  ✅ Seq (structured logging - optional)
```

---

## 🔄 Complete Example Workflow

### Scenario: Home Inspector Reviews Residential Plan

**Input**: Home inspector uploads plan PDF for a 2-story residential home, GA jurisdiction, Standard spec tier.

**Step 1: Coordinator Agent** 
- Reads: "Parse GA residential plan, check IRC/IECC/NEC, price Standard"
- Dispatches: Parser → Compliance → Pricing → Render

**Step 2: Parser Agent**
- Extracts: 12 windows, 4 doors, 2500 SF flooring, 1000 SF roofing
- Confidence: 95% (structured schedule)
- RFI: None needed
- Output: Plan graph + quantities → Redis cache

**Step 3: Compliance Agent**
- Loads: IRC 2018, IECC 2015, NEC 2017, GA Amendments
- Runs checks:
  - "Windows tempered?" → FAIL (not noted on schedule)
  - "Electrical panel placement?" → PASS (in utility room)
  - "Energy compliance?" → REVIEW (efficiency info missing)
- Output: 3 findings (1 Critical, 2 Info)

**Step 4: Pricing Agent**
- Looks up TradeBase: Windows (vinyl double) = $400 base
- Applies regional factor (GA = 1.00 for residential)
- Applies Standard spec tier (base rates)
- Calculates:
  - 12 windows × $400 = $4,800
  - 4 doors × $750 = $3,000
  - 2500 SF flooring × $8 = $20,000
  - 1000 SF roofing × $12 = $12,000
  - Subtotal: $39,800
  - OH&P (15% combined): $5,970
  - Contingency (2%, low risk): $800
  - **Total: $46,570**
- Output: Estimate object → PostgreSQL

**Step 5: Render Agent**
- Loads: Proposal_Residential.jinja2 template
- Populates: 3 findings, $46.5K estimate, GA contact info
- Polishes narrative (GPT-4): "Property has code violations requiring remediation"
- Generates: proposal.pdf (3 pages, branded)
- Exports: proposal.csv (for accounting)
- Archives: MinIO with audit trail
- Output: PDF URL + email link

**Step 6: Integration Agent** (Optional)
- Creates Odoo quotation (linked to prospect)
- Posts AR entry in QB
- Sync status: SUCCESS

**Result**: Inspector gets professional PDF proposal in 2 minutes. Client can accept/request changes. Workflow is fully versioned & audited.

---

## 🎯 Summary: What Makes Eagle Eye Powerful

| Feature | Capability | Status |
|---------|-----------|--------|
| **Plan Parsing** | Deterministic + optional AI vision | ✅ Full |
| **Code Compliance** | IRC/IECC/NEC + GA amendments | ✅ Full |
| **Pricing** | TradeBase + regional factors + spec tiers + OH&P | ✅ Full |
| **Proposal Generation** | PDF + CSV + DOCX + HTML + Xactimate export | ✅ Full |
| **CRM/ERP Integration** | Odoo, ERPNext, QB, Procore (roadmap) | ✅ Partial |
| **BIM Support** | IfcOpenShell QTO extraction | ✅ Full |
| **Versioning** | Complete audit trail for plans, findings, estimates | ✅ Full |
| **Multi-Code Support** | International Residential Code + IECC + NEC + GA | ✅ Full |
| **AI Orchestration** | 8-agent swarm (MCP + smolagents + n8n) | ✅ Ready |
| **Scalability** | Async/distributed, Kubernetes-ready | ✅ Full |
| **Production Grade** | Health checks, Serilog logging, Seq monitoring | ✅ Full |

---

## 📞 Support & Next Steps

### To Deploy This System:

1. **Local Dev**: `make all` (starts everything locally)
2. **Docker**: `docker compose up -d --build`
3. **Production**: See DEPLOYMENT.md (Kubernetes, AWS, Azure steps)
4. **API Only**: Use EagleEye.NET REST API for custom integrations

### To Add Custom Code Standards:
- Edit `services/rules/` (Georgia amendments example)
- Add to `infra/seeds/` CSV imports
- Restart rules service

### To Customize Pricing:
- Upload TradeBase changes to `infra/seeds/`
- Adjust regional factors per ZIP code
- Update OH&P policies per trade

This is a **complete, production-ready system** for construction plan review, compliance checking, and pricing estimation with enterprise integrations and agentic orchestration.

---

**Questions?** This document covers the full Eagle Eye ecosystem. Need details on any specific component?
