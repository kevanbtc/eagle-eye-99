var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => Results.Text("EagleEye.Web running", "text/plain"));

app.Run();
