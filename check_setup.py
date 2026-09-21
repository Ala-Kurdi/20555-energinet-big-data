from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = PROJECT_ROOT / "data" / "snapshot_manifest.json"
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def check_setup() -> list[str]:
    errors: list[str] = []
    if sys.version_info < (3, 11):
        errors.append(f"Python 3.11+ kræves; fundet {sys.version.split()[0]}.")

    try:
        import pandas as pd

        pandas_version = pd.__version__
    except ImportError:
        pandas_version = "MANGLER"
        errors.append("pandas mangler. Kør: python -m pip install -r requirements.txt")

    if not MANIFEST_PATH.exists():
        return errors + [f"Manifest mangler: {MANIFEST_PATH}"]
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for name, expected in manifest["files"].items():
        path = RAW_DIR / name
        if not path.exists():
            errors.append(f"Råfil mangler: {name}")
            continue
        if path.stat().st_size != expected["bytes"]:
            errors.append(f"Forkert filstørrelse: {name}")
        if sha256_file(path) != expected["sha256"].lower():
            errors.append(f"Checksum matcher ikke: {name}")
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "records" in payload and len(payload["records"]) != expected["rows"]:
            errors.append(f"Forkert rækkeantal: {name}")

    if not errors:
        print("SETUP PASS")
        print(f"- Python: {sys.version.split()[0]}")
        print(f"- pandas: {pandas_version}")
        print(f"- kontrollerede råfiler: {len(manifest['files'])}")
        print("- næste trin: læs OPGAVE.md og begynd ved TODO 1 i src/pipeline.py")
    return errors


def main() -> None:
    errors = check_setup()
    if errors:
        print("SETUP FEJLEDE")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
