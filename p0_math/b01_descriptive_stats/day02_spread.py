"""Day 2 - measures of spread, built from scratch.

Covers: variance/std (two-pass, naive shortcut, Welford), percentiles,
IQR, Tukey and z-score outliers, histograms, bin rules, boxplots.
"""
import bisect
import math
import random

from day01_central_tendency import mean


# ---------------------------------------------------------------------------
# Variance and standard deviation
# ---------------------------------------------------------------------------
def variance(x, ddof=0):
    """Two-pass variance. ddof = 'delta degrees of freedom': divide by len(x) - ddof.

    ddof=0 -> population variance, ddof=1 -> sample variance
    (one degree of freedom is used up by estimating the mean).
    """
    n = len(x)
    if n - ddof <= 0:
        raise ValueError(f"Need len(x) - ddof > 0, got len(x)={n}, ddof={ddof}.")
    avg = mean(x)
    sum_of_squares = 0
    for num in x:
        sum_of_squares += (num - avg) ** 2
    return sum_of_squares / (n - ddof)


def std(x, ddof=0):
    """Standard deviation: square root of the variance, back in the data's units."""
    return math.sqrt(variance(x, ddof))


def variance_naive(x):
    """Shortcut formula mean(x^2) - mean(x)^2 (population).

    Correct on paper, numerically unsafe: subtracting two huge, nearly equal
    numbers loses the small difference (catastrophic cancellation).
    """
    n = len(x)
    if n == 0:
        raise ValueError("Need at least one value.")
    mean_of_squares = sum(v * v for v in x) / n
    return mean_of_squares - mean(x) ** 2


def welford(x, ddof=0):
    """One-pass, numerically safe variance (Welford's online algorithm).

    Keeps only a 'notepad' of three numbers: k (count), running mean, M2
    (running sum of squared deviations). Works on any iterable, incl. streams.
    """
    k, running_mean, m2 = 0, 0.0, 0.0
    for value in x:
        k += 1                                  # 1. count it
        delta = value - running_mean            # 2. gap to the OLD mean
        running_mean += delta / k               # 3. nudge the mean
        m2 += delta * (value - running_mean)    # 4. old gap x NEW gap
    if k - ddof <= 0:
        raise ValueError(f"Need count - ddof > 0, got count={k}, ddof={ddof}.")
    return m2 / (k - ddof)


# ---------------------------------------------------------------------------
# Percentiles, IQR, outliers
# ---------------------------------------------------------------------------
def percentile(x, q):
    """q-th percentile (q in [0, 100]) with linear interpolation (NumPy's default).

    Position h = (n - 1) * q/100 on the sorted data (0-indexed); if h falls
    between two positions, walk the fractional part of the gap.
    """
    if len(x) == 0:
        raise ValueError("Need at least one value.")
    if not 0 <= q <= 100:
        raise ValueError(f"q must be in [0, 100], got {q}.")
    s = sorted(x)
    h = (len(s) - 1) * q / 100
    lower = math.floor(h)
    upper = min(lower + 1, len(s) - 1)
    fraction = h - lower
    return s[lower] + fraction * (s[upper] - s[lower])


def iqr(x):
    """Interquartile range Q3 - Q1: width of the middle half of the data."""
    return percentile(x, 75) - percentile(x, 25)


def tukey_fences(x, k=1.5):
    """Return (lower_fence, upper_fence) = (Q1 - k*IQR, Q3 + k*IQR)."""
    q1, q3 = percentile(x, 25), percentile(x, 75)
    spread = q3 - q1
    return q1 - k * spread, q3 + k * spread


def tukey_outliers(x, k=1.5):
    """Indices of values outside Tukey's fences (robust: based on quartiles)."""
    low, high = tukey_fences(x, k)
    return [i for i, v in enumerate(x) if v < low or v > high]


def zscore_outliers(x, t=3.0):
    """Indices of values with |z| > t. Not robust: the outlier inflates the std
    it is measured with (masking). With n values, |z| can never exceed (n-1)/sqrt(n).
    """
    avg, sd = mean(x), std(x)
    if sd == 0:
        return []
    return [i for i, v in enumerate(x) if abs((v - avg) / sd) > t]


# ---------------------------------------------------------------------------
# Histograms and bin rules
# ---------------------------------------------------------------------------
def histogram(x, bins=10):
    """Counts and edges, matching np.histogram.

    bins: int (equal-width bins over [min, max]) or a sorted list of edges.
    Every bin is half-open [a, b) except the LAST, which is closed [a, b],
    so the maximum value is counted.
    """
    if isinstance(bins, int):
        if bins < 1:
            raise ValueError("bins must be >= 1.")
        lo, hi = min(x), max(x)
        if lo == hi:                     # all values equal: widen like NumPy
            lo, hi = lo - 0.5, hi + 0.5
        width = (hi - lo) / bins
        edges = [lo + i * width for i in range(bins)] + [hi]
    else:
        edges = list(bins)
    counts = [0] * (len(edges) - 1)
    for v in x:
        if v < edges[0] or v > edges[-1]:
            continue                     # outside the range: ignored
        if v == edges[-1]:
            counts[-1] += 1              # last bin is closed on the right
        else:
            counts[bisect.bisect_right(edges, v) - 1] += 1
    return counts, edges


def sturges_bins(x):
    """Sturges: ceil(log2 n) + 1 bins. Simple; too few bins for big or skewed data."""
    return math.ceil(math.log2(len(x))) + 1


def fd_bins(x):
    """Freedman-Diaconis: width = 2 * IQR * n^(-1/3); bins = ceil(range / width).
    Uses the IQR, so it is robust to outliers."""
    width = 2 * iqr(x) * len(x) ** (-1 / 3)
    data_range = max(x) - min(x)
    if width == 0 or data_range == 0:
        return 1
    return math.ceil(data_range / width)


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
def draw_boxplot(ax, x, k=1.5, position=1, width=0.5):
    """Draw a Tukey boxplot from our own quartiles and whisker logic."""
    from matplotlib.patches import Rectangle

    q1, med, q3 = percentile(x, 25), percentile(x, 50), percentile(x, 75)
    low, high = tukey_fences(x, k)
    inside = [v for v in x if low <= v <= high]
    w_low, w_high = min(inside), max(inside)       # whiskers stop at real data
    outliers = [v for v in x if v < low or v > high]
    left = position - width / 2
    ax.add_patch(Rectangle((left, q1), width, q3 - q1, fill=False, linewidth=1.5))
    ax.plot([left, left + width], [med, med], linewidth=2, color="tab:orange")
    ax.plot([position, position], [q3, w_high], color="black")
    ax.plot([position, position], [w_low, q1], color="black")
    for w in (w_low, w_high):
        ax.plot([position - width / 4, position + width / 4], [w, w], color="black")
    ax.scatter([position] * len(outliers), outliers, facecolors="none", edgecolors="black")


def make_plots(path="day02_plots.png"):
    import matplotlib.pyplot as plt

    random.seed(42)
    rents = [math.exp(random.gauss(math.log(650), 0.35)) for _ in range(1000)]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, rule, name in [(axes[0], sturges_bins, "Sturges"), (axes[1], fd_bins, "Freedman-Diaconis")]:
        counts, edges = histogram(rents, rule(rents))
        widths = [edges[i + 1] - edges[i] for i in range(len(counts))]
        ax.bar(edges[:-1], counts, width=widths, align="edge", edgecolor="white")
        ax.set_title(f"{name}: {len(counts)} bins")
        ax.set_xlabel("Rent (EUR / month)")
        ax.set_ylabel("Count")

    draw_boxplot(axes[2], rents, position=1)
    axes[2].boxplot(rents, positions=[2], whis=1.5, widths=0.5)
    axes[2].set_xticks([1, 2], ["ours", "plt.boxplot"])
    axes[2].set_xlim(0.4, 2.6)
    axes[2].set_title("Boxplot: ours vs matplotlib")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print(f"Plots saved to {path}")
    plt.show()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def run_tests():
    import numpy as np

    data = [2, 4, 4, 4, 5, 5, 7, 9]

    # Variance / std: known answers + random arrays vs NumPy
    for xs, ddof, expected in [([1, 2, 6], 0, 14 / 3), ([1, 2, 6], 1, 7.0),
                               (data, 0, 4.0), (data, 1, 32 / 7)]:
        assert math.isclose(variance(xs, ddof), expected)
    assert math.isclose(std(data), 2.0)
    random.seed(0)
    arrays = [[random.uniform(-100, 100) for _ in range(random.randint(2, 50))] for _ in range(100)]
    for xs in arrays:
        for ddof in (0, 1):
            assert math.isclose(variance(xs, ddof), np.var(xs, ddof=ddof), rel_tol=1e-9)
            assert math.isclose(std(xs, ddof), np.std(xs, ddof=ddof), rel_tol=1e-9)
    for xs, ddof in [([5], 1), ([5, 6], 3), ([], 0)]:
        try:
            variance(xs, ddof)
            raise AssertionError("expected ValueError")
        except ValueError:
            pass
    print("variance / std ............ OK")

    # Naive shortcut vs two-pass vs Welford on huge numbers
    small = [4, 7, 13, 16]
    huge = [1e9 + v for v in small]
    print(f"  small data: naive={variance_naive(small)}, two-pass={variance(small)}, welford={welford(small)}")
    print(f"  huge data:  naive={variance_naive(huge)}, two-pass={variance(huge)}, welford={welford(huge)}")
    assert math.isclose(variance_naive(small), 22.5)
    assert not math.isclose(variance_naive(huge), 22.5)        # shortcut breaks
    assert math.isclose(variance(huge), 22.5)
    assert math.isclose(welford(huge), 22.5)
    print("naive fails, two-pass + Welford survive ... OK")

    # Welford: worked example + random arrays
    assert math.isclose(welford([10, 4, 7, 11]), 7.5)
    assert math.isclose(welford([10, 4, 7, 11], ddof=1), 10.0)
    for xs in arrays:
        for ddof in (0, 1):
            assert math.isclose(welford(xs, ddof), variance(xs, ddof), rel_tol=1e-9)
    print("welford ................... OK")

    # Percentiles and IQR
    assert percentile(data, 25) == 4 and percentile(data, 50) == 4.5 and percentile(data, 75) == 5.5
    assert iqr(data) == 1.5
    for xs in arrays + [[3.0], [1, 1, 1, 2]]:
        for q in (0, 10, 25, 33.3, 50, 75, 90, 100):
            assert math.isclose(percentile(xs, q), float(np.percentile(xs, q)), rel_tol=1e-9, abs_tol=1e-12)
    print("percentile / iqr .......... OK")

    # Outliers
    tukey = [data[i] for i in tukey_outliers(data)]
    zs = [data[i] for i in zscore_outliers(data)]
    print(f"  today's data: Tukey -> {tukey}, z-score -> {zs}")
    assert tukey == [9] and zs == []
    scores = [3, 5, 6, 8, 10, 12, 13, 15, 30]
    assert [scores[i] for i in tukey_outliers(scores)] == [30]
    print("outliers .................. OK")

    # Histograms and bin rules
    for xs in arrays:
        for b in (1, 5, 13):
            counts, edges = histogram(xs, b)
            np_counts, np_edges = np.histogram(xs, bins=b)
            assert counts == list(np_counts) and np.allclose(edges, np_edges)
        custom = [-100, -50, 0, 25, 100]
        assert histogram(xs, custom)[0] == list(np.histogram(xs, bins=custom)[0])
    assert sturges_bins(data) == 4 and fd_bins(data) == 5
    assert sturges_bins(data) == len(np.histogram_bin_edges(data, "sturges")) - 1
    assert fd_bins(data) == len(np.histogram_bin_edges(data, "fd")) - 1
    print(f"  today's data: Sturges -> {sturges_bins(data)} bins, FD -> {fd_bins(data)} bins")
    print("histogram / bin rules ..... OK")

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
    make_plots()