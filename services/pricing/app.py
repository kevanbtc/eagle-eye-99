"""
Eagle Eye Pricing Engine
TradeBase catalog + regional factors
"""
import pandas as pd
import sys
from typing import Dict, List, Any
from pathlib import Path

sys.path.append("../../packages/shared")
from models import LineItem, Estimate, EstimateSummary


def load_tradebase_catalog(csv_path: str = "../../infra/seeds/tradebase/catalog.csv") -> pd.DataFrame:
    """Load the TradeBase pricing catalog"""
    # In production, this would query from database
    # For now, return mock data
    return pd.DataFrame({
        "Trade": ["Concrete", "Framing", "Drywall", "Electrical", "Plumbing"],
        "Item": ["Foundation", "Wall Framing", "Drywall Install", "Rough-in", "Rough-in"],
        "UoM": ["LF", "SF", "SF", "EA", "EA"],
        "Unit Cost": [45.00, 8.50, 2.75, 850.00, 1200.00],
        "Region": ["Atlanta_GA"] * 5
    })


def load_regional_factors(region: str = "Atlanta_GA", cbsa_code: str = None, zip_code: str = None) -> Dict[str, float]:
    """
    Load regional adjustment factors with priority: ZIP > CBSA > Region default
    """
    # In production, query from database with priority
    # 1. Check for zip-specific factors
    # 2. Fall back to CBSA-level factors
    # 3. Fall back to region default
    
    base_factors = {
        "labor_idx": 1.02,
        "material_idx": 1.00,
        "demo_idx": 1.05,
        "permit_idx": 1.10
    }
    
    # Apply ZIP-level overrides if available
    if zip_code:
        zip_overrides = {
            "30301": {"labor_idx": 1.15, "material_idx": 1.05},  # Downtown Atlanta premium
            "30350": {"labor_idx": 1.12, "material_idx": 1.04},  # Sandy Springs
            "30518": {"labor_idx": 1.06, "material_idx": 1.01},  # Buford/Lake Lanier
        }
        if zip_code in zip_overrides:
            base_factors.update(zip_overrides[zip_code])
    
    # Apply CBSA-level overrides if available
    elif cbsa_code:
        cbsa_overrides = {
            "12060": {"labor_idx": 1.08, "material_idx": 1.02},  # Atlanta metro
            "31420": {"labor_idx": 0.92, "material_idx": 0.98},  # Macon
            "46660": {"labor_idx": 0.88, "material_idx": 0.96},  # Valdosta
        }
        if cbsa_code in cbsa_overrides:
            base_factors.update(cbsa_overrides[cbsa_code])
    
    return base_factors


def get_spec_tier_pricing(tier: str = "Standard") -> Dict[str, Dict[str, Any]]:
    """
    Load spec tier bundle pricing
    Returns dict of category -> item details with base costs
    """
    # In production, query from spec_tier_bundles table
    # For now, return representative pricing
    
    spec_bundles = {
        "Standard": {
            "Roofing": {"item": "Architectural Shingle - 30yr", "unit_cost": 3.25, "uom": "SF"},
            "Windows": {"item": "Vinyl Window - Energy Star", "unit_cost": 385, "uom": "EA"},
            "Flooring_Carpet": {"item": "Carpet - Nylon", "unit_cost": 3.50, "uom": "SF"},
            "Flooring_Hard": {"item": "Luxury Vinyl Plank", "unit_cost": 4.25, "uom": "SF"},
            "Cabinets": {"item": "Semi-Custom Painted", "unit_cost": 185, "uom": "LF"},
            "Countertops": {"item": "Laminate or Basic Quartz", "unit_cost": 42, "uom": "SF"},
            "Fixtures": {"item": "Builder-Grade Faucets", "unit_cost": 145, "uom": "EA"},
            "Lighting": {"item": "Builder-Grade Fixtures", "unit_cost": 85, "uom": "EA"},
        },
        "Premium": {
            "Roofing": {"item": "Designer Shingle - 50yr", "unit_cost": 4.75, "uom": "SF"},
            "Windows": {"item": "Fiberglass Window - Low-E", "unit_cost": 625, "uom": "EA"},
            "Flooring_Hard": {"item": "Engineered Hardwood", "unit_cost": 8.50, "uom": "SF"},
            "Cabinets": {"item": "Custom Stained", "unit_cost": 295, "uom": "LF"},
            "Countertops": {"item": "Mid-Grade Quartz/Granite", "unit_cost": 68, "uom": "SF"},
            "Fixtures": {"item": "Mid-Range Designer", "unit_cost": 285, "uom": "EA"},
            "Lighting": {"item": "Designer Fixtures", "unit_cost": 195, "uom": "EA"},
        },
        "Luxury": {
            "Roofing": {"item": "Standing Seam Metal", "unit_cost": 12.50, "uom": "SF"},
            "Windows": {"item": "Wood-Clad Premium - Impact", "unit_cost": 1150, "uom": "EA"},
            "Flooring_Hard": {"item": "Solid Hardwood - Wide Plank", "unit_cost": 14.00, "uom": "SF"},
            "Cabinets": {"item": "Full Custom Premium", "unit_cost": 485, "uom": "LF"},
            "Countertops": {"item": "Premium Stone - Waterfall", "unit_cost": 125, "uom": "SF"},
            "Fixtures": {"item": "Luxury Brands - Premium", "unit_cost": 625, "uom": "EA"},
            "Lighting": {"item": "Luxury Chandeliers/Pendants", "unit_cost": 485, "uom": "EA"},
        }
    }
    
    return spec_bundles.get(tier, spec_bundles["Standard"])


def calculate_line_items(
    quantities: List[Dict[str, Any]],
    catalog: pd.DataFrame,
    factors: Dict[str, float],
    spec_tier: str = "Standard"
) -> List[LineItem]:
    """
    Calculate line items from quantities with spec tier pricing
    """
    line_items = []
    spec_pricing = get_spec_tier_pricing(spec_tier)
    
    for qty in quantities:
        trade = qty.get("trade", "General")
        item = qty.get("item", "Unknown")
        category = qty.get("category")  # e.g., "Roofing", "Windows", "Flooring_Hard"
        uom = qty.get("uom", "EA")
        quantity = qty.get("quantity", 0)
        
        # First, try to match from spec tier bundles (for finish items)
        if category and category in spec_pricing:
            spec_item = spec_pricing[category]
            base_unit_cost = spec_item["unit_cost"]
            item = spec_item["item"]  # Use spec tier item name
            uom = spec_item["uom"]
        else:
            # Fallback to catalog lookup for structural/rough items
            match = catalog[
                (catalog["Trade"] == trade) & 
                (catalog["Item"] == item)
            ]
            
            if not match.empty:
                base_unit_cost = float(match.iloc[0]["Unit Cost"])
            else:
                # Use placeholder
                base_unit_cost = 100.00
        
        # Apply regional factors
        adjusted_cost = base_unit_cost * factors.get("labor_idx", 1.0) * factors.get("material_idx", 1.0)
        ext_cost = round(quantity * adjusted_cost, 2)
        
        line_items.append(LineItem(
            wbs=qty.get("wbs", "01.01"),
            assembly=qty.get("assembly", trade),
            line_item=item,
            uom=uom,
            qty=quantity,
            qty_confidence=qty.get("confidence", "Medium"),
            needs_rfi=qty.get("confidence") == "Low",
            unit_cost=round(adjusted_cost, 2),
            ext_cost=ext_cost,
            trade=trade
        ))
    
    return line_items


def calculate_summary(
    line_items: List[LineItem],
    overhead_pct: float = 10.0,
    profit_pct: float = 10.0,
    contingency_pct: float = 5.0
) -> EstimateSummary:
    """Calculate estimate summary with O&P and contingency"""
    subtotal = sum(item.ext_cost for item in line_items)
    
    overhead_amt = round(subtotal * (overhead_pct / 100), 2)
    profit_amt = round(subtotal * (profit_pct / 100), 2)
    total = subtotal + overhead_amt + profit_amt
    
    contingency_amt = round(total * (contingency_pct / 100), 2)
    grand_total = total + contingency_amt
    
    return EstimateSummary(
        subtotal=subtotal,
        overhead_pct=overhead_pct,
        profit_pct=profit_pct,
        overhead_amt=overhead_amt,
        profit_amt=profit_amt,
        total=total,
        contingency_pct=contingency_pct,
        contingency_amt=contingency_amt,
        grand_total=grand_total
    )


def create_estimate(
    project_id: str,
    quantities: List[Dict[str, Any]],
    region: str = "Atlanta_GA",
    cbsa_code: str = None,
    zip_code: str = None,
    spec_tier: str = "Standard",
    overhead_pct: float = 10.0,
    profit_pct: float = 10.0
) -> Estimate:
    """
    Create a complete estimate from quantities with regional and spec tier adjustments
    """
    # Load catalog and factors
    catalog = load_tradebase_catalog()
    factors = load_regional_factors(region, cbsa_code, zip_code)
    
    # Calculate line items with spec tier pricing
    line_items = calculate_line_items(quantities, catalog, factors, spec_tier)
    
    # Group by trade
    base_items = {}
    for item in line_items:
        trade = item.trade or "General"
        if trade not in base_items:
            base_items[trade] = []
        base_items[trade].append(item)
    
    # Calculate summary
    summary = calculate_summary(line_items, overhead_pct, profit_pct)
    
    return Estimate(
        project_id=project_id,
        base=base_items,
        alternates={},
        allowances={
            "Permits": round(summary.subtotal * 0.02, 2),
            "Testing & Inspections": 2500.00,
            "Misc Materials": 1500.00
        },
        summary=summary,
        version=1
    )


if __name__ == "__main__":
    # Example usage
    mock_quantities = [
        {"wbs": "01.01", "trade": "Concrete", "item": "Foundation", "uom": "LF", "quantity": 200, "assembly": "Foundation"},
        {"wbs": "02.01", "trade": "Framing", "item": "Wall Framing", "uom": "SF", "quantity": 3500, "assembly": "Wall Framing"},
        {"wbs": "03.01", "trade": "Drywall", "item": "Drywall Install", "uom": "SF", "quantity": 7000, "assembly": "Interior Finish"},
    ]
    
    estimate = create_estimate("test-project", mock_quantities)
    
    print(f"\nEstimate Summary:")
    print(f"  Subtotal: ${estimate.summary.subtotal:,.2f}")
    print(f"  O&P: ${estimate.summary.overhead_amt + estimate.summary.profit_amt:,.2f}")
    print(f"  Contingency: ${estimate.summary.contingency_amt:,.2f}")
    print(f"  Grand Total: ${estimate.summary.grand_total:,.2f}")
