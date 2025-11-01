using EagleEye.Application;
using EagleEye.Domain;
using FluentAssertions;
using Xunit;

namespace EagleEye.Tests;

public class PricingEngineTests
{
    [Fact]
    public void PriceEstimate_Computes_Totals()
    {
        var engine = new PricingEngine();
        var estimate = new Estimate
        {
            Lines =
            [
                new EstimateLine { Quantity = 10, UnitCost = 5 }, // 50
                new EstimateLine { Quantity = 3, UnitCost = 20 }  // 60
            ]
        };
        var ohp = new OHPRule { OverheadPct = 0.1m, ProfitPct = 0.1m };
        var risks = new[] { new RiskItem { ContingencyPct = 0.05m } };

        var priced = engine.PriceEstimate(estimate, ohp, risks);

        priced.Subtotal.Should().Be(110m);
        priced.Overhead.Should().Be(11.00m); // 10% of subtotal
        priced.Profit.Should().Be(12.10m);   // 10% of (subtotal + OH)
        priced.Contingency.Should().Be(5.50m); // 5% of subtotal
        priced.Total.Should().Be(138.60m);
    }
}
