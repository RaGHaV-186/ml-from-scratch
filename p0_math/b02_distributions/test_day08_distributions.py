import math

import numpy as np
import pytest
from day08_distributions import (
    bernoulli_pmf,
    binomial_pmf,
    exponential_cdf,
    exponential_pdf,
    normal_pdf,
    poisson_pmf,
    sample_bernoulli,
    sample_exponential,
    uniform_pdf,
)
from scipy import stats

rng = np.random.default_rng(8)


# ---------- known values from today's problems ----------
def test_known_values():
    assert bernoulli_pmf(1, 0.95) == pytest.approx(0.95)
    assert bernoulli_pmf(0, 0.95) == pytest.approx(0.05)
    assert binomial_pmf(9, 10, 0.95) == pytest.approx(0.3151, abs=1e-4)
    assert poisson_pmf(0, 4) == pytest.approx(math.exp(-4))
    assert exponential_cdf(0.5, 4) == pytest.approx(1 - math.exp(-2))
    assert uniform_pdf(5, 3, 7) == pytest.approx(0.25)
    assert normal_pdf(5, 5, 0.5) == pytest.approx(1 / (0.5 * math.sqrt(2 * math.pi)))


# ---------- impossible values get probability 0 ----------
def test_outside_support_is_zero():
    assert bernoulli_pmf(2, 0.3) == 0
    assert binomial_pmf(-1, 10, 0.3) == 0
    assert binomial_pmf(11, 10, 0.3) == 0
    assert poisson_pmf(-1, 3) == 0
    assert exponential_pdf(-1, 2) == 0
    assert exponential_cdf(-1, 2) == 0
    assert uniform_pdf(2.9, 3, 7) == 0
    assert uniform_pdf(7.1, 3, 7) == 0


# ---------- bad settings raise errors ----------
def test_invalid_parameters():
    for f, args in [
        (bernoulli_pmf, (1, 1.5)),
        (binomial_pmf, (1, 10, -0.1)),
        (poisson_pmf, (1, 0)),
        (exponential_pdf, (1, -2)),
        (uniform_pdf, (5, 7, 3)),
        (normal_pdf, (0, 0, 0)),
    ]:
        with pytest.raises(ValueError):
            f(*args)


# ---------- probabilities add up to 1 ----------
def test_pmfs_sum_to_one():
    assert sum(binomial_pmf(k, 20, 0.3) for k in range(21)) == pytest.approx(1)
    assert sum(poisson_pmf(k, 4) for k in range(60)) == pytest.approx(1)


# ---------- 1000 random checks against SciPy ----------
def test_against_scipy():
    for _ in range(1000):
        n = int(rng.integers(1, 40))
        p = rng.uniform(0.01, 0.99)
        k = int(rng.integers(0, n + 1))
        lam = rng.uniform(0.1, 10)
        t = rng.uniform(0, 3)
        a = rng.uniform(-5, 5)
        b = a + rng.uniform(0.1, 10)
        x = rng.uniform(a - 1, b + 1)
        mu, sigma = rng.uniform(-5, 5), rng.uniform(0.1, 5)
        z = rng.uniform(-10, 10)

        assert binomial_pmf(k, n, p) == pytest.approx(stats.binom.pmf(k, n, p))
        assert poisson_pmf(k, lam) == pytest.approx(stats.poisson.pmf(k, lam))
        assert exponential_pdf(t, lam) == pytest.approx(
            stats.expon.pdf(t, scale=1 / lam)
        )
        assert exponential_cdf(t, lam) == pytest.approx(
            stats.expon.cdf(t, scale=1 / lam)
        )
        assert uniform_pdf(x, a, b) == pytest.approx(
            stats.uniform.pdf(x, loc=a, scale=b - a)
        )
        assert normal_pdf(z, mu, sigma) == pytest.approx(
            stats.norm.pdf(z, mu, sigma), abs=1e-12
        )


# ---------- samplers built from Uniform(0, 1) ----------
def test_sample_bernoulli():
    s = sample_bernoulli(0.3, 100_000, np.random.default_rng(1))
    assert set(np.unique(s)) <= {0, 1}
    assert s.mean() == pytest.approx(0.3, abs=0.01)
    assert s.var() == pytest.approx(0.3 * 0.7, abs=0.01)


def test_sample_exponential():
    s = sample_exponential(4, 100_000, np.random.default_rng(2))
    assert (s >= 0).all()
    assert s.mean() == pytest.approx(1 / 4, rel=0.02)
    assert (s > 0.5).mean() == pytest.approx(math.exp(-2), abs=0.01)  # P(wait > t)


def test_samplers_use_the_rng():  # same seed -> same numbers
    a = sample_exponential(4, 10, np.random.default_rng(42))
    b = sample_exponential(4, 10, np.random.default_rng(42))
    assert np.array_equal(a, b)
