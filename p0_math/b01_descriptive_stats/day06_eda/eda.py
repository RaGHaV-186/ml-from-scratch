import pandas as pd

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

if __name__ == "__main__":
    data = load_columns("insurance.csv")
    print(len(data["age"]), list(data.keys()))
    for name, values in data.items():
        print(name, column_type(values), values[:3])