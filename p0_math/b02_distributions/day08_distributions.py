import math

import numpy as np


def bernoulli_pmf(k, p):
    if p > 1 or p < 0:
        raise ValueError

    if k == 1:
        return p
    elif k == 0:
        return 1 - p
    else:
        return 0


def binomial_pmf(k, n, p):
    if p > 1 or p < 0:
        raise ValueError
    if k < 0 or k > n:
        return 0

    return math.comb(n, k) * (p**k) * ((1 - p) ** (n - k))


def poisson_pmf(k, lam):
    if lam <= 0:
        raise ValueError
    if k < 0:
        return 0

    return (lam**k) * (math.exp(-lam)) / math.factorial(k)


def exponential_pdf(t, lam):
    if lam <= 0:
        raise ValueError

    if t < 0:
        return 0

    return lam * math.exp(-lam * t)


def exponential_cdf(t, lam):
    if lam <= 0:
        raise ValueError

    if t < 0:
        return 0

    return 1 - math.exp(-lam * t)


def uniform_pdf(x, a, b):
    if b <= a:
        raise ValueError
    if x >= a and x <= b:
        return 1 / (b - a)
    else:
        return 0


def normal_pdf(x, mu, sigma):
    if sigma <= 0:
        raise ValueError

    return math.exp(-((x - mu) ** 2) / (2 * sigma**2)) / (
        sigma * math.sqrt(2 * math.pi)
    )


def sample_bernoulli(p, size, rng):
    if p > 1 or p < 0:
        raise ValueError

    u = rng.random(size)
    return (u < p).astype(int)


def sample_exponential(lam, size, rng):
    if lam <= 0:
        raise ValueError

    u = rng.random(size)
    return -np.log(1 - u) / lam
