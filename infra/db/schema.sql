-- Eagle Eye Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Accounts (CRM)
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT, -- Owner, GC, Lender, Partner
    contact_email TEXT,
    contact_phone TEXT,
    billing_address JSONB,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Contacts
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    first_name TEXT,
    last_name TEXT,
    role TEXT, -- PM, PE, Estimator, Owner, etc.
    email TEXT,
    phone TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Opportunities
CREATE TABLE opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    stage TEXT DEFAULT 'Lead', -- Lead, Qualified, Proposal, Won, Lost
    value NUMERIC(12, 2),
    probability INTEGER, -- 0-100
    close_date DATE,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Addresses
CREATE TABLE addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    line1 TEXT NOT NULL,
    line2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    county TEXT,
    lat NUMERIC(10, 7),
    lon NUMERIC(10, 7),
    cbsa_code TEXT, -- For demographic pricing
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Jurisdictions
CREATE TABLE jurisdictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    city TEXT,
    county TEXT,
    state TEXT NOT NULL,
    code_set TEXT NOT NULL, -- IRC2018_IECC2015_NEC2017_GA
    amendments_jsonb JSONB, -- GA-specific overlays, local ordinances
    climate_zone TEXT, -- IECC Zone 3, 4, etc.
    wind_speed INTEGER, -- mph ultimate
    seismic_category TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE SET NULL,
    opportunity_id UUID REFERENCES opportunities(id) ON DELETE SET NULL,
    address_id UUID REFERENCES addresses(id) ON DELETE SET NULL,
    jurisdiction_id UUID REFERENCES jurisdictions(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    scope TEXT,
    spec_tier TEXT, -- Standard, Premium, Luxury
    roof_option TEXT, -- Shingle, Standing-Seam, Tile
    window_tier TEXT, -- Standard, Energy-Star, Premium
    energy_path TEXT, -- Prescriptive, Performance, Sealed-Attic
    status TEXT DEFAULT 'draft', -- draft, parsing, reviewing, pricing, complete
    living_sf NUMERIC(10, 2),
    total_sf NUMERIC(10, 2),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Files (Plans, Photos, Documents)
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    mime TEXT,
    s3_key TEXT NOT NULL,
    sha256 TEXT,
    kind TEXT,
    size_bytes BIGINT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Findings (Code Compliance Issues)
CREATE TABLE findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    finding_code TEXT, -- RR-101, RR-102, etc.
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    severity TEXT NOT NULL, -- Red, Orange, Yellow
    discipline TEXT, -- Structural, Envelope, MEP, Civil
    location TEXT, -- Sheet ref: A1.04 / Detail 3
    code_citation TEXT, -- IRC 2018 R602.10
    consequence TEXT, -- "Shear failure/rework"
    fix TEXT, -- "Provide BWLs, HD schedule"
    ve_alt TEXT, -- "Portal frame at openings"
    evidence_refs TEXT[], -- Array of sheet/detail refs
    submittal_needed TEXT, -- "BCI calc pack", "Stamped truss set"
    status TEXT DEFAULT 'open', -- open, acknowledged, resolved, wont-fix
    resolved_by TEXT,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Estimates (Pricing)
CREATE TABLE estimates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    base JSONB,
    alternates JSONB,
    allowances JSONB,
    summary JSONB,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by TEXT
);

-- Pricing Catalog (TradeBase)
CREATE TABLE pricing_catalog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT,
    trade TEXT NOT NULL,
    item TEXT NOT NULL,
    uom TEXT NOT NULL,
    unit_cost NUMERIC(10, 2) NOT NULL,
    region TEXT,
    effective_dt DATE,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Regional Factors (zip/CBSA-level)
CREATE TABLE regional_factors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region TEXT NOT NULL, -- "Atlanta_GA", "Cobb_County_GA", "30301"
    region_type TEXT, -- zip, county, cbsa, city
    labor_idx NUMERIC(5, 3) DEFAULT 1.0,
    material_idx NUMERIC(5, 3) DEFAULT 1.0,
    delivery_idx NUMERIC(5, 3) DEFAULT 1.0,
    demo_idx NUMERIC(5, 3) DEFAULT 1.0,
    permit_idx NUMERIC(5, 3) DEFAULT 1.0,
    finish_profile TEXT, -- "Brookhaven_Luxury", "Cobb_Mid"
    effective_dt DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(region, effective_dt)
);

-- Spec Tier Bundles
CREATE TABLE spec_tier_bundles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tier TEXT NOT NULL, -- Standard, Premium, Luxury
    component TEXT NOT NULL, -- Window, Roof, Cabinet, Flooring
    default_item TEXT, -- "Vinyl Double-Hung", "Standing Seam", etc.
    unit_cost_multiplier NUMERIC(5, 3) DEFAULT 1.0,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Submittals
CREATE TABLE submittals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL, -- "BCI Calc Pack", "Stamped Truss Set"
    category TEXT, -- Structural, MEP, Envelope
    status TEXT DEFAULT 'needed', -- needed, submitted, approved, rejected
    due_date DATE,
    submitted_date DATE,
    approved_date DATE,
    file_id UUID REFERENCES files(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Draws
CREATE TABLE draws (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    draw_number INTEGER NOT NULL,
    name TEXT NOT NULL, -- "Contract Signing & Permits", "Foundation Complete"
    amount NUMERIC(12, 2) NOT NULL,
    percentage NUMERIC(5, 2), -- % of total
    stage TEXT, -- permit, foundation, framing, drywall, final
    status TEXT DEFAULT 'pending', -- pending, requested, approved, paid
    due_date DATE,
    paid_date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Plan Graph (Versioned parsing results)
CREATE TABLE plan_graphs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    graph_data JSONB NOT NULL,
    files_hash TEXT,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit Log
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    action TEXT NOT NULL,
    user_id TEXT,
    changes JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_contacts_account ON contacts(account_id);
CREATE INDEX idx_opportunities_account ON opportunities(account_id);
CREATE INDEX idx_opportunities_stage ON opportunities(stage);
CREATE INDEX idx_addresses_zip ON addresses(zip_code);
CREATE INDEX idx_addresses_county ON addresses(county);
CREATE INDEX idx_jurisdictions_state ON jurisdictions(state);
CREATE INDEX idx_projects_account ON projects(account_id);
CREATE INDEX idx_projects_address ON projects(address_id);
CREATE INDEX idx_projects_jurisdiction ON projects(jurisdiction_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_files_project ON files(project_id);
CREATE INDEX idx_findings_project ON findings(project_id);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_findings_status ON findings(status);
CREATE INDEX idx_estimates_project ON estimates(project_id);
CREATE INDEX idx_pricing_catalog_trade ON pricing_catalog(trade);
CREATE INDEX idx_pricing_catalog_region ON pricing_catalog(region);
CREATE INDEX idx_regional_factors_region ON regional_factors(region);
CREATE INDEX idx_plan_graphs_project ON plan_graphs(project_id);
CREATE INDEX idx_submittals_project ON submittals(project_id);
CREATE INDEX idx_submittals_status ON submittals(status);
CREATE INDEX idx_draws_project ON draws(project_id);
CREATE INDEX idx_draws_status ON draws(status);
CREATE INDEX idx_audit_log_entity ON audit_log(entity_type, entity_id);

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_accounts_updated_at BEFORE UPDATE ON accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_findings_updated_at BEFORE UPDATE ON findings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_submittals_updated_at BEFORE UPDATE ON submittals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_draws_updated_at BEFORE UPDATE ON draws
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
