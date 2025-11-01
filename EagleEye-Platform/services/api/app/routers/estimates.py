from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
from ..db import get_db
from ..models import Estimate, Finding

router = APIRouter(prefix="/estimates", tags=["estimates"])

@router.post("/{project_id}/quick")
def quick_estimate(project_id: str, db: Session = Depends(get_db)):
    # Minimal placeholder logic: create a tiny estimate and one sample finding
    payload = {
        "base": [{"ee_code":"EE-RBL-DW-HANG-001","uom":"SF","qty":1000,"unit":1.75,"ext":1750}],
        "alternates": [{"name":"Standing seam roof","amount":12000}],
        "allowances": [{"name":"Inspections/Testing","amount":500}],
        "summary": {"subtotal":14250, "op":0.10, "cont":0.05, "total":14250*1.15}
    }
    est = Estimate(project_id=project_id, payload=json.dumps(payload))
    db.add(est)
    f = Finding(project_id=project_id, severity="orange", discipline="Envelope", location="A1/Details-03", code_citation="IRC 2018 R703.4", impact="Moisture intrusion risk", recommendation="Add pan flashing & end dams at head/jamb", ve_alt="Factory-flashed unit")
    db.add(f)
    db.commit(); db.refresh(est)
    return {"estimate_id": str(est.id), "payload": payload}

@router.get("/{project_id}")
def get_latest_estimate(project_id: str, db: Session = Depends(get_db)):
    row = db.query(Estimate).filter(Estimate.project_id==project_id).order_by(Estimate.created_at.desc()).first()
    return {"estimate_id": str(row.id), "payload": json.loads(row.payload)} if row else {"estimate_id": None, "payload": None}

@router.get("/{project_id}/findings")
def list_findings(project_id: str, db: Session = Depends(get_db)):
    q = db.query(Finding).filter(Finding.project_id==project_id).all()
    return [{"id": str(x.id), "severity": x.severity, "discipline": x.discipline, "location": x.location, "code_citation": x.code_citation, "impact": x.impact, "recommendation": x.recommendation, "ve_alt": x.ve_alt} for x in q]
