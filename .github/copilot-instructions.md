# Eagle Eye - CRM + Senior Review + Pricing System

## Project Overview
Monorepo for Eagle Eye: a construction plan review and pricing system that ingests plan PDFs, runs code compliance checks, generates pricing estimates, and produces professional proposals.

## Architecture
- **Frontend**: Next.js + TypeScript + Tailwind + shadcn/ui
- **Backend Services**: FastAPI microservices (API, Parser, Rules, Pricing, Reports)
- **Orchestration**: MCP server + n8n workflows
- **Infrastructure**: PostgreSQL, MinIO (S3), Redis
- **Templates**: Jinja2 for PDF/CSV generation

## Project Status
- [x] Verify copilot-instructions.md file created
- [x] Clarify Project Requirements - Complete monorepo for plan review & pricing system
- [x] Scaffold the Project - All services, frontend, infra, and workflows created
- [ ] Customize the Project
- [ ] Install Required Extensions
- [ ] Compile the Project
- [ ] Create and Run Task
- [ ] Launch the Project
- [ ] Ensure Documentation is Complete

## Development Guidelines
- Use deterministic code checks first, LLM for last-mile polish only
- Maintain version control for plan graphs, findings, and estimates
- Follow FastAPI best practices for all Python services
- Use Pydantic models for data validation
- Shared types between Python and TypeScript via packages/shared
