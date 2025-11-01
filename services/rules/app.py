"""
Eagle Eye Rules Service - Code Compliance Checks
IRC 2018, IECC 2015, NEC 2017, Georgia Amendments
"""
import sys
sys.path.append("../../packages/shared")
from models import Finding
from typing import List, Dict, Any

# Import all rule packs
from irc_2018 import run_irc_2018_checks
from iecc_2015 import run_iecc_2015_checks
from nec_2017 import run_nec_2017_checks
from georgia_amendments import run_georgia_checks


def run_all_checks(plan_graph: Dict[str, Any], jurisdiction: Dict[str, Any] = None) -> List[Finding]:
    """
    Run all code compliance checks based on jurisdiction
    Returns list of findings sorted by severity (Red > Orange > Yellow)
    """
    all_findings = []
    
    # Determine which code sets to run based on jurisdiction
    code_set = jurisdiction.get("code_set", "IRC2018_IECC2015_NEC2017_GA") if jurisdiction else "IRC2018_IECC2015_NEC2017_GA"
    state = jurisdiction.get("state", "GA") if jurisdiction else "GA"
    
    # IRC 2018 checks (structural, egress, foundations)
    if "IRC2018" in code_set or "IRC" in code_set:
        all_findings.extend(run_irc_2018_checks(plan_graph))
    
    # IECC 2015 checks (energy, insulation, air sealing)
    if "IECC2015" in code_set or "IECC" in code_set:
        all_findings.extend(run_iecc_2015_checks(plan_graph))
    
    # NEC 2017 checks (electrical, load calc, EV, life safety)
    if "NEC2017" in code_set or "NEC" in code_set:
        all_findings.extend(run_nec_2017_checks(plan_graph))
    
    # State amendments
    if state == "GA":
        all_findings.extend(run_georgia_checks(plan_graph))
    
    # Sort by severity (Red > Orange > Yellow)
    severity_order = {"Red": 0, "Orange": 1, "Yellow": 2}
    all_findings.sort(key=lambda f: severity_order.get(f.severity, 3))
    
    # Assign IDs if not already set
    for i, finding in enumerate(all_findings, 1):
        if not finding.finding_code:
            finding.finding_code = f"F-{i:03d}"
    
    return all_findings


if __name__ == "__main__":
    # Example usage
    import json
    
    # Mock plan graph
    mock_graph = {
        "sheets": [
            {"page": 1, "sheet_type": "architectural", "text_preview": "Floor plan with R-30 attic"},
            {"page": 2, "sheet_type": "structural", "text_preview": "Braced wall elevations"},
        ],
        "schedules": {
            "windows": [{"raw_text": "Window schedule with U-factor ratings"}],
            "doors": []
        }
    }
    
    mock_jurisdiction = {
        "state": "GA",
        "code_set": "IRC2018_IECC2015_NEC2017_GA",
        "climate_zone": "3"
    }
    
    findings = run_all_checks(mock_graph, mock_jurisdiction)
    
    print(f"\nFound {len(findings)} code compliance issues:")
    for finding in findings:
        print(f"\n[{finding.severity}] {finding.finding_code} - {finding.code_citation}")
        print(f"  Location: {finding.location}")
        print(f"  Consequence: {finding.consequence}")
        print(f"  Fix: {finding.fix}")
        if finding.ve_alt:
            print(f"  VE Alt: {finding.ve_alt}")
        if finding.submittal_needed:
            print(f"  Submittal: {finding.submittal_needed}")

    
    findings = run_all_checks(mock_graph)
    
    print(f"Found {len(findings)} issues:")
    for finding in findings:
        print(f"\n[{finding.severity}] {finding.code_citation}")
        print(f"  {finding.impact}")
        print(f"  → {finding.recommendation}")
