"""Separate miniopgaver, ikke Energinet-facit. Implementér ét trin ad gangen."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent

def load():
    return pd.DataFrame(json.loads((ROOT / "data/flow.json").read_text(encoding="utf-8"))["records"])

def validate(frame):
    """M02: kræv timestamp/device/flow_l_min, UTC-tid, ikke-tom nøgle,
    entydig timestamp+device og 10-minuttersgrid. Fejl på brud.
    Numerisk flow: manglende værdier tillades og bevares, negative afvises."""

    required = ["timestamp", "device", "flow_l_min"]

    missing = [col for col in required if col not in frame.columns]
    if missing:
        raise ValueError(f"Manglende kolonner: {missing}")

    df = frame.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="raise"
    )

    if df["device"].isna().any() or df["device"].astype(str).str.strip().eq("").any():
        raise ValueError("Device må ikke være tom")

    if df.duplicated(["timestamp", "device"]).any():
        raise ValueError("Dublet i timestamp + device")

    if (
        (df["timestamp"].dt.minute % 10 != 0)
        | (df["timestamp"].dt.second != 0)
        | (df["timestamp"].dt.microsecond != 0)
    ).any():
        raise ValueError("Timestamp ligger ikke på 10-minuttersgrid")

    df["flow_l_min"] = pd.to_numeric(
        df["flow_l_min"],
        errors="raise"
    )

    if (df["flow_l_min"].dropna() < 0).any():
        raise ValueError("Flow må ikke være negativt")

    return df

def aggregate(frame):
    """M02: beregn liter fra 10-minutters middelværdier.
    Én række pr. UTC-time/device; kolonner hour_utc, device, measured_l,
    rows, valid, complete. Alle-null sum skal forblive manglende.
    complete kræver 6 unikke grid-intervaller OG 6 gyldige flowværdier."""

    df = frame.copy()

    # L/min × 10 minutter = liter i intervallet
    df["liters"] = df["flow_l_min"] * 10

    # Find UTC-timen for hver måling
    df["hour_utc"] = df["timestamp"].dt.floor("h")

    # Gruppér pr. time og device
    hourly = (
        df.groupby(["hour_utc", "device"])
        .agg(
            measured_l=("liters", lambda x: x.sum(min_count=1)),
            rows=("timestamp", "size"),
            valid=("flow_l_min", "count"),
            intervals=("timestamp", "nunique"),
        )
        .reset_index()
    )

    # En komplet time kræver 6 intervaller og 6 gyldige målinger
    hourly["complete"] = (
        (hourly["intervals"] == 6)
        & (hourly["valid"] == 6)
    )

    return hourly[
        ["hour_utc", "device", "measured_l", "rows", "valid", "complete"]
    ]

def combine(hourly, manual):
    """M03: outer join på hour_utc/device med valideret 1:1.
    Bevar joinstatus; differencen er measured_l minus manual_l.
    Sammenligningsscope kræver match og complete; slet ingen rækker."""
    raise NotImplementedError("M03: combine")

if __name__ == "__main__":
    print(aggregate(validate(load())))
