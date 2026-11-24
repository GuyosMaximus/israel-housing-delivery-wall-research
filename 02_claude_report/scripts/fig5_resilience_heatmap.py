"""Fig 5 -- Delivery-wall stress grid: developer DSCR and bank collateral coverage.

Representative project (normalised so that baseline revenue R = 1):
  costs     = land + construction + soft = 0.83 R  (baseline margin 17%)
  bank loan = loan-to-cost x costs
Shock grid: price drop p in [0, 20%], construction delay m in [0, 24] months.
  * cancellations of promotion (20/80, balloon) presales once p > threshold, resold at (1-p)*0.95
  * overrun = cost inflation on construction + interest carry + continued balloon-interest subsidy
              + Sale-Law late-delivery compensation (150% of rent, after a 2-month grace)
  DSCR      = (revenue - costs - overrun + loan) / loan      (cash available at delivery / debt due)
  coverage  = [(1-p) R (1-haircut) - overrun] / (loan + Sale-Law guarantees)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

from viz_common import apply_style, save, print_width, badge, INK, NAVY, STEEL, RED
from data_sources import CALIBRATION as C

PRICE_DROPS = np.arange(0, 0.2001, 0.025)
DELAYS = np.arange(0, 25, 3)
UNIT_PRICE = C["mc_price_median_nis"]


def project(p, m):
    R = 1.0
    units_value = C["dev_units"] * UNIT_PRICE
    pre, promo = C["dev_presold_share"], C["dev_balloon_share_of_presales"]
    cancel = min(1.0, C["dev_cancel_elasticity"] * max(0.0, p - C["dev_cancel_threshold"]))
    revenue = R * (pre * (1 - promo * cancel) + pre * promo * cancel * (1 - p) * 0.95 + (1 - pre) * (1 - p))
    costs = C["dev_land_cost_share"] + C["dev_construction_cost_share"] + C["dev_soft_cost_share"]
    loan = C["dev_loan_to_cost"] * costs
    yrs = m / 12
    overrun = (C["dev_construction_cost_share"] * ((1 + C["dev_cost_inflation"]) ** yrs - 1)
               + loan * C["dev_loan_rate"] * yrs
               + pre * promo * 0.5 * C["dev_balloon_subsidy_rate"] * yrs
               + C["dev_units"] * pre * C["dev_late_penalty_rent_nis"] * 1.5 * max(0, m - 2) / units_value)
    dscr = (revenue - costs - overrun + loan) / loan
    guarantees = pre * C["bank_guarantee_paid_in_share"]
    coverage = ((1 - p) * R * (1 - C["bank_collateral_haircut"]) - overrun) / (loan + guarantees)
    return dscr, coverage, cancel


def grids():
    D = np.zeros((len(DELAYS), len(PRICE_DROPS)))
    B = np.zeros_like(D)
    for i, m in enumerate(DELAYS):
        for j, p in enumerate(PRICE_DROPS):
            D[i, j], B[i, j], _ = project(p, m)
    return D, B


def run():
    apply_style()
    D, B = grids()
    cmap = LinearSegmentedColormap.from_list("div", [(0.0, RED), (0.5, "#f2f1ee"), (0.75, STEEL), (1.0, NAVY)])
    fig, axes = plt.subplots(2, 1, figsize=(print_width("fig5"), 7.6), gridspec_kw={"hspace": 0.45, "top": 0.895, "bottom": 0.1})
    panels = [(D, 1.0, "(a) Developer DSCR at delivery", "DSCR (x)", "{:.2f}"),
              (B * 100, 100.0, "(b) Bank collateral coverage of exposure", "Coverage, %", "{:.0f}")]
    for ax, (Z, centre, title, cbl, fmt) in zip(axes, panels):
        lo, hi = Z.min(), Z.max()
        norm = TwoSlopeNorm(vcenter=centre, vmin=min(lo, centre - 1e-6), vmax=max(hi, centre + 1e-6))
        im = ax.imshow(Z, cmap=cmap, norm=norm, aspect="auto", origin="lower")
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                dark_text = abs(norm(Z[i, j]) - 0.5) < 0.35
                # D06: numbers >= 8.5 pt at print width, outlined in their cell colour so the contour never hides them
                halo = cmap(norm(Z[i, j]))
                ax.text(j, i, fmt.format(Z[i, j]), ha="center", va="center", fontsize=8.5, zorder=5,
                        color=INK if dark_text else "white",
                        path_effects=[pe.withStroke(linewidth=1.5, foreground=halo)])
        # break-even boundary drawn on the cell edges between cells >= centre and cells < centre
        ok = Z >= centre
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                if j + 1 < Z.shape[1] and ok[i, j] != ok[i, j + 1]:
                    ax.plot([j + 0.5, j + 0.5], [i - 0.5, i + 0.5], color=INK, lw=1.6, solid_capstyle="projecting", zorder=4)
                if i + 1 < Z.shape[0] and ok[i, j] != ok[i + 1, j]:
                    ax.plot([j - 0.5, j + 0.5], [i + 0.5, i + 0.5], color=INK, lw=1.6, solid_capstyle="projecting", zorder=4)
        ax.set_xlim(-0.5, Z.shape[1] - 0.5)
        ax.set_ylim(-0.5, Z.shape[0] - 0.5)
        ax.set_xticks(range(len(PRICE_DROPS)), [("0%" if p == 0 else f"-{p*100:g}%") for p in PRICE_DROPS], rotation=45)
        ax.set_yticks(range(len(DELAYS)), [f"{m}" for m in DELAYS])
        ax.set_xlabel("Housing price change")
        ax.set_ylabel("Delivery delay, months")
        ax.set_title(title, loc="left", fontsize=8.5)
        ax.grid(False)
        cb = fig.colorbar(im, ax=ax, shrink=0.9, pad=0.02)
        cb.set_label(cbl)
        cb.outline.set_visible(False)
    fig.suptitle("Stress grid: price declines x delivery delays",
                 x=0.02, ha="left", fontsize=9.5, fontweight="bold", color=INK, y=0.995)
    fig.text(0.02, 0.972, "ILLUSTRATIVE SCENARIO - calibrated model, not observed data.\nBlack line = break-even (DSCR = 1.0; coverage = 100%).", ha="left", va="top", fontsize=7.5, style="italic", color=INK)
    path = save(fig, "fig5_delivery_wall_resilience_heatmap.png")

    def first_fail(Z, thr):
        cells = [(DELAYS[i], PRICE_DROPS[j]) for i in range(Z.shape[0]) for j in range(Z.shape[1]) if Z[i, j] < thr]
        return len(cells), cells

    nd, _ = first_fail(D, 1.0)
    nb, _ = first_fail(B, 1.0)
    metrics = {
        "grid_price_drops": [round(float(p), 3) for p in PRICE_DROPS],
        "grid_delays_months": [int(m) for m in DELAYS],
        "dscr_baseline": round(float(D[0, 0]), 3),
        "dscr_worst": round(float(D.min()), 3),
        "coverage_baseline_pct": round(float(B[0, 0] * 100), 1),
        "coverage_worst_pct": round(float(B.min() * 100), 1),
        "cells_dscr_below_1": f"{nd}/{D.size}",
        "cells_coverage_below_100": f"{nb}/{B.size}",
        "dscr_at_minus10_delay12": round(float(D[list(DELAYS).index(12), 4]), 3),
        "dscr_grid": np.round(D, 3).tolist(),
        "coverage_grid_pct": np.round(B * 100, 1).tolist(),
    }
    return path, metrics


if __name__ == "__main__":
    print(run())
