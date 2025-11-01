# Eagle Eye: Complete Estimating System Technical Build Guide

**Purpose**: Build a fast, accurate estimating system that impresses customers on their first estimate  
**Time Investment**: 2-3 months to full production  
**ROI**: 60x faster estimates = 60x more capacity = massive revenue increase  
**Document Date**: November 1, 2025

---

## PART 1: THE SYSTEM ARCHITECTURE (How It All Works)

### The Magic: 5-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    CUSTOMER UPLOADS FILES                   │
│               (PDF plans + Excel template + photos)          │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────────┐     ┌──────────────────┐
│  Stage 1: PARSE  │     │  Stage 2: ENRICH │
│  Extract Data    │────▶│  Add Regional    │
│  from PDFs       │     │  Factors & Rules │
└──────────────────┘     └────────┬─────────┘
        │                         │
        │                    ┌────▼─────────┐
        │                    │ Stage 3: CHECK│
        │                    │ Compliance    │
        │                    │ Rules Engine  │
        │                    └────┬──────────┘
        │                         │
        └────────────┬────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   Stage 4: ESTIMATE        │
        │   Calculate Costs          │
        │   Labor + Materials + O&P  │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   Stage 5: GENERATE        │
        │   PDF + Excel + CSV        │
        │   Ready to send to client  │
        └────────────────────────────┘
```

### What Each Stage Does

#### **STAGE 1: PARSE (Extract from PDFs)**

**Input**: PDF construction plans (any format)

**What Happens**:
1. Convert PDF to high-quality images (300 DPI)
2. Run OCR (Tesseract) to extract text
3. Use computer vision to find:
   - Component tables/schedules
   - Dimension annotations
   - Material callouts
   - Detail references
4. Create structured data (JSON)

**Output**:
```json
{
  "components": [
    {
      "type": "Windows",
      "quantity": 12,
      "size": "3'x5'",
      "material": "vinyl",
      "model": "Anderson 400 series",
      "location": "Exterior walls",
      "specification": "Double-pane, Low-E, argon",
      "confidence": 0.95
    },
    {
      "type": "HVAC System",
      "quantity": 1,
      "capacity": "2.5 ton",
      "type": "Central Air",
      "location": "Attic",
      "model": "Carrier 25HNB",
      "seer_rating": 16,
      "confidence": 0.87
    }
  ],
  "structural_elements": [
    {
      "element": "Floor joist",
      "spacing": "16\" OC",
      "size": "2x10",
      "material": "Pressure treated pine"
    }
  ],
  "site_conditions": {
    "terrain": "sloped",
    "drainage": "poor",
    "existing_structure": "1995 ranch",
    "access": "limited"
  }
}
```

**Tech Stack**:
- `pdf2image` - PDF to images
- `pytesseract` - OCR
- `YOLO v8` or `SAM` - Computer vision (find tables)
- `spaCy` - Natural language parsing (extract specs)
- Output: Pydantic model in `packages/shared/models.py`

---

#### **STAGE 2: ENRICH (Add Regional Context)**

**Input**: Parsed components + Project ZIP code

**What Happens**:
1. Look up regional factors:
   - Labor rates by trade (carpenter, electrician, plumber)
   - Material cost index (varies by region)
   - Permitting delays/costs
   - Local code amendments
2. Cross-reference component database:
   - Match components to standard specs
   - Find manufacturer data sheets
   - Get typical pricing tiers
3. Flag any unusual requirements

**Output**:
```json
{
  "project_location": {
    "zip": "30601",
    "city": "Madison",
    "state": "GA",
    "region": "Southeast",
    "labor_rate_multiplier": 0.92,
    "material_cost_index": 0.95,
    "permitting_cost": "$850",
    "permitting_days": 14,
    "local_amendments": [
      "Georgia Energy Code 2023",
      "Madison Storm Water Ordinance",
      "Slope Stability (>20% grade)"
    ]
  },
  "components_enriched": [
    {
      "type": "Windows",
      "quantity": 12,
      "base_cost_per_unit": "$450",
      "regional_cost_per_unit": "$427.50",
      "labor_hours_per_unit": 2.5,
      "regional_labor_rate": "$65/hr",
      "material_cost_total": "$5,130",
      "labor_cost_total": "$1,950",
      "spec_database_reference": "WIN-1400-3X5-DP-LE",
      "energy_code_compliance": "IECC 2015 compliant"
    }
  ],
  "site_conditions_risk": {
    "terrain_slope": "CAUTION - site is sloped",
    "drainage_poor": "CAUTION - poor drainage noted",
    "existing_structure": "1995 = pre-code. May need foundation upgrade.",
    "access_limited": "CAUTION - limited site access. Add 15% labor multiplier"
  }
}
```

**Tech Stack**:
- PostgreSQL: `regional_factors` table (ZIP code lookup)
- Redis: Cache regional factors (fast lookup)
- Python: `services/pricing/regional_adjuster.py`

**Regional Factors Table**:
```sql
-- infra/db/schema.sql
CREATE TABLE regional_factors (
  zip_code VARCHAR(5) PRIMARY KEY,
  city VARCHAR(100),
  state VARCHAR(2),
  region VARCHAR(50),
  labor_rate_multiplier DECIMAL(3,2),
  material_cost_index DECIMAL(3,2),
  permitting_cost DECIMAL(10,2),
  permitting_days INT,
  flood_zone VARCHAR(10),
  snow_load INT,
  wind_speed INT,
  seismic_zone INT,
  local_amendments TEXT[],
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

#### **STAGE 3: CHECK (Compliance Rules)**

**Input**: Enriched components + Local codes + Site conditions

**What Happens**:
1. Run deterministic rule checks:
   - IRC 2018 structural requirements
   - IECC 2015 energy requirements
   - NEC 2017 electrical requirements
   - State amendments
2. For each rule, check if component passes
3. If FAILS → Flag as RED (stop work) or ORANGE (should fix)
4. Generate recommendation + code citation

**Output**:
```json
{
  "compliance_findings": [
    {
      "rule_id": "IRC-2018-R402.4",
      "rule_description": "Air barrier and thermal breaks required",
      "component": "Exterior walls - 1995 construction",
      "status": "FAIL",
      "severity": "ORANGE",
      "finding": "Original construction (1995) predates air sealing requirements. New additions must comply with current IECC 2015.",
      "recommendation": "Add continuous air barrier to exterior walls of addition using: (a) house wrap (Tyvek), (b) closed-cell foam, or (c) rigid insulation.",
      "cost_to_fix": "$1,200",
      "code_citation": "IECC 2015 Section 402.4.1.1 - Continuous Air Barrier",
      "location_in_plans": "Sheet A2.1, Details 3-5",
      "reference_link": "https://codes.iccsafe.org/content/icc-2015-iecc-m1"
    },
    {
      "rule_id": "IECC-2015-C402.3.6",
      "rule_description": "HVAC ductwork must be sealed",
      "component": "HVAC - Carrier 25HNB",
      "status": "PASS",
      "severity": "GREEN",
      "finding": "HVAC system is rated SEER 16, meets IECC 2015 minimum of SEER 14.",
      "recommendation": "Ensure ductwork is sealed at all joints with mastic sealant per IECC 2015.",
      "code_citation": "IECC 2015 Section C402.3.6 - HVAC Efficiency"
    },
    {
      "rule_id": "NEC-2017-210.52",
      "rule_description": "GFCI required for kitchen/bathroom receptacles",
      "component": "Electrical - Kitchen island",
      "status": "FAIL",
      "severity": "RED",
      "finding": "Kitchen island prep area requires GFCI protection. Plans show standard receptacles.",
      "recommendation": "Install GFCI-protected receptacles on kitchen island per NEC 2017 Article 210.52(C).",
      "cost_to_fix": "$150",
      "code_citation": "NEC 2017 Article 210.52(C)(1) - Kitchen Countertop Receptacles",
      "location_in_plans": "Sheet E1.2, Electrical plan"
    }
  ],
  "summary": {
    "total_checks_run": 47,
    "passed": 44,
    "failed": 3,
    "red_critical": 1,
    "orange_important": 1,
    "yellow_optional": 1
  }
}
```

**How to Implement Rules**:

```python
# services/rules/rules_engine.py

from dataclasses import dataclass
from typing import List, Literal

@dataclass
class Rule:
    rule_id: str
    code: str  # "IRC-2018", "IECC-2015", "NEC-2017", "GA-Amendment"
    section: str  # "R402.4", etc.
    title: str
    check_function: callable
    severity: Literal["RED", "ORANGE", "YELLOW"]
    
class RulesEngine:
    def __init__(self):
        self.rules: List[Rule] = [
            Rule(
                rule_id="IECC-2015-C402.3.6",
                code="IECC-2015",
                section="C402.3.6",
                title="HVAC System must meet SEER rating",
                check_function=self.check_hvac_seer,
                severity="RED"
            ),
            Rule(
                rule_id="NEC-2017-210.52",
                code="NEC-2017",
                section="210.52",
                title="Kitchen receptacles must have GFCI",
                check_function=self.check_kitchen_gfci,
                severity="RED"
            ),
            # ... 50+ more rules
        ]
    
    def check_hvac_seer(self, component: dict) -> tuple[bool, str]:
        """Check if HVAC meets SEER 14+ requirement"""
        if component["type"] != "HVAC System":
            return True, "Not applicable"
        
        seer = component.get("seer_rating", 0)
        if seer >= 14:
            return True, f"SEER {seer} meets requirement"
        else:
            return False, f"SEER {seer} below minimum of 14"
    
    def check_kitchen_gfci(self, component: dict) -> tuple[bool, str]:
        """Check if kitchen receptacles have GFCI"""
        if component["type"] != "Electrical" or "kitchen" not in component.get("location", "").lower():
            return True, "Not applicable"
        
        has_gfci = component.get("gfci_protected", False)
        if has_gfci:
            return True, "Kitchen receptacles are GFCI protected"
        else:
            return False, "Kitchen receptacles missing GFCI protection"
    
    def run_all_checks(self, components: List[dict], jurisdiction: str) -> List[dict]:
        """Run all applicable rules for jurisdiction"""
        findings = []
        
        for rule in self.rules:
            # Filter by jurisdiction
            if jurisdiction == "GA" and "GA-" not in rule.rule_id:
                continue
            
            for component in components:
                passed, message = rule.check_function(component)
                
                if not passed:  # Only log failures
                    findings.append({
                        "rule_id": rule.rule_id,
                        "component": component.get("type"),
                        "status": "FAIL",
                        "severity": rule.severity,
                        "finding": message,
                        "code_citation": f"{rule.code} Section {rule.section} - {rule.title}"
                    })
        
        return findings

# Usage
engine = RulesEngine()
findings = engine.run_all_checks(
    components=[hvac_component, window_component, electrical_component],
    jurisdiction="GA"
)
```

**Tech Stack**:
- Python: `services/rules/rules_engine.py` + `rules_database.py`
- PostgreSQL: Store rule definitions + code citations
- Fast path: Return results in <1 second for standard checks

---

#### **STAGE 4: ESTIMATE (Calculate Costs)**

**Input**: Enriched components + Compliance findings + Regional factors

**What Happens**:
1. Calculate material cost (per component)
2. Calculate labor cost (per component)
3. Add regional adjustments
4. Add O&P (overhead & profit)
5. Add permitting/inspection costs
6. Generate cost breakdown

**Output**:
```json
{
  "estimate_summary": {
    "project_name": "Smith Residence Addition",
    "address": "123 Oak Street, Madison, GA 30601",
    "total_estimate": "$52,450",
    "breakdown": {
      "materials": "$28,300",
      "labor": "$16,850",
      "permits_fees": "$950",
      "contingency": "$2,800",
      "overhead_profit": "$3,550"
    }
  },
  "line_items": [
    {
      "item_number": 1,
      "description": "Windows - Double pane vinyl, Anderson 400 series 3'x5'",
      "quantity": 12,
      "unit": "Each",
      "unit_cost": "$427.50",
      "labor_hours": 2.5,
      "labor_rate": "$65/hr",
      "labor_cost_per_unit": "$162.50",
      "material_cost_total": "$5,130",
      "labor_cost_total": "$1,950",
      "line_total": "$7,080",
      "notes": "IECC 2015 compliant, Low-E, Argon gas"
    },
    {
      "item_number": 2,
      "description": "HVAC - Carrier 25HNB central air, 2.5 ton, SEER 16",
      "quantity": 1,
      "unit": "Unit",
      "unit_cost": "$4,200",
      "labor_hours": 16,
      "labor_rate": "$75/hr (HVAC tech)",
      "labor_cost": "$1,200",
      "material_cost": "$4,200",
      "line_total": "$5,400",
      "notes": "Exceeds IECC requirement, ductwork sealing per code"
    },
    {
      "item_number": 3,
      "description": "Exterior walls - Stud framing, insulation, air barrier, drywall",
      "quantity": 800,
      "unit": "SF",
      "unit_cost": "$18.50/SF",
      "labor_hours": 0.45,
      "labor_rate": "$55/hr",
      "labor_cost_per_unit": "$24.75/SF",
      "material_cost_total": "$14,800",
      "labor_cost_total": "$9,900",
      "line_total": "$24,700",
      "notes": "Includes continuous air barrier (Tyvek), R-21 insulation"
    }
  ],
  "cost_adjustments": {
    "regional_labor_multiplier": 0.92,
    "regional_material_index": 0.95,
    "site_complexity": {
      "factor": 1.10,
      "reason": "Sloped terrain, limited access, poor drainage"
    },
    "existing_structure_adjustment": {
      "factor": 1.05,
      "reason": "1995 construction - may have compatibility issues"
    }
  },
  "contingency": {
    "percentage": 10,
    "reason": "Standard for renovation work with existing structure",
    "amount": "$2,800"
  }
}
```

**How to Implement Pricing**:

```python
# services/pricing/estimator.py

from decimal import Decimal
from typing import List, Dict

class EstimateCalculator:
    def __init__(self, tradebase_client, regional_db):
        self.tradebase = tradebase_client  # Third-party pricing API
        self.regional_db = regional_db     # PostgreSQL regional factors
    
    def calculate_line_item(self, component: dict, location: dict) -> dict:
        """Calculate cost for a single component"""
        
        # 1. Get base pricing from TradeBase (material + labor)
        base_estimate = self.tradebase.estimate(
            component_type=component["type"],
            specification=component["specification"],
            quantity=component["quantity"]
        )
        # Returns: {"material": 5000, "labor_hours": 20, "labor_rate": 65}
        
        # 2. Apply regional adjustments
        regional_labor_multiplier = self.regional_db.get_labor_multiplier(
            location["zip"]
        )
        regional_material_index = self.regional_db.get_material_index(
            location["zip"]
        )
        
        adjusted_labor_rate = base_estimate["labor_rate"] * regional_labor_multiplier
        adjusted_material = base_estimate["material"] * regional_material_index
        adjusted_labor_cost = (
            base_estimate["labor_hours"] * adjusted_labor_rate
        )
        
        # 3. Add site complexity adjustments
        site_complexity_factor = self._calculate_site_complexity(
            component, location
        )
        adjusted_labor_cost *= site_complexity_factor
        
        # 4. Calculate O&P (typically 20% for contractors)
        op_rate = 0.20  # 20% overhead & profit
        total_before_op = adjusted_material + adjusted_labor_cost
        op_amount = total_before_op * op_rate
        
        return {
            "item_number": component["id"],
            "description": f"{component['type']} - {component['specification']}",
            "quantity": component["quantity"],
            "unit": component["unit"],
            "base_material_cost": base_estimate["material"],
            "adjusted_material_cost": adjusted_material,
            "base_labor_hours": base_estimate["labor_hours"],
            "adjusted_labor_rate": adjusted_labor_rate,
            "adjusted_labor_cost": adjusted_labor_cost,
            "subtotal": total_before_op,
            "overhead_profit_amount": op_amount,
            "line_total": total_before_op + op_amount,
            "regional_labor_multiplier": regional_labor_multiplier,
            "regional_material_index": regional_material_index,
            "site_complexity_factor": site_complexity_factor
        }
    
    def _calculate_site_complexity(self, component: dict, location: dict) -> float:
        """Calculate site complexity multiplier"""
        multiplier = 1.0
        
        # Sloped terrain
        if location.get("terrain") == "sloped":
            multiplier *= 1.10
        
        # Poor drainage
        if location.get("drainage") == "poor":
            multiplier *= 1.08
        
        # Limited access
        if location.get("access") == "limited":
            multiplier *= 1.12
        
        # Existing structure compatibility
        if location.get("year_built", 2025) < 2000:
            multiplier *= 1.05
        
        return multiplier
    
    def calculate_full_estimate(
        self, 
        components: List[dict], 
        location: dict,
        compliance_findings: List[dict]
    ) -> dict:
        """Calculate complete estimate"""
        
        line_items = []
        for component in components:
            line_item = self.calculate_line_item(component, location)
            line_items.append(line_item)
        
        # Calculate totals
        material_total = sum(li["adjusted_material_cost"] for li in line_items)
        labor_total = sum(li["adjusted_labor_cost"] for li in line_items)
        op_total = sum(li["overhead_profit_amount"] for li in line_items)
        
        # Add permits and inspection
        permit_cost = self.regional_db.get_permit_cost(location["zip"])
        
        # Add contingency (10% for renovations, 5% for new construction)
        contingency_percent = 0.10 if location.get("existing_structure") else 0.05
        subtotal = material_total + labor_total + op_total + permit_cost
        contingency = subtotal * contingency_percent
        
        total = subtotal + contingency
        
        # Add compliance fix costs
        compliance_cost = sum(
            Decimal(finding.get("cost_to_fix", 0))
            for finding in compliance_findings
        )
        total += compliance_cost
        
        return {
            "line_items": line_items,
            "summary": {
                "materials": material_total,
                "labor": labor_total,
                "overhead_profit": op_total,
                "permits_fees": permit_cost,
                "compliance_fixes": compliance_cost,
                "subtotal": subtotal,
                "contingency": contingency,
                "total": total
            }
        }

# Usage
calculator = EstimateCalculator(tradebase_client, regional_db)
estimate = calculator.calculate_full_estimate(
    components=parsed_components,
    location=project_location,
    compliance_findings=compliance_findings
)
```

**Pricing Data Sources**:
- **TradeBase** (paid API): $0.10-$0.50 per lookup, most accurate
- **RS Means** (annual subscription): $800/year, good for commercial
- **Build-it**: Free regional pricing data
- **Your own database**: Collect from past jobs (most accurate long-term)

**Tech Stack**:
- FastAPI microservice: `services/pricing/`
- PostgreSQL: Material prices, labor rates by trade
- Redis: Cache pricing lookups (TTL: 24 hours)
- Third-party: TradeBase API for real-time pricing

---

#### **STAGE 5: GENERATE (Create Deliverables)**

**Input**: Estimate + Compliance findings + Project info

**What Happens**:
1. Generate Excel file with findings + estimates
2. Generate professional PDF proposal
3. Generate Xactimate CSV (ready for GC)
4. Generate compliance report

**Output**: 4 files ready to email

```python
# services/reports/report_generator.py

from jinja2 import Environment, FileSystemLoader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, PageBreak
import openpyxl
import csv

class ReportGenerator:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader('templates/')
        )
    
    def generate_excel(self, estimate: dict, findings: list) -> bytes:
        """Generate Excel file with estimate + findings"""
        
        wb = openpyxl.Workbook()
        
        # Sheet 1: Project Info
        ws_project = wb.active
        ws_project.title = "PROJECT_INFO"
        ws_project['A1'] = "Project Name"
        ws_project['B1'] = estimate["project_name"]
        ws_project['A2'] = "Address"
        ws_project['B2'] = estimate["address"]
        # ... populate rest
        
        # Sheet 2: Estimate Line Items
        ws_estimate = wb.create_sheet("ESTIMATE")
        ws_estimate['A1'] = "Item"
        ws_estimate['B1'] = "Description"
        ws_estimate['C1'] = "Qty"
        ws_estimate['D1'] = "Unit"
        ws_estimate['E1'] = "Unit Cost"
        ws_estimate['F1'] = "Total"
        
        for idx, line_item in enumerate(estimate["line_items"], 2):
            ws_estimate[f'A{idx}'] = line_item["item_number"]
            ws_estimate[f'B{idx}'] = line_item["description"]
            ws_estimate[f'C{idx}'] = line_item["quantity"]
            ws_estimate[f'D{idx}'] = line_item["unit"]
            ws_estimate[f'E{idx}'] = line_item["unit_cost"]
            ws_estimate[f'F{idx}'] = line_item["line_total"]
        
        # Sheet 3: Compliance Findings
        ws_findings = wb.create_sheet("FINDINGS")
        ws_findings['A1'] = "Code"
        ws_findings['B1'] = "Rule"
        ws_findings['C1'] = "Status"
        ws_findings['D1'] = "Severity"
        ws_findings['E1'] = "Finding"
        ws_findings['F1'] = "Recommendation"
        ws_findings['G1'] = "Cost to Fix"
        
        for idx, finding in enumerate(findings, 2):
            ws_findings[f'A{idx}'] = finding["rule_id"]
            ws_findings[f'B{idx}'] = finding["rule_description"]
            ws_findings[f'C{idx}'] = finding["status"]
            ws_findings[f'D{idx}'] = finding["severity"]
            ws_findings[f'E{idx}'] = finding["finding"]
            ws_findings[f'F{idx}'] = finding["recommendation"]
            ws_findings[f'G{idx}'] = finding["cost_to_fix"]
        
        # Save to bytes
        from io import BytesIO
        output = BytesIO()
        wb.save(output)
        return output.getvalue()
    
    def generate_pdf_proposal(self, estimate: dict, findings: list) -> bytes:
        """Generate professional PDF proposal"""
        
        template = self.env.get_template('proposal_comprehensive.pdf.j2')
        
        # Render Jinja2 template with data
        html_content = template.render(
            project_name=estimate["project_name"],
            address=estimate["address"],
            line_items=estimate["line_items"],
            total=estimate["summary"]["total"],
            findings=findings,
            estimate_date="November 1, 2025",
            valid_until="November 30, 2025"
        )
        
        # Convert HTML to PDF using WeasyPrint
        from weasyprint import HTML, CSS
        pdf_bytes = HTML(string=html_content).write_pdf()
        
        return pdf_bytes
    
    def generate_xactimate_csv(self, estimate: dict) -> str:
        """Generate CSV in Xactimate format"""
        
        output = []
        output.append("Line#,Item,Qty,Unit,Unit Price,Total,Labor Hrs,Rate,Description")
        
        for line_item in estimate["line_items"]:
            row = [
                line_item["item_number"],
                line_item["description"],
                line_item["quantity"],
                line_item["unit"],
                line_item["unit_cost"],
                line_item["line_total"],
                line_item.get("labor_hours", 0),
                line_item.get("labor_rate", 0),
                line_item.get("notes", "")
            ]
            output.append(",".join(str(x) for x in row))
        
        return "\n".join(output)

# Usage
generator = ReportGenerator()
excel_bytes = generator.generate_excel(estimate, findings)
pdf_bytes = generator.generate_pdf_proposal(estimate, findings)
csv_content = generator.generate_xactimate_csv(estimate)
```

**Tech Stack**:
- Jinja2 templates (in `templates/` folder)
- ReportLab or WeasyPrint for PDF generation
- openpyxl for Excel
- Python CSV module

---

## PART 2: HOW TO BUILD IT (Step-by-Step Implementation)

### Phase 1: Foundation (Week 1-2)

**Goal**: Get the pipeline running end-to-end

```bash
# Step 1: Create project structure
mkdir -p services/{api,parser,rules,pricing,reports}
mkdir -p packages/shared/models
mkdir -p templates
mkdir -p infra/db
mkdir -p apps/web

# Step 2: Create backend Docker structure
cat > services/parser/Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libpoppler-cpp-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
EOF

# Step 3: Build services
cd services/parser
pip install -r requirements.txt
python -m pytest tests/  # Run tests
```

**Files to Create**:

1. **`packages/shared/models.py`** - Shared data models
```python
from pydantic import BaseModel
from typing import List, Optional

class Component(BaseModel):
    type: str
    quantity: float
    unit: str
    size: Optional[str]
    material: Optional[str]
    model: Optional[str]
    location: str
    confidence: float

class ProjectInfo(BaseModel):
    name: str
    address: str
    zip_code: str
    city: str
    state: str
    jurisdiction: str

class EstimateLineItem(BaseModel):
    item_number: int
    description: str
    quantity: float
    unit_cost: float
    labor_hours: float
    labor_rate: float
    line_total: float
```

2. **`services/parser/app.py`** - Parser microservice
```python
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pdf2image
import pytesseract
import json

app = FastAPI()

@app.post("/parse-pdf/")
async def parse_pdf(file: UploadFile = File(...)):
    """Parse PDF and extract components"""
    
    # Convert PDF to images
    pdf_path = f"/tmp/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())
    
    images = pdf2image.convert_from_path(pdf_path)
    
    # Run OCR on each page
    text_by_page = []
    for image in images:
        text = pytesseract.image_to_string(image)
        text_by_page.append(text)
    
    # Parse text to find components (AI model)
    components = extract_components(text_by_page)
    
    return {
        "pages": len(images),
        "components": components,
        "raw_text": text_by_page
    }

def extract_components(text_by_page: list) -> list:
    """Use regex or LLM to extract components from text"""
    # TODO: Implement extraction logic
    pass
```

3. **`services/api/main.py`** - Orchestration API
```python
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import httpx
import json

app = FastAPI()

PARSER_URL = "http://parser:8001"
RULES_URL = "http://rules:8002"
PRICING_URL = "http://pricing:8003"
REPORTS_URL = "http://reports:8004"

@app.post("/analyze")
async def analyze_project(
    project_id: str,
    file_urls: dict,  # {"pdf": "s3://...", "excel": "s3://..."}
    background_tasks: BackgroundTasks
):
    """Main analysis workflow"""
    
    # Stage 1: Parse
    parser_response = await httpx.post(
        f"{PARSER_URL}/parse-pdf/",
        files={"file": open(file_urls["pdf"], "rb")}
    )
    components = parser_response.json()["components"]
    
    # Stage 2: Enrich
    pricing_response = await httpx.post(
        f"{PRICING_URL}/enrich/",
        json={"components": components, "zip": project_id}
    )
    enriched = pricing_response.json()
    
    # Stage 3: Check compliance
    rules_response = await httpx.post(
        f"{RULES_URL}/check/",
        json={"components": enriched["components"], "jurisdiction": "GA"}
    )
    findings = rules_response.json()["findings"]
    
    # Stage 4: Calculate estimate
    estimate_response = await httpx.post(
        f"{PRICING_URL}/estimate/",
        json={"components": enriched, "findings": findings}
    )
    estimate = estimate_response.json()
    
    # Stage 5: Generate reports (background)
    background_tasks.add_task(
        generate_reports,
        project_id=project_id,
        estimate=estimate,
        findings=findings
    )
    
    return {
        "status": "processing",
        "project_id": project_id,
        "message": "Analysis started. Check status for results."
    }

async def generate_reports(project_id: str, estimate: dict, findings: list):
    """Generate all reports"""
    
    reports_response = await httpx.post(
        f"{REPORTS_URL}/generate-all/",
        json={"estimate": estimate, "findings": findings, "project_id": project_id}
    )
    
    # Save to S3
    reports = reports_response.json()
    # ... upload files
```

---

### Phase 2: Build Out Parser Service (Week 3)

**Goal**: Extract components from PDFs accurately

```python
# services/parser/extraction_engine.py

import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from typing import List, Dict

class ComponentExtractor:
    def __init__(self, yolo_model_path="models/yolo_tables.pt"):
        """Initialize with YOLO model for table detection"""
        import torch
        self.model = torch.hub.load('ultralytics/yolov8', 'custom', 
                                     path=yolo_model_path)
    
    def extract_from_pdf(self, pdf_path: str) -> Dict:
        """Full extraction pipeline"""
        
        # Convert to images
        images = self._pdf_to_images(pdf_path)
        
        all_components = []
        for page_num, image in enumerate(images):
            # Find tables
            tables = self._detect_tables(image)
            
            # OCR on each table
            for table_coords in tables:
                table_image = image.crop(table_coords)
                table_text = pytesseract.image_to_string(table_image)
                components = self._parse_table(table_text)
                all_components.extend(components)
            
            # Also find text annotations
            page_text = pytesseract.image_to_string(image)
            annotations = self._parse_annotations(page_text)
            all_components.extend(annotations)
        
        return {
            "components": all_components,
            "page_count": len(images),
            "confidence": self._calculate_confidence(all_components)
        }
    
    def _detect_tables(self, image: Image) -> List[tuple]:
        """Use YOLO to find tables in image"""
        results = self.model(image)
        tables = []
        
        for detection in results.xyxy[0]:
            x1, y1, x2, y2, conf, _ = detection
            if conf > 0.7:  # Confidence threshold
                tables.append((int(x1), int(y1), int(x2), int(y2)))
        
        return tables
    
    def _parse_table(self, text: str) -> List[dict]:
        """Parse table text into components"""
        
        # Try to detect table structure
        lines = text.split('\n')
        components = []
        
        # Look for patterns like "Windows | 12 | 3'x5' | Vinyl"
        pattern = r'(\w+)\s+\|\s+(\d+)\s+\|\s+([\d\'\x\"]+)\s+\|\s+(.*)'
        
        for line in lines:
            match = re.match(pattern, line)
            if match:
                component_type, qty, size, specs = match.groups()
                components.append({
                    "type": component_type.strip(),
                    "quantity": int(qty),
                    "size": size.strip(),
                    "specification": specs.strip()
                })
        
        return components
    
    def _parse_annotations(self, text: str) -> List[dict]:
        """Parse drawing annotations for specs"""
        
        components = []
        
        # Look for common patterns
        patterns = {
            "windows": r'(\d+)\s*[Ww]indows?.*?(\d+\'x\d+\')?.*?(vinyl|wood|aluminum)?',
            "doors": r'(\d+)\s*[Dd]oors?.*?(\d+\'x\d+\')?',
            "hvac": r'HVAC.*?(\d\.?\d*\s*ton)',
            "roofing": r'(\d+)\s*[Ss]quare?.*?roofing',
        }
        
        for comp_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                components.append({
                    "type": comp_type.title(),
                    "quantity": int(match.group(1)),
                    "specification": match.group(0),
                    "confidence": 0.7  # Lower confidence for annotations
                })
        
        return components

# Usage
extractor = ComponentExtractor()
result = extractor.extract_from_pdf("project_plans.pdf")
print(f"Found {len(result['components'])} components")
```

---

### Phase 3: Build Rules Engine (Week 4)

**Goal**: Implement compliance checking

```python
# services/rules/rules_database.py

RULE_DEFINITIONS = {
    "IECC-2015-C402.3.6": {
        "code": "IECC 2015",
        "section": "C402.3.6",
        "title": "HVAC System Efficiency",
        "description": "HVAC systems must meet minimum SEER rating",
        "applies_to": ["HVAC System"],
        "check": lambda comp: comp.get("seer_rating", 0) >= 14,
        "fail_message": lambda comp: f"SEER {comp.get('seer_rating', '?')} is below minimum of 14",
        "fix_message": "Upgrade HVAC to SEER 14+ rated unit",
        "severity": "RED",
        "cost_to_fix": 1500,
        "citations": ["https://codes.iccsafe.org/content/icc-2015-iecc-c402"]
    },
    "NEC-2017-210.52": {
        "code": "NEC 2017",
        "section": "210.52",
        "title": "Kitchen Countertop Receptacles",
        "description": "GFCI protection required for kitchen receptacles",
        "applies_to": ["Electrical"],
        "check": lambda comp: comp.get("gfci_protected", False) if "kitchen" in comp.get("location", "").lower() else True,
        "fail_message": "Kitchen receptacles lack GFCI protection",
        "fix_message": "Install GFCI-protected receptacles per NEC 210.52(C)",
        "severity": "RED",
        "cost_to_fix": 150,
        "citations": ["https://www.nfpa.org/codes-and-standards"]
    },
    "IRC-2018-R402.4": {
        "code": "IRC 2018",
        "section": "R402.4",
        "title": "Air Barrier and Thermal Breaks",
        "description": "Continuous air barrier required for exterior walls",
        "applies_to": ["Exterior walls", "Roofing"],
        "check": lambda comp: comp.get("air_barrier", False) if "exterior" in comp.get("location", "").lower() else True,
        "fail_message": "Exterior walls missing continuous air barrier",
        "fix_message": "Install house wrap or rigid insulation for continuous air barrier",
        "severity": "ORANGE",
        "cost_to_fix": 1200,
        "citations": ["https://codes.iccsafe.org/content/icc-2018-irc"]
    }
}

# services/rules/rules_engine.py

class RulesEngine:
    def __init__(self, jurisdiction="GA"):
        self.jurisdiction = jurisdiction
        self.rules = RULE_DEFINITIONS
    
    def check_component(self, component: dict) -> List[dict]:
        """Check component against all applicable rules"""
        
        findings = []
        
        for rule_id, rule in self.rules.items():
            # Check if rule applies to this component type
            applies = any(
                comp_type.lower() in component.get("type", "").lower()
                for comp_type in rule["applies_to"]
            )
            
            if not applies:
                continue
            
            # Run check
            passed = rule["check"](component)
            
            if not passed:
                findings.append({
                    "rule_id": rule_id,
                    "code": rule["code"],
                    "section": rule["section"],
                    "title": rule["title"],
                    "component": component.get("type"),
                    "status": "FAIL",
                    "severity": rule["severity"],
                    "finding": rule["fail_message"](component),
                    "recommendation": rule["fix_message"],
                    "cost_to_fix": rule["cost_to_fix"],
                    "citations": rule["citations"]
                })
        
        return findings

# FastAPI endpoint
@app.post("/check-compliance")
async def check_compliance(components: List[dict], jurisdiction: str = "GA"):
    engine = RulesEngine(jurisdiction)
    all_findings = []
    
    for component in components:
        findings = engine.check_component(component)
        all_findings.extend(findings)
    
    return {
        "total_checked": len(components),
        "findings_count": len(all_findings),
        "findings": all_findings
    }
```

---

### Phase 4: Build Pricing Service (Week 5)

**Goal**: Calculate accurate costs with regional adjustments

```python
# services/pricing/regional_db.py

import pandas as pd
from sqlalchemy import create_engine

class RegionalPricingDB:
    def __init__(self, db_url="postgresql://user:pass@db:5432/eagle_eye"):
        self.engine = create_engine(db_url)
    
    def get_regional_factors(self, zip_code: str) -> dict:
        """Look up regional factors for ZIP code"""
        
        query = f"""
        SELECT 
            zip_code, city, state, region,
            labor_rate_multiplier,
            material_cost_index,
            permitting_cost,
            permitting_days,
            snow_load, wind_speed, seismic_zone
        FROM regional_factors
        WHERE zip_code = '{zip_code}'
        """
        
        result = pd.read_sql(query, self.engine)
        if result.empty:
            # Return defaults if not found
            return {
                "labor_rate_multiplier": 1.0,
                "material_cost_index": 1.0,
                "permitting_cost": 500,
                "snow_load": 0,
                "wind_speed": 100
            }
        
        return result.iloc[0].to_dict()

# services/pricing/estimator.py

class PricingEngine:
    def __init__(self, regional_db):
        self.regional_db = regional_db
        self.tradebase = TradeBaseAPI(api_key="...")  # Third-party pricing
    
    def estimate_component(self, component: dict, zip_code: str) -> dict:
        """Get price for a single component"""
        
        # 1. Base pricing from TradeBase
        base = self.tradebase.get_pricing(
            component_type=component["type"],
            specification=component["specification"],
            quantity=component["quantity"]
        )
        # Returns: {
        #   "material_total": 5000,
        #   "labor_hours": 20,
        #   "base_labor_rate": 65
        # }
        
        # 2. Regional adjustments
        regional = self.regional_db.get_regional_factors(zip_code)
        
        adjusted_labor_rate = (
            base["base_labor_rate"] * regional["labor_rate_multiplier"]
        )
        adjusted_labor_cost = (
            base["labor_hours"] * adjusted_labor_rate
        )
        adjusted_material = (
            base["material_total"] * regional["material_cost_index"]
        )
        
        # 3. Overhead & Profit (20%)
        op_rate = 0.20
        subtotal = adjusted_material + adjusted_labor_cost
        op_cost = subtotal * op_rate
        
        return {
            "component_type": component["type"],
            "quantity": component["quantity"],
            "base_material": base["material_total"],
            "adjusted_material": adjusted_material,
            "labor_hours": base["labor_hours"],
            "base_labor_rate": base["base_labor_rate"],
            "adjusted_labor_rate": adjusted_labor_rate,
            "adjusted_labor_cost": adjusted_labor_cost,
            "subtotal": subtotal,
            "overhead_profit": op_cost,
            "total": subtotal + op_cost,
            "regional_multiplier_labor": regional["labor_rate_multiplier"],
            "regional_multiplier_material": regional["material_cost_index"]
        }
```

---

### Phase 5: Generate Reports (Week 6)

**Goal**: Create professional PDF + Excel outputs

See Stage 5 above for implementation.

---

## PART 3: How to Make Customers BLOWN AWAY (The Wow Factor)

### First Estimate Strategy

**Key**: Make the first estimate so impressive they feel like they're getting a premium service

```
┌─────────────────────────────────────────────────────────────┐
│                    CUSTOMER UPLOADS PDF                     │
│            (They've never used Eagle Eye before)             │
└─────────────────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
    5 MIN LATER:            WHAT THEY GET:
    "Your analysis       ✅ Excel with all components extracted
     is complete!"       ✅ Professional PDF proposal ($X price)
                         ✅ 3 code compliance issues found
                         ✅ Specific fixes + costs for each
                         ✅ Xactimate-ready export
                         ✅ Ready to send to client TODAY
                         
REACTION: "How did you do this in 5 minutes?
          It usually takes us 3-4 DAYS!"
```

### Design Principles for Wow Factor

**1. Speed** - Show results in real-time
```python
# In API response, stream progress updates
from fastapi.responses import StreamingResponse
import json

@app.post("/analyze-stream")
async def analyze_stream(project_id: str):
    async def event_generator():
        # Stage 1
        yield f"data: {json.dumps({'stage': 1, 'message': 'Extracting from PDFs...'})}\n\n"
        # ... do work
        
        # Stage 2
        yield f"data: {json.dumps({'stage': 2, 'message': 'Enriching regional data...'})}\n\n"
        # ... do work
        
        # Stage 3
        yield f"data: {json.dumps({'stage': 3, 'message': 'Checking compliance...'})}\n\n"
        # ... do work
        
        # Complete
        yield f"data: {json.dumps({'stage': 'complete', 'url': 'download_url'})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**2. Accuracy** - Show detailed breakdowns
```
Project: Smith Residence Addition
Estimate Breakdown:

MATERIALS ($28,300)
├─ Windows (12 @ $427.50)        $5,130
├─ HVAC System (1 @ $4,200)      $4,200
├─ Roofing (2,400 SF @ $8.50)   $20,400
├─ Misc materials                 ... (itemized)
└─ Regional factor: 0.95x

LABOR ($16,850)
├─ Carpentry (120 hrs @ $65)    $7,800
├─ HVAC technician (16 hrs @ $75) $1,200
├─ Electrician (20 hrs @ $80)   $1,600
├─ General labor (40 hrs @ $45)  $1,800
├─ Project management (8 hrs)    $600
└─ Regional factor: 0.92x (saving $800!)

OVERHEAD & PROFIT (20%)          $8,850

PERMITS & FEES                    $950

CONTINGENCY (10%)                 $2,800

CODE COMPLIANCE FIXES             $1,650
├─ GFCI upgrade                   $150
├─ Air sealing                    $1,200
├─ Truss documentation            $300

TOTAL ESTIMATE                    $60,450
```

**3. Professionalism** - PDF should look like it was hand-done
```
┌──────────────────────────────────────────┐
│                                          │
│           EAGLE EYE ESTIMATE             │
│        Construction Plan Analysis        │
│                                          │
│  Project: Smith Residence Addition      │
│  Address: 123 Oak Street                │
│           Madison, GA 30601             │
│  Prepared: November 1, 2025             │
│  Valid Until: November 30, 2025         │
│                                          │
├──────────────────────────────────────────┤
│                                          │
│  EXECUTIVE SUMMARY                      │
│                                          │
│  Project Scope:                         │
│    • 800 SF addition to existing home   │
│    • New HVAC system (2.5 ton)          │
│    • Complete roofing replacement      │
│                                          │
│  Total Estimate: $60,450                │
│  Materials: $28,300  Labor: $16,850     │
│  Permits: $950       Contingency: $2,800│
│                                          │
│  Code Compliance: 3 items noted         │
│    1 Critical (GFCI)                    │
│    1 Important (Air sealing)            │
│    1 Information (Truss docs)           │
│                                          │
│  RECOMMENDED ACTION:                    │
│    ✓ All estimates are complete        │
│    ✓ Code issues can be fixed in-scope │
│    ✓ Ready to proceed with bidding     │
│                                          │
├──────────────────────────────────────────┤
│                                          │
│  [DETAILED LINE ITEMS]                  │
│  [COMPLIANCE REPORT]                    │
│  [TERMS & CONDITIONS]                   │
│                                          │
└──────────────────────────────────────────┘
```

**4. Value-Add Features** - Things that surprise and delight

```python
# Auto-include these in every estimate:

COMPLIANCE_BONUS = """
🛡️ CODE COMPLIANCE REPORT (Usually costs $500+)
   • All code references with locations
   • Specific recommendations
   • Links to code sections
   • Ready for lender/inspector review
"""

REGIONAL_SAVINGS = """
💰 REGIONAL PRICING OPTIMIZATION
   Your region: Georgia (Southeast)
   Labor rate multiplier: 0.92x
   Material index: 0.95x
   Estimated savings vs. national average: $2,400
"""

CONTINGENCY_GUIDANCE = """
⚠️ CONTINGENCY ANALYSIS
   Recommended contingency: 10% ($2,800)
   Reason: Renovation + existing structure (1995)
   
   If you prefer 5% contingency: $1,400 (tighter budget)
   If you prefer 15% contingency: $4,200 (safer estimate)
"""

PAYMENT_SCHEDULE = """
📋 SUGGESTED PAYMENT SCHEDULE
   Initial deposit: $15,000 (25%) - Upon contract
   1st draw: $15,000 (25%) - Rough-in stage
   2nd draw: $15,000 (25%) - Close-in stage
   Final: $15,450 (25%) - Completion
"""
```

---

## PART 4: Deployment Architecture

### Local Development (Week 1)

```bash
# Docker Compose local dev stack
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: dev123
      POSTGRES_DB: eagle_eye
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  parser:
    build: ./services/parser
    ports:
      - "8001:8000"
    environment:
      DATABASE_URL: postgresql://postgres:dev123@db:5432/eagle_eye
      REDIS_URL: redis://redis:6379

  rules:
    build: ./services/rules
    ports:
      - "8002:8000"
    environment:
      DATABASE_URL: postgresql://postgres:dev123@db:5432/eagle_eye

  pricing:
    build: ./services/pricing
    ports:
      - "8003:8000"
    environment:
      DATABASE_URL: postgresql://postgres:dev123@db:5432/eagle_eye
      TRADEBASE_API_KEY: ${TRADEBASE_API_KEY}

  reports:
    build: ./services/reports
    ports:
      - "8004:8000"

  api:
    build: ./services/api
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
      - parser
      - rules
      - pricing
      - reports

  web:
    build: ./apps/web
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
```

### Production Deployment (Week 8+)

```yaml
# Kubernetes deployment (if scaling)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: parser-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: parser
  template:
    metadata:
      labels:
        app: parser
    spec:
      containers:
      - name: parser
        image: eagle-eye/parser:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

---

## PART 5: Customer Success Timeline

### Day 1 (First Estimate)

```
09:00 AM - Customer receives email: "Upload your plans to get started"
09:05 AM - Customer uploads PDF + Excel template
09:10 AM - Email received: "Analysis in progress... [████░░░░░░] 40%"
09:15 AM - Email received: "Analysis complete! Download your results"
09:16 AM - Customer opens PDF proposal
09:18 AM - Reaction: "Wow! This took you 10 minutes??"
09:19 AM - Customer emails to contractor/client
09:20 AM - YOU'VE WON THE BID (vs. competitor who takes 3-4 days)
```

### Week 1-2 (Adoption)

```
✓ Team learns how to use system (30 min training)
✓ First 5 estimates generated (saves 50 hours)
✓ Clients impressed with speed
✓ 90% faster turnaround vs. before
✓ Team freed up for higher-value work
```

### Month 1

```
✓ 50+ estimates generated
✓ $25,000+ in labor hours saved
✓ Can take on projects that were previously backlogged
✓ Increase in proposal conversion rate (faster = more professional)
```

### Year 1

```
✓ 500+ estimates generated
✓ 3x more capacity with same team
✓ $30,000+ in annual savings
✓ System paid for itself 20x over
✓ Competitive advantage: "We give you estimates in 5-10 minutes"
```

---

## NEXT STEPS: Start Building

### Minimum Viable Product (MVP) - 2 weeks

Focus on just the core loop:
1. Upload PDF
2. Extract components (basic regex)
3. Calculate costs (simple pricing DB)
4. Generate Excel + PDF

```python
# MVP: Bare minimum version
# Can be built in 2 weeks with 1-2 developers

@app.post("/simple-estimate")
async def simple_estimate(
    pdf_file: UploadFile,
    zip_code: str,
    jurisdiction: str = "GA"
):
    """MVP: Simple end-to-end estimate"""
    
    # Step 1: Parse PDF (simple regex + OCR)
    pdf_path = save_file(pdf_file)
    components = extract_components_simple(pdf_path)
    
    # Step 2: Get regional pricing
    regional_factors = get_regional_pricing(zip_code)
    
    # Step 3: Calculate costs
    estimate = calculate_costs(components, regional_factors)
    
    # Step 4: Check basic compliance
    findings = check_basic_compliance(components, jurisdiction)
    
    # Step 5: Generate Excel + PDF
    excel_file = generate_excel(estimate, findings)
    pdf_file = generate_pdf(estimate, findings)
    
    return {
        "estimate": estimate,
        "findings": findings,
        "download_urls": {
            "excel": f"s3://bucket/{project_id}.xlsx",
            "pdf": f"s3://bucket/{project_id}.pdf"
        }
    }
```

### Full Product - 2-3 months

Add:
- Advanced PDF parsing (YOLO models)
- Comprehensive rules engine (50+ rules)
- Advanced regional pricing
- Xactimate export
- Professional reporting

**YOU ARE NOW READY TO EXECUTE**

---
