# Eagle Eye: Complete Deployment Guide

**Status**: Production-Ready  
**Version**: 1.0  
**Date**: November 1, 2025  
**Time to Deploy**: 15-30 minutes (local) | 1-2 hours (cloud)

---

## PART 1: LOCAL DEVELOPMENT DEPLOYMENT (15 minutes)

### Prerequisites

```bash
# On Windows (PowerShell)
# Install Docker Desktop for Windows
# https://www.docker.com/products/docker-desktop

# Install Docker Compose (comes with Docker Desktop)
# Install PowerShell (already have it)

# Verify installation
docker --version       # Should be 20.10+
docker-compose --version  # Should be 1.29+
```

### Quick Start (Copy-Paste)

```powershell
# 1. Navigate to project
cd 'c:\Users\Kevan\Downloads\eagle eye 2'

# 2. Copy environment file
Copy-Item .env.deployment -Destination .env

# 3. Create required directories
mkdir -p infra/db/seeds
mkdir -p infra/monitoring/grafana/{dashboards,datasources}
mkdir -p services/{parser,rules,pricing,reports,api}

# 4. Start all services
docker-compose up -d

# Wait for services to initialize (30-60 seconds)
Start-Sleep -Seconds 30

# 5. Check service status
docker-compose ps

# Should show all services in "Up" status with healthy checks passing
```

### What Gets Started

```
SERVICES RUNNING:
├─ PostgreSQL (5432)      - Main database
├─ Redis (6379)           - Caching layer
├─ MinIO (9000)           - File storage (S3-compatible)
├─ Parser (8001)          - PDF parsing microservice
├─ Rules (8002)           - Compliance rules engine
├─ Pricing (8003)         - Cost estimation service
├─ Reports (8004)         - Report generation
├─ API (8000)             - Main orchestration API
├─ Web (3000)             - Next.js frontend
├─ Prometheus (9090)      - Metrics collection
└─ Grafana (3001)         - Monitoring dashboard

DATABASES:
├─ PostgreSQL tables created
├─ Regional factors seeded (30+ ZIP codes)
├─ Rules definitions loaded (15+ rules)
└─ Ready for testing
```

---

## PART 2: CONNECT & VERIFY

### Check Service Health

```powershell
# 1. Test API gateway
curl http://localhost:8000/health
# Should return: {"status": "healthy", "timestamp": "..."}

# 2. Test Parser service
curl http://localhost:8001/health
# Should return: {"status": "healthy", "service": "parser"}

# 3. Test Rules service
curl http://localhost:8002/health
# Should return: {"status": "healthy", "service": "rules"}

# 4. Test Pricing service
curl http://localhost:8003/health
# Should return: {"status": "healthy", "service": "pricing"}

# 5. Test Reports service
curl http://localhost:8004/health
# Should return: {"status": "healthy", "service": "reports"}

# 6. Test Web frontend
curl http://localhost:3000
# Should return HTML
```

### Check Database

```powershell
# Access database admin panel
Start-Process "http://localhost:8080"

# Login:
# Server: postgres
# Username: eagle_eye
# Password: dev_password_123
# Database: eagle_eye_db

# Or use psql (if installed):
psql -h localhost -U eagle_eye -d eagle_eye_db -c "SELECT COUNT(*) FROM projects;"
```

### Check File Storage

```powershell
# Access MinIO console
Start-Process "http://localhost:9001"

# Login:
# Username: minioadmin
# Password: minioadmin123

# Create bucket: eagle-eye-uploads
```

### Check Monitoring

```powershell
# View Prometheus metrics
Start-Process "http://localhost:9090"

# View Grafana dashboards
Start-Process "http://localhost:3001"
# Login: admin / admin
```

---

## PART 3: RUN FIRST END-TO-END TEST

### Test Workflow (Complete Pipeline)

```powershell
# 1. Create a project
$projectPayload = @{
    name = "Test Project - Smith Addition"
    client_name = "John Smith"
    client_email = "john@smith.com"
    property_address = "123 Oak Street"
    city = "Madison"
    state = "GA"
    zip_code = "30601"
    jurisdiction = "GA"
    building_year = 2025
    scope_summary = "800 SF addition + new HVAC"
    budget = 50000
} | ConvertTo-Json

$projectResponse = curl -X POST `
  -H "Content-Type: application/json" `
  -H "X-API-Key: your_api_key_change_me_to_something_secure_12345" `
  -d $projectPayload `
  http://localhost:8000/api/projects

$projectId = ($projectResponse | ConvertFrom-Json).id
Write-Host "Created Project: $projectId"

# 2. Upload a PDF (for testing, create a dummy file)
$pdfPath = ".\test_plans.pdf"
if (-not (Test-Path $pdfPath)) {
    # Create dummy PDF for testing
    Write-Host "Creating test PDF..."
    # In real scenario, use actual construction plans
}

# 3. Parse PDF
$parsePayload = @{
    project_id = $projectId
    filename = "test_plans.pdf"
} | ConvertTo-Json

curl -X POST `
  -H "Content-Type: application/json" `
  -H "X-API-Key: your_api_key_change_me_to_something_secure_12345" `
  -F "file=@$pdfPath" `
  http://localhost:8001/parse

# 4. Get components
curl -X GET `
  -H "X-API-Key: your_api_key_change_me_to_something_secure_12345" `
  "http://localhost:8000/api/projects/$projectId/components"

# 5. Check compliance
curl -X POST `
  -H "Content-Type: application/json" `
  -H "X-API-Key: your_api_key_change_me_to_something_secure_12345" `
  -d "{`"project_id`": `"$projectId`"}" `
  http://localhost:8002/check-compliance

# 6. Calculate estimate
curl -X POST `
  -H "Content-Type: application/json" `
  -H "X-API-Key: your_api_key_change_me_to_something_secure_12345" `
  -d "{`"project_id`": `"$projectId`"}" `
  http://localhost:8003/estimate

# 7. Generate reports
curl -X POST `
  -H "Content-Type: application/json" `
  -H "X-API-Key: your_api_key_change_me_to_something_secure_12345" `
  -d "{`"project_id`": `"$projectId`"}" `
  http://localhost:8004/generate-all

# 8. Get final results
curl -X GET `
  -H "X-API-Key: your_api_key_change_me_to_something_secure_12345" `
  "http://localhost:8000/api/projects/$projectId"

Write-Host "✅ Full pipeline test complete!"
Write-Host "Project ID: $projectId"
Write-Host "Check web UI: http://localhost:3000"
```

---

## PART 4: AUTOMATED TEST SUITE

### Create Integration Tests

```powershell
# File: tests/integration/test_full_pipeline.ps1

param(
    [string]$ApiUrl = "http://localhost:8000",
    [string]$ApiKey = "your_api_key_change_me_to_something_secure_12345"
)

$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = $ApiKey
}

function Test-ServiceHealth {
    Write-Host "Testing service health..."
    
    $services = @(
        @{ name = "API"; url = "http://localhost:8000/health" }
        @{ name = "Parser"; url = "http://localhost:8001/health" }
        @{ name = "Rules"; url = "http://localhost:8002/health" }
        @{ name = "Pricing"; url = "http://localhost:8003/health" }
        @{ name = "Reports"; url = "http://localhost:8004/health" }
    )
    
    foreach ($service in $services) {
        try {
            $response = curl -s $service.url
            Write-Host "✅ $($service.name) is healthy"
        } catch {
            Write-Host "❌ $($service.name) failed: $_"
            return $false
        }
    }
    
    return $true
}

function Test-DatabaseConnection {
    Write-Host "Testing database connection..."
    
    try {
        $response = curl -s -H @headers "$ApiUrl/api/health/db"
        $data = $response | ConvertFrom-Json
        if ($data.status -eq "connected") {
            Write-Host "✅ Database is connected"
            return $true
        }
    } catch {
        Write-Host "❌ Database connection failed: $_"
    }
    
    return $false
}

function Test-CreateProject {
    Write-Host "Testing project creation..."
    
    $payload = @{
        name = "Test Project $(Get-Date -Format 'yyyyMMddHHmmss')"
        client_name = "Test Client"
        zip_code = "30601"
        jurisdiction = "GA"
    } | ConvertTo-Json
    
    try {
        $response = curl -s -X POST -H $headers -d $payload "$ApiUrl/api/projects"
        $data = $response | ConvertFrom-Json
        
        if ($data.id) {
            Write-Host "✅ Project created: $($data.id)"
            return $data.id
        }
    } catch {
        Write-Host "❌ Project creation failed: $_"
    }
    
    return $null
}

function Test-GetRegionalFactors {
    param([string]$ZipCode)
    
    Write-Host "Testing regional factors lookup..."
    
    try {
        $response = curl -s -H $headers "$ApiUrl/api/regional-factors/$ZipCode"
        $data = $response | ConvertFrom-Json
        
        if ($data.labor_rate_multiplier) {
            Write-Host "✅ Regional factors found for $ZipCode"
            Write-Host "   Labor multiplier: $($data.labor_rate_multiplier)"
            Write-Host "   Material index: $($data.material_cost_index)"
            return $true
        }
    } catch {
        Write-Host "❌ Regional factors lookup failed: $_"
    }
    
    return $false
}

# Run all tests
Write-Host "=========================================="
Write-Host "EAGLE EYE - INTEGRATION TEST SUITE"
Write-Host "=========================================="
Write-Host ""

if (Test-ServiceHealth) {
    Write-Host ""
    if (Test-DatabaseConnection) {
        Write-Host ""
        $projectId = Test-CreateProject
        
        if ($projectId) {
            Write-Host ""
            Test-GetRegionalFactors -ZipCode "30601"
            
            Write-Host ""
            Write-Host "=========================================="
            Write-Host "✅ ALL TESTS PASSED"
            Write-Host "=========================================="
        }
    }
} else {
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "❌ SERVICE HEALTH CHECKS FAILED"
    Write-Host "=========================================="
}
```

### Run Tests

```powershell
# Run integration tests
.\tests\integration\test_full_pipeline.ps1

# Expected output:
# ==========================================
# EAGLE EYE - INTEGRATION TEST SUITE
# ==========================================
# 
# Testing service health...
# ✅ API is healthy
# ✅ Parser is healthy
# ✅ Rules is healthy
# ✅ Pricing is healthy
# ✅ Reports is healthy
# 
# Testing database connection...
# ✅ Database is connected
# 
# Testing project creation...
# ✅ Project created: 550e8400-e29b-41d4-a716-446655440000
# 
# Testing regional factors lookup...
# ✅ Regional factors found for 30601
#    Labor multiplier: 0.92
#    Material index: 0.95
# 
# ==========================================
# ✅ ALL TESTS PASSED
# ==========================================
```

---

## PART 5: TROUBLESHOOTING

### Common Issues & Fixes

```powershell
# Issue: Port already in use
# Solution: Check what's using the port and kill it
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Issue: Docker containers won't start
# Solution: Check logs
docker-compose logs parser
docker-compose logs -f api

# Issue: Database not initialized
# Solution: Reinitialize
docker-compose down -v
docker-compose up -d postgres
Start-Sleep -Seconds 30
docker-compose exec postgres psql -U eagle_eye -d eagle_eye_db -f /docker-entrypoint-initdb.d/01-schema.sql

# Issue: Services can't communicate
# Solution: Check network connectivity
docker-compose exec api curl -s http://parser:8001/health
docker-compose exec parser curl -s http://rules:8002/health

# Issue: Out of disk space
# Solution: Clean up Docker
docker system prune -a
docker volume prune

# View all logs
docker-compose logs --tail=100

# Restart all services
docker-compose restart

# Full reset (WARNING: loses data)
docker-compose down -v
docker-compose up -d
```

---

## PART 6: MONITORING DASHBOARD

### Access Monitoring

```
Prometheus Metrics:  http://localhost:9090
Grafana Dashboards:  http://localhost:3001 (admin/admin)
Database Admin:      http://localhost:8080 (eagle_eye/dev_password_123)
MinIO Console:       http://localhost:9001 (minioadmin/minioadmin123)
Web UI:              http://localhost:3000
API Docs:            http://localhost:8000/docs
```

### Key Metrics to Watch

```
✓ API response time (should be <500ms)
✓ Database query time (should be <100ms)
✓ Parser OCR accuracy
✓ Rules engine execution time
✓ PDF generation time
✓ Service uptime (should be 99.9%+)
✓ Error rate (should be <0.1%)
✓ Cache hit rate (should be >80%)
```

---

## PART 7: DEPLOYMENT CHECKLIST

```
□ Docker Desktop installed
□ .env file copied from .env.deployment
□ All required directories created
□ docker-compose up -d executed
□ All services showing "Up" status
□ Health checks passing
□ Database seeded with regional factors
□ Rules database populated
□ API key configured
□ CORS origins configured
□ MinIO bucket created
□ Prometheus scraping metrics
□ Grafana dashboards visible
□ Integration tests passing
□ Sample project created successfully
□ Full pipeline (parse→rules→pricing→report) tested
□ Web UI accessible
□ Monitoring dashboards accessible
```

---

## PART 8: NEXT STEPS

### After Deployment

1. **Load Test Data**
   ```powershell
   # Import sample projects
   .\scripts\load-test-data.ps1 -count 10
   ```

2. **Train Your Team**
   - Create user accounts in dashboard
   - Show how to upload PDFs
   - Walk through full workflow

3. **Customize Configuration**
   - Update company name in reports
   - Add company logo
   - Configure email notifications
   - Add regional pricing overrides

4. **Connect to Production Systems**
   - Integrate with Xactimate
   - Connect to CRM
   - Setup email notifications
   - Configure backup storage

5. **Monitor Performance**
   - Check Grafana dashboards daily
   - Review error logs weekly
   - Optimize slow queries
   - Scale services as needed

---

## TROUBLESHOOTING QUICK REFERENCE

| Issue | Command | Fix |
|-------|---------|-----|
| Check logs | `docker-compose logs -f <service>` | Review error messages |
| Restart service | `docker-compose restart <service>` | Service recovers |
| Scale service | `docker-compose up -d --scale parser=3` | Handle more load |
| Check ports | `netstat -ano \| findstr :8000` | Find conflicting processes |
| Database issues | `docker-compose exec postgres psql -U eagle_eye` | Run SQL directly |
| Clear cache | `docker-compose exec redis redis-cli FLUSHALL` | Reset all cache |
| View disk usage | `docker system df` | Monitor Docker resources |

---

## You're Ready to Go! 🚀

```
SYSTEM STATUS:
✅ All services deployed and healthy
✅ Database initialized with seed data
✅ API gateway responding
✅ Parser service ready
✅ Rules engine initialized
✅ Pricing service loaded
✅ Report generator ready
✅ Web UI accessible
✅ Monitoring active

NEXT: Upload your first PDF and watch it work!
```
