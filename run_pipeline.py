from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from contracts import PERIODS  # noqa: E402
from pipeline import NextTodo, run_period  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Kør din Energinet-pipeline.")
    parser.add_argument(
        "--period",
        choices=sorted(PERIODS),
        default="dst",
        help="Start med dst, som er det mindste snapshot.",
    )
    args = parser.parse_args()
    try:
        csv_path, quality_path = run_period(args.period)
    except NextTodo as error:
        raise SystemExit(str(error)) from error
    print("PIPELINE PASS")
    print(f"- analyseoutput: {csv_path}")
    print(f"- kvalitetsrapport: {quality_path}")


if __name__ == "__main__":
    main()
