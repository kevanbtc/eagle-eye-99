"""
NEC 2017 Electrical Rules
Load calculations, AFCI/GFCI, EV readiness, smoke/CO
"""
import sys
sys.path.append("../../packages/shared")
from models import Finding
from typing import List, Dict, Any


def article_210_receptacles(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    NEC 2017 210.52 - Receptacle Outlet Requirements
    Wall outlets max 12ft spacing; GFCI requirements
    """
    findings = []
    
    # Look for electrical plans
    electrical_sheets = [
        sheet for sheet in plan_graph.get("sheets", [])
        if sheet.get("sheet_type") == "electrical"
    ]
    
    if not electrical_sheets:
        findings.append(Finding(
            finding_code="ME-301",
            severity="Yellow",
            discipline="Electrical",
            location="Electrical plans",
            code_citation="NEC 2017 210.52",
            consequence="Code corrections during rough-in; failed inspection",
            fix="Provide electrical plans showing receptacle locations. Verify 12ft max spacing per NEC 210.52(A). Mark GFCI-protected circuits (bathrooms, kitchens, outdoors, garage).",
            ve_alt=None,
            evidence_refs=["Electrical floor plans"],
            submittal_needed="Electrical plans with receptacle layout"
        ))
    
    return findings


def article_210_afci_requirements(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    NEC 2017 210.12 - AFCI Protection
    Required for dwelling unit branch circuits
    """
    findings = []
    
    has_afci_spec = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "AFCI" in text or "ARC FAULT" in text:
            has_afci_spec = True
            break
    
    if not has_afci_spec:
        findings.append(Finding(
            finding_code="ME-302",
            severity="Yellow",
            discipline="Electrical/Safety",
            location="Panel schedule / notes",
            code_citation="NEC 2017 210.12",
            consequence="AFCI breaker requirement missed; panel/breaker corrections",
            fix="Specify AFCI breakers for dwelling unit 15/20A circuits (bedrooms, living, etc.). Note combination AFCI or panel with AFCI breakers.",
            ve_alt=None,
            evidence_refs=["Panel schedule"],
            submittal_needed="Panel schedule with AFCI breakers noted"
        ))
    
    return findings


def article_220_load_calculation(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    NEC 2017 220 - Branch-Circuit, Feeder, and Service Calculations
    Check for load calc and service size
    """
    findings = []
    
    has_load_calc = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "LOAD CALC" in text or "SERVICE" in text and "AMP" in text:
            has_load_calc = True
            break
    
    if not has_load_calc:
        findings.append(Finding(
            finding_code="ME-303",
            severity="Orange",
            discipline="Electrical/Load",
            location="Electrical notes / panel schedule",
            code_citation="NEC 2017 220",
            consequence="Service size unclear; potential undersizing with EV/HVAC loads",
            fix="Provide load calculation per NEC 220 (general lighting, appliances, HVAC, EV if applicable). Specify service size (typically 200A for modern SFR).",
            ve_alt="Consider 200A service minimum for future EV/solar readiness",
            evidence_refs=["Electrical notes"],
            submittal_needed="NEC 220 load calculation"
        ))
    
    return findings


def article_625_ev_charging(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    NEC 2017 625 - Electric Vehicle Charging
    Check for EV circuit/conduit provision
    """
    findings = []
    
    has_ev_provision = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "EV" in text or "ELECTRIC VEHICLE" in text or "EVSE" in text or "CHARGING" in text:
            has_ev_provision = True
            break
    
    # If not mentioned, recommend as future-proofing
    if not has_ev_provision:
        findings.append(Finding(
            finding_code="ME-304",
            severity="Yellow",
            discipline="Electrical/EV",
            location="Garage / panel schedule",
            code_citation="NEC 2017 625 (future-proofing recommendation)",
            consequence="No EV charging readiness; costly retrofit later",
            fix="Pre-wire EV circuit: 240V/50A dedicated circuit to garage with 6 AWG in 1\" conduit. Update load calc and panel schedule.",
            ve_alt="Minimum: conduit stub for future EV circuit pull",
            evidence_refs=["Garage plan", "Panel schedule"],
            submittal_needed="EV circuit on panel schedule; update load calc"
        ))
    
    return findings


def irc_r315_smoke_co_detectors(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IRC 2018 R315 - Carbon Monoxide & Smoke Alarms
    (Part of NEC/Life Safety integration)
    """
    findings = []
    
    has_co_spec = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "CO" in text or "CARBON MONOXIDE" in text or "SMOKE" in text:
            has_co_spec = True
            break
    
    if not has_co_spec:
        findings.append(Finding(
            finding_code="ME-305",
            severity="Yellow",
            discipline="MEP/Life Safety",
            location="Electrical plans / general notes",
            code_citation="IRC 2018 R315; NEC integration",
            consequence="CO/smoke detector placement missing; final inspection hold",
            fix="Show CO detector locations (outside sleeping areas, each level). Show smoke alarm locations (bedrooms, hallways, each level). Specify interconnected hardwired with battery backup.",
            ve_alt=None,
            evidence_refs=["Electrical plans", "Life safety notes"],
            submittal_needed="CO/smoke detector plan"
        ))
    
    return findings


def run_nec_2017_checks(plan_graph: Dict[str, Any]) -> List[Finding]:
    """Run all NEC 2017 electrical checks"""
    findings = []
    
    findings.extend(article_210_receptacles(plan_graph))
    findings.extend(article_210_afci_requirements(plan_graph))
    findings.extend(article_220_load_calculation(plan_graph))
    findings.extend(article_625_ev_charging(plan_graph))
    findings.extend(irc_r315_smoke_co_detectors(plan_graph))
    
    return findings
