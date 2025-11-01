"""
IfcOpenShell Quantity Takeoff Service
Auto-extract quantities from IFC models for Eagle Eye pricing
"""
from flask import Flask, request, jsonify
import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.shape
from typing import Dict, List, Any
import tempfile
import os

app = Flask(__name__)


def extract_quantities_from_ifc(ifc_path: str) -> Dict[str, Any]:
    """
    Extract quantities from IFC model
    Returns structured quantities compatible with Eagle Eye parser
    """
    ifc_file = ifcopenshell.open(ifc_path)
    
    quantities = {
        "walls": [],
        "windows": [],
        "doors": [],
        "slabs": [],
        "roofs": [],
        "columns": [],
        "beams": [],
        "metadata": {
            "ifc_schema": ifc_file.schema,
            "project_name": None,
            "total_elements": 0
        }
    }
    
    # Get project info
    project = ifc_file.by_type("IfcProject")
    if project:
        quantities["metadata"]["project_name"] = project[0].Name
    
    # Extract walls
    walls = ifc_file.by_type("IfcWall")
    for wall in walls:
        wall_data = {
            "ifc_guid": wall.GlobalId,
            "name": wall.Name or "Unnamed Wall",
            "type": wall.ObjectType or "Standard",
            "quantities": {},
            "properties": {},
            "confidence": "High"  # IFC data is explicit
        }
        
        # Get quantities from property sets
        for definition in wall.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcElementQuantity'):
                    for quantity in property_set.Quantities:
                        if quantity.is_a('IfcQuantityArea'):
                            wall_data["quantities"]["area_sf"] = quantity.AreaValue * 10.764  # m² to SF
                        elif quantity.is_a('IfcQuantityLength'):
                            wall_data["quantities"]["length_lf"] = quantity.LengthValue * 3.281  # m to LF
                        elif quantity.is_a('IfcQuantityVolume'):
                            wall_data["quantities"]["volume_cf"] = quantity.VolumeValue * 35.315  # m³ to CF
        
        # Get properties (material, fire rating, etc.)
        for definition in wall.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcPropertySet'):
                    for prop in property_set.HasProperties:
                        if prop.is_a('IfcPropertySingleValue'):
                            wall_data["properties"][prop.Name] = str(prop.NominalValue.wrappedValue) if prop.NominalValue else None
        
        quantities["walls"].append(wall_data)
    
    # Extract windows
    windows = ifc_file.by_type("IfcWindow")
    for window in windows:
        window_data = {
            "ifc_guid": window.GlobalId,
            "name": window.Name or "Unnamed Window",
            "type": window.ObjectType or "Standard",
            "quantities": {},
            "properties": {},
            "confidence": "High"
        }
        
        # Get window dimensions
        for definition in window.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcElementQuantity'):
                    for quantity in property_set.Quantities:
                        if quantity.is_a('IfcQuantityArea'):
                            window_data["quantities"]["area_sf"] = quantity.AreaValue * 10.764
                        elif quantity.is_a('IfcQuantityLength'):
                            if quantity.Name == "Width":
                                window_data["quantities"]["width_in"] = quantity.LengthValue * 39.37  # m to inches
                            elif quantity.Name == "Height":
                                window_data["quantities"]["height_in"] = quantity.LengthValue * 39.37
        
        # Get window properties (U-factor, SHGC, etc.)
        for definition in window.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcPropertySet'):
                    for prop in property_set.HasProperties:
                        if prop.is_a('IfcPropertySingleValue'):
                            window_data["properties"][prop.Name] = str(prop.NominalValue.wrappedValue) if prop.NominalValue else None
        
        quantities["windows"].append(window_data)
    
    # Extract doors
    doors = ifc_file.by_type("IfcDoor")
    for door in doors:
        door_data = {
            "ifc_guid": door.GlobalId,
            "name": door.Name or "Unnamed Door",
            "type": door.ObjectType or "Standard",
            "quantities": {},
            "properties": {},
            "confidence": "High"
        }
        
        # Get door dimensions
        for definition in door.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcElementQuantity'):
                    for quantity in property_set.Quantities:
                        if quantity.is_a('IfcQuantityArea'):
                            door_data["quantities"]["area_sf"] = quantity.AreaValue * 10.764
                        elif quantity.is_a('IfcQuantityLength'):
                            if quantity.Name == "Width":
                                door_data["quantities"]["width_in"] = quantity.LengthValue * 39.37
                            elif quantity.Name == "Height":
                                door_data["quantities"]["height_in"] = quantity.LengthValue * 39.37
        
        quantities["doors"].append(door_data)
    
    # Extract slabs/floors
    slabs = ifc_file.by_type("IfcSlab")
    for slab in slabs:
        slab_data = {
            "ifc_guid": slab.GlobalId,
            "name": slab.Name or "Unnamed Slab",
            "type": slab.ObjectType or slab.PredefinedType or "FLOOR",
            "quantities": {},
            "properties": {},
            "confidence": "High"
        }
        
        for definition in slab.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcElementQuantity'):
                    for quantity in property_set.Quantities:
                        if quantity.is_a('IfcQuantityArea'):
                            slab_data["quantities"]["area_sf"] = quantity.AreaValue * 10.764
                        elif quantity.is_a('IfcQuantityVolume'):
                            slab_data["quantities"]["volume_cf"] = quantity.VolumeValue * 35.315
        
        if slab.PredefinedType == "ROOF":
            quantities["roofs"].append(slab_data)
        else:
            quantities["slabs"].append(slab_data)
    
    # Extract columns
    columns = ifc_file.by_type("IfcColumn")
    for column in columns:
        column_data = {
            "ifc_guid": column.GlobalId,
            "name": column.Name or "Unnamed Column",
            "type": column.ObjectType or "Standard",
            "quantities": {},
            "confidence": "High"
        }
        
        for definition in column.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcElementQuantity'):
                    for quantity in property_set.Quantities:
                        if quantity.is_a('IfcQuantityLength'):
                            column_data["quantities"]["length_lf"] = quantity.LengthValue * 3.281
                        elif quantity.is_a('IfcQuantityVolume'):
                            column_data["quantities"]["volume_cf"] = quantity.VolumeValue * 35.315
        
        quantities["columns"].append(column_data)
    
    # Extract beams
    beams = ifc_file.by_type("IfcBeam")
    for beam in beams:
        beam_data = {
            "ifc_guid": beam.GlobalId,
            "name": beam.Name or "Unnamed Beam",
            "type": beam.ObjectType or "Standard",
            "quantities": {},
            "confidence": "High"
        }
        
        for definition in beam.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a('IfcElementQuantity'):
                    for quantity in property_set.Quantities:
                        if quantity.is_a('IfcQuantityLength'):
                            beam_data["quantities"]["length_lf"] = quantity.LengthValue * 3.281
                        elif quantity.is_a('IfcQuantityVolume'):
                            beam_data["quantities"]["volume_cf"] = quantity.VolumeValue * 35.315
        
        quantities["beams"].append(beam_data)
    
    # Update total count
    quantities["metadata"]["total_elements"] = (
        len(quantities["walls"]) +
        len(quantities["windows"]) +
        len(quantities["doors"]) +
        len(quantities["slabs"]) +
        len(quantities["roofs"]) +
        len(quantities["columns"]) +
        len(quantities["beams"])
    )
    
    return quantities


def convert_to_eagle_eye_format(ifc_quantities: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert IFC quantities to Eagle Eye parser-compatible format
    """
    eagle_eye_quantities = []
    
    # Convert walls
    for wall in ifc_quantities["walls"]:
        if "area_sf" in wall["quantities"]:
            eagle_eye_quantities.append({
                "schedule_type": "walls",
                "item_name": wall["name"],
                "item_type": wall["type"],
                "quantity": wall["quantities"]["area_sf"],
                "uom": "SF",
                "confidence": "High",
                "source": "IFC_Model",
                "ifc_guid": wall["ifc_guid"],
                "category": "Framing",
                "trade": "Carpentry",
                "wbs": "02.01"
            })
    
    # Convert windows
    for idx, window in enumerate(ifc_quantities["windows"], 1):
        eagle_eye_quantities.append({
            "schedule_type": "windows",
            "item_name": window["name"],
            "item_type": window["type"],
            "quantity": 1,
            "uom": "EA",
            "confidence": "High",
            "source": "IFC_Model",
            "ifc_guid": window["ifc_guid"],
            "category": "Windows",
            "trade": "Openings",
            "wbs": "04.01",
            "properties": window["properties"]
        })
    
    # Convert doors
    for idx, door in enumerate(ifc_quantities["doors"], 1):
        eagle_eye_quantities.append({
            "schedule_type": "doors",
            "item_name": door["name"],
            "item_type": door["type"],
            "quantity": 1,
            "uom": "EA",
            "confidence": "High",
            "source": "IFC_Model",
            "ifc_guid": door["ifc_guid"],
            "category": "Doors",
            "trade": "Openings",
            "wbs": "04.02"
        })
    
    # Convert slabs/roofs
    for slab in ifc_quantities["slabs"]:
        if "area_sf" in slab["quantities"]:
            eagle_eye_quantities.append({
                "schedule_type": "floors",
                "item_name": slab["name"],
                "item_type": slab["type"],
                "quantity": slab["quantities"]["area_sf"],
                "uom": "SF",
                "confidence": "High",
                "source": "IFC_Model",
                "ifc_guid": slab["ifc_guid"],
                "category": "Flooring",
                "trade": "Concrete",
                "wbs": "01.02"
            })
    
    for roof in ifc_quantities["roofs"]:
        if "area_sf" in roof["quantities"]:
            eagle_eye_quantities.append({
                "schedule_type": "roofs",
                "item_name": roof["name"],
                "item_type": roof["type"],
                "quantity": roof["quantities"]["area_sf"],
                "uom": "SF",
                "confidence": "High",
                "source": "IFC_Model",
                "ifc_guid": roof["ifc_guid"],
                "category": "Roofing",
                "trade": "Roofing",
                "wbs": "03.01"
            })
    
    return {
        "quantities": eagle_eye_quantities,
        "metadata": ifc_quantities["metadata"],
        "summary": {
            "total_items": len(eagle_eye_quantities),
            "walls": len(ifc_quantities["walls"]),
            "windows": len(ifc_quantities["windows"]),
            "doors": len(ifc_quantities["doors"]),
            "slabs": len(ifc_quantities["slabs"]),
            "roofs": len(ifc_quantities["roofs"])
        }
    }


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ifcopenshell-qto"})


@app.route('/qto', methods=['POST'])
def extract_qto():
    """
    Extract quantities from uploaded IFC file
    Expects multipart/form-data with 'file' field
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.ifc'):
        return jsonify({"error": "File must be .ifc format"}), 400
    
    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ifc') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        # Extract quantities
        ifc_quantities = extract_quantities_from_ifc(tmp_path)
        
        # Convert to Eagle Eye format
        eagle_eye_data = convert_to_eagle_eye_format(ifc_quantities)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return jsonify({
            "success": True,
            "data": eagle_eye_data
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/qto/raw', methods=['POST'])
def extract_qto_raw():
    """
    Extract raw IFC quantities (not converted to Eagle Eye format)
    Useful for debugging or custom processing
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if not file.filename.lower().endswith('.ifc'):
        return jsonify({"error": "File must be .ifc format"}), 400
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ifc') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        ifc_quantities = extract_quantities_from_ifc(tmp_path)
        
        os.unlink(tmp_path)
        
        return jsonify({
            "success": True,
            "data": ifc_quantities
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
