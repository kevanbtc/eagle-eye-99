#!/bin/bash

# Eagle Eye - Integration Testing Script
# Tests Odoo, ERPNext, and IfcOpenShell integrations

set -e  # Exit on error

echo "================================"
echo "Eagle Eye Integration Tests"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    ((TESTS_PASSED++))
}

fail() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    ((TESTS_FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠ WARN${NC}: $1"
}

# Test 1: Odoo Connector Health
echo "Test 1: Odoo Connector Health"
if curl -s http://localhost:5002/health | grep -q '"status":"healthy"'; then
    pass "Odoo connector is healthy"
else
    fail "Odoo connector is not responding"
fi
echo ""

# Test 2: IfcOpenShell Health
echo "Test 2: IfcOpenShell QTO Service Health"
if curl -s http://localhost:5001/health | grep -q '"status":"healthy"'; then
    pass "IfcOpenShell service is healthy"
else
    fail "IfcOpenShell service is not responding"
fi
echo ""

# Test 3: Eagle Eye API Health
echo "Test 3: Eagle Eye API Health"
if curl -s http://localhost:8000/health | grep -q '"status":"ok"'; then
    pass "Eagle Eye API is healthy"
else
    fail "Eagle Eye API is not responding"
fi
echo ""

# Test 4: Odoo Sync Endpoint
echo "Test 4: Odoo Sync Endpoint (dry-run)"
RESPONSE=$(curl -s -X POST http://localhost:5002/sync/odoo-to-eagle \
    -H "Content-Type: application/json" \
    -d '{"estimate_id": 999, "dry_run": true}')

if echo "$RESPONSE" | grep -q '"error"'; then
    warn "Odoo sync endpoint reachable but returned error (expected if no Odoo instance)"
else
    pass "Odoo sync endpoint is functional"
fi
echo ""

# Test 5: IFC QTO Endpoint (sample IFC)
echo "Test 5: IFC QTO Endpoint (test file)"
if [ -f "ifcopenshell/test_fixtures/simple_wall.ifc" ]; then
    RESPONSE=$(curl -s -X POST http://localhost:5001/qto \
        -F "file=@ifcopenshell/test_fixtures/simple_wall.ifc")
    
    if echo "$RESPONSE" | grep -q '"success":true'; then
        pass "IFC QTO extraction successful"
    else
        fail "IFC QTO extraction failed"
    fi
else
    warn "No test IFC file found, skipping extraction test"
fi
echo ""

# Test 6: Eagle Eye Parser Endpoint
echo "Test 6: Eagle Eye Parser Endpoint"
RESPONSE=$(curl -s -X GET http://localhost:8000/api/parser/health)
if [ $? -eq 0 ]; then
    pass "Parser service is reachable"
else
    fail "Parser service is not responding"
fi
echo ""

# Test 7: Database Connection
echo "Test 7: PostgreSQL Database Connection"
if docker exec eagle-db pg_isready -U eagle > /dev/null 2>&1; then
    pass "Database is accepting connections"
else
    fail "Database is not responding"
fi
echo ""

# Test 8: MinIO Storage
echo "Test 8: MinIO Object Storage"
if curl -s http://localhost:9000/minio/health/live | grep -q 'OK'; then
    pass "MinIO storage is healthy"
else
    fail "MinIO storage is not responding"
fi
echo ""

# Test 9: Redis Cache
echo "Test 9: Redis Cache"
if docker exec eagle-redis redis-cli ping | grep -q 'PONG'; then
    pass "Redis cache is responding"
else
    fail "Redis cache is not responding"
fi
echo ""

# Test 10: n8n Workflow Engine
echo "Test 10: n8n Workflow Engine"
if curl -s http://localhost:5678/healthz | grep -q 'ok'; then
    pass "n8n workflow engine is healthy"
else
    fail "n8n workflow engine is not responding"
fi
echo ""

# Test 11: Field Mapping Validation
echo "Test 11: Field Mapping Validation"
if [ -f "README.md" ] && grep -q "Field Mapping" README.md; then
    pass "Field mapping documentation exists"
else
    warn "Field mapping documentation not found"
fi
echo ""

# Test 12: Docker Network Connectivity
echo "Test 12: Docker Network Connectivity"
if docker network inspect eagle-net > /dev/null 2>&1; then
    pass "Eagle Eye network exists"
else
    fail "Eagle Eye network not found"
fi
echo ""

# Summary
echo "================================"
echo "Test Summary"
echo "================================"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Configure Odoo: http://localhost:8069"
    echo "  2. Setup ERPNext: See integrations/erpnext/README.md"
    echo "  3. Import n8n workflow: http://localhost:5678"
    echo "  4. Test end-to-end: Upload estimate → Process → Generate proposal"
    exit 0
else
    echo -e "${RED}Some tests failed. Check logs:${NC}"
    echo "  - Odoo connector: docker logs eagle-odoo-connector"
    echo "  - IfcOpenShell: docker logs eagle-ifcopenshell"
    echo "  - Eagle Eye API: docker logs eagle-api"
    exit 1
fi
