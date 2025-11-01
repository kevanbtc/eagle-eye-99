-- Spec Tier Bundles - Finish Preference Profiles
-- Standard, Premium, Luxury specifications for regional pricing

-- Roofing Specifications
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Roofing', 'Architectural Shingle - 30yr', 'Standard architectural shingle, 30-year warranty, basic color selection', 3.25, 'SF', '{"brands": ["GAF Timberline HD", "Owens Corning Duration"], "warranty": "30-year"}'),
('Premium', 'Roofing', 'Designer Shingle - 50yr', 'Premium designer shingle with enhanced wind/impact rating, expanded color palette', 4.75, 'SF', '{"brands": ["GAF Timberline HDZ", "CertainTeed Landmark Pro"], "warranty": "50-year", "wind_rating": "130 mph"}'),
('Luxury', 'Roofing', 'Standing Seam Metal', 'Standing seam metal roof, concealed fasteners, 24ga steel or aluminum', 12.50, 'SF', '{"brands": ["Custom fabricated", "MBCI"], "warranty": "Lifetime", "colors": "Custom Kynar finish"}'),
('Luxury', 'Roofing', 'Clay/Concrete Tile', 'Clay or concrete tile roofing system with underlayment and battens', 15.00, 'SF', '{"brands": ["Boral", "Eagle Roofing"], "warranty": "50-year", "weight": "8-12 psf"}');

-- Window Specifications
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Windows', 'Vinyl Window - Energy Star', 'Vinyl window, Energy Star rated, white or tan, single-hung or casement', 385, 'EA', '{"brands": ["Simonton", "American Craftsman"], "u_factor": "0.30", "shgc": "0.28"}'),
('Premium', 'Windows', 'Fiberglass Window - Low-E', 'Fiberglass or aluminum-clad wood, Low-E glass, color options', 625, 'EA', '{"brands": ["Marvin Essential", "Andersen 400 Series"], "u_factor": "0.28", "shgc": "0.26", "colors": "6 standard"}'),
('Luxury', 'Windows', 'Wood-Clad Premium - Impact', 'Premium wood-clad window, impact-rated glass, custom colors, hardware upgrades', 1150, 'EA', '{"brands": ["Marvin Ultimate", "Pella Architect Series"], "u_factor": "0.25", "shgc": "0.24", "colors": "Custom", "impact_rated": true}');

-- Exterior Doors
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Doors', 'Fiberglass Entry Door', 'Fiberglass entry door, standard glass, brushed nickel hardware', 1250, 'EA', '{"brands": ["Therma-Tru", "Masonite"], "finish": "Smooth or woodgrain", "glass": "Standard decorative"}'),
('Premium', 'Doors', 'Wood Entry Door - Stained', 'Solid wood or wood veneer entry door, stained finish, upgraded hardware', 2400, 'EA', '{"brands": ["Simpson", "Jeld-Wen Custom Wood"], "finish": "Custom stain", "glass": "Decorative or sidelites"}'),
('Luxury', 'Doors', 'Custom Mahogany Entry', 'Custom mahogany entry door system with sidelites and transom, premium hardware', 4800, 'EA', '{"brands": ["Custom fabrication", "Simpson Mastermark"], "finish": "Hand-rubbed", "glass": "Beveled or art glass"}');

-- Flooring Specifications
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Flooring', 'Carpet - Nylon', 'Nylon carpet, builder-grade pad, standard colors', 3.50, 'SF', '{"brands": ["Mohawk", "Shaw"], "pile": "Cut pile or frieze", "warranty": "10-year"}'),
('Standard', 'Flooring', 'Luxury Vinyl Plank', 'Luxury vinyl plank (LVP), waterproof, wood-look, click-lock install', 4.25, 'SF', '{"brands": ["LifeProof", "CoreLuxe"], "thickness": "5-6mm", "warranty": "Lifetime residential"}'),
('Premium', 'Flooring', 'Engineered Hardwood', 'Engineered hardwood, 5\" planks, site-finished or prefinished', 8.50, 'SF', '{"brands": ["Bruce", "Somerset"], "species": "Oak, Maple, Hickory", "finish": "Multiple stain options"}'),
('Luxury', 'Flooring', 'Solid Hardwood - Wide Plank', 'Solid hardwood, 6-8\" wide planks, site-finished with custom stain', 14.00, 'SF', '{"brands": ["Custom millwork", "Carlisle"], "species": "White Oak, Walnut, Cherry", "finish": "Hand-scraped or smooth"}'),
('Luxury', 'Flooring', 'Large Format Tile', 'Large format porcelain tile, 24x48 or larger, rectified edges', 11.50, 'SF', '{"brands": ["Daltile", "Emser"], "finish": "Polished or matte", "patterns": "Book-matched available"}');

-- Cabinet Specifications
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Cabinets', 'Semi-Custom Painted', 'Semi-custom cabinets, painted finish, soft-close hinges, limited door styles', 185, 'LF', '{"brands": ["KraftMaid", "Diamond NOW"], "finish": "White or gray", "door_styles": "Shaker, recessed panel"}'),
('Premium', 'Cabinets', 'Custom Stained', 'Custom cabinets, stained wood finish, soft-close drawers, expanded door styles', 295, 'LF', '{"brands": ["Wellborn", "Ultracraft"], "finish": "Cherry, Maple, Oak", "door_styles": "10+ options", "hardware": "Upgraded pulls"}'),
('Luxury', 'Cabinets', 'Full Custom Premium', 'Full custom cabinetry, premium wood species, inset doors, custom finish', 485, 'LF', '{"brands": ["Custom cabinet shop", "Dura Supreme"], "finish": "Hand-rubbed or glazed", "door_styles": "Unlimited", "hardware": "Premium designer", "features": "Soft-close all, organizers"}');

-- Countertop Specifications
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Countertops', 'Laminate or Basic Quartz', 'Laminate countertop or basic quartz, standard edge, limited color selection', 42, 'SF', '{"brands": ["Formica", "MSI Q-Quartz"], "edge": "Eased or beveled", "thickness": "Standard"}'),
('Premium', 'Countertops', 'Mid-Grade Quartz/Granite', 'Mid-grade quartz or granite, upgraded edge, expanded color palette', 68, 'SF', '{"brands": ["Cambria", "Level 3 Granite"], "edge": "Bullnose or ogee", "thickness": "3cm"}'),
('Luxury', 'Countertops', 'Premium Stone - Waterfall', 'Premium quartz, quartzite, or exotic granite with waterfall edge details', 125, 'SF', '{"brands": ["Cambria premium", "Exotic granite"], "edge": "Mitered waterfall", "thickness": "3cm", "features": "Book-matched slabs"}');

-- Plumbing Fixtures
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Fixtures', 'Builder-Grade Faucets', 'Builder-grade faucets and fixtures, chrome or brushed nickel finish', 145, 'EA', '{"brands": ["Delta Foundations", "Kohler Devonshire"], "finish": "Chrome or brushed nickel"}'),
('Premium', 'Fixtures', 'Mid-Range Designer', 'Mid-range designer faucets, expanded finish options, upgraded features', 285, 'EA', '{"brands": ["Kohler", "Moen Arbor"], "finish": "Multiple finishes", "features": "Pulldown spray, touchless"}'),
('Luxury', 'Fixtures', 'Luxury Brands - Premium', 'Luxury brand fixtures with premium finishes and advanced features', 625, 'EA', '{"brands": ["Brizo", "Grohe", "Hansgrohe"], "finish": "Custom finishes", "features": "Thermostatic, digital controls"}');

-- Light Fixtures
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Lighting', 'Builder-Grade Fixtures', 'Builder-grade light fixtures, basic styles, standard finishes', 85, 'EA', '{"brands": ["Home Depot Commercial Electric", "Lithonia"], "finish": "Brushed nickel, bronze"}'),
('Premium', 'Lighting', 'Designer Fixtures', 'Designer light fixtures, transitional styles, upgraded finishes', 195, 'EA', '{"brands": ["Kichler", "Progress Lighting"], "finish": "Multiple finishes", "styles": "Transitional, contemporary"}'),
('Luxury', 'Lighting', 'Luxury Chandeliers/Pendants', 'Luxury light fixtures, custom designs, premium finishes', 485, 'EA', '{"brands": ["Visual Comfort", "Hudson Valley"], "finish": "Custom finishes", "styles": "Statement pieces"}');

-- HVAC Equipment
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'HVAC', 'Standard Efficiency - 14 SEER', 'Standard efficiency HVAC system, 14 SEER AC, 80% AFUE furnace', 4200, 'SYS', '{"brands": ["Goodman", "American Standard"], "seer": "14", "afue": "80%", "warranty": "10-year parts"}'),
('Premium', 'HVAC', 'High Efficiency - 16 SEER', 'High efficiency HVAC, 16 SEER AC, 95% AFUE furnace, zoning capability', 6500, 'SYS', '{"brands": ["Carrier Infinity", "Trane XL"], "seer": "16", "afue": "95%", "warranty": "10-year parts", "features": "Zoning, smart thermostat"}'),
('Luxury', 'HVAC', 'Premium Efficiency - 18+ SEER', 'Premium HVAC system, 18+ SEER variable-speed, geothermal option', 9800, 'SYS', '{"brands": ["Carrier Greenspeed", "Lennox Signature"], "seer": "18-20", "afue": "98%", "warranty": "12-year parts", "features": "Variable speed, multi-zone, air purification"}');

-- Appliance Packages
INSERT INTO spec_tier_bundles (tier, category, item_name, description, unit_cost_base, uom, metadata) VALUES
('Standard', 'Appliances', 'Builder Package', 'Builder-grade appliance package: range, microwave, dishwasher, refrigerator', 2800, 'PKG', '{"brands": ["GE", "Whirlpool"], "finish": "Stainless or black", "features": "Basic"}'),
('Premium', 'Appliances', 'Mid-Grade Package', 'Mid-grade appliance package with upgraded features and finishes', 5200, 'PKG', '{"brands": ["KitchenAid", "Bosch"], "finish": "Stainless steel", "features": "Convection oven, quiet dishwasher"}'),
('Luxury', 'Appliances', 'Luxury Package', 'Luxury appliance package with pro-style range and premium finishes', 12500, 'PKG', '{"brands": ["Wolf", "Sub-Zero", "Miele"], "finish": "Stainless, custom panels", "features": "Pro range, built-in refrigeration, wine cooler"}');

-- Regional Cost Multiplier Examples (to be combined with spec tiers)
-- These would be used to adjust base costs based on location
INSERT INTO regional_factors (region_type, region_code, region_name, labor_multiplier, material_multiplier, metadata) VALUES
('CBSA', '12060', 'Atlanta-Sandy Springs-Roswell, GA', 1.08, 1.02, '{"counties": ["Fulton", "DeKalb", "Gwinnett", "Cobb"], "notes": "Metro Atlanta area"}'),
('CBSA', '31420', 'Macon-Bibb County, GA', 0.92, 0.98, '{"counties": ["Bibb"], "notes": "Central Georgia"}'),
('CBSA', '46660', 'Valdosta, GA', 0.88, 0.96, '{"counties": ["Lowndes"], "notes": "South Georgia"}'),
('ZIP', '30301', 'Atlanta Downtown', 1.15, 1.05, '{"cbsa": "12060", "notes": "Downtown premium"}'),
('ZIP', '30350', 'Sandy Springs/Dunwoody', 1.12, 1.04, '{"cbsa": "12060", "notes": "North Atlanta suburbs"}'),
('ZIP', '30518', 'Buford/Lake Lanier', 1.06, 1.01, '{"cbsa": "12060", "notes": "Northeast suburbs"}');
