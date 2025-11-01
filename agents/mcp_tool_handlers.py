"""
MCP Tool Handler Registry

Maps agent tool calls to actual MCP server endpoints.
Implements handlers for all tools defined in agent_training.py:
- CRM: project management
- Ingest: plan parsing
- Rules: compliance checking
- Pricing: cost estimation
- Reports: document generation

Each handler:
1. Validates input parameters
2. Calls the MCP service endpoint (or returns mock data)
3. Processes the response
4. Returns structured result for agent
5. Logs success/failure for audit trail
"""

import asyncio
import json
import logging
import sys
import os
from typing import Any, Callable, Dict, Optional
from datetime import datetime, timezone
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

# Mock settings for when config not available
class MockSettings:
    class API:
        crm_base_url = "http://api:8000"
        parser_base_url = "http://parser:8001"
        rules_base_url = "http://rules:8002"
        pricing_base_url = "http://pricing:8003"
        reports_base_url = "http://reports:8004"
    
    api = API()

try:
    from config.settings import get_settings
except ImportError:
    def get_settings():
        return MockSettings()


@dataclass
class ToolCallResult:
    """Result of a tool call execution"""
    tool_name: str
    status: str  # "success" or "error"
    result: Any
    duration_ms: float
    timestamp: str
    error_message: Optional[str] = None


class MCPToolHandlerRegistry:
    """
    Registry for MCP tool handlers.
    
    Usage:
        registry = MCPToolHandlerRegistry()
        registry.register("crm.create_project", create_project_handler)
        result = await registry.execute("crm.create_project", params)
    """
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.settings = get_settings()
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register all default MCP handlers"""
        # CRM Handlers
        self.register("crm.create_project", self._handle_crm_create_project)
        self.register("crm.list_projects", self._handle_crm_list_projects)
        self.register("crm.get_project", self._handle_crm_get_project)
        self.register("crm.update_project", self._handle_crm_update_project)
        
        # Ingest Handlers
        self.register("ingest.parse", self._handle_ingest_parse)
        self.register("ingest.extract_data", self._handle_ingest_extract_data)
        
        # Rules Handlers
        self.register("rules.check_compliance", self._handle_rules_check_compliance)
        self.register("rules.get_violations", self._handle_rules_get_violations)
        self.register("rules.apply_amendments", self._handle_rules_apply_amendments)
        
        # Pricing Handlers
        self.register("pricing.estimate", self._handle_pricing_estimate)
        self.register("pricing.calculate_factors", self._handle_pricing_calculate_factors)
        self.register("pricing.get_regional_rates", self._handle_pricing_get_regional_rates)
        
        # Reports Handlers
        self.register("reports.generate_proposal", self._handle_reports_generate_proposal)
        self.register("reports.export_compliance_report", self._handle_reports_export_compliance)
        self.register("reports.create_summary", self._handle_reports_create_summary)
        
        logger.info(f"[+] Registered {len(self.handlers)} MCP tool handlers")
    
    def register(self, tool_name: str, handler: Callable):
        """Register a handler for a tool"""
        self.handlers[tool_name] = handler
    
    async def execute(self, tool_name: str, params: Dict[str, Any]) -> ToolCallResult:
        """
        Execute a tool handler.
        
        Args:
            tool_name: Name of the tool (e.g., "crm.create_project")
            params: Input parameters for the tool
            
        Returns:
            ToolCallResult with status, result, and timing
        """
        if tool_name not in self.handlers:
            return ToolCallResult(
                tool_name=tool_name,
                status="error",
                result=None,
                duration_ms=0,
                timestamp=datetime.now(timezone.utc).isoformat(),
                error_message=f"Unknown tool: {tool_name}"
            )
        
        handler = self.handlers[tool_name]
        start_time = datetime.now(timezone.utc)
        
        try:
            result = await handler(params)
            duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            
            return ToolCallResult(
                tool_name=tool_name,
                status="success",
                result=result,
                duration_ms=duration,
                timestamp=start_time.isoformat()
            )
        except Exception as e:
            duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            logger.error(f"[-] Error executing tool {tool_name}: {str(e)}")
            
            return ToolCallResult(
                tool_name=tool_name,
                status="error",
                result=None,
                duration_ms=duration,
                timestamp=start_time.isoformat(),
                error_message=str(e)
            )
    
    # ============================================================================
    # CRM HANDLERS
    # ============================================================================
    
    async def _handle_crm_create_project(self, params: Dict) -> Dict:
        """Create a new project in CRM"""
        required = ["project_name", "client_name"]
        self._validate_params(params, required)
        
        # Mock implementation
        return {
            "project_id": f"proj_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "project_name": params.get("project_name"),
            "client_name": params.get("client_name"),
            "address": params.get("address", {}),
            "status": "created",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def _handle_crm_list_projects(self, params: Dict) -> Dict:
        """List all projects or filter by criteria"""
        return {
            "projects": [],
            "total": 0,
            "filters_applied": params
        }
    
    async def _handle_crm_get_project(self, params: Dict) -> Dict:
        """Get project details"""
        required = ["project_id"]
        self._validate_params(params, required)
        
        return {
            "project_id": params.get("project_id"),
            "project_name": "Sample Project",
            "client_name": "Sample Client",
            "status": "active"
        }
    
    async def _handle_crm_update_project(self, params: Dict) -> Dict:
        """Update project information"""
        required = ["project_id"]
        self._validate_params(params, required)
        
        project_id = params.pop("project_id")
        return {
            "project_id": project_id,
            "status": "updated",
            "updates": params,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    
    # ============================================================================
    # INGEST HANDLERS
    # ============================================================================
    
    async def _handle_ingest_parse(self, params: Dict) -> Dict:
        """Parse construction plans (PDF files)"""
        required = ["file_paths"]
        self._validate_params(params, required)
        
        file_paths = params["file_paths"]
        if not isinstance(file_paths, list):
            file_paths = [file_paths]
        
        # Mock implementation
        return {
            "plan_graph": {
                "floors": 1,
                "rooms": 5,
                "square_footage": 2500,
                "construction_type": "wood_frame",
                "systems": {
                    "electrical": "present",
                    "plumbing": "present",
                    "hvac": "present"
                }
            },
            "parsed_files": len(file_paths),
            "elements_found": 47,
            "status": "parsed",
            "parse_date": datetime.now(timezone.utc).isoformat()
        }
    
    async def _handle_ingest_extract_data(self, params: Dict) -> Dict:
        """Extract specific data from parsed plans"""
        required = ["plan_graph", "extraction_type"]
        self._validate_params(params, required)
        
        extraction_type = params.get("extraction_type")
        
        return {
            "extraction_type": extraction_type,
            "data_extracted": True,
            "element_count": 12,
            "status": "extracted",
            "extraction_date": datetime.now(timezone.utc).isoformat()
        }
    
    # ============================================================================
    # RULES HANDLERS
    # ============================================================================
    
    async def _handle_rules_check_compliance(self, params: Dict) -> Dict:
        """Check plan against building codes"""
        required = ["plan_graph", "jurisdictions"]
        self._validate_params(params, required)
        
        return {
            "is_compliant": True,
            "violations": [],
            "jurisdictions_checked": params.get("jurisdictions", []),
            "check_date": datetime.now(timezone.utc).isoformat(),
            "status": "compliant"
        }
    
    async def _handle_rules_get_violations(self, params: Dict) -> Dict:
        """Get list of code violations"""
        required = ["plan_graph"]
        self._validate_params(params, required)
        
        return {
            "violations": [],
            "critical_count": 0,
            "major_count": 0,
            "minor_count": 0,
            "total_violations": 0,
            "check_date": datetime.now(timezone.utc).isoformat()
        }
    
    async def _handle_rules_apply_amendments(self, params: Dict) -> Dict:
        """Apply state/local code amendments"""
        required = ["plan_graph", "state"]
        self._validate_params(params, required)
        
        state = params.get("state", "GA")
        
        return {
            "state": state,
            "local_jurisdiction": params.get("local_jurisdiction", ""),
            "amendments_applied": [f"{state} Building Code Amendments"],
            "status": "applied",
            "applied_date": datetime.now(timezone.utc).isoformat()
        }
    
    # ============================================================================
    # PRICING HANDLERS
    # ============================================================================
    
    async def _handle_pricing_estimate(self, params: Dict) -> Dict:
        """Generate cost estimate for project"""
        required = ["plan_graph", "jurisdiction"]
        self._validate_params(params, required)
        
        # Mock estimation based on square footage
        sq_ft = params.get("plan_graph", {}).get("square_footage", 2500)
        base_rate = 100  # $ per sq ft
        regional_factor = 0.95  # GA factor
        
        labor_cost = sq_ft * base_rate * 0.6 * regional_factor
        material_cost = sq_ft * base_rate * 0.3 * regional_factor
        contingency = (labor_cost + material_cost) * 0.1
        total = labor_cost + material_cost + contingency
        
        return {
            "total_estimate": int(total),
            "currency": "USD",
            "breakdown": {
                "labor": int(labor_cost),
                "materials": int(material_cost),
                "contingency": int(contingency)
            },
            "square_footage": sq_ft,
            "rate_per_sqft": base_rate,
            "regional_factor": regional_factor,
            "jurisdiction": params.get("jurisdiction"),
            "estimate_date": datetime.now(timezone.utc).isoformat(),
            "status": "estimated"
        }
    
    async def _handle_pricing_calculate_factors(self, params: Dict) -> Dict:
        """Calculate regional and project-specific cost factors"""
        required = ["jurisdiction", "project_type"]
        self._validate_params(params, required)
        
        jurisdiction = params.get("jurisdiction", {})
        state = jurisdiction.get("state", "GA") if isinstance(jurisdiction, dict) else "GA"
        
        # Mock regional factors by state
        factors = {
            "GA": 0.95,
            "CA": 1.15,
            "TX": 1.0,
            "NY": 1.25,
            "FL": 0.98
        }
        
        regional_factor = factors.get(state, 1.0)
        
        return {
            "regional_factor": regional_factor,
            "project_type_factor": 1.0,
            "quality_factor": 1.0,
            "combined_factor": regional_factor,
            "jurisdiction": params.get("jurisdiction"),
            "calculation_date": datetime.now(timezone.utc).isoformat()
        }
    
    async def _handle_pricing_get_regional_rates(self, params: Dict) -> Dict:
        """Get regional labor and material rates"""
        required = ["jurisdiction"]
        self._validate_params(params, required)
        
        return {
            "labor_rate_per_hour": 75,
            "material_markup": 1.25,
            "equipment_daily_rate": 500,
            "crane_rate_daily": 2000,
            "permit_average": 1500,
            "jurisdiction": params.get("jurisdiction"),
            "effective_date": datetime.now(timezone.utc).isoformat(),
            "currency": "USD"
        }
    
    # ============================================================================
    # REPORTS HANDLERS
    # ============================================================================
    
    async def _handle_reports_generate_proposal(self, params: Dict) -> Dict:
        """Generate professional proposal document"""
        required = ["project_id", "compliance_findings", "estimate"]
        self._validate_params(params, required)
        
        return {
            "proposal_id": f"prop_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "project_id": params.get("project_id"),
            "document_url": "/reports/proposal_123.pdf",
            "document_size_kb": 245,
            "status": "generated",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "pages": 8
        }
    
    async def _handle_reports_export_compliance(self, params: Dict) -> Dict:
        """Export compliance report"""
        required = ["project_id", "findings"]
        self._validate_params(params, required)
        
        export_format = params.get("format", "pdf")
        
        return {
            "report_id": f"comp_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "project_id": params.get("project_id"),
            "document_url": f"/reports/compliance_123.{export_format}",
            "export_format": export_format,
            "document_size_kb": 185,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "status": "exported"
        }
    
    async def _handle_reports_create_summary(self, params: Dict) -> Dict:
        """Create executive summary"""
        required = ["project_id"]
        self._validate_params(params, required)
        
        return {
            "summary_id": f"summ_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "project_id": params.get("project_id"),
            "summary_text": "Executive summary of project review and recommendations.",
            "key_findings": [
                "Plan is compliant with IRC 2018",
                "No critical violations found",
                "Two minor items for consideration"
            ],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "created"
        }
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def _validate_params(self, params: Dict, required: list) -> None:
        """Validate that required parameters are present"""
        missing = [p for p in required if p not in params or params[p] is None]
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")


# Global registry instance
_registry: Optional[MCPToolHandlerRegistry] = None


def get_handler_registry() -> MCPToolHandlerRegistry:
    """Get or create the global handler registry"""
    global _registry
    if _registry is None:
        _registry = MCPToolHandlerRegistry()
    return _registry


async def execute_tool(tool_name: str, params: Dict[str, Any]) -> ToolCallResult:
    """
    Convenience function to execute a tool via the global registry.
    
    Usage:
        result = await execute_tool("crm.create_project", {
            "project_name": "Office Renovation",
            "client_name": "ABC Corp"
        })
    """
    registry = get_handler_registry()
    return await registry.execute(tool_name, params)


# ============================================================================
# TEST/DEMO
# ============================================================================

async def test_handlers():
    """Test all handlers with mock data"""
    registry = get_handler_registry()
    
    print("\n[*] Testing MCP Tool Handlers")
    print("=" * 80)
    
    # Test CRM
    print("\n[*] CRM Handlers")
    result = await registry.execute("crm.create_project", {
        "project_name": "Office Renovation",
        "client_name": "ABC Corp",
        "address": {"city": "Atlanta", "state": "GA"}
    })
    print(f"  [{'+ ' if result.status == 'success' else '- '}] create_project: {result.status} ({result.duration_ms:.1f}ms)")
    project_id = result.result.get("project_id") if result.result else "test_proj_123"
    
    # Test Ingest
    print("\n[*] Ingest Handlers")
    result = await registry.execute("ingest.parse", {
        "file_paths": ["plans.pdf"]
    })
    print(f"  [{'+ ' if result.status == 'success' else '- '}] parse: {result.status} ({result.duration_ms:.1f}ms)")
    plan_graph = result.result.get("plan_graph") if result.result else {}
    
    # Test Rules
    print("\n[*] Rules Handlers")
    result = await registry.execute("rules.check_compliance", {
        "plan_graph": plan_graph,
        "jurisdictions": ["IRC", "IECC", "NEC"]
    })
    print(f"  [{'+ ' if result.status == 'success' else '- '}] check_compliance: {result.status} ({result.duration_ms:.1f}ms)")
    
    # Test Pricing
    print("\n[*] Pricing Handlers")
    result = await registry.execute("pricing.estimate", {
        "plan_graph": plan_graph,
        "jurisdiction": {"state": "GA", "city": "Atlanta"}
    })
    print(f"  [{'+ ' if result.status == 'success' else '- '}] estimate: {result.status} ({result.duration_ms:.1f}ms)")
    estimate = result.result if result.result else {}
    
    # Test Reports
    print("\n[*] Reports Handlers")
    result = await registry.execute("reports.generate_proposal", {
        "project_id": project_id,
        "compliance_findings": [],
        "estimate": estimate
    })
    print(f"  [{'+ ' if result.status == 'success' else '- '}] generate_proposal: {result.status} ({result.duration_ms:.1f}ms)")
    
    print("\n[+] All handler tests completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(test_handlers())
