# eagle_eye_estimator (Frappe app)

Glue + pro features to turn ERPNext into an Xactimate-class estimator while keeping deterministic rules and AI sidecars separate.

## What’s inside
- Core DocTypes (Assembly, Assembly Item, Rate Catalogue, Vendor Quote, Takeoff Package, Estimate v2, OH&P Policy, Risk Register, Xactimate Map)
- CSV importer stub for catalogs (GEstimator/PrecisionEstimator)
- Proposal print format for Estimate v2 (fixtures)

## Install (into an existing bench)

1) Copy this folder into your bench/apps:

```bash
# from your bench root
cp -r /path/to/eagle_eye_estimator apps/eagle_eye_estimator
```

2) Install the app:

```bash
bench --site <yoursite> install-app eagle_eye_estimator
```

3) (Optional) Load fixtures after install:

```bash
bench --site <yoursite> execute eagle_eye_estimator.utils.importers.load_sample_fixtures
```

## Dev notes
- Keep AI and proprietary pricing catalogs in separate microservices (HTTP) to avoid GPL coupling.
- This app ships minimal DocType JSON; tailor fields as your team standardizes.
