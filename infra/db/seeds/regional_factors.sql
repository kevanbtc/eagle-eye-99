-- ============================================================================
-- REGIONAL FACTORS SEED DATA
-- Load this after schema.sql
-- ============================================================================

INSERT INTO regional_factors (zip_code, city, state, region, labor_rate_multiplier, material_cost_index, permitting_cost, permitting_days, snow_load, wind_speed, seismic_zone) VALUES
-- Georgia
('30601', 'Madison', 'GA', 'Southeast', 0.92, 0.95, 850, 14, 10, 100, 0),
('30601', 'Athens', 'GA', 'Southeast', 0.90, 0.93, 750, 12, 10, 100, 0),
('30301', 'Atlanta', 'GA', 'Southeast', 0.95, 0.97, 950, 16, 10, 105, 0),
('31401', 'Savannah', 'GA', 'Southeast', 0.88, 0.92, 800, 14, 5, 95, 0),
-- Florida  
('33101', 'Miami', 'FL', 'Southeast', 1.10, 1.05, 1200, 20, 0, 120, 1),
('32801', 'Orlando', 'FL', 'Southeast', 1.05, 1.02, 1000, 18, 0, 110, 0),
-- North Carolina
('27601', 'Raleigh', 'NC', 'Southeast', 0.93, 0.94, 800, 14, 15, 105, 0),
('28202', 'Charlotte', 'NC', 'Southeast', 0.94, 0.95, 850, 15, 12, 100, 0),
-- South Carolina
('29401', 'Charleston', 'SC', 'Southeast', 0.91, 0.93, 750, 13, 8, 105, 0),
('29215', 'Columbia', 'SC', 'Southeast', 0.89, 0.92, 700, 12, 10, 100, 0),
-- Virginia
('23219', 'Richmond', 'VA', 'Northeast', 0.98, 0.97, 900, 15, 20, 95, 1),
('22201', 'Arlington', 'VA', 'Northeast', 1.15, 1.08, 1500, 20, 20, 100, 1),
-- New York
('10001', 'New York City', 'NY', 'Northeast', 1.45, 1.25, 2500, 25, 40, 90, 3),
('14201', 'Buffalo', 'NY', 'Northeast', 1.05, 0.99, 1100, 17, 90, 85, 2),
-- California
('90001', 'Los Angeles', 'CA', 'West', 1.35, 1.18, 1800, 22, 0, 75, 4),
('94102', 'San Francisco', 'CA', 'West', 1.55, 1.30, 2200, 25, 0, 65, 4),
('92101', 'San Diego', 'CA', 'West', 1.28, 1.15, 1700, 21, 0, 70, 4),
('90210', 'Los Angeles', 'CA', 'West', 1.32, 1.17, 1750, 21, 0, 75, 4),
-- Texas
('75201', 'Dallas', 'TX', 'South', 0.85, 0.88, 600, 10, 10, 100, 1),
('77001', 'Houston', 'TX', 'South', 0.83, 0.87, 550, 9, 0, 105, 0),
('78201', 'San Antonio', 'TX', 'South', 0.82, 0.86, 500, 8, 0, 110, 0),
-- Colorado
('80202', 'Denver', 'CO', 'Mountain', 1.05, 1.02, 1100, 16, 80, 75, 2),
('80401', 'Boulder', 'CO', 'Mountain', 1.08, 1.04, 1200, 17, 120, 70, 2),
-- Illinois
('60601', 'Chicago', 'IL', 'Midwest', 1.12, 1.08, 1400, 18, 60, 85, 2),
-- Minnesota
('55401', 'Minneapolis', 'MN', 'Midwest', 1.02, 1.00, 950, 15, 100, 80, 1),
-- Washington
('98101', 'Seattle', 'WA', 'West', 1.18, 1.10, 1300, 19, 50, 60, 3),
('98121', 'Seattle', 'WA', 'West', 1.18, 1.10, 1300, 19, 50, 60, 3),
-- Oregon
('97201', 'Portland', 'OR', 'West', 1.12, 1.06, 1150, 17, 40, 65, 3),
-- Massachusetts
('02101', 'Boston', 'MA', 'Northeast', 1.28, 1.15, 1800, 21, 70, 80, 2),
-- Ohio
('43085', 'Columbus', 'OH', 'Midwest', 0.90, 0.92, 700, 12, 30, 85, 1);

-- ============================================================================
-- RULES DEFINITIONS SEED DATA
-- ============================================================================

INSERT INTO rule_definitions (rule_id, code, section, title, description, applies_to_components, severity, base_cost_to_fix, fix_message, jurisdiction, active) VALUES
-- IECC Energy Code
('IECC-2015-C402.3.6', 'IECC 2015', 'C402.3.6', 'HVAC System Efficiency', 'HVAC systems must meet minimum SEER rating for cooling and HSPF for heating', ARRAY['HVAC System', 'Air Conditioning', 'Heat Pump'], 'RED', 1500, 'Upgrade HVAC to SEER 14+ rated unit', 'GA', true),
('IECC-2015-C402.4', 'IECC 2015', 'C402.4', 'Air Sealing & Thermal Breaks', 'Continuous air barrier required at building envelope', ARRAY['Exterior Walls', 'Roofing', 'Windows', 'Doors'], 'ORANGE', 1200, 'Install house wrap or continuous air barrier', 'GA', true),
('IECC-2015-C402.2', 'IECC 2015', 'C402.2', 'Insulation Requirements', 'Walls, roofs, and foundations must meet R-value requirements', ARRAY['Insulation', 'Exterior Walls', 'Roofing'], 'ORANGE', 2000, 'Add insulation to meet minimum R-value requirements', 'GA', true),
-- IRC Structural
('IRC-2018-R402.1', 'IRC 2018', 'R402.1', 'Exterior Walls', 'Exterior walls must be properly framed and braced', ARRAY['Exterior Walls', 'Framing'], 'RED', 3000, 'Add proper bracing and structural support', 'GA', true),
('IRC-2018-R606', 'IRC 2018', 'R606', 'Masonry Construction', 'Masonry walls must be reinforced per code', ARRAY['Masonry', 'Brick', 'Concrete Block'], 'RED', 5000, 'Add reinforcement to masonry walls', 'GA', true),
-- NEC Electrical
('NEC-2017-210.52', 'NEC 2017', '210.52', 'Receptacle Outlets - General', 'GFCI protection required for kitchen and bathroom receptacles', ARRAY['Electrical', 'Receptacles', 'Outlets'], 'RED', 150, 'Install GFCI-protected receptacles', 'GA', true),
('NEC-2017-215', 'NEC 2017', '215', 'Feeders', 'Feeder conductors must be properly sized', ARRAY['Electrical', 'Feeder', 'Wiring'], 'RED', 800, 'Upgrade feeder conductors to proper size', 'GA', true),
('NEC-2017-225', 'NEC 2017', '225', 'Outside Branch Circuits and Feeders', 'Outside circuits must be GFCI and disconnect switches installed', ARRAY['Electrical', 'Exterior Circuits'], 'ORANGE', 400, 'Add GFCI protection and disconnect switch', 'GA', true),
-- Roof & Water Management
('IRC-2018-R905', 'IRC 2018', 'R905', 'Roof Assemblies and Rooftop Structures', 'Roofing must be properly installed per manufacturer specs', ARRAY['Roofing', 'Roof'], 'ORANGE', 2500, 'Replace or repair roof per manufacturer specifications', 'GA', true),
('IRC-2018-R703.2', 'IRC 2018', 'R703.2', 'Weather Protection', 'All exterior surfaces must be weather-resistant', ARRAY['Exterior Walls', 'Windows', 'Doors', 'Roofing'], 'ORANGE', 1500, 'Add weather protection (flashing, sealant, etc.)', 'GA', true),
-- Accessibility
('ADA-2010-203', 'ADA 2010', '203', 'General Accessibility Requirements', 'Common use circulation paths must be accessible', ARRAY['Doors', 'Stairs', 'Ramps'], 'YELLOW', 3000, 'Add accessibility features (ramps, wider doors, etc.)', 'GA', true),
-- Window & Door
('IRC-2018-R612', 'IRC 2018', 'R612', 'Interior Glazed Surfaces', 'Glazing near doors must be tempered or laminated', ARRAY['Windows', 'Doors', 'Glass'], 'ORANGE', 500, 'Replace with tempered or laminated glass', 'GA', true),
-- HVAC specific
('IECC-2015-C403.2', 'IECC 2015', 'C403.2', 'HVAC Controls', 'HVAC systems require proper controls and thermostats', ARRAY['HVAC System', 'Thermostat'], 'YELLOW', 400, 'Upgrade to programmable thermostat with proper controls', 'GA', true),
-- Water & Plumbing
('IRC-2018-P2601', 'IRC 2018', 'P2601', 'General', 'Plumbing materials must meet code standards', ARRAY['Plumbing', 'Pipes', 'Water Lines'], 'ORANGE', 1000, 'Replace with code-compliant plumbing materials', 'GA', true);

-- Add jurisdiction-specific amendments for Georgia
INSERT INTO rule_definitions (rule_id, code, section, title, description, applies_to_components, severity, base_cost_to_fix, fix_message, jurisdiction, active) VALUES
('GA-AMEND-FLOOD', 'Georgia', 'Flood Regulations', 'Flood Zone Requirements', 'Properties in flood zones must meet special requirements', ARRAY['Foundation', 'Electrical', 'HVAC'], 'RED', 2000, 'Elevate utilities and add flood protection measures', 'GA', true),
('GA-AMEND-SLOPE', 'Georgia', 'Slope Stability', 'Grading on Slopes > 20%', 'Special grading and drainage required on steep slopes', ARRAY['Foundation', 'Grading'], 'ORANGE', 1500, 'Add proper grading and drainage for slope', 'GA', true),
('GA-AMEND-TREE', 'Georgia', 'Tree Preservation', 'Protected Trees', 'Certain trees must be preserved during construction', ARRAY['Site', 'Landscape'], 'YELLOW', 500, 'Preserve protected trees or plant replacements', 'GA', true);
