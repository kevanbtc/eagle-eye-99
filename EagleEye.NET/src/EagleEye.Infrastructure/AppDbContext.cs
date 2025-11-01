using EagleEye.Domain;
using Microsoft.EntityFrameworkCore;

namespace EagleEye.Infrastructure;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Assembly> Assemblies => Set<Assembly>();
    public DbSet<AssemblyItem> AssemblyItems => Set<AssemblyItem>();
    public DbSet<RateCatalogueItem> RateCatalogue => Set<RateCatalogueItem>();
    public DbSet<VendorQuote> VendorQuotes => Set<VendorQuote>();
    public DbSet<TakeoffPackage> Takeoffs => Set<TakeoffPackage>();
    public DbSet<OHPRule> OHPRules => Set<OHPRule>();
    public DbSet<RiskItem> Risks => Set<RiskItem>();
    public DbSet<XactimateCode> Xactimate => Set<XactimateCode>();
    public DbSet<Estimate> Estimates => Set<Estimate>();
    public DbSet<EstimateLine> EstimateLines => Set<EstimateLine>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Assembly>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.Code).HasMaxLength(64);
            e.Property(x => x.Name).HasMaxLength(256);
            e.HasMany(x => x.Items).WithOne().HasForeignKey(ai => ai.AssemblyId);
        });

        modelBuilder.Entity<AssemblyItem>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.Name).HasMaxLength(256);
        });

        modelBuilder.Entity<RateCatalogueItem>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.Region).HasMaxLength(64);
            e.Property(x => x.Vendor).HasMaxLength(128);
            e.Property(x => x.Name).HasMaxLength(256);
        });

        modelBuilder.Entity<VendorQuote>(e => e.HasKey(x => x.Id));

        modelBuilder.Entity<TakeoffPackage>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.Project).HasMaxLength(128);
            e.Property(x => x.Sheet).HasMaxLength(64);
            e.Property(x => x.Zone).HasMaxLength(64);
            e.Property(x => x.Quantities)
             .HasConversion(
                v => System.Text.Json.JsonSerializer.Serialize(v, (System.Text.Json.JsonSerializerOptions?)null),
                v => System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, decimal>>(v, (System.Text.Json.JsonSerializerOptions?)null) ?? new())
             .HasColumnType("jsonb");
        });

        modelBuilder.Entity<OHPRule>(e => e.HasKey(x => x.Id));
        modelBuilder.Entity<RiskItem>(e => e.HasKey(x => x.Id));
        modelBuilder.Entity<XactimateCode>(e => e.HasKey(x => x.Id));

        modelBuilder.Entity<Estimate>(e =>
        {
            e.HasKey(x => x.Id);
            e.HasMany(x => x.Lines).WithOne().HasForeignKey(l => l.EstimateId);
        });
        modelBuilder.Entity<EstimateLine>(e => e.HasKey(x => x.Id));
    }
}
