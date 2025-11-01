using EagleEye.Application;
using EagleEye.Domain;
using Microsoft.AspNetCore.Mvc;

namespace EagleEye.Modules.Estimating.Controllers;

[ApiController]
[Route("api/estimating")]
public sealed class EstimatingController(PricingEngine engine) : ControllerBase
{
    [HttpPost("price")] 
    public ActionResult<Estimate> Price([FromBody] PriceRequest request)
    {
        if (request is null) return BadRequest();

        var estimate = new Estimate
        {
            Id = Guid.NewGuid(),
            Project = request.Project ?? string.Empty,
            Lines = request.Lines.Select(l => new EstimateLine
            {
                Id = Guid.NewGuid(),
                AssemblyId = l.AssemblyId ?? Guid.Empty,
                AssemblyCode = l.AssemblyCode ?? string.Empty,
                AssemblyName = l.AssemblyName ?? string.Empty,
                Quantity = l.Quantity,
                UnitCost = l.UnitCost
            }).ToList()
        };

        var ohp = request.OHP is null ? null : new OHPRule
        {
            Id = Guid.NewGuid(),
            Trade = request.OHP.Trade ?? "GENERAL",
            OverheadPct = request.OHP.OverheadPct,
            ProfitPct = request.OHP.ProfitPct
        };

        var risks = (request.Risks ?? []).Select(r => new RiskItem
        {
            Id = Guid.NewGuid(),
            Description = r.Description ?? string.Empty,
            Severity = r.Severity,
            ContingencyPct = r.ContingencyPct
        });

        var priced = engine.PriceEstimate(estimate, ohp, risks);
        return Ok(priced);
    }
}

public sealed record PriceRequest
{
    public string? Project { get; init; }
    public List<PriceLine> Lines { get; init; } = new();
    public OHPReq? OHP { get; init; }
    public List<RiskReq>? Risks { get; init; }
}

public sealed record PriceLine
{
    public Guid? AssemblyId { get; init; }
    public string? AssemblyCode { get; init; }
    public string? AssemblyName { get; init; }
    public decimal Quantity { get; init; }
    public decimal UnitCost { get; init; }
}

public sealed record OHPReq
{
    public string? Trade { get; init; }
    public decimal OverheadPct { get; init; }
    public decimal ProfitPct { get; init; }
}

public sealed record RiskReq
{
    public string? Description { get; init; }
    public int Severity { get; init; }
    public decimal ContingencyPct { get; init; }
}
