# Clinical Trial Operational Analytics MVP

This repository now includes an MVP website for clinical trial operational analytics.

## What it does

- Shows **planned vs actual enrollment** in a single bar chart.
- Supports filter dropdowns for:
  - WHO Region
  - Country
  - Therapeutic Area
  - Indication Class
- Provides site-level and country-level enrollment tables.
- Uses **ClinicalTrials.gov v2 API** as the primary public data source.
- Refreshes cached data every 24 hours.

## Tech stack

- Frontend: Single-page JavaScript (no external CDN dependencies)
- Backend: Python (standard library HTTP server)
- Deployment target: AWS-friendly (container/EC2 compatible)

## Run locally

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python backend/server.py
```

Then open: `http://localhost:8000`

## Notes on enrollment logic

Public sources generally do not provide full, reliable site-level actual enrollment. For this MVP:

- Study-level planned enrollment is distributed equally across sites in that study.
- Actual enrollment is estimated proportionally from planned with a status-based factor:
  - `COMPLETED` and `ACTIVE_NOT_RECRUITING`: 100%
  - Other statuses: 60%

This matches your requested proportional estimation approach and can be replaced later with richer source logic.
