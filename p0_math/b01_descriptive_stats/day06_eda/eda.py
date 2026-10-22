import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from day01_central_tendency import mean, median, mode
from day02_spread import tukey_outliers, zscore_outliers, sturges_bins, fd_bins, tukey_fences
from day03_correlation import pearson, spearman
from day02_spread import percentile
from day05_bayes_rv import bayes_posterior




def load_columns(path):
    df = pd.read_csv(path)
    data = {}

    for name in df.columns:
        data[name] = df[name].tolist()

    return data

def column_type(values):
    if isinstance(values[0], str):
        return "categorical"
    elif all(isinstance(v, int) for v in values):
        return "discrete"
    else:
        return "continuous"

def frequency_table(values):
    counts = {}
    for v in values:
        if v in counts:
            counts[v] += 1
        else:
            counts[v] = 1
    return counts

def ecdf(x, t):
    count = 0
    for v in x:
        if v <= t:
            count += 1
    return count / len(x)

if __name__ == "__main__":
    data = load_columns("insurance.csv")
    print(len(data["age"]), list(data.keys()))
    for name, values in data.items():
        print(name, column_type(values), values[:3])

    mean_charges = mean(data["charges"])
    median_charges = median(data["charges"])

    result = ((mean_charges-median_charges)/median_charges) * 100
    print(result)
    print(frequency_table(data["smoker"]))
    print(frequency_table(data["region"]))

    for name, values in data.items():
        if column_type(values) == "categorical":
            print(name, frequency_table(values))
        else:
            print(name,
                  round(mean(values), 2),
                  round(median(values), 2),
                  mode(values))

    charges = data["charges"]

    print("fences:", tukey_fences(charges))
    print("tukey outliers:", len(tukey_outliers(charges)))
    print("z-score outliers:", len(zscore_outliers(charges)))
    print("sturges bins:", sturges_bins(charges))
    print("fd bins:", fd_bins(charges))

    df = pd.read_csv("insurance.csv")
    print(df[df["charges"] == 1639.5631])

    for col in ["age", "bmi", "children"]:
        p = pearson(data[col],charges)
        s = spearman(data[col],charges)
        print(col, round(p, 3), round(s, 3))

    pairs = list(zip(data["sex"], data["smoker"]))
    table = frequency_table(pairs)
    print(table)
    p_smoke_male = table[("male", "yes")] / (table[("male", "yes")] + table[("male","no" )])
    p_smoke_female = table[("female","yes")] / (table[("female", "yes")] + table[("female", "no")])
    print(round(p_smoke_male * 100, 1), round(p_smoke_female * 100, 1))

    q3 = percentile(charges, 75)
    print("Q3:", q3)
    is_top = [c > q3 for c in charges]                 # True / False per person
    table2 = frequency_table(list(zip(data["smoker"], is_top)))
    print(table2)
    p_direct = table2[("yes", True)] / (table2[("yes", True)] + table2[("no", True)])
    prior = p_direct / 1338  # P(smoker)
    smoker_counts = frequency_table(data["smoker"])
    prior = smoker_counts["yes"] / len(charges)
    p_top_given_smoker = table2[("yes", True)] / smoker_counts["yes"]
    p_top_given_non = table2[("no", True)] / smoker_counts["no"]
    p_bayes = bayes_posterior(prior, p_top_given_smoker, p_top_given_non)

    print(round(p_direct, 4), round(p_bayes, 4))

    print("P(charges <= 10000):", round(ecdf(charges, 10000), 3))
