// Core Type Definitions for Eagle Eye Web Platform

// User & Auth
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  company: string;
  role: "admin" | "manager" | "viewer";
  createdAt: string;
  updatedAt: string;
}

export interface AuthToken {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

// Project
export type BuildingType = 
  | "residential"
  | "commercial"
  | "industrial"
  | "healthcare"
  | "education"
  | "hospitality"
  | "mixed-use"
  | "other";

export type ProjectStatus = "draft" | "in-progress" | "completed" | "archived";

export interface Project {
  id: string;
  userId: string;
  name: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  buildingType: BuildingType;
  squareFeet: number;
  description?: string;
  status: ProjectStatus;
  createdAt: string;
  updatedAt: string;
}

// Line Item
export interface LineItem {
  id: string;
  category: string;
  name: string;
  quantity: number;
  unit: string;
  unitCost: number;
  totalCost: number;
  notes?: string;
}

// Estimate
export interface Estimate {
  id: string;
  projectId: string;
  baselineCost: number;
  lineItems: LineItem[];
  upgrades: SelectedUpgrade[];
  totalCost: number;
  regionalFactor: number;
  taxLabor: number;
  contingency: number;
  summary: string;
  createdAt: string;
  updatedAt: string;
}

// Upgrade
export type UpgradeCategory =
  | "energy-efficiency"
  | "renewable-energy"
  | "water-conservation"
  | "waste-management"
  | "leed-certification"
  | "esg-programs";

export interface Upgrade {
  id: string;
  name: string;
  category: UpgradeCategory;
  cost: number;
  annualSavings: number;
  rebates: number;
  taxCredits: number;
  paybackYears: number;
  description: string;
  specs: Record<string, string | number>;
  certifications?: string[];
}

export interface SelectedUpgrade extends Upgrade {
  quantity: number;
  totalCost: number;
}

// Incentive
export interface Incentive {
  id: string;
  name: string;
  type: "federal" | "state" | "utility" | "local";
  amount: number;
  percentage?: number;
  description: string;
  eligibility: string;
  deadline?: string;
}

// Financing Option
export type FinancingType = "cash" | "loan" | "lease" | "ppa";

export interface FinancingOption {
  id: string;
  type: FinancingType;
  name: string;
  downPayment: number;
  interestRate?: number;
  term: number; // months
  monthlyPayment?: number;
  totalCost: number;
  notes?: string;
}

// Financial Analysis
export interface FinancialAnalysis {
  projectCost: number;
  availableIncentives: Incentive[];
  costAfterIncentives: number;
  financingOptions: FinancingOption[];
  selectedFinancing?: FinancingOption;
  annualSavings: number;
  paybackPeriod: number;
  roi25Year: number;
  irr: number;
  npv: number;
}

// Proposal
export type ProposalTemplate = "investor" | "lender" | "homeowner";
export type ProposalStatus = "draft" | "sent" | "opened" | "accepted" | "declined";

export interface ProposalSection {
  id: string;
  title: string;
  content: string;
  order: number;
}

export interface Proposal {
  id: string;
  estimateId: string;
  projectId: string;
  template: ProposalTemplate;
  title: string;
  sections: ProposalSection[];
  status: ProposalStatus;
  sentAt?: string;
  expiresAt?: string;
  openedAt?: string;
  createdAt: string;
  updatedAt: string;
}

// Document
export type DocumentType = "pdf" | "excel" | "word" | "image" | "other";

export interface Document {
  id: string;
  projectId: string;
  fileName: string;
  type: DocumentType;
  size: number; // bytes
  url: string;
  extractedData?: Record<string, any>;
  status: "uploaded" | "processing" | "extracted" | "failed";
  uploadedAt: string;
}

// Team Member
export type TeamRole = "admin" | "manager" | "viewer";

export interface TeamMember {
  id: string;
  userId: string;
  companyId: string;
  email: string;
  firstName: string;
  lastName: string;
  role: TeamRole;
  invitedAt: string;
  joinedAt?: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface ApiPaginatedResponse<T> {
  success: boolean;
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Form Data
export interface ProjectFormData {
  name: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  buildingType: BuildingType;
  squareFeet: number;
  description?: string;
}

export interface EstimateFormData {
  projectId: string;
  lineItems: LineItem[];
  upgrades: SelectedUpgrade[];
}

export interface ProposalFormData {
  estimateId: string;
  template: ProposalTemplate;
  title: string;
  sections: ProposalSection[];
  customizations?: Record<string, any>;
}

// Dashboard Stats
export interface DashboardStats {
  totalProjects: number;
  pendingEstimates: number;
  sentProposals: number;
  acceptedProposals: number;
  totalRevenue: number;
  recentProjects: Project[];
}
