import math
import numpy as np


def percentile(x, q):
    """q in [0, 1]. Linear interpolation with h = (n-1)q, 0-based."""
    if len(x) == 0:
        raise ValueError("Need at least one value.")
    if not 0 <= q <= 1:
        raise ValueError(f"q must be in [0, 1], got {q}.")
    s = sorted(x)                      # new list: input stays unchanged
    h = (len(s) - 1) * q
    lower = math.floor(h)
    upper = min(lower + 1, len(s) - 1)
    fraction = h - lower
    return s[lower] + fraction * (s[upper] - s[lower])


def welford(x, ddof=1):
    """One pass. Returns (mean, variance)."""
    k, running_mean, m2 = 0, 0.0, 0.0
    for value in x:
        k += 1
        delta = value - running_mean            # uses the OLD mean
        running_mean += delta / k
        m2 += delta * (value - running_mean)    # old mean × new mean
    if k - ddof <= 0:
        raise ValueError(f"Need count - ddof > 0, got count={k}, ddof={ddof}.")
    return running_mean, m2 / (k - ddof)


def rank(x):
    """Ranks starting at 1; ties get the average rank."""
    x = np.array(x)
    s = np.sort(x)
    ranks = []
    for v in x:
        positions = np.where(s == v)[0]         # all sorted positions holding v
        ranks.append(positions.mean() + 1)
    return np.array(ranks)