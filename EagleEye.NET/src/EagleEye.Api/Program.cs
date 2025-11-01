using EagleEye.Application;
using EagleEye.Infrastructure;
using EagleEye.Modules.Estimating.Controllers;
using Microsoft.AspNetCore.Mvc.ApplicationParts;
using Microsoft.EntityFrameworkCore;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

var services = builder.Services;
var config = builder.Configuration;

// Configure Serilog
builder.Host.UseSerilog((context, loggerConfig) =>
{
    loggerConfig
        .MinimumLevel.Information()
        .WriteTo.Console()
        .WriteTo.Seq(config["Seq:Url"] ?? "http://localhost:5341");
});

// Add services to the container.
var mvc = services.AddControllers();
mvc.PartManager.ApplicationParts.Add(new AssemblyPart(typeof(EstimatingController).Assembly));

services.AddEndpointsApiExplorer();
services.AddSwaggerGen();
services.AddScoped<PricingEngine>();
services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>();

var connStr = config.GetConnectionString("Default") ??
              "Host=localhost;Port=5432;Database=eagleeye;Username=eagle;Password=eagle";
services.AddDbContext<AppDbContext>(o => o.UseNpgsql(connStr));

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseSerilogRequestLogging();
app.UseRouting();
app.MapControllers();
app.MapHealthChecks("/health");

app.Run();
