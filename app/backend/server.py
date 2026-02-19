from __future__ import annotations

import json
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from data_pipeline import DataPipeline

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
pipeline = DataPipeline()


def apply_filters(rows: list[dict], region: str | None, country: str | None, ta: str | None, indication: str | None):
    filtered = rows
    if region:
        filtered = [r for r in filtered if r["region"] == region]
    if country:
        filtered = [r for r in filtered if r["country"] == country]
    if ta:
        filtered = [r for r in filtered if r["therapeutic_area"] == ta]
    if indication:
        filtered = [r for r in filtered if r["indication_class"] == indication]
    return filtered


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            return self.serve_file(FRONTEND_DIR / "index.html", "text/html")
        if parsed.path.startswith("/static/"):
            file_path = FRONTEND_DIR / parsed.path.replace("/static/", "")
            return self.serve_static(file_path)
        if parsed.path == "/api/filters":
            return self.serve_filters()
        if parsed.path == "/api/enrollment":
            return self.serve_enrollment(parsed.query)

        self.send_response(404)
        self.end_headers()

    def serve_filters(self):
        rows = pipeline.load_or_refresh()["site_rows"]
        payload = {
            "regions": sorted(set(r["region"] for r in rows)),
            "countries": sorted(set(r["country"] for r in rows)),
            "therapeutic_areas": sorted(set(r["therapeutic_area"] for r in rows)),
            "indication_classes": sorted(set(r["indication_class"] for r in rows)),
        }
        self.send_json(payload)

    def serve_enrollment(self, query_string: str):
        query = parse_qs(query_string)
        region = query.get("region", [None])[0]
        country = query.get("country", [None])[0]
        ta = query.get("ta", [None])[0]
        indication = query.get("indication", [None])[0]

        data = pipeline.load_or_refresh()
        rows = apply_filters(data["site_rows"], region, country, ta, indication)

        planned = round(sum(r["planned_enrollment"] for r in rows), 2)
        actual = round(sum(r["actual_enrollment"] for r in rows), 2)

        by_country = defaultdict(lambda: {"planned": 0.0, "actual": 0.0})
        by_site = defaultdict(lambda: {"planned": 0.0, "actual": 0.0, "country": ""})

        for r in rows:
            by_country[r["country"]]["planned"] += r["planned_enrollment"]
            by_country[r["country"]]["actual"] += r["actual_enrollment"]
            by_site[r["site_name"]]["planned"] += r["planned_enrollment"]
            by_site[r["site_name"]]["actual"] += r["actual_enrollment"]
            by_site[r["site_name"]]["country"] = r["country"]

        country_rows = [
            {"country": c, "planned": round(v["planned"], 2), "actual": round(v["actual"], 2)}
            for c, v in by_country.items()
        ]
        site_rows = [
            {"site_name": s, "country": v["country"], "planned": round(v["planned"], 2), "actual": round(v["actual"], 2)}
            for s, v in by_site.items()
        ]

        country_rows.sort(key=lambda x: x["planned"], reverse=True)
        site_rows.sort(key=lambda x: x["planned"], reverse=True)

        payload = {
            "summary": {"planned": planned, "actual": actual},
            "by_country": country_rows[:50],
            "by_site": site_rows[:100],
            "source": data["source"],
            "generated_at": data["generated_at"],
        }
        self.send_json(payload)

    def serve_static(self, file_path: Path):
        if not file_path.exists() or not file_path.is_file():
            self.send_response(404)
            self.end_headers()
            return

        if file_path.suffix == ".js":
            ctype = "application/javascript"
        elif file_path.suffix == ".css":
            ctype = "text/css"
        else:
            ctype = "application/octet-stream"
        self.serve_file(file_path, ctype)

    def serve_file(self, file_path: Path, content_type: str):
        try:
            body = file_path.read_bytes()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host: str = "0.0.0.0", port: int = 8000):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Clinical trial analytics running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
