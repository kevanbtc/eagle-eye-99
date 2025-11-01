"""
Odoo <-> Eagle Eye Connector
Bidirectional sync between Odoo Construction Estimator and Eagle Eye pricing engine
"""
from flask import Flask, request, jsonify
import xmlrpc.client
import requests
import os
from typing import Dict, List, Any
import json

app = Flask(__name__)

# Odoo connection config
ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')

# Eagle Eye API config
EAGLE_API_URL = os.getenv('EAGLE_API_URL', 'http://localhost:8000')


def odoo_authenticate():
    """Authenticate with Odoo and return uid"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    return uid


def odoo_execute(model: str, method: str, args: List = None, kwargs: Dict = None):
    """Execute Odoo RPC call"""
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    
    uid = odoo_authenticate()
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    
    return models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        model, method, args, kwargs
    )


def fetch_odoo_estimate(estimate_id: int) -> Dict[str, Any]:
    """
    Fetch estimate from Odoo Construction Estimator
    Returns estimate with line items in Eagle Eye-compatible format
    """
    # Fetch estimate header
    estimate = odoo_execute(
        'construction.estimate',
        'read',
        [[estimate_id]],
        {'fields': ['name', 'partner_id', 'project_id', 'state', 'total_amount']}
    )
    
    if not estimate:
        raise ValueError(f"Estimate {estimate_id} not found")
    
    estimate = estimate[0]
    
    # Fetch estimate lines
    line_ids = odoo_execute(
        'construction.estimate.line',
        'search',
        [[['estimate_id', '=', estimate_id]]]
    )
    
    lines = odoo_execute(
        'construction.estimate.line',
        'read',
        [line_ids],
        {'fields': [
            'product_id', 'name', 'product_uom', 'product_uom_qty',
            'price_unit', 'price_subtotal', 'analytic_account_id'
        ]}
    )
    
    # Convert to Eagle Eye format
    quantities = []
    for line in lines:
        quantities.append({
            "odoo_line_id": line['id'],
            "wbs": line.get('analytic_account_id', [None, 'General'])[1] if line.get('analytic_account_id') else 'General',
            "assembly": line.get('product_id', [None, 'Unknown'])[1] if line.get('product_id') else 'Unknown',
            "item": line['name'],
            "uom": line.get('product_uom', [None, 'EA'])[1] if line.get('product_uom') else 'EA',
            "quantity": line['product_uom_qty'],
            "unit_cost": line['price_unit'],
            "ext_cost": line['price_subtotal'],
            "trade": "General",  # Could be enhanced with product category mapping
            "confidence": "Medium"  # Odoo data is user-entered
        })
    
    return {
        "estimate_id": estimate_id,
        "name": estimate['name'],
        "partner_id": estimate.get('partner_id', [None, None])[0],
        "project_id": estimate.get('project_id', [None, None])[0],
        "state": estimate['state'],
        "quantities": quantities,
        "metadata": {
            "source": "odoo",
            "total_lines": len(quantities)
        }
    }


def push_to_eagle_eye(odoo_estimate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Push Odoo estimate to Eagle Eye for code review + pricing enhancement
    """
    payload = {
        "project_id": f"odoo_{odoo_estimate['estimate_id']}",
        "name": odoo_estimate['name'],
        "quantities": odoo_estimate['quantities'],
        "source": "odoo_connector"
    }
    
    # Call Eagle Eye pricing endpoint
    response = requests.post(
        f"{EAGLE_API_URL}/api/estimates/process",
        json=payload
    )
    
    response.raise_for_status()
    return response.json()


def update_odoo_estimate(estimate_id: int, eagle_eye_result: Dict[str, Any]):
    """
    Update Odoo estimate with Eagle Eye findings and adjusted pricing
    """
    # Add findings as internal notes
    if eagle_eye_result.get('findings'):
        findings_text = "\n\n=== Eagle Eye Code Review ===\n"
        for finding in eagle_eye_result['findings']:
            findings_text += f"\n[{finding['severity']}] {finding['code_citation']}\n"
            findings_text += f"  {finding['consequence']}\n"
            findings_text += f"  Fix: {finding['fix']}\n"
        
        odoo_execute(
            'construction.estimate',
            'write',
            [[estimate_id], {'notes': findings_text}]
        )
    
    # Optionally update line items with adjusted pricing
    if eagle_eye_result.get('estimate') and eagle_eye_result['estimate'].get('base'):
        # This would update individual line items with regional adjustments
        # Implementation depends on Odoo Construction Estimator schema
        pass
    
    return {"success": True, "updated": estimate_id}


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "odoo-eagle-connector"})


@app.route('/sync/odoo-to-eagle', methods=['POST'])
def sync_odoo_to_eagle():
    """
    Fetch estimate from Odoo, process through Eagle Eye, return enhanced estimate
    
    Request: {"estimate_id": 123}
    """
    data = request.get_json()
    estimate_id = data.get('estimate_id')
    
    if not estimate_id:
        return jsonify({"error": "estimate_id required"}), 400
    
    try:
        # Fetch from Odoo
        odoo_estimate = fetch_odoo_estimate(estimate_id)
        
        # Process through Eagle Eye
        eagle_result = push_to_eagle_eye(odoo_estimate)
        
        # Update Odoo with findings
        update_result = update_odoo_estimate(estimate_id, eagle_result)
        
        return jsonify({
            "success": True,
            "odoo_estimate": odoo_estimate,
            "eagle_eye_result": eagle_result,
            "odoo_update": update_result
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/sync/eagle-to-odoo', methods=['POST'])
def sync_eagle_to_odoo():
    """
    Create new Odoo estimate from Eagle Eye project
    
    Request: {"project_id": "uuid"}
    """
    data = request.get_json()
    project_id = data.get('project_id')
    
    if not project_id:
        return jsonify({"error": "project_id required"}), 400
    
    try:
        # Fetch Eagle Eye estimate
        response = requests.get(f"{EAGLE_API_URL}/api/estimates/{project_id}")
        response.raise_for_status()
        eagle_estimate = response.json()
        
        # Create Odoo estimate
        estimate_vals = {
            'name': eagle_estimate.get('name', f'Eagle Eye Import {project_id}'),
            'state': 'draft',
        }
        
        estimate_id = odoo_execute(
            'construction.estimate',
            'create',
            [estimate_vals]
        )
        
        # Create estimate lines
        if eagle_estimate.get('base'):
            for trade, items in eagle_estimate['base'].items():
                for item in items:
                    line_vals = {
                        'estimate_id': estimate_id,
                        'name': item['line_item'],
                        'product_uom_qty': item['qty'],
                        'price_unit': item['unit_cost'],
                    }
                    odoo_execute(
                        'construction.estimate.line',
                        'create',
                        [line_vals]
                    )
        
        return jsonify({
            "success": True,
            "odoo_estimate_id": estimate_id,
            "eagle_project_id": project_id
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/webhook/odoo-estimate-updated', methods=['POST'])
def odoo_webhook():
    """
    Webhook endpoint for Odoo to trigger Eagle Eye processing
    Configure in Odoo: Settings > Automation > Create automation rule
    """
    data = request.get_json()
    estimate_id = data.get('estimate_id')
    
    if not estimate_id:
        return jsonify({"error": "estimate_id required"}), 400
    
    try:
        # Trigger async processing
        odoo_estimate = fetch_odoo_estimate(estimate_id)
        eagle_result = push_to_eagle_eye(odoo_estimate)
        update_odoo_estimate(estimate_id, eagle_result)
        
        return jsonify({
            "success": True,
            "processed": estimate_id
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
