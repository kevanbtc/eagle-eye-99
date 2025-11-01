# Eagle Eye Integrations

Open-source estimating & takeoff integrations for Eagle Eye plan review system.

## Available Integrations

### 1. ERPNext (Full OSS ERP)
- **Path**: `integrations/erpnext/`
- **Use Case**: Full CRM + estimating + job cost in one stack
- **Stack**: Frappe framework + ERPNext Construction/EPC module
- **Integration**: Custom doctypes for Eagle Eye estimates, bidirectional sync via MCP

### 2. Odoo Community (Fastest UI)
- **Path**: `integrations/odoo/`
- **Use Case**: Quick estimate-to-quote-to-SO workflow with polished PDFs
- **Stack**: Odoo Community + Construction Estimator modules
- **Integration**: REST API connector to Eagle Eye pricing engine

### 3. BlenderBIM / IfcOpenShell (BIM/QTO)
- **Path**: `integrations/ifcopenshell/`
- **Use Case**: Model-based quantity takeoff from IFC files
- **Stack**: IfcOpenShell + Python API for automated QTO
- **Integration**: Container service that feeds quantities to Eagle Eye parser

### 4. Easy-PDF-Takeoff (PDF Quantities)
- **Path**: `integrations/pdf-takeoff/`
- **Use Case**: Manual PDF takeoff helper (areas/lengths)
- **Stack**: Windows GUI tool with CSV export
- **Integration**: CSV import bridge to Eagle Eye quantities

## Quick Start Options

### Option A: Odoo Fast Track (Recommended for MVP)
```bash
cd integrations/odoo
docker-compose up -d
# Access Odoo at http://localhost:8069
# Install Construction Estimator module from Apps
# Configure Eagle Eye connector in Settings > Integrations
```

### Option B: ERPNext (Best for Full OSS Control)
```bash
cd integrations/erpnext
docker-compose up -d
# Access ERPNext at http://localhost:8080
# Run setup wizard, enable Construction module
# Import Eagle Eye custom doctypes
```

### Option C: IfcOpenShell (For BIM Workflows)
```bash
cd integrations/ifcopenshell
docker-compose up -d
# POST IFC file to http://localhost:5001/qto
# Receives JSON quantities for Eagle Eye parser
```

## Integration Architecture

```
┌─────────────────┐
│  ERPNext/Odoo   │
│   (Estimating)  │
└────────┬────────┘
         │ REST API / Frappe RPC
         ▼
┌─────────────────┐
│   MCP Server    │ ◄── Eagle Eye orchestrator
└────────┬────────┘
         │
    ┌────┴─────┬─────────┬─────────┐
    ▼          ▼         ▼         ▼
┌────────┐ ┌──────┐ ┌─────┐ ┌─────────┐
│ Parser │ │Rules │ │Price│ │ Reports │
└────────┘ └──────┘ └─────┘ └─────────┘
    ▲
    │ IFC → JSON quantities
    │
┌─────────────────┐
│ IfcOpenShell    │
│  (BIM QTO)      │
└─────────────────┘
```

## Field Mapping

All integrations map to Eagle Eye's shared schema:

| Eagle Eye Field | ERPNext Field | Odoo Field | IFC Property |
|-----------------|---------------|------------|--------------|
| `wbs` | `cost_code` | `analytic_account_id` | `IfcClassification` |
| `assembly` | `bom_name` | `product_tmpl_id.name` | `IfcElementType` |
| `line_item` | `description` | `name` | `IfcElement.Name` |
| `uom` | `stock_uom` | `product_uom` | `IfcQuantityArea.Unit` |
| `qty` | `qty` | `product_uom_qty` | `IfcQuantityArea.AreaValue` |
| `unit_cost` | `rate` | `price_unit` | Custom property |
| `ext_cost` | `amount` | `price_subtotal` | Calculated |

## Data Flow Examples

### 1. Odoo → Eagle Eye → Proposal PDF
```
1. Create estimate in Odoo Construction Estimator
2. Webhook triggers n8n workflow
3. n8n calls Eagle Eye MCP /process-estimate
4. Rules engine adds code compliance findings
5. Pricing engine applies regional factors + spec tiers
6. Reports service generates comprehensive proposal PDF
7. PDF/CSV pushed back to Odoo as attachment
```

### 2. IFC → IfcOpenShell → Eagle Eye → ERPNext
```
1. Upload IFC model to IfcOpenShell service
2. Auto-extract quantities (walls, windows, doors, floors)
3. POST quantities to Eagle Eye parser
4. Parser adds confidence scores
5. Pricing engine creates estimate
6. Sync estimate to ERPNext via Frappe API
7. PM reviews/adjusts in ERPNext UI
```

## Configuration

See each integration's README for detailed setup:
- [ERPNext Setup](./erpnext/README.md)
- [Odoo Setup](./odoo/README.md)
- [IfcOpenShell Setup](./ifcopenshell/README.md)
- [PDF Takeoff Bridge](./pdf-takeoff/README.md)
