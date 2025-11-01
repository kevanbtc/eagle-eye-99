# EagleEye.NET Build Review – Missing Components

## Critical Missing Items

### 1. **Solution File (.sln)** ❌ CRITICAL
- **Issue**: `dotnet build` from root fails with `MSB1003: Specify a project or solution file`
- **Impact**: Cannot build entire project tree from root; users must build individual projects
- **Fix**: Create `EagleEye.NET.sln` and add all projects to it

### 2. **API launchSettings.json** ❌ IMPORTANT
- **Issue**: No debug profile configuration for Kestrel
- **Location**: Should be at `src/EagleEye.Api/Properties/launchSettings.json`
- **Impact**: Port binding may default incorrectly; Swagger URL unclear
- **Required Fields**: 
  - HTTP profile on port 5000
  - HTTPS profile on port 5001
  - Environment variables (ASPNETCORE_ENVIRONMENT, etc.)

### 3. **Web project scaffolding incomplete** ⚠️ MEDIUM
- **Issue**: `EagleEye.Web/Program.cs` is minimal; no real Blazor or Razor Pages setup
- **Impact**: Web tier is just a stub; not production-ready
- **Options**:
  - Expand to full Blazor Server or WebAssembly
  - OR document as "placeholder" and keep minimal

### 4. **Global usings file** ⚠️ MINOR
- **Issue**: No `GlobalUsings.cs` defined across projects
- **Impact**: Repeated `using` statements; not critical but clutters code
- **Fix**: Optional; can add per-project GlobalUsings or leave as-is

### 5. **EF Core migrations** ⚠️ IMPORTANT
- **Issue**: No migrations folder or initial migration in Infrastructure
- **Impact**: Database schema not tracked in code; devs can't run `dotnet ef database update`
- **Fix**: Create `Infrastructure/Migrations/Initial` migration
  - Command: `dotnet ef migrations add Initial --project src/EagleEye.Infrastructure --startup-project src/EagleEye.Api`

### 6. **Health check endpoint** ⚠️ MEDIUM
- **Issue**: README mentions `GET /health` but not implemented
- **Impact**: Kubernetes/container orchestration expects health checks
- **Fix**: Add `AddHealthChecks()` to DI and `MapHealthChecks()` to endpoints

### 7. **Configuration/appsettings variations** ⚠️ MINOR
- **Issue**: Only `appsettings.json` exists; missing `appsettings.Development.json` and `appsettings.Production.json`
- **Impact**: No environment-specific overrides (logging levels, DB hosts, feature flags)
- **Fix**: Add Development and Production config files

### 8. **Dockerfile & Docker Compose API service** ⚠️ MEDIUM
- **Issue**: `docker-compose.yml` has Postgres, Redis, Seq but **no API service**
- **Impact**: Can't run full stack in containers; only infra runs
- **Fix**: Add `eagleeye-api` service to docker-compose.yml

### 9. **CI/CD workflow validation** ⚠️ MINOR
- **Issue**: `.github/workflows/dotnet.yml` created but not validated locally
- **Status**: GitHub will validate on push; should work (standard template)
- **Fix**: Minor; verify paths and dotnet version match

### 10. **Serilog logging integration** ⚠️ MEDIUM
- **Issue**: README mentions Serilog + Seq, but **not wired in Program.cs**
- **Impact**: Logging goes to console only; structured logging to Seq is unavailable
- **Fix**: Add `UseSerilog()` in Program.cs and configure Seq sink

### 11. **Hangfire job configuration** ⚠️ MEDIUM
- **Issue**: README mentions Hangfire ready but **not configured**
- **Impact**: No background job scheduler wired
- **Fix**: Add Hangfire DI + dashboard mapping (optional; lower priority)

### 12. **README.md linting** ⚠️ MINOR
- **Issue**: Markdown linter flags:
  - MD029: Ordered list numbering inconsistency
  - MD040: Fenced code blocks missing language specifiers
- **Fix**: Already noted; update code block markers (e.g., ` ```bash ` vs ` ``` `)

### 13. **appsettings.json – outdated connection string** ⚠️ MINOR
- **Issue**: Stored value says `eagle:eagle` but older notes may reference `postgres:postgres`
- **Status**: FIXED (already updated to match docker-compose)
- **Verify**: Current file has `Username=eagle;Password=eagle` ✅

---

## Summary Table

| Component | Status | Severity | Impact |
|-----------|--------|----------|--------|
| Solution file (.sln) | ❌ Missing | CRITICAL | Cannot build from root |
| launchSettings.json | ❌ Missing | HIGH | Port/debug profile unclear |
| Initial EF migration | ❌ Missing | HIGH | DB schema not in code |
| Health endpoint | ❌ Missing | MEDIUM | K8s/container readiness unknown |
| Serilog config | ❌ Missing | MEDIUM | Structured logging disabled |
| Docker Compose API | ❌ Missing | MEDIUM | Full stack can't run in containers |
| Environment configs | ⚠️ Partial | MEDIUM | No per-environment overrides |
| Hangfire wiring | ⚠️ Partial | MEDIUM | Background jobs disabled |
| Web project | ⚠️ Stub | MEDIUM | UI layer incomplete |
| GlobalUsings | ⚠️ Partial | LOW | Code repetition |
| Dockerfile (API) | ❌ Missing | MEDIUM | Can't containerize API directly |

---

## Recommended Fix Order

1. **Create `EagleEye.NET.sln`** – unblocks root-level builds
2. **Add `launchSettings.json`** – ensures consistent debug experience
3. **Create initial migration** – gets DB schema under version control
4. **Add Serilog wiring** – enables structured logging as advertised
5. **Wire health checks** – production-ready observability
6. **Add Docker API service** – full stack in containers
7. **Environment configs** – per-environment customization
8. **Dockerfile** – optional; enables standalone API containerization
9. **Hangfire** – optional; background job support
10. **README linting** – polish; documentation accuracy
