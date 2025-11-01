# Eagle Eye Web Platform - Complete Architecture

**Status**: 🚀 Ready for implementation  
**Framework**: Next.js 14 + React 18 + TypeScript + Tailwind CSS  
**Backend Integration**: FastAPI microservices + MCP Server  
**Database**: PostgreSQL (via existing services)

---

## Platform Overview

### What Teams Can Do

1. **Dashboard**
   - View all projects at a glance
   - See project status, timeline, and budget
   - Track compliance issues and recommendations
   - Monitor proposal status

2. **Project Management**
   - Create new projects (manual or document-based)
   - Upload PDF plans and specifications
   - Auto-extract project data via AI
   - Manage team members and permissions

3. **Estimate Generation**
   - Generate line-item estimates with full breakdown
   - See costs by category (HVAC, Windows, Doors, etc.)
   - Apply regional factors automatically
   - Export as Excel, PDF, or CSV

4. **Upgrade & Enhancement Planning**
   - Browse upgrade catalog (Energy Star, LEED, Solar, etc.)
   - See cost/benefit for each upgrade
   - Multi-scenario comparison (Silver/Gold/Platinum)
   - Calculate ROI and payback period

5. **Financial Analysis**
   - View available incentives (federal, state, utility, local)
   - Compare financing options (cash, loan, lease, PPA)
   - See 25-year cash flow projections
   - Print funding-ready analysis

6. **Proposal Generation**
   - Create professional proposals automatically
   - Multiple output formats (PDF, HTML, Excel)
   - Customize for different audiences (investor, lender, homeowner)
   - Track proposal status and responses

7. **Document Management**
   - Upload plans, specs, questionnaires
   - AI extraction of project information
   - Auto-generate CRM records
   - Search and organize documents

8. **Team Collaboration**
   - Invite team members with role-based access
   - Comment on projects and estimates
   - Version history and change tracking
   - Export and share reports

---

## Technical Architecture

### Frontend Structure

```
apps/web/src/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/
│   │   ├── projects/[id]/
│   │   ├── estimates/[id]/
│   │   ├── proposals/[id]/
│   │   ├── upgrades/
│   │   ├── financial/[id]/
│   │   ├── team/
│   │   └── layout.tsx
│   ├── api/
│   │   ├── projects/
│   │   ├── estimates/
│   │   ├── proposals/
│   │   ├── documents/
│   │   └── financials/
│   ├── layout.tsx
│   └── page.tsx (homepage)
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── AuthGuard.tsx
│   ├── dashboard/
│   │   ├── ProjectCard.tsx
│   │   ├── StatsSummary.tsx
│   │   ├── RecentActivity.tsx
│   │   └── QuickActions.tsx
│   ├── projects/
│   │   ├── ProjectForm.tsx
│   │   ├── ProjectList.tsx
│   │   ├── DocumentUploader.tsx
│   │   └── ProjectDetails.tsx
│   ├── estimates/
│   │   ├── EstimateBuilder.tsx
│   │   ├── LineItemTable.tsx
│   │   ├── EstimatePreview.tsx
│   │   ├── ExportDialog.tsx
│   │   └── RegionalFactorView.tsx
│   ├── upgrades/
│   │   ├── UpgradeBrowser.tsx
│   │   ├── UpgradeCard.tsx
│   │   ├── UpgradeComparison.tsx
│   │   ├── ROICalculator.tsx
│   │   └── ScenarioBuilder.tsx
│   ├── financial/
│   │   ├── IncentiveCalculator.tsx
│   │   ├── FinancingComparison.tsx
│   │   ├── CashFlowChart.tsx
│   │   ├── ProposalBuilder.tsx
│   │   └── FundingReadyView.tsx
│   ├── proposals/
│   │   ├── ProposalPreview.tsx
│   │   ├── ProposalCustomizer.tsx
│   │   ├── ProposalExport.tsx
│   │   ├── ProposalStatus.tsx
│   │   └── SendProposal.tsx
│   ├── common/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   ├── DataTable.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorBoundary.tsx
│   └── layouts/
│       ├── DashboardLayout.tsx
│       └── MainLayout.tsx
├── hooks/
│   ├── useProjects.ts
│   ├── useEstimates.ts
│   ├── useProposals.ts
│   ├── useFinancials.ts
│   ├── useAuth.ts
│   ├── useDocuments.ts
│   ├── useUpgrades.ts
│   └── useApi.ts
├── lib/
│   ├── api.ts (HTTP client)
│   ├── auth.ts (Authentication)
│   ├── validation.ts (Form validation)
│   ├── formatting.ts (Currency, date, etc.)
│   ├── calculations.ts (Financial math)
│   └── types.ts (TypeScript interfaces)
├── store/
│   ├── authStore.ts (Zustand)
│   ├── projectStore.ts
│   ├── estimateStore.ts
│   ├── proposalStore.ts
│   └── uiStore.ts
└── styles/
    ├── globals.css
    └── variables.css
```

### Backend Integration Points

#### FastAPI Services (Existing)

```
services/
├── api/                    ← Main API service
│   ├── routes/projects.py
│   ├── routes/estimates.py
│   ├── routes/proposals.py
│   └── routes/documents.py
├── parser/                 ← PDF/document parsing
│   └── Enhanced for questionnaires
├── rules/                  ← Compliance checking
│   └── Rule engine
├── pricing/                ← Cost estimation
│   ├── pricing_engine.py
│   └── developer_base.py   ← New Phase 1
└── reports/                ← Proposal generation
    └── report_generator.py
```

#### New API Endpoints

```
POST   /api/v1/projects              - Create project
GET    /api/v1/projects              - List projects
GET    /api/v1/projects/:id          - Get project
PUT    /api/v1/projects/:id          - Update project
DELETE /api/v1/projects/:id          - Delete project

POST   /api/v1/documents/upload      - Upload PDF/Excel/Word
POST   /api/v1/documents/parse       - AI parse document

POST   /api/v1/estimates             - Generate estimate
GET    /api/v1/estimates/:id         - Get estimate
PUT    /api/v1/estimates/:id         - Update estimate
POST   /api/v1/estimates/:id/export  - Export (PDF/Excel/CSV)

GET    /api/v1/upgrades              - List available upgrades
GET    /api/v1/upgrades/catalog      - Full upgrade catalog
POST   /api/v1/upgrades/recommend    - Get recommendations

POST   /api/v1/financial/incentives  - Calculate incentives
POST   /api/v1/financial/financing   - Compare financing options
POST   /api/v1/financial/cashflow    - Generate 25-year projections

POST   /api/v1/proposals             - Generate proposal
GET    /api/v1/proposals/:id         - Get proposal
PUT    /api/v1/proposals/:id         - Update proposal
POST   /api/v1/proposals/:id/export  - Export proposal
POST   /api/v1/proposals/:id/send    - Send via email

GET    /api/v1/team                  - List team members
POST   /api/v1/team                  - Invite member
PUT    /api/v1/team/:id              - Update role
DELETE /api/v1/team/:id              - Remove member

POST   /api/v1/auth/login            - User login
POST   /api/v1/auth/register         - User registration
POST   /api/v1/auth/logout           - User logout
```

---

## User Workflows

### Workflow 1: Quick Estimate (5 minutes)

```
1. Dashboard → "New Estimate"
2. Enter basic info (building type, sqft, location)
3. System auto-calculates baseline estimate
4. Review line items
5. Export as PDF/Excel
6. Done!
```

### Workflow 2: Full Project with Upgrades (30 minutes)

```
1. Create Project
2. Upload PDF plans (optional)
3. Select building type + upgrades
4. System generates estimate with all options
5. View 3 scenarios (Silver/Gold/Platinum)
6. Compare costs and ROI
7. Select preferred scenario
8. Generate funding-ready proposal
9. Export and send
```

### Workflow 3: Document Upload & Auto-Processing (15 minutes)

```
1. Upload project PDF (plans + specs)
2. AI extracts project information
3. Auto-generate CRM record
4. Review extracted data
5. System auto-recommends upgrades
6. Generate estimate
7. Create proposal
8. Done!
```

### Workflow 4: Funding Package Generation (20 minutes)

```
1. Open project
2. Select financing scenario
3. View incentives (federal, state, utility, local)
4. Compare options (cash, loan, lease, PPA)
5. See 25-year cash flow with escalation
6. Select preferred option
7. Generate investor/lender proposal
8. Export all documentation
```

---

## Key Features by Page

### 1. Homepage (Public)

- Hero section: "Professional Estimates & Proposals in Minutes"
- Feature highlights
- Pricing plans
- CTA: "Get Started Free" / "Request Demo"
- Login link

### 2. Dashboard (Authenticated)

- Welcome message with quick stats
- Recent projects (cards showing status, budget, deadline)
- Key metrics: Total projects, pending estimates, sent proposals
- Quick action buttons
- Activity timeline

### 3. Projects Page

- Projects list/grid view
- Filters: Status, type, date range
- Search by project name/address
- Create new project button
- Bulk actions (export, delete)
- Project details view

### 4. Estimate Builder

- Step 1: Project details (building type, sqft, location)
- Step 2: Select components
- Step 3: Choose upgrades (optional)
- Step 4: Apply regional factors
- Step 5: Review breakdown
- Step 6: Export (PDF/Excel/CSV)

### 5. Upgrades Browser

- Filterable catalog (by category)
- Upgrade cards (name, cost, annual savings, ROI)
- "Add to Project" button
- Detailed view with specs
- Comparison matrix

### 6. Financial Analysis

- Incentives calculator (federal, state, utility, local)
- Financing comparison (cash vs loan vs lease vs PPA)
- 25-year cash flow chart
- ROI/IRR/NPV calculations
- Export analysis

### 7. Proposals

- Proposal templates (investor, lender, homeowner)
- Customization options
- Preview before send
- Export (PDF, HTML, Excel)
- Email delivery
- Track status (opened, clicked, etc.)

### 8. Team Management

- Team members list
- Invite members
- Role-based permissions (Admin, Manager, Viewer)
- Activity log
- Usage statistics

---

## Data Models

### User
```typescript
{
  id: string
  email: string
  password: hashed
  firstName: string
  lastName: string
  company: string
  role: "admin" | "manager" | "viewer"
  createdAt: date
  updatedAt: date
}
```

### Project
```typescript
{
  id: string
  userId: string
  name: string
  address: string
  city: string
  state: string
  zipCode: string
  buildingType: string
  squareFeet: number
  description?: string
  status: "draft" | "in-progress" | "completed"
  createdAt: date
  updatedAt: date
}
```

### Estimate
```typescript
{
  id: string
  projectId: string
  baselineCost: number
  lineItems: LineItem[]
  upgrades: Upgrade[]
  totalCost: number
  regionalFactor: number
  summary: string
  createdAt: date
  updatedAt: date
}
```

### Proposal
```typescript
{
  id: string
  estimateId: string
  template: "investor" | "lender" | "homeowner"
  title: string
  content: string
  status: "draft" | "sent" | "opened" | "accepted"
  sentAt?: date
  expiresAt?: date
  createdAt: date
  updatedAt: date
}
```

### Upgrade
```typescript
{
  id: string
  name: string
  category: string
  cost: number
  annualSavings: number
  rebates: number
  taxCredits: number
  paybackYears: number
  description: string
  specs: object
}
```

---

## Security & Permissions

### Authentication
- JWT tokens (issued by FastAPI backend)
- Refresh token rotation
- Secure httpOnly cookies

### Authorization
- Role-based access control (RBAC)
- Project-level permissions
- Team member access control
- Audit logging

### Data Protection
- HTTPS only
- SQL injection prevention (via ORM)
- CSRF protection
- XSS prevention (React sanitization)
- Rate limiting on API endpoints

---

## Deployment

### Frontend (Next.js)
- Vercel (recommended) or Docker
- Environment: .env.local
- Build: `npm run build`
- Start: `npm start`

### Backend (FastAPI)
- Docker container
- Environment variables for DB, secrets
- Run: `docker-compose up`

### Database
- PostgreSQL (existing)
- Migrations via Alembic
- Connection pooling

### Storage
- MinIO (existing S3-compatible)
- Document uploads
- PDF generation
- Export files

---

## Development Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | Next.js | 14.2+ |
| UI Framework | React | 18.3+ |
| Styling | Tailwind CSS | 3.4+ |
| UI Components | shadcn/ui + Radix | Latest |
| State Management | Zustand | 4.5+ |
| HTTP Client | Axios | 1.7+ |
| Backend API | FastAPI | 0.104+ |
| Database | PostgreSQL | 13+ |
| Storage | MinIO | Latest |
| Authentication | JWT | - |

---

## Implementation Priority

### Phase 1: Core Platform (Weeks 1-2)
- [ ] Auth pages (login, register)
- [ ] Dashboard
- [ ] Project CRUD
- [ ] Basic estimate builder

### Phase 2: Estimation & Upgrades (Weeks 2-3)
- [ ] Line-item estimation
- [ ] Upgrade browser & selection
- [ ] ROI calculator
- [ ] Export functionality

### Phase 3: Financial Analysis (Week 4)
- [ ] Incentives calculator
- [ ] Financing comparison
- [ ] Cash flow projections
- [ ] Proposal builder

### Phase 4: Document Processing (Week 5)
- [ ] Document uploader
- [ ] AI extraction
- [ ] Auto CRM generation
- [ ] Questionnaire UI

### Phase 5: Team & Admin (Week 6)
- [ ] Team management
- [ ] Role-based access
- [ ] Audit logging
- [ ] Usage analytics

### Phase 6: Polish & Deploy (Week 7)
- [ ] Performance optimization
- [ ] Testing
- [ ] Documentation
- [ ] Deployment setup

---

## Success Metrics

- **Adoption**: 50+ teams using platform within 3 months
- **Speed**: Average time to generate estimate < 5 minutes
- **Conversion**: 85%+ proposal conversion rate
- **Satisfaction**: 4.5+/5 user rating
- **Efficiency**: 10x faster than manual process

