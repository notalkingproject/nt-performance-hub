"""Lightweight diagnostics for NT Performance Hub."""
from __future__ import annotations

import argparse
import ast
import json
import time
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["app.py", "web/index.html", "web/app.js", "web/styles.css", "web/generative.js", "requirements.txt"]


def check_files() -> list[str]:
    lines = []
    for rel in REQUIRED:
        path = ROOT / rel
        status = "ok" if path.exists() else "missing"
        size = path.stat().st_size if path.exists() else 0
        lines.append(f"{rel}: {status} ({size:,} bytes)")
    return lines


def check_python_syntax() -> str:
    ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
    return "app.py syntax: ok"


def fetch_json(url: str, timeout: float = 2.0) -> tuple[float, dict]:
    start = time.perf_counter()
    with urlopen(url, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return (time.perf_counter() - start) * 1000, payload


def check_server(base_url: str) -> list[str]:
    base = base_url.rstrip("/")
    checks = []
    health_ms, health = fetch_json(f"{base}/health")
    checks.append(f"/health: {health_ms:.1f} ms ok={health.get('ok')}")
    status_ms, status = fetch_json(f"{base}/api/status?settings=0&blt=0")
    checks.append(f"/api/status light: {status_ms:.1f} ms app_id={status.get('version')} settings={'settings' in status} blt_cached={status.get('blt', {}).get('cached')}")
    full_ms, full = fetch_json(f"{base}/api/status?settings=1&blt=0")
    checks.append(f"/api/status full-no-blt: {full_ms:.1f} ms settings={'settings' in full} presets={len(full.get('presets', []))}")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run portable app diagnostics.")
    parser.add_argument("--url", default="", help="Optional running app URL, for example http://127.0.0.1:8080")
    args = parser.parse_args()
    print("NT Performance Hub diagnostics")
    print(f"root: {ROOT}")
    for line in check_files():
        print(line)
    print(check_python_syntax())
    if args.url:
        for line in check_server(args.url):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())