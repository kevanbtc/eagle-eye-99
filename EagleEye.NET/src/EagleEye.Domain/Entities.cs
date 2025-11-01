namespace EagleEye.Domain;

public enum ItemKind { Material, Labor, Equipment }

public sealed class Assembly
{
    public Guid Id { get; set; }
    public string Code { get; set; } = ""; // CSI/UniFormat
    public string Name { get; set; } = "";
    public string Unit { get; set; } = "EA"; // SF, LF, EA, etc.
    public string? Formula { get; set; } // Expression to compute qty from takeoff attrs
    public List<AssemblyItem> Items { get; set; } = new();
}

public sealed class AssemblyItem
{
    public Guid Id { get; set; }
    public Guid AssemblyId { get; set; }
    public ItemKind Kind { get; set; }
    public string Name { get; set; } = "";
    public string Unit { get; set; } = "EA";
    public decimal BaseCost { get; set; } // cost per unit
    public decimal WasteFactor { get; set; } // 0.10 = +10%
    public decimal Productivity { get; set; } // qty/unit labor hour for labor items
}

public sealed class RateCatalogueItem
{
    public Guid Id { get; set; }
    public string Region { get; set; } = "US-GEN";
    public string Vendor { get; set; } = "BASE";
    public string Name { get; set; } = "";
    public string Unit { get; set; } = "EA";
    public decimal Cost { get; set; }
    public DateTime EffectiveFrom { get; set; } = DateTime.UtcNow.Date;
    public DateTime? EffectiveTo { get; set; }
}

public sealed class VendorQuote
{
    public Guid Id { get; set; }
    public string Vendor { get; set; } = "";
    public string ItemName { get; set; } = "";
    public string Unit { get; set; } = "EA";
    public decimal Price { get; set; }
    public DateTime ValidUntil { get; set; }
}

public sealed class TakeoffPackage
{
    public Guid Id { get; set; }
    public string Project { get; set; } = "";
    public string Sheet { get; set; } = "";
    public string Zone { get; set; } = "";
    public Dictionary<string, decimal> Quantities { get; set; } = new(); // e.g., {"SF": 123.4}
}

public sealed class OHPRule
{
    public Guid Id { get; set; }
    public string Trade { get; set; } = "GENERAL";
    public decimal OverheadPct { get; set; } // 0.10
    public decimal ProfitPct { get; set; }   // 0.10
}

public sealed class RiskItem
{
    public Guid Id { get; set; }
    public string Description { get; set; } = "";
    public int Severity { get; set; } // 1-5
    public decimal ContingencyPct { get; set; } // 0.05 adds to estimate
}

public sealed class XactimateCode
{
    public Guid Id { get; set; }
    public Guid AssemblyId { get; set; }
    public string Code { get; set; } = ""; // e.g., RFG... etc.
}

public sealed class Estimate
{
    public Guid Id { get; set; }
    public string Project { get; set; } = "";
    public DateTime CreatedOn { get; set; } = DateTime.UtcNow;
    public List<EstimateLine> Lines { get; set; } = new();
    public decimal Subtotal { get; set; }
    public decimal Overhead { get; set; }
    public decimal Profit { get; set; }
    public decimal Contingency { get; set; }
    public decimal Total { get; set; }
}

public sealed class EstimateLine
{
    public Guid Id { get; set; }
    public Guid EstimateId { get; set; }
    public Guid AssemblyId { get; set; }
    public string AssemblyCode { get; set; } = "";
    public string AssemblyName { get; set; } = "";
    public decimal Quantity { get; set; }
    public decimal UnitCost { get; set; }
    public decimal LineTotal { get; set; }
}
