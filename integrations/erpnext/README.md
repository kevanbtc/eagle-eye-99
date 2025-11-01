# ERPNext Integration for Eagle Eye

## Overview

ERPNext integration provides full CRM + estimating + job costing in a 100% open-source stack.

## Quick Start

### 1. Deploy ERPNext

```bash
# Using official Frappe Docker
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
cp example.env .env

# Edit .env to set ERPNEXT_VERSION=version-15

# Start containers
docker-compose -f compose.yaml \
  -f overrides/compose.noproxy.yaml \
  -f overrides/compose.erpnext.yaml \
  up -d

# Initialize site
docker-compose exec backend \
  bench new-site eagle.local \
  --admin-password admin \
  --db-name eagle_erp

# Install ERPNext
docker-compose exec backend \
  bench --site eagle.local install-app erpnext

# Enable Construction module
docker-compose exec backend \
  bench --site eagle.local set-config construction_enabled 1
```

### 2. Import Eagle Eye Custom Doctypes

```bash
# Copy custom doctypes
docker cp ./custom_doctypes backend:/home/frappe/frappe-bench/apps/erpnext/

# Import
docker-compose exec backend \
  bench --site eagle.local migrate
```

### 3. Configure API Access

1. Login to ERPNext at `http://localhost:8080`
2. Go to **Settings > API > Generate Keys**
3. Create API key for Eagle Eye integration
4. Set environment variables:

```bash
export ERPNEXT_URL=http://localhost:8080
export ERPNEXT_API_KEY=your_api_key
export ERPNEXT_API_SECRET=your_api_secret
```

## Custom Doctypes

### Eagle Eye Estimate

Extends ERPNext's native `Quotation` doctype with construction-specific fields:

**Fields:**
- `eagle_project_id` (Link to Eagle Eye project)
- `code_review_status` (Draft, Reviewed, Approved)
- `findings_count` (Int)
- `risk_level` (Red, Orange, Yellow, Green)
- `spec_tier` (Standard, Premium, Luxury)
- `regional_factor` (Decimal)
- `confidence_score` (Percent)

**Child Table: Estimate Lines**
- Standard ERPNext quotation items
- Additional: `qty_confidence`, `needs_rfi`, `finding_codes`

### Eagle Eye Finding

Custom doctype to store code compliance findings:

**Fields:**
- `project` (Link)
- `finding_code` (e.g., RR-103)
- `severity` (Red, Orange, Yellow)
- `discipline` (Structural, Envelope, etc.)
- `code_citation` (IRC 2018 R602.10)
- `consequence` (Long Text)
- `fix` (Long Text)
- `ve_alt` (Long Text)
- `submittal_needed` (Text)
- `status` (Open, Resolved, Deferred)

### Eagle Eye Submittal

Tracks required vendor submittals:

**Fields:**
- `project` (Link)
- `finding_id` (Link to Finding)
- `submittal_type` (Truss Calcs, PE Stamp, Product Data)
- `vendor` (Link to Supplier)
- `due_date` (Date)
- `submitted_date` (Date)
- `approved_date` (Date)
- `status` (Needed, Submitted, Approved, Rejected)
- `attachment` (File)

## API Integration

### Sync ERPNext → Eagle Eye

```python
# Fetch ERPNext quotation
import requests

response = requests.get(
    f"{ERPNEXT_URL}/api/resource/Quotation/{quotation_id}",
    headers={
        "Authorization": f"token {API_KEY}:{API_SECRET}"
    }
)
quotation = response.json()['data']

# Push to Eagle Eye for code review
eagle_response = requests.post(
    f"{EAGLE_API_URL}/api/estimates/process",
    json={
        "project_id": quotation['eagle_project_id'],
        "quantities": quotation['items'],
        "spec_tier": quotation['spec_tier']
    }
)

# Update ERPNext with findings
findings = eagle_response.json()['findings']
for finding in findings:
    requests.post(
        f"{ERPNEXT_URL}/api/resource/Eagle Eye Finding",
        headers={"Authorization": f"token {API_KEY}:{API_SECRET}"},
        json={
            "project": quotation['eagle_project_id'],
            "finding_code": finding['finding_code'],
            "severity": finding['severity'],
            # ... other fields
        }
    )
```

### Sync Eagle Eye → ERPNext

```python
# Create quotation from Eagle Eye estimate
estimate = requests.get(f"{EAGLE_API_URL}/api/estimates/{project_id}").json()

quotation_data = {
    "doctype": "Quotation",
    "party_name": estimate['account']['name'],
    "eagle_project_id": project_id,
    "spec_tier": estimate['project']['spec_tier'],
    "items": [
        {
            "item_code": item['assembly'],
            "item_name": item['line_item'],
            "qty": item['qty'],
            "rate": item['unit_cost'],
            "qty_confidence": item['qty_confidence'],
        }
        for trade_items in estimate['base'].values()
        for item in trade_items
    ]
}

response = requests.post(
    f"{ERPNEXT_URL}/api/resource/Quotation",
    headers={"Authorization": f"token {API_KEY}:{API_SECRET}"},
    json=quotation_data
)
```

## Workflow Integration

### n8n Workflow: ERPNext ↔ Eagle Eye

1. **Trigger**: ERPNext webhook on Quotation save
2. **Extract**: Fetch quotation items via API
3. **Transform**: Convert to Eagle Eye quantities format
4. **Process**: POST to Eagle Eye `/api/estimates/process`
5. **Code Review**: Rules engine runs IRC/IECC/NEC checks
6. **Pricing**: Apply regional factors + spec tiers
7. **Findings**: Create ERPNext "Eagle Eye Finding" records
8. **Update**: Update quotation with adjusted pricing
9. **Report**: Generate proposal PDF, attach to quotation
10. **Notify**: Email PM with review results

See: `../../workflows/n8n/erpnext-eagle-sync.json`

## Report Templates

ERPNext Print Formats can use Eagle Eye data:

### Custom Print Format: Eagle Eye Proposal

**Jinja Template:**
```jinja
{% raw %}
<!-- Fetch Eagle Eye findings for this quotation -->
{% set findings = frappe.get_all(
    'Eagle Eye Finding',
    filters={'project': doc.eagle_project_id},
    fields=['finding_code', 'severity', 'code_citation', 'consequence', 'fix']
) %}

<h2>Code Compliance Review</h2>
<table>
  <tr>
    <th>Code</th>
    <th>Severity</th>
    <th>Citation</th>
    <th>Fix</th>
  </tr>
  {% for finding in findings %}
  <tr class="severity-{{ finding.severity|lower }}">
    <td>{{ finding.finding_code }}</td>
    <td>{{ finding.severity }}</td>
    <td>{{ finding.code_citation }}</td>
    <td>{{ finding.fix[:100] }}...</td>
  </tr>
  {% endfor %}
</table>
{% endraw %}
```

## Advantages of ERPNext Integration

✅ **Fully Open Source** - No proprietary licenses, full code access
✅ **CRM Built-In** - Contacts, opportunities, quotes in one place
✅ **Job Costing** - Track actuals vs estimates during construction
✅ **Accounting** - GL, AP, AR integration for draws/billing
✅ **Extensible** - Python/JS customization, extensive API
✅ **Mobile** - Native mobile app for field updates
✅ **Multi-Company** - Support multiple GC entities in one instance

## Development

### Testing Locally

```bash
# Start ERPNext
cd frappe_docker && docker-compose up -d

# Install Eagle Eye custom app
docker-compose exec backend bash
cd /home/frappe/frappe-bench/apps
bench get-app eagle_eye https://github.com/your-org/eagle_eye_erpnext
bench --site eagle.local install-app eagle_eye

# Run tests
bench --site eagle.local run-tests --app eagle_eye
```

### Custom App Structure

```
eagle_eye_erpnext/
├── eagle_eye/
│   ├── eagle_eye/
│   │   ├── doctype/
│   │   │   ├── eagle_eye_estimate/
│   │   │   ├── eagle_eye_finding/
│   │   │   └── eagle_eye_submittal/
│   │   ├── api/
│   │   │   └── eagle_sync.py
│   │   └── hooks.py
│   └── public/
│       └── js/
│           └── eagle_eye.bundle.js
└── setup.py
```

## Resources

- [ERPNext Documentation](https://docs.erpnext.com/)
- [Frappe Framework Guide](https://frappeframework.com/docs)
- [Construction Module](https://erpnext.com/industries/construction)
- [API Reference](https://frappeframework.com/docs/user/en/api)
