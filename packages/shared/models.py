"""
Shared Pydantic models for Eagle Eye services
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# Finding Models
class Finding(BaseModel):
    id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    finding_code: Optional[str] = Field(None, description="RR-101, EE-201, ME-301, GA-401, etc.")
    severity: str = Field(..., description="Red, Orange, or Yellow")
    discipline: str = Field(..., description="Structural, Envelope, Mechanical, etc.")
    location: str = Field(..., description="Sheet reference or location")
    code_citation: str = Field(..., description="IRC 2018 R602.10, etc.")
    consequence: str = Field(..., description="What happens if not fixed - schedule/cost impact")
    fix: str = Field(..., description="Specific fix recommendation")
    ve_alt: Optional[str] = Field(None, description="Value engineering alternative")
    evidence_refs: Optional[List[str]] = Field(default_factory=list, description="Sheet/page references")
    submittal_needed: Optional[str] = Field(None, description="Submittal requirement if applicable")
    # Legacy fields (deprecated but kept for compatibility)
    impact: Optional[str] = Field(None, description="DEPRECATED - use consequence")
    recommendation: Optional[str] = Field(None, description="DEPRECATED - use fix")
    evidence: Optional[Dict[str, Any]] = None
    status: str = "open"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Pricing Models
class LineItem(BaseModel):
    wbs: str = Field(..., description="Work Breakdown Structure code")
    assembly: str = Field(..., description="Assembly name")
    line_item: str = Field(..., description="Line item description")
    uom: str = Field(..., description="Unit of measure")
    qty: float = Field(..., description="Quantity")
    qty_confidence: Optional[str] = Field("Medium", description="High, Medium, or Low confidence in quantity")
    needs_rfi: Optional[bool] = Field(False, description="Flag for RFI if low confidence")
    unit_cost: float = Field(..., description="Unit cost")
    ext_cost: float = Field(..., description="Extended cost")
    notes: Optional[str] = None
    alt_group: Optional[str] = Field(None, description="Alternate group identifier")
    trade: Optional[str] = None
    confidence: Optional[str] = Field(None, description="High, Medium, Low - DEPRECATED, use qty_confidence")


class EstimateSummary(BaseModel):
    subtotal: float
    overhead_pct: float = 10.0
    profit_pct: float = 10.0
    overhead_amt: float
    profit_amt: float
    total: float
    contingency_pct: float = 5.0
    contingency_amt: float
    grand_total: float


class Estimate(BaseModel):
    id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    base: Dict[str, List[LineItem]] = Field(default_factory=dict)
    alternates: Dict[str, List[LineItem]] = Field(default_factory=dict)
    allowances: Dict[str, float] = Field(default_factory=dict)
    summary: Optional[EstimateSummary] = None
    version: int = 1
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None


# Project Models
class ProjectAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    county: Optional[str] = None


class Jurisdiction(BaseModel):
    state: str = "GA"
    county: Optional[str] = None
    municipality: Optional[str] = None
    code_set: str = "IRC2018_IECC2015_NEC2017_GA"


class Project(BaseModel):
    id: Optional[UUID] = None
    account_id: Optional[UUID] = None
    name: str
    address_json: Optional[Dict[str, Any]] = None
    jurisdiction: Optional[Jurisdiction] = None
    scope: Optional[str] = None
    spec_tier: Optional[str] = Field(None, description="Standard, Premium, Luxury")
    status: str = "draft"
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# File Models
class File(BaseModel):
    id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    name: str
    mime: Optional[str] = None
    s3_key: str
    sha256: Optional[str] = None
    kind: Optional[str] = Field(None, description="plan, photo, document, etc.")
    size_bytes: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


# Plan Graph Models
class PlanGraph(BaseModel):
    sheets: List[Dict[str, Any]] = Field(default_factory=list)
    schedules: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    quantities: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Regional Factor Models
class RegionalFactor(BaseModel):
    id: Optional[UUID] = None
    region: str
    labor_idx: float = 1.0
    material_idx: float = 1.0
    demo_idx: float = 1.0
    permit_idx: float = 1.0
    effective_dt: Optional[datetime] = None
