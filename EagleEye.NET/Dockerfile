FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["src/EagleEye.Domain/EagleEye.Domain.csproj", "src/EagleEye.Domain/"]
COPY ["src/EagleEye.Application/EagleEye.Application.csproj", "src/EagleEye.Application/"]
COPY ["src/EagleEye.Infrastructure/EagleEye.Infrastructure.csproj", "src/EagleEye.Infrastructure/"]
COPY ["src/EagleEye.Modules.Estimating/EagleEye.Modules.Estimating.csproj", "src/EagleEye.Modules.Estimating/"]
COPY ["src/EagleEye.Api/EagleEye.Api.csproj", "src/EagleEye.Api/"]

RUN dotnet restore "src/EagleEye.Api/EagleEye.Api.csproj"

COPY . .

RUN dotnet build "src/EagleEye.Api/EagleEye.Api.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "src/EagleEye.Api/EagleEye.Api.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=publish /app/publish .

EXPOSE 5000
ENV ASPNETCORE_URLS=http://+:5000
ENTRYPOINT ["dotnet", "EagleEye.Api.dll"]
