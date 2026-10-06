"""Tests for day03_correlation.py.

Put this file next to day03_correlation.py and run:
    uv run python test_day03_correlation.py

Functions you haven't written yet are skipped, so you can run this
after each function you finish.
"""
import numpy as np
from scipy import stats

import day03_correlation as d3

STUDENTS_X = [1, 2, 3, 4, 5]
STUDENTS_Y = [2, 3, 5, 6, 9]
OUTLIER_Y = [2, 3, 5, 6, 100]


def raises(fn, *args, **kwargs):
    """True if fn(*args, **kwargs) raises ValueError."""
    try:
        fn(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_covariance():
    cov = d3.covariance
    # hand examples from the lesson
    assert np.isclose(cov(STUDENTS_X, STUDENTS_Y), 4.25)
    assert np.isclose(cov([1, 2, 3], [6, 4, 2]), -2.0)
    assert np.isclose(cov([1, 2, 3], [6, 4, 2], ddof=0), -4 / 3)
    # variance = covariance with itself (Day 2 link)
    assert np.isclose(cov(STUDENTS_X, STUDENTS_X), 2.5)
    # scaling: cov(a*x, b*y) = a*b*cov(x, y)  ->  x*10, y*100 gives -2 * 1000
    assert np.isclose(cov([10, 20, 30], [600, 400, 200]), -2000.0)
    # symmetric
    assert np.isclose(cov(STUDENTS_X, STUDENTS_Y), cov(STUDENTS_Y, STUDENTS_X))
    # must not modify the caller's data
    a = np.array([1.0, 2.0, 3.0])
    cov(a, [6, 4, 2])
    assert np.array_equal(a, [1.0, 2.0, 3.0])
    # errors
    assert raises(cov, [1, 2, 3], [1, 2])          # unequal lengths
    assert raises(cov, [5, 6], [1, 2], ddof=2)     # n - ddof = 0
    assert raises(cov, [5, 6], [1, 2], ddof=3)     # n - ddof < 0
    print("covariance: all tests passed")


def test_pearson():
    r = d3.pearson
    # hand examples: 17 / sqrt(10 * 30) ≈ 0.9815, and a perfect downward line
    assert np.isclose(r(STUDENTS_X, STUDENTS_Y), 17 / np.sqrt(10 * 30))
    assert np.isclose(r([1, 2, 3], [6, 4, 2]), -1.0)
    # units cancel: metres -> cm leaves r unchanged
    assert np.isclose(r(STUDENTS_X, STUDENTS_Y),
                      r(STUDENTS_X, [v * 100 for v in STUDENTS_Y]))
    # flipping the sign of y flips the sign of r
    assert np.isclose(r(STUDENTS_X, [-v for v in STUDENTS_Y]),
                      -r(STUDENTS_X, STUDENTS_Y))
    # outlier drags Pearson down: 199 / sqrt(10 * 7382.8) ≈ 0.732
    assert np.isclose(r(STUDENTS_X, OUTLIER_Y), 199 / np.sqrt(10 * 7382.8))
    # r only sees straight lines: y = x^2 on [-2..2] gives r = 0
    assert np.isclose(r([-2, -1, 0, 1, 2], [4, 1, 0, 1, 4]), 0.0)
    # errors
    assert raises(r, [1, 2, 3], [4, 4, 4])         # constant column, std = 0
    assert raises(r, [1, 2, 3], [1, 2])            # unequal lengths
    print("pearson: all tests passed")


def test_rank():
    rk = d3.rank
    assert np.allclose(rk([10, 20, 30, 40]), [1, 2, 3, 4])
    assert np.allclose(rk([50, 10, 30]), [3, 1, 2])          # original order kept
    assert np.allclose(rk([5, 7, 7, 9]), [1, 2.5, 2.5, 4])   # tie -> average
    assert np.allclose(rk([3, 3, 3]), [2, 2, 2])             # all tied
    assert np.allclose(rk([2, 1, 2, 1]), [3.5, 1.5, 3.5, 1.5])
    print("rank: all tests passed")


def test_spearman():
    rho = d3.spearman
    assert np.isclose(rho([10, 20, 30, 40], [3, 1, 4, 2]), 0.0)   # hand exercise
    assert np.isclose(rho(STUDENTS_X, OUTLIER_Y), 1.0)            # outlier ignored
    assert np.isclose(rho([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]), 1.0)  # curved but monotonic
    assert np.isclose(rho([1, 2, 3, 4], [40, 30, 20, 10]), -1.0)
    print("spearman: all tests passed")


def test_against_libraries(trials=1000):
    rng = np.random.default_rng(0)
    for _ in range(trials):
        n = int(rng.integers(3, 50))
        x = rng.normal(size=n)
        y = 0.5 * x + rng.normal(size=n)
        assert np.isclose(d3.covariance(x, y), np.cov(x, y)[0, 1])
        assert np.isclose(d3.covariance(x, y, ddof=0), np.cov(x, y, ddof=0)[0, 1])
        assert np.isclose(d3.pearson(x, y), np.corrcoef(x, y)[0, 1])
        assert np.isclose(d3.pearson(x, y), stats.pearsonr(x, y)[0])

        # small integers -> lots of ties, the hard case for rank/spearman
        xi = rng.integers(0, 5, size=n)
        yi = rng.integers(0, 5, size=n)
        assert np.allclose(d3.rank(xi), stats.rankdata(xi))
        if np.std(xi) > 0 and np.std(yi) > 0:
            assert np.isclose(d3.spearman(xi, yi), stats.spearmanr(xi, yi)[0])
    print(f"library check: {trials} random trials matched NumPy and SciPy")


if __name__ == "__main__":
    tests = [
        ("covariance", test_covariance),
        ("pearson", test_pearson),
        ("rank", test_rank),
        ("spearman", test_spearman),
    ]
    for name, test in tests:
        if hasattr(d3, name):
            test()
        else:
            print(f"{name}: not written yet, skipped")

    if all(hasattr(d3, name) for name, _ in tests):
        test_against_libraries()
        print("\nAll Day 3 tests passed")
    else:
        print("\nLibrary check runs once all four functions exist")