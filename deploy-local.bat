@echo off
REM ============================================================================
REM EAGLE EYE - LOCAL DEPLOYMENT (NO DOCKER)
REM ============================================================================
REM Simplified batch script to start Eagle Eye services locally
REM ============================================================================

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         EAGLE EYE - LOCAL DEPLOYMENT (PYTHON SERVICES)        ║
echo ║                                                                ║
echo ║  Bypassing Docker/WSL issues - running services directly      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    exit /b 1
)
echo [OK] Python found

REM Create virtual environment if needed
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)
echo [OK] Virtual environment ready

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install --quiet --upgrade pip
pip install --quiet fastapi uvicorn pydantic python-dotenv

REM Create services directory
if not exist services\api mkdir services\api

REM Create simple API service
(
echo from fastapi import FastAPI, UploadFile, File
echo from fastapi.responses import JSONResponse
echo from datetime import datetime
echo import uuid
echo import json
echo.
echo app = FastAPI(title="Eagle Eye API", version="1.0.0"^)
echo.
echo projects = {}
echo estimates = {}
echo.
echo @app.get("/health"^)
echo async def health(^):
echo     return {"status": "healthy", "service": "api", "timestamp": datetime.now().isoformat(^)}
echo.
echo @app.get("/"^)
echo async def root(^):
echo     return {
echo         "name": "Eagle Eye Estimating System",
echo         "status": "running",
echo         "mode": "local-development"
echo     }
echo.
echo @app.get("/projects"^)
echo async def get_projects(^):
echo     return {"projects": list(projects.values(^))}
echo.
echo @app.post("/projects"^)
echo async def create_project(data: dict^):
echo     project_id = str(uuid.uuid4(^)^)
echo     project = {
echo         "id": project_id,
echo         "client_name": data.get("client_name", "Client"^),
echo         "project_name": data.get("project_name", "Project"^),
echo         "created_at": datetime.now().isoformat(^)
echo     }
echo     projects[project_id] = project
echo     return project
echo.
echo @app.post("/analyze/{project_id}"^)
echo async def analyze_project(project_id: str, file: UploadFile = File(...^)^):
echo     estimate = {
echo         "id": str(uuid.uuid4(^)^),
echo         "project_id": project_id,
echo         "status": "completed",
echo         "analysis": {
echo             "components_found": 15,
echo             "total_cost": 52500.00,
echo             "labor_cost": 25000.00,
echo             "material_cost": 22000.00
echo         }
echo     }
echo     return estimate
echo.
echo if __name__ == "__main__":
echo     import uvicorn
echo     uvicorn.run(app, host="0.0.0.0", port=8000^)
) > services\api\app.py

echo [OK] API service created

REM Display summary
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                 EAGLE EYE - READY TO START!                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Starting API Gateway on port 8000...
echo.
echo After start, open your browser to:
echo   • http://localhost:8000/
echo   • http://localhost:8000/docs (interactive docs^)
echo.
echo Press Ctrl+C to stop
echo.

REM Start API
python services\api\app.py
