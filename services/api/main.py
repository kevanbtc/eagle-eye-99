"""
Eagle Eye API - Main FastAPI application
"""
from fastapi import FastAPI, UploadFile, Depends, HTTPException, File as FastAPIFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
import hashlib
import os

# Import shared models (in production, this would be from packages/shared)
import sys
sys.path.append("../../packages/shared")
from models import Project, Finding, Estimate, LineItem, File as FileModel

app = FastAPI(
    title="Eagle Eye API",
    description="Construction Plan Review & Pricing System",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5678"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database and S3 connections would be initialized here
# from db import get_db, init_db
# from storage import S3Client

# Pydantic models for API
class ProjectCreate(BaseModel):
    account_id: Optional[UUID] = None
    name: str
    address_json: Optional[Dict[str, Any]] = None
    jurisdiction: Optional[Dict[str, Any]] = None
    scope: Optional[str] = None
    spec_tier: Optional[str] = None


class RunPipelineRequest(BaseModel):
    modes: List[str] = ["parse", "rules", "price", "render"]


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Projects
@app.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    """Create a new project"""
    # In production: insert into database
    project_id = uuid4()
    return Project(
        id=project_id,
        **project.model_dump(),
        status="draft",
        created_at=datetime.utcnow()
    )


@app.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: UUID):
    """Get project by ID"""
    # In production: query from database
    raise HTTPException(status_code=404, detail="Project not found")


@app.get("/projects", response_model=List[Project])
async def list_projects(account_id: Optional[UUID] = None, skip: int = 0, limit: int = 100):
    """List all projects"""
    # In production: query from database with filters
    return []


# File uploads
@app.post("/projects/{project_id}/files", response_model=FileModel)
async def upload_file(project_id: UUID, file: UploadFile = FastAPIFile(...)):
    """Upload a plan file to a project"""
    # Read file content
    content = await file.read()
    
    # Compute SHA256
    sha256_hash = hashlib.sha256(content).hexdigest()
    
    # In production: upload to S3/MinIO
    s3_key = f"projects/{project_id}/files/{sha256_hash}/{file.filename}"
    
    # In production: save to database
    file_record = FileModel(
        id=uuid4(),
        project_id=project_id,
        name=file.filename or "untitled",
        mime=file.content_type,
        s3_key=s3_key,
        sha256=sha256_hash,
        kind="plan",
        size_bytes=len(content),
        created_at=datetime.utcnow()
    )
    
    return file_record


@app.get("/projects/{project_id}/files", response_model=List[FileModel])
async def list_files(project_id: UUID):
    """List all files for a project"""
    # In production: query from database
    return []


# Pipeline execution
@app.post("/projects/{project_id}/run")
async def run_pipeline(project_id: UUID, request: RunPipelineRequest):
    """Execute the review pipeline (parse, rules, price, render)"""
    # In production: enqueue tasks to Celery/Redis or call MCP tools
    return {
        "project_id": str(project_id),
        "queued": request.modes,
        "status": "processing"
    }


# Findings
@app.get("/projects/{project_id}/findings", response_model=List[Finding])
async def get_findings(
    project_id: UUID,
    severity: Optional[str] = None,
    discipline: Optional[str] = None
):
    """Get code compliance findings for a project"""
    # In production: query from database with filters
    return []


@app.post("/projects/{project_id}/findings", response_model=Finding)
async def create_finding(project_id: UUID, finding: Finding):
    """Create a new finding"""
    # In production: insert into database
    finding.id = uuid4()
    finding.project_id = project_id
    finding.created_at = datetime.utcnow()
    return finding


@app.patch("/projects/{project_id}/findings/{finding_id}")
async def update_finding(project_id: UUID, finding_id: UUID, updates: Dict[str, Any]):
    """Update a finding (e.g., status change)"""
    # In production: update in database
    return {"id": str(finding_id), **updates}


# Estimates
@app.get("/projects/{project_id}/estimate", response_model=Estimate)
async def get_estimate(project_id: UUID, version: Optional[int] = None):
    """Get the pricing estimate for a project"""
    # In production: query from database
    raise HTTPException(status_code=404, detail="Estimate not found")


@app.post("/projects/{project_id}/estimate", response_model=Estimate)
async def create_estimate(project_id: UUID, estimate: Estimate):
    """Create or update an estimate"""
    # In production: insert/update in database
    estimate.id = uuid4()
    estimate.project_id = project_id
    estimate.created_at = datetime.utcnow()
    return estimate


# Reports
@app.get("/projects/{project_id}/reports")
async def get_reports(project_id: UUID):
    """Get URLs for generated reports"""
    # In production: return signed S3 URLs
    return {
        "proposal_pdf": f"s3://eagle-files/projects/{project_id}/reports/proposal.pdf",
        "lender_summary_pdf": f"s3://eagle-files/projects/{project_id}/reports/lender_summary.pdf",
        "xactimate_csv": f"s3://eagle-files/projects/{project_id}/reports/xactimate.csv",
    }


@app.post("/projects/{project_id}/reports/generate")
async def generate_reports(project_id: UUID, report_types: List[str]):
    """Trigger report generation"""
    # In production: call reports service
    return {
        "project_id": str(project_id),
        "report_types": report_types,
        "status": "generating"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
