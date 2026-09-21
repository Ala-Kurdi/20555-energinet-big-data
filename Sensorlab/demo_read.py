"""Modul01-demo på konstruerede eksempeldata. Kør fra valgfri mappe."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
payload = json.loads((ROOT / "data/flow.json").read_text(encoding="utf-8"))
frame = pd.DataFrame(payload["records"])
print(frame.head())
print(frame.dtypes)
print(frame.groupby("device")["flow_l_min"].agg(["size", "count", "mean"]))
# Selvstændig ændring: vis kun B og find antallet af manglende værdier.
