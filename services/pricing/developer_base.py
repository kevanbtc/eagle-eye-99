"""
Eagle Eye - Developer Base Model System (Phase 1 Starter)
Services: pricing/developer_base.py

This module provides the DeveloperBase class and pricing tier support.
Integrates with existing demo.py and PricingEngine.

QUICK START:
    developer_base = DeveloperBase("residential", 5000, "30601")
    cost = developer_base.calculate_baseline()  # $500,000 (example)
    
    # Apply upgrades
    solar = UPGRADE_CATALOG["SOLAR_ELECTRIC"][0]
    upgraded_cost = developer_base.add_upgrade(solar)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class PricingTier(Enum):
    """Three standard pricing tiers"""
    STANDARD = 1.0      # Base cost
    PREMIUM = 1.15      # 15% better finishes
    LUXURY = 1.30       # 30% high-end finishes


class BuildingType(Enum):
    """Supported building types"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MIXED_USE = "mixed_use"
    RETAIL = "retail"
    OFFICE = "office"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"


# Regional pricing multipliers (base data from demo.py)
REGIONAL_FACTORS = {
    "30601": {"city": "Madison", "state": "GA", "labor": 0.92, "material": 0.95, "permit": 450},
    "30303": {"city": "Atlanta", "state": "GA", "labor": 1.05, "material": 1.08, "permit": 550},
    "33139": {"city": "Miami", "state": "FL", "labor": 1.08, "material": 1.12, "permit": 600},
    "27601": {"city": "Raleigh", "state": "NC", "labor": 0.98, "material": 1.00, "permit": 500},
}

# Cost per square foot by building type
BASELINE_COST_BY_TYPE = {
    "residential": 100,      # $100/sqft
    "commercial": 150,       # $150/sqft
    "industrial": 80,        # $80/sqft
    "mixed_use": 130,        # $130/sqft
    "retail": 140,           # $140/sqft
    "office": 160,           # $160/sqft
    "healthcare": 250,       # $250/sqft
    "education": 180,        # $180/sqft
}

# Energy use baseline (kWh/year per sqft)
ENERGY_USE_PER_SQFT = {
    "residential": 10,       # 10 kWh/sqft/year
    "commercial": 15,        # 15 kWh/sqft/year
    "industrial": 20,        # 20 kWh/sqft/year
    "office": 18,            # 18 kWh/sqft/year
}

# CO2 conversion factor (lbs CO2 per kWh)
CO2_FACTOR = 0.92  # Average US grid

# Water use baseline (gallons/year per sqft)
WATER_USE_PER_SQFT = {
    "residential": 15,       # 15 gal/sqft/year
    "commercial": 8,         # 8 gal/sqft/year
    "industrial": 50,        # 50 gal/sqft/year
    "office": 5,             # 5 gal/sqft/year
}


@dataclass
class DeveloperBase:
    """
    The 'base case' - standard construction for a project.
    
    Defines:
    - Building type (residential, commercial, etc.)
    - Size (square footage)
    - Location (ZIP code for regional pricing)
    - Standard components included
    - Baseline costs, energy use, emissions
    
    Example:
        base = DeveloperBase("residential", 5000, "30601")
        base.calculate_baseline()
        print(f"Base cost: ${base.baseline_cost:,.0f}")
        print(f"Annual energy: {base.baseline_energy_kwh:,.0f} kWh")
    """
    
    building_type: str           # residential, commercial, etc.
    sqft: int                    # Square footage
    zip_code: str                # Location for regional factors
    pricing_tier: PricingTier = PricingTier.STANDARD
    
    # Calculated properties
    baseline_cost: float = 0.0
    baseline_energy_kwh: float = 0.0
    baseline_water_gal: float = 0.0
    baseline_co2_tons: float = 0.0
    components: Dict = None
    upgrades: List = None
    
    def __post_init__(self):
        """Initialize calculated properties"""
        if self.components is None:
            self.components = {}
        if self.upgrades is None:
            self.upgrades = []
    
    @property
    def regional_factor(self) -> Dict:
        """Get regional pricing factor for ZIP code"""
        return REGIONAL_FACTORS.get(
            self.zip_code,
            {"labor": 1.0, "material": 1.0, "permit": 500}
        )
    
    @property
    def cost_per_sqft(self) -> float:
        """Base cost per square foot for building type"""
        base_cost = BASELINE_COST_BY_TYPE.get(self.building_type, 100)
        # Apply tier multiplier
        return base_cost * self.pricing_tier.value
    
    def calculate_baseline(self) -> float:
        """
        Calculate total baseline cost for this project.
        
        Returns:
            float: Total project cost in dollars
        
        Formula:
            cost = sqft × cost_per_sqft × regional_labor_factor × tier_multiplier
        """
        
        # Base cost
        cost = self.sqft * self.cost_per_sqft * self.regional_factor["labor"]
        
        # Add permits
        cost += self.regional_factor.get("permit", 500)
        
        self.baseline_cost = cost
        return cost
    
    def calculate_baseline_energy(self) -> float:
        """Calculate annual baseline energy use in kWh"""
        energy_per_sqft = ENERGY_USE_PER_SQFT.get(self.building_type, 12)
        self.baseline_energy_kwh = self.sqft * energy_per_sqft
        
        # Calculate CO2
        self.baseline_co2_tons = self.baseline_energy_kwh * CO2_FACTOR / 2000  # Convert lbs to tons
        
        return self.baseline_energy_kwh
    
    def calculate_baseline_water(self) -> float:
        """Calculate annual baseline water use in gallons"""
        water_per_sqft = WATER_USE_PER_SQFT.get(self.building_type, 10)
        self.baseline_water_gal = self.sqft * water_per_sqft
        return self.baseline_water_gal
    
    def get_base_components(self) -> Dict:
        """
        Get list of standard components for this building type.
        
        Returns:
            Dict: {"component_name": {"quantity": X, "cost": Y}}
        """
        
        components_by_type = {
            "residential": {
                "Foundation": {"sqft": self.sqft, "unit_cost": 8},
                "Framing": {"sqft": self.sqft, "unit_cost": 9},
                "Roof": {"sqft": self.sqft, "unit_cost": 9},
                "Exterior": {"sqft": self.sqft, "unit_cost": 15},
                "HVAC": {"capacity_tons": 1 + (self.sqft / 1500), "unit_cost": 7000},
                "Windows": {"count": self.sqft / 100, "unit_cost": 450},
                "Doors": {"count": self.sqft / 500, "unit_cost": 400},
                "Electrical": {"outlets": self.sqft / 50, "unit_cost": 150},
                "Plumbing": {"fixtures": self.sqft / 400, "unit_cost": 800},
                "Interior": {"sqft": self.sqft, "unit_cost": 12},
            },
            "commercial": {
                "Foundation": {"sqft": self.sqft, "unit_cost": 12},
                "Framing": {"sqft": self.sqft, "unit_cost": 15},
                "Roof": {"sqft": self.sqft, "unit_cost": 14},
                "Exterior": {"sqft": self.sqft, "unit_cost": 20},
                "HVAC": {"capacity_tons": 1 + (self.sqft / 500), "unit_cost": 10000},
                "Lighting": {"sqft": self.sqft, "unit_cost": 5},
                "Electrical": {"outlets": self.sqft / 30, "unit_cost": 200},
                "Plumbing": {"fixtures": self.sqft / 300, "unit_cost": 1200},
                "Interior": {"sqft": self.sqft, "unit_cost": 25},
            }
        }
        
        return components_by_type.get(self.building_type, {})
    
    def add_upgrade(self, upgrade: Dict) -> float:
        """
        Add an upgrade to this project.
        
        Args:
            upgrade: Dict with keys: name, cost, annual_savings, etc.
        
        Returns:
            float: New total project cost
        """
        
        self.upgrades.append(upgrade)
        return self.calculate_total_cost()
    
    def calculate_total_cost(self) -> float:
        """Calculate total cost including all upgrades"""
        total = self.baseline_cost
        for upgrade in self.upgrades:
            total += upgrade.get("cost", 0)
        return total
    
    def calculate_total_annual_savings(self) -> float:
        """Calculate total annual savings from all upgrades"""
        total_savings = 0
        for upgrade in self.upgrades:
            total_savings += upgrade.get("annual_savings", 0)
        return total_savings
    
    def get_summary(self) -> Dict:
        """
        Get comprehensive summary of this project.
        
        Returns:
            Dict with all key metrics
        """
        
        # Calculate if not done
        if self.baseline_cost == 0:
            self.calculate_baseline()
        if self.baseline_energy_kwh == 0:
            self.calculate_baseline_energy()
        if self.baseline_water_gal == 0:
            self.calculate_baseline_water()
        
        return {
            "project_info": {
                "building_type": self.building_type,
                "square_footage": self.sqft,
                "location": self.zip_code,
                "city": self.regional_factor.get("city", "Unknown"),
                "state": self.regional_factor.get("state", "XX"),
                "pricing_tier": self.pricing_tier.name,
            },
            
            "baseline": {
                "cost": self.baseline_cost,
                "cost_per_sqft": self.baseline_cost / self.sqft,
                "annual_energy_kwh": self.baseline_energy_kwh,
                "annual_water_gallons": self.baseline_water_gal,
                "annual_co2_tons": self.baseline_co2_tons,
            },
            
            "upgrades": {
                "count": len(self.upgrades),
                "total_cost": sum(u.get("cost", 0) for u in self.upgrades),
                "upgrades_list": [u.get("name", "Unknown") for u in self.upgrades],
            },
            
            "project_total": {
                "cost": self.calculate_total_cost(),
                "annual_savings": self.calculate_total_annual_savings(),
                "payback_years": self.calculate_payback_period(),
            },
        }
    
    def calculate_payback_period(self) -> float:
        """Calculate simple payback period in years"""
        annual_savings = self.calculate_total_annual_savings()
        if annual_savings <= 0:
            return float('inf')
        
        total_investment = sum(u.get("cost", 0) for u in self.upgrades)
        return total_investment / annual_savings if annual_savings > 0 else float('inf')


# Example upgrade catalog (will be expanded in Phase 2)
UPGRADE_CATALOG = {
    "SOLAR_ELECTRIC": [
        {
            "id": "SOLAR-5KW",
            "name": "5kW Solar System",
            "category": "renewable_energy",
            "cost": 12500,
            "annual_production_kwh": 6500,
            "annual_savings": 975,  # 6500 kWh × $0.15/kWh
            "federal_itc": 3750,    # 30% ITC
            "payback_years": 9.2,
        },
        {
            "id": "SOLAR-10KW",
            "name": "10kW Solar System",
            "category": "renewable_energy",
            "cost": 24000,
            "annual_production_kwh": 13000,
            "annual_savings": 1950,
            "federal_itc": 7200,
            "payback_years": 9.8,
        },
    ],
    
    "HVAC_EFFICIENCY": [
        {
            "id": "HVAC-SEER16",
            "name": "SEER 16+ High-Efficiency HVAC",
            "category": "efficiency",
            "cost": 8500,
            "annual_savings": 1200,
            "federal_credit": 600,
            "payback_years": 6.3,
        },
    ],
    
    "INSULATION": [
        {
            "id": "INSULATION-SPRAY",
            "name": "Spray Foam Insulation Upgrade",
            "category": "efficiency",
            "cost": 5000,
            "annual_savings": 800,
            "payback_years": 6.2,
        },
    ],
}


# Integration with existing demo.py
def integrate_with_pricing_engine(developer_base: DeveloperBase, 
                                  components: List[Dict]) -> Dict:
    """
    Integrate DeveloperBase with existing PricingEngine.
    
    This bridges the new Developer Base Model with the current system.
    
    Example:
        base = DeveloperBase("residential", 5000, "30601")
        components = [{"type": "HVAC", "quantity": 2}, ...]
        result = integrate_with_pricing_engine(base, components)
    """
    
    return {
        "base_cost": developer_base.calculate_baseline(),
        "components": developer_base.get_base_components(),
        "regional_factors": developer_base.regional_factor,
        "pricing_tier": developer_base.pricing_tier.name,
    }


if __name__ == "__main__":
    # Quick test
    print("Eagle Eye Developer Base Model - Phase 1")
    print("=" * 50)
    
    # Create a 5000 sqft residential project in Madison, GA
    base = DeveloperBase("residential", 5000, "30601")
    
    # Calculate baseline
    cost = base.calculate_baseline()
    print(f"\nProject: 5,000 sqft residential in Madison, GA")
    print(f"Baseline cost: ${cost:,.2f}")
    
    # Calculate energy
    energy = base.calculate_baseline_energy()
    print(f"Baseline energy: {energy:,.0f} kWh/year")
    print(f"Baseline CO2: {base.baseline_co2_tons:.1f} tons/year")
    
    # Add an upgrade
    solar_upgrade = UPGRADE_CATALOG["SOLAR_ELECTRIC"][0]
    total = base.add_upgrade(solar_upgrade)
    print(f"\nAfter adding 5kW solar:")
    print(f"Total cost: ${total:,.2f}")
    print(f"Annual savings: ${base.calculate_total_annual_savings():,.2f}")
    print(f"Payback: {base.calculate_payback_period():.1f} years")
    
    # Get summary
    print(f"\nProject Summary:")
    summary = base.get_summary()
    print(f"  Building type: {summary['project_info']['building_type']}")
    print(f"  Total cost: ${summary['project_total']['cost']:,.2f}")
    print(f"  Annual savings: ${summary['project_total']['annual_savings']:,.2f}")
