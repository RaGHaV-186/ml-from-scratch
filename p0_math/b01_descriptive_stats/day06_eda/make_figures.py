"""Day 6: figures for the EDA report.

Drawing code written by Claude (AI help) on request. The number of histogram bins comes
from Raghav's fd_bins (day02_spread.py); matplotlib only draws.
Saves 4 PNGs into figures/. Run from PyCharm like eda.py.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # save files, don't open windows
import matplotlib.pyplot as plt

from eda import load_columns
from day01_central_tendency import mean, median
from day02_spread import fd_bins, tukey_fences

HERE = Path(__file__).parent
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)

data = load_columns(HERE / "insurance.csv")
charges = data["charges"]
is_smoker = [s == "yes" for s in data["smoker"]]
SMOKER, NON = "#e05a47", "#0d9488"  # coral / teal

# 1. Histogram of charges with mean and median
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(charges, bins=fd_bins(charges), color="#94a3b8", edgecolor="white")
ax.axvline(median(charges), color=NON, lw=2, label=f"median {median(charges):,.0f}")
ax.axvline(mean(charges), color=SMOKER, lw=2, ls="--", label=f"mean {mean(charges):,.0f}")
ax.set(title="Medical charges: right-skewed (FD bins)", xlabel="charges ($)", ylabel="people")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "01_charges_histogram.png", dpi=150)

# 2. Boxplot of charges: non-smokers vs smokers, with the overall Tukey upper fence
fig, ax = plt.subplots(figsize=(6, 4.5))
groups = [[c for c, s in zip(charges, is_smoker) if not s], [c for c, s in zip(charges, is_smoker) if s]]
box = ax.boxplot(groups, whis=1.5, patch_artist=True)
ax.set_xticks([1, 2], [f"non-smoker (n={len(groups[0])})", f"smoker (n={len(groups[1])})"])
for patch, colour in zip(box["boxes"], [NON, SMOKER]):
    patch.set_facecolor(colour)
    patch.set_alpha(0.45)
ax.axhline(tukey_fences(charges)[1], color="grey", ls=":", label="overall Tukey upper fence")
ax.set(title="Charges by smoking status", ylabel="charges ($)")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "02_charges_by_smoker_boxplot.png", dpi=150)


# 3 + 4. Scatter plots coloured by smoker (age tests H3, bmi tests the H3b U-shape)
def scatter(col, filename, title):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for flag, colour, label in [(False, NON, "non-smoker"), (True, SMOKER, "smoker")]:
        xs = [x for x, s in zip(data[col], is_smoker) if s == flag]
        ys = [c for c, s in zip(charges, is_smoker) if s == flag]
        ax.scatter(xs, ys, s=10, alpha=0.6, color=colour, label=label)
    ax.set(title=title, xlabel=col, ylabel="charges ($)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=150)


scatter("age", "03_age_vs_charges.png", "Age vs charges, coloured by smoking status")
scatter("bmi", "04_bmi_vs_charges.png", "BMI vs charges: is it U-shaped? (H3b)")

print("Saved:", *sorted(p.name for p in OUT.glob("*.png")), sep="\n  ")
