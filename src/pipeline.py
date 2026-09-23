from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from contracts import (
    EXPECTED_INTERVALS_PER_HOUR,
    EXPECTED_PRICE_AREAS,
    MINIMUM_ANALYSIS_COLUMNS,
    PERIODS,
    REALTIME_EXTERNAL_EXCHANGE_COLUMNS,
    REALTIME_PRODUCTION_COLUMNS,
    REALTIME_REQUIRED_COLUMNS,
    SETTLEMENT_REQUIRED_COLUMNS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "output"


class NextTodo(NotImplementedError):
    """Bruges til at pege på næste nummererede trin i starterprojektet."""


def load_records(path: Path, expected_dataset: str) -> pd.DataFrame:
    """Indlæser records og udfører de første kontroller af JSON-konvolutten."""
    if not path.exists():
        raise FileNotFoundError(f"Råfilen findes ikke: {path}")
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("dataset") != expected_dataset:
        raise ValueError(
            f"{path.name} angiver {payload.get('dataset')!r}; "
            f"forventede {expected_dataset!r}."
        )
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError(f"{path.name} mangler en liste med records.")
    if payload.get("total") is not None and int(payload["total"]) != len(records):
        raise ValueError(f"{path.name}: total matcher ikke antallet af records.")
    return pd.DataFrame(records)


def validate_snapshot(
    frame: pd.DataFrame,
    required_columns: list[str],
    timestamp_column: str,
    label: str,
) -> pd.DataFrame:
    """TODO 1: Implementér den fatale datakontrakt.

    Minimum:
    - kontrollér obligatoriske kolonner;
    - konvertér timestampkolonnen og fejl tydeligt på ugyldige værdier;
    - kontrollér DK1/DK2;
    - kontrollér dubletter på timestamp + PriceArea;
    - returnér en kopi med den konverterede timestampkolonne.
    """

    missing = sorted(set(required_columns) - set(frame.columns))
    if missing:
        raise ValueError(
            f"{label}: mangler obligatoriske kolonner: {missing}"
        )

    df = frame.copy()

    try:
        df[timestamp_column] = pd.to_datetime(
            df[timestamp_column],
            utc=True,
            errors="raise",
        )
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"{label}: ugyldig timestamp i {timestamp_column}"
        ) from exc

    invalid_price_areas = (
        set(df["PriceArea"].dropna()) - set(EXPECTED_PRICE_AREAS)
    )

    if invalid_price_areas:
        raise ValueError(
            f"{label}: ugyldige PriceArea-værdier: "
            f"{sorted(invalid_price_areas)}"
        )

    if df["PriceArea"].isna().any():
        raise ValueError(
            f"{label}: PriceArea må ikke mangle"
        )

    duplicates = df.duplicated(
        subset=[timestamp_column, "PriceArea"],
        keep=False,
    )

    if duplicates.any():
        raise ValueError(
            f"{label}: dubletter på {timestamp_column} + PriceArea"
        )

    return df

def mw_to_mwh(values: pd.Series, interval_minutes: int = 5) -> pd.Series:
    """TODO 2: Konvertér gennemsnitlig effekt til energi for intervallet."""

    numeric = pd.to_numeric(values, errors="raise")

    if interval_minutes <= 0:
        raise ValueError("Intervallet skal være større end 0 minutter.")

    return numeric * (interval_minutes / 60)

def prepare_realtime(frame: pd.DataFrame) -> pd.DataFrame:
    """TODO 3: Skab én realtime-række pr. UTC-time og prisområde.

    Outputtet skal mindst indeholde:
    - hour_utc, price_area og rt_interval_count;
    - offshore, onshore og sol i MWh;
    - udenlandsk udveksling uden Storebælt;
    - en prisområdebalance, hvor Storebælt er med;
    - antal negative produktionsintervaller.

    Husk at omregne hvert interval før summering.
    """

    df = frame.copy()

    df["hour_utc"] = df["Minutes5UTC"].dt.floor("h")

    df["offshore_mwh"] = mw_to_mwh(df["OffshoreWindPower"])
    df["onshore_mwh"] = mw_to_mwh(df["OnshoreWindPower"])
    df["solar_mwh"] = mw_to_mwh(df["SolarPower"])

    external_exchange_mw = df[REALTIME_EXTERNAL_EXCHANGE_COLUMNS].sum(
        axis=1,
        min_count=1,
    )

    df["external_exchange_mwh"] = mw_to_mwh(external_exchange_mw)

    df["load_balance_mwh"] = (
        df["external_exchange_mwh"]
        + mw_to_mwh(df["ExchangeGreatBelt"])
    )

    df["negative_production_interval"] = (
        df[REALTIME_PRODUCTION_COLUMNS].lt(0).any(axis=1)
    )

    hourly = (
        df.groupby(["hour_utc", "PriceArea"], as_index=False)
        .agg(
            rt_interval_count=("Minutes5UTC", "nunique"),
            rt_offshore_wind_mwh=("offshore_mwh", "sum"),
            rt_onshore_wind_mwh=("onshore_mwh", "sum"),
            rt_solar_mwh=("solar_mwh", "sum"),
            rt_external_exchange_mwh=("external_exchange_mwh", "sum"),
            rt_load_balance_mwh=("load_balance_mwh", "sum"),
            rt_negative_production_intervals=(
                "negative_production_interval",
                "sum",
            ),
        )
        .rename(columns={"PriceArea": "price_area"})
    )

    return hourly

def prepare_settlement(frame: pd.DataFrame) -> pd.DataFrame:
    """TODO 4: Skab sammenligningsfelter i afregningsdata.

    Outputtet skal mindst indeholde:
    - hour_utc, hour_dk og price_area;
    - samlet offshore og onshore;
    - sol både uden og med self-consumption;
    - udenlandsk udveksling uden Storebælt;
    - gross consumption.
    """
    df = frame.copy()

    # Tid og prisområde
    df["hour_utc"] = df["HourUTC"]
    df["hour_dk"] = df["HourDK"]
    df["price_area"] = df["PriceArea"]

    # Vindproduktion
    df["st_offshore_wind_mwh"] = (
        df["OffshoreWindLt100MW_MWh"]
        + df["OffshoreWindGe100MW_MWh"]
    )

    df["st_onshore_wind_mwh"] = (
        df["OnshoreWindLt50kW_MWh"]
        + df["OnshoreWindGe50kW_MWh"]
    )

    # Solproduktion uden self-consumption
    df["st_solar_grid_mwh"] = (
        df["SolarPowerLt10kW_MWh"]
        + df["SolarPowerGe10Lt40kW_MWh"]
        + df["SolarPowerGe40kW_MWh"]
    )

    # Solproduktion inklusive self-consumption
    df["st_solar_all_mwh"] = (
        df["st_solar_grid_mwh"]
        + df["SolarPowerSelfConMWh"]
    )

    # Udenlandsk udveksling uden Storebælt
    df["st_external_exchange_mwh"] = (
        df["ExchangeNO_MWh"]
        + df["ExchangeSE_MWh"]
        + df["ExchangeGE_MWh"]
        + df["ExchangeNL_MWh"]
        + df["ExchangeGB_MWh"]
    )

    # Bruttoforbrug
    df["st_gross_consumption_mwh"] = df["GrossConsumptionMWh"]

    return df[
        [
            "hour_utc",
            "hour_dk",
            "price_area",
            "st_offshore_wind_mwh",
            "st_onshore_wind_mwh",
            "st_solar_grid_mwh",
            "st_solar_all_mwh",
            "st_external_exchange_mwh",
            "st_gross_consumption_mwh",
        ]
    ].copy()


def join_and_flag(realtime: pd.DataFrame, settlement: pd.DataFrame) -> pd.DataFrame:
    """TODO 5: Udfør outer join og tilføj kvalitetsflag.

    Join på hour_utc + price_area, og validér én-til-én-kardinalitet.
    Bevar mindst flag for joinstatus og præcis 12 realtime-intervaller.
    Tilføj gerne negative værdier, frosne tilstande og metadataadvarsler.
    """
    joined = realtime.merge(
        settlement,
        on=["hour_utc", "price_area"],
        how="outer",
        validate="one_to_one",
        indicator=True,
    )

    # Join-kvalitet: findes rækken i begge datasæt?
    joined["quality_join_matched"] = joined["_merge"].eq("both")

    # Realtime-kvalitet: har timen præcis 12 fem-minutters intervaller?
    joined["quality_rt_complete_hour"] = (
        joined["rt_interval_count"].eq(EXPECTED_INTERVALS_PER_HOUR)
    )

    def build_issue_codes(row: pd.Series) -> str:
        issues = []

        if not row["quality_join_matched"]:
            issues.append("JOIN_MISSING")

        if not row["quality_rt_complete_hour"]:
            issues.append("RT_INCOMPLETE")

        if row.get("rt_negative_production_intervals", 0) > 0:
            issues.append("NEGATIVE_PRODUCTION")

        return ";".join(issues)

    joined["quality_issue_codes"] = joined.apply(
        build_issue_codes,
        axis=1,
    )

    joined = joined.drop(columns=["_merge"])

    return joined

def create_quality_summary(analysis_ready: pd.DataFrame) -> dict:
    """TODO 6: Lav en lille maskinlæsbar rapport med tællinger.

    Medtag mindst samlet rækkeantal, joinstatus, fulde/ufuldstændige timer
    og antal rækker med hvert kvalitetsflag.
    """
    total_rows = len(analysis_ready)

    matched_rows = int(
        analysis_ready["quality_join_matched"].sum()
    )

    complete_hours = int(
        analysis_ready["quality_rt_complete_hour"].sum()
    )

    summary = {
        "total_rows": total_rows,
        "join_matched": matched_rows,
        "join_missing": total_rows - matched_rows,
        "rt_complete_hours": complete_hours,
        "rt_incomplete_hours": total_rows - complete_hours,
    }

    issue_counts: dict[str, int] = {}

    for codes in analysis_ready["quality_issue_codes"]:
        if not codes:
            continue

        for code in codes.split(";"):
            issue_counts[code] = issue_counts.get(code, 0) + 1

    summary["issue_counts"] = issue_counts

    return summary


def write_outputs(
    period: str,
    analysis_ready: pd.DataFrame,
    quality_summary: dict,
) -> tuple[Path, Path]:
    missing = sorted(set(MINIMUM_ANALYSIS_COLUMNS) - set(analysis_ready.columns))
    if missing:
        raise ValueError(f"Analyseoutputtet mangler obligatoriske kolonner: {missing}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / f"analysis_ready_{period}.csv"
    quality_path = OUTPUT_DIR / f"quality_{period}.json"
    analysis_ready.to_csv(csv_path, index=False)
    with quality_path.open("w", encoding="utf-8") as handle:
        json.dump(quality_summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return csv_path, quality_path


def run_period(period: str) -> tuple[Path, Path]:
    if period not in PERIODS:
        raise ValueError(f"Ukendt periode: {period}")
    realtime_name, settlement_name = PERIODS[period]
    realtime_raw = load_records(
        RAW_DIR / realtime_name, "ElectricityProdex5MinRealtime"
    )
    settlement_raw = load_records(
        RAW_DIR / settlement_name, "ProductionConsumptionSettlement"
    )
    realtime_valid = validate_snapshot(
        realtime_raw,
        REALTIME_REQUIRED_COLUMNS,
        "Minutes5UTC",
        "realtime",
    )
    settlement_valid = validate_snapshot(
        settlement_raw,
        SETTLEMENT_REQUIRED_COLUMNS,
        "HourUTC",
        "afregning",
    )
    realtime_hourly = prepare_realtime(realtime_valid)
    settlement_hourly = prepare_settlement(settlement_valid)
    analysis_ready = join_and_flag(realtime_hourly, settlement_hourly)
    quality_summary = create_quality_summary(analysis_ready)
    return write_outputs(period, analysis_ready, quality_summary)
