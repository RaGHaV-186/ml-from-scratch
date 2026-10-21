import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from day01_central_tendency import mean, median, mode
from day02_spread import tukey_outliers, zscore_outliers, sturges_bins, fd_bins, tukey_fences
from day03_correlation import pearson, spearman

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