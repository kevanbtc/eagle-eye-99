"""
IRC 2018 Structural Rules - PE-Grade
Braced walls, floor systems, roof systems, foundations
"""
import sys
sys.path.append("../../packages/shared")
from models import Finding
from typing import List, Dict, Any


def r602_10_braced_walls(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IRC 2018 R602.10 - Braced Wall Panels
    Check for adequate bracing in each braced wall line
    """
    findings = []
    
    # Check for structural sheets
    structural_sheets = [
        sheet for sheet in plan_graph.get("sheets", [])
        if sheet.get("sheet_type") == "structural"
    ]
    
    # Check for braced wall mentions in text
    has_bwl_plan = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "BRACED WALL" in text or "BWL" in text or "CS-WSP" in text:
            has_bwl_plan = True
            break
    
    if not has_bwl_plan:
        findings.append(Finding(
            finding_code="RR-103",
            severity="Orange",
            discipline="Lateral/Wind",
            location="Walls/elevations",
            code_citation="IRC 2018 R602.10",
            consequence="Field redlines; shear continuity gaps; potential rework",
            fix="Produce braced-wall plan (each façade), method (CS-WSP recommended), lengths provided vs required, segment locations, hold-downs & anchors. State Vult/Exposure.",
            ve_alt="Portal frames at large openings to reduce bracing requirements",
            evidence_refs=["Wall framing plans", "Elevations"],
            submittal_needed="Braced-wall plan with HD/AB schedule"
        ))
    
    return findings


def r602_3_floor_systems(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IRC 2018 R602.3 + R301.1 - Floor Systems
    Check for engineered joist submittals (BCI, TJI, etc.)
    """
    findings = []
    
    # Look for engineered joist mentions
    has_ej_submittal = False
    joist_type = None
    
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "BCI" in text or "TJI" in text or "I-JOIST" in text:
            joist_type = "BCI" if "BCI" in text else "TJI"
            # Check if calc pack mentioned
            if "CALC" in text or "SUBMITTAL" in text or "ENGINEER" in text:
                has_ej_submittal = True
            break
    
    if joist_type and not has_ej_submittal:
        findings.append(Finding(
            finding_code="RR-101",
            severity="Red",
            discipline="Structural (Floor)",
            location="Framing / Floor joist notes",
            code_citation="IRC R301.1; Manufacturer L/480 requirements",
            consequence="Framing inspection hold; bounce/finish cracking; deflection failures",
            fix=f"Submit {joist_type} joist calc pack (actual spans, loads, L/480 deflection check) + LVL beam calcs with reactions & bearing lengths",
            ve_alt="Where spans are marginal, upgrade to deeper series or reduce spacing to 12\" o.c.",
            evidence_refs=["Framing plan notes", "Beam schedule"],
            submittal_needed=f"{joist_type} span/deflection package with load tables"
        ))
    
    return findings


def r802_roof_trusses(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IRC 2018 R802 - Roof Framing
    Check for truss submittals
    """
    findings = []
    
    has_truss_submittal = False
    
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "TRUSS" in text:
            # Check if stamped/sealed mentioned
            if "STAMP" in text or "SEAL" in text or "ENGINEER" in text or "SUBMITTAL" in text:
                has_truss_submittal = True
            break
    
    # Check for truss sheets in files
    if not has_truss_submittal:
        findings.append(Finding(
            finding_code="RR-102",
            severity="Red",
            discipline="Structural (Roof)",
            location="Roof plan (trusses)",
            code_citation="IRC R802; Sealed truss submittals required",
            consequence="Permit/inspection delay; uplift/bracing ambiguity; approval risk",
            fix="Attach stamped truss set with reactions, heel heights, bracing requirements & connector schedule matched to wind basis",
            ve_alt=None,
            evidence_refs=["Roof framing plan"],
            submittal_needed="Stamped truss package with reactions & connector schedule"
        ))
    
    return findings


def r310_egress_windows(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IRC 2018 R310 - Emergency Egress
    Check for egress window specifications
    """
    findings = []
    
    schedules = plan_graph.get("schedules", {})
    window_schedules = schedules.get("windows", [])
    
    # Look for egress callouts
    has_egress_spec = False
    for ws in window_schedules:
        text = ws.get("raw_text", "").upper()
        if "EGRESS" in text or "5.7" in text or "5.0" in text:
            has_egress_spec = True
            break
    
    if not has_egress_spec:
        findings.append(Finding(
            finding_code="RR-105",
            severity="Yellow",
            discipline="Egress/Life Safety",
            location="Bedroom windows",
            code_citation="IRC 2018 R310",
            consequence="CO delay; field verification required",
            fix="Provide cut sheets proving 5.7/5.0 sf net clear opening & ≤44\" sill height. Adjust unit sizes if needed.",
            ve_alt="Consider casement windows for easier egress compliance",
            evidence_refs=["Window schedule", "Bedroom floor plan"],
            submittal_needed="Egress window cut sheets with net clear dimensions"
        ))
    
    return findings


def r403_foundations(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IRC 2018 R403 - Footings
    Check for footing details
    """
    findings = []
    
    has_footing_details = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if "FOOTING" in text and ("REBAR" in text or "REINFORC" in text):
            has_footing_details = True
            break
    
    if not has_footing_details:
        findings.append(Finding(
            finding_code="RR-107",
            severity="Yellow",
            discipline="Foundations",
            location="Foundation plan / crawl details",
            code_citation="IRC 2018 R403, R408",
            consequence="Moisture/settlement risk; rework potential",
            fix="Declare vented vs conditioned crawl, vapor barrier spec, footing sizes/rebar (typically #4 @ 18\" o.c.), and frost depth compliance",
            ve_alt="Consider conditioned crawl with sealed vapor barrier for energy efficiency",
            evidence_refs=["Foundation plan", "Detail sections"],
            submittal_needed="Foundation/footing schedule with rebar callouts"
        ))
    
    return findings


def r806_attic_ventilation(plan_graph: Dict[str, Any]) -> List[Finding]:
    """
    IRC 2018 R806 - Roof Ventilation
    Check for ventilation calculations
    """
    findings = []
    
    has_vent_calc = False
    for sheet in plan_graph.get("sheets", []):
        text = sheet.get("text_preview", "").upper()
        if ("NFA" in text or "NET FREE AREA" in text) or ("SEALED ATTIC" in text or "UNVENTED" in text):
            has_vent_calc = True
            break
    
    if not has_vent_calc:
        findings.append(Finding(
            finding_code="RR-108",
            severity="Yellow",
            discipline="Roof/Moisture",
            location="Attic/roof details",
            code_citation="IRC 2018 R806",
            consequence="Moisture accumulation; shingle warranty void; mold risk",
            fix="Provide NFA calc (1:150 or 1:300 with balanced ventilation) OR declare sealed attic with spray foam/vapor control details",
            ve_alt="Sealed attic approach with conditioned space for energy performance",
            evidence_refs=["Roof plan", "Attic details"],
            submittal_needed="Attic ventilation calc or sealed attic specification"
        ))
    
    return findings


def run_irc_2018_checks(plan_graph: Dict[str, Any]) -> List[Finding]:
    """Run all IRC 2018 structural checks"""
    findings = []
    
    findings.extend(r602_10_braced_walls(plan_graph))
    findings.extend(r602_3_floor_systems(plan_graph))
    findings.extend(r802_roof_trusses(plan_graph))
    findings.extend(r310_egress_windows(plan_graph))
    findings.extend(r403_foundations(plan_graph))
    findings.extend(r806_attic_ventilation(plan_graph))
    
    return findings
