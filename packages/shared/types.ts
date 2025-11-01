/**
 * Shared types for TypeScript (frontend and other TS services)
 */

export type Severity = 'Red' | 'Orange' | 'Yellow';
export type FindingStatus = 'open' | 'acknowledged' | 'resolved' | 'wont-fix';
export type ProjectStatus = 'draft' | 'parsing' | 'reviewing' | 'pricing' | 'complete';
export type SpecTier = 'Standard' | 'Premium' | 'Luxury';
export type Confidence = 'High' | 'Medium' | 'Low';

export interface Finding {
  id?: string;
  project_id?: string;
  severity: Severity;
  discipline: string;
  location: string;
  code_citation: string;
  impact: string;
  recommendation: string;
  ve_alt?: string;
  evidence?: Record<string, any>;
  status: FindingStatus;
  created_at?: string;
  updated_at?: string;
}

export interface LineItem {
  wbs: string;
  assembly: string;
  line_item: string;
  uom: string;
  qty: number;
  unit_cost: number;
  ext_cost: number;
  notes?: string;
  alt_group?: string;
  trade?: string;
  confidence?: Confidence;
}

export interface EstimateSummary {
  subtotal: number;
  overhead_pct: number;
  profit_pct: number;
  overhead_amt: number;
  profit_amt: number;
  total: number;
  contingency_pct: number;
  contingency_amt: number;
  grand_total: number;
}

export interface Estimate {
  id?: string;
  project_id?: string;
  base: Record<string, LineItem[]>;
  alternates: Record<string, LineItem[]>;
  allowances: Record<string, number>;
  summary?: EstimateSummary;
  version: number;
  created_at?: string;
  created_by?: string;
}

export interface ProjectAddress {
  street: string;
  city: string;
  state: string;
  zip_code: string;
  county?: string;
}

export interface Jurisdiction {
  state: string;
  county?: string;
  municipality?: string;
  code_set: string;
}

export interface Project {
  id?: string;
  account_id?: string;
  name: string;
  address_json?: Record<string, any>;
  jurisdiction?: Jurisdiction;
  scope?: string;
  spec_tier?: SpecTier;
  status: ProjectStatus;
  metadata?: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

export interface FileUpload {
  id?: string;
  project_id?: string;
  name: string;
  mime?: string;
  s3_key: string;
  sha256?: string;
  kind?: string;
  size_bytes?: number;
  metadata?: Record<string, any>;
  created_at?: string;
}

export interface PlanGraph {
  sheets: Array<Record<string, any>>;
  schedules: Record<string, Array<Record<string, any>>>;
  quantities: Record<string, any>;
  metadata: Record<string, any>;
}

export interface RegionalFactor {
  id?: string;
  region: string;
  labor_idx: number;
  material_idx: number;
  demo_idx: number;
  permit_idx: number;
  effective_dt?: string;
}
