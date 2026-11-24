"""Shared plotting style + helpers for all figures (Agent 3 / PYTHON_VIZ_AGENT).

Palette: validated categorical order (blue, orange, aqua, ...) from the dataviz
reference palette; text in neutral ink, never series color. One y-axis per panel
(no dual axes) -- multi-measure figures use stacked small multiples.
"""
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# Report brand palette (A4 preamble; orchestrator directive 5). Navy/amber/green pass the
# all-pairs CVD check (worst dE 9.7); identity is ALSO carried by line style / markers / direct labels.
NAVY, STEEL, RED, AMBER, GREEN = "#1F3A5F", "#4A6FA5", "#B03A2E", "#D68910", "#1E8449"
SERIES = [NAVY, AMBER, GREEN, STEEL, RED]
LINESTYLES = ["-", (0, (5, 2)), (0, (1.5, 1.5))]
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8984"
GRID = "#e4e3df"
SURFACE = "#ffffff"
CRITICAL = RED   # reserved for regulatory thresholds only
NEUTRAL = "#b9b8b2"

DPI = 300
FIG_W = 6.3   # legacy default width (16 cm)

# D06: each figure is drawn at its PRINT width (fraction of 	extwidth in the .tex include), so that
# matplotlib point sizes = printed point sizes (scale ~1). Smallest text in any figure = 7.5 pt.
TEXTWIDTH_CM = 15.5   # A4, left 2.5 cm + right 3 cm margins
PRINT_FRAC = {"fig1": 0.62, "fig2": 0.60, "fig3": 0.55, "fig4": 0.62, "fig5": 0.85, "fig6": 0.65, "fig7": 0.85}


def print_width(key):
    """Figure width in inches for the figure's print width in the report."""
    return PRINT_FRAC[key] * TEXTWIDTH_CM / 2.54


def apply_style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK2,
        "axes.titlecolor": INK,
        "axes.titlesize": 9,
        "axes.titleweight": "bold",
        "axes.labelsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.frameon": False,
        "legend.fontsize": 7.5,
        "lines.linewidth": 1.5,
        "font.family": "DejaVu Sans",
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
        "savefig.facecolor": SURFACE,
    })


def save(fig, name):
    path = OUT / name
    fig.savefig(path)
    plt.close(fig)
    return path


def badge(ax, text="ILLUSTRATIVE SCENARIO\ncalibrated model, not observed data", loc="lower right", xy=None):
    """Visible label for any panel built on calibrated / scenario values (brief rule)."""
    x, ha = (0.99, "right") if "right" in loc else (0.01, "left")
    y, va = (0.02, "bottom") if "lower" in loc else (0.98, "top")
    if xy is not None:
        x, y = xy
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=7.5, color=INK2, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="#f6f5f2", ec=GRID, lw=0.8), zorder=10)


def verified_marker(ax, s, color, label="verified source point"):
    ax.plot(s.index, s.values, "o", ms=6, mfc=color, mec="white", mew=1.2, zorder=5, label=label)
