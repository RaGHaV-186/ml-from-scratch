import numpy as np
import pytest
from scipy import stats
from day08_recall import percentile, welford, rank

rng = np.random.default_rng(8)

# ---------- percentile ----------
def test_percentile_known():
    data = [55, 3, 21, 8, 30, 10, 14]          # unsorted on purpose
    assert percentile(data, 0.25) == pytest.approx(9.0)
    assert percentile(data, 0.5) == pytest.approx(14.0)
    assert percentile(data, 0.75) == pytest.approx(25.5)
    assert percentile(data, 0) == pytest.approx(3)
    assert percentile(data, 1) == pytest.approx(55)

def test_percentile_does_not_mutate():
    data = [5, 1, 9]
    percentile(data, 0.5)
    assert data == [5, 1, 9]

def test_percentile_errors():
    with pytest.raises(ValueError):
        percentile([], 0.5)
    with pytest.raises(ValueError):
        percentile([1, 2], 1.5)

def test_percentile_random():
    for _ in range(1000):
        x = rng.normal(size=rng.integers(1, 30)).tolist()
        q = rng.uniform()
        assert percentile(x, q) == pytest.approx(np.percentile(x, 100 * q))

# ---------- welford ----------
def test_welford_known():
    m, v = welford([4, 7, 13, 16])
    assert m == pytest.approx(10.0)
    assert v == pytest.approx(30.0)
    _, v0 = welford([4, 7, 13, 16], ddof=0)
    assert v0 == pytest.approx(22.5)

def test_welford_large_offset():              # the catastrophic-cancellation case
    m, v = welford([1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16])
    assert m == pytest.approx(1e9 + 10)
    assert v == pytest.approx(30.0)

def test_welford_errors():
    with pytest.raises(ValueError):
        welford([5.0])                         # n - ddof = 0
    with pytest.raises(ValueError):
        welford([5, 6], ddof=3)

def test_welford_random():
    for _ in range(1000):
        x = rng.normal(50, 10, size=rng.integers(2, 50))
        m, v = welford(x.tolist())
        assert m == pytest.approx(x.mean())
        assert v == pytest.approx(x.var(ddof=1))

# ---------- rank ----------
def test_rank_ties():
    assert rank([7, 3, 7, 1, 7]) == pytest.approx([4, 2, 4, 1, 4])
    assert rank([10, 20, 20, 5]) == pytest.approx([2, 3.5, 3.5, 1])

def test_rank_random():
    for _ in range(1000):
        x = rng.integers(0, 6, size=rng.integers(1, 20)).tolist()   # lots of ties
        assert rank(x) == pytest.approx(stats.rankdata(x).tolist())