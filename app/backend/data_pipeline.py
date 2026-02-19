from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen

from ta_mapping import map_indication_class, map_therapeutic_area
from who_regions import country_to_who_region

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_FILE = DATA_DIR / "site_enrollment_cache.json"
META_FILE = DATA_DIR / "cache_meta.json"
CTGOV_ENDPOINT = "https://clinicaltrials.gov/api/v2/studies"


class DataPipeline:
    def __init__(self, max_studies: int = 1200):
        self.max_studies = max_studies
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def cache_is_fresh(self) -> bool:
        if not META_FILE.exists():
            return False
        meta = json.loads(META_FILE.read_text())
        updated = datetime.fromisoformat(meta["last_updated"])
        return datetime.now(timezone.utc) - updated < timedelta(days=1)

    def load_or_refresh(self) -> dict[str, Any]:
        if CACHE_FILE.exists() and self.cache_is_fresh():
            return json.loads(CACHE_FILE.read_text())
        try:
            data = self.fetch_and_transform()
        except Exception:
            data = self.load_fallback_sample()
        CACHE_FILE.write_text(json.dumps(data))
        META_FILE.write_text(json.dumps({"last_updated": datetime.now(timezone.utc).isoformat()}))
        return data


    def load_fallback_sample(self) -> dict[str, Any]:
        sample_file = DATA_DIR / "sample_site_rows.json"
        return json.loads(sample_file.read_text())

    def fetch_and_transform(self) -> dict[str, Any]:
        studies = self.fetch_studies()
        site_rows = []

        for study in studies:
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            conditions_mod = protocol.get("conditionsModule", {})
            contacts_mod = protocol.get("contactsLocationsModule", {})
            design_mod = protocol.get("designModule", {})

            nct_id = ident.get("nctId", "Unknown")
            conditions = conditions_mod.get("conditions", [])
            locations = contacts_mod.get("locations", [])
            enrollment_info = design_mod.get("enrollmentInfo", {})

            planned = enrollment_info.get("count") or 0
            overall_status = status.get("overallStatus", "UNKNOWN")

            site_count = len(locations)
            if site_count == 0:
                continue

            site_planned = planned / site_count if planned else 0
            completion_factor = 1.0 if overall_status in {"COMPLETED", "ACTIVE_NOT_RECRUITING"} else 0.6
            site_actual = site_planned * completion_factor

            ta = map_therapeutic_area(conditions)
            indication_class = map_indication_class(conditions)

            for loc in locations:
                country = loc.get("country", "Unknown")
                facility = loc.get("facility", "Unknown Site")
                region = country_to_who_region(country)

                site_rows.append(
                    {
                        "nct_id": nct_id,
                        "site_name": facility,
                        "country": country,
                        "region": region,
                        "therapeutic_area": ta,
                        "indication_class": indication_class,
                        "planned_enrollment": round(site_planned, 2),
                        "actual_enrollment": round(site_actual, 2),
                    }
                )

        return {
            "site_rows": site_rows,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": ["ClinicalTrials.gov v2 API"],
        }

    def fetch_studies(self) -> list[dict[str, Any]]:
        studies: list[dict[str, Any]] = []
        page_token = None

        while len(studies) < self.max_studies:
            params = {"pageSize": 100, "format": "json", "countTotal": "true"}
            if page_token:
                params["pageToken"] = page_token
            url = f"{CTGOV_ENDPOINT}?{urlencode(params)}"

            with urlopen(url, timeout=60) as response:  # noqa: S310
                payload = json.loads(response.read().decode("utf-8"))

            batch = payload.get("studies", [])
            if not batch:
                break

            studies.extend(batch)
            page_token = payload.get("nextPageToken")
            if not page_token:
                break

        return studies[: self.max_studies]
