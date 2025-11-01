from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Project
from ..schemas import ProjectIn, ProjectOut

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectOut)
def create_project(data: ProjectIn, db: Session = Depends(get_db)):
    obj = Project(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return ProjectOut(id=str(obj.id), status=obj.status, **data.model_dump())

@router.get("/", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    q = db.query(Project).all()
    return [ProjectOut(id=str(p.id), account_id=str(p.account_id), name=p.name, jurisdiction=p.jurisdiction, address=p.address, status=p.status) for p in q]
