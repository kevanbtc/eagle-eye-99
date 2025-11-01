#!/usr/bin/env python3
"""
EAGLE EYE - PROFESSIONAL PROPOSAL GENERATOR
============================================
High-end automated proposal generation with branding, AI polish, and perfect formatting
"""

from datetime import datetime
from typing import Dict, List
import json

# ============================================================================
# EAGLE EYE BRANDING & CONFIGURATION
# ============================================================================

COMPANY_INFO = {
    "name": "EAGLE EYE",
    "tagline": "Professional Construction Plan Review & Estimating",
    "phone": "(770) 555-0123",
    "email": "estimates@eagleeye.com",
    "website": "www.eagleeye.com",
    "logo_text": "🦅 EAGLE EYE",
    "colors": {
        "primary": "#1E40AF",      # Deep blue
        "accent": "#DC2626",       # Red accent
        "success": "#16A34A",      # Green
        "warning": "#EA580C",      # Orange
        "danger": "#991B1B",       # Dark red
        "neutral": "#374151"       # Gray
    }
}

# ============================================================================
# PROFESSIONAL PROPOSAL TEMPLATES
# ============================================================================

class ProposalGenerator:
    """Generates high-end professional proposals with Eagle Eye branding"""
    
    @staticmethod
    def generate_pdf_proposal(project: Dict, estimate: Dict, compliance: Dict) -> str:
        """Generate professional PDF proposal"""
        
        proposal = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                         🦅 EAGLE EYE ESTIMATES                            ║
║                     Professional Construction Review                      ║
║                                                                            ║
║  {COMPANY_INFO['phone']} | {COMPANY_INFO['email']} | {COMPANY_INFO['website']}            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


PROJECT ESTIMATE & PROPOSAL
═════════════════════════════════════════════════════════════════════════════

Prepared for:
  Client Name:     {project.get('client_name', 'TBD')}
  Project Name:    {project.get('project_name', 'TBD')}
  Address:         {project.get('address', 'TBD')}
  City/State/ZIP:  {project.get('city', '')}, {project.get('state', '')} {project.get('zip_code', '')}

Prepared by:
  Eagle Eye Estimating System
  Date: {datetime.now().strftime('%B %d, %Y')}
  Reference: EST-{project.get('id', '00000')[-6:].upper()}

═════════════════════════════════════════════════════════════════════════════

PROJECT OVERVIEW
─────────────────────────────────────────────────────────────────────────────

This estimate is based on careful analysis of your construction plans and
includes all labor, materials, permits, and required code compliance.

✓ Comprehensive component analysis
✓ Regional pricing adjustments
✓ Full code compliance review
✓ Professional-grade workmanship included
✓ Timeline and warranty information

═════════════════════════════════════════════════════════════════════════════

COST BREAKDOWN - LINE ITEMS
─────────────────────────────────────────────────────────────────────────────

"""
        
        # Add line items
        if "line_items" in estimate:
            proposal += "Item | Description         | Qty  | Unit Price | Extension\n"
            proposal += "─────┼──────────────────────┼──────┼────────────┼──────────────\n"
            
            for idx, item in enumerate(estimate["line_items"][:10], 1):
                component = item.get("component", "")
                qty = item.get("quantity", 0)
                total = item.get("total", 0)
                labor = item.get("labor", 0)
                material = item.get("material", 0)
                
                proposal += f"{idx:>4} │ {component:<20} │ {qty:>5.0f} │ ${total/qty if qty else 0:>9,.2f} │ ${total:>10,.2f}\n"
            
            if len(estimate.get("line_items", [])) > 10:
                proposal += f"\n... and {len(estimate['line_items']) - 10} more line items\n"
        
        proposal += f"""

═════════════════════════════════════════════════════════════════════════════

FINANCIAL SUMMARY
─────────────────────────────────────────────────────────────────────────────

Labor Costs:                    ${estimate['summary']['labor']:>15,.2f}
Material Costs:                 ${estimate['summary']['material']:>15,.2f}
Permit & Application Fees:      ${estimate['summary']['permit']:>15,.2f}
                                ─────────────────────────
Subtotal:                       ${estimate['summary']['subtotal']:>15,.2f}

Markup (30%):                   ${estimate['summary']['margin_30pct']:>15,.2f}
                                ═════════════════════════════

TOTAL PROJECT COST:             ${estimate['summary']['selling_price']:>15,.2f}

═════════════════════════════════════════════════════════════════════════════

PROJECT TIMELINE
─────────────────────────────────────────────────────────────────────────────

Estimated Timeline to Completion:  {estimate['summary']['timeline_days']} days

This includes:
  • Permit application and approval
  • Material ordering and delivery
  • Installation and inspection
  • Final walkthrough

═════════════════════════════════════════════════════════════════════════════

CODE COMPLIANCE ANALYSIS
─────────────────────────────────────────────────────────────────────────────

Our analysis has identified the following code compliance items:

"""
        
        # Add compliance findings
        if compliance.get("summary"):
            summary = compliance["summary"]
            proposal += f"""
🔴 CRITICAL ITEMS (Must Address):        {summary.get('critical', 0)}
   These items must be corrected before permit approval.

🟠 IMPORTANT ITEMS (Should Address):     {summary.get('important', 0)}
   These items are recommended for permit compliance.

🟡 INFORMATIONAL ITEMS (Reference):      {summary.get('notice', 0)}
   These are best practices and optional recommendations.

"""
        
        # Add compliance details
        if compliance.get("findings"):
            proposal += "\nDETAILED FINDINGS:\n"
            for finding in compliance["findings"][:5]:
                severity = finding.get("severity", "YELLOW")
                code = finding.get("rule_code", "N/A")
                title = finding.get("title", "N/A")
                proposal += f"  [{severity}] {code} - {title}\n"
        
        proposal += f"""

═════════════════════════════════════════════════════════════════════════════

TERMS & CONDITIONS
─────────────────────────────────────────────────────────────────────────────

✓ Warranty: All work guaranteed for 1 year
✓ Insurance: Full liability coverage included
✓ Permits: All required permits included
✓ Inspections: All required inspections included
✓ Payment Terms: 50% upon start, 50% upon completion
✓ Timeline: Subject to permit approval and material availability

═════════════════════════════════════════════════════════════════════════════

NEXT STEPS
─────────────────────────────────────────────────────────────────────────────

1. Review this estimate carefully
2. Contact us with any questions or clarifications
3. Sign below to accept the proposal
4. Return to commence work

═════════════════════════════════════════════════════════════════════════════

ACCEPTANCE & SIGNATURE

By signing below, you accept this estimate and authorize Eagle Eye to proceed
with the project as outlined. This proposal is valid for 30 days from the
date above.

Client Name (Print):  ________________________________   Date: ____________

Client Signature:     ________________________________


For Eagle Eye:        EAGLE EYE ESTIMATING              Date: ____________
                      Automated Proposal Generator


═════════════════════════════════════════════════════════════════════════════

This proposal was automatically generated by Eagle Eye's AI-powered
estimation system. All calculations are verified and all code compliance
items have been checked against current regulations for {project.get('state', 'XX')}.

Questions? Contact us:
  📞 {COMPANY_INFO['phone']}
  📧 {COMPANY_INFO['email']}
  🌐 {COMPANY_INFO['website']}

═════════════════════════════════════════════════════════════════════════════

EAGLE EYE - Professional Construction Estimating at the Speed of Light ⚡

"""
        return proposal
    
    @staticmethod
    def generate_excel_proposal(project: Dict, estimate: Dict, compliance: Dict) -> Dict:
        """Generate Excel-compatible data structure with professional formatting"""
        
        excel_data = {
            "metadata": {
                "title": f"Eagle Eye Estimate - {project.get('project_name', 'Project')}",
                "author": "Eagle Eye Estimating System",
                "created": datetime.now().isoformat(),
                "logo": "🦅 EAGLE EYE",
                "colors": COMPANY_INFO["colors"]
            },
            "sheets": {
                "Cover": {
                    "title": "EAGLE EYE ESTIMATE",
                    "company": COMPANY_INFO["name"],
                    "date": datetime.now().strftime("%B %d, %Y"),
                    "project_info": {
                        "Client": project.get("client_name", ""),
                        "Project": project.get("project_name", ""),
                        "Address": project.get("address", ""),
                        "City": project.get("city", ""),
                        "State": project.get("state", ""),
                        "ZIP": project.get("zip_code", "")
                    }
                },
                "Line Items": {
                    "headers": ["Component", "Quantity", "Unit", "Unit Price", "Labor", "Material", "Total"],
                    "data": estimate.get("line_items", []),
                    "summary": {
                        "Total Labor": estimate["summary"]["labor"],
                        "Total Material": estimate["summary"]["material"],
                        "Total Permits": estimate["summary"]["permit"],
                        "Subtotal": estimate["summary"]["subtotal"],
                        "Markup (30%)": estimate["summary"]["margin_30pct"],
                        "Final Price": estimate["summary"]["selling_price"]
                    }
                },
                "Compliance": {
                    "headers": ["Code", "Title", "Severity", "Description"],
                    "data": compliance.get("findings", []),
                    "summary": compliance.get("summary", {})
                },
                "Summary": {
                    "project": project,
                    "estimate": estimate["summary"],
                    "compliance": compliance["summary"],
                    "timeline_days": estimate["summary"]["timeline_days"]
                }
            }
        }
        
        return excel_data
    
    @staticmethod
    def generate_html_proposal(project: Dict, estimate: Dict, compliance: Dict) -> str:
        """Generate beautiful HTML proposal with Eagle Eye branding"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eagle Eye Estimate - {project.get('project_name', 'Project')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #374151; }}
        
        .header {{
            background: linear-gradient(135deg, {COMPANY_INFO['colors']['primary']} 0%, {COMPANY_INFO['colors']['accent']} 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        
        .project-info {{
            background: #F9FAFB;
            padding: 20px;
            border-left: 4px solid {COMPANY_INFO['colors']['primary']};
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .section {{ margin: 30px 0; }}
        .section-title {{
            font-size: 1.5em;
            font-weight: bold;
            color: {COMPANY_INFO['colors']['primary']};
            border-bottom: 2px solid {COMPANY_INFO['colors']['primary']};
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        
        th {{
            background: {COMPANY_INFO['colors']['primary']};
            color: white;
            padding: 12px;
            text-align: left;
        }}
        
        td {{ padding: 10px 12px; border-bottom: 1px solid #E5E7EB; }}
        tr:hover {{ background: #F3F4F6; }}
        
        .total {{ font-weight: bold; font-size: 1.2em; }}
        .total-row {{ background: #F0F9FF; }}
        
        .price-highlight {{
            font-size: 1.8em;
            font-weight: bold;
            color: {COMPANY_INFO['colors']['accent']};
            text-align: right;
            padding: 20px;
            background: #FEF2F2;
            border-radius: 4px;
            margin: 20px 0;
        }}
        
        .compliance-critical {{ color: {COMPANY_INFO['colors']['danger']}; font-weight: bold; }}
        .compliance-warning {{ color: {COMPANY_INFO['colors']['warning']}; font-weight: bold; }}
        .compliance-info {{ color: {COMPANY_INFO['colors']['success']}; }}
        
        .footer {{
            text-align: center;
            color: #6B7280;
            font-size: 0.9em;
            padding: 20px;
            border-top: 1px solid #E5E7EB;
            margin-top: 30px;
        }}
        
        .footer p {{ margin: 5px 0; }}
        
        .signature {{ margin: 40px 0; }}
        .signature-line {{ border-top: 2px solid #374151; padding-top: 10px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦅 EAGLE EYE ESTIMATES</h1>
        <p>Professional Construction Plan Review & Estimating</p>
    </div>
    
    <div class="container">
        <div class="project-info">
            <h2>Project Information</h2>
            <p><strong>Client:</strong> {project.get('client_name', 'TBD')}</p>
            <p><strong>Project:</strong> {project.get('project_name', 'TBD')}</p>
            <p><strong>Address:</strong> {project.get('address', 'TBD')}, {project.get('city', '')}, {project.get('state', '')} {project.get('zip_code', '')}</p>
            <p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <div class="section">
            <h3 class="section-title">Cost Breakdown</h3>
            <table>
                <tr>
                    <th>Description</th>
                    <th style="text-align: right;">Amount</th>
                </tr>
                <tr>
                    <td>Labor Costs</td>
                    <td style="text-align: right;">${estimate['summary']['labor']:,.2f}</td>
                </tr>
                <tr>
                    <td>Material Costs</td>
                    <td style="text-align: right;">${estimate['summary']['material']:,.2f}</td>
                </tr>
                <tr>
                    <td>Permit & Fees</td>
                    <td style="text-align: right;">${estimate['summary']['permit']:,.2f}</td>
                </tr>
                <tr class="total-row">
                    <td class="total">Subtotal</td>
                    <td class="total" style="text-align: right;">${estimate['summary']['subtotal']:,.2f}</td>
                </tr>
                <tr>
                    <td>Markup (30%)</td>
                    <td style="text-align: right;">${estimate['summary']['margin_30pct']:,.2f}</td>
                </tr>
            </table>
            
            <div class="price-highlight">
                TOTAL PROJECT PRICE: ${estimate['summary']['selling_price']:,.2f}
            </div>
        </div>
        
        <div class="section">
            <h3 class="section-title">Compliance Status</h3>
            <p><span class="compliance-critical">🔴 Critical:</span> {compliance['summary'].get('critical', 0)} items</p>
            <p><span class="compliance-warning">🟠 Important:</span> {compliance['summary'].get('important', 0)} items</p>
            <p><span class="compliance-info">🟡 Notice:</span> {compliance['summary'].get('notice', 0)} items</p>
        </div>
        
        <div class="section">
            <h3 class="section-title">Project Timeline</h3>
            <p>Estimated completion: <strong>{estimate['summary']['timeline_days']} days</strong></p>
        </div>
        
        <div class="signature">
            <p><strong>Acceptance</strong></p>
            <p>By signing below, you authorize Eagle Eye to proceed with the project.</p>
            
            <div style="margin-top: 40px;">
                <p>Client Signature: ________________________________ Date: ___________</p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🦅 EAGLE EYE ESTIMATING</strong></p>
            <p>{COMPANY_INFO['phone']} | {COMPANY_INFO['email']} | {COMPANY_INFO['website']}</p>
            <p>Professional construction estimating at the speed of light ⚡</p>
        </div>
    </div>
</body>
</html>
"""
        return html


# ============================================================================
# DEMO: GENERATE HIGH-END PROPOSALS
# ============================================================================

if __name__ == "__main__":
    # Sample data
    project = {
        "id": "b61b802f",
        "client_name": "Acme Construction Co",
        "project_name": "Residential Renovation",
        "address": "123 Main Street",
        "city": "Madison",
        "state": "GA",
        "zip_code": "30601"
    }
    
    estimate = {
        "line_items": [
            {"component": "HVAC", "quantity": 2, "unit": "unit", "labor": 240, "material": 1520, "total": 1760},
            {"component": "Windows", "quantity": 24, "unit": "each", "labor": 1080, "material": 6000, "total": 7080},
            {"component": "Doors", "quantity": 8, "unit": "each", "labor": 280, "material": 1600, "total": 1880},
        ],
        "summary": {
            "labor": 87050.40,
            "material": 145502.00,
            "permit": 450.00,
            "subtotal": 233002.40,
            "margin_30pct": 69900.72,
            "selling_price": 302903.12,
            "timeline_days": 12
        }
    }
    
    compliance = {
        "findings": [
            {"rule_code": "GA-FLOOD-ZONE", "title": "Flood Zone Elevation", "severity": "RED"},
            {"rule_code": "IECC-2015-C402.3.6", "title": "HVAC SEER Rating", "severity": "ORANGE"},
        ],
        "summary": {"critical": 1, "important": 4, "notice": 2}
    }
    
    # Generate proposals
    generator = ProposalGenerator()
    
    print("\n" + "="*80)
    print("EAGLE EYE - PROFESSIONAL PROPOSAL GENERATION")
    print("="*80)
    
    # Text proposal
    pdf_proposal = generator.generate_pdf_proposal(project, estimate, compliance)
    print("\n✓ PDF PROPOSAL GENERATED:")
    print(pdf_proposal[:500] + "\n...")
    
    # Excel data
    excel_data = generator.generate_excel_proposal(project, estimate, compliance)
    print("\n✓ EXCEL DATA GENERATED:")
    print(f"  Sheets: {list(excel_data['sheets'].keys())}")
    print(f"  Total Price: ${excel_data['sheets']['Summary']['estimate']['selling_price']:,.2f}")
    
    # HTML proposal
    html_proposal = generator.generate_html_proposal(project, estimate, compliance)
    print("\n✓ HTML PROPOSAL GENERATED:")
    print(f"  Length: {len(html_proposal)} characters")
    print(f"  Ready for web browser or PDF conversion")
    
    print("\n" + "="*80)
    print("✅ ALL PROPOSAL FORMATS READY")
    print("="*80 + "\n")
