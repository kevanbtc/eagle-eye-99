# Eagle Eye Web Platform - Setup & Deployment Guide

**Status**: 🚀 Ready for development  
**Stack**: Next.js 14 + React 18 + FastAPI + PostgreSQL  
**Estimated Setup Time**: 30 minutes

---

## Part 1: Quick Start (5 minutes)

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL 13+ (or Docker)
- Docker & Docker Compose

### Install & Run

#### 1. Frontend (Next.js)
```bash
cd apps/web
npm install
npm run dev
```
Frontend will be at `http://localhost:3000`

#### 2. Backend (FastAPI)
```bash
# In a new terminal
cd services/api
pip install -r requirements.txt
python main.py
```
Backend will be at `http://localhost:8000`

#### 3. Database
```bash
# Using Docker Compose
cd infra
docker-compose up -d
```
Database will be ready at `localhost:5432`

---

## Part 2: Frontend Features

### 1. Dashboard Page
**File**: `apps/web/src/app/(dashboard)/dashboard/page.tsx`

**Features**:
- Welcome message with user name
- 4 stat cards (Total Projects, Pending Estimates, Sent Proposals, Accepted)
- Recent projects list
- Quick action cards
- Getting started guide
- Activity feed

**How to customize**:
- Edit colors in stat cards
- Add new quick actions
- Modify welcome message

### 2. Projects Page
**File**: `apps/web/src/app/(dashboard)/projects/page.tsx` (to create)

**Features needed**:
- List all projects (table or card view)
- Filters (status, type, date)
- Search by name/address
- Create new project button
- Edit/delete actions
- Project details view

### 3. Estimate Builder
**File**: `apps/web/src/app/(dashboard)/estimates/[id]/page.tsx` (to create)

**Features needed**:
- Multi-step form
- Project selection
- Line item table
- Add/edit line items
- Upgrade selection
- Regional factor application
- Export options (PDF, Excel, CSV)

### 4. Upgrades Browser
**File**: `apps/web/src/app/(dashboard)/upgrades/page.tsx` (to create)

**Features needed**:
- Upgrade catalog grid
- Filter by category
- Search upgrades
- View details
- ROI calculator
- Add to project button
- Comparison view

### 5. Financial Analysis
**File**: `apps/web/src/app/(dashboard)/financial/[id]/page.tsx` (to create)

**Features needed**:
- Incentives calculator
- Financing comparison table
- 25-year cash flow chart
- ROI/IRR/NPV display
- Export analysis

### 6. Proposals
**File**: `apps/web/src/app/(dashboard)/proposals/page.tsx` (to create)

**Features needed**:
- Proposal list with status
- Template selection
- Customization options
- Preview before send
- Export/send options
- Tracking/analytics

---

## Part 3: Backend API Endpoints

### Create FastAPI Routes

#### File: `services/api/routes/projects.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

@router.post("")
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    return db_project

@router.get("")
async def list_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}")
async def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}")
async def update_project(project_id: str, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    return db_project

@router.delete("/{project_id}")
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}
```

#### File: `services/api/routes/estimates.py`

```python
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from services.pricing.developer_base import DeveloperBase
from app.models import Estimate, Project

router = APIRouter(prefix="/api/v1/estimates", tags=["estimates"])

@router.post("")
async def create_estimate(project_id: str, db: Session = Depends(get_db)):
    """Generate estimate for a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Use DeveloperBase to calculate
    base = DeveloperBase(
        building_type=project.buildingType,
        square_feet=project.squareFeet,
        zip_code=project.zipCode
    )
    
    baseline_cost = base.calculate_baseline()
    line_items = base.get_components()
    
    estimate = Estimate(
        projectId=project_id,
        baselineCost=baseline_cost,
        totalCost=baseline_cost,
        lineItems=line_items
    )
    
    db.add(estimate)
    db.commit()
    
    return estimate

@router.post("/{estimate_id}/export")
async def export_estimate(estimate_id: str, format: str = "pdf", db: Session = Depends(get_db)):
    """Export estimate as PDF, Excel, or CSV"""
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    # Use ReportGenerator to create file
    from proposal_generator import ReportGenerator
    
    report_gen = ReportGenerator()
    
    if format == "pdf":
        file_path = report_gen.generate_pdf(estimate)
    elif format == "excel":
        file_path = report_gen.generate_excel(estimate)
    elif format == "csv":
        file_path = report_gen.generate_csv(estimate)
    else:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    return {"file_path": file_path, "format": format}
```

#### File: `services/api/routes/upgrades.py`

```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models import Upgrade

router = APIRouter(prefix="/api/v1/upgrades", tags=["upgrades"])

@router.get("")
async def list_upgrades(category: str = Query(None), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List available upgrades, optionally filtered by category"""
    query = db.query(Upgrade)
    
    if category:
        query = query.filter(Upgrade.category == category)
    
    upgrades = query.offset(skip).limit(limit).all()
    return upgrades

@router.get("/catalog")
async def get_upgrade_catalog(db: Session = Depends(get_db)):
    """Get full upgrade catalog organized by category"""
    categories = {}
    upgrades = db.query(Upgrade).all()
    
    for upgrade in upgrades:
        if upgrade.category not in categories:
            categories[upgrade.category] = []
        categories[upgrade.category].append(upgrade)
    
    return categories

@router.post("/recommend")
async def recommend_upgrades(project_id: str, budget: float = None, db: Session = Depends(get_db)):
    """Get upgrade recommendations for a project"""
    from services.pricing.developer_base import DeveloperBase
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    base = DeveloperBase(
        building_type=project.buildingType,
        square_feet=project.squareFeet,
        zip_code=project.zipCode
    )
    
    # Get recommendations based on building type and budget
    recommendations = base.get_recommended_upgrades(budget)
    
    return recommendations
```

#### File: `services/api/routes/proposals.py`

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.models import Proposal, Estimate

router = APIRouter(prefix="/api/v1/proposals", tags=["proposals"])

@router.post("")
async def create_proposal(estimate_id: str, template: str, db: Session = Depends(get_db)):
    """Generate a proposal from an estimate"""
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    # Generate proposal based on template
    from proposal_generator import ProposalGenerator
    
    generator = ProposalGenerator()
    proposal_content = generator.generate(estimate, template)
    
    proposal = Proposal(
        estimateId=estimate_id,
        template=template,
        content=proposal_content,
        status="draft"
    )
    
    db.add(proposal)
    db.commit()
    
    return proposal

@router.post("/{proposal_id}/send")
async def send_proposal(proposal_id: str, email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Send proposal via email"""
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Add background task to send email
    background_tasks.add_task(send_email_task, proposal_id, email)
    
    proposal.status = "sent"
    proposal.sent_at = datetime.now()
    db.commit()
    
    return {"message": "Proposal sent", "proposal_id": proposal_id}

@router.post("/{proposal_id}/export")
async def export_proposal(proposal_id: str, format: str = "pdf", db: Session = Depends(get_db)):
    """Export proposal in various formats"""
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Export based on format
    from proposal_generator import ReportGenerator
    
    generator = ReportGenerator()
    
    if format == "pdf":
        file_path = generator.export_proposal_pdf(proposal)
    elif format == "html":
        file_path = generator.export_proposal_html(proposal)
    elif format == "excel":
        file_path = generator.export_proposal_excel(proposal)
    else:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    return {"file_path": file_path, "format": format}
```

---

## Part 4: Database Models

Create SQLAlchemy models in `services/api/models.py`:

```python
from sqlalchemy import Column, String, Float, Integer, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(String, index=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zipCode = Column(String)
    buildingType = Column(String)
    squareFeet = Column(Float)
    description = Column(String, nullable=True)
    status = Column(String, default="draft")
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Estimate(Base):
    __tablename__ = "estimates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    projectId = Column(String, ForeignKey("projects.id"))
    baselineCost = Column(Float)
    totalCost = Column(Float)
    regionalFactor = Column(Float, default=1.0)
    lineItems = Column(JSON)  # Store as JSON
    upgrades = Column(JSON)
    summary = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Proposal(Base):
    __tablename__ = "proposals"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    estimateId = Column(String, ForeignKey("estimates.id"))
    template = Column(String)
    title = Column(String)
    content = Column(String)
    status = Column(String, default="draft")
    sentAt = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    projectId = Column(String, ForeignKey("projects.id"))
    fileName = Column(String)
    type = Column(String)
    size = Column(Integer)
    url = Column(String)
    extractedData = Column(JSON, nullable=True)
    status = Column(String, default="uploaded")
    uploadedAt = Column(DateTime, default=datetime.utcnow)
```

---

## Part 5: Environment Configuration

### Frontend `.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Eagle Eye
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Backend `.env`
```
DATABASE_URL=postgresql://user:password@localhost:5432/eagle_eye
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=eagle-eye

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## Part 6: Deployment Options

### Option 1: Local Docker
```bash
docker-compose up -d
# Builds and runs frontend, backend, database, and MinIO
```

### Option 2: Vercel + Railway

**Frontend** (Vercel):
```bash
npm install -g vercel
vercel
# Follow prompts to deploy
```

**Backend** (Railway):
```bash
# Push code to GitHub
# Connect to Railway
# Add environment variables
# Deploy
```

**Database** (Railway):
- Create PostgreSQL instance
- Connect from backend

### Option 3: AWS + ECS

**Frontend** (CloudFront + S3):
```bash
npm run build
# Upload to S3
# Configure CloudFront
```

**Backend** (ECS Fargate):
- Create Docker image
- Push to ECR
- Create ECS task
- Setup load balancer

---

## Part 7: Testing

### Run Frontend Tests
```bash
npm test
```

### Run Backend Tests
```bash
pytest tests/
```

### Integration Testing
```bash
# Test full workflow
pytest tests/integration/
```

---

## Part 8: Monitoring & Analytics

### Frontend Monitoring
- Sentry: `npm install @sentry/nextjs`
- Google Analytics

### Backend Monitoring
- Prometheus metrics
- CloudWatch logs

### Error Tracking
- Sentry
- LogRocket

---

## Checklist: Getting Started

- [ ] Clone repository
- [ ] Install Node.js and Python
- [ ] Install dependencies: `npm install` and `pip install`
- [ ] Setup database connection
- [ ] Create `.env` files
- [ ] Start frontend: `npm run dev`
- [ ] Start backend: `python main.py`
- [ ] Visit `http://localhost:3000`
- [ ] Create test user account
- [ ] Create test project
- [ ] Generate estimate
- [ ] Create proposal
- [ ] Export and verify

---

## Next Steps

1. **Week 1**: Core CRUD operations (projects, estimates)
2. **Week 2**: Upgrade selection and ROI calculation
3. **Week 3**: Financial analysis and cash flow
4. **Week 4**: Document upload and AI extraction
5. **Week 5**: Proposal generation and email
6. **Week 6**: Team management and permissions
7. **Week 7**: Testing and optimization
8. **Week 8**: Production deployment

---

## Support & Troubleshooting

### Port Already in Use
```bash
# Find process using port 3000
lsof -i :3000
# Kill process
kill -9 <PID>
```

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -h localhost

# Check environment variables
echo $DATABASE_URL
```

### API Not Responding
```bash
# Check backend server
curl http://localhost:8000/docs

# Check logs
tail -f logs/app.log
```

---

**Your Eagle Eye platform is ready to deploy! Start building! 🚀**
