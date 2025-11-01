# Eagle Eye Developer Base Model System
## Comprehensive Guide to Upgrades, Financing & Funding-Ready Proposals

**Date**: November 1, 2025  
**Status**: Architecture & Implementation Plan  
**Audience**: Senior Developers, SR Engineering, Financial Partners

---

## PART 1: SYSTEM OVERVIEW

### What This System Does

This system transforms Eagle Eye from a basic estimating tool to a **complete SR (Senior/Strategic) Developer platform** that:

1. **Base Model Definition** - Creates flexible "Developer Base" with all core construction elements
2. **Upgrade Catalog** - Adds Energy Star, LEED, solar, ESG, net-zero capabilities with full financial modeling
3. **Financial Integration** - Calculates rebates (federal, state, local), tax credits, depreciation, equity buildup
4. **PPA Support** - Power Purchase Agreements for solar + storage systems with 25-year modeling
5. **Smart Onboarding** - Documents → CRM (automatic) + Questions → Proposals (automatic)
6. **Funding Ready** - All proposals include underwriting info for SBA, PACE, green bonds, venture capital

### Key Innovation: Tiered Architecture

```
LEVEL 1: BASE CASE (Standard Construction)
├─ Core components
├─ Local compliance codes
├─ Regional labor/materials
└─ Simple timeline

LEVEL 2: DEVELOPER BASE (Professional Grade)
├─ Everything in LEVEL 1 +
├─ Upgrade framework
├─ Financial modeling
├─ Tax incentive calculations
└─ Rebate integration

LEVEL 3: SR/STRATEGIC (Institutional Grade)
├─ Everything in LEVEL 2 +
├─ PPA support
├─ LEED/Energy Star modeling
├─ ESG reporting
├─ Multi-year cash flow analysis
├─ Venture capital ready
└─ Institutional investor metrics
```

---

## PART 2: DEVELOPER BASE MODEL ARCHITECTURE

### 2.1 Base Project Structure

Every project starts with a **Developer Base** - a standardized set of building components:

```python
# Location: services/pricing/developer_base.py

class DeveloperBase:
    """
    The 'base case' - all standard construction for given:
    - Building type (residential, commercial, industrial)
    - Square footage
    - Location (ZIP code)
    - Year built / renovation year
    """
    
    def __init__(self, building_type: str, sqft: int, zip_code: str):
        self.building_type = building_type
        self.sqft = sqft
        self.zip_code = zip_code
        self.components = {}
        self.baseline_cost = 0
        self.baseline_energy_use = 0  # kWh/year
        self.baseline_emissions = 0   # tons CO2/year
    
    @property
    def base_components(self) -> Dict:
        """
        Standard components for building type.
        Example for 2,000 sqft residential:
        """
        return {
            "Foundation": {"sqft": 2000, "cost": "$15k"},
            "Framing": {"sqft": 2000, "cost": "$45k"},
            "Roof": {"sqft": 2000, "cost": "$18k"},
            "HVAC": {"tons": 2.5, "cost": "$7k"},
            "Windows": {"count": 24, "cost": "$12k"},
            "Doors": {"count": 8, "cost": "$3k"},
            "Insulation": {"sqft": 2000, "cost": "$8k"},
            "Electrical": {"outlets": 48, "cost": "$6k"},
            "Plumbing": {"fixtures": 12, "cost": "$8k"},
            "Interior": {"sqft": 2000, "cost": "$25k"},
        }
    
    def calculate_baseline(self):
        """Calculate baseline cost for region + building type"""
        regional_factor = get_regional_factor(self.zip_code)
        per_sqft = BASELINE_COST_BY_TYPE[self.building_type]
        
        self.baseline_cost = self.sqft * per_sqft * regional_factor
        self.baseline_energy_use = self.sqft * ENERGY_USE_PER_SQFT[self.building_type]
        self.baseline_emissions = self.baseline_energy_use * CO2_FACTOR
        
        return self.baseline_cost
```

### 2.2 Developer Pricing Tiers

The system supports 3 pricing tiers, each with different cost structures:

```python
class PricingTier(Enum):
    """Three pricing tiers with cost multipliers"""
    STANDARD = 1.0      # Base cost
    PREMIUM = 1.15      # 15% better finishes
    LUXURY = 1.30       # 30% high-end finishes

# Each component has tier-specific costs:
COMPONENT_COSTS = {
    "HVAC": {
        "STANDARD": {"labor": 120, "material": 800},
        "PREMIUM": {"labor": 140, "material": 920},
        "LUXURY": {"labor": 160, "material": 1100},
    },
    "Windows": {
        "STANDARD": {"labor": 45, "material": 250},
        "PREMIUM": {"labor": 60, "material": 350},
        "LUXURY": {"labor": 80, "material": 500},
    },
    # ... all components with tier pricing
}
```

---

## PART 3: UPGRADE SYSTEM

### 3.1 Upgrade Catalog Structure

Every upgrade is defined with complete financial details:

```python
# Location: services/pricing/upgrade_catalog.py

@dataclass
class Upgrade:
    """Comprehensive upgrade definition"""
    
    id: str                          # "SOLAR-10KW-TIER-1"
    name: str                        # "10kW Solar System"
    category: str                    # "renewable_energy"
    tier: str                        # "standard", "premium", "luxury"
    
    # Physical specifications
    specifications: Dict             # {"capacity_kw": 10, "panel_type": "monocrystalline"}
    
    # Costs
    cost_installed: float            # $25,000
    cost_labor: float                # $3,000
    cost_materials: float            # $20,000
    cost_permits: float              # $1,200
    cost_interconnection: float      # $800
    
    # Performance metrics
    annual_production_kwh: float     # 13,500 kWh/year
    co2_offset_tons: float           # 9.5 tons/year
    energy_offset_percentage: float  # 45% of baseline
    
    # Financial incentives
    federal_itc: float               # 30% tax credit (federal)
    state_rebate: float              # $2,500 (varies by state)
    utility_rebate: float            # $1,000 (varies by utility)
    local_incentive: float           # $500 (varies by locality)
    depreciation_schedule: str       # "MACRS-5-year" or "straight-line-25-year"
    
    # PPA & Financing
    ppa_available: bool              # True for solar
    ppa_price_per_kwh: float         # $0.08/kWh escalation factor
    lease_available: bool            # True
    loan_term_years: List[int]       # [5, 10, 15, 20, 25]
    
    # Certifications & compliance
    certifications: List[str]        # ["LEED", "Energy Star", "UL-1703"]
    code_compliance: Dict            # {"IEC": "61730", "NEC": "690"}
    
    # Maintenance & warranties
    warranty_years: int              # 25 years product, 10 years labor
    annual_maintenance_cost: float   # $150/year
    
    # ESG metrics
    esg_score_improvement: float     # +15 points
    sustainability_metrics: Dict     # {"water_savings": "10k gal/year"}
    
    # Metadata
    created_date: str
    last_updated: str
    vendor_options: List[str]        # ["Sunrun", "Vivint Solar", "local_installer"]
    
    def calculate_irr(self, financing_option: str) -> float:
        """Calculate Internal Rate of Return for this upgrade"""
        pass
    
    def calculate_payback_period(self) -> int:
        """Calculate simple payback in years"""
        annual_savings = self.annual_production_kwh * UTILITY_RATE
        return int(self.cost_installed / annual_savings)
    
    def calculate_lifetime_value(self, years: int = 25) -> float:
        """Calculate 25-year net present value"""
        pass
```

### 3.2 Pre-Built Upgrade Categories

```python
UPGRADE_CATEGORIES = {
    # ENERGY EFFICIENCY
    "HVAC_EFFICIENCY": [
        "Upgrade to SEER 16+ system",
        "Heat pump with backup heating",
        "Variable capacity system",
        "Smart thermostat with learning",
    ],
    
    "INSULATION": [
        "Exterior wall spray foam (R-15)",
        "Attic rigid foam (R-30)",
        "Foundation wall insulation",
        "Thermal bridge breaks",
    ],
    
    "WINDOWS": [
        "Triple-pane Low-E windows (U-0.20)",
        "Smart electrochromic windows",
        "Automated cellular shades",
    ],
    
    "WATER_HEATING": [
        "Heat pump water heater",
        "On-demand tankless system",
        "Solar thermal collector",
    ],
    
    # RENEWABLE ENERGY
    "SOLAR_ELECTRIC": [
        "5kW rooftop solar",
        "10kW rooftop solar",
        "15kW ground mount solar",
        "Hybrid with battery storage",
    ],
    
    "SOLAR_THERMAL": [
        "Solar hot water heating",
        "Solar space heating",
    ],
    
    "BATTERY_STORAGE": [
        "10kWh lithium battery system",
        "20kWh system",
        "30kWh system",
    ],
    
    # WATER & WASTE
    "WATER_EFFICIENCY": [
        "Rainwater harvesting (5000 gal tank)",
        "Greywater system",
        "Low-flow fixtures",
        "Smart irrigation controller",
    ],
    
    "WASTE": [
        "On-site composting system",
        "Smart waste sorting",
    ],
    
    # LEED & CERTIFICATIONS
    "LEED_PACKAGE": [
        "LEED certification (Silver)",
        "LEED certification (Gold)",
        "LEED certification (Platinum)",
    ],
    
    "ENERGY_STAR": [
        "Energy Star certification",
        "Energy Star certification + HVAC",
    ],
    
    "NET_ZERO": [
        "Net-zero energy package",
        "Net-zero water package",
        "Net-zero energy + water combo",
    ],
    
    # ESG & SOCIAL
    "ESG_REPORTING": [
        "ESG audit & reporting",
        "Carbon footprint assessment",
        "Life cycle assessment",
    ],
    
    "COMMUNITY_BENEFITS": [
        "On-site job training program",
        "Community solar allocation",
        "Minority-owned supplier requirement",
    ],
}
```

### 3.3 Upgrade Selection Engine

```python
class UpgradeSelector:
    """Intelligently recommends upgrades based on project parameters"""
    
    def recommend_upgrades(
        self,
        base_cost: float,
        location: str,
        building_type: str,
        goals: List[str],  # ["save_money", "zero_energy", "leed_gold"]
        budget_multiplier: float = 1.0
    ) -> List[Upgrade]:
        """
        Recommend upgrades that meet goals
        
        Example:
            selector = UpgradeSelector()
            recommendations = selector.recommend_upgrades(
                base_cost=250000,
                location="30601",
                building_type="residential",
                goals=["net_zero", "leed_gold", "tax_incentives"],
                budget_multiplier=1.20  # 20% above base
            )
        """
        
        recommended = []
        
        # Goal: Save money
        if "save_money" in goals:
            recommended.extend(self.rank_by_irr())
        
        # Goal: Energy independence
        if "zero_energy" in goals:
            recommended.extend(self.get_renewable_energy_path())
        
        # Goal: LEED certification
        if "leed_gold" in goals:
            recommended.extend(self.get_leed_points_path("gold"))
        
        # Goal: ESG compliance
        if "esg_leader" in goals:
            recommended.extend(self.get_esg_compliance_path())
        
        # Sort by ROI and filter by budget
        return self.sort_and_filter(recommended, base_cost * budget_multiplier)
```

---

## PART 4: FINANCIAL ENGINEERING

### 4.1 Rebate & Incentive Engine

```python
# Location: services/pricing/incentives.py

class IncentiveCalculator:
    """Calculate all available rebates, tax credits, incentives"""
    
    def calculate_solar_incentives(
        self,
        system_cost: float,
        location: str,  # ZIP code
        year: int
    ) -> Dict:
        """
        Calculate all solar incentives:
        - Federal ITC (Investment Tax Credit)
        - State incentives
        - Utility rebates
        - Local programs
        """
        
        incentives = {
            "federal_itc": {
                "percentage": 0.30,  # 30% federal tax credit (2025)
                "amount": system_cost * 0.30,
                "description": "Federal Investment Tax Credit - 30%",
                "sunset": "2032",
                "cumulative": False
            },
            
            "state_incentives": self.get_state_incentives(location, system_cost),
            "utility_rebates": self.get_utility_rebates(location, system_cost),
            "local_programs": self.get_local_programs(location),
            
            "total_incentives": 0,  # Calculated below
            "net_cost": system_cost,
            "roi_months": 0,  # Calculated below
        }
        
        # Sum incentives
        total = incentives["federal_itc"]["amount"]
        total += sum(x.get("amount", 0) for x in incentives["state_incentives"])
        total += sum(x.get("amount", 0) for x in incentives["utility_rebates"])
        total += sum(x.get("amount", 0) for x in incentives["local_programs"])
        
        incentives["total_incentives"] = total
        incentives["net_cost"] = max(0, system_cost - total)
        
        return incentives
    
    def get_state_incentives(self, location: str, cost: float) -> List[Dict]:
        """State-specific incentives (Georgia example)"""
        state = get_state_from_zip(location)
        
        if state == "GA":
            return [
                {
                    "name": "Georgia Energy Tax Credit",
                    "percentage": 0.25,
                    "amount": cost * 0.25,
                    "max_amount": 2500,
                    "description": "25% state tax credit up to $2,500"
                },
                # Add other GA programs
            ]
        
        elif state == "NY":
            return [
                {
                    "name": "NY Energy Storage Grand",
                    "amount": 3500,
                    "description": "Battery storage rebate"
                },
                # NY programs
            ]
        
        # ... other states
        return []
    
    def get_utility_rebates(self, location: str, cost: float) -> List[Dict]:
        """Utility-specific rebates (varies by provider)"""
        utility = get_utility_from_zip(location)
        
        # Rebates vary by utility - this is a framework
        rebates = []
        
        if "solar_rebate" in utility.programs:
            rebates.append({
                "name": f"{utility.name} Solar Rebate",
                "amount": utility.solar_rebate_per_kw * system_kw,
                "description": "Utility rebate for distributed solar"
            })
        
        return rebates
    
    def calculate_depreciation(
        self,
        system_cost: float,
        system_type: str,
        ownership_model: str = "owned"  # "owned", "leased", "ppa"
    ) -> Dict:
        """
        Calculate tax depreciation schedules
        
        Solar systems typically qualify for:
        - MACRS 5-year property (most common)
        - MACRS 7-year property (some cases)
        - MACRS 15-year for land/structural improvements
        
        For commercial (25% energy tax credit applies to 75% of cost)
        """
        
        if ownership_model == "owned":
            return self.calculate_macrs_depreciation(system_cost, "5-year")
        elif ownership_model == "leased":
            return {"note": "Lessor claims depreciation, not owner"}
        elif ownership_model == "ppa":
            return {"note": "PPA provider claims depreciation"}
    
    def calculate_macrs_depreciation(self, basis: float, schedule: str) -> Dict:
        """MACRS depreciation schedule"""
        
        if schedule == "5-year":
            percentages = [0.20, 0.32, 0.192, 0.1152, 0.1152, 0.0576]
        elif schedule == "7-year":
            percentages = [0.1429, 0.2449, 0.1749, 0.1249, 0.0893, 0.0892, 0.0893, 0.0446]
        else:
            raise ValueError(f"Unknown schedule: {schedule}")
        
        depreciation_schedule = []
        for year, pct in enumerate(percentages, 1):
            annual_deduction = basis * pct
            depreciation_schedule.append({
                "year": year,
                "percentage": pct,
                "amount": annual_deduction,
                "cumulative": basis * sum(percentages[:year])
            })
        
        return {
            "schedule": schedule,
            "basis": basis,
            "detail": depreciation_schedule,
            "total_deduction": basis
        }
```

### 4.2 Financing Options & Cash Flow Modeling

```python
# Location: services/pricing/financing.py

@dataclass
class FinancingOption:
    """Represents one financing pathway"""
    
    option_name: str                 # "PACE Loan", "SBA Loan", "Lease", "PPA"
    down_payment_pct: float          # 0.20 (20% down)
    interest_rate: float             # 0.055 (5.5%)
    term_years: int                  # 10 years
    monthly_payment: float           # Calculated
    total_cost: float                # Calculated (interest included)
    breakeven_months: int            # Calculated
    
    # Tax/financial benefits
    interest_tax_deductible: bool    # True for loans, False for lease/PPA
    depreciation_available: bool     # Depends on ownership
    federal_credits_available: bool  # ITC, etc.
    state_credits_available: bool
    
    # Risks
    pre_payment_penalty: float       # 0.0 (no penalty) to 0.05 (5% penalty)
    balloon_payment: float           # $0 or amount due at end
    default_consequences: str        # Description of risks
    
    def calculate_monthly_payment(self, principal: float):
        """Calculate fixed monthly payment using amortization"""
        monthly_rate = self.interest_rate / 12
        num_payments = self.term_years * 12
        
        if monthly_rate == 0:
            return principal / num_payments
        
        return principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
               ((1 + monthly_rate)**num_payments - 1)
    
    def calculate_cash_flow(
        self,
        project_cost: float,
        annual_savings: float,
        years: int = 25
    ) -> List[Dict]:
        """
        Generate annual cash flow projection
        
        Returns: [
            {
                "year": 1,
                "loan_payment": -12000,
                "energy_savings": 4000,
                "tax_benefits": 2000,
                "net_cash_flow": -6000,
                "cumulative": -6000
            },
            ...
        ]
        """
        
        down_payment = project_cost * self.down_payment_pct
        financed_amount = project_cost - down_payment
        
        cash_flows = [
            {
                "year": 0,
                "description": "Initial investment",
                "down_payment": -down_payment,
                "incentives": 0,  # Applied in year 0 or 1
                "net_cash_flow": -down_payment,
                "cumulative": -down_payment
            }
        ]
        
        monthly_payment = self.calculate_monthly_payment(financed_amount)
        annual_payment = monthly_payment * 12
        
        cumulative = -down_payment
        
        for year in range(1, years + 1):
            
            # Loan payment (negative cash)
            loan_payment = -annual_payment if year <= self.term_years else 0
            
            # Energy savings (positive cash)
            savings = annual_savings * (1.03 ** year)  # 3% annual increase
            
            # Tax benefits (positive cash) - only in first few years
            tax_benefit = self.calculate_annual_tax_benefit(year)
            
            # Maintenance costs (negative cash)
            maintenance = -500 if year > 5 else -200  # Typical PV maintenance
            
            net_year = loan_payment + savings + tax_benefit + maintenance
            cumulative += net_year
            
            cash_flows.append({
                "year": year,
                "loan_payment": loan_payment,
                "energy_savings": savings,
                "tax_benefits": tax_benefit,
                "maintenance": maintenance,
                "net_cash_flow": net_year,
                "cumulative": cumulative
            })
        
        return cash_flows
    
    def calculate_annual_tax_benefit(self, year: int) -> float:
        """Calculate tax deduction/credit benefit per year"""
        # Simplified: ITC in year 1, then depreciation deductions
        if year == 1 and self.federal_credits_available:
            return 5000  # Example
        elif year > 1 and self.depreciation_available:
            return 2000  # Annual depreciation tax benefit
        return 0
    
    def calculate_irr(self, project_cost: float, annual_savings: float, years: int = 25) -> float:
        """Calculate Internal Rate of Return"""
        # IRR = rate where NPV = 0
        # Simplified calculation
        cash_flows = self.calculate_cash_flow(project_cost, annual_savings, years)
        
        # Use numpy for actual IRR calculation (not shown here)
        # For now, return simplified metric
        return self.simple_roi(project_cost, annual_savings, self.term_years)
    
    @staticmethod
    def simple_roi(cost: float, annual_savings: float, years: int) -> float:
        """Simple ROI calculation"""
        return (annual_savings * years / cost) - 1
```

### 4.3 PPA (Power Purchase Agreement) Engine

```python
# Location: services/pricing/ppa.py

class PowerPurchaseAgreement:
    """
    Power Purchase Agreement for renewable energy systems.
    Typical structure:
    - Developer/TPO owns system
    - Customer purchases power at agreed rate
    - Contract typically 20-25 years
    - Price typically starts 15-25% below utility rate
    - Annual escalation (typical: 2-3%)
    """
    
    def __init__(
        self,
        system_cost: float,
        system_capacity_kw: float,
        annual_production_kwh: float,
        initial_rate_per_kwh: float = 0.08,
        annual_escalation: float = 0.025,  # 2.5%/year
        contract_years: int = 25
    ):
        self.system_cost = system_cost
        self.system_capacity_kw = system_capacity_kw
        self.annual_production_kwh = annual_production_kwh
        self.initial_rate_per_kwh = initial_rate_per_kwh
        self.annual_escalation = annual_escalation
        self.contract_years = contract_years
    
    def calculate_annual_payment(self, year: int) -> float:
        """
        Calculate annual PPA payment for given year
        Year 1 payment = annual_production * rate * (1 + escalation)^years
        """
        escalated_rate = self.initial_rate_per_kwh * \
                        ((1 + self.annual_escalation) ** (year - 1))
        
        return self.annual_production_kwh * escalated_rate
    
    def calculate_total_contract_value(self) -> float:
        """Total value of PPA over contract term"""
        total = 0
        for year in range(1, self.contract_years + 1):
            total += self.calculate_annual_payment(year)
        return total
    
    def calculate_customer_savings(
        self,
        current_utility_rate: float,
        degradation_rate: float = 0.005  # 0.5% annual
    ) -> float:
        """
        Calculate customer's total savings vs buying from utility
        
        Accounts for:
        - System degradation (production decreases ~0.5%/year)
        - Utility rate increases (~3%/year)
        - PPA price increases (contractual)
        """
        
        total_savings = 0
        total_ppa_payments = 0
        total_utility_cost = 0
        
        system_production = self.annual_production_kwh
        
        for year in range(1, self.contract_years + 1):
            
            # System production (degrades)
            production = system_production * ((1 - degradation_rate) ** (year - 1))
            
            # PPA payment (escalates per contract)
            ppa_payment = self.calculate_annual_payment(year)
            total_ppa_payments += ppa_payment
            
            # Utility cost (increases ~3%/year)
            utility_cost = production * current_utility_rate * \
                          ((1.03) ** (year - 1))
            total_utility_cost += utility_cost
            
            total_savings += (utility_cost - ppa_payment)
        
        return {
            "total_savings_25_years": total_savings,
            "average_annual_savings": total_savings / self.contract_years,
            "total_ppa_payments": total_ppa_payments,
            "total_utility_cost_avoided": total_utility_cost,
            "payback_on_financing": total_savings / self.system_cost,
        }
    
    def generate_ppa_schedule(self) -> List[Dict]:
        """Generate year-by-year PPA payment schedule"""
        
        schedule = []
        for year in range(1, self.contract_years + 1):
            
            annual_payment = self.calculate_annual_payment(year)
            cumulative = sum(self.calculate_annual_payment(y) 
                           for y in range(1, year + 1))
            
            schedule.append({
                "year": year,
                "rate_per_kwh": self.initial_rate_per_kwh * \
                               ((1 + self.annual_escalation) ** (year - 1)),
                "kwh_produced": self.annual_production_kwh * \
                               ((1 - 0.005) ** (year - 1)),
                "annual_payment": annual_payment,
                "cumulative_payments": cumulative
            })
        
        return schedule
```

---

## PART 5: SMART ONBOARDING SYSTEM

### 5.1 Document-to-CRM Parser

```python
# Location: services/crm/document_parser.py

class OnboardingDocumentParser:
    """
    Parses onboarding documents and auto-generates CRM records.
    
    Accepts:
    - PDF (scanned or digital)
    - Excel workbook
    - Word document
    - Web form submission
    - Email
    
    Extracts:
    - Project information
    - Developer/owner info
    - Building specifications
    - Goals and requirements
    - Budget constraints
    
    Auto-generates:
    - CRM project record
    - Preliminary estimate
    - Compliance checklist
    - Upgrade recommendations
    """
    
    def parse_document(self, file_path: str) -> Dict:
        """
        Parse onboarding document and extract structured data
        
        Returns:
        {
            "project": {...},
            "owner": {...},
            "building": {...},
            "goals": [...],
            "constraints": {...},
            "proposed_upgrades": [...],
            "confidence_score": 0.95
        }
        """
        
        # Detect file type
        file_type = detect_file_type(file_path)
        
        if file_type == "pdf":
            text = self.extract_pdf_text(file_path)
        elif file_type == "excel":
            text = self.extract_excel_data(file_path)
        elif file_type == "word":
            text = self.extract_word_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Use LLM to understand document
        extracted_data = self.extract_with_llm(text)
        
        # Validate and normalize data
        validated = self.validate_extracted_data(extracted_data)
        
        # Auto-generate recommendations
        recommendations = self.generate_recommendations(validated)
        
        return {
            **validated,
            "proposed_upgrades": recommendations,
            "confidence_score": self.calculate_confidence(extracted_data)
        }
    
    def extract_with_llm(self, document_text: str) -> Dict:
        """Use LLM to intelligently extract structured data"""
        
        prompt = """
        You are an expert real estate developer and energy specialist.
        Parse this onboarding document and extract:
        
        1. PROJECT INFO:
           - Project name
           - Project type (residential, commercial, industrial, mixed-use)
           - Location/address
           - Square footage
           - Year built
           - Current condition (move-in ready, needs renovation, new construction)
        
        2. OWNER/DEVELOPER INFO:
           - Name
           - Contact info
           - Company (if applicable)
           - Experience level (first-time, experienced developer)
        
        3. GOALS:
           - What problem are we solving? (reduce energy costs, increase value, comply with regs, ESG goals)
           - Timeline (immediate, 6 months, 1-2 years, 3+ years)
           - Budget flexibility (fixed, +10%, +20%, +30%, flexible)
        
        4. CONSTRAINTS:
           - Budget (if specified)
           - Aesthetic requirements (must match existing, modern desired, historic preservation)
           - Technical constraints (roof condition, electrical capacity, gas lines)
           - Regulatory (HOA requirements, historic district, covenant restrictions)
        
        5. DESIRED UPGRADES (if mentioned):
           - Energy efficiency
           - Renewable energy
           - Water conservation
           - LEED certification level
           - Net-zero aspirations
        
        Document:
        {document_text}
        
        Return as JSON with high confidence for clear items, lower confidence for ambiguous items.
        """
        
        response = llm_call(prompt)  # Use OpenAI, Ollama, or HuggingFace
        return json.loads(response)
    
    def generate_recommendations(self, project_data: Dict) -> List[Dict]:
        """
        Auto-generate upgrade recommendations based on extracted data.
        
        Uses rules like:
        - If energy bills mentioned as "very high" → recommend solar + efficiency
        - If "LEED" mentioned → recommend LEED-qualifying upgrades
        - If "30+ years old" → recommend full envelope upgrade
        - If commercial → recommend smart building automation
        """
        
        recommendations = []
        
        # Rule: Energy cost concern
        if "high_energy_bills" in project_data.get("concerns", []):
            recommendations.append({
                "upgrade": "Solar + Efficiency Package",
                "rationale": "Address root cause of high energy costs",
                "estimated_savings": "40-60%"
            })
        
        # Rule: LEED goal
        if "leed" in str(project_data.get("goals", "")).lower():
            leed_level = extract_leed_level(project_data.get("goals"))
            recommendations.extend(self.get_leed_path(leed_level))
        
        # Rule: ESG requirement
        if "esg" in str(project_data.get("goals", "")).lower():
            recommendations.extend([
                {"upgrade": "Renewable energy system", "reason": "ESG compliance"},
                {"upgrade": "Water conservation", "reason": "ESG compliance"},
                {"upgrade": "Local hiring/training", "reason": "ESG compliance"},
            ])
        
        # Rule: Age-based
        building_age = project_data.get("year_built", 2000)
        if building_age < 1990:
            recommendations.append({
                "upgrade": "Complete envelope upgrade",
                "rationale": "Building codes require minimum efficiency standards",
                "priority": "high"
            })
        
        return recommendations
```

### 5.2 Interactive Onboarding Questions

```python
# Location: services/crm/onboarding_questionnaire.py

class OnboardingQuestionnaire:
    """
    Interactive multi-step questionnaire that generates:
    1. CRM project record
    2. Preliminary design options
    3. Funding-ready proposal
    
    Design pattern: Question → Answer → Next Question (adaptive)
    """
    
    QUESTIONS = {
        "step_1": {
            "title": "Project Basics",
            "questions": [
                {
                    "id": "building_type",
                    "question": "What type of building?",
                    "options": ["residential", "commercial", "industrial", "mixed-use"],
                    "required": True
                },
                {
                    "id": "square_footage",
                    "question": "How many square feet?",
                    "type": "number",
                    "required": True
                },
                {
                    "id": "location",
                    "question": "What's the address or ZIP code?",
                    "type": "text",
                    "required": True
                },
                {
                    "id": "year_built",
                    "question": "What year was it built?",
                    "type": "number",
                    "required": True
                },
            ]
        },
        
        "step_2": {
            "title": "Your Goals (Choose all that apply)",
            "questions": [
                {
                    "id": "goals",
                    "question": "What are your primary goals?",
                    "options": [
                        "Save on energy costs",
                        "Reduce carbon footprint",
                        "Get LEED certification",
                        "Achieve net-zero energy",
                        "Increase property value",
                        "Comply with regulations",
                        "ESG/sustainability leadership",
                        "Energy independence"
                    ],
                    "type": "multi-select",
                    "required": True
                },
                {
                    "id": "timeline",
                    "question": "When do you need this done?",
                    "options": ["ASAP", "Within 6 months", "Within 1 year", "1-2 years", "3+ years"],
                    "required": True
                }
            ]
        },
        
        "step_3": {
            "title": "Budget & Constraints",
            "questions": [
                {
                    "id": "budget_flexibility",
                    "question": "How flexible is your budget?",
                    "options": [
                        "Fixed budget (can't go over)",
                        "+10% flexibility",
                        "+20% flexibility",
                        "+30% flexibility",
                        "Flexible (find best solution)",
                    ],
                    "required": True
                },
                {
                    "id": "constraints",
                    "question": "Any constraints? (select all)",
                    "options": [
                        "Must preserve historic character",
                        "HOA/covenant restrictions",
                        "Roof condition issues",
                        "Electrical capacity limited",
                        "Space constraints",
                        "Other"
                    ],
                    "type": "multi-select"
                }
            ]
        },
        
        "step_4": {
            "title": "Financing Preferences",
            "questions": [
                {
                    "id": "financing_model",
                    "question": "How would you prefer to pay?",
                    "options": [
                        "All cash (own it outright)",
                        "Loan (own and finance)",
                        "Lease (third-party ownership)",
                        "PPA (pay for energy only)",
                        "Not sure - show me options"
                    ],
                    "required": True
                },
                {
                    "id": "tax_optimization",
                    "question": "Tax incentives important?",
                    "options": [
                        "Yes, maximize tax benefits",
                        "Somewhat",
                        "Not important"
                    ]
                }
            ]
        },
    }
    
    def generate_full_proposal(self, answers: Dict) -> Dict:
        """
        Generate complete funding-ready proposal from questionnaire answers.
        
        Returns:
        {
            "crm_record": {...},           # CRM project + owner record
            "design_options": [...],       # 3 design tiers
            "financial_analysis": {...},  # Cash flow, ROI, incentives
            "proposal_document": "...",    # HTML/PDF ready
            "next_steps": [...],           # Action items
        }
        """
        
        # Step 1: Create CRM record
        crm_record = self.create_crm_project(answers)
        
        # Step 2: Recommend upgrade packages
        design_options = self.generate_design_options(
            building_type=answers.get("building_type"),
            sqft=answers.get("square_footage"),
            goals=answers.get("goals"),
            location=answers.get("location"),
            budget_flexibility=answers.get("budget_flexibility")
        )
        
        # Step 3: Run financial modeling
        financial_analysis = self.run_financial_analysis(
            design_options,
            financing_model=answers.get("financing_model"),
            optimize_taxes=answers.get("tax_optimization")
        )
        
        # Step 4: Generate proposal document
        proposal_doc = self.generate_proposal_document(
            crm_record,
            design_options,
            financial_analysis,
            answers
        )
        
        # Step 5: Create next steps
        next_steps = self.generate_next_steps(answers, design_options)
        
        return {
            "crm_record": crm_record,
            "design_options": design_options,
            "financial_analysis": financial_analysis,
            "proposal_document": proposal_doc,
            "next_steps": next_steps
        }
```

---

## PART 6: FUNDING-READY PROPOSAL GENERATION

### 6.1 Proposal Content Structure

Every proposal includes sections designed for institutional investors/lenders:

```python
# Location: services/reports/proposal_generator.py

@dataclass
class FundingReadyProposal:
    """
    Comprehensive proposal structure for securing financing.
    Includes all information required by:
    - Commercial banks
    - PACE program administrators
    - SBA lenders
    - Green bond programs
    - Venture capital / impact investors
    """
    
    # SECTION 1: EXECUTIVE SUMMARY
    executive_summary: str         # 1-page overview with key metrics
    
    # SECTION 2: PROJECT DESCRIPTION
    project_overview: str          # Building details, location, current state
    project_goals: List[str]       # What we're trying to achieve
    investment_amount: float       # Total project cost
    
    # SECTION 3: DEVELOPER/OWNER INFO
    developer_profile: Dict        # Experience, track record, team
    
    # SECTION 4: TECHNICAL SPECIFICATIONS
    base_case: Dict                # Current building specs
    proposed_upgrades: List[Dict]  # All improvements with specs
    compliance: Dict               # Code compliance, certifications
    
    # SECTION 5: FINANCIAL ANALYSIS
    base_case_economics: Dict      # Current annual energy cost, emissions
    
    # Three financing scenarios
    option_1_cash: Dict            # All-cash option
    option_2_loan: Dict            # Traditional loan
    option_3_ppa: Dict             # PPA or lease
    
    # Tax incentives & rebates
    federal_incentives: Dict       # ITC, tax credits
    state_incentives: Dict         # State programs
    utility_rebates: Dict          # Rebate programs
    local_incentives: Dict         # City/county programs
    total_incentives: float
    
    # Cash flow projections
    cashflow_25_years: List[Dict]  # Year-by-year P&L
    
    # Return metrics
    roi: float                     # Return on investment %
    irr: float                     # Internal rate of return
    payback_period: int            # Years to breakeven
    npv_25_years: float            # Net present value
    
    # SECTION 6: RISK ANALYSIS
    risks: List[Dict]              # What could go wrong
    mitigation_strategies: List[Dict]  # How we address them
    
    # SECTION 7: ENVIRONMENTAL & SOCIAL
    energy_savings: float          # Annual kWh reduced
    co2_reduction: float           # Annual tons CO2 avoided
    water_savings: float           # Gallons/year saved
    esg_metrics: Dict              # Environmental + Social + Governance
    
    # SECTION 8: TECHNICAL DRAWINGS & SPECS
    architectural_drawings: List   # Images/PDFs
    equipment_specifications: Dict # Detailed specs for each system
    performance_warranties: List   # Warranty details
    
    # SECTION 9: LEGAL & COMPLIANCE
    permits_required: List[str]    # What approvals needed
    permitting_timeline: Dict      # When permits take
    financing_requirements: Dict   # What documents lender needs
    
    # SECTION 10: NEXT STEPS & TIMELINE
    project_timeline: Dict         # Design → Permitting → Construction → O&M
    next_steps: List[str]          # Immediate actions
    
    # APPENDICES
    appendix_a: str                # Detailed cost breakdown
    appendix_b: str                # Incentive documentation
    appendix_c: str                # Equipment quotes
    appendix_d: str                # Technical studies (load calc, etc.)
    appendix_e: str                # Financing term sheets


class ProposalGenerator:
    """Generate funding-ready proposals from project data"""
    
    def generate_funding_ready_proposal(
        self,
        crm_record: Dict,
        design_options: List[Dict],
        selected_option: int = 1,  # Which design option (1, 2, or 3)
        output_format: str = "pdf"  # "pdf", "html", "docx", "all"
    ) -> Dict:
        """
        Generate complete funding-ready proposal.
        
        Returns:
        {
            "proposal_pdf": bytes,
            "proposal_html": str,
            "proposal_docx": bytes,
            "supporting_docs": {
                "financial_model": bytes,
                "technical_specs": bytes,
                "warranty_docs": bytes,
            }
        }
        """
        
        # Get selected design option
        design = design_options[selected_option - 1]
        
        # Build proposal object
        proposal = FundingReadyProposal(
            executive_summary=self.build_exec_summary(crm_record, design),
            project_overview=self.build_project_overview(crm_record),
            project_goals=crm_record.get("goals", []),
            investment_amount=design.get("total_cost"),
            
            developer_profile=self.build_developer_profile(crm_record),
            
            base_case=self.calculate_base_case(crm_record),
            proposed_upgrades=design.get("upgrades", []),
            compliance=self.check_compliance(crm_record, design),
            
            # Financial scenarios
            option_1_cash=self.calculate_cash_scenario(crm_record, design),
            option_2_loan=self.calculate_loan_scenario(crm_record, design),
            option_3_ppa=self.calculate_ppa_scenario(crm_record, design),
            
            # Incentives
            federal_incentives=self.calculate_federal_incentives(design),
            state_incentives=self.calculate_state_incentives(crm_record, design),
            utility_rebates=self.calculate_utility_rebates(crm_record, design),
            local_incentives=self.calculate_local_incentives(crm_record, design),
            total_incentives=0,  # Calculated below
            
            # Financials
            cashflow_25_years=self.project_cashflow(crm_record, design, 25),
            roi=self.calculate_roi(crm_record, design),
            irr=self.calculate_irr(crm_record, design),
            payback_period=self.calculate_payback(crm_record, design),
            npv_25_years=self.calculate_npv(crm_record, design),
            
            # Environmental
            energy_savings=design.get("annual_kwh_saved", 0),
            co2_reduction=self.calculate_co2(design),
            water_savings=design.get("annual_water_saved", 0),
            esg_metrics=self.calculate_esg_score(design),
        )
        
        # Calculate total incentives
        proposal.total_incentives = sum([
            v.get("amount", 0) if isinstance(v, dict) else 0
            for v in [proposal.federal_incentives, proposal.state_incentives,
                     proposal.utility_rebates, proposal.local_incentives]
        ])
        
        # Render to output formats
        outputs = {}
        
        if output_format in ["pdf", "all"]:
            outputs["proposal_pdf"] = self.render_proposal_pdf(proposal, crm_record)
        
        if output_format in ["html", "all"]:
            outputs["proposal_html"] = self.render_proposal_html(proposal, crm_record)
        
        if output_format in ["docx", "all"]:
            outputs["proposal_docx"] = self.render_proposal_docx(proposal, crm_record)
        
        # Generate supporting documents
        if output_format in ["all", "full"]:
            outputs["supporting_docs"] = {
                "financial_model": self.generate_financial_model_xlsx(proposal),
                "technical_specs": self.generate_technical_specs_pdf(design),
                "equipment_quotes": self.generate_equipment_quotes(design),
            }
        
        return outputs
```

---

## PART 7: INTEGRATION WITH EXISTING SYSTEMS

### 7.1 How It Integrates with Current Architecture

```python
# The new system extends the existing 5-stage pipeline:

ENHANCED_PIPELINE = {
    "STAGE 0: ONBOARDING": {
        # NEW: Parse documents/questionnaire
        # NEW: Auto-generate CRM record
        # NEW: Extract goals and constraints
    },
    
    "STAGE 1: PARSE": {
        # EXISTING: Extract from PDFs
        # ENHANCED: Use for detailed cost estimation
        # ENHANCED: Match to upgrade opportunities
    },
    
    "STAGE 2: ENRICH": {
        # EXISTING: Add regional factors
        # ENHANCED: Add upgrade costs + incentives
        # ENHANCED: Calculate financial benefits
    },
    
    "STAGE 3: CHECK": {
        # EXISTING: Compliance rules
        # ENHANCED: Check which upgrades help compliance
        # ENHANCED: Flag LEED/Energy Star opportunities
    },
    
    "STAGE 4: ESTIMATE": {
        # EXISTING: Calculate base costs
        # ENHANCED: Add upgrade costs
        # ENHANCED: Calculate incentives & financing options
        # ENHANCED: Model 25-year cash flow
    },
    
    "STAGE 5: GENERATE": {
        # EXISTING: Create proposals
        # ENHANCED: Generate funding-ready proposals
        # ENHANCED: Include financial analysis
        # ENHANCED: Multiple financing scenarios
    },
}
```

### 7.2 Data Model Extensions

```python
# Add to existing Pydantic models in packages/shared/models.py

from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class UpgradeOption(BaseModel):
    """Represents a single upgrade choice"""
    upgrade_id: str
    name: str
    category: str
    cost: float
    annual_savings: float
    payback_years: float
    rebates: float
    tax_credits: float


class DesignOption(BaseModel):
    """One complete design tier"""
    tier_name: str              # "Silver", "Gold", "Platinum"
    base_cost: float
    upgrades: List[UpgradeOption]
    total_cost: float
    annual_energy_savings: float
    annual_water_savings: float
    co2_reduction_tons: float
    leed_points: Optional[int]
    energy_star_eligible: bool
    net_zero_capable: bool


class FinancialScenario(BaseModel):
    """One financing pathway"""
    scenario_name: str          # "Cash", "Loan", "Lease", "PPA"
    down_payment: float
    monthly_cost: float
    total_25_year_cost: float
    roi: float
    irr: float
    payback_months: int
    incentives: float
    tax_benefits: float


class FundingReadyProject(BaseModel):
    """Complete project with all funding info"""
    crm_id: str
    design_options: List[DesignOption]
    financial_scenarios: List[FinancialScenario]
    federal_incentives: Dict
    state_incentives: Dict
    utility_rebates: Dict
    environmental_impact: Dict
    esg_score: float
    proposal_ready: bool
```

---

## PART 8: IMPLEMENTATION ROADMAP

### Phase 1: Developer Base Model (Week 1)
- [ ] Create `DeveloperBase` class
- [ ] Build pricing tier system (Standard/Premium/Luxury)
- [ ] Integrate with existing `PricingEngine`
- [ ] Test with demo.py

### Phase 2: Upgrade Catalog (Week 2)
- [ ] Create `Upgrade` dataclass
- [ ] Build upgrade database (50+ upgrades)
- [ ] Create `UpgradeSelector` with recommendation engine
- [ ] Add to demo and test

### Phase 3: Financial Engineering (Week 3)
- [ ] Build `IncentiveCalculator` (federal/state/local)
- [ ] Implement MACRS depreciation
- [ ] Create `FinancingOption` modeling
- [ ] Build cash flow projections

### Phase 4: PPA System (Week 4)
- [ ] Create `PowerPurchaseAgreement` class
- [ ] Build PPA calculator
- [ ] Model 25-year customer savings
- [ ] Test with solar scenarios

### Phase 5: Smart Onboarding (Week 5)
- [ ] Build `OnboardingDocumentParser`
- [ ] Create LLM extraction prompts
- [ ] Build `OnboardingQuestionnaire`
- [ ] Auto-generate CRM records

### Phase 6: Funding-Ready Proposals (Week 6)
- [ ] Create `ProposalGenerator` enhancements
- [ ] Build financial model exports
- [ ] Create proposal templates
- [ ] Add investor-ready sections

### Phase 7: Integration & Testing (Week 7)
- [ ] Integrate all components
- [ ] Create end-to-end workflows
- [ ] Build comprehensive testing
- [ ] Create documentation

### Phase 8: Deploy & Optimize (Week 8)
- [ ] Deploy to production
- [ ] Optimize performance
- [ ] Create user guides
- [ ] Train team

---

## PART 9: EXAMPLE WORKFLOWS

### Example 1: Document Upload → Full Proposal (< 5 minutes)

```
USER UPLOADS: "Madison_Office_Renovation.pdf"
   ↓
SYSTEM PARSES: Extracts project specs, owner info, goals
   ↓
LLM ANALYZES: "This is a 5,000 sqft office needing LEED gold + energy savings"
   ↓
CRM AUTO-GENERATED: Project record created, all fields populated
   ↓
RECOMMENDATIONS: "Here are 3 design options optimized for LEED Gold"
   ├─ Option 1 (Silver): $150K, 30% energy savings
   ├─ Option 2 (Gold): $225K, 60% energy savings, LEED Gold
   └─ Option 3 (Platinum): $320K, Net-zero capable
   ↓
FINANCIAL MODELING: Auto-calculates for each option
   ├─ Federal ITC: $15,750 (7% of $225K)
   ├─ State rebate: $2,500
   ├─ Utility incentive: $3,000
   ├─ Total incentives: $21,250
   ├─ Net cost after incentives: $203,750
   ├─ 15-year simple payback: 8.3 years
   ├─ 25-year savings: $185,000
   └─ IRR: 8.2%
   ↓
PROPOSAL GENERATED: Professional PDF with all sections
   ├─ Executive summary
   ├─ Design options (3 tiers)
   ├─ Financial analysis (cash, loan, PPA options)
   ├─ 25-year cash flow projection
   ├─ Technical specifications
   ├─ Incentive breakdown
   ├─ ESG metrics
   └─ Next steps
   ↓
FUNDING-READY: Includes all info banks/investors need
   ├─ Owner credit analysis (if available)
   ├─ Equipment warranties
   ├─ Technical specifications
   ├─ Performance guarantees
   └─ Financing options

RESULT: Complete, professional proposal ready to send to owner or lender
TIME: 3-5 minutes (mostly automated)
```

### Example 2: Interactive Questionnaire → Customized Design

```
USER SELECTS: "Questionnaire Mode"
   ↓
STEP 1: "What type of building?"
USER: "Commercial office"
   ↓
STEP 2: "How many square feet?"
USER: "12,000"
   ↓
STEP 3: "Location?"
USER: "Atlanta, GA (30303)"
   ↓
STEP 4: "Your goals?"
USER: [✓] Energy savings [✓] LEED [✓] Tax benefits
   ↓
STEP 5: "Budget?"
USER: "+20% flexibility"
   ↓
STEP 6: "Financing?"
USER: "Show me all options"
   ↓
SYSTEM GENERATES: 3 optimized design options
   
   OPTION 1: Energy Focus ($180K)
   ├─ Advanced HVAC: SEER 18
   ├─ LED lighting: 95% reduction
   ├─ Weatherization
   ├─ Smart controls
   ├─ Annual savings: $22K
   ├─ Payback: 8.2 years
   ├─ LEED points: 45 (Silver)
   └─ Incentives: $28K
   
   OPTION 2: LEED Gold ($280K)
   ├─ Everything in Option 1 +
   ├─ 10 kW solar system
   ├─ Water efficiency upgrades
   ├─ Green cleaning supplies
   ├─ Annual savings: $38K
   ├─ Payback: 7.4 years
   ├─ LEED points: 65 (Gold)
   └─ Incentives: $42K
   
   OPTION 3: Net-Zero ($420K)
   ├─ Everything in Option 2 +
   ├─ Expand solar to 25 kW
   ├─ Energy storage battery
   ├─ Geothermal heating/cooling
   ├─ Annual savings: $62K
   ├─ Payback: 6.8 years
   ├─ LEED points: 85 (Platinum)
   ├─ Net-zero energy: YES
   └─ Incentives: $68K
   ↓
USER SELECTS: "Option 2 - LEED Gold"
   ↓
SYSTEM GENERATES: Funding-ready proposal
   ├─ Financial scenario 1: All-cash ($280K)
   ├─ Financial scenario 2: SBA loan (10 years, $2,800/month)
   ├─ Financial scenario 3: PACE loan (20 years, $1,500/month)
   ├─ Financial scenario 4: Solar lease (25 years, $200/month)
   ├─ 25-year cash flow projection
   ├─ Tax benefit summary
   ├─ Technical specifications
   ├─ LEED path documentation
   └─ Next steps
   ↓
RESULT: Complete, customized, funding-ready proposal
TIME: 10 minutes (mostly automated, 2 min user interaction)
```

---

## PART 10: SUCCESS METRICS

Once implemented, the system should achieve:

✅ **Speed**: Generate complete funding-ready proposal in < 5 minutes  
✅ **Accuracy**: 95%+ confidence in extracted project data  
✅ **Completeness**: All sections needed by investors/lenders included  
✅ **Professionalism**: Proposals look like they took weeks to create  
✅ **Funding Success**: Design options that meet lenders' underwriting requirements  
✅ **Transparency**: Clear explanation of every cost, incentive, and assumption  
✅ **Flexibility**: Supports multiple financing paths, technologies, and strategies  
✅ **Scalability**: Can handle 1,000s of projects without manual work  

---

## NEXT STEPS

1. **Review this architecture** - Ensure alignment with vision
2. **Prioritize phases** - Which features matter most?
3. **Estimate resources** - How many developers for 8-week build?
4. **Start Phase 1** - Build Developer Base model
5. **Integrate incrementally** - Test each component before next phase
6. **Deploy to production** - Start with beta users
7. **Gather feedback** - Iterate based on real usage

---

**This is a comprehensive blueprint for transforming Eagle Eye into a professional-grade, funding-ready development platform. The system maintains ease-of-use while adding sophisticated financial engineering, compliance, and investor-ready documentation capabilities.**
