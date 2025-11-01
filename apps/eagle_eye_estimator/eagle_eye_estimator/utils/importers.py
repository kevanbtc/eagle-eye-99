import csv
from typing import Optional

import frappe


def import_catalog(csv_path: str, region: Optional[str] = None, simulate: bool = False) -> dict:
    """Import a flat price sheet CSV into Items/Item Prices and Assemblies.

    Expected CSV headers (min):
      trade, code, name, unit, base_cost, labor_pct, material_pct, equipment_pct
    Additional columns are ignored.

    This is a minimal stub: tailor to your catalogs. Run inside a site context.
    """
    created_items = 0
    created_prices = 0
    created_assemblies = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = (row.get("code") or "").strip()
            name = (row.get("name") or code)
            unit = (row.get("unit") or "EA").strip()
            base_cost = float(row.get("base_cost") or 0)

            if not code:
                continue

            # Ensure Item exists
            item = frappe.db.get_value("Item", {"item_code": code})
            if not item and not simulate:
                doc = frappe.get_doc({
                    "doctype": "Item",
                    "item_code": code,
                    "item_name": name,
                    "is_stock_item": 0,
                    "stock_uom": unit,
                    "include_item_in_manufacturing": 0,
                    "item_group": "Services"
                }).insert(ignore_permissions=True)
                item = doc.name
                created_items += 1

            # Item Price
            if not simulate:
                frappe.get_doc({
                    "doctype": "Item Price",
                    "item_code": code,
                    "price_list": "Standard Selling",
                    "currency": "USD",
                    "price_list_rate": base_cost
                }).insert(ignore_permissions=True)
                created_prices += 1

            # Basic Assembly mirror (if desired)
            if not simulate:
                if not frappe.db.exists("Assembly", code):
                    a = frappe.get_doc({
                        "doctype": "Assembly",
                        "code": code,
                        "name_en": name,
                        "trade": row.get("trade") or "",
                        "unit": unit,
                        "items": [
                            {"item": code, "description": name, "qty_formula": "1", "wastage_pct": 0}
                        ]
                    }).insert(ignore_permissions=True)
                    created_assemblies += 1

    return {
        "items": created_items,
        "prices": created_prices,
        "assemblies": created_assemblies,
    }


def import_catalog_async(csv_path: str, region: Optional[str] = None):
    """Enqueue background job to import catalog."""
    frappe.enqueue(import_catalog, queue="long", job_name=f"Import Catalog {csv_path}", csv_path=csv_path, region=region)
    return {"enqueued": True, "path": csv_path}


def load_sample_fixtures():
    """Programmatically create a basic Proposal print format for Estimate v2.
    Useful if you don't want to manage JSON fixtures yet.
    """
    name = "Proposal - Eagle Eye"
    if not frappe.db.exists("Print Format", name):
        html = frappe.read_file(frappe.get_app_path("eagle_eye_estimator", "eagle_eye_estimator", "print_format", "proposal_eagle_eye", "proposal_eagle_eye.html"))
        frappe.get_doc({
            "doctype": "Print Format",
            "name": name,
            "doc_type": "Estimate v2",
            "module": "Eagle Eye Estimator",
            "html": html,
            "print_format_type": "Jinja",
            "standard": "Yes"
        }).insert(ignore_permissions=True)
    return {"ok": True, "print_format": name}
