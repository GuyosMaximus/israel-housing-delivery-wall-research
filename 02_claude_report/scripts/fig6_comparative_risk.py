"""Fig 6 -- US 2007 vs. Spain 2007 vs. Israel 2026 across four leverage / exposure metrics (grouped bars)."""
import numpy as np
import matplotlib.pyplot as plt

from viz_common import apply_style, save, print_width, badge, SERIES, INK

from data_sources import COMPARATIVE


def run():
    apply_style()
    metrics = COMPARATIVE["metrics"]
    countries = ["US 2007", "Spain 2007", "Israel 2026"]
    x = np.arange(len(metrics))
    w = 0.28
    fig, ax = plt.subplots(figsize=(print_width("fig6"), 3.6))
    for k, (c, color) in enumerate(zip(countries, SERIES)):
        vals = COMPARATIVE[c]
        bars = ax.bar(x + (k - 1) * w, vals, w - 0.015, color=color, label=c, edgecolor="white", linewidth=1)
        for b, v, ok in zip(bars, vals, COMPARATIVE["verified"][c]):
            ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v}" + ("" if ok else "*"), ha="center", va="bottom",
                    fontsize=7.5, color=INK)
    ax.set_xticks(x, ["Reported\nLTV", "Effective LTV\n(incl. hidden\nleverage)", "Household\ndebt / GDP",
                      "Bank credit\nexposure to\nreal estate"])
    ax.set_ylabel("Percent")
    ax.set_ylim(0, 128)
    ax.set_title("Israel 2026 vs. the 2007 crisis economies")
    ax.legend(loc="upper left", ncol=3, fontsize=7.5)
    badge(ax, "* = calibrated (ILLUSTRATIVE); no star = verified (BIS, BoI)", loc="upper right")
    ax.texts[-1].set_position((0.99, 0.88))
    path = save(fig, "fig6_comparative_risk_2008_vs_2026.png")
    out = {c: dict(zip(metrics, COMPARATIVE[c])) for c in countries}
    out["status"] = COMPARATIVE["status"]
    return path, out


if __name__ == "__main__":
    print(run())
