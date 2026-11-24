"""Fig 4 -- Monte Carlo (N = 10,000) PTI distribution of deferred-payment buyers at the 2026-27 delivery wall.

Each simulated buyer: correlated log-normal (price, income); LTV ~ Beta capped at 75%; term 25/30y;
income shock between signing and delivery. PTI = mortgage annuity / net household income.
Same random draws are reused across the three rate scenarios (common random numbers).
"""
import numpy as np
import matplotlib.pyplot as plt

from viz_common import apply_style, save, print_width, badge, LINESTYLES, SERIES, INK, INK2, MUTED, CRITICAL
from data_sources import CALIBRATION as C


def simulate():
    rng = np.random.default_rng(C["mc_seed"])
    n = C["mc_n"]
    rho = C["mc_price_income_corr"]
    z = rng.multivariate_normal([0, 0], [[1, rho], [rho, 1]], size=n)
    price = C["mc_price_median_nis"] * np.exp(C["mc_price_sigma_log"] * z[:, 0])
    income = C["mc_income_median_nis_month"] * np.exp(C["mc_income_sigma_log"] * z[:, 1])
    income *= np.exp(rng.normal(0, C["mc_income_shock_sd"], n))
    a, b = C["mc_ltv_alpha_beta"]
    ltv = np.minimum(rng.beta(a, b, n), C["mc_ltv_cap"])
    term = rng.choice(C["mc_term_years_choices"], n)
    loan = price * ltv
    out = {}
    for rate in C["mc_mortgage_rates"]:
        r = rate / 12
        pay = loan * r / (1 - (1 + r) ** (-term * 12))
        out[rate] = pay / income
    return out, {"ltv_mean": float(ltv.mean()), "price_median": float(np.median(price)),
                 "income_median": float(np.median(income))}


def run():
    apply_style()
    pti, draws = simulate()
    thr, cap = C["pti_risk_threshold"], C["pti_hard_cap"]
    fig, ax = plt.subplots(figsize=(print_width("fig4"), 4.4))
    bins = np.linspace(0, 1.0, 81)
    labels = {0.040: "Benign: 4.00%", 0.0525: "Base: 5.25%", 0.065: "Stress: 6.50%"}
    metrics = {}
    for (rate, x), color, lsty in zip(pti.items(), SERIES, LINESTYLES):
        share40 = float((x > thr).mean())
        share50 = float((x > cap).mean())
        ax.hist(x * 100, bins=bins * 100, histtype="step", lw=1.6, ls=lsty, color=color,
                label=f"{labels[rate]}  (PTI>40%: {share40:.0%})")
        ax.hist(x * 100, bins=bins * 100, color=color, alpha=0.10)
        metrics[f"rate_{rate:.4f}"] = {
            "pti_median": round(float(np.median(x)), 4), "pti_p90": round(float(np.percentile(x, 90)), 4),
            "share_pti_above_40": round(share40, 4), "share_pti_above_50": round(share50, 4),
        }
    ymax = ax.get_ylim()[1] * 1.22
    ax.set_ylim(0, ymax)
    ax.axvline(thr * 100, color=CRITICAL, lw=1.4, ls="--")
    ax.text(thr * 100 - 0.8, ymax * 0.98, "40% PTI\n(100% risk\nweight,\nDir. 329)", color=CRITICAL, fontsize=7.5, va="top", ha="right")
    ax.axvline(cap * 100, color=CRITICAL, lw=1, ls=":")
    ax.text(cap * 100 + 0.8, ymax * 0.98, "50% hard cap\n(Directive 329)", color=CRITICAL, fontsize=7.5, va="top")
    ax.set_xlim(0, 90)
    ax.set_xlabel("Payment-to-income at delivery, %")
    ax.set_ylabel(f"Simulated buyers (N = {C['mc_n']:,})")
    ax.set_title("Monte Carlo: buyer PTI at the\n2026-27 delivery wall")
    ax.legend(loc="upper left", bbox_to_anchor=(-0.02, -0.15), title="Mortgage rate scenario", title_fontsize=7.5, fontsize=7.5,
              alignment="left")
    badge(ax, loc="upper right", xy=(0.99, 0.80))
    path = save(fig, "fig4_pti_monte_carlo.png")
    metrics["draws"] = {k: round(v, 3) for k, v in draws.items()}
    return path, metrics


if __name__ == "__main__":
    print(run())
