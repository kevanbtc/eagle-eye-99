# Integration Testing Guide

Complete guide for testing Eagle Eye OSS integrations (Odoo, ERPNext, IfcOpenShell).

---

## Prerequisites

Before running tests:

```bash
# 1. Start all services
cd eagle-eye-2
make all  # Starts core + integrations

# 2. Wait for services to be ready (30-60 seconds)
sleep 60

# 3. Verify services are running
docker ps
```

Expected containers:

- `eagle-db` (PostgreSQL)
- `eagle-minio` (Object storage)
- `eagle-redis` (Cache)
- `eagle-api` (Main API)
- `eagle-parser`, `eagle-rules`, `eagle-pricing`, `eagle-reports`
- `eagle-n8n` (Workflow engine)
- `eagle-ifcopenshell` (IFC QTO service)
- `eagle-odoo` (Odoo 17)
- `eagle-odoo-connector` (Odoo ↔ Eagle Eye bridge)

---

## Test Suite 1: Health Checks

### 1.1 Core Services Health

```bash
# Eagle Eye API
curl http://localhost:8000/health
# Expected: {"status":"ok","version":"1.0.0"}

# Parser service
curl http://localhost:8001/health
# Expected: {"status":"healthy","service":"parser"}

# Rules engine
curl http://localhost:8002/health
# Expected: {"status":"healthy","service":"rules"}

# Pricing service
curl http://localhost:8003/health
# Expected: {"status":"healthy","service":"pricing"}

# Reports service
curl http://localhost:8004/health
# Expected: {"status":"healthy","service":"reports"}
```

### 1.2 Integration Services Health

```bash
# IfcOpenShell QTO
curl http://localhost:5001/health
# Expected: {"status":"healthy","service":"ifcopenshell-qto","version":"0.7.0"}

# Odoo connector
curl http://localhost:5002/health
# Expected: {"status":"healthy","service":"odoo-connector","odoo_connected":false}
# Note: odoo_connected will be false until Odoo is configured

# n8n workflow engine
curl http://localhost:5678/healthz
# Expected: {"status":"ok"}
```

### 1.3 Data Layer Health

```bash
# PostgreSQL
docker exec eagle-db pg_isready -U eagle
# Expected: eagle-db:5432 - accepting connections

# Redis
docker exec eagle-redis redis-cli ping
# Expected: PONG

# MinIO
curl http://localhost:9000/minio/health/live
# Expected: 200 OK
```

**✅ Checkpoint**: All services should return healthy status

---

## Test Suite 2: IfcOpenShell Integration

### 2.1 Create Sample IFC File

If you don't have a test IFC, create a minimal one:

```python
# generate_test_ifc.py
import ifcopenshell
import ifcopenshell.api

model = ifcopenshell.api.run("project.create_file")
project = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcProject", name="Test Project")
context = ifcopenshell.api.run("context.add_context", model, context_type="Model")

# Create a simple wall
site = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSite", name="Site")
building = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuilding", name="Building")
storey = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Level 1")

wall = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcWall", name="Wall-001")

# Add quantity
qto = model.create_entity("IfcElementQuantity", Name="BaseQuantities")
area = model.create_entity("IfcQuantityArea", Name="NetSideArea", AreaValue=120.0)  # 120 m²
qto.Quantities = [area]
wall.IsDefinedBy = [model.create_entity("IfcRelDefinesByProperties", RelatingPropertyDefinition=qto)]

model.write("test_wall.ifc")
print("Created test_wall.ifc (120 m² wall)")
```

Run:

```bash
python generate_test_ifc.py
```

### 2.2 Test IFC Upload & QTO

```bash
# Upload IFC file
curl -X POST http://localhost:5001/qto \
  -F "file=@test_wall.ifc" \
  -o ifc_result.json

# View results
cat ifc_result.json | python -m json.tool
```

**Expected output**:

```json
{
  "success": true,
  "data": {
    "quantities": [
      {
        "element_type": "IfcWall",
        "name": "Wall-001",
        "wbs": "02.01",
        "assembly": "Wood Frame Wall",
        "item": "2x6 @ 16\" O.C.",
        "uom": "SF",
        "quantity": 1291.68,  // 120 m² × 10.764 = 1291.68 SF
        "trade": "Rough Carpentry",
        "category": "Framing",
        "confidence": "High",
        "properties": {
          "material": "Unknown",
          "thickness": null
        }
      }
    ],
    "metadata": {
      "total_elements": 1,
      "file_size_mb": 0.02
    },
    "summary": {
      "walls": 1,
      "windows": 0,
      "doors": 0
    }
  }
}
```

### 2.3 Test IFC → Eagle Eye Pipeline

```bash
# Send IFC quantities directly to Eagle Eye API
curl -X POST http://localhost:8000/api/estimates/process \
  -H "Content-Type: application/json" \
  -d @ifc_result.json

# Expected: {"estimate_id": 123, "status": "processing"}
```

**✅ Checkpoint**: IFC quantities extracted and converted to imperial units

---

## Test Suite 3: Odoo Integration

### 3.1 Configure Odoo (First-Time Setup)

```bash
# 1. Access Odoo
open http://localhost:8069

# 2. Create database
#    - Database name: eagle_odoo_test
#    - Email: admin@test.com
#    - Password: admin
#    - Country: United States
#    - Demo data: No

# 3. Install Construction Estimator module
#    - Go to Apps
#    - Search "construction estimator"
#    - Click Install
#    - Wait 1-2 minutes

# 4. Create test estimate
#    - Go to Construction > Estimates
#    - Click Create
#    - Partner: Create new "Test Client"
#    - Add lines:
#      * Product: "2x6 Wall Framing" | Qty: 1200 | Unit: SF | Price: 4.50
#      * Product: "Vinyl Windows" | Qty: 12 | Unit: EA | Price: 385.00
#      * Product: "Interior Doors" | Qty: 8 | Unit: EA | Price: 225.00
#    - Save (note the estimate ID)
```

### 3.2 Test Odoo → Eagle Eye Sync

```bash
# Sync estimate from Odoo to Eagle Eye
curl -X POST http://localhost:5002/sync/odoo-to-eagle \
  -H "Content-Type: application/json" \
  -d '{
    "estimate_id": 1,
    "project_name": "Test Project - Odoo Integration",
    "client_name": "Test Client"
  }' | python -m json.tool
```

**Expected output**:

```json
{
  "success": true,
  "odoo_estimate_id": 1,
  "eagle_eye_estimate_id": 456,
  "sync_summary": {
    "line_items_synced": 3,
    "total_quantity": 1220,
    "total_cost_odoo": 11020.00,
    "status": "processed"
  },
  "findings_count": 5,
  "pricing_adjustments": {
    "regional_factor_applied": true,
    "spec_tier": "Standard"
  }
}
```

### 3.3 Verify Sync in Eagle Eye

```bash
# Get estimate details
curl http://localhost:8000/api/estimates/456 | python -m json.tool

# Expected: Full estimate with code findings + regional pricing
```

### 3.4 Test Eagle Eye → Odoo Push Back

```bash
# Update Odoo estimate with Eagle Eye findings
curl -X POST http://localhost:5002/sync/eagle-to-odoo \
  -H "Content-Type: application/json" \
  -d '{
    "odoo_estimate_id": 1,
    "eagle_eye_estimate_id": 456,
    "update_pricing": true
  }' | python -m json.tool
```

**Expected output**:

```json
{
  "success": true,
  "odoo_estimate_id": 1,
  "findings_added": 5,
  "pricing_updated": true,
  "notes_added": "Eagle Eye Review: 5 findings (2 Red, 1 Orange, 2 Yellow)"
}
```

### 3.5 Verify in Odoo UI

```bash
# 1. Go back to Odoo estimate
# 2. Check "Internal Notes" field - should have Eagle Eye findings
# 3. Check line item prices - should be updated with regional factors
# 4. Verify total cost adjusted
```

**✅ Checkpoint**: Odoo ↔ Eagle Eye bidirectional sync working

---

## Test Suite 4: n8n Multi-Source Workflow

### 4.1 Import Workflow

```bash
# 1. Access n8n
open http://localhost:5678

# 2. Login (if prompted)
#    - User: admin (from N8N_BASIC_AUTH_USER env var)
#    - Password: <from N8N_BASIC_AUTH_PASSWORD>

# 3. Import workflow
#    - Click Workflows > Import from File
#    - Select: workflows/n8n/multi-source-integration.json
#    - Click Import

# 4. Configure credentials
#    - Click Settings > Credentials
#    - Add "Odoo" credential:
#      * Host: http://odoo:8069
#      * Database: eagle_odoo_test
#      * Username: admin@test.com
#      * Password: admin
#    - Add "Eagle Eye API" credential:
#      * Base URL: http://api:8000
#      * API Key: (leave empty for now, or set in .env)

# 5. Activate workflow
#    - Click "Inactive" toggle to "Active"
```

### 4.2 Test Webhook Trigger

```bash
# Trigger workflow with Odoo source
curl -X POST http://localhost:5678/webhook/estimate-process \
  -H "Content-Type: application/json" \
  -d '{
    "source": "odoo",
    "estimate_id": 1,
    "project_name": "Webhook Test Project",
    "client_email": "test@example.com"
  }' | python -m json.tool
```

**Expected output**:

```json
{
  "workflow_id": "abc123",
  "status": "processing",
  "estimate_id": 1,
  "eagle_eye_estimate_id": 789
}
```

### 4.3 Monitor Workflow Execution

```bash
# 1. Go to n8n UI
# 2. Click "Executions" tab
# 3. Click most recent execution
# 4. Verify all nodes executed successfully:
#    ✓ Webhook Trigger
#    ✓ Source Router (routed to Odoo branch)
#    ✓ Fetch Odoo Estimate
#    ✓ Normalize to Eagle Eye Format
#    ✓ Eagle Eye Parser (skipped - already have quantities)
#    ✓ Code Compliance Check
#    ✓ Regional Pricing
#    ✓ Generate Proposal PDF
#    ✓ Update Odoo Estimate
#    ✓ Generate Xactimate CSV
#    ✓ Email Notification
```

### 4.4 Verify Output Files

```bash
# Check MinIO for generated files
curl http://localhost:9000/eagle-reports/ \
  --user minioadmin:minioadmin

# Expected: List of PDFs and CSVs
# - proposal_789.pdf
# - xactimate_789.csv
```

**✅ Checkpoint**: Full n8n workflow executing end-to-end

---

## Test Suite 5: End-to-End Integration Flow

### 5.1 Complete IFC → Eagle Eye → Odoo Flow

```bash
# Step 1: Upload IFC to IfcOpenShell
curl -X POST http://localhost:5001/qto \
  -F "file=@test_wall.ifc" \
  -o ifc_quantities.json

# Step 2: Create Odoo estimate from IFC quantities
# (Manual step in Odoo UI - import line items)

# Step 3: Trigger n8n workflow
curl -X POST http://localhost:5678/webhook/estimate-process \
  -H "Content-Type: application/json" \
  -d '{
    "source": "ifc",
    "file_path": "/tmp/test_wall.ifc",
    "project_name": "IFC Integration Test",
    "client_email": "test@example.com"
  }'

# Step 4: Verify Odoo estimate updated
# (Check Odoo UI for findings and pricing)

# Step 5: Download proposal PDF
curl http://localhost:8000/api/reports/download/proposal_789.pdf \
  -o proposal.pdf

# Step 6: Verify PDF content
open proposal.pdf
# Expected: Comprehensive proposal with:
# - Section A: Executive Summary
# - Section B: Risk Register (code findings)
# - Section C: Detailed Code Analysis
# - Section F: Cost Estimate (IFC quantities + regional pricing)
# - Section H: Required Submittals
```

**✅ Checkpoint**: Complete multi-source integration working

---

## Test Suite 6: Error Handling

### 6.1 Test Invalid IFC File

```bash
# Create empty file
echo "invalid ifc data" > invalid.ifc

# Upload invalid IFC
curl -X POST http://localhost:5001/qto \
  -F "file=@invalid.ifc"

# Expected: {"success": false, "error": "Invalid IFC file format"}
```

### 6.2 Test Missing Odoo Estimate

```bash
# Try to sync non-existent estimate
curl -X POST http://localhost:5002/sync/odoo-to-eagle \
  -H "Content-Type: application/json" \
  -d '{"estimate_id": 99999}'

# Expected: {"success": false, "error": "Estimate not found in Odoo"}
```

### 6.3 Test Network Failure

```bash
# Stop Odoo temporarily
docker stop eagle-odoo

# Try to sync
curl -X POST http://localhost:5002/sync/odoo-to-eagle \
  -H "Content-Type: application/json" \
  -d '{"estimate_id": 1}'

# Expected: {"success": false, "error": "Cannot connect to Odoo"}

# Restart Odoo
docker start eagle-odoo
sleep 30  # Wait for Odoo to be ready
```

**✅ Checkpoint**: Error handling graceful, no crashes

---

## Test Suite 7: Performance & Load

### 7.1 Test Concurrent IFC Uploads

```bash
# Upload 5 IFC files simultaneously
for i in {1..5}; do
  curl -X POST http://localhost:5001/qto \
    -F "file=@test_wall.ifc" \
    -o "ifc_result_$i.json" &
done
wait

# Verify all completed successfully
for i in {1..5}; do
  echo "Result $i:"
  cat ifc_result_$i.json | python -m json.tool | grep success
done
```

### 7.2 Test Large IFC File

```bash
# (Requires actual large IFC model - skip if not available)
# Example: 500MB Revit model exported to IFC

curl -X POST http://localhost:5001/qto \
  -F "file=@large_building.ifc" \
  -o large_result.json

# Expected: Processing time 30-120 seconds
# Expected: Quantities for 100+ elements
```

### 7.3 Test Odoo Batch Sync

```bash
# Create 10 estimates in Odoo (manual or via script)
# Then sync all at once

for id in {1..10}; do
  curl -X POST http://localhost:5002/sync/odoo-to-eagle \
    -H "Content-Type: application/json" \
    -d "{\"estimate_id\": $id}" &
done
wait

# Verify all synced successfully
# Check database for 10 new estimates
docker exec eagle-db psql -U eagle -d eagle -c "SELECT COUNT(*) FROM estimates;"
```

**✅ Checkpoint**: System handles concurrent requests

---

## Automated Test Script

Run all tests with one command:

```bash
# Make executable
chmod +x integrations/test-integration.sh

# Run tests
./integrations/test-integration.sh
```

**Expected output**:

```
================================
Eagle Eye Integration Tests
================================

Test 1: Odoo Connector Health
✓ PASS: Odoo connector is healthy

Test 2: IfcOpenShell QTO Service Health
✓ PASS: IfcOpenShell service is healthy

Test 3: Eagle Eye API Health
✓ PASS: Eagle Eye API is healthy

...

================================
Test Summary
================================
Passed: 12
Failed: 0

All tests passed!

Next steps:
  1. Configure Odoo: http://localhost:8069
  2. Setup ERPNext: See integrations/erpnext/README.md
  3. Import n8n workflow: http://localhost:5678
  4. Test end-to-end: Upload estimate → Process → Generate proposal
```

---

## Troubleshooting

### Services won't start

```bash
# Check Docker logs
docker logs eagle-ifcopenshell
docker logs eagle-odoo-connector

# Common issues:
# - Port conflicts (8069, 5001, 5002 already in use)
# - Insufficient memory (need 16GB RAM minimum)
# - Missing environment variables (check .env file)
```

### IFC upload fails

```bash
# Verify IfcOpenShell installed
docker exec eagle-ifcopenshell python -c "import ifcopenshell; print(ifcopenshell.version)"

# Check file permissions
ls -la test_wall.ifc

# Verify file is valid IFC
head -n 5 test_wall.ifc
# Should see: ISO-10303-21;
```

### Odoo sync returns errors

```bash
# Verify Odoo database exists
docker exec eagle-odoo-db psql -U odoo -l

# Check Odoo connector logs
docker logs eagle-odoo-connector --tail 100

# Test Odoo API directly
curl -X POST http://localhost:8069/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "service": "common",
      "method": "version"
    },
    "id": 1
  }'
```

### n8n workflow stuck

```bash
# Check n8n logs
docker logs eagle-n8n --tail 100

# Verify webhook is registered
curl http://localhost:5678/webhook/estimate-process

# Restart n8n
docker restart eagle-n8n
sleep 10
```

---

## Test Data Cleanup

After testing, clean up test data:

```bash
# Truncate test estimates (keeps schema)
docker exec eagle-db psql -U eagle -d eagle -c "TRUNCATE estimates CASCADE;"

# Delete test files from MinIO
docker exec eagle-minio mc rm --recursive --force /data/eagle-reports/

# Reset Odoo test database
docker exec eagle-odoo-db psql -U odoo -c "DROP DATABASE eagle_odoo_test;"
docker exec eagle-odoo-db psql -U odoo -c "CREATE DATABASE eagle_odoo_test;"
```

---

## Continuous Testing

Set up automated testing:

```bash
# Create cron job (daily at 3 AM)
(crontab -l ; echo "0 3 * * * cd /opt/eagle-eye && ./integrations/test-integration.sh") | crontab -

# Run on every deployment
echo "./integrations/test-integration.sh" >> .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

---

**Testing complete!** 🎉

All integrations verified:

- ✅ IfcOpenShell: IFC → Quantities → Eagle Eye
- ✅ Odoo: Bidirectional sync working
- ✅ n8n: Multi-source workflow orchestrating
- ✅ Error handling: Graceful failures
- ✅ Performance: Handles concurrent requests

**Next**: Deploy to staging/production and onboard beta users!
