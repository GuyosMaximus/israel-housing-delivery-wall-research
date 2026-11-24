"""Single registry of every number used in the figures (Agent 3).

Status vocabulary (also exported to comms/data_summary.json):
  * "official"        -- published decision/statistic, every value checked against the publisher.
  * "official_approx" -- official series reconstructed at anchor points and interpolated monthly.
                         Points listed in `verified_points` were checked against a source on
                         2026-11-15; the remaining anchors are NOT verified and are shown in the
                         figures only as the interpolated line (no marker).
  * "calibrated"      -- model parameter chosen by the author to match stylised facts. NOT data.

Nothing is downloaded at run time; the pipeline is reproducible offline.
"""
import numpy as np
import pandas as pd

MONTHS = pd.date_range("2021-01-01", "2026-09-01", freq="MS")
LAST_VERIFIED = pd.Timestamp("2026-09-01")  # latest month with a verified observation (CBS inventory, BOI rate)


def _interp(anchors):
    s = pd.Series({pd.Timestamp(k): v for k, v in anchors.items()}).sort_index()
    s = s.reindex(s.index.union(MONTHS)).interpolate("time").reindex(MONTHS)
    return s


# ---------------------------------------------------------------- Bank of Israel policy rate (official, verified)
BOI_RATE_DECISIONS = {  # effective month -> rate (%)
    "2021-01": 0.10, "2022-04": 0.35, "2022-05": 0.75, "2022-07": 1.25, "2022-08": 2.00,
    "2022-10": 2.75, "2022-11": 3.25, "2023-01": 3.75, "2023-02": 4.25, "2023-04": 4.50,
    "2023-05": 4.75, "2024-01": 4.50, "2025-11": 4.25, "2026-01": 4.00, "2026-05": 3.75,
    "2026-07": 3.50, "2026-09": 3.25,
}


def boi_rate():
    s = pd.Series({pd.Timestamp(k): v for k, v in BOI_RATE_DECISIONS.items()}).sort_index()
    return s.reindex(s.index.union(MONTHS)).ffill().reindex(MONTHS)


# ---------------------------------------------------------------- CBS: unsold new dwellings, end of month
# verified 2026-11-16 against dated sources: Jan-26 (TheMarker), Jul-26 (Globes, ~85,000),
# Aug-26 / Sep-26 (CBS release of 12 Nov 2026 via Ynet / Nadlan Center)
UNSOLD_VERIFIED = {"2026-01": 86_290, "2026-07": 85_000, "2026-08": 85_680, "2026-09": 85_080}
UNSOLD_ANCHORS = {
    "2021-01": 49_000, "2021-12": 46_000, "2022-06": 48_000, "2022-12": 52_000,
    "2023-06": 56_000, "2023-12": 61_000, "2024-04": 65_900, "2025-04": 79_410, "2025-12": 86_090,  # unverified anchors
    # 2025-12: CBS not seasonally adjusted (about 83,340 SA, secondary source); BoI annual report ch. 8 quotes about 83,000, SA basis.
    **UNSOLD_VERIFIED,
}

# ---------------------------------------------------------------- Residential deals per month (Chief Economist, MoF / Tax Authority)
# Verified 2026-11-16: Apr-26 5,081 and May-26 8,246 (Semerenko table of MoF data); Aug-26 7,532 (ToI, MoF).
# The earlier "May-26 = 5,081, 20-year low" and "2025 = 84,879" could not be sourced -> dropped / unverified.
TRANSACTIONS_VERIFIED = {"2026-04": 5_081, "2026-05": 8_246, "2026-08": 7_532}
TRANSACTIONS_ANCHORS = {
    "2021-01": 10_500, "2021-06": 12_500, "2021-12": 13_000, "2022-06": 10_500,
    "2022-12": 8_000, "2023-06": 7_000, "2023-12": 6_800, "2024-07": 7_950, "2025-07": 7_073,
    **TRANSACTIONS_VERIFIED, "2026-09": 7_000,
}

# ---------------------------------------------------------------- CBS dwellings price index (rebased Jan-2021 = 100)
# Levels are an UNVERIFIED reconstruction (the Jan-2021..Jan-2025 levels came from a secondary site and
# conflict with CEIC). Only y/y changes are verified: -2.0% Apr-May 2026 (CBS 222/2026), -1.8% Jul-Aug 2026.
PRICE_INDEX_VERIFIED = {}
PRICE_INDEX_ANCHORS = {
    "2021-01": 100.0, "2022-01": 110.6, "2023-01": 131.3, "2024-01": 128.5, "2025-01": 138.2,
    "2025-08": 140.0,   # CBS: +0.5% y/y Aug-Sep 2025 (level approximate)
    "2026-01": 139.0,
    "2026-08": 137.5,   # CBS: -1.8% y/y Jul-Aug 2026 applied to 2025-08 level
    "2026-09": 137.3,
}

# ---------------------------------------------------------------- Promotion share (CALIBRATED, not data)
# Calibration targets (MoF Chief Economist review, Aug-2026, p. 12, read 2026-11-24): 20% in May-2026 and 30% in Aug-2026 of
# free-market developer sales with delivery >= 1 year in 5 monitored areas (not national). Sep-2026 = held flat (assumption).
# The earlier 0.33 came from a press headline ("about a third"); 2025-09 = 0.31 is an unverified, different-date observation, kept. BOI restricted 20/80 & 10/90 deals from Mar-2025.
PROMO_SHARE_ANCHORS = {
    "2021-01": 0.03, "2022-06": 0.05, "2023-03": 0.12, "2023-12": 0.30,
    "2024-06": 0.40, "2025-02": 0.45, "2025-04": 0.30, "2025-09": 0.31, "2026-05": 0.20, "2026-08": 0.30, "2026-09": 0.30,
}
NEW_DWELLING_WEIGHT = 0.38  # calibrated share of new dwellings in all transactions


def monthly_panel():
    df = pd.DataFrame(index=MONTHS)
    df["boi_rate"] = boi_rate()
    df["unsold"] = _interp(UNSOLD_ANCHORS)
    df["transactions"] = _interp(TRANSACTIONS_ANCHORS)
    df["price_index"] = _interp(PRICE_INDEX_ANCHORS)
    df["promo_share"] = _interp(PROMO_SHARE_ANCHORS)
    return df


def verified_points(d):
    return pd.Series({pd.Timestamp(k): v for k, v in d.items()}).sort_index()


# ---------------------------------------------------------------- Context facts (verified, used in text not charts)
CONTEXT_FACTS = {
    # Upgraded 2026-11-16 after reading the primary BoI boxes (12 May 2026) text directly.
    "developer_credit_2025_bn_nis": {"value": 69, "prev_2024": 49, "change_pct": 40, "unit": "NIS bn", "period": "2025",
                                     "source_key": "boi2026_recredit", "verified": True, "status": "official",
                                     "note": "Financial credit to residential construction projects, end-2024 -> end-2025 (primary text)"},
    "construction_re_share_business_credit": {"value": 39, "share_of_total_credit_to_public": 21, "growth_2025_pct": 14,
                                              "unit": "% of balance-sheet business credit", "period": "2025",
                                              "source_key": "boi2026_recredit", "verified": True, "status": "official",
                                              "note": "Supersedes the 2024H1 value of ~40% (boi_fsr2024h1)"},
    "signing_to_mortgage_gap_months": {"value": 8, "earlier": "about 6 months (2018-2022)", "unit": "months", "period": "2025",
                                       "source_key": "boi2026_resloans", "verified": True, "status": "official"},
    # Verified 2026-11-24 in the primary texts (press box 12-May-2026 and BoI survey 2025, Box 5.3, pp. 147-155).
    "absorption_capacity_avg": {"value": 58, "prev_2024": 70, "unit": "%", "period": "2025-12",
                                "source_key": ["boi2026_recredit", "boi_survey2025"], "verified": True, "status": "official",
                                "note": "Maximum fall in apartment sale prices without bank loss on the project, average. "
                                        "It is NOT a 58% drop in sales."},
    "absorption_below_40_share_of_credit": {"value": 33, "prev_2024": 22, "unit": "% of credit to started projects", "period": "2025-12",
                                            "source_key": "boi_survey2025", "verified": True, "status": "official", "note": "8% below 30"},
    "projects_construction_ahead_of_sales": {"value": 44, "prev_2024": 35, "unit": "% of total exposure of the five groups", "period": "2025-12",
                                             "source_key": ["boi2026_recredit", "boi_survey2025"], "verified": True, "status": "official"},
    "cre_credit_split_2025": {"value": {"land": 104, "of_which_residential_land": 81, "residential_projects": 69, "total": 367},
                              "unit": "NIS bn", "period": "2025-12", "source_key": "boi_survey2025", "verified": True, "status": "official"},
    "boi_macro_stress_test_2025": {"value": {"cet1_drop_pp": 1.5, "cet1_start": 11.5, "cet1_trough": 10.0, "cre_cumulative_loss_rate_pct": 3.3,
                                             "total_credit_losses_bn": 84, "cre_share_of_losses_pct": 20.9, "price_cumulative_gap_pct": 15},
                                   "unit": "mixed", "period": "scenario from 2024-12", "source_key": "boi_survey2025", "verified": True,
                                   "status": "official", "note": "Full macro scenario with income and dynamic balance sheet; not our model"},
    # Read 2026-11-24 in the Mizrahi-Tefahot Q3-2026 report, p. 67 (note 5: guarantees mostly reinsured).
    "mizrahi_construction_split_2026q3": {"value": {"guarantee_credit_risk_bn": 7.6, "guarantees_nominal_bn": 18.3,
                                                    "project_assistance_share_of_onbalance_pct": 59},
                                          "unit": "NIS bn / %", "period": "2026-09-30", "source_key": "mizrahi_q3_2026",
                                          "verified": True, "status": "official",
                                          "note": "7,613 vs nominal 18,293 NIS m; 32,470 of 54,876 NIS m = 59%"},
    "absorption_cdf_hapoalim_share": {"value": 53, "unit": "% of credit behind the 0.25/0.50/0.75 nodes", "period": "2026-09-30",
                                      "source_key": ["leumi_q3_2026", "hapoalim_q3_2026"], "verified": True, "status": "derived",
                                      "note": "52,634 of 99,962 NIS m; Hapoalim p. 61 note 4: completed value; Leumi p. 80 note c: inventory prices"},
    "unsold_2025_12_seasonally_adjusted": {"value": 83000, "unit": "dwellings, approx., seasonally adjusted", "period": "2025-12",
                                           "source_key": "boi_annual2025_housing", "verified": True, "status": "official",
                                           "note": "Fig 2 series is NOT seasonally adjusted (2025-12 anchor 86,090)"},
    "boi_stress_floor_cet1": {"value": 6.5, "unit": "%", "period": "2024 survey", "source_key": "boi_survey2024", "verified": True, "status": "official"},
    "promo_share_long_delivery_new_deals": {"value": 31, "unit": "% of new-dwelling deals, delivery > 1y", "period": "2025-09",
                                            "source_key": "mof_chiefecon_2025", "verified": False, "status": "press_secondary",
                                            "note": "cited source predates/does not show the value; use promo_share_new_deals_2026_08"},
    "promo_share_new_deals_2026_08": {"value": 30, "superseded_value": 33, "unit": "% of free-market developer sales, delivery >= 1 year, 5 monitored areas (Center, Tel Aviv, Hadera, Netanya, Beer Sheva)", "period": "2026-08",
                                      "source_key": ["mof_review_2026_08", "nadlancenter_2026_08_promos"], "verified": True, "status": "official"},
    "price_index_yoy": {"value": {"2025-08/09": 0.5, "2026-04/05": -2.0, "2026-07/08": -1.8}, "unit": "% y/y",
                        "source_key": ["cbs_priceindex", "cbs_priceindex_2026_222", "toi_housing_2026_10"],
                        "verified": True, "status": "official / press_secondary"},
}

# ---------------------------------------------------------------- Cross-country comparison
COMPARATIVE = {
    "metrics": ["Reported LTV", "Effective LTV", "Household debt / GDP", "Bank exposure to real estate"],
    "US 2007":     [80, 95, 98, 55],
    "Spain 2007":  [70, 85, 82, 60],
    "Israel 2026": [60, 85, 43, 39],
    "verified": {  # per country, per metric
        "US 2007":     [False, False, True, False],
        "Spain 2007":  [False, False, False, False],
        "Israel 2026": [False, False, True, True],  # exposure 39% = official (boi2026_recredit)
    },
    "status": {
        "Reported LTV": "calibrated - typical first-lien LTV at origination (Israel: BOI reports ~50% of new mortgages above 60% LTV)",
        "Effective LTV": "calibrated - US: CLTV incl. piggy-back seconds; Spain: incl. consumer top-ups; "
                         "Israel: model output = 75% regulatory LTV on NPV-discounted price (0.75/0.88)",
        "Household debt / GDP": "official - BIS credit to households (US Q4-2007 98.4%; Israel Dec-2025 42.5%); Spain 2007 approximate",
        "Bank exposure to real estate": "US/Spain: calibrated - stylised share of bank credit tied to real estate; "
                                        "Israel 2026: official - 39% of balance-sheet business credit to construction & real estate, "
                                        "2025 (Bank of Israel, boi2026_recredit; supersedes ~40% in BOI FSR 2024H1)",
    },
    "source_keys": ["bis_hhdebt", "boi2026_recredit", "boi_fsr2024h1", "fcic2011"],
}

# ---------------------------------------------------------------- Calibrated simulation parameters
CALIBRATION = {
    "npv_discount_rates": [0.05, 0.055, 0.06],
    "npv_deferral_years": 3.0,
    "npv_deferred_share": 0.80,
    "mc_n": 10_000,
    "mc_seed": 20262027,
    "mc_mortgage_rates": [0.040, 0.0525, 0.065],
    "mc_price_median_nis": 2_400_000,
    "mc_price_sigma_log": 0.30,
    "mc_income_median_nis_month": 26_000,
    "mc_income_sigma_log": 0.35,
    "mc_price_income_corr": 0.55,
    "mc_ltv_alpha_beta": [9.0, 4.0],
    "mc_ltv_cap": 0.75,
    "mc_term_years_choices": [25, 30],
    "mc_income_shock_sd": 0.05,
    "pti_risk_threshold": 0.40,
    "pti_hard_cap": 0.50,
    "us_teaser_rate": 0.08, "us_reset_rate": 0.11, "us_loan_usd": 200_000, "us_initial_dti": 0.40,
    "il_price_nis": 2_500_000, "il_income_nis_month": 28_000, "il_mortgage_rate": 0.05,
    "il_ltv_at_delivery": 0.75, "il_balloon_rate": 0.055,
    "dev_units": 200, "dev_presold_share": 0.60, "dev_land_cost_share": 0.30,
    "dev_construction_cost_share": 0.45, "dev_soft_cost_share": 0.08, "dev_loan_to_cost": 0.70,
    "dev_loan_rate": 0.0725, "dev_cost_inflation": 0.05, "dev_balloon_subsidy_rate": 0.055,
    "dev_balloon_share_of_presales": 0.45, "dev_late_penalty_rent_nis": 7_500,
    "dev_cancel_threshold": 0.05, "dev_cancel_elasticity": 2.0,
    "bank_collateral_haircut": 0.10, "bank_guarantee_paid_in_share": 0.30,
}

# ---------------------------------------------------------------- CET1 model inputs (official: Q3-2026 bank reports, NIS m, 30.9.2026)
# D/T/P = debts / total credit risk / allowance, construction + real-estate activity in Israel; G = guarantees to home buyers
# (nominal, gross of reinsurance); E = shareholders' equity; min = required CET1 incl. housing-loan add-on (%).
BANKS = {
    "Leumi":               dict(CET1=70_936, RWA=623_358, min=10.23, D=149_317, T=238_418, P=3_368, G=47_972, E=71_442, src="leumi_q3_2026", reported=11.38),
    "Hapoalim":            dict(CET1=67_480, RWA=580_553, min=10.24, D=116_083, T=188_829, P=2_575, G=31_513, E=67_530, src="hapoalim_q3_2026", reported=11.62),
    "Mizrahi-Tefahot":     dict(CET1=37_170, RWA=368_119, min=9.60, D=54_442, T=98_698, P=709, G=18_293, E=36_667, src="mizrahi_q3_2026", reported=10.10),
    "Discount":            dict(CET1=35_821, RWA=347_080, min=9.21, D=56_484, T=90_415, P=1_251, G=17_480, E=35_098, src="discount_q3_2026", reported=10.32),
    "First International": dict(CET1=14_730, RWA=143_282, min=9.24, D=24_491, T=36_206, P=469, G=2_984, E=14_533, src="fibi_q3_2026", reported=10.28),
}
# Cumulative distribution of absorption capacity by credit (official points, spliced; see cet1_model_spec.md)
ABSORPTION_CDF = [(0, 0), (0.25, 0.010), (0.30, 0.08), (0.40, 0.33), (0.50, 0.556), (0.75, 0.752), (1.0, 1.0)]
CET1_PARAMS = {  # calibrated unless noted
    "res_share": 150 / 367,        # official inputs (BoI survey 2025, table 5.1), calibrated use
    "guarantee_draw": 1.0, "resale_discount": 0.05, "enforcement_cost": 0.05, "zeta": 1.0,
    "tax": 0.3475,                 # official statutory rate 2026, excl. special tax
    "stress_floor": 6.5,           # official, BoI stress-test minimum
}
