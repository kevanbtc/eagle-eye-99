"""
Example: Agents Using MCP Tool Handlers

This module demonstrates how agents use the tool handler registry
to execute complete workflows autonomously.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agents.agent_executor import EagleEyeAgent, AgentRole
except ImportError:
    # Mock for testing without full agent setup
    class AgentRole:
        ORCHESTRATOR = "ORCHESTRATOR"
        COMPLIANCE = "COMPLIANCE"
        PRICING = "PRICING"
        PROPOSAL = "PROPOSAL"
    
    class EagleEyeAgent:
        def __init__(self, role, llm_provider):
            self.role = role
            self.llm_provider = llm_provider

from agents.mcp_tool_handlers import (
    get_handler_registry,
    execute_tool,
    ToolCallResult
)


async def example_1_single_agent_full_review():
    """
    Example 1: Single agent performs complete project review
    
    This shows how one orchestrator agent chains multiple tool calls
    to perform a full review workflow.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Single Agent Full Review")
    print("=" * 80)
    
    # Create orchestrator agent
    agent = EagleEyeAgent(
        role=AgentRole.ORCHESTRATOR,
        llm_provider="openai"
    )
    
    # Define workflow parameters
    workflow_params = {
        "project_name": "Downtown Office Complex",
        "client_name": "Metro Development Corp",
        "address": {"city": "Atlanta", "state": "GA", "zip": "30303"},
        "file_paths": ["plans_floor1.pdf", "plans_floor2.pdf", "details.pdf"],
        "project_type": "commercial",
        "spec_tier": "standard"
    }
    
    print("\n[*] Project: Downtown Office Complex")
    print("[*] Client: Metro Development Corp")
    print("[*] Location: Atlanta, GA")
    print("[*] Type: Commercial")
    print("[*] Tier: Standard")
    
    # Execute workflow
    print("\n[*] Executing full_review workflow...")
    print("[*] Agent will:")
    print("    1. Create project in CRM")
    print("    2. Parse construction plans")
    print("    3. Check code compliance")
    print("    4. Generate cost estimate")
    print("    5. Create professional proposal")
    
    # In real implementation:
    # result = await agent.execute_workflow("full_review", workflow_params)
    
    # For demo, manually execute tool chain
    print("\n[*] Tool Execution Chain:")
    
    registry = get_handler_registry()
    
    # Step 1: Create project
    print("\n[1/5] Creating project...")
    proj_result = await registry.execute("crm.create_project", {
        "project_name": workflow_params["project_name"],
        "client_name": workflow_params["client_name"],
        "address": workflow_params["address"]
    })
    print(f"     Status: {proj_result.status}")
    print(f"     Project ID: {proj_result.result['project_id']}")
    print(f"     Completed in {proj_result.duration_ms:.1f}ms")
    project_id = proj_result.result['project_id']
    
    # Step 2: Parse plans
    print("\n[2/5] Parsing construction plans...")
    parse_result = await registry.execute("ingest.parse", {
        "file_paths": workflow_params["file_paths"]
    })
    print(f"     Status: {parse_result.status}")
    print(f"     Files parsed: {parse_result.result['parsed_files']}")
    print(f"     Elements found: {parse_result.result['elements_found']}")
    print(f"     Completed in {parse_result.duration_ms:.1f}ms")
    plan_graph = parse_result.result['plan_graph']
    
    # Step 3: Check compliance
    print("\n[3/5] Checking code compliance...")
    compliance_result = await registry.execute("rules.check_compliance", {
        "plan_graph": plan_graph,
        "jurisdictions": ["IRC", "IECC", "NEC"]
    })
    print(f"     Status: {compliance_result.status}")
    print(f"     Is compliant: {compliance_result.result['is_compliant']}")
    print(f"     Violations: {len(compliance_result.result['violations'])}")
    print(f"     Completed in {compliance_result.duration_ms:.1f}ms")
    
    # Step 4: Generate estimate
    print("\n[4/5] Generating cost estimate...")
    pricing_result = await registry.execute("pricing.estimate", {
        "plan_graph": plan_graph,
        "jurisdiction": workflow_params["address"]
    })
    print(f"     Status: {pricing_result.status}")
    print(f"     Total Estimate: ${pricing_result.result['total_estimate']:,}")
    print(f"     Labor: ${pricing_result.result['breakdown']['labor']:,}")
    print(f"     Materials: ${pricing_result.result['breakdown']['materials']:,}")
    print(f"     Contingency: ${pricing_result.result['breakdown']['contingency']:,}")
    print(f"     Rate per sq ft: ${pricing_result.result['rate_per_sqft']}")
    print(f"     Completed in {pricing_result.duration_ms:.1f}ms")
    
    # Step 5: Generate proposal
    print("\n[5/5] Generating professional proposal...")
    proposal_result = await registry.execute("reports.generate_proposal", {
        "project_id": project_id,
        "compliance_findings": compliance_result.result['violations'],
        "estimate": pricing_result.result
    })
    print(f"     Status: {proposal_result.status}")
    print(f"     Proposal ID: {proposal_result.result['proposal_id']}")
    print(f"     Document URL: {proposal_result.result['document_url']}")
    print(f"     Document size: {proposal_result.result['document_size_kb']} KB")
    print(f"     Pages: {proposal_result.result['pages']}")
    print(f"     Completed in {proposal_result.duration_ms:.1f}ms")
    
    print("\n[+] Workflow completed successfully!")
    print(f"[+] Total execution time: All steps completed")
    print(f"[+] Proposal ready for client review at: {proposal_result.result['document_url']}")


async def example_2_specialized_agents():
    """
    Example 2: Multiple specialized agents working in parallel
    
    This shows how different agents can specialize in different tasks
    and work together to complete a project.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Specialized Agents (Parallel Execution)")
    print("=" * 80)
    
    # Create specialized agents
    compliance_agent = EagleEyeAgent(role=AgentRole.COMPLIANCE, llm_provider="ollama")
    pricing_agent = EagleEyeAgent(role=AgentRole.PRICING, llm_provider="huggingface")
    proposal_agent = EagleEyeAgent(role=AgentRole.PROPOSAL, llm_provider="openai")
    
    print("\n[*] Created 3 specialized agents:")
    print("    - Compliance Agent (Ollama: local, deterministic)")
    print("    - Pricing Agent (HuggingFace: specialized math)")
    print("    - Proposal Agent (OpenAI: best writing quality)")
    
    registry = get_handler_registry()
    
    # First, parse the plans (all agents need this)
    print("\n[*] Shared step: Parse construction plans")
    parse_result = await registry.execute("ingest.parse", {
        "file_paths": ["plans.pdf"]
    })
    plan_graph = parse_result.result['plan_graph']
    print(f"    [+] Plan parsed: {parse_result.result['elements_found']} elements")
    
    # Now run specialized agents in parallel
    print("\n[*] Running specialized agents in parallel...")
    
    compliance_check = registry.execute("rules.check_compliance", {
        "plan_graph": plan_graph,
        "jurisdictions": ["IRC", "IECC", "NEC"]
    })
    
    pricing_estimate = registry.execute("pricing.estimate", {
        "plan_graph": plan_graph,
        "jurisdiction": {"state": "GA"}
    })
    
    # Execute in parallel
    compliance_result, pricing_result = await asyncio.gather(
        compliance_check,
        pricing_estimate
    )
    
    print(f"    [+] Compliance check: {compliance_result.status} ({compliance_result.duration_ms:.1f}ms)")
    print(f"    [+] Pricing estimate: {pricing_result.status} ({pricing_result.duration_ms:.1f}ms)")
    
    print("\n[+] Both agents completed simultaneously!")
    is_compliant = compliance_result.result['is_compliant']
    compliance_status = "Compliant" if is_compliant else f"{len(compliance_result.result['violations'])} violations"
    print(f"    Compliance: {compliance_status}")
    print(f"    Estimate: ${pricing_result.result['total_estimate']:,}")


async def example_3_error_handling():
    """
    Example 3: Error handling and recovery
    
    This shows how handlers gracefully handle errors and agents recover.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Error Handling & Recovery")
    print("=" * 80)
    
    registry = get_handler_registry()
    
    # Example 1: Missing required parameters
    print("\n[*] Test 1: Missing required parameters")
    result = await registry.execute("crm.create_project", {
        "project_name": "Test Project"
        # Missing: "client_name"
    })
    print(f"    Status: {result.status}")
    print(f"    Error: {result.error_message}")
    
    # Example 2: Unknown tool
    print("\n[*] Test 2: Unknown tool")
    result = await registry.execute("invalid.tool", {})
    print(f"    Status: {result.status}")
    print(f"    Error: {result.error_message}")
    
    # Example 3: Recovery with fallback
    print("\n[*] Test 3: Automatic fallback to mock response")
    print("    (If real service unavailable, agents still work)")
    result = await registry.execute("pricing.estimate", {
        "plan_graph": {"square_footage": 2500},
        "jurisdiction": {"state": "GA"}
    })
    print(f"    Status: {result.status}")
    print(f"    Result: Estimate generated: ${result.result['total_estimate']:,}")


async def example_4_audit_trail():
    """
    Example 4: Audit trail tracking for compliance
    
    This shows how all tool calls are tracked for regulatory compliance.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Audit Trail & Compliance Tracking")
    print("=" * 80)
    
    registry = get_handler_registry()
    
    # Perform a series of tool calls
    print("\n[*] Executing tools and tracking audit trail...")
    
    calls = []
    
    # Call 1
    result = await registry.execute("crm.create_project", {
        "project_name": "Audit Test Project",
        "client_name": "Test Client"
    })
    calls.append({
        "tool": result.tool_name,
        "status": result.status,
        "timestamp": result.timestamp,
        "duration_ms": result.duration_ms
    })
    
    # Call 2
    result = await registry.execute("ingest.parse", {
        "file_paths": ["test.pdf"]
    })
    calls.append({
        "tool": result.tool_name,
        "status": result.status,
        "timestamp": result.timestamp,
        "duration_ms": result.duration_ms
    })
    
    # Call 3
    result = await registry.execute("rules.check_compliance", {
        "plan_graph": {"floors": 1},
        "jurisdictions": ["IRC"]
    })
    calls.append({
        "tool": result.tool_name,
        "status": result.status,
        "timestamp": result.timestamp,
        "duration_ms": result.duration_ms
    })
    
    # Print audit trail
    print("\n[*] Audit Trail:")
    print("-" * 80)
    for i, call in enumerate(calls, 1):
        print(f"\n[{i}] {call['tool']}")
        print(f"    Status: {call['status']}")
        print(f"    Timestamp: {call['timestamp']}")
        print(f"    Duration: {call['duration_ms']:.1f}ms")
    
    print("\n[+] Audit trail complete - ready for compliance review!")


async def example_5_workflow_templates():
    """
    Example 5: Different workflow templates for different needs
    
    This shows how the same handlers can be used in different workflows.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Workflow Templates")
    print("=" * 80)
    
    registry = get_handler_registry()
    
    # Template 1: Full Review (all steps)
    print("\n[TEMPLATE 1] Full Review Workflow")
    print("  Steps: Create -> Parse -> Compliance -> Pricing -> Proposal")
    print("  Use case: Complete project assessment")
    print("  Time: ~50ms total")
    
    # Template 2: Compliance Only
    print("\n[TEMPLATE 2] Compliance-Only Workflow")
    print("  Steps: Parse -> Compliance")
    print("  Use case: Code review for existing plans")
    print("  Time: ~10ms total")
    
    parse_result = await registry.execute("ingest.parse", {
        "file_paths": ["existing_plans.pdf"]
    })
    
    compliance_result = await registry.execute("rules.check_compliance", {
        "plan_graph": parse_result.result['plan_graph'],
        "jurisdictions": ["IRC"]
    })
    
    print(f"  Result: {compliance_result.status} - {'Compliant' if compliance_result.result['is_compliant'] else 'Has violations'}")
    
    # Template 3: Pricing Only
    print("\n[TEMPLATE 3] Pricing-Only Workflow")
    print("  Steps: Pricing")
    print("  Use case: Quick cost estimate")
    print("  Time: ~5ms total")
    
    pricing_result = await registry.execute("pricing.estimate", {
        "plan_graph": parse_result.result['plan_graph'],
        "jurisdiction": {"state": "GA"}
    })
    
    print(f"  Result: Estimate = ${pricing_result.result['total_estimate']:,}")


async def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("MCP TOOL HANDLERS - INTEGRATION EXAMPLES")
    print("=" * 80)
    
    await example_1_single_agent_full_review()
    await example_2_specialized_agents()
    await example_3_error_handling()
    await example_4_audit_trail()
    await example_5_workflow_templates()
    
    print("\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print("\n[+] Handler Registry is ready for production use!")
    print("[+] Agents can now execute complete workflows autonomously")
    print("[+] All tool calls are tracked for compliance\n")


if __name__ == "__main__":
    asyncio.run(main())
