# Eagle Eye Agent Training & Agentic Format Guide

## Overview

This guide explains how to train and deploy LLM agents (OpenAI, Ollama, HuggingFace) to operate Eagle Eye autonomously in **agentic format** - where agents execute multi-step workflows without human intervention.

## What is "Agentic Format"?

Agentic format means:
- **Autonomous execution**: Agent decides what to do without user guidance
- **Tool calling**: Agent calls MCP tools to accomplish goals
- **Multi-step workflows**: Chains actions to solve complex problems
- **Error recovery**: Handles failures and retries intelligently
- **Audit trail**: Logs all decisions and actions for compliance

## System Architecture

```
User Request
    ↓
┌─────────────────────────┐
│  EagleEyeAgent Executor │
│  (Orchestrator, Role)   │
└────────┬────────────────┘
         ↓
    ┌────────────────────────────┐
    │  LLM Provider Selection    │
    │  (OpenAI/Ollama/HuggingFace)
    └────┬───────────────────────┘
         ↓
    ┌────────────────────────────┐
    │  System Prompt             │
    │  + Tool Specifications     │
    │  + Conversation History    │
    └────┬───────────────────────┘
         ↓
    ┌────────────────────────────┐
    │  LLM Inference             │
    │  (Generate next action)    │
    └────┬───────────────────────┘
         ↓
    ┌────────────────────────────┐
    │  Tool Call Execution       │
    │  (MCP Server)              │
    └────┬───────────────────────┘
         ↓
    ┌────────────────────────────┐
    │  Memory & Decision Log     │
    │  (Audit Trail)             │
    └────┬───────────────────────┘
         ↓
    Output & Report
```

## Training the Agents

### Step 1: Configure LLM Providers

All three providers are already configured in your `.env.local`:

```bash
# OpenAI (Cloud)
OPENAI_API_KEY=sk-proj-test123456789
OPENAI_MODEL=gpt-4-turbo-preview

# Ollama (Local)
OLLAMA_ENABLED=true
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# Hugging Face (Cloud)
HUGGINGFACE_API_KEY=hf_YOUR_TOKEN_HERE
HUGGINGFACE_MODEL=meta-llama/Llama-2-7b-chat-hf
```

### Step 2: Create Agents with Specialized Roles

```python
from agents.agent_executor import EagleEyeAgent, AgentRole

# Orchestrator Agent - Coordinates entire workflow
orchestrator = EagleEyeAgent(
    role=AgentRole.ORCHESTRATOR,  # Sees all tools
    llm_provider="openai"         # Use GPT-4 for complex decisions
)

# Compliance Agent - Focuses on code checking
compliance = EagleEyeAgent(
    role=AgentRole.COMPLIANCE,
    llm_provider="ollama"         # Use local LLM for consistent behavior
)

# Pricing Agent - Focuses on cost estimation
pricing = EagleEyeAgent(
    role=AgentRole.PRICING,
    llm_provider="huggingface"    # Use specialized model
)

# Proposal Agent - Focuses on client communication
proposal = EagleEyeAgent(
    role=AgentRole.PROPOSAL,
    llm_provider="openai"         # Use GPT-4 for writing quality
)
```

### Step 3: System Prompts

Each agent gets a **specialized system prompt** that trains it for its role:

**Orchestrator (Coordinates entire workflow)**
```
You are an autonomous agent that orchestrates the Eagle Eye system.
Your role is to:
1. Intake project information from clients
2. Coordinate multi-step workflows
3. Make decisions about next steps
4. Handle errors and retries
5. Produce final deliverables
```

**Compliance Agent (Code checking specialist)**
```
Your focus is strict adherence to building codes:
- IRC 2018 (International Residential Code)
- IECC 2015 (International Energy Conservation Code)
- NEC 2017 (National Electrical Code)
- Georgia state amendments

Process violations with severity levels:
- CRITICAL: Life/safety issues, must fix
- MAJOR: Code violations, must fix
- MINOR: Best practices, should fix
```

**Pricing Agent (Cost estimation specialist)**
```
Your focus is accurate cost estimation:
- Extract material quantities from plans
- Apply labor rates by trade
- Add regional cost factors
- Calculate contingencies
- Generate detailed line-item estimates

Be conservative - underestimate and surprise clients positively.
```

**Proposal Agent (Client communication specialist)**
```
Your focus is professional client communication:
- Explain findings in non-technical language
- Highlight risks and mitigations
- Build confidence in recommendations
- Clear call-to-action
- Professional formatting

Make proposals that inspire confidence and action.
```

## Tool Specifications

Agents are given complete specifications for all available MCP tools:

### CRM Tools
```
crm.create_project     - Create new project with client info
crm.list_projects      - List projects with filtering
crm.update_project     - Update project status/info
crm.get_project        - Fetch project details
```

### Ingest Tools
```
ingest.parse           - Parse PDF plans into structured data
ingest.extract_areas   - Extract room/space dimensions
ingest.extract_layers  - Extract electrical/plumbing layers
```

### Rules Tools
```
rules.check_compliance - Run code compliance checks
rules.get_violations   - Get violation details
rules.get_corrections  - Get suggested corrections
```

### Pricing Tools
```
pricing.estimate       - Generate cost estimate
pricing.get_rates      - Get labor rates by trade
pricing.get_factors    - Get regional cost factors
pricing.calculate_loi  - Calculate line-of-item costs
```

### Reports Tools
```
reports.generate_proposal    - Generate proposal PDF
reports.generate_summary     - Generate executive summary
reports.generate_compliance  - Generate compliance report
reports.export_csv           - Export data as CSV
```

## Workflow Templates

Pre-built workflows that agents follow:

### Full Review Workflow
```
1. Create Project
   └─ Input: name, address, client, spec tier
   
2. Parse Plans
   └─ Input: project_id, file_paths
   └─ Output: plan_graph
   
3. Check Compliance
   └─ Input: project_id, plan_graph, codes
   └─ Output: violations, status
   
4. Generate Estimate
   └─ Input: project_id, plan_graph, jurisdiction
   └─ Output: line_items, total_cost
   
5. Create Proposal
   └─ Input: project_id, findings, estimate
   └─ Output: proposal.pdf
```

### Compliance-Only Workflow
```
1. Parse Plans (compliance-only mode)
2. Check Compliance
3. Report Violations
```

### Pricing-Only Workflow
```
1. Generate Estimate
2. Output cost breakdown
```

## Decision Trees

Agents use **decision trees** to guide their reasoning:

### Project Type Decision
```
Q: What type of project?
├─ Residential → IRC, IECC, NEC + residential amendments
├─ Commercial → IBC, IECC, NEC + commercial amendments
└─ Industrial → IBC, NEC + industrial amendments
```

### Location Decision
```
Q: What state?
├─ GA (Georgia)     → GA_AMENDMENTS, factor=0.95
├─ CA (California)  → CA_AMENDMENTS, factor=1.15
├─ TX (Texas)       → factor=1.0
└─ NY (New York)    → NYC_AMENDMENTS, factor=1.25
```

### Spec Tier Decision
```
Q: What specification level?
├─ Basic     → Meets code minimum, markup=1.0x
├─ Standard  → Good value, code+improvements, markup=1.2x
└─ Premium   → Exceeds code, best practices, markup=1.5x
```

## Agent Memory & State Management

Each agent maintains **persistent memory**:

```python
# Access agent memory
agent.memory.conversation_history    # All turns with LLM
agent.memory.decision_log            # Decisions made
agent.memory.tool_call_log           # Tools called & results
agent.memory.error_log               # Errors & recovery
agent.memory.project_context         # Current project data

# Save to disk for audit trail
agent.memory.save(output_dir=".agent_memory")

# Load from disk to resume
memory = AgentMemory.load("path/to/agent.json")
agent.memory = memory
```

## Example: Full Workflow Execution

### User Input
```
"Please review this house plan for compliance and give me a quote"
```

### Agent Reasoning (Internal)
```
1. User wants a house plan reviewed
2. Need compliance analysis + pricing
3. Should create project first
4. Then parse plan
5. Check IRC/IECC/NEC codes
6. Generate estimate
7. Create proposal
8. Summarize findings for client
```

### Agent Actions (Tool Calls)

```python
# Step 1: Create Project
crm.create_project({
    "name": "House Plan Review",
    "address": {...},
    "client_name": "John Doe",
    "spec_tier": "standard"
})
# Returns: project_id = "proj_123"

# Step 2: Parse Plan
ingest.parse({
    "project_id": "proj_123",
    "file_paths": ["house_plan.pdf"]
})
# Returns: plan_graph = {...}

# Step 3: Check Compliance
rules.check_compliance({
    "project_id": "proj_123",
    "plan_graph": plan_graph,
    "code_standards": ["IRC_2018", "IECC_2015", "NEC_2017"],
    "jurisdiction": "GA"
})
# Returns: violations = [...]

# Step 4: Generate Estimate
pricing.estimate({
    "project_id": "proj_123",
    "plan_graph": plan_graph,
    "jurisdiction": "GA",
    "spec_tier": "standard"
})
# Returns: estimate = {...}

# Step 5: Create Proposal
reports.generate_proposal({
    "project_id": "proj_123",
    "compliance_findings": violations,
    "estimate": estimate
})
# Returns: document_url = "s3://..."
```

## Ease of Use: Key Features

### 1. **One-Line Agent Creation**
```python
agent = EagleEyeAgent(role=AgentRole.COMPLIANCE, llm_provider="openai")
```

### 2. **Automatic Tool Discovery**
Agent automatically gets all available MCP tools.

### 3. **Intelligent Defaults**
- Selects appropriate codes based on location
- Applies regional cost factors automatically
- Chooses sensible defaults for missing parameters

### 4. **Error Recovery**
- Logs all errors for audit
- Attempts recovery automatically
- Falls back to alternative approaches if needed

### 5. **Human-Readable Output**
- Explains decisions in plain language
- Suggests next steps clearly
- Professional proposal generation

### 6. **Audit Trail**
Every action logged with:
- Timestamp
- Tool called
- Parameters used
- Result
- Duration

## Getting Started

### 1. Install Dependencies
```bash
pip install aiohttp pydantic openai
```

### 2. Create an Agent
```python
from agents.agent_executor import EagleEyeAgent, AgentRole

agent = EagleEyeAgent(
    role=AgentRole.ORCHESTRATOR,
    llm_provider="openai"
)
```

### 3. Execute a Workflow
```python
result = await agent.execute_workflow(
    workflow_name="full_review",
    workflow_params={
        "project_name": "Atlanta Office",
        "file_paths": ["plans.pdf"],
        "client_name": "ABC Corp"
    }
)
```

### 4. Review Results & Audit Trail
```python
report = agent.get_execution_report()
print(f"Status: {report['execution_state']}")
print(f"Tool calls: {report['tool_calls']}")
print(f"Errors: {report['errors']}")
agent.memory.save()  # Save for audit
```

## Best Practices

1. **Start with Orchestrator Agent** - Coordinates everything
2. **Use Specialized Agents for Complex Tasks** - Compliance specialist for code, Pricing specialist for costs
3. **Monitor Error Logs** - Check for patterns that need fixing
4. **Save Memory Regularly** - Audit trail is critical
5. **Test with Small Projects First** - Build confidence before scaling
6. **Review Tool Outputs** - Don't blindly trust agent decisions
7. **Use Decision Trees** - Let agent know the business rules

## Troubleshooting

### Agent Isn't Calling Tools
- Check system prompt is set correctly
- Verify tool specifications are provided
- Check agent has role-appropriate tools

### Tool Calls Failing
- Verify MCP server is running
- Check tool parameters are correct
- Review error log for details

### Poor Decision Making
- Provide clearer system prompt
- Add more context to request
- Use specialized agent for that task

### LLM Not Responding
- Check API key is valid
- Verify LLM service is running
- Check network connectivity

## Next Steps

1. ✅ Agents configured with all 3 LLM providers
2. ✅ System prompts for each specialization
3. ✅ Tool specifications ready
4. ✅ Memory & audit trail system
5. ⏳ Deploy and test with real projects
6. ⏳ Monitor performance and refine prompts
7. ⏳ Build specialized agents for complex tasks
8. ⏳ Create team dashboards for oversight
