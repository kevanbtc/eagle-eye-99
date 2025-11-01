# 🦅 EagleEye.NET — Estimating & Precon System (Clean Architecture)

**What you get** (ready for GitHub Codespaces / Dev Containers):

- ASP.NET Core **Web API** with OpenAPI/Swagger at `/swagger`
- **Clean Architecture**: Domain, Application, Infrastructure, Modules
- **Estimating Module** with domain entities, EF Core, and a **PricingEngine**
- **PostgreSQL** + **Redis** + optional **Seq** via `docker-compose.yml`
- **Hangfire** jobs ready (background tasks), **Serilog** logging
- **Blazor Web** placeholder for UI wiring (can be replaced with your preferred stack)
- GitHub Actions CI for build + tests

## Quickstart (Codespaces or local Dev Container)

1. Start services:

```bash
docker compose up -d
```

2. Restore & run API:

```bash
cd src/EagleEye.Api
dotnet restore
dotnet run
```

3. API is on `http://localhost:8080` (Codespaces will forward). Open:

- OpenAPI: `http://localhost:8080/swagger`
- Health: `GET /health`
- Sample calc: `POST /api/estimating/calc`

4. Apply EF Core migrations (you can generate new ones as needed):

```bash
cd src/EagleEye.Api
# (If you add migrations)
# dotnet ef migrations add Initial --project ../EagleEye.Infrastructure --startup-project .
# dotnet ef database update --project ../EagleEye.Infrastructure --startup-project .
```

## Environment

- Default PostgreSQL: `Host=localhost;Port=5432;Database=eagleeye;Username=eagle;Password=eagle`
- Redis: `localhost:6379`

> Note: Packages are referenced with floating versions (8.* etc.) to keep you on stable .NET 8 lines. Codespaces will restore latest minors.

---

## Structure

```
src/
  EagleEye.Api/                 # Web API (ASP.NET Core)
  EagleEye.Web/                 # Blazor placeholder
  EagleEye.Domain/              # Entities
  EagleEye.Application/         # DTOs + PricingEngine
  EagleEye.Infrastructure/      # EF Core Db + Repos
  EagleEye.Modules.Estimating/  # Controllers & module services
tests/
  EagleEye.Tests/               # xUnit placeholder
```

## Estimating Concepts Included

- **Assembly** (CSI code, unit, formulas)
- **AssemblyItem** (material/labor/equipment with wastage)
- **RateCatalogueItem** (region/vendor/validity)
- **VendorQuote** (import-ready)
- **TakeoffPackage** (sheets/zones/quantities)
- **Estimate** + **EstimateLine** (calc + OH&P)
- **OHPRule** (overhead/profit policy)
- **RiskItem** (contingency link)
- **XactimateCode** (crosswalk export later)

## License

You own whatever you build here. This scaffold is MIT.
