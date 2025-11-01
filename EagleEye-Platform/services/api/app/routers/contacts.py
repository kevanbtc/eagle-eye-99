from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Contact
from ..schemas import ContactIn, ContactOut

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactOut)
def create_contact(data: ContactIn, db: Session = Depends(get_db)):
    obj = Contact(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return ContactOut(**data.model_dump(), id=str(obj.id))

@router.get("/", response_model=list[ContactOut])
def list_contacts(db: Session = Depends(get_db)):
    q = db.query(Contact).all()
    return [ContactOut(id=str(c.id), account_id=str(c.account_id), name=c.name, email=c.email, phone=c.phone, role=c.role) for c in q]
