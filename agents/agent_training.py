"""
Eagle Eye MCP Agent Training & Configuration
Trains LLM agents (OpenAI, Ollama, HuggingFace) to operate autonomously in agentic format
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================================
# AGENT CONFIGURATION & SYSTEM PROMPTS
# ============================================================================

SYSTEM_PROMPT_BASE = """You are an AI agent operating the Eagle Eye construction plan review and pricing system.

## Your Role
You are an autonomous agent that:
1. Ingests PDF construction plans
2. Runs code compliance checks against IRC 2018, IECC 2015, NEC 2017, Georgia amendments
3. Generates pricing estimates with regional factors
4. Produces professional proposals

## Key Principles
- Be systematic and thorough in analysis
- Validate all inputs before processing
- Track decisions and reasoning in logs
- Handle errors gracefully with recovery steps
- Always ask for clarification if ambiguous
- Maintain audit trail of all actions

## Available Tools
You have access to MCP tools organized by category:
- CRM: Project management and client tracking
- Ingest: Plan PDF parsing and extraction
- Rules: Code compliance checking
- Pricing: Estimate generation with regional factors
- Reports: Proposal generation and export

## Operating Mode
You operate in AGENTIC format, meaning:
- You execute multi-step workflows autonomously
- You make decisions based on context and rules
- You can chain tool calls to accomplish complex tasks
- You recover from errors and retry operations
- You log all actions for audit compliance

## Response Format
Always respond with:
1. REASONING: Your thought process
2. ACTION: The tool(s) you're calling
3. RESULT: What happened
4. NEXT: What happens next
"""

SYSTEM_PROMPT_COMPLIANCE = """## Specialized: Code Compliance Agent

Your focus is strict adherence to building codes:
- IRC 2018 (International Residential Code)
- IECC 2015 (International Energy Conservation Code)
- NEC 2017 (National Electrical Code)
- Georgia state amendments

Process:
1. Parse plan sections
2. Extract requirements and specs
3. Match against code standards
4. Flag violations with severity
5. Suggest corrections

Return findings as structured violations with:
- Code reference (e.g., IRC 2018 R101.1)
- Violation description
- Severity (critical/major/minor)
- Required correction
"""

SYSTEM_PROMPT_PRICING = """## Specialized: Pricing Agent

Your focus is accurate cost estimation:
- Labor rates by trade
- Material costs and markups
- Regional cost factors (by state/county)
- Specification tier (basic/standard/premium)
- Contingency calculations

Process:
1. Analyze plan scope
2. Calculate material quantities
3. Apply labor rates
4. Add regional factors
5. Include contingency
6. Generate detailed breakdown

Return estimates as:
- Line items with costs
- Subtotals by category
- Regional factor adjustments
- Final price with markup
"""

SYSTEM_PROMPT_PROPOSAL = """## Specialized: Proposal Agent

Your focus is professional client communication:
- Executive summary of findings
- Compliance status and risks
- Cost breakdown and value proposition
- Timeline and deliverables
- Next steps and recommendations

Process:
1. Summarize compliance findings
2. Explain pricing rationale
3. Highlight risks and mitigations
4. Build confidence in recommendations
5. Clear call to action

Generate professional documents that:
- Are client-friendly (non-technical language option)
- Include detailed appendices for specialists
- Have clear decision points
- Specify payment terms and schedule
"""


# ============================================================================
# TOOL SPECIFICATIONS FOR AGENT TRAINING
# ============================================================================

TOOL_SPECS = {
    "crm": [
        {
            "name": "crm.create_project",
            "description": "Create a new project with client and location info",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Project name"},
                    "address": {"type": "object", "description": "Full address"},
                    "client_name": {"type": "string", "description": "Client/owner name"},
                    "spec_tier": {"type": "string", "enum": ["basic", "standard", "premium"]},
                    "jurisdiction": {"type": "string", "description": "State code (GA, CA, TX)"}
                },
                "required": ["name", "address", "client_name"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "status": {"type": "string"},
                    "created_at": {"type": "string"}
                }
            },
            "examples": [
                {
                    "input": {
                        "name": "Atlanta Office Renovation",
                        "address": {"city": "Atlanta", "state": "GA", "zip": "30303"},
                        "client_name": "ABC Corp",
                        "spec_tier": "standard"
                    },
                    "output": {
                        "project_id": "proj_abc123",
                        "status": "created",
                        "created_at": "2024-01-15T10:30:00Z"
                    }
                }
            ]
        },
        {
            "name": "crm.list_projects",
            "description": "List all projects with optional filtering",
            "input_schema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["active", "completed", "archived"]},
                    "limit": {"type": "integer", "description": "Max results"}
                }
            },
            "output_schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "name": {"type": "string"},
                        "status": {"type": "string"},
                        "created_at": {"type": "string"}
                    }
                }
            }
        }
    ],
    "ingest": [
        {
            "name": "ingest.parse",
            "description": "Parse PDF construction plans into structured data",
            "input_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "Project ID"},
                    "file_paths": {"type": "array", "items": {"type": "string"}, "description": "Paths to PDF files"},
                    "extraction_type": {"type": "string", "enum": ["full", "summary", "compliance-only"]}
                },
                "required": ["project_id", "file_paths"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "plan_graph": {"type": "object", "description": "Parsed plan structure"},
                    "pages_processed": {"type": "integer"},
                    "extraction_status": {"type": "string"}
                }
            }
        }
    ],
    "rules": [
        {
            "name": "rules.check_compliance",
            "description": "Run code compliance checks against parsed plan",
            "input_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "plan_graph": {"type": "object"},
                    "code_standards": {"type": "array", "items": {"type": "string"}, "description": ["IRC_2018", "IECC_2015", "NEC_2017", "GA_AMENDMENTS"]},
                    "jurisdiction": {"type": "string"}
                },
                "required": ["project_id", "plan_graph", "code_standards"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "compliance_status": {"type": "string", "enum": ["compliant", "violations_found"]},
                    "violations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "code_reference": {"type": "string"},
                                "violation": {"type": "string"},
                                "severity": {"type": "string", "enum": ["critical", "major", "minor"]},
                                "correction": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    ],
    "pricing": [
        {
            "name": "pricing.estimate",
            "description": "Generate pricing estimate with regional factors",
            "input_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "plan_graph": {"type": "object"},
                    "jurisdiction": {"type": "string", "description": "State code"},
                    "county": {"type": "string", "description": "County for regional factors"},
                    "spec_tier": {"type": "string", "enum": ["basic", "standard", "premium"]},
                    "contingency_pct": {"type": "number", "description": "Contingency percentage", "default": 10}
                },
                "required": ["project_id", "plan_graph", "jurisdiction"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "line_items": {"type": "array"},
                    "subtotal": {"type": "number"},
                    "regional_adjustment": {"type": "number"},
                    "contingency": {"type": "number"},
                    "total": {"type": "number"},
                    "estimate_confidence": {"type": "string", "enum": ["high", "medium", "low"]}
                }
            }
        }
    ],
    "reports": [
        {
            "name": "reports.generate_proposal",
            "description": "Generate professional proposal PDF",
            "input_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "compliance_findings": {"type": "object"},
                    "estimate": {"type": "object"},
                    "template": {"type": "string", "enum": ["comprehensive", "summary", "executive"]},
                    "output_format": {"type": "string", "enum": ["pdf", "html", "csv"]}
                },
                "required": ["project_id", "compliance_findings", "estimate"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "document_url": {"type": "string"},
                    "format": {"type": "string"},
                    "generated_at": {"type": "string"}
                }
            }
        }
    ]
}


# ============================================================================
# AGENT EXECUTION WORKFLOWS
# ============================================================================

WORKFLOW_TEMPLATES = {
    "full_review": {
        "name": "Full Plan Review & Proposal",
        "description": "Complete workflow: ingest → compliance → pricing → proposal",
        "steps": [
            {
                "step": 1,
                "name": "Create Project",
                "tool": "crm.create_project",
                "params": ["name", "address", "client_name", "spec_tier", "jurisdiction"]
            },
            {
                "step": 2,
                "name": "Parse Plans",
                "tool": "ingest.parse",
                "params": ["project_id", "file_paths"],
                "depends_on": [1]
            },
            {
                "step": 3,
                "name": "Check Compliance",
                "tool": "rules.check_compliance",
                "params": ["project_id", "plan_graph", "code_standards", "jurisdiction"],
                "depends_on": [2]
            },
            {
                "step": 4,
                "name": "Generate Estimate",
                "tool": "pricing.estimate",
                "params": ["project_id", "plan_graph", "jurisdiction", "spec_tier"],
                "depends_on": [2]
            },
            {
                "step": 5,
                "name": "Create Proposal",
                "tool": "reports.generate_proposal",
                "params": ["project_id", "compliance_findings", "estimate"],
                "depends_on": [3, 4]
            }
        ]
    },
    "compliance_check": {
        "name": "Compliance Check Only",
        "description": "Quick compliance analysis of parsed plans",
        "steps": [
            {
                "step": 1,
                "name": "Parse Plans",
                "tool": "ingest.parse",
                "params": ["project_id", "file_paths", "extraction_type"],
                "extraction_type": "compliance-only"
            },
            {
                "step": 2,
                "name": "Check Compliance",
                "tool": "rules.check_compliance",
                "params": ["project_id", "plan_graph", "code_standards"],
                "depends_on": [1]
            }
        ]
    },
    "pricing_only": {
        "name": "Pricing Estimate Only",
        "description": "Generate pricing estimate for known scope",
        "steps": [
            {
                "step": 1,
                "name": "Generate Estimate",
                "tool": "pricing.estimate",
                "params": ["project_id", "plan_graph", "jurisdiction", "spec_tier"]
            }
        ]
    }
}


# ============================================================================
# AGENT CONTEXT & EXAMPLES
# ============================================================================

AGENT_EXAMPLES = {
    "compliance_analysis": {
        "scenario": "Analyzing a residential project for code compliance",
        "user_request": "Review this house plan for compliance with Georgia building codes",
        "agent_reasoning": """
1. User provided a house plan PDF
2. Project is in Georgia, so I need to check IRC 2018, IECC 2015, NEC 2017, and GA amendments
3. I should parse the plan first to extract details
4. Then run compliance checks systematically
5. Report violations by severity with corrections needed
        """,
        "agent_actions": [
            {
                "action": "ingest.parse",
                "input": {
                    "project_id": "res_proj_001",
                    "file_paths": ["house_plans.pdf"],
                    "extraction_type": "full"
                }
            },
            {
                "action": "rules.check_compliance",
                "input": {
                    "project_id": "res_proj_001",
                    "plan_graph": "<<parsed_plan_data>>",
                    "code_standards": ["IRC_2018", "IECC_2015", "NEC_2017", "GA_AMENDMENTS"],
                    "jurisdiction": "GA"
                }
            }
        ]
    },
    "pricing_workflow": {
        "scenario": "Generating estimate for construction project",
        "user_request": "What would this office renovation cost in Atlanta with standard spec tier?",
        "agent_reasoning": """
1. User wants pricing for an office renovation in Atlanta
2. Need to use standard spec tier (mid-range)
3. Atlanta is in Fulton County, Georgia
4. I'll apply GA regional cost factor
5. Include 10% contingency for standard tier
        """,
        "agent_actions": [
            {
                "action": "pricing.estimate",
                "input": {
                    "project_id": "comm_proj_002",
                    "plan_graph": "<<parsed_plan_data>>",
                    "jurisdiction": "GA",
                    "county": "Fulton",
                    "spec_tier": "standard",
                    "contingency_pct": 10
                }
            }
        ]
    }
}


# ============================================================================
# AGENT DECISION TREES
# ============================================================================

DECISION_TREES = {
    "project_intake": {
        "question": "What type of project?",
        "options": {
            "residential": {
                "codes": ["IRC_2018", "IECC_2015", "NEC_2017"],
                "default_tier": "standard",
                "next": "location_intake"
            },
            "commercial": {
                "codes": ["IBC_2018", "IECC_2015", "NEC_2017"],
                "default_tier": "standard",
                "next": "location_intake"
            },
            "industrial": {
                "codes": ["IBC_2018", "NEC_2017"],
                "default_tier": "premium",
                "next": "location_intake"
            }
        }
    },
    "location_intake": {
        "question": "What state is the project?",
        "options": {
            "GA": {"code_amendments": ["GA_AMENDMENTS"], "regional_factor": 0.95},
            "CA": {"code_amendments": ["CA_AMENDMENTS"], "regional_factor": 1.15},
            "TX": {"code_amendments": [], "regional_factor": 1.0},
            "NY": {"code_amendments": ["NYC_AMENDMENTS"], "regional_factor": 1.25}
        }
    },
    "spec_tier": {
        "question": "What specification tier?",
        "options": {
            "basic": {"description": "Budget-conscious, meets code minimum", "markup": 1.0},
            "standard": {"description": "Good value, meets code with improvements", "markup": 1.2},
            "premium": {"description": "High-end, exceeds code, best practices", "markup": 1.5}
        }
    }
}


def format_tool_spec_for_agent(tool_spec: Dict[str, Any], provider: str = "openai") -> Dict[str, Any]:
    """
    Format tool specification for different LLM providers
    
    Args:
        tool_spec: Raw tool specification
        provider: 'openai', 'ollama', or 'huggingface'
    
    Returns:
        Provider-specific formatted tool spec
    """
    if provider == "openai":
        # OpenAI function_tools format
        return {
            "type": "function",
            "function": {
                "name": tool_spec["name"],
                "description": tool_spec["description"],
                "parameters": tool_spec["input_schema"]
            }
        }
    elif provider == "ollama":
        # Ollama format (simpler, similar to OpenAI but without type wrapper)
        return {
            "name": tool_spec["name"],
            "description": tool_spec["description"],
            "parameters": tool_spec["input_schema"]
        }
    elif provider == "huggingface":
        # HuggingFace format (JSON schema string)
        return {
            "name": tool_spec["name"],
            "description": tool_spec["description"],
            "schema": json.dumps(tool_spec["input_schema"])
        }
    else:
        return tool_spec


if __name__ == "__main__":
    import json
    
    print("=" * 80)
    print("EAGLE EYE AGENT TRAINING FRAMEWORK")
    print("=" * 80)
    print()
    
    print("📋 System Prompt (Base)")
    print("-" * 80)
    print(SYSTEM_PROMPT_BASE[:300] + "...\n")
    
    print("🔧 Available Tools by Category")
    print("-" * 80)
    for category, tools in TOOL_SPECS.items():
        print(f"\n  {category.upper()}: {len(tools)} tools")
        for tool in tools:
            print(f"    - {tool['name']}: {tool['description']}")
    
    print("\n📊 Workflow Templates")
    print("-" * 80)
    for workflow_name, workflow in WORKFLOW_TEMPLATES.items():
        print(f"\n  {workflow['name']} ({workflow_name})")
        print(f"    Steps: {len(workflow['steps'])}")
    
    print("\n✅ Configuration ready for agent training!")
    print("=" * 80)
