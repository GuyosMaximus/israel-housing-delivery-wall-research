"""Fig 7 -- Illustrative CET1 erosion of the five large Israeli banking groups.

Spec, parameters and rationale: cet1_model_spec.md (fixed before the first run).
Amounts in NIS million, 30.9.2026. Buyer default is not bank default: losses arise only where the
project cushion (absorption capacity) is exhausted.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from viz_common import apply_style, save, print_width, INK, NAVY, AMBER, RED, NEUTRAL
from data_sources import CALIBRATION as C, BANKS, CET1_PARAMS as K, ABSORPTION_CDF

NAMES = list(BANKS)
XA, FA = (np.array(v, float) for v in zip(*ABSORPTION_CDF))


def F(x):
    return float(np.interp(x, XA, FA))


def intF(x):
    """Exact integral of the piecewise-linear F from 0 to x (F = 1 above 1)."""
    pts = np.append(XA[XA < x], x)
    y = np.interp(pts, XA, FA)
    return float(np.sum(np.diff(pts) * (y[1:] + y[:-1]) / 2))


def overrun(m):
    """Delay cost per unit of project revenue: same terms as fig5_resilience_heatmap.project()."""
    costs = C["dev_land_cost_share"] + C["dev_construction_cost_share"] + C["dev_soft_cost_share"]
    loan, yrs, pre = C["dev_loan_to_cost"] * costs, m / 12, C["dev_presold_share"]
    return (C["dev_construction_cost_share"] * ((1 + C["dev_cost_inflation"]) ** yrs - 1)
            + loan * C["dev_loan_rate"] * yrs
            + pre * C["dev_balloon_share_of_presales"] * 0.5 * C["dev_balloon_subsidy_rate"] * yrs
            + pre * C["dev_late_penalty_rent_nis"] * 1.5 * max(0, m - 2) / C["mc_price_median_nis"])


def erosion(d, q, m, base="inventory"):
    pre = C["dev_presold_share"]
    lost = pre * C["dev_balloon_share_of_presales"] * d * (1 - (1 - q) * (1 - K["resale_discount"]))
    return q + (lost + overrun(m)) / ((1 - pre) if base == "inventory" else 1.0)


def loss_rate(d, q, m, variant, zeta=K["zeta"], k=K["enforcement_cost"], base="inventory"):
    """Gross loss as a share of EAD."""
    x = erosion(d, q, m, base)
    if variant == "A":
        return zeta * F(x) * (1 - (1 - q) * (1 - k))
    pre = C["dev_presold_share"]
    costs = C["dev_land_cost_share"] + C["dev_construction_cost_share"] + C["dev_soft_cost_share"]
    per_rev = C["dev_loan_to_cost"] * costs + pre * C["bank_guarantee_paid_in_share"]
    return zeta * (1 - pre) / per_rev * intF(x)


def ead_prov(b, s=K["res_share"], delta=K["guarantee_draw"], broad=False):
    v = BANKS[b]
    if broad:
        return float(v["T"]), float(v["P"])
    return s * v["D"] + delta * v["G"], s * v["P"]


def apply_rate(rate, **ead_kw):
    """Net pre-tax loss and CET1 per bank + system, for a gross loss rate on EAD."""
    out, N = {}, 0.0
    for b, v in BANKS.items():
        ead, prov = ead_prov(b, **ead_kw)
        net = max(0.0, rate * ead - prov)
        N += net
        post = net * (1 - K["tax"])
        out[b] = {"net_loss_nis_m": round(net), "cet1_drop_bp_post_tax": round(post / v["RWA"] * 1e4, 1),
                  "cet1_drop_bp_pre_tax": round(net / v["RWA"] * 1e4, 1),
                  "cet1_after_pct": round((v["CET1"] - post) / v["RWA"] * 100, 2),
                  "gap_to_min_bp": round((v["CET1"] - post) / v["RWA"] * 1e4 - v["min"] * 100, 1)}
    E, R, K1 = (sum(v[k] for v in BANKS.values()) for k in ("E", "RWA", "CET1"))
    out["system"] = {"net_loss_nis_bn": round(N / 1e3, 2), "loss_to_equity_pct": round(N / E * 100, 2),
                     "loss_to_equity_post_tax_pct": round(N * (1 - K["tax"]) / E * 100, 2),
                     "cet1_drop_bp_post_tax": round(N * (1 - K["tax"]) / R * 1e4, 1),
                     "cet1_after_pct": round((K1 - N * (1 - K["tax"])) / R * 100, 2),
                     "banks_below_minimum": [b for b in NAMES if out[b]["gap_to_min_bp"] < 0],
                     "banks_below_6.5": [b for b in NAMES if out[b]["cet1_after_pct"] < K["stress_floor"]]}
    return out


def scenario(d, q, m, variant, loss_kw=None, ead_kw=None):
    x = erosion(d, q, m, (loss_kw or {}).get("base", "inventory"))
    r = loss_rate(d, q, m, variant, **(loss_kw or {}))
    return {"d": d, "q": q, "m": m, "x": round(x, 4), "PF": round(F(x) * (loss_kw or {}).get("zeta", K["zeta"]), 4),
            "loss_rate_pct": round(r * 100, 2), **apply_rate(r, **(ead_kw or {}))}


def breakeven_rates():
    out, tot_e, tot_p = {}, 0.0, 0.0
    E = sum(v["E"] for v in BANKS.values())
    for b, v in BANKS.items():
        ead, prov = ead_prov(b)
        tot_e, tot_p = tot_e + ead, tot_p + prov
        for key, floor in (("to_minimum", v["min"]), ("to_6.5", K["stress_floor"])):
            head = v["CET1"] - floor / 100 * v["RWA"]
            out.setdefault(b, {})[key + "_loss_rate_pct"] = round((head / (1 - K["tax"]) + prov) / ead * 100, 2)
        out[b]["headroom_bp"] = round((v["CET1"] / v["RWA"] * 100 - v["min"]) * 100, 1)
    out["system_10pct_equity_loss_rate_pct"] = round((0.10 * E + tot_p) / tot_e * 100, 2)
    out["system_ead_nis_bn"], out["system_prov_nis_bn"] = round(tot_e / 1e3, 1), round(tot_p / 1e3, 2)
    return out


def breakeven_q(m, variant, d=0.25):
    """Smallest price fall (0.1 pp grid, 0-80%) at which each test is breached; None = not reached."""
    res = {}
    for q in np.arange(0, 0.8001, 0.001):
        r = apply_rate(loss_rate(d, q, m, variant))
        for b in r["system"]["banks_below_minimum"]:
            res.setdefault(b, round(float(q) * 100, 1))
        if r["system"]["loss_to_equity_pct"] >= 10:
            res.setdefault("system_10pct_equity", round(float(q) * 100, 1))
        if r["system"]["banks_below_6.5"]:
            res.setdefault("first_bank_below_6.5", round(float(q) * 100, 1))
    return {k: res.get(k) for k in NAMES + ["system_10pct_equity", "first_bank_below_6.5"]}


POINTS = {"baseline": (0.05, 0.05, 0), "grid_centre": (0.20, 0.20, 12), "severe_REQ": (0.25, 0.20, 24),
          "beyond_severe": (0.40, 0.40, 24)}


def compute():
    ax = [0.15, 0.175, 0.20, 0.225, 0.25]
    res = {"points": {f"{k}_{v}": scenario(*p, v) for k, p in POINTS.items() for v in "AB"}}
    res["transmission_test_buyer_default_only"] = {v: scenario(0.25, 0.0, 0, v)["system"]["loss_to_equity_pct"] for v in "AB"}
    res["transmission_test_d100_only"] = {v: scenario(1.0, 0.0, 0, v)["system"]["loss_to_equity_pct"] for v in "AB"}
    res["grid_axis"] = ax
    for v in "AB":
        for m in (0, 12, 24):
            cells = [[scenario(d, q, m, v)["system"] for q in ax] for d in ax]
            res[f"grid_{v}_m{m}_loss_to_equity_pct"] = [[c["loss_to_equity_pct"] for c in r] for r in cells]
            res[f"grid_{v}_m{m}_cet1_drop_bp"] = [[c["cet1_drop_bp_post_tax"] for c in r] for r in cells]
    S = {"base": ({}, {}), "zeta_0.5": ({"zeta": .5}, {}), "zeta_0.25": ({"zeta": .25}, {}),
         "s_projects_only_0.188": ({}, {"s": 69 / 367}), "s_1.0": ({}, {"s": 1.0}),
         "delta_0": ({}, {"delta": 0.0}), "delta_0.5": ({}, {"delta": .5}),
         "EAD_total_credit_risk": ({}, {"broad": True}), "k_10pct (A only)": ({"k": .10}, {}),
         "absorption_base_full_value": ({"base": "full"}, {})}
    res["sensitivity"] = {}
    for pt in ("grid_centre", "severe_REQ"):
        for name, (lk, ek) in S.items():
            res["sensitivity"].setdefault(pt, {})[name] = {
                v: {k: scenario(*POINTS[pt], v, lk, ek)["system"][k] for k in ("loss_to_equity_pct", "cet1_drop_bp_post_tax")}
                for v in "AB"}
    res["breakeven_loss_rate"] = breakeven_rates()
    res["breakeven_price_fall_pct_d25"] = {f"m{m}_{v}": breakeven_q(m, v) for m in (0, 12, 24) for v in "AB"}
    sev = {v: res["points"][f"severe_REQ_{v}"]["system"]["loss_to_equity_pct"] for v in "AB"}
    res["REQ_H3_01_condition2"] = {"loss_to_equity_pct": sev, "threshold_pct": 10,
                                   "result": "met" if max(sev.values()) < 10 else "not met" if min(sev.values()) >= 10
                                   else "inconclusive (method-dependent)"}
    res["reference_BoI_2025_survey_stress"] = {"cet1_drop_pp": 1.5, "cre_cumulative_loss_rate_pct": 3.3,
                                               "cre_loss_nis_bn": round(0.209 * 84, 1), "source_key": "boi_survey2025"}
    return res


def run():
    apply_style()
    res = compute()
    fig, ax = plt.subplots(figsize=(print_width("fig7") - 0.4, 3.7))
    y = np.arange(len(NAMES))[::-1]
    labels = {"centre": "Grid centre: 20% / 20% / 12 months*", "sev": "Severe (REQ-H3-01): 25% / 20% / 24 months*"}
    for yi, b in zip(y, NAMES):
        v = BANKS[b]
        start = v["CET1"] / v["RWA"] * 100
        pt = {(p, var): res["points"][f"{p}_{var}"][b]["cet1_after_pct"] for p in ("grid_centre", "severe_REQ") for var in "AB"}
        for off, p, col in ((0.16, "grid_centre", AMBER), (-0.16, "severe_REQ", RED)):
            a, bb = pt[p, "A"], pt[p, "B"]
            ax.plot([a, start], [yi + off] * 2, color="#dddcd7", lw=1, zorder=1)
            ax.plot([a, bb], [yi + off] * 2, color=col, lw=2.2, zorder=3, solid_capstyle="butt")
            ax.plot(a, yi + off, "o", ms=5.5, color=col, mec="white", mew=.8, zorder=4)
            ax.plot(bb, yi + off, "o", ms=5.5, mfc="white", mec=col, mew=1.4, zorder=4)
            ax.text(a - 0.09, yi + off, f"{a:.1f}", ha="right", va="center", fontsize=7.5, color=INK, zorder=6,
                    bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
        ax.plot(start, yi, "D", ms=6, color=NAVY, mec="white", mew=.8, zorder=5)
        ax.text(start + 0.1, yi, f"{start:.2f}", ha="left", va="center", fontsize=7.5, color=INK)
        ax.plot([v["min"]] * 2, [yi - .38, yi + .38], color=INK, lw=1.8, zorder=2)
    ax.axvline(K["stress_floor"], color=NEUTRAL, lw=1.2, ls=(0, (4, 2)), zorder=0)
    ax.text(K["stress_floor"] + .05, len(NAMES) - .5, "6.5% stress-test floor (BoI)", fontsize=7.5, color=INK, va="bottom")
    ax.set_yticks(y, [b.replace("First International", "First Int'l") for b in NAMES], fontsize=8, color=INK)
    ax.set_ylim(-0.6, len(NAMES) - .1)
    lo = min(res["points"][f"severe_REQ_A"][b]["cet1_after_pct"] for b in NAMES)
    ax.set_xlim(min(6.2, lo - .6), 12.3)
    ax.set_xlabel("CET1 ratio, % of risk-weighted assets (static RWA, after tax, no profit offset)", fontsize=7.5)
    ax.grid(axis="y", visible=False)
    ax.set_title("CET1 of the five large groups: start and after shock", loc="left", fontsize=9, pad=24)
    ax.text(0, 1.015, "ILLUSTRATIVE SCENARIO - calibrated model, not a BoI or bank stress test.\nStart and minimum: published Q3-2026 reports.",
            transform=ax.transAxes, fontsize=7.5, style="italic", va="bottom", color=INK)
    h = [Line2D([], [], marker="D", ls="", color=NAVY, label="Reported, 30 Sep 2026"),
         Line2D([], [], color=INK, lw=1.8, marker="|", ls="", ms=11, mew=1.8, label="Bank's regulatory minimum"),
         Line2D([], [], color=AMBER, lw=2.2, marker="o", ms=5, label=labels["centre"]),
         Line2D([], [], color=RED, lw=2.2, marker="o", ms=5, label=labels["sev"]),
         Line2D([], [], marker="o", ls="", color=MUTED_, label="Variant A: zero-cushion LGD"),
         Line2D([], [], marker="o", ls="", mfc="white", mec=MUTED_, mew=1.4, label="Variant B: shortfall depth only")]
    fig.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.0), ncol=2, fontsize=7.5,
               columnspacing=1.0, handletextpad=.5)
    fig.text(0.5, -0.2, "* buyer default / price fall / delivery delay", ha="center", fontsize=7.5, style="italic", color=INK)
    return save(fig, "fig7_bank_cet1_erosion.png"), res


MUTED_ = "#52514e"

if __name__ == "__main__":
    import json
    print(json.dumps(run()[1], indent=1, default=str))
