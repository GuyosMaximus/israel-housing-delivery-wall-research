"""Fig 2 -- Unsold new-dwelling inventory vs. BOI policy rate and monthly transactions, 2021-2026.

Three measures on three scales -> stacked small multiples on a shared time axis (no dual axis).
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from viz_common import apply_style, save, print_width, verified_marker, SERIES, INK, INK2, MUTED, CRITICAL, GRID
from data_sources import monthly_panel, verified_points, UNSOLD_VERIFIED, TRANSACTIONS_VERIFIED


def run():
    apply_style()
    df = monthly_panel()
    fig, axes = plt.subplots(3, 1, figsize=(print_width("fig2"), 6.0), sharex=True,
                             gridspec_kw={"height_ratios": [1.3, 1, 1], "hspace": 0.5})

    # (a) unsold inventory
    ax = axes[0]
    ax.plot(df.index, df["unsold"] / 1000, color=SERIES[0], label="interpolated series")
    verified_marker(ax, verified_points(UNSOLD_VERIFIED) / 1000, SERIES[0])
    ax.legend(loc="lower right")
    ax.axhline(85, color=CRITICAL, lw=1, ls="--")
    ax.text(df.index[1], 86.5, "85,000 units", color=CRITICAL, fontsize=7.5)
    ax.set_ylabel("Thousand units")
    ax.set_title("(a) Unsold new dwellings (CBS)", loc="left", fontsize=8.5)
    ax.set_ylim(40, 95)

    # (b) BOI rate
    ax = axes[1]
    ax.step(df.index, df["boi_rate"], where="post", color=SERIES[1])
    ax.set_ylabel("Percent")
    ax.set_title("(b) Bank of Israel policy rate", loc="left", fontsize=8.5)
    ax.set_ylim(0, 5.5)
    ax.annotate("0.10% -> 4.75%\nin 13 months", xy=(pd.Timestamp("2023-05-01"), 4.75),
                xytext=(pd.Timestamp("2021-01-15"), 4.0), fontsize=7.5, va="bottom", color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.annotate("3.25% after five cuts\n(Nov-25 to Sep-26)", xy=(pd.Timestamp("2026-09-01"), 3.25),
                xytext=(pd.Timestamp("2024-09-01"), 1.4), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))

    # (c) transactions
    ax = axes[2]
    ax.bar(df.index, df["transactions"] / 1000, width=22, color=SERIES[2], edgecolor="white", linewidth=0.4)
    ax.set_ylabel("Thousand deals / month")
    verified_marker(ax, verified_points(TRANSACTIONS_VERIFIED) / 1000, SERIES[0], label="verified point")
    ax.legend(loc="upper right")
    ax.set_title("(c) Residential deals per month\n     (MoF Chief Economist)", loc="left", fontsize=8.5)
    ax.set_ylim(0, 15)

    axes[-1].xaxis.set_major_locator(mdates.YearLocator())
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.suptitle("Inventory build-up as rates rose\nand turnover fell", x=0.02, ha="left",
                 fontsize=9.5, fontweight="bold", color=INK, y=0.99)
    path = save(fig, "fig2_unsold_inventory_vs_rates.png")

    yearly = df.groupby(df.index.year).agg(unsold_end=("unsold", "last"), boi_rate_end=("boi_rate", "last"),
                                           transactions_avg=("transactions", "mean"))
    metrics = {
        "unsold_first_month_above_85k": str(df.index[df["unsold"] >= 85_000][0].date()),
        "unsold_change_2021_01_to_last_pct": round((df["unsold"].iloc[-1] / df["unsold"].iloc[0] - 1) * 100, 1),
        "transactions_peak_to_trough_pct": round((df["transactions"].min() / df["transactions"].max() - 1) * 100, 1),
        "corr_rate_vs_unsold": round(df["boi_rate"].corr(df["unsold"]), 3),
        "corr_rate_vs_transactions": round(df["boi_rate"].corr(df["transactions"]), 3),
        "yearly": {int(k): {c: round(float(v), 2) for c, v in row.items()} for k, row in yearly.iterrows()},
    }
    return path, metrics


if __name__ == "__main__":
    print(run())
