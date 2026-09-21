from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from check_setup import check_setup, sha256_file  # noqa: E402
from pipeline import load_records  # noqa: E402


class StarterSetupTests(unittest.TestCase):
    def test_setup_and_all_checksums(self) -> None:
        self.assertEqual(check_setup(), [])

    def test_manifest_period_row_counts_match_payloads(self) -> None:
        manifest = json.loads(
            (PROJECT_ROOT / "data" / "snapshot_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        raw_dir = PROJECT_ROOT / "data" / "raw"
        for period in manifest["periods"].values():
            realtime = load_records(
                raw_dir / period["realtime_file"],
                "ElectricityProdex5MinRealtime",
            )
            settlement = load_records(
                raw_dir / period["settlement_file"],
                "ProductionConsumptionSettlement",
            )
            self.assertEqual(len(realtime), period["realtime_rows"])
            self.assertEqual(len(settlement), period["settlement_rows"])

    def test_raw_files_are_unchanged(self) -> None:
        manifest = json.loads(
            (PROJECT_ROOT / "data" / "snapshot_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        raw_dir = PROJECT_ROOT / "data" / "raw"
        for name, expected in manifest["files"].items():
            self.assertEqual(sha256_file(raw_dir / name), expected["sha256"].lower())


if __name__ == "__main__":
    unittest.main()
