"""Run every figure, export comms/data_summary.json, and (with --sync) copy outputs into build/.

Usage:  py -X utf8 run_all.py [--sync]
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import fig1_payment_shock, fig2_inventory_rates, fig3_npv_gap
import fig4_pti_monte_carlo, fig5_resilience_heatmap, fig6_comparative_risk
import fig7_bank_cet1_erosion
from data_sources import (CALIBRATION, BOI_RATE_DECISIONS, UNSOLD_ANCHORS, UNSOLD_VERIFIED, TRANSACTIONS_ANCHORS,
                          TRANSACTIONS_VERIFIED, PRICE_INDEX_ANCHORS, PRICE_INDEX_VERIFIED, PROMO_SHARE_ANCHORS,
                          NEW_DWELLING_WEIGHT, LAST_VERIFIED, CONTEXT_FACTS,
                          BANKS, CET1_PARAMS, ABSORPTION_CDF)

HERE = Path(__file__).resolve().parent
# project root = nearest ancestor holding comms/ (works from 03_python_viz and from build/scripts)
PROJECT = next((p for p in HERE.parents if (p / "comms").is_dir()), HERE.parent)
BUILD_FIG = PROJECT / "build" / "figures"
BUILD_SCR = PROJECT / "build" / "scripts"
COMMS = PROJECT / "comms"

MODULES = [fig1_payment_shock, fig2_inventory_rates, fig3_npv_gap,
           fig4_pti_monte_carlo, fig5_resilience_heatmap, fig6_comparative_risk, fig7_bank_cet1_erosion]


def series(anchors, verified, unit, period, status, source_key, note=""):
    return {"unit": unit, "period": period, "status": status, "source_key": source_key,
            "verified": bool(verified), "verified_points": verified, "anchor_values": anchors, "note": note}


def agent1_numbers():
    """Agent 1's checked market figures (R08), merged if the file exists."""
    f = PROJECT / "01_intro_history" / "remediation_numbers.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def build_summary(results):
    a1 = agent1_numbers()
    return {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "generator": "03_python_viz/run_all.py (Agent 3)",
        "rule": "A1/A2: state as fact ONLY values with verified=true (or listed in verified_points); "
                "everything else must be framed as illustration / scenario / assumption in the Hebrew text.",
        "data_status_legend": {
            "official": "published decision/statistic; every value verified against the publisher",
            "official_approx": "official series; only `verified_points` were checked - other anchors are interpolation inputs",
            "calibrated": "model parameter chosen by the author; NOT data",
        },
        "last_verified_month": str(LAST_VERIFIED.date()),
        "official_data": {
            "boi_policy_rate": {**series(BOI_RATE_DECISIONS, BOI_RATE_DECISIONS, "% per year", "2021-01..2026-09",
                                         "official", "boi_rate_decisions",
                                         "Path 2021-2026 via boi_rate_decisions (Trading Economics); 2025-11, 2026-01, 2026-07, 2026-09 decisions "
                                         "from BoI primary releases. Held 3.25% on 2026-10-21 (single secondary source)."),
                                "verified": True},
            "unsold_new_dwellings": series(UNSOLD_ANCHORS, UNSOLD_VERIFIED, "dwellings, end of month (not seasonally adjusted)",
                                           "2021-01..2026-09", "official_approx",
                                           ["cbs_newdwellings", "globes_2026_09_inventory", "cbs_newdwellings_2026q3"],
                                           "Sep-2026 SA value 86,666; 25.8 months of supply. CBS drops a unit 15 months after completion. "
                                           "Anchors before 2026 unverified."),
            "residential_transactions": series(TRANSACTIONS_ANCHORS, TRANSACTIONS_VERIFIED, "deals per month",
                                               "2021-01..2026-09", "official_approx", ["semerenko_market", "toi_housing_2026_10"],
                                               "Verified: Apr-26 5,081; May-26 8,246; Aug-26 7,532. NOT verified: 2025 total 84,879, "
                                               "'20-year low' claim. Anchors before 2026 unverified."),
            "dwelling_price_index": series(PRICE_INDEX_ANCHORS, PRICE_INDEX_VERIFIED, "index, Jan-2021 = 100",
                                           "2021-01..2026-09", "official_approx", ["cbs_priceindex", "cbs_priceindex_2026_222", "toi_housing_2026_10"],
                                           "LEVELS UNVERIFIED (reconstruction). Verified y/y only: +0.5% Aug-Sep 2025; "
                                           "-2.0% Apr-May 2026; -1.8% Jul-Aug 2026."),
            "household_debt_gdp": {"values": {"US 2007Q4": 98.4, "Israel 2025-12": 42.5}, "unit": "% of GDP",
                                   "period": "2007Q4 / 2025-12", "status": "official", "source_key": "bis_hhdebt",
                                   "verified": True},
        },
        "bank_capital_2026q3": {
            "period": "2026-09-30", "unit": "NIS m (min, reported: %)", "status": "official", "verified": True,
            "legend": {"D": "debts, construction + real-estate activity, Israel", "T": "total credit risk, same sectors",
                       "P": "allowance for credit losses, same sectors", "G": "guarantees to home buyers, nominal",
                       "E": "shareholders' equity", "min": "required CET1 ratio", "reported": "published CET1 ratio"},
            "source_key": [v["src"] for v in BANKS.values()], "values": BANKS},
        "absorption_capacity_cdf": {"value": ABSORPTION_CDF, "status": "official points, spliced by the author",
                                    "source_key": ["boi_survey2025", "leumi_q3_2026", "hapoalim_q3_2026"], "verified": True},
        "context_facts": {**CONTEXT_FACTS, **a1.get("context_facts", {})},
        "derived_agent1": a1.get("derived", {}),
        "calibrated_parameters": {
            **{k: {"value": v, "status": "calibrated", "verified": False} for k, v in CALIBRATION.items()},
            **{"cet1_" + k: {"value": v, "status": "calibrated; see cet1_model_spec.md", "verified": False}
               for k, v in CET1_PARAMS.items()},
            "promo_share_of_new_sales": {"value": PROMO_SHARE_ANCHORS, "status": "calibrated", "verified": False,
                                         "calibration_target": "20% May-2026 and 30% Aug-2026, free-market developer sales, delivery >= 1 year, 5 areas (mof_review_2026_08, p. 12)"},
            "new_dwelling_weight_in_transactions": {"value": NEW_DWELLING_WEIGHT, "status": "calibrated", "verified": False},
        },
        "simulation_outputs": {"status": "calibrated - scenario results, never state as observed facts", **results},
        "figures": {k: f"figures/{k}.png" for k in results},
    }


def sync():
    BUILD_FIG.mkdir(parents=True, exist_ok=True)
    BUILD_SCR.mkdir(parents=True, exist_ok=True)
    for png in (HERE / "output").glob("fig*.png"):
        shutil.copy2(png, BUILD_FIG / png.name)
    if HERE == BUILD_SCR:
        return
    for py in HERE.glob("*.py"):
        shutil.copy2(py, BUILD_SCR / py.name)
    print("synced to build/figures and build/scripts")


def main():
    results = {}
    for mod in MODULES:
        path, metrics = mod.run()
        results[path.stem] = metrics
        print("OK", path.name)

    COMMS.mkdir(exist_ok=True)
    (COMMS / "data_summary.json").write_text(
        json.dumps(build_summary(results), indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    (HERE / "logs").mkdir(exist_ok=True)
    (HERE / "logs" / "last_run.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print("data_summary.json written")
    if "--sync" in sys.argv:
        sync()
    else:
        print("(build sync skipped; pass --sync)")


if __name__ == "__main__":
    main()
