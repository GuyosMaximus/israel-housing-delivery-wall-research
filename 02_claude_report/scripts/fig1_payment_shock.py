"""Fig 1 -- Payment shock at delivery (Israel 20/80, 20/50/30+balloon) vs. US 2/28 teaser ARM reset."""
import numpy as np
import matplotlib.pyplot as plt

from viz_common import apply_style, save, print_width, badge, LINESTYLES, SERIES, INK, INK2, MUTED
from data_sources import CALIBRATION as C


def annuity(principal, rate, years):
    r = rate / 12
    n = years * 12
    return principal * r / (1 - (1 + r) ** -n)


def compute():
    months = np.arange(-24, 25)
    # --- US 2/28 subprime: 2y teaser then reset on remaining 28y balance
    p0 = annuity(C["us_loan_usd"], C["us_teaser_rate"], 30)
    r = C["us_teaser_rate"] / 12
    bal = C["us_loan_usd"] * (1 + r) ** 24 - p0 * ((1 + r) ** 24 - 1) / r
    p1 = annuity(bal, C["us_reset_rate"], 28)
    income_us = p0 / C["us_initial_dti"]
    us = np.where(months < 0, p0, p1) / income_us

    # --- Israel 20/80: nothing paid between signing and delivery, then full mortgage
    loan_il = C["il_price_nis"] * C["il_ltv_at_delivery"]
    pm = annuity(loan_il, C["il_mortgage_rate"], 30)
    inc = C["il_income_nis_month"]
    il_2080 = np.where(months < 0, 0.0, pm) / inc

    # --- Israel 20/50/30 with bank balloon (interest-only) on the 50% tranche from month -18
    balloon = 0.50 * C["il_price_nis"]
    io = balloon * C["il_balloon_rate"] / 12
    il_205030 = np.where(months < -18, 0.0, np.where(months < 0, io, pm)) / inc

    return months, {
        "US 2/28 subprime ARM (2005-07)": us,
        "Israel 20/80 (2023-26)": il_2080,
        "Israel 20/50/30 + balloon loan (2023-26)": il_205030,
    }, {
        "us_teaser_payment_usd": round(p0), "us_reset_payment_usd": round(p1),
        "us_pti_before": round(us[0], 3), "us_pti_after": round(us[-1], 3),
        "us_payment_increase_pct": round((p1 / p0 - 1) * 100, 1),
        "il_mortgage_payment_nis": round(pm), "il_pti_after": round(pm / inc, 3),
        "il_205030_interest_only_nis": round(io), "il_205030_pti_before": round(io / inc, 3),
        "il_205030_payment_increase_pct": round((pm / io - 1) * 100, 1),
    }


def run():
    apply_style()
    months, series, metrics = compute()
    fig, ax = plt.subplots(figsize=(print_width("fig1"), 3.9))
    styles = [dict(), dict(ls=LINESTYLES[1], zorder=4), dict(lw=3.0)]  # Israeli lines coincide after delivery
    for (name, y), color, st in zip(series.items(), SERIES, styles):
        ax.step(months, y * 100, where="post", color=color, label=name, **st)
    ax.axvline(0, color=MUTED, lw=1, ls="--")
    ax.text(0.5, 44, "Reset / delivery\n(month 0)", color=INK2, fontsize=7.5, va="center")

    # direct labels of the jumps (selective, not on every point)
    us_b, us_a = metrics["us_pti_before"] * 100, metrics["us_pti_after"] * 100
    il_a = metrics["il_pti_after"] * 100
    ax.annotate(f"+{us_a - us_b:.1f} pp (+{metrics['us_payment_increase_pct']:.0f}%)",
                xy=(3, us_a), xytext=(5, us_a + 6), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.annotate(f"0 -> {il_a:.0f}% of income\n(+{il_a:.0f} pp)", xy=(1, il_a), xytext=(5, il_a - 13),
                fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.annotate(f"interest-only\n{metrics['il_205030_pti_before']*100:.0f}% -> {il_a:.0f}%",
                xy=(-10, metrics["il_205030_pti_before"] * 100), xytext=(-16, 27), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))

    ax.set_xlim(-24, 24)
    ax.set_ylim(-2, 66)
    ax.set_xlabel("Months relative to rate reset (US) / key delivery (Israel)")
    ax.set_ylabel("Debt service, % of income")
    ax.set_title("Payment shock at reset / delivery")
    ax.legend(loc="upper left", bbox_to_anchor=(-0.02, -0.15), ncol=1, fontsize=7.5)
    badge(ax, loc="lower right")
    path = save(fig, "fig1_payment_shock_2080_vs_teaser.png")
    return path, metrics


if __name__ == "__main__":
    print(run())
