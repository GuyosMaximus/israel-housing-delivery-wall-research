"""Fig 3 -- Official price index vs. NPV-discounted economic price.

For a deferred-payment deal with share `d` of the nominal price P paid after T years:
    P_NPV = P * [(1 - d) + d / (1 + r)^T]
The aggregate economic index discounts only the share of transactions that are new dwellings sold
under promotions:   I_NPV = I_nominal * [1 - w_new * s_promo(t) * (1 - P_NPV/P)].
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from viz_common import apply_style, save, print_width, badge, verified_marker, LINESTYLES, SERIES, INK, INK2, MUTED, GRID
from data_sources import monthly_panel, verified_points, PRICE_INDEX_VERIFIED, CALIBRATION as C, NEW_DWELLING_WEIGHT


def npv_ratio(r, d=C["npv_deferred_share"], T=C["npv_deferral_years"]):
    return (1 - d) + d / (1 + r) ** T


def run():
    apply_style()
    df = monthly_panel()
    lo, mid, hi = C["npv_discount_rates"]
    agg = {r: df["price_index"] * (1 - NEW_DWELLING_WEIGHT * df["promo_share"] * (1 - npv_ratio(r))) for r in (lo, mid, hi)}
    deal = {r: df["price_index"] * npv_ratio(r) for r in (lo, hi)}

    fig, axes = plt.subplots(2, 1, figsize=(print_width("fig3"), 5.6), sharex=True,
                             gridspec_kw={"height_ratios": [2, 1], "hspace": 0.3, "top": 0.8})
    ax = axes[0]
    ax.plot(df.index, df["price_index"], color=SERIES[0], label="Official index (P nominal, CBS;\napprox. reconstruction)")
    ax.fill_between(df.index, agg[hi], agg[lo], color=SERIES[1], alpha=0.25, lw=0)
    ax.plot(df.index, agg[mid], color=SERIES[1], ls=LINESTYLES[1], label="Market-wide economic index\n(P NPV, r = 5-6%)")
    m = df.index >= pd.Timestamp("2023-03-01")
    ax.fill_between(df.index[m], deal[hi][m], deal[lo][m], color=SERIES[2], alpha=0.30, lw=0,
                    label="20/80 deal itself:\nP NPV band (r = 5-6%)")
    ax.set_ylabel("Index, Jan-2021 = 100")
    ax.set_title("(a) Nominal vs. NPV-discounted price level", loc="left", fontsize=8.5)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.set_ylim(95, 172)

    disc_lo, disc_hi = (1 - npv_ratio(lo)) * 100, (1 - npv_ratio(hi)) * 100
    last = df.index[-1]
    ax.annotate(f"hidden discount on a\n20/80 deal: {disc_lo:.1f}-{disc_hi:.1f}%", xy=(last, deal[lo].iloc[-1]),
                xytext=(pd.Timestamp("2023-07-01"), 99), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))

    gap = (1 - agg[mid] / df["price_index"]) * 100
    gap_lo = (1 - agg[lo] / df["price_index"]) * 100
    gap_hi = (1 - agg[hi] / df["price_index"]) * 100
    ax = axes[1]
    ax.fill_between(df.index, gap_lo, gap_hi, color=SERIES[1], alpha=0.25, lw=0)
    ax.plot(df.index, gap, color=SERIES[1])
    ax.set_ylabel("Overstatement, %")
    ax.set_title("(b) Overstatement of official index\n     (market-wide)", loc="left", fontsize=8.5)
    ax.set_ylim(0, 3)
    fig.text(0.02, 0.925, "ILLUSTRATIVE SCENARIO: NPV lines and panel (b)\nuse a calibrated promotion share (model, not data)",
             ha="left", va="top", fontsize=7.5, style="italic", color=INK)
    axes[1].xaxis.set_major_locator(mdates.YearLocator())
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.suptitle("Deferred-payment promotions\ninflate measured prices", x=0.02, ha="left",
                 fontsize=9.5, fontweight="bold", color=INK, y=0.995)
    path = save(fig, "fig3_npv_price_discount_gap.png")

    peak = gap.idxmax()
    metrics = {
        "deal_discount_pct": {f"r={r:.3f}": round((1 - npv_ratio(r)) * 100, 2) for r in C["npv_discount_rates"]},
        "market_overstatement_peak_pct": round(float(gap.max()), 2),
        "market_overstatement_peak_month": str(peak.date()),
        "market_overstatement_last_pct": round(float(gap.iloc[-1]), 2),
        "price_index_last": round(float(df["price_index"].iloc[-1]), 1),
        "npv_index_last_r5.5": round(float(agg[mid].iloc[-1]), 1),
    }
    return path, metrics


if __name__ == "__main__":
    print(run())
