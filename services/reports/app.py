"""
Eagle Eye Reports Service
Jinja2 → PDF/CSV rendering
"""
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import csv
from io import StringIO
from typing import Dict, Any, List


def get_template_env() -> Environment:
    """Get Jinja2 environment with templates"""
    template_dir = Path("../../templates")
    return Environment(loader=FileSystemLoader(str(template_dir)))


def render_proposal_pdf(context: Dict[str, Any], output_path: str):
    """
    Render Eagle Eye Proposal PDF
    Sections: A-I (Executive, Risk, Code, Structural, Envelope, Estimate, Draw, Submittals, Appendix)
    """
    env = get_template_env()
    template = env.get_template("proposal.pdf.j2")
    
    html_content = template.render(**context)
    
    # Generate PDF
    HTML(string=html_content).write_pdf(output_path)
    
    print(f"Generated proposal PDF: {output_path}")


def render_lender_summary_pdf(context: Dict[str, Any], output_path: str):
    """
    Render Lender Summary PDF
    Simplified view with totals, risk assessment, draw schedule
    """
    env = get_template_env()
    template = env.get_template("lender_summary.pdf.j2")
    
    html_content = template.render(**context)
    HTML(string=html_content).write_pdf(output_path)
    
    print(f"Generated lender summary PDF: {output_path}")


def render_xactimate_csv(line_items: List[Dict[str, Any]], output_path: str):
    """
    Render Xactimate-compatible CSV
    Columns: WBS, Assembly, Line Item, UoM, Qty, Unit, Ext, Notes, Alt Group
    """
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['WBS', 'Assembly', 'Line Item', 'UoM', 'Qty', 'Unit Cost', 'Ext Cost', 'Notes', 'Alt Group']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in line_items:
            writer.writerow({
                'WBS': item.get('wbs', ''),
                'Assembly': item.get('assembly', ''),
                'Line Item': item.get('line_item', ''),
                'UoM': item.get('uom', ''),
                'Qty': item.get('qty', 0),
                'Unit Cost': f"{item.get('unit_cost', 0):.2f}",
                'Ext Cost': f"{item.get('ext_cost', 0):.2f}",
                'Notes': item.get('notes', ''),
                'Alt Group': item.get('alt_group', '')
            })
    
    print(f"Generated Xactimate CSV: {output_path}")


def generate_all_reports(project_data: Dict[str, Any], output_dir: str):
    """
    Generate all reports for a project
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Proposal PDF
    proposal_context = {
        "project": project_data.get("project", {}),
        "findings": project_data.get("findings", []),
        "estimate": project_data.get("estimate", {}),
        "company": {
            "name": "Eagle Eye AI",
            "address": "Atlanta, GA",
            "phone": "(555) 123-4567",
            "email": "proposals@eagleeye.ai"
        }
    }
    render_proposal_pdf(proposal_context, str(output_path / "proposal.pdf"))
    
    # Lender Summary
    lender_context = {
        "project": project_data.get("project", {}),
        "summary": project_data.get("estimate", {}).get("summary", {}),
        "risk_count": len([f for f in project_data.get("findings", []) if f.get("severity") == "Red"])
    }
    render_lender_summary_pdf(lender_context, str(output_path / "lender_summary.pdf"))
    
    # Xactimate CSV
    line_items = []
    estimate = project_data.get("estimate", {})
    for trade, items in estimate.get("base", {}).items():
        line_items.extend(items)
    
    render_xactimate_csv(line_items, str(output_path / "xactimate.csv"))
    
    print(f"\nAll reports generated in {output_dir}")


if __name__ == "__main__":
    # Example usage
    mock_project_data = {
        "project": {
            "name": "123 Main Street Renovation",
            "address": "123 Main St, Atlanta, GA 30301"
        },
        "findings": [
            {
                "severity": "Red",
                "code_citation": "IRC 2018 R602.10",
                "impact": "Missing braced wall panels",
                "recommendation": "Add BWL per facade"
            }
        ],
        "estimate": {
            "base": {
                "Concrete": [
                    {"wbs": "01.01", "assembly": "Foundation", "line_item": "Foundation", 
                     "uom": "LF", "qty": 200, "unit_cost": 45.00, "ext_cost": 9000.00}
                ]
            },
            "summary": {
                "subtotal": 50000.00,
                "grand_total": 60000.00
            }
        }
    }
    
    generate_all_reports(mock_project_data, "./output")
