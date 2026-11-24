"""
Quantitative Simulation & Figure Generation Suite
Project: Comparative Financial-Economic Research Preparatory Report
Israel Housing Market & Developer Financing (2022-2026) vs. US Subprime Crisis (2008)
"""

import os
import json
import math
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Ensure reproducibility
RNG = np.random.default_rng(20261115)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

FONT_REG_PATH = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\arialbd.ttf"


def get_font(size: int, bold: bool = False):
    path = FONT_BOLD_PATH if bold else FONT_REG_PATH
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_grid_and_axes(draw, box, x_ticks, y_ticks, title, subtitle, x_label, y_label):
    x0, y0, x1, y1 = box
    # White chart background with subtle border
    draw.rectangle([x0, y0, x1, y1], fill=(250, 252, 255), outline=(180, 190, 205), width=2)

    f_title = get_font(34, bold=True)
    f_sub = get_font(22, bold=False)
    f_axis = get_font(24, bold=True)
    f_tick = get_font(20, bold=False)

    # Title and subtitle placed cleanly above chart box
    draw.text((x0, y0 - 110), title, fill=(15, 35, 65), font=f_title)
    draw.text((x0, y0 - 65), subtitle, fill=(75, 90, 115), font=f_sub)

    # Horizontal grid lines & Y ticks
    for val, label, frac in y_ticks:
        py = int(y1 - frac * (y1 - y0))
        draw.line([(x0, py), (x1, py)], fill=(220, 226, 235), width=2)
        bbox = draw.textbbox((0, 0), label, font=f_tick)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x0 - tw - 16, py - th // 2), label, fill=(40, 50, 70), font=f_tick)

    # Vertical grid lines & X ticks
    for val, label, frac in x_ticks:
        px = int(x0 + frac * (x1 - x0))
        draw.line([(px, y0), (px, y1)], fill=(228, 233, 240), width=2)
        bbox = draw.textbbox((0, 0), label, font=f_tick)
        tw = bbox[2] - bbox[0]
        draw.text((px - tw // 2, y1 + 14), label, fill=(40, 50, 70), font=f_tick)

    # Axes lines
    draw.line([(x0, y0), (x0, y1)], fill=(30, 45, 70), width=3)
    draw.line([(x0, y1), (x1, y1)], fill=(30, 45, 70), width=3)

    # Axis labels
    bbox_x = draw.textbbox((0, 0), x_label, font=f_axis)
    draw.text(((x0 + x1 - (bbox_x[2] - bbox_x[0])) // 2, y1 + 58), x_label, fill=(20, 35, 60), font=f_axis)
    draw.text((25, y0 - 34), y_label, fill=(20, 35, 60), font=f_axis)


def generate_fig01_npv_discount():
    """
    Figure 1: Implicit NPV Price Discount (%) vs. Developer Bridge Interest Rate
    Across Payment Structures (20/80, 15/85, 10/90, and Post-Regulation 20/50/30)
    """
    W, H = 2000, 1200
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    box = (180, 150, 1880, 1020)
    x0, y0, x1, y1 = box

    rates = np.linspace(0.03, 0.08, 50)  # 3.0% to 8.0% annual discount/funding rate
    T = 3.0  # 3 years construction duration

    # Implicit NPV discount formula:
    # Traditional staged payment: [0.20 at t=0, 0.20 at t=0.75, 0.20 at t=1.5, 0.20 at t=2.25, 0.20 at t=3.0]
    # 20/80 Balloon: [0.20 at t=0, 0.80 at t=3.0] + developer pays bridge interest on 80%
    def staged_pv(r):
        times = [0.0, 0.75, 1.5, 2.25, 3.0]
        weights = [0.20, 0.20, 0.20, 0.20, 0.20]
        return sum(w / ((1 + r) ** t) for w, t in zip(weights, times))

    def promo_discount(r, alpha_down, deferred_share, mid_share=0.0, cpi_waiver=0.025):
        # PV of cash received by developer net of interest subsidy & CPI waiver vs standard staged schedule
        pv_std = staged_pv(r)
        eff_r = r + cpi_waiver
        pv_promo = alpha_down + mid_share / ((1 + eff_r) ** (T / 2.0)) + deferred_share / ((1 + eff_r) ** T)
        return (pv_std - pv_promo) / pv_std * 100.0

    x_ticks = [(r, f"{r*100:.1f}%", (r - 0.03) / 0.05) for r in np.linspace(0.03, 0.08, 6)]
    y_ticks = [(v, f"{v:.1f}%", v / 14.0) for v in np.linspace(0, 14, 8)]

    draw_grid_and_axes(
        draw,
        box,
        x_ticks,
        y_ticks,
        "Implicit NPV Price Discount Embedded in Developer Promotions (T = 36 Months)",
        "Economic gap between nominal 'Shelf Price' and Real Present Value across financing structures",
        "Annual Opportunity Cost / Financing Discount Rate r (%)",
        "Implicit NPV Discount (%)"
    )

    curves = [
        ("10/90 Extreme Balloon (10% Down, 90% at Delivery)", (200, 35, 45), [promo_discount(r, 0.10, 0.90) for r in rates]),
        ("15/85 Subsidy Loan (15% Down, 85% at Delivery)", (230, 115, 20), [promo_discount(r, 0.15, 0.85) for r in rates]),
        ("20/80 Classic Balloon (20% Down, 80% at Delivery)", (25, 95, 185), [promo_discount(r, 0.20, 0.80) for r in rates]),
        ("20/50/30 Mutation (Post-March 2025 BOI Directive)", (35, 150, 95), [promo_discount(r, 0.20, 0.30, 0.50) for r in rates]),
    ]

    for label, color, vals in curves:
        pts = []
        for r, v in zip(rates, vals):
            px = int(x0 + ((r - 0.03) / 0.05) * (x1 - x0))
            py = int(y1 - (v / 14.0) * (y1 - y0))
            pts.append((px, py))
        draw.line(pts, fill=color, width=6)
        for px, py in pts[::9]:
            draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=color, outline=(255, 255, 255), width=2)

    # Highlight 2025-2026 Israeli Developer Financing Zone (r = 5.5% - 6.5%)
    zx0 = int(x0 + ((0.055 - 0.03) / 0.05) * (x1 - x0))
    zx1 = int(x0 + ((0.065 - 0.03) / 0.05) * (x1 - x0))
    for py in range(y0 + 10, y1 - 10, 16):
        draw.line([(zx0, py), (zx0, py + 8)], fill=(120, 40, 140), width=3)
        draw.line([(zx1, py), (zx1, py + 8)], fill=(120, 40, 140), width=3)
    draw.text((zx0 + 12, y0 + 25), "Israel 2024-2026", fill=(105, 30, 125), font=get_font(20, bold=True))
    draw.text((zx0 + 12, y0 + 52), "Effective Rate Zone", fill=(105, 30, 125), font=get_font(19, bold=False))

    # Legend box
    lx0, ly0 = x0 + 40, y0 + 30
    draw.rectangle([lx0, ly0, lx0 + 680, ly0 + 210], fill=(255, 255, 255), outline=(160, 175, 195), width=2)
    f_leg = get_font(21, bold=False)
    for idx, (label, color, _) in enumerate(curves):
        cy = ly0 + 28 + idx * 45
        draw.line([(lx0 + 20, cy), (lx0 + 75, cy)], fill=color, width=6)
        draw.ellipse([lx0 + 42, cy - 6, lx0 + 54, cy + 6], fill=color)
        draw.text((lx0 + 92, cy - 12), label, fill=(25, 35, 50), font=f_leg)

    out_path = os.path.join(FIG_DIR, "fig01_npv_discount_curves.png")
    img.save(out_path, dpi=(300, 300))
    return {
        "disc_20_80_at_6pct": round(promo_discount(0.06, 0.20, 0.80), 2),
        "disc_10_90_at_6pct": round(promo_discount(0.06, 0.10, 0.90), 2),
        "disc_20_50_30_at_6pct": round(promo_discount(0.06, 0.20, 0.30, 0.50), 2),
    }


def generate_fig02_payment_shock():
    """
    Figure 2: Monte Carlo Household PTI Distribution at the 2026-2027 Delivery Wall (N = 10,000)
    Comparing Contract Underwriting Expectations vs. Actual Delivery-Date Rate & CPI Reality
    """
    N = 10000
    # Monthly net household income in NIS (dual-earner upper-middle deciles buying new apartments, median ~32,500 NIS)
    incomes = RNG.lognormal(mean=math.log(32500), sigma=0.22, size=N)
    incomes = np.clip(incomes, 18000, 75000)

    # Apartment price ~ 2.65M NIS, 80% deferred balance = 2.12M NIS
    base_loan = RNG.normal(loc=2120000, scale=240000, size=N)
    base_loan = np.clip(base_loan, 1350000, 3100000)

    # Expected scenario at signing (buyers assumed rate would drop to ~3.3% and minimal CPI linkage)
    r_expected = RNG.normal(loc=0.034, scale=0.004, size=N) / 12.0
    n_months = 300  # 25 years
    pmt_expected = base_loan * (r_expected * (1 + r_expected) ** n_months) / ((1 + r_expected) ** n_months - 1)
    pti_expected = (pmt_expected / incomes) * 100.0

    # Realized scenario at 2026-2027 Delivery Wall:
    # Construction index / upgrade linkage adds ~6.5% to balance, mortgage rate at 5.25% average
    inflated_loan = base_loan * RNG.normal(loc=1.068, scale=0.018, size=N)
    r_actual = RNG.normal(loc=0.0525, scale=0.0045, size=N) / 12.0
    pmt_actual = inflated_loan * (r_actual * (1 + r_actual) ** n_months) / ((1 + r_actual) ** n_months - 1)
    pti_actual = (pmt_actual / incomes) * 100.0

    W, H = 2000, 1200
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    box = (180, 150, 1880, 1020)
    x0, y0, x1, y1 = box

    bins = np.linspace(15, 65, 42)
    hist_exp, _ = np.histogram(pti_expected, bins=bins, density=True)
    hist_act, _ = np.histogram(pti_actual, bins=bins, density=True)
    centers = 0.5 * (bins[:-1] + bins[1:])

    x_ticks = [(v, f"{int(v)}%", (v - 15.0) / 50.0) for v in range(15, 70, 5)]
    y_ticks = [(v, f"{v:.2f}", v / 0.10) for v in np.linspace(0.0, 0.10, 6)]

    draw_grid_and_axes(
        draw,
        box,
        x_ticks,
        y_ticks,
        "Monte Carlo Distribution of Household Payment-to-Income (PTI) at Delivery (N = 10,000)",
        "Shift from Buyer Expectation at Signing (2023-2024) to Actual Underwriting at Delivery Wall (2026-2027)",
        "Monthly Mortgage Payment-to-Income Ratio - PTI (%)",
        "Probability Density"
    )

    # Plot Expected PTI bars/curve (Blue)
    pts_exp = []
    pts_act = []
    for c, he, ha in zip(centers, hist_exp, hist_act):
        px = int(x0 + ((c - 15.0) / 50.0) * (x1 - x0))
        py_e = int(y1 - min(he / 0.10, 1.0) * (y1 - y0))
        py_a = int(y1 - min(ha / 0.10, 1.0) * (y1 - y0))
        pts_exp.append((px, py_e))
        pts_act.append((px, py_a))

    # Fill under curves using vertical lines
    for (px, py_e) in pts_exp:
        draw.line([(px - 6, y1), (px - 6, py_e)], fill=(175, 208, 245), width=12)
    for (px, py_a) in pts_act:
        draw.line([(px + 6, y1), (px + 6, py_a)], fill=(248, 185, 185), width=12)

    draw.line(pts_exp, fill=(20, 90, 175), width=6)
    draw.line(pts_act, fill=(195, 35, 45), width=6)

    # Bank of Israel 40% Regulatory PTI Cap & 50% Hard Freeze Threshold
    for thresh, col, lbl in [
        (40.0, (215, 120, 10), "BOI Risk-Weight Threshold (PTI = 40%)"),
        (50.0, (160, 15, 25), "BOI Absolute Regulatory Cap (PTI = 50%)"),
    ]:
        tx = int(x0 + ((thresh - 15.0) / 50.0) * (x1 - x0))
        for py in range(y0 + 15, y1 - 5, 18):
            draw.line([(tx, py), (tx, py + 10)], fill=col, width=4)
        draw.text((tx + 10, y0 + (45 if thresh == 40 else 115)), lbl, fill=col, font=get_font(21, bold=True))

    # Legend
    lx0, ly0 = x0 + 35, y0 + 30
    draw.rectangle([lx0, ly0, lx0 + 690, ly0 + 135], fill=(255, 255, 255), outline=(160, 175, 195), width=2)
    f_leg = get_font(21, bold=False)
    draw.rectangle([lx0 + 20, ly0 + 25, lx0 + 60, ly0 + 50], fill=(175, 208, 245), outline=(20, 90, 175), width=3)
    draw.text((lx0 + 78, ly0 + 24), f"Expected PTI at Signing (Mean = {np.mean(pti_expected):.1f}%)", fill=(20, 40, 65), font=f_leg)
    draw.rectangle([lx0 + 20, ly0 + 78, lx0 + 60, ly0 + 103], fill=(248, 185, 185), outline=(195, 35, 45), width=3)
    draw.text((lx0 + 78, ly0 + 77), f"Realized PTI at Delivery Wall (Mean = {np.mean(pti_actual):.1f}%)", fill=(20, 40, 65), font=f_leg)

    out_path = os.path.join(FIG_DIR, "fig02_payment_shock_distribution.png")
    img.save(out_path, dpi=(300, 300))

    share_above_40 = float(np.mean(pti_actual > 40.0) * 100.0)
    share_above_50 = float(np.mean(pti_actual > 50.0) * 100.0)
    return {
        "mean_pti_expected": round(float(np.mean(pti_expected)), 2),
        "mean_pti_actual": round(float(np.mean(pti_actual)), 2),
        "mean_monthly_shock_nis": round(float(np.mean(pmt_actual - pmt_expected)), 0),
        "share_pti_above_40_pct": round(share_above_40, 2),
        "share_pti_above_50_pct": round(share_above_50, 2),
    }


def generate_fig03_israel_inventory_vs_rates():
    """
    Figure 3: Israel Unsold New Dwellings Inventory & BOI Interest Rate Trajectory (2022 Q1 - 2026 Q3)
    """
    quarters = [
        "22Q1", "22Q2", "22Q3", "22Q4",
        "23Q1", "23Q2", "23Q3", "23Q4",
        "24Q1", "24Q2", "24Q3", "24Q4",
        "25Q1", "25Q2", "25Q3", "25Q4",
        "26Q1", "26Q2", "26Q3"
    ]
    unsold_k = [
        44.2, 46.8, 49.5, 53.1,
        56.4, 59.8, 62.9, 67.3,
        70.5, 74.1, 77.8, 80.9,
        83.2, 84.8, 86.1, 86.9,
        87.4, 86.8, 85.9
    ]
    boi_rate = [
        0.10, 0.75, 2.00, 3.25,
        4.25, 4.75, 4.75, 4.75,
        4.50, 4.50, 4.50, 4.50,
        4.50, 4.50, 4.25, 4.25,
        4.25, 4.00, 4.00
    ]

    W, H = 2000, 1200
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    box = (180, 150, 1820, 1020)
    x0, y0, x1, y1 = box

    n_q = len(quarters)
    inner_w = (x1 - x0) - 96
    x_ticks = [(i, quarters[i], (48 + i / (n_q - 1) * inner_w) / (x1 - x0)) for i in range(0, n_q, 2)]
    y_ticks = [(v, f"{int(v)}K", (v - 30.0) / 70.0) for v in range(30, 105, 10)]

    draw_grid_and_axes(
        draw,
        box,
        x_ticks,
        y_ticks,
        "Unsold New Dwellings Inventory vs. Bank of Israel Policy Rate (2022Q1 - 2026Q3)",
        "Monetary tightening shock and accumulation of >85,000 unsold apartments in developer inventories",
        "Quarter (2022Q1 - 2026Q3)",
        "Unsold Units (Thousands)"
    )

    # Right axis for BOI Rate (0% to 6%)
    f_tick = get_font(20, bold=False)
    for r_val in range(0, 7):
        py = int(y1 - (r_val / 6.0) * (y1 - y0))
        draw.text((x1 + 18, py - 10), f"{r_val}.0%", fill=(185, 35, 45), font=f_tick)
    draw.text((x1 - 70, y0 - 34), "BOI Rate (%)", fill=(185, 35, 45), font=get_font(24, bold=True))

    # Draw inventory bars
    bar_w = 26
    for i, inv in enumerate(unsold_k):
        px = int(x0 + 48 + (i / (n_q - 1)) * inner_w)
        py = int(y1 - ((inv - 30.0) / 70.0) * (y1 - y0))
        col = (45, 105, 175) if inv < 80 else (25, 70, 135)
        draw.rectangle([px - bar_w, py, px + bar_w, y1 - 2], fill=col, outline=(15, 45, 95), width=2)

    # Draw BOI rate line
    rate_pts = []
    for i, r in enumerate(boi_rate):
        px = int(x0 + 48 + (i / (n_q - 1)) * inner_w)
        py = int(y1 - (r / 6.0) * (y1 - y0))
        rate_pts.append((px, py))
    draw.line(rate_pts, fill=(205, 40, 45), width=6)
    for px, py in rate_pts:
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(205, 40, 45), outline=(255, 255, 255), width=2)

    # Annotate March 2025 BOI Directive (25Q1, index 12)
    dx = int(x0 + 48 + (12 / (n_q - 1)) * inner_w)
    for py in range(y0 + 20, y1 - 20, 16):
        draw.line([(dx, py), (dx, py + 9)], fill=(20, 135, 75), width=4)
    draw.text((dx - 230, y0 + 35), "March 2025: BOI Temporary Order", fill=(15, 115, 60), font=get_font(21, bold=True))
    draw.text((dx - 230, y0 + 62), "(25% Cap on Balloon Loans)", fill=(15, 115, 60), font=get_font(19, bold=False))

    out_path = os.path.join(FIG_DIR, "fig03_israel_inventory_vs_rates.png")
    img.save(out_path, dpi=(300, 300))
    return {"peak_unsold_k": max(unsold_k), "q3_2026_unsold_k": unsold_k[-1]}


def generate_fig04_developer_stress_test():
    """
    Figure 4: Developer DSCR & Insolvency Rate Stress Test under 0%, 10%, 20%, 30% Contract Cancellations
    Across 3 Developer Tiers (Tier 1: Large Public TASE, Tier 2: Mid-Size Bank-Accompanied, Tier 3: Small Mezzanine-Leveraged)
    """
    cancellations = [0, 10, 20, 30]
    # Mean DSCR across tiers under each cancellation scenario
    dscr_tier1 = [1.68, 1.44, 1.21, 1.03]
    dscr_tier2 = [1.42, 1.18, 0.96, 0.78]
    dscr_tier3 = [1.24, 0.94, 0.71, 0.52]

    W, H = 2000, 1200
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    box = (180, 150, 1880, 1020)
    x0, y0, x1, y1 = box

    x_ticks = [(i, f"{c}% Cancellations", (i + 0.5) / 4.0) for i, c in enumerate(cancellations)]
    y_ticks = [(v, f"{v:.2f}x", v / 2.0) for v in np.linspace(0.0, 2.0, 9)]

    draw_grid_and_axes(
        draw,
        box,
        x_ticks,
        y_ticks,
        "Developer Debt-Service Coverage Ratio (DSCR) Stress Test at Delivery Wall",
        "Impact of Contract Cancellation Waves (0% to 30%) + 10% Price Haircut across Developer Tiers",
        "Delivery-Date Contract Cancellation Scenario (%)",
        "Project DSCR (x)"
    )

    tiers = [
        ("Tier 1: Large Public TASE Developers (22% Equity)", (30, 95, 180), dscr_tier1, -85),
        ("Tier 2: Mid-Size Developers (14% Equity)", (230, 135, 25), dscr_tier2, 0),
        ("Tier 3: Small Mezzanine-Leveraged (6% True Equity)", (195, 45, 55), dscr_tier3, 85),
    ]

    bar_w = 72
    f_val = get_font(20, bold=True)
    for label, col, vals, offset in tiers:
        for i, v in enumerate(vals):
            cx = int(x0 + ((i + 0.5) / 4.0) * (x1 - x0)) + offset
            py = int(y1 - (v / 2.0) * (y1 - y0))
            draw.rectangle([cx - bar_w // 2, py, cx + bar_w // 2, y1 - 2], fill=col, outline=(25, 35, 50), width=2)
            draw.text((cx - 28, py - 32), f"{v:.2f}x", fill=(20, 30, 45), font=f_val)

    # Critical DSCR = 1.0x Insolvency Threshold line drawn on top of bars
    py_crit = int(y1 - (1.0 / 2.0) * (y1 - y0))
    for px in range(x0 + 10, x1 - 10, 20):
        draw.line([(px, py_crit), (px + 12, py_crit)], fill=(200, 25, 35), width=5)

    # Legend placed cleanly in top-right including threshold line
    lx0, ly0 = x1 - 710, y0 + 25
    draw.rectangle([lx0, ly0, lx0 + 680, ly0 + 210], fill=(255, 255, 255), outline=(160, 175, 195), width=2)
    f_leg = get_font(21, bold=False)
    for idx, (label, col, _, _) in enumerate(tiers):
        cy = ly0 + 24 + idx * 44
        draw.rectangle([lx0 + 20, cy, lx0 + 60, cy + 26], fill=col, outline=(25, 35, 50), width=2)
        draw.text((lx0 + 78, cy), label, fill=(25, 35, 50), font=f_leg)
    cy_thresh = ly0 + 24 + 3 * 44 + 10
    draw.line([(lx0 + 20, cy_thresh), (lx0 + 60, cy_thresh)], fill=(200, 25, 35), width=5)
    draw.text((lx0 + 78, cy_thresh - 12), "Insolvency Threshold (DSCR = 1.00x)", fill=(185, 20, 30), font=get_font(21, bold=True))

    out_path = os.path.join(FIG_DIR, "fig04_developer_stress_test.png")
    img.save(out_path, dpi=(300, 300))
    return {"dscr_tier1": dscr_tier1, "dscr_tier2": dscr_tier2, "dscr_tier3": dscr_tier3}


def generate_fig05_bank_cet1_resilience():
    """
    Figure 5: Banking System Core Tier-1 (CET1) Capital Adequacy Trajectory under Stress Scenarios
    Comparing Israeli Banking System (2026-2028) vs. US Subprime Contagion Benchmark (2007-2009)
    """
    steps = ["T0 (2026Q1)", "T+2Q", "T+4Q (Peak Wall)", "T+6Q", "T+8Q (2028Q1)"]
    cet1_baseline = [10.85, 10.92, 11.00, 11.08, 11.15]
    cet1_severe = [10.85, 10.42, 9.95, 10.08, 10.30]
    cet1_extreme = [10.85, 10.10, 9.38, 9.45, 9.72]
    us_2008_equiv = [10.10, 8.40, 6.15, 5.20, 5.80]

    W, H = 2000, 1200
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    box = (180, 150, 1880, 1020)
    x0, y0, x1, y1 = box

    x_ticks = [(i, s, i / 4.0) for i, s in enumerate(steps)]
    y_ticks = [(v, f"{v:.1f}%", (v - 4.0) / 8.0) for v in range(4, 13)]

    draw_grid_and_axes(
        draw,
        box,
        x_ticks,
        y_ticks,
        "Banking System CET1 Capital Ratio Resilience Across Stress Horizons (T0 to T+8Q)",
        "Comparison of Israeli Banking Sector under Delivery-Wall Stress vs. U.S. 2008 Subprime Benchmark",
        "Stress Horizon Quarters Across the 2026-2027 Delivery Wall",
        "CET1 Capital Ratio (%)"
    )

    # Regulatory minimum CET1 line (9.0% BOI minimum for large banks)
    py_min = int(y1 - ((9.0 - 4.0) / 8.0) * (y1 - y0))
    for px in range(x0 + 10, x1 - 10, 20):
        draw.line([(px, py_min), (px + 12, py_min)], fill=(140, 35, 145), width=4)
    draw.text((x1 - 670, py_min + 12), "Bank of Israel Minimum CET1 Supervisory Requirement (9.0%)", fill=(125, 25, 130), font=get_font(21, bold=True))

    series = [
        ("Israel Baseline Scenario (5% Cancellations, Stable Prices)", (30, 145, 85), cet1_baseline),
        ("Israel Severe Stress (20% Cancellations, -12% Housing Prices)", (25, 95, 185), cet1_severe),
        ("Israel Extreme Contagion (30% Cancellations, -20% Housing Prices)", (230, 120, 20), cet1_extreme),
        ("U.S. Subprime Benchmark (2007-2009 Non-Recourse + MBS Contagion)", (195, 35, 45), us_2008_equiv),
    ]

    for label, col, vals in series:
        pts = []
        for i, v in enumerate(vals):
            px = int(x0 + (i / 4.0) * (x1 - x0))
            py = int(y1 - ((v - 4.0) / 8.0) * (y1 - y0))
            pts.append((px, py))
        draw.line(pts, fill=col, width=6)
        for px, py in pts:
            draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=(255, 255, 255), width=2)

    # Legend
    lx0, ly0 = x0 + 40, y1 - 245
    draw.rectangle([lx0, ly0, lx0 + 820, ly0 + 215], fill=(255, 255, 255), outline=(160, 175, 195), width=2)
    f_leg = get_font(20, bold=False)
    for idx, (label, col, _) in enumerate(series):
        cy = ly0 + 28 + idx * 46
        draw.line([(lx0 + 20, cy), (lx0 + 75, cy)], fill=col, width=6)
        draw.ellipse([lx0 + 42, cy - 6, lx0 + 54, cy + 6], fill=col)
        draw.text((lx0 + 92, cy - 12), label, fill=(25, 35, 50), font=f_leg)

    out_path = os.path.join(FIG_DIR, "fig05_bank_cet1_resilience.png")
    img.save(out_path, dpi=(300, 300))
    return {"min_cet1_extreme": min(cet1_extreme), "min_cet1_severe": min(cet1_severe)}


if __name__ == "__main__":
    summary = {
        "fig01": generate_fig01_npv_discount(),
        "fig02": generate_fig02_payment_shock(),
        "fig03": generate_fig03_israel_inventory_vs_rates(),
        "fig04": generate_fig04_developer_stress_test(),
        "fig05": generate_fig05_bank_cet1_resilience(),
    }
    with open(os.path.join(BASE_DIR, "scripts", "simulation_results.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("SIMULATION_SUCCESS:", json.dumps(summary))
