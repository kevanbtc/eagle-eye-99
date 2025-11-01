from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any

class AccountIn(BaseModel):
    name: str
    type: Optional[str] = None

class AccountOut(AccountIn):
    id: str

class ContactIn(BaseModel):
    account_id: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None

class ContactOut(ContactIn):
    id: str

class ProjectIn(BaseModel):
    account_id: str
    name: str
    jurisdiction: Optional[str] = None
    address: Optional[str] = None

class ProjectOut(ProjectIn):
    id: str
    status: str

class FindingOut(BaseModel):
    id: str
    severity: str
    discipline: str
    location: str
    code_citation: str
    impact: str
    recommendation: str
    ve_alt: Optional[str] = None

class EstimateOut(BaseModel):
    id: str
    project_id: str
    payload: Any
