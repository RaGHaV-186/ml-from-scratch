"""Day 6: verify every hand-coded number in eda.py against NumPy / SciPy / pandas.

Written by Claude (AI help) on request. Raghav's functions are imported, never copied.
Run from PyCharm like eda.py. Every line should say OK.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# importing eda also adds b01_descriptive_stats/ to sys.path, so the day files import too
from eda import load_columns, frequency_table, ecdf
from day01_central_tendency import mean, median
from day02_spread import percentile, tukey_fences, tukey_outliers, zscore_outliers, sturges_bins, fd_bins
from day03_correlation import pearson, spearman
from day05_bayes_rv import bayes_posterior

CSV = Path(__file__).parent / "insurance.csv"
TOL = 1e-6
results = []


def check(name, mine, library, tol=TOL):
    ok = abs(float(mine) - float(library)) <= tol * max(1.0, abs(float(library)))
    results.append(ok)
    print(f"{'OK  ' if ok else 'FAIL'} {name:<38} mine={mine:<22.10g} library={library:.10g}")


def check_equal(name, mine, library):
    ok = mine == library
    results.append(ok)
    print(f"{'OK  ' if ok else 'FAIL'} {name:<38} mine={mine}  library={library}")


data = load_columns(CSV)
df = pd.read_csv(CSV)
charges = data["charges"]
arr = np.array(charges)

print("\n--- B. Centre ---")
for col in ["age", "bmi", "children", "charges"]:
    check(f"mean({col})", mean(data[col]), df[col].mean())
    check(f"median({col})", median(data[col]), df[col].median())
gap_mine = (mean(charges) - median(charges)) / median(charges) * 100
gap_lib = (df["charges"].mean() - df["charges"].median()) / df["charges"].median() * 100
check("H1: mean above median (%)", gap_mine, gap_lib)
check_equal("frequency_table(smoker)", frequency_table(data["smoker"]),
            df["smoker"].value_counts().to_dict())

print("\n--- C. Spread & outliers ---")
q1_lib, q3_lib = np.percentile(arr, 25), np.percentile(arr, 75)
check("percentile(charges, 25)", percentile(charges, 25), q1_lib)
check("percentile(charges, 75)", percentile(charges, 75), q3_lib)
iqr = q3_lib - q1_lib
low_lib, high_lib = q1_lib - 1.5 * iqr, q3_lib + 1.5 * iqr
low_mine, high_mine = tukey_fences(charges)
check("tukey lower fence", low_mine, low_lib)
check("tukey upper fence", high_mine, high_lib)
check_equal("tukey outlier count", len(tukey_outliers(charges)),
            int(((arr < low_lib) | (arr > high_lib)).sum()))
z_mine = len(zscore_outliers(charges))
z0 = int((np.abs((arr - arr.mean()) / arr.std(ddof=0)) > 3).sum())
z1 = int((np.abs((arr - arr.mean()) / arr.std(ddof=1)) > 3).sum())
ok = z_mine in (z0, z1)
results.append(ok)
print(f"{'OK  ' if ok else 'FAIL'} {'z-score outlier count':<38} mine={z_mine}  library ddof=0: {z0}, ddof=1: {z1}")
check_equal("sturges bins", sturges_bins(charges), len(np.histogram_bin_edges(arr, "sturges")) - 1)
check_equal("fd bins", fd_bins(charges), len(np.histogram_bin_edges(arr, "fd")) - 1)

print("\n--- D. Relationships ---")
for col in ["age", "bmi", "children"]:
    check(f"pearson({col}, charges)", pearson(data[col], charges),
          stats.pearsonr(df[col], df["charges"])[0])
    check(f"spearman({col}, charges)", spearman(data[col], charges),
          stats.spearmanr(df[col], df["charges"])[0])

print("\n--- E. Probability ---")
ct = pd.crosstab(df["sex"], df["smoker"])
table = frequency_table(list(zip(data["sex"], data["smoker"])))
for sex in ["male", "female"]:
    for smk in ["yes", "no"]:
        check_equal(f"count({sex}, smoker={smk})", table[(sex, smk)], int(ct.loc[sex, smk]))
p_male_lib = (df.loc[df["sex"] == "male", "smoker"] == "yes").mean()
p_female_lib = (df.loc[df["sex"] == "female", "smoker"] == "yes").mean()
check("P(smoker | male)", table[("male", "yes")] / (table[("male", "yes")] + table[("male", "no")]), p_male_lib)
check("P(smoker | female)", table[("female", "yes")] / (table[("female", "yes")] + table[("female", "no")]), p_female_lib)

q3 = percentile(charges, 75)
top_lib = df["charges"] > q3_lib
p_top_lib = (df.loc[top_lib, "smoker"] == "yes").mean()
table2 = frequency_table(list(zip(data["smoker"], [c > q3 for c in charges])))
p_direct = table2[("yes", True)] / (table2[("yes", True)] + table2[("no", True)])
counts = frequency_table(data["smoker"])
p_bayes = bayes_posterior(counts["yes"] / len(charges),
                          table2[("yes", True)] / counts["yes"],
                          table2[("no", True)] / counts["no"])
check("H4: P(smoker | top 25%), direct", p_direct, p_top_lib)
check("H4: P(smoker | top 25%), Bayes", p_bayes, p_top_lib)
check("ecdf(charges, 10000)", ecdf(charges, 10000), float((arr <= 10000).mean()))

print(f"\n{sum(results)}/{len(results)} checks passed")
