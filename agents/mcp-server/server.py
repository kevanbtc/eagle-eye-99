"""
Eagle Eye MCP Server
Orchestration tools for pipeline execution
"""
import sys
import json
from typing import Any, Dict

# Tool registry
TOOLS = {}

def tool(name: str):
    """Decorator to register MCP tools"""
    def wrap(fn):
        TOOLS[name] = fn
        return fn
    return wrap


@tool("crm.create_project")
def create_project(args: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new project in the CRM"""
    # In production: calls API service
    import requests
    
    api_url = args.get("api_url", "http://api:8000")
    project_data = {
        "name": args.get("name"),
        "address_json": args.get("address"),
        "spec_tier": args.get("spec_tier", "Standard")
    }
    
    # resp = requests.post(f"{api_url}/projects", json=project_data)
    # return resp.json()
    
    return {
        "project_id": "mock-uuid-1234",
        "status": "created"
    }


@tool("ingest.parse")
def ingest_parse(args: Dict[str, Any]) -> Dict[str, Any]:
    """Parse plan PDFs into structured plan graph"""
    # In production: calls parser service
    project_id = args.get("project_id")
    file_paths = args.get("file_paths", [])
    
    return {
        "project_id": project_id,
        "plan_graph": {
            "sheets": len(file_paths),
            "schedules": {"windows": 0, "doors": 0}
        },
        "status": "parsed"
    }


@tool("rules.check")
def rules_check(args: Dict[str, Any]) -> Dict[str, Any]:
    """Run code compliance checks"""
    # In production: calls rules service
    project_id = args.get("project_id")
    plan_graph = args.get("plan_graph", {})
    
    return {
        "project_id": project_id,
        "findings": [
            {
                "severity": "Red",
                "code_citation": "IRC 2018 R602.10",
                "impact": "Missing braced wall panels"
            }
        ],
        "status": "checked"
    }


@tool("pricing.estimate")
def pricing_estimate(args: Dict[str, Any]) -> Dict[str, Any]:
    """Generate pricing estimate"""
    # In production: calls pricing service
    project_id = args.get("project_id")
    quantities = args.get("quantities", [])
    region = args.get("region", "Atlanta_GA")
    
    return {
        "project_id": project_id,
        "estimate": {
            "subtotal": 50000.00,
            "grand_total": 60000.00
        },
        "status": "priced"
    }


@tool("reports.render")
def reports_render(args: Dict[str, Any]) -> Dict[str, Any]:
    """Render proposal PDFs and CSVs"""
    # In production: calls reports service
    project_id = args.get("project_id")
    report_types = args.get("report_types", ["proposal", "xactimate"])
    
    return {
        "project_id": project_id,
        "reports": {
            "proposal_pdf": f"s3://eagle-files/projects/{project_id}/reports/proposal.pdf",
            "xactimate_csv": f"s3://eagle-files/projects/{project_id}/reports/xactimate.csv"
        },
        "status": "rendered"
    }


@tool("pipeline.run")
def pipeline_run(args: Dict[str, Any]) -> Dict[str, Any]:
    """Run the complete pipeline"""
    project_id = args.get("project_id")
    file_paths = args.get("file_paths", [])
    
    # Parse
    parse_result = ingest_parse({"project_id": project_id, "file_paths": file_paths})
    
    # Rules
    rules_result = rules_check({"project_id": project_id, "plan_graph": parse_result["plan_graph"]})
    
    # Price
    pricing_result = pricing_estimate({"project_id": project_id, "quantities": []})
    
    # Render
    reports_result = reports_render({"project_id": project_id})
    
    return {
        "project_id": project_id,
        "pipeline": {
            "parse": parse_result["status"],
            "rules": rules_result["status"],
            "pricing": pricing_result["status"],
            "reports": reports_result["status"]
        },
        "status": "complete"
    }


def main():
    """MCP stdio server main loop"""
    print("Eagle Eye MCP Server started", file=sys.stderr)
    
    for line in sys.stdin:
        try:
            req = json.loads(line.strip())
            tool_name = req.get("name")
            arguments = req.get("arguments", {})
            
            if tool_name in TOOLS:
                result = TOOLS[tool_name](arguments)
                response = {"success": True, "result": result}
            else:
                response = {"success": False, "error": f"Unknown tool: {tool_name}"}
            
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except Exception as e:
            error_response = {"success": False, "error": str(e)}
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
