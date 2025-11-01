#!/usr/bin/env powershell
# Eagle Eye Deployment Script
# This script handles all deployment tasks

param(
    [ValidateSet('local', 'staging', 'prod')]
    [string]$Environment = 'local',
    
    [switch]$BuildImages = $false,
    [switch]$ResetData = $false,
    [switch]$RunTests = $false,
    [switch]$Help = $false
)

$ErrorActionPreference = "Stop"

# Colors for output
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$Blue = "`e[34m"
$Reset = "`e[0m"

function Write-Success { Write-Host "$Green✅ $args$Reset" }
function Write-Warning { Write-Host "$Yellow⚠️  $args$Reset" }
function Write-Error-Custom { Write-Host "$Red❌ $args$Reset" }
function Write-Info { Write-Host "$Blue ℹ️  $args$Reset" }
function Write-Header { Write-Host "$Blue========================================$Reset"; Write-Host "$Blue$args$Reset"; Write-Host "$Blue========================================$Reset" }

function Show-Help {
    Write-Host @"
Eagle Eye Deployment Script

Usage:
    .\deploy.ps1 [Environment] [Options]

Environments:
    local       - Local development (Docker Compose)
    staging     - Staging environment (Docker Compose + networking)
    prod        - Production environment (requires cloud provider)

Options:
    -BuildImages    Build Docker images before deployment
    -ResetData      Reset database (WARNING: deletes all data)
    -RunTests       Run integration tests after deployment
    -Help          Show this help message

Examples:
    .\deploy.ps1 local
    .\deploy.ps1 local -BuildImages -RunTests
    .\deploy.ps1 staging -BuildImages

"@
}

if ($Help) {
    Show-Help
    exit 0
}

Write-Header "EAGLE EYE DEPLOYMENT SYSTEM"
Write-Info "Environment: $Environment"
Write-Info "Build Images: $BuildImages"
Write-Info "Reset Data: $ResetData"
Write-Info "Run Tests: $RunTests"

# Check prerequisites
function Check-Prerequisites {
    Write-Header "CHECKING PREREQUISITES"
    
    # Check Docker
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error-Custom "Docker is not installed. Please install Docker Desktop."
        exit 1
    }
    Write-Success "Docker installed: $(docker --version)"
    
    # Check Docker Compose
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Error-Custom "Docker Compose is not installed."
        exit 1
    }
    Write-Success "Docker Compose installed: $(docker-compose --version)"
    
    # Check .env file
    if (-not (Test-Path .env)) {
        Write-Warning ".env file not found. Copying from .env.deployment..."
        Copy-Item .env.deployment -Destination .env
        Write-Success ".env created"
    } else {
        Write-Success ".env file exists"
    }
    
    # Check required directories
    @('infra/db/seeds', 'infra/monitoring/grafana/dashboards', 'infra/monitoring/grafana/datasources') | ForEach-Object {
        if (-not (Test-Path $_)) {
            mkdir -p $_ | Out-Null
            Write-Success "Created directory: $_"
        }
    }
}

# Build Docker images
function Build-Images {
    Write-Header "BUILDING DOCKER IMAGES"
    
    Write-Info "Building parser service..."
    docker build -t eagle-eye/parser:latest ./services/parser
    Write-Success "Parser built"
    
    Write-Info "Building rules service..."
    docker build -t eagle-eye/rules:latest ./services/rules
    Write-Success "Rules built"
    
    Write-Info "Building pricing service..."
    docker build -t eagle-eye/pricing:latest ./services/pricing
    Write-Success "Pricing built"
    
    Write-Info "Building reports service..."
    docker build -t eagle-eye/reports:latest ./services/reports
    Write-Success "Reports built"
    
    Write-Info "Building API service..."
    docker build -t eagle-eye/api:latest ./services/api
    Write-Success "API built"
    
    Write-Info "Building web frontend..."
    docker build -t eagle-eye/web:latest ./apps/web
    Write-Success "Web built"
}

# Start services
function Start-Services {
    Write-Header "STARTING SERVICES"
    
    Write-Info "Starting Docker Compose stack..."
    docker-compose up -d
    
    Write-Info "Waiting for services to initialize..."
    Start-Sleep -Seconds 30
    
    # Check service status
    Write-Info "Verifying service health..."
    $services = @('postgres', 'redis', 'minio', 'parser', 'rules', 'pricing', 'reports', 'api', 'web')
    
    foreach ($service in $services) {
        $status = docker-compose ps $service | Select-String "Up"
        if ($status) {
            Write-Success "$service is running"
        } else {
            Write-Error-Custom "$service failed to start"
            docker-compose logs $service
            exit 1
        }
    }
}

# Reset database
function Reset-Database {
    Write-Header "RESETTING DATABASE"
    Write-Warning "This will delete ALL data!"
    
    $confirm = Read-Host "Are you sure? Type 'yes' to confirm"
    if ($confirm -ne 'yes') {
        Write-Info "Database reset cancelled"
        return
    }
    
    Write-Info "Stopping services..."
    docker-compose down -v
    
    Write-Info "Removing volumes..."
    docker volume rm eagle_eye_postgres_data 2>$null
    
    Write-Info "Restarting services..."
    docker-compose up -d
    Start-Sleep -Seconds 30
    
    Write-Success "Database reset complete"
}

# Run tests
function Run-Tests {
    Write-Header "RUNNING INTEGRATION TESTS"
    
    Write-Info "Testing service health..."
    
    $testResults = @{
        passed = 0
        failed = 0
    }
    
    # Test each service
    $services = @(
        @{ name = "API"; url = "http://localhost:8000/health" }
        @{ name = "Parser"; url = "http://localhost:8001/health" }
        @{ name = "Rules"; url = "http://localhost:8002/health" }
        @{ name = "Pricing"; url = "http://localhost:8003/health" }
        @{ name = "Reports"; url = "http://localhost:8004/health" }
    )
    
    foreach ($service in $services) {
        try {
            $response = curl -s -w "%{http_code}" -o /dev/null $service.url
            if ($response -eq 200) {
                Write-Success "✅ $($service.name) is healthy"
                $testResults.passed++
            } else {
                Write-Error-Custom "❌ $($service.name) returned $response"
                $testResults.failed++
            }
        } catch {
            Write-Error-Custom "❌ $($service.name) error: $_"
            $testResults.failed++
        }
    }
    
    # Test database
    Write-Info "Testing database connectivity..."
    try {
        $result = docker-compose exec -T postgres psql -U eagle_eye -d eagle_eye_db -c "SELECT COUNT(*) FROM projects;" 2>&1
        if ($result -match "\d+") {
            Write-Success "✅ Database is connected"
            $testResults.passed++
        }
    } catch {
        Write-Error-Custom "❌ Database error: $_"
        $testResults.failed++
    }
    
    # Summary
    Write-Header "TEST RESULTS"
    Write-Success "Passed: $($testResults.passed)"
    Write-Error-Custom "Failed: $($testResults.failed)"
    
    if ($testResults.failed -eq 0) {
        Write-Success "All tests passed!"
    } else {
        exit 1
    }
}

# Display status
function Show-Status {
    Write-Header "DEPLOYMENT STATUS"
    
    Write-Info "Container Status:"
    docker-compose ps
    
    Write-Info ""
    Write-Info "Service URLs:"
    Write-Info "  API:              http://localhost:8000"
    Write-Info "  Web UI:           http://localhost:3000"
    Write-Info "  Parser:           http://localhost:8001"
    Write-Info "  Rules:            http://localhost:8002"
    Write-Info "  Pricing:          http://localhost:8003"
    Write-Info "  Reports:          http://localhost:8004"
    Write-Info "  Database Admin:   http://localhost:8080"
    Write-Info "  MinIO Console:    http://localhost:9001"
    Write-Info "  Prometheus:       http://localhost:9090"
    Write-Info "  Grafana:          http://localhost:3001"
    
    Write-Info ""
    Write-Info "Default Credentials:"
    Write-Info "  Database:    eagle_eye / dev_password_123"
    Write-Info "  MinIO:       minioadmin / minioadmin123"
    Write-Info "  Grafana:     admin / admin"
}

# Main execution
try {
    Check-Prerequisites
    
    if ($ResetData) {
        Reset-Database
    }
    
    if ($BuildImages) {
        Build-Images
    }
    
    Start-Services
    
    if ($RunTests) {
        Run-Tests
    }
    
    Show-Status
    
    Write-Header "✅ DEPLOYMENT COMPLETE"
    Write-Success "Eagle Eye is ready to use!"
    Write-Info "Next step: Open http://localhost:3000 in your browser"
    
} catch {
    Write-Error-Custom "Deployment failed: $_"
    Write-Info "Check logs with: docker-compose logs"
    exit 1
}
