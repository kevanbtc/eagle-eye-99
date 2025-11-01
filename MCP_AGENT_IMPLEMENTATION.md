# MCP Agent Implementation Guide

## Quick Start: Train & Deploy Agents in 5 Steps

### Step 1: Create Agents (Python)

```python
from agents.agent_executor import EagleEyeAgent, AgentRole

# Create agents for different specializations
orchestrator = EagleEyeAgent(
    role=AgentRole.ORCHESTRATOR,    # Coordinates all workflows
    llm_provider="openai"            # Cloud GPT-4 for complex decisions
)

compliance = EagleEyeAgent(
    role=AgentRole.COMPLIANCE,       # Focuses on code checking
    llm_provider="ollama"            # Local LLM for consistency
)

pricing = EagleEyeAgent(
    role=AgentRole.PRICING,          # Focuses on cost estimation
    llm_provider="huggingface"       # Specialized model
)

proposal = EagleEyeAgent(
    role=AgentRole.PROPOSAL,         # Focuses on client communication
    llm_provider="openai"            # GPT-4 for writing quality
)
```

### Step 2: Register MCP Tools

```python
# Define tool handlers (connect to MCP server)
def create_project_handler(params):
    # Call MCP server
    response = mcp_client.call("crm.create_project", params)
    return response

def parse_plans_handler(params):
    # Call MCP server
    response = mcp_client.call("ingest.parse", params)
    return response

# Register tools with agents
orchestrator.register_tool("crm.create_project", create_project_handler)
orchestrator.register_tool("ingest.parse", parse_plans_handler)
# ... register other tools
```

### Step 3: Execute Workflows

```python
# Execute full review workflow
result = await orchestrator.execute_workflow(
    workflow_name="full_review",
    workflow_params={
        "project_name": "Atlanta Office Renovation",
        "client_name": "ABC Corporation",
        "address": {
            "street": "123 Main St",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30303"
        },
        "file_paths": ["plans.pdf"],
        "spec_tier": "standard"
    }
)
```

### Step 4: Monitor Execution

```python
# Check agent memory and decision log
print(orchestrator.memory.execution_state)
for decision in orchestrator.memory.decision_log:
    print(f"Decision: {decision['decision']}")
    print(f"Reasoning: {decision['reasoning']}")
    print(f"Outcome: {decision['outcome']}")
```

### Step 5: Save & Review Audit Trail

```python
# Save agent memory to disk (for compliance)
filepath = orchestrator.memory.save(output_dir=".agent_memory")
print(f"Audit trail saved to: {filepath}")

# Generate execution report
report = orchestrator.get_execution_report()
print(f"Total tool calls: {report['tool_calls']}")
print(f"Total errors: {report['errors']}")
print(f"Status: {report['execution_state']}")
```

---

## MCP Integration Points

### What is MCP?

MCP (Model Context Protocol) is a standardized interface for:
- **Discoverable tools**: LLM agents find available operations
- **Safe execution**: Sandboxed tool invocation
- **Structured I/O**: JSON schemas for inputs/outputs
- **Error handling**: Graceful failure recovery

### Agent ↔ MCP Server Communication

```
┌──────────────────────┐
│   LLM Agent          │
│  (OpenAI/Ollama/HF)  │
└─────────┬────────────┘
          │ calls tools with JSON params
          ↓
┌──────────────────────┐
│   MCP Router         │
│  (Tool dispatcher)   │
└─────────┬────────────┘
          │ routes to appropriate service
          ↓
┌───────────────────────┐
│   Backend Services    │
├───────────────────────┤
│ - CRM/API service     │
│ - Parser service      │
│ - Rules engine        │
│ - Pricing engine      │
│ - Report generator    │
└───────────────────────┘
```

### Tool Categories & Operations

**CRM Tools** (Client & Project Management)
```
crm.create_project     → Creates new project in system
crm.list_projects      → Lists all projects with filtering
crm.update_project     → Updates project metadata
crm.get_project        → Retrieves full project details
crm.assign_agent       → Assigns agent to project
crm.update_status      → Updates project workflow status
```

**Ingest Tools** (Plan Parsing & Extraction)
```
ingest.parse           → Parse PDF into structured plan_graph
ingest.extract_areas   → Extract room/space dimensions
ingest.extract_layers  → Extract electrical/plumbing layers
ingest.get_markup      → Get markup/annotations from plans
ingest.validate        → Validate extracted data completeness
```

**Rules Tools** (Code Compliance Checking)
```
rules.check_compliance → Run compliance checks against codes
rules.get_violations   → Get detailed violation information
rules.get_corrections  → Get suggested corrections
rules.get_codes        → Get applicable codes for jurisdiction
rules.validate_scope   → Validate project scope against codes
```

**Pricing Tools** (Cost Estimation)
```
pricing.estimate       → Generate complete cost estimate
pricing.get_rates      → Get labor rates by trade
pricing.get_factors    → Get regional cost adjustment factors
pricing.calculate_loi  → Calculate line-of-item cost breakdown
pricing.get_contingency → Calculate contingency amount
```

**Reports Tools** (Document Generation)
```
reports.generate_proposal    → Generate proposal PDF/HTML
reports.generate_compliance  → Generate compliance report
reports.generate_summary     → Generate executive summary
reports.export_csv           → Export data as CSV
reports.send_proposal        → Send proposal to client
```

---

## Agentic Format: The Key Concepts

### 1. **Autonomous Decision Making**

Agent doesn't ask "what should I do?" — it decides based on rules:

```
User: "Review this house plan for compliance and quote me"

Agent reasoning:
  IF project_type == "residential" 
    THEN codes = ["IRC_2018", "IECC_2015", "NEC_2017"]
  
  IF jurisdiction == "GA" 
    THEN codes += ["GA_AMENDMENTS"]
    THEN cost_factor = 0.95
  
  WORKFLOW = ["create_project", "parse_plans", "check_compliance", 
              "estimate_cost", "generate_proposal"]
  
  EXECUTE(WORKFLOW)
```

### 2. **Tool Chaining**

Agent chains multiple tool calls to solve complex problems:

```
Step 1: Create project
  → Returns: project_id

Step 2: Parse plans (depends on Step 1)
  Input: project_id
  → Returns: plan_graph

Step 3: Check compliance (depends on Step 2)
  Input: project_id, plan_graph
  → Returns: violations

Step 4: Generate estimate (depends on Step 2)
  Input: project_id, plan_graph
  → Returns: estimate

Step 5: Create proposal (depends on Steps 3 & 4)
  Input: project_id, violations, estimate
  → Returns: proposal_url
```

### 3. **Error Recovery**

Agent handles failures gracefully:

```python
# If PDF parsing fails
try:
    result = mcp.call("ingest.parse", {"file_paths": ["bad.pdf"]})
except ParsingError as e:
    # Log error
    agent.memory.log_error("parse_error", str(e))
    
    # Try recovery
    recovery_action = "split_pdf_into_pages_and_retry"
    
    # Retry
    for page in split_pages(file_path):
        result = mcp.call("ingest.parse", {"file_paths": [page]})
```

### 4. **Contextual Awareness**

Agent maintains context across multi-turn conversations:

```python
# Agent remembers previous decisions
agent.memory.project_context = {
    "project_id": "proj_123",
    "jurisdiction": "GA",
    "spec_tier": "standard",
    "codes": ["IRC_2018", "IECC_2015", "NEC_2017", "GA_AMENDMENTS"],
    "findings": [...],
    "estimate": {...}
}

# Uses context for follow-up requests
User: "Can you increase the estimate by 15%?"
Agent: "Based on current estimate of $250,000, new total is $287,500"
```

### 5. **Audit Trail & Compliance**

Every action is logged for compliance:

```python
# All decisions logged
{
    "timestamp": "2024-01-15T10:30:00Z",
    "decision": "Apply GA_AMENDMENTS",
    "reasoning": "Project in Georgia jurisdiction",
    "outcome": "Added GA amendments to code standards"
}

# All tool calls logged
{
    "timestamp": "2024-01-15T10:30:05Z",
    "tool": "rules.check_compliance",
    "input": {...},
    "result": {"violations": [...]},
    "duration_ms": 234
}

# All errors logged
{
    "timestamp": "2024-01-15T10:30:10Z",
    "type": "validation_error",
    "message": "Missing required floor area",
    "recovery_action": "prompt_user_for_missing_data"
}
```

---

## Maximizing Ease of Use

### 1. **Smart Defaults**

```python
# Agent figures out most parameters automatically
agent.execute_workflow(
    workflow="full_review",
    workflow_params={
        "project_name": "Office Renovation",
        "address": {"city": "Atlanta", "state": "GA"}
        # Agent infers:
        # - jurisdiction = "GA"
        # - codes = ["IRC_2018", "IECC_2015", "NEC_2017", "GA_AMENDMENTS"]
        # - cost_factor = 0.95
        # - spec_tier = "standard" (default)
    }
)
```

### 2. **Natural Language Interface**

```python
# Agents can handle conversational requests
user_request = "Please check this plan for compliance and give me a rough estimate"

agent.add_message("user", user_request)
response = await agent.process_request()  # Handles all steps automatically
agent.add_message("assistant", response)
```

### 3. **Progressive Disclosure**

```python
# Simple requests get simple answers
"What would this cost?" 
→ Returns: $250,000 estimate

# Detailed requests get detailed answers
"Generate a full proposal with compliance report and detailed cost breakdown"
→ Returns: Complete proposal with all sections
```

### 4. **Fallback & Alternatives**

```python
# If OpenAI fails, try Ollama
try:
    result = orchestrator.execute_workflow(...)  # Uses OpenAI
except APIError:
    fallback_agent = EagleEyeAgent(
        role=AgentRole.ORCHESTRATOR,
        llm_provider="ollama"  # Switch to local
    )
    result = await fallback_agent.execute_workflow(...)
```

### 5. **Batch Operations**

```python
# Process multiple projects efficiently
projects = [
    {"name": "Project A", "file": "plans_a.pdf"},
    {"name": "Project B", "file": "plans_b.pdf"},
    {"name": "Project C", "file": "plans_c.pdf"}
]

results = []
for project in projects:
    result = await orchestrator.execute_workflow(
        workflow="full_review",
        workflow_params=project
    )
    results.append(result)
    
# All audit trails preserved
orchestrator.memory.save()
```

---

## Configuration Files Used

All configuration is stored and loaded automatically:

**`.env.local` (Local Development)**
```env
# All three LLM providers configured
OPENAI_API_KEY=sk-proj-...
OLLAMA_ENABLED=true
OLLAMA_MODEL=llama2
HUGGINGFACE_API_KEY=hf_...
```

**`agents/agent_training.py`**
- System prompts for each role
- Tool specifications with input/output schemas
- Workflow templates (full_review, compliance_check, pricing_only)
- Decision trees for intelligent defaults
- Agent examples and reasoning patterns

**`agents/agent_executor.py`**
- Agent creation and initialization
- Tool registration and calling
- Memory management and persistence
- Workflow execution engine
- Audit trail and reporting

**`config/settings.py`**
- Settings loaded from `.env.local`
- Type-safe configuration with validation
- Support for all LLM providers

---

## Deployment Checklist

- [x] OpenAI, Ollama, HuggingFace configured
- [x] Agent training framework ready
- [x] System prompts for each role
- [x] Tool specifications defined
- [x] Workflow templates created
- [x] Memory/audit system in place
- [ ] MCP server endpoints configured
- [ ] Tool handlers implemented and tested
- [ ] Error handling and recovery tested
- [ ] Batch testing with real projects
- [ ] Team training on agent capabilities
- [ ] Monitoring dashboard created
- [ ] Compliance review completed

---

## Next Steps

1. **Implement Tool Handlers**: Connect agent tools to actual MCP server endpoints
2. **Test with Sample Projects**: Run agents on real construction plans
3. **Fine-Tune Prompts**: Adjust system prompts based on results
4. **Add Specialized Agents**: Create agents for specific use cases
5. **Deploy to Production**: Container-based deployment with monitoring
6. **Build Dashboard**: Real-time agent monitoring and analytics
7. **Create Team Training**: Documentation and examples for team

---

## Support & Troubleshooting

**Agent Not Making Decisions?**
- Check system prompt is being set
- Verify tools are registered
- Check agent has appropriate role

**Tools Not Being Called?**
- Verify tool specifications match LLM provider format
- Check tool registry has entries
- Review agent logs for errors

**Poor Quality Outputs?**
- Review and improve system prompt
- Provide more context in requests
- Use specialized agent for that task
- Fine-tune with examples

**Performance Issues?**
- Use Ollama for speed (local)
- Use OpenAI for quality (cloud)
- Batch similar requests together
- Monitor tool call durations
