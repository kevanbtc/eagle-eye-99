from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db, Base, engine
from ..models import Account
from ..schemas import AccountIn, AccountOut

router = APIRouter(prefix="/accounts", tags=["accounts"])
Base.metadata.create_all(bind=engine)

@router.post("/", response_model=AccountOut)
def create_account(data: AccountIn, db: Session = Depends(get_db)):
    obj = Account(name=data.name, type=data.type)
    db.add(obj); db.commit(); db.refresh(obj)
    return AccountOut(id=str(obj.id), name=obj.name, type=obj.type)

@router.get("/", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    q = db.query(Account).all()
    return [AccountOut(id=str(a.id), name=a.name, type=a.type) for a in q]
