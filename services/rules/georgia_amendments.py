"""
Georgia State Amendments & Local Requirements
Atlanta metro area specifics
"""
import sys
sys.path.append("../../packages/shared")
from models import Finding
from typing import List, Dict, Any


def ga_termite_treatment(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    Georgia Amendment - Termite Protection Required
    All counties in Georgia require termite pre-treatment
    """
    findings = []
    
    has_termite_spec = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "TERMITE" in text or "PEST" in text:
            has_termite_spec = True
            break
    
    if not has_termite_spec:
        findings.append(Finding(
            finding_code="GA-401",
            severity="Yellow",
            discipline="Site / Foundation",
            location="Foundation plans / general notes",
            code_citation="Georgia Amendment - Termite Protection (all counties)",
            consequence="Permit hold; add $800-$1,200 to budget; pre-treatment coordination",
            fix="Specify termite pre-treatment per Georgia requirements. Coordinate with licensed pest control vendor. Note on plans.",
            ve_alt=None,
            evidence_refs=["Foundation plan", "General notes"],
            submittal_needed="Termite treatment contract/certification"
        ))
    
    return findings


def ga_roof_low_slope(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    Georgia / Hot-Humid Climate - Low-Slope Roof Details
    Extra scrutiny for porches at 1:12 to 2:12
    """
    findings = []
    
    # Check for low-slope mentions
    has_low_slope = False
    has_low_slope_detail = False
    
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        # Look for pitch ratios
        if any(pitch in text for pitch in ["1:12", "1.5:12", "2:12", "1/12", "1.5/12"]):
            has_low_slope = True
        if has_low_slope and ("UNDERLAYMENT" in text or "ICE/WATER" in text or "HIGH-TEMP" in text):
            has_low_slope_detail = True
    
    if has_low_slope and not has_low_slope_detail:
        findings.append(Finding(
            finding_code="RR-104",
            severity="Orange",
            discipline="Envelope/Roof",
            location="Porch roof / low-slope areas",
            code_citation="IRC R905; Georgia hot-humid climate; manufacturer specs",
            consequence="Water intrusion at porch/roof tie-ins; warranty void; leak risk",
            fix="Specify low-slope system: high-temp underlayment (Ice & Water Shield equivalent), metal panel OR modified bitumen suitable for pitch. Include kick-out flashings and roof-to-wall details.",
            ve_alt="Standing-seam metal (Option B) suitable for low slopes; better longevity",
            evidence_refs=["Roof plan", "Porch details"],
            submittal_needed="Low-slope roofing spec and flashing details"
        ))
    
    return findings


def atlanta_drainage_requirements(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    City of Atlanta - Drainage & Stormwater
    Rain garden / detention if required by lot size/impervious
    """
    findings = []
    
    # Check for civil/site plans
    site_sheets = [
        sheet for sheet in plan_graph.get("sheets", [])
        if sheet.get("sheet_type") == "site" or "CIVIL" in sheet.get("text_preview", "").upper()
    ]
    
    has_drainage_plan = False
    for sheet in site_sheets:
        text = sheet.get("text_preview", "").upper()
        if "DRAINAGE" in text or "RAIN GARDEN" in text or "DETENTION" in text:
            has_drainage_plan = True
            break
    
    # Only flag if site plan exists but no drainage details
    if site_sheets and not has_drainage_plan:
        findings.append(Finding(
            finding_code="GA-402",
            severity="Yellow",
            discipline="Civil/Site",
            location="Site plan",
            code_citation="City of Atlanta Drainage Ordinance",
            consequence="Permit review comment; potential rain garden requirement; drawdown compliance",
            fix="Verify if stormwater management required (lot coverage, impervious area). If rain garden needed, show location, sizing, drawdown ≤72h, and native plantings.",
            ve_alt=None,
            evidence_refs=["Site plan"],
            submittal_needed="Stormwater management plan (if applicable)"
        ))
    
    return findings


def ga_building_official_notes(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    Georgia / AHJ - Common Plan Review Notes
    Items frequently called out by GA building officials
    """
    findings = []
    
    # Check for common missing items
    has_wind_spec = False
    has_snow_load = False
    
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "WIND" in text and ("MPH" in text or "SPEED" in text):
            has_wind_spec = True
        if "SNOW" in text or "GROUND SNOW LOAD" in text:
            has_snow_load = True
    
    if not has_wind_spec:
        findings.append(Finding(
            finding_code="GA-403",
            severity="Yellow",
            discipline="Structural/Design Criteria",
            location="Title sheet / design notes",
            code_citation="IRC R301.2; Georgia wind speeds",
            consequence="Permit review delay; wind basis unclear for braced walls/trusses",
            fix="State design wind speed (Vult) and Exposure category. Typical Atlanta metro: 115-120 mph Vult, Exposure B/C depending on site.",
            ve_alt=None,
            evidence_refs=["Title sheet", "Structural notes"],
            submittal_needed="Design criteria statement with wind speed"
        ))
    
    if not has_snow_load:
        findings.append(Finding(
            finding_code="GA-404",
            severity="Yellow",
            discipline="Structural/Design Criteria",
            location="Title sheet / design notes",
            code_citation="IRC R301.2; Georgia snow loads",
            consequence="Roof load basis incomplete",
            fix="State ground snow load. Typical Georgia: 5-10 psf depending on county elevation.",
            ve_alt=None,
            evidence_refs=["Title sheet", "Structural notes"],
            submittal_needed="Design criteria statement with snow load"
        ))
    
    return findings


def run_georgia_checks(plan_graph: Dict[str, Any]) -> List[Finding]:
    """Run all Georgia amendment and local checks"""
    findings = []
    
    findings.extend(ga_termite_treatment(plan_graph))
    findings.extend(ga_roof_low_slope(plan_graph))
    findings.extend(atlanta_drainage_requirements(plan_graph))
    findings.extend(ga_building_official_notes(plan_graph))
    
    return findings
