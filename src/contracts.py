from __future__ import annotations


PERIODS = {
    "january": ("realtime_2026-01.json", "settlement_2026-01.json"),
    "june": ("realtime_2026-06.json", "settlement_2026-06.json"),
    "dst": ("realtime_dst_2026-03-28_31.json", "settlement_dst_2026-03-28_31.json"),
}

EXPECTED_PRICE_AREAS = {"DK1", "DK2"}
EXPECTED_INTERVALS_PER_HOUR = 12

REALTIME_PRODUCTION_COLUMNS = [
    "ProductionLt100MW",
    "ProductionGe100MW",
    "OffshoreWindPower",
    "OnshoreWindPower",
    "SolarPower",
]

REALTIME_EXTERNAL_EXCHANGE_COLUMNS = [
    "ExchangeGermany",
    "ExchangeNetherlands",
    "ExchangeGreatBritain",
    "ExchangeNorway",
    "ExchangeSweden",
]

REALTIME_REQUIRED_COLUMNS = [
    "Minutes5UTC",
    "Minutes5DK",
    "PriceArea",
    *REALTIME_PRODUCTION_COLUMNS,
    "ExchangeGreatBelt",
    *REALTIME_EXTERNAL_EXCHANGE_COLUMNS,
    "BornholmSE4",
]

SETTLEMENT_REQUIRED_COLUMNS = [
    "HourUTC",
    "HourDK",
    "PriceArea",
    "CentralPowerMWh",
    "LocalPowerMWh",
    "CommercialPowerMWh",
    "LocalPowerSelfConMWh",
    "OffshoreWindLt100MW_MWh",
    "OffshoreWindGe100MW_MWh",
    "OnshoreWindLt50kW_MWh",
    "OnshoreWindGe50kW_MWh",
    "SolarPowerLt10kW_MWh",
    "SolarPowerGe10Lt40kW_MWh",
    "SolarPowerGe40kW_MWh",
    "SolarPowerSelfConMWh",
    "ExchangeNO_MWh",
    "ExchangeSE_MWh",
    "ExchangeGE_MWh",
    "ExchangeNL_MWh",
    "ExchangeGB_MWh",
    "ExchangeGreatBelt_MWh",
    "GrossConsumptionMWh",
]

MINIMUM_ANALYSIS_COLUMNS = [
    "hour_utc",
    "hour_dk",
    "price_area",
    "rt_interval_count",
    "rt_offshore_wind_mwh",
    "rt_onshore_wind_mwh",
    "rt_solar_mwh",
    "rt_external_exchange_mwh",
    "rt_load_balance_mwh",
    "st_offshore_wind_mwh",
    "st_onshore_wind_mwh",
    "st_solar_grid_mwh",
    "st_solar_all_mwh",
    "st_external_exchange_mwh",
    "st_gross_consumption_mwh",
    "quality_join_matched",
    "quality_rt_complete_hour",
    "quality_issue_codes",
]
