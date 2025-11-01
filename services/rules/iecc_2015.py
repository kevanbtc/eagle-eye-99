"""
IECC 2015 Energy Code Rules (Georgia Climate Zone 3)
R-values, U-factors, SHGC, air sealing
"""
import sys
sys.path.append("../../packages/shared")
from models import Finding
from typing import List, Dict, Any


def r402_1_insulation_requirements(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IECC 2015 R402.1 - Insulation & Fenestration Requirements
    Climate Zone 3 (Georgia): R-30 ceiling, R-13/20 walls, R-5 slab edge
    """
    findings = []
    
    # Check for insulation callouts
    has_r30_ceiling = False
    has_r13_walls = False
    has_insulation_details = False
    
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "R-30" in text or "R30" in text:
            has_r30_ceiling = True
        if "R-13" in text or "R13" in text or "R-20" in text:
            has_r13_walls = True
        if "INSULATION" in text:
            has_insulation_details = True
    
    if not (has_r30_ceiling and has_r13_walls):
        findings.append(Finding(
            finding_code="EE-201",
            severity="Orange",
            discipline="Envelope/Energy",
            location="Building sections / wall details",
            code_citation="IECC 2015 R402.1 (Climate Zone 3, Georgia)",
            consequence="Energy code non-compliance; blower door failure; utility cost impact",
            fix="Add insulation callouts: R-30 ceiling/attic, R-13 wall cavities (or R-20 continuous), R-5 slab edge per IECC Table R402.1.2. Specify installation grade I.",
            ve_alt="Upgrade to R-38 attic + R-15 walls for better energy performance, resale value, and code compliance buffer",
            evidence_refs=["Wall sections", "Roof/attic details"],
            submittal_needed="Insulation schedule with R-values and installation method"
        ))
    
    return findings


def r402_4_air_sealing(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IECC 2015 R402.4 - Air Leakage
    Max 3 ACH50 (or 5 ACH50 if not tested)
    """
    findings = []
    
    schedules = plan_graph.get("schedules", {})
    window_schedules = schedules.get("windows", [])
    
    # Check for air sealing details
    has_air_seal_spec = False
    has_window_ratings = False
    
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "AIR SEAL" in text or "BLOWER DOOR" in text or "ACH50" in text:
            has_air_seal_spec = True
            break
    
    for ws in window_schedules:
        text = ws.get("raw_text", "").upper()
        if "U-FACTOR" in text or "SHGC" in text or "U=" in text:
            has_window_ratings = True
            break
    
    if not has_window_ratings:
        findings.append(Finding(
            finding_code="EE-202",
            severity="Yellow",
            discipline="Envelope/Windows",
            location="Window schedule",
            code_citation="IECC 2015 R402.4.1, Table R402.1.2",
            consequence="Cannot verify air leakage compliance (Max 0.30 cfm/sf window area). Energy loss.",
            fix="Provide window schedule with U-factor (≤0.35 CZ3) and SHGC (≤0.25 for south-facing recommended). Specify installation with pan flashing and air seal details.",
            ve_alt="Consider high-performance windows (U ≤ 0.30, SHGC ≤ 0.23) for energy code buffer and comfort",
            evidence_refs=["Window schedule"],
            submittal_needed="Window cut sheets with NFRC ratings"
        ))
    
    if not has_air_seal_spec:
        findings.append(Finding(
            finding_code="EE-203",
            severity="Yellow",
            discipline="Envelope/Air Barrier",
            location="General notes / sections",
            code_citation="IECC 2015 R402.4",
            consequence="Blower door test failure risk (target ≤3 ACH50); energy penalty",
            fix="Add air sealing continuity details at: rim joists, top plates, penetrations, windows/doors. Specify blower door target ≤3 ACH50 or use 5 ACH50 table values.",
            ve_alt="Sealed attic approach with spray foam for comprehensive air barrier",
            evidence_refs=["Wall sections", "General notes"],
            submittal_needed="Air barrier continuity plan"
        ))
    
    return findings


def r402_2_ufactor_requirements(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IECC 2015 R402.2 - UA Alternative (Trade-off Path)
    Optional if prescriptive path not met
    """
    findings = []
    
    # This is typically handled by energy modeler
    # Flag if neither prescriptive nor performance path is mentioned
    
    has_energy_path = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if any(keyword in text for keyword in ["PRESCRIPTIVE", "PERFORMANCE", "RESCHECK", "COMCHECK", "UA TRADE"]):
            has_energy_path = True
            break
    
    if not has_energy_path:
        findings.append(Finding(
            finding_code="EE-204",
            severity="Yellow",
            discipline="Energy/Compliance",
            location="General notes",
            code_citation="IECC 2015 R402.2",
            consequence="Energy compliance path unclear; permit review delay",
            fix="Declare energy compliance path: Prescriptive (R-values + U/SHGC) OR UA Trade-off (REScheck) OR Performance (energy model). Provide documentation.",
            ve_alt=None,
            evidence_refs=["Title sheet", "General notes"],
            submittal_needed="REScheck report or energy compliance declaration"
        ))
    
    return findings


def run_iecc_2015_checks(plan_graph: Dict[str, Any]) -> List[Finding]:
    """Run all IECC 2015 energy checks"""
    findings = []
    
    findings.extend(r402_1_insulation_requirements(plan_graph))
    findings.extend(r402_4_air_sealing(plan_graph))
    findings.extend(r402_2_ufactor_requirements(plan_graph))
    
    return findings
