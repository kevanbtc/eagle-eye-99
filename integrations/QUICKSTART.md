# Quick Start: OSS Estimating Integrations

Choose your integration path based on your needs:

## 🚀 Option A: Odoo (Fastest - Recommended for MVP)

**Best for**: Teams who want a working estimator UI in hours

```bash
# 1. Start Eagle Eye core
cd eagle-eye-2
make up

# 2. Deploy Odoo + Connector
cd integrations/odoo
docker-compose up -d

# 3. Setup Odoo
# - Browse to http://localhost:8069
# - Create database: "eagle_odoo"
# - Install "Construction Estimator" from Apps
# - Go to Settings > Integrations > Eagle Eye
# - Enter Eagle Eye API URL: http://host.docker.internal:8000

# 4. Test workflow
# - Create estimate in Odoo
# - Click "Send to Eagle Eye" button
# - Review returns with code findings + adjusted pricing
# - Generate proposal PDF
```

**What you get**:
- ✅ Full estimating UI (line items, assemblies, quotes)
- ✅ PDF proposals with Eagle Eye code review
- ✅ Quote → Sales Order → Invoice workflow
- ✅ Customer portal for client approvals

**Caveats**:
- Some Construction Estimator modules are paid (check Odoo Apps marketplace)
- Community edition has basic reporting; upgrade for advanced features

---

## 🏗️ Option B: ERPNext (Best for Full Control)

**Best for**: Teams who need 100% OSS + deep customization

```bash
# 1. Clone Frappe Docker
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker

# 2. Configure for ERPNext
cp example.env .env
# Edit .env: ERPNEXT_VERSION=version-15

# 3. Deploy
docker-compose -f compose.yaml \
  -f overrides/compose.noproxy.yaml \
  -f overrides/compose.erpnext.yaml up -d

# 4. Initialize
docker-compose exec backend \
  bench new-site eagle.local --admin-password admin
docker-compose exec backend \
  bench --site eagle.local install-app erpnext

# 5. Import Eagle Eye custom doctypes
cd ../../eagle-eye-2/integrations/erpnext
# Follow README.md for custom doctype setup

# 6. Configure API
# - Login to http://localhost:8080
# - Settings > API > Generate Keys
# - Copy API key/secret to .env
```

**What you get**:
- ✅ 100% open source (AGPLv3)
- ✅ Full CRM (leads, opps, contacts)
- ✅ Job costing (track actuals vs estimates)
- ✅ Accounting (GL, AP, AR for draws)
- ✅ Python/JS customization

**Caveats**:
- Steeper learning curve than Odoo
- Custom doctypes require Python development
- Requires more server resources

---

## 📐 Option C: IfcOpenShell (For BIM/Model Workflows)

**Best for**: Teams with IFC models who want auto-QTO

```bash
# 1. Start IfcOpenShell service
cd eagle-eye-2/integrations/ifcopenshell
docker-compose up -d

# 2. Upload IFC file
curl -X POST http://localhost:5001/qto \
  -F "file=@/path/to/model.ifc" \
  -o quantities.json

# 3. Process through Eagle Eye
curl -X POST http://localhost:8000/api/parser/process \
  -H "Content-Type: application/json" \
  -d @quantities.json

# 4. Get estimate
curl http://localhost:8000/api/estimates/{project_id}
```

**What you get**:
- ✅ Auto-extract walls, windows, doors, slabs from IFC
- ✅ High confidence quantities (explicit model data)
- ✅ Properties (U-factor, fire rating, materials)
- ✅ Feeds directly into Eagle Eye pricing

**Caveats**:
- Requires IFC-compliant models (Revit, ArchiCAD, etc.)
- Quality depends on model detail/accuracy
- Doesn't replace plan review (still need code checks)

---

## 🔗 Option D: Hybrid (All Three)

**Best for**: Large teams with varied workflows

```bash
# 1. Start all services
cd eagle-eye-2
make up

cd integrations/ifcopenshell && docker-compose up -d
cd ../odoo && docker-compose up -d

# 2. Configure n8n workflows
# - Browse to http://localhost:5678
# - Import: workflows/n8n/multi-source-integration.json
# - Configure credentials for Odoo/ERPNext

# 3. Use cases:
# - Odoo: Quick estimates from takeoff sheets
# - ERPNext: Full project lifecycle (CRM → quote → job → billing)
# - IFC: Auto-QTO for BIM projects
# - All feed into Eagle Eye code review + pricing
```

**Workflow examples**:

```
1. BIM-First Project:
   Revit → IFC → IfcOpenShell → Eagle Eye → ERPNext → Job Costing

2. Plan Review Project:
   PDF → Manual Takeoff → Odoo Estimate → Eagle Eye → Proposal PDF

3. GC Bidding:
   Subcontractor quotes → ERPNext → Eagle Eye regional adjust → Bid package
```

---

## 🎯 Quick Decision Matrix

| Criteria | Odoo | ERPNext | IfcOpenShell |
|----------|------|---------|--------------|
| **Setup time** | 1 hour | 4 hours | 30 min |
| **OSS license** | LGPL (Community) | AGPLv3 | LGPL |
| **UI quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | N/A (API only) |
| **Customization** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **CRM built-in** | Yes | Yes | No |
| **Job costing** | Limited | Full | No |
| **BIM support** | No | No | Yes (IFC only) |
| **Best for** | Fast MVP | Full control | Auto-QTO |

---

## 📊 Integration Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Odoo     │     │   ERPNext   │     │ IFC Models  │
│ (Estimator) │     │ (CRM+Jobs)  │     │ (Revit/AC)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ XML-RPC           │ Frappe API        │ Upload
       ▼                   ▼                   ▼
┌────────────────────────────────────────────────────┐
│          Eagle Eye Integration Layer               │
│  (Odoo Connector / ERPNext API / IfcOpenShell)    │
└────────────────────┬───────────────────────────────┘
                     │
                     │ Normalized quantities
                     ▼
      ┌──────────────────────────────┐
      │      Eagle Eye MCP/n8n       │
      │      (Orchestration)         │
      └──────┬──────────────┬────────┘
             │              │
    ┌────────▼─────┐   ┌───▼────────┐
    │ Code Review  │   │  Regional  │
    │ (IRC/IECC)   │   │  Pricing   │
    └────────┬─────┘   └───┬────────┘
             │             │
             │             │
             ▼             ▼
      ┌──────────────────────────────┐
      │    Comprehensive Proposal    │
      │  (PDF + Xactimate CSV)       │
      └──────────────────────────────┘
             │
             │ Push back to source
             ▼
┌─────────────┐     ┌─────────────┐
│ Odoo Quote  │     │ ERPNext Job │
│   Updated   │     │   Created   │
└─────────────┘     └─────────────┘
```

---

## 🛠️ Next Steps

After choosing your integration:

1. **Configure webhooks** (Odoo/ERPNext → n8n)
2. **Map custom fields** (spec tier, CBSA code, etc.)
3. **Test end-to-end**:
   - Create estimate in source system
   - Trigger Eagle Eye processing
   - Verify findings + pricing
   - Generate proposal PDF
4. **Train team** on workflow
5. **Monitor RFI patterns** (low confidence items)
6. **Refine pricing** (update regional factors, spec tiers)

---

## 📚 Resources

- **Odoo**: https://apps.odoo.com/apps/modules/18.0/construction_estimator
- **ERPNext**: https://docs.erpnext.com/docs/user/manual/en/CRM
- **IfcOpenShell**: https://ifcopenshell.org/
- **Eagle Eye Docs**: `../README.md`
- **API Reference**: http://localhost:8000/docs (after `make up`)

---

## ⚙️ Troubleshooting

### Odoo connector fails
```bash
# Check Odoo is running
curl http://localhost:8069
# Check connector logs
docker logs eagle-odoo-connector
# Verify env vars
docker exec eagle-odoo-connector env | grep ODOO
```

### ERPNext API auth fails
```bash
# Regenerate API keys in ERPNext UI
# Update .env with new credentials
# Restart services
```

### IfcOpenShell crashes on upload
```bash
# Check IFC file is valid
# Try with smaller/simpler model first
# Check logs: docker logs eagle-ifcopenshell
```

### n8n workflow stuck
```bash
# Check all services running: docker ps
# Verify network connectivity: docker network inspect eagle-eye-2_default
# Check n8n logs: docker logs eagle-n8n
# Re-import workflow JSON
```
