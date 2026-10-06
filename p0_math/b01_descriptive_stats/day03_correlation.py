import numpy as np

def covariance(x,y,ddof=1):
    x = np.array(x)
    y = np.array(y)
    n = len(x)
    if len(x) != len(y):
        raise ValueError("Both arrays should be of equal length")
    if n-ddof <= 0:
        raise ValueError("n-ddoff must be positive")

    dx = x -x.mean()
    dy = y - y.mean()

    pair_sum = (dx * dy).sum()

    return pair_sum/(n-ddof)

def pearson(x,y):
    x = np.array(x)
    y = np.array(y)
    x_std = x.std(ddof=1)
    y_std = y.std(ddof=1)
    if x_std == 0 or y_std == 0:
        raise ValueError("the standard deviation is zero")
    return (covariance(x,y))/(x_std * y_std)

def rank(x):
    x = np.array(x)
    s = np.sort(x)
    ranks = []
    for v in x:
        positions = np.where(s == v)[0]
        ranks.append(positions.mean() + 1)
    return np.array(ranks)

def spearman(x,y):
    return pearson(rank(x),rank(y))