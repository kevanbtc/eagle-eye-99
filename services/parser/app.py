"""
Eagle Eye Parser Service - PDF Plan Parsing
"""
import pdfplumber
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import re


def extract_text_blocks(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract text blocks from PDF with page and position info"""
    blocks = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            
            # Extract words with positions
            words = page.extract_words()
            
            blocks.append({
                "page": page_num,
                "text": text,
                "words": words,
                "width": page.width,
                "height": page.height
            })
    
    return blocks


def extract_schedules(pdf_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract window/door/equipment schedules from PDF
    Uses simple heuristics to detect schedule tables
    """
    schedules = {
        "windows": [],
        "doors": [],
        "equipment": [],
        "finishes": []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            text_upper = text.upper()
            
            # Detect window schedule
            if "WINDOW SCHEDULE" in text_upper or "WINDOW SCHED" in text_upper:
                tables = page.extract_tables()
                schedules["windows"].append({
                    "page": page_num,
                    "raw_text": text,
                    "tables": tables
                })
            
            # Detect door schedule
            if "DOOR SCHEDULE" in text_upper or "DOOR SCHED" in text_upper:
                tables = page.extract_tables()
                schedules["doors"].append({
                    "page": page_num,
                    "raw_text": text,
                    "tables": tables
                })
            
            # Detect equipment schedule
            if "EQUIPMENT SCHEDULE" in text_upper or "EQUIP SCHED" in text_upper:
                tables = page.extract_tables()
                schedules["equipment"].append({
                    "page": page_num,
                    "raw_text": text,
                    "tables": tables
                })
            
            # Detect finish schedule
            if "FINISH SCHEDULE" in text_upper or "FINISHES" in text_upper:
                tables = page.extract_tables()
                schedules["finishes"].append({
                    "page": page_num,
                    "raw_text": text,
                    "tables": tables
                })
    
    return schedules


def detect_sheet_type(text: str) -> str:
    """Detect the type of sheet based on content"""
    text_upper = text.upper()
    
    # Structural patterns
    if any(keyword in text_upper for keyword in ["STRUCTURAL", "FOUNDATION", "FRAMING", "BEAM SCHEDULE"]):
        return "structural"
    
    # Architectural patterns
    if any(keyword in text_upper for keyword in ["FLOOR PLAN", "ELEVATIONS", "SECTIONS"]):
        return "architectural"
    
    # Mechanical patterns
    if any(keyword in text_upper for keyword in ["HVAC", "MECHANICAL", "DUCTWORK"]):
        return "mechanical"
    
    # Electrical patterns
    if any(keyword in text_upper for keyword in ["ELECTRICAL", "LIGHTING", "PANEL SCHEDULE"]):
        return "electrical"
    
    # Plumbing patterns
    if any(keyword in text_upper for keyword in ["PLUMBING", "PIPING", "FIXTURE"]):
        return "plumbing"
    
    # Site/Civil patterns
    if any(keyword in text_upper for keyword in ["SITE PLAN", "CIVIL", "GRADING"]):
        return "site"
    
    return "unknown"


def extract_dimensions(text: str) -> List[Dict[str, Any]]:
    """Extract dimension callouts from text"""
    # Pattern: numbers with feet/inches (e.g., 10'-6", 8'0")
    dimension_pattern = r"(\d+)[''][-\s]?(\d+)[\""]?"
    
    matches = re.findall(dimension_pattern, text)
    
    dimensions = []
    for match in matches:
        feet = int(match[0])
        inches = int(match[1]) if match[1] else 0
        total_inches = feet * 12 + inches
        
        dimensions.append({
            "feet": feet,
            "inches": inches,
            "total_inches": total_inches
        })
    
    return dimensions


def assess_quantity_confidence(item: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Assess confidence level for extracted quantity
    Returns: "High", "Medium", or "Low"
    
    Confidence scoring rules:
    - High: Found in clear schedule table with multiple corroborating data points
    - Medium: Found in text but with some ambiguity or single source
    - Low: Inferred, unclear, or contradictory information
    """
    confidence = "Medium"  # Default
    
    # Check if from schedule table
    is_from_schedule = item.get("source") == "schedule_table"
    has_qty_column = item.get("has_qty_column", False)
    has_corroboration = item.get("corroboration_count", 0) > 1
    
    # High confidence: clear schedule with quantities
    if is_from_schedule and has_qty_column and has_corroboration:
        confidence = "High"
    # High confidence: explicit callout with dimensions
    elif item.get("has_dimensions") and item.get("has_qty_callout"):
        confidence = "High"
    # Low confidence: inferred or unclear
    elif item.get("is_inferred") or item.get("has_contradictions"):
        confidence = "Low"
    # Low confidence: handwritten notes or poor OCR
    elif context.get("has_handwritten_notes") or context.get("ocr_quality") == "poor":
        confidence = "Low"
    # Low confidence: missing critical information
    elif not item.get("has_unit_of_measure"):
        confidence = "Low"
    
    return confidence


def extract_quantities_with_confidence(schedules: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
    """
    Extract quantities from schedules with confidence scoring
    """
    quantities = []
    
    for schedule_type, schedule_list in schedules.items():
        for schedule in schedule_list:
            tables = schedule.get("tables", [])
            
            for table in tables:
                if not table:
                    continue
                
                # Assume first row is header
                headers = table[0] if len(table) > 0 else []
                
                # Find quantity column
                qty_col_idx = None
                for idx, header in enumerate(headers):
                    if header and any(keyword in str(header).upper() for keyword in ["QTY", "QUANTITY", "COUNT", "#"]):
                        qty_col_idx = idx
                        break
                
                # Extract items from rows
                for row_idx, row in enumerate(table[1:], 1):
                    if not row or len(row) == 0:
                        continue
                    
                    # Extract quantity
                    qty_value = None
                    if qty_col_idx is not None and qty_col_idx < len(row):
                        qty_str = str(row[qty_col_idx]).strip()
                        # Try to parse as number
                        try:
                            qty_value = float(qty_str)
                        except (ValueError, AttributeError):
                            pass
                    
                    # Build item context
                    item_context = {
                        "source": "schedule_table",
                        "has_qty_column": qty_col_idx is not None,
                        "corroboration_count": 1,  # Could be enhanced with cross-reference checking
                        "has_dimensions": False,
                        "has_qty_callout": qty_value is not None,
                        "is_inferred": qty_value is None,
                        "has_contradictions": False,
                        "has_unit_of_measure": True  # Assume schedule has UOM
                    }
                    
                    # Assess confidence
                    confidence = assess_quantity_confidence(item_context, {})
                    
                    if qty_value:
                        quantities.append({
                            "schedule_type": schedule_type,
                            "page": schedule.get("page"),
                            "row": row_idx,
                            "quantity": qty_value,
                            "raw_data": row,
                            "confidence": confidence,
                            "needs_rfi": confidence == "Low"
                        })
    
    return quantities


def build_plan_graph(files: List[str]) -> Dict[str, Any]:
    """
    Build a plan graph from multiple PDF files
    Returns structured data about sheets, schedules, and quantities
    """
    graph = {
        "sheets": [],
        "schedules": {
            "windows": [],
            "doors": [],
            "equipment": [],
            "finishes": []
        },
        "quantities": [],
        "rfi_items": [],  # Low-confidence items flagged for RFI
        "metadata": {
            "total_files": len(files),
            "total_pages": 0,
            "confidence_summary": {
                "high": 0,
                "medium": 0,
                "low": 0
            }
        }
    }
    
    for file_path in files:
        # Extract text blocks
        blocks = extract_text_blocks(file_path)
        
        # Extract schedules
        schedules = extract_schedules(file_path)
        
        # Merge schedules
        for schedule_type, schedule_data in schedules.items():
            graph["schedules"][schedule_type].extend(schedule_data)
        
        # Process each page
        for block in blocks:
            sheet_info = {
                "file": Path(file_path).name,
                "page": block["page"],
                "sheet_type": detect_sheet_type(block["text"]),
                "dimensions": extract_dimensions(block["text"]),
                "text_preview": block["text"][:500] if block["text"] else ""
            }
            graph["sheets"].append(sheet_info)
            graph["metadata"]["total_pages"] += 1
    
    # Extract quantities with confidence scoring
    quantities = extract_quantities_with_confidence(graph["schedules"])
    graph["quantities"] = quantities
    
    # Separate RFI items and update summary
    for qty in quantities:
        confidence_level = qty.get("confidence", "Medium").lower()
        graph["metadata"]["confidence_summary"][confidence_level] = \
            graph["metadata"]["confidence_summary"].get(confidence_level, 0) + 1
        
        if qty.get("needs_rfi"):
            graph["rfi_items"].append({
                "item": qty,
                "reason": f"Low confidence ({qty.get('confidence')}) - requires manual verification",
                "suggested_question": f"Please verify quantity for {qty.get('schedule_type')} on page {qty.get('page')}"
            })
    
    return graph


def parse_project_files(project_id: str, file_paths: List[str]) -> Dict[str, Any]:
    """
    Main entry point for parsing project files
    Returns the complete plan graph
    """
    print(f"Parsing {len(file_paths)} files for project {project_id}")
    
    plan_graph = build_plan_graph(file_paths)
    
    print(f"Extracted {len(plan_graph['sheets'])} sheets")
    print(f"Found {len(plan_graph['schedules']['windows'])} window schedules")
    print(f"Found {len(plan_graph['schedules']['doors'])} door schedules")
    print(f"Extracted {len(plan_graph['quantities'])} quantities")
    print(f"Confidence: {plan_graph['metadata']['confidence_summary']}")
    print(f"RFI items: {len(plan_graph['rfi_items'])}")
    
    return plan_graph


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python app.py <pdf_file1> [pdf_file2] ...")
        sys.exit(1)
    
    files = sys.argv[1:]
    result = parse_project_files("test-project", files)
    
    print(json.dumps(result, indent=2))
