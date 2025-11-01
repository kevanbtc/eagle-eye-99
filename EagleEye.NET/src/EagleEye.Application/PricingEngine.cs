using EagleEye.Domain;

namespace EagleEye.Application;

public sealed class PricingEngine
{
    public Estimate PriceEstimate(Estimate estimate, OHPRule? ohpRule, IEnumerable<RiskItem>? risks = null)
    {
        if (estimate is null) throw new ArgumentNullException(nameof(estimate));

        // Compute line totals and subtotal
        decimal subtotal = 0m;
        foreach (var line in estimate.Lines)
        {
            line.LineTotal = Math.Round(line.Quantity * line.UnitCost, 2, MidpointRounding.AwayFromZero);
            subtotal += line.LineTotal;
        }
        estimate.Subtotal = Math.Round(subtotal, 2, MidpointRounding.AwayFromZero);

        // Overhead & Profit
        var oh = ohpRule?.OverheadPct ?? 0m;
        var pr = ohpRule?.ProfitPct ?? 0m;
        estimate.Overhead = Math.Round(estimate.Subtotal * oh, 2, MidpointRounding.AwayFromZero);
        estimate.Profit = Math.Round((estimate.Subtotal + estimate.Overhead) * pr, 2, MidpointRounding.AwayFromZero);

        // Contingency from risks
        decimal riskPct = 0m;
        if (risks != null)
        {
            riskPct = risks.Sum(r => r.ContingencyPct);
            riskPct = Math.Clamp(riskPct, 0m, 0.50m); // cap at +50%
        }
        estimate.Contingency = Math.Round(estimate.Subtotal * riskPct, 2, MidpointRounding.AwayFromZero);

        estimate.Total = estimate.Subtotal + estimate.Overhead + estimate.Profit + estimate.Contingency;
        estimate.Total = Math.Round(estimate.Total, 2, MidpointRounding.AwayFromZero);
        return estimate;
    }
}
