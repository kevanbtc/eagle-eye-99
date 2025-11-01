# Eagle Eye - AI Swarm Agent Roles & Responsibilities (Visual Guide)

## Quick Reference: Agent Roles at a Glance

```
USER UPLOAD PLAN PDF
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 🎯 COORDINATOR AGENT (Mission Planner)                      │
│    Reads: jurisdiction, modes (parse, rules, price)        │
│    Decides: agent sequence, retry logic, escalation        │
└────────────┬──────────────────────────────────────────────┘
             │
             ├──────────┬──────────┬──────────┬──────────┐
             │          │          │          │          │
             ▼          ▼          ▼          ▼          ▼
         ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
         │ PARSER │ │COMPLIANCE│ PRICING │ RENDER │ │QUALITY │
         │ AGENT  │ │ AGENT  │ │ AGENT  │ │ AGENT │ │ AGENT  │
         └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
             │          │          │          │          │
             └──────────┴──────────┴──────────┴──────────┘
                        │
                        ▼
            [Cache results in Redis]
                        │
                        ▼
            [Archive to MinIO + Email]
                        │
                        ▼
            PROPOSAL PDF READY
```

---

## Agent Interaction Matrix

```
                    PARSE    RULES    PRICE    RENDER   QA
┌──────────────────────────────────────────────────────────────┐
│ PARSE Agent       (X)      YES      YES      NO       YES    │
│                   └─ Sends quantities to Rules, Pricing       │
├──────────────────────────────────────────────────────────────┤
│ RULES Agent      YES       (X)      NO       YES      YES    │
│                   └─ Generates findings for Render + QA       │
├──────────────────────────────────────────────────────────────┤
│ PRICING Agent    YES       NO       (X)      YES      YES    │
│                   └─ Uses Parse quantities, Render uses est  │
├──────────────────────────────────────────────────────────────┤
│ RENDER Agent     NO        YES      YES      (X)      YES    │
│                   └─ Combines findings + pricing for PDF      │
├──────────────────────────────────────────────────────────────┤
│ QA Agent         YES       YES      YES      YES      (X)    │
│                   └─ Monitors all outputs, flags issues       │
└──────────────────────────────────────────────────────────────┘

KEY:
(X) = Self (agent owns this stage)
YES = Consumes input from
NO = Does not need
```

---

## AI Swarm Data Flow

```
INPUT: Plan PDF (bytes) + metadata (jurisdiction, spec_tier, modes)
  │
  ▼ Redis Queue: {project_id: {status: "parsing", ...}}
  
┌──────────────────────────────────────────────────────────────────┐
│ PARSER AGENT                                                     │
│ INPUT: PDF bytes from MinIO                                      │
│ PROCESS:                                                         │
│   1. pdfplumber.open(pdf) → extract tables, text, coordinates   │
│   2. Tesseract OCR for scanned regions                           │
│   3. Optional: SAM/Grounding DINO for walls/doors/windows      │
│   4. Build plan graph (sheets, cross-refs, confidence)          │
│ OUTPUT → Redis: plan:{project_id}:graph                         │
│          { sheets: [...], schedules: {...}, qty: {...}, meta }  │
│ STATUS: job:{project_id}:status = "parsing_complete"           │
└──────────────────────────────────────────────────────────────────┘
  │
  ▼ Coordinator checks Redis, spawns next agents
  
┌──────────────────────────────────────────────────────────────────┐
│ COMPLIANCE AGENT                                                 │
│ INPUT: plan graph from Redis + jurisdiction (GA)                │
│ PROCESS:                                                         │
│   1. Load rules from PostgreSQL (IRC/IECC/NEC/GA)              │
│   2. For each extracted quantity, run rule checks               │
│   3. Generate Finding objects (violation, ref, severity)        │
│   4. Cross-reference code sections from external API            │
│ OUTPUT → PostgreSQL: findings table                             │
│          [{code, violation, section, severity, ...}, ...]       │
│ CACHE → Redis: findings:{project_id}:v1                        │
│ STATUS: job:{project_id}:status = "compliance_complete"        │
└──────────────────────────────────────────────────────────────────┘
  │
  ▼ Coordinator checks Redis, spawns next agents
  
┌──────────────────────────────────────────────────────────────────┐
│ PRICING AGENT                                                    │
│ INPUT: plan graph from Redis + findings + spec_tier            │
│ PROCESS:                                                         │
│   1. For each quantity, lookup TradeBase rate (material+labor)  │
│   2. Apply regional factor (GA: 0.95-1.15 based on ZIP)        │
│   3. Match spec tier (Standard/Premium/Luxury)                  │
│   4. Calculate Overhead & Profit per trade                      │
│   5. Score contingency based on parse confidence               │
│   6. Build line items + summary                                 │
│ OUTPUT → PostgreSQL: estimates table                            │
│          {id, project_id, lines: [...], summary: {...}}         │
│ CACHE → Redis: estimate:{project_id}:v1                        │
│ STATUS: job:{project_id}:status = "pricing_complete"           │
└──────────────────────────────────────────────────────────────────┘
  │
  ▼ Coordinator checks Redis, spawns next agents
  
┌──────────────────────────────────────────────────────────────────┐
│ RENDER AGENT                                                     │
│ INPUT: findings + estimate + project metadata (all from Redis)  │
│ PROCESS:                                                         │
│   1. Select Jinja2 template (proposal_residential.j2)           │
│   2. Populate template context (findings, costs, terms)         │
│   3. Optional: GPT-4 polish narrative (exec summary)            │
│   4. Render Jinja2 → HTML                                       │
│   5. WeasyPrint HTML → PDF                                      │
│   6. Export CSV (Xactimate format)                              │
│   7. Upload artifacts to MinIO (audit trail)                    │
│ OUTPUT → Files in MinIO + links in PostgreSQL                  │
│          {proposal.pdf, proposal.csv, archive_metadata}         │
│ NOTIFY: Webhook callback to API → email user                   │
│ STATUS: job:{project_id}:status = "complete"                   │
└──────────────────────────────────────────────────────────────────┘
  │
  ▼ Quality Agent (runs in parallel, validates all outputs)
  
┌──────────────────────────────────────────────────────────────────┐
│ QUALITY AGENT (Monitoring Thread)                               │
│ INPUT: All Redis outputs (parse, findings, estimate, render)    │
│ PROCESS:                                                         │
│   1. Calculate aggregate confidence (avg of parse + price low-cf)│
│   2. Detect parsing anomalies (missing quantities, outliers)    │
│   3. Detect compliance mismatches (contradictions in findings)  │
│   4. Detect pricing outliers (cost per SF > 2σ from mean)      │
│   5. Detect loops (infinite retries)                            │
│   6. If issues found → flag for manual review                   │
│   7. If low confidence → recommend Vision Agent reparse        │
│ OUTPUT → PostgreSQL: quality_checks table                       │
│          {project_id, confidence, rfi_flags, recommendations}   │
│ ACTION: If critical → escalate to ops (email)                   │
│         If low-conf → optionally re-trigger Parser with Vision │
└──────────────────────────────────────────────────────────────────┘

FINAL OUTPUT:
  ├─ proposal.pdf (in MinIO)
  ├─ proposal.csv (in MinIO)
  ├─ findings[v1] (in PostgreSQL)
  ├─ estimate[v1] (in PostgreSQL)
  ├─ audit_log (all steps, timestamps, agent names)
  └─ user email (proposal is ready, click to download)
```

---

## Agent Invocation Patterns

### Pattern 1: Linear Pipeline (Standard)
```
User: "Parse and price this plan"
Coordinator: parse → (wait) → pricing → render
Time: ~30 seconds
Result: Estimate + PDF
```

### Pattern 2: Compliance-First (Code Review Focus)
```
User: "Check compliance for this plan"
Coordinator: parse → compliance → (wait)
Time: ~15 seconds
Result: Findings list (no pricing)
```

### Pattern 3: Vision Fallback (Low OCR Confidence)
```
Parser: "Confidence 45% on schedules (handwritten)"
Quality Agent: "Too low, trigger Vision"
Coordinator: vision_agent → reparse_with_vision → pricing
Time: ~60 seconds
Result: Higher confidence parsing → estimate
```

### Pattern 4: Full Suite (Compliance + Pricing + Render)
```
User: "Full review with proposal"
Coordinator: parse → compliance → pricing → render → (wait)
Parallel: quality_agent (monitoring)
Time: ~45 seconds
Result: Findings + Estimate + PDF + CSV
```

### Pattern 5: Integration Sync (CRM Update)
```
Coordinator: parse → compliance → pricing → render → (wait)
Integration Agent: create_odoo_quote → post_qbo_entry → (wait)
Final: Proposal + CRM quote linked + AR posted
Time: ~60 seconds
Result: Full end-to-end workflow
```

---

## Error Handling & Retry Logic

```
TRY: Agent executes task
  │
  ├─ SUCCESS → output to Redis/PostgreSQL, continue
  │
  ├─ TIMEOUT (>30 sec) → Retry 1x (exponential backoff)
  │                       If still timeout → escalate to ops
  │
  ├─ VALIDATION ERROR → Quality Agent triggered
  │                      Suggest fix (re-parse, manual entry)
  │                      Wait for human correction
  │
  ├─ MISSING DATA → Quality Agent flags RFI
  │                  Add to RFI list for client
  │                  Continue with defaults
  │
  └─ CATASTROPHIC ERROR → Stop pipeline
                           Log error in PostgreSQL
                           Email ops team
                           Flag project as "error"
```

---

## Agent Dependencies Graph

```
        ┌────────────────────────┐
        │ Coordinator Agent      │ (master orchestrator)
        │ (reads job params)     │
        └────────────┬───────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
         ▼                        ▼
    ┌─────────────┐          ┌─────────────┐
    │ Parser      │ ◄────┐   │ Vision      │
    │ Agent       │      └───│ Agent       │
    └──────┬──────┘          │ (optional)  │
           │                 └─────────────┘
           │
      [quantities + graph in Redis]
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────┐
│Compliance│  │ Pricing     │
│ Agent    │  │ Agent       │
│(rules)   │  │ (costs)     │
└────┬─────┘  └──────┬──────┘
     │               │
     │       ┌───────┘
     │       │
     └───┬───┴───┐
         │       │
         ▼       ▼
    ┌───────────────────┐
    │ Render Agent      │
    │ (PDF + CSV)       │
    └─────────┬─────────┘
              │
    [proposal in MinIO]
              │
              ▼
    ┌───────────────────┐
    │ Integration Agent │
    │ (optional: CRM)   │
    └───────────────────┘
```

---

## MCP Tools Reference (What Each Agent Calls)

### Parser Agent Tools
```python
mcp_parse_pdf(file_path: str) → {sheets, tables, text, coordinates}
mcp_ocr_image(image_bytes: bytes) → {text, confidence}
mcp_segment_image(image_bytes: bytes) → {masks, labels}  # SAM
mcp_detect_objects(image_bytes: bytes) → {boxes, labels}  # Grounding DINO
mcp_build_plan_graph(quantities: dict) → {sheets, refs, metadata}
```

### Compliance Agent Tools
```python
mcp_load_code_rules(code: str, jurisdiction: str) → {rules: [...]}
mcp_check_rule(rule: dict, quantities: dict) → {pass: bool, violations: [...]}
mcp_generate_finding(violation: str, code_ref: str) → Finding
mcp_cite_code(code: str, section: str) → {url, authority, text}
```

### Pricing Agent Tools
```python
mcp_lookup_rate(assembly: str, region: str, spec_tier: str) → {cost, unit}
mcp_apply_regional_factors(base_cost: float, region: str) → adjusted_cost
mcp_calculate_ohp(subtotal: float, trade: str) → {overhead, profit}
mcp_score_contingency(confidence: float, findings_count: int) → pct
mcp_generate_alternate(estimate: Estimate, mode: str) → Estimate
```

### Render Agent Tools
```python
mcp_render_jinja2(template: str, context: dict) → html
mcp_pdf_from_html(html: str, css: str) → pdf_bytes
mcp_polish_narrative(text: str, model: str) → polished_text  # GPT-4
mcp_export_csv(estimate: Estimate, format: str) → csv_bytes  # Xactimate
mcp_archive_to_minio(file_bytes: bytes, key: str) → {url, metadata}
```

### Quality Agent Tools
```python
mcp_calculate_confidence(parse_score: float, findings_count: int) → score
mcp_generate_rfi(missing_fields: list) → {questions, placeholders}
mcp_flag_for_review(reason: str, severity: str) → flag_id
mcp_suggest_actions(issue_type: str, context: dict) → [actions]
```

### Integration Agent Tools
```python
mcp_odoo_api(method: str, args: dict) → result  # xmlrpc
mcp_erpnext_api(method: str, args: dict) → result  # frappe
mcp_quickbooks_api(method: str, args: dict) → result  # OAuth + QBXML
mcp_sync_status(project_id: str) → {status, timestamp, errors}
```

---

## State Machine: Agent Orchestration

```
[START] ─────► job created in Redis
                    │
                    ▼
        ┌──────────────────────┐
        │ COORDINATOR READS    │
        │ job params           │
        │ (modes, jurisdiction)│
        └──────────┬───────────┘
                   │
            ┌──────▼──────┐
            │ All modes   │
            │ in request? │
            └──┬───┬──┬───┘
               │   │  │
         [parse] [rules] [price]
               │   │  │
               └───┴──┘
                   │
    ┌──────────────┴──────────────┐
    │ Dispatch to Agent Queue     │
    │ (Redis: agent_queue:parser)  │
    │        (agent_queue:comply)  │
    │        (agent_queue:price)   │
    └──────────┬──────────────────┘
               │
          [AGENTS WORKING]
               │
    ┌──────────┴──────────┐
    │ Poll Agent Status   │
    │ (every 5 seconds)   │
    └──────┬───────┬──────┘
           │       │
        SUCCESS  TIMEOUT
           │       │
           │   ┌───▼────────┐
           │   │ Retry Logic│
           │   │ Max 3x     │
           │   └───┬───────┘
           │       │
           │   SUCCESS
           │       │
           └───┬───┘
               │
         [Check All Done]
               │
           ┌───▼──────┐
           │ Render   │
           │ Agent    │
           └────┬─────┘
                │
            ┌───▼───────┐
            │ Archive   │
            │ to MinIO  │
            └────┬──────┘
                 │
            ┌────▼──────────┐
            │ Email User    │
            │ (proposal url)│
            └────┬──────────┘
                 │
              [DONE] ─────► Remove from job queue
```

---

## Example Inputs/Outputs

### Input: Job Submission
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_id": "plan-v1.pdf",
  "jurisdiction": "GA",
  "spec_tier": "Standard",
  "modes": ["parse", "compliance", "pricing", "render"],
  "client_email": "inspector@example.com",
  "callback_webhook": "https://webhook.site/12345"
}
```

### Output After Parser
```json
{
  "project_id": "550e8400-...",
  "plan_graph": {
    "sheets": [
      {"name": "A1", "type": "floor_plan", "areas": {...}},
      {"name": "A2", "type": "schedule", "items": [
        {"id": "W1", "type": "window", "qty": 12, "desc": "Vinyl Double", "confidence": 0.95}
      ]}
    ]
  },
  "confidence_score": 0.92,
  "rfi_flags": []
}
```

### Output After Compliance
```json
{
  "findings": [
    {
      "code": "IRC_2018",
      "violation": "Windows not tempered safety glass (Kitchen)",
      "section": "2406.1",
      "severity": "Critical",
      "url": "https://codes.iccsafe.org/2018/IRC-2/2406.1",
      "remediation": "Install tempered glass or protective bars",
      "quantity_affected": 12,
      "estimated_cost_to_fix": 1200
    }
  ],
  "compliance_score": 0.75,
  "total_findings": 3
}
```

### Output After Pricing
```json
{
  "estimate": {
    "lines": [
      {"assembly": "Windows - Vinyl Double", "qty": 12, "unit": "EA", "unit_cost": 450, "extended": 5400},
      {"assembly": "Doors - Exterior", "qty": 4, "unit": "EA", "unit_cost": 850, "extended": 3400}
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
}
```

### Final Output After Render
```json
{
  "proposal": {
    "pdf_url": "https://s3.minio/proposals/550e8400-.../proposal.pdf",
    "csv_url": "https://s3.minio/proposals/550e8400-.../proposal.csv",
    "email_sent_to": "inspector@example.com",
    "created_at": "2025-11-01T12:34:56Z",
    "archive_key": "archive/550e8400-.../2025-11-01-proposal-v1"
  }
}
```

---

## Monitoring & Observability

```
Serilog + Seq Integration:

Every agent logs:
├─ Agent start (project_id, mode)
├─ Tool call (tool_name, input, output, duration_ms)
├─ Milestones (parsing_complete, compliance_complete)
├─ Errors (exception, stack_trace, retry_count)
└─ Agent finish (project_id, duration_ms, status)

Seq Dashboard shows:
├─ Real-time agent activity
├─ Performance metrics (parse time, pricing time, etc.)
├─ Error rates by agent
├─ End-to-end workflow duration
└─ Alerts (timeouts, errors, escalations)
```

---

**This is the complete AI Swarm design for Eagle Eye!**

Each agent is independent but coordinated, enabling:
- Parallel execution where possible
- Graceful degradation (if one agent fails, others may continue)
- Full observability (every step logged)
- Deterministic + AI hybrid (fast parsing, smart decisions)
