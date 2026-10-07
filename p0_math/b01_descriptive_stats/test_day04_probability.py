"""Tests for day04_probability.py (Day 4: counting, conditional probability, Monte Carlo).

Put this file next to day04_probability.py and run:
    uv run pytest test_day04_probability.py -v

Simulation tests use a fixed seed and a tolerance of about 4-5 standard errors,
so a correct implementation passes essentially always.
"""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day04_probability import (  # noqa: E402
    combinations,
    factorial,
    p_at_least_one,
    p_exactly_k_heads,
    permutations,
    simulate_at_least_one_six,
    simulate_both_aces,
    simulate_king_given_face,
)

N = 100_000  # trials for simulation tests


# ---------------------------------------------------------------- Part A: counting
class TestFactorial:
    @pytest.mark.parametrize("n, expected", [(0, 1), (1, 1), (3, 6), (5, 120), (6, 720), (10, 3_628_800)])
    def test_known_values(self, n, expected):
        assert factorial(n) == expected

    def test_matches_math(self):
        for n in range(0, 25):
            assert factorial(n) == math.factorial(n)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)


class TestPermutations:
    @pytest.mark.parametrize(
        "n, k, expected",
        [
            (5, 2, 20),       # president + VP from 5
            (8, 3, 336),      # podium from 8 runners
            (10, 3, 720),     # Problem 4
            (9, 2, 72),       # Problem 9: captain + VC
            (6, 6, 720),      # all 6 books: 6!/0!
            (10, 4, 5040),    # Problem 7: PIN without repeats
            (5, 0, 1),        # choosing nothing: one way
        ],
    )
    def test_lesson_examples(self, n, k, expected):
        assert permutations(n, k) == expected

    def test_matches_math(self):
        for n in range(0, 15):
            for k in range(0, n + 1):
                assert permutations(n, k) == math.perm(n, k)

    @pytest.mark.parametrize("n, k", [(3, 4), (-1, 0), (5, -1)])
    def test_invalid_raises(self, n, k):
        with pytest.raises(ValueError):
            permutations(n, k)


class TestCombinations:
    @pytest.mark.parametrize(
        "n, k, expected",
        [
            (3, 2, 3),        # {A,B,C} choose 2
            (5, 2, 10),       # 2-person committee
            (6, 3, 20),       # Problem 5: pizza
            (7, 2, 21),       # Problem 6: concert
            (9, 4, 126),      # Problem 8: starting line-up
            (52, 2, 1326),    # pairs of cards
            (5, 0, 1),
            (5, 5, 1),
        ],
    )
    def test_lesson_examples(self, n, k, expected):
        assert combinations(n, k) == expected

    def test_matches_math(self):
        for n in range(0, 20):
            for k in range(0, n + 1):
                assert combinations(n, k) == math.comb(n, k)

    def test_symmetry(self):
        # choosing k to take = choosing n-k to leave behind
        for n in range(0, 15):
            for k in range(0, n + 1):
                assert combinations(n, k) == combinations(n, n - k)

    def test_story_proof_identity(self):
        # pick a k-committee then a chair  ==  pick the chair then k-1 others
        for n in range(1, 15):
            for k in range(1, n + 1):
                assert k * combinations(n, k) == n * combinations(n - 1, k - 1)

    def test_returns_int(self):
        assert isinstance(combinations(10, 4), int)

    @pytest.mark.parametrize("n, k", [(3, 4), (-1, 0), (5, -1)])
    def test_invalid_raises(self, n, k):
        with pytest.raises(ValueError):
            combinations(n, k)


# ------------------------------------------------------- Part B: exact probabilities
class TestExactProbabilities:
    @pytest.mark.parametrize(
        "n, k, expected",
        [
            (3, 2, 3 / 8),
            (3, 1, 3 / 8),
            (4, 2, 6 / 16),
            (5, 3, 10 / 32),
            (3, 0, 1 / 8),
            (10, 4, 210 / 1024),
        ],
    )
    def test_exactly_k_heads(self, n, k, expected):
        assert p_exactly_k_heads(n, k) == pytest.approx(expected)

    def test_exactly_k_heads_sums_to_one(self):
        for n in range(0, 12):
            assert sum(p_exactly_k_heads(n, k) for k in range(n + 1)) == pytest.approx(1.0)

    @pytest.mark.parametrize(
        "p, n, expected",
        [
            (1 / 2, 3, 7 / 8),             # at least one head in 3 flips
            (1 / 6, 2, 11 / 36),           # at least one 6 in 2 rolls
            (1 / 6, 4, 1 - 625 / 1296),    # de Mere: about 0.518
            (0.0, 10, 0.0),
            (1.0, 1, 1.0),
            (0.3, 0, 0.0),                 # zero tries: can't succeed
        ],
    )
    def test_at_least_one(self, p, n, expected):
        assert p_at_least_one(p, n) == pytest.approx(expected)

    def test_at_least_one_never_exceeds_one(self):
        # the "add 1/6 each roll" mistake would break this
        assert p_at_least_one(1 / 6, 7) <= 1.0

    @pytest.mark.parametrize("p, n", [(-0.1, 3), (1.1, 3), (0.5, -1)])
    def test_at_least_one_invalid_raises(self, p, n):
        with pytest.raises(ValueError):
            p_at_least_one(p, n)


# --------------------------------------------------------------- Part C: Monte Carlo
class TestSimulateAtLeastOneSix:
    def test_four_rolls(self):
        est = simulate_at_least_one_six(4, N, np.random.default_rng(0))
        assert est == pytest.approx(1 - (5 / 6) ** 4, abs=0.008)

    def test_two_rolls(self):
        est = simulate_at_least_one_six(2, N, np.random.default_rng(1))
        assert est == pytest.approx(11 / 36, abs=0.008)

    def test_agrees_with_exact_function(self):
        for n_rolls in (1, 3, 6):
            est = simulate_at_least_one_six(n_rolls, N, np.random.default_rng(n_rolls))
            assert est == pytest.approx(p_at_least_one(1 / 6, n_rolls), abs=0.008)

    def test_returns_probability(self):
        est = simulate_at_least_one_six(4, 1000, np.random.default_rng(2))
        assert isinstance(est, float)
        assert 0.0 <= est <= 1.0

    def test_reproducible_with_same_seed(self):
        a = simulate_at_least_one_six(4, 5000, np.random.default_rng(42))
        b = simulate_at_least_one_six(4, 5000, np.random.default_rng(42))
        assert a == b

    def test_invalid_trials_raises(self):
        with pytest.raises(ValueError):
            simulate_at_least_one_six(4, 0, np.random.default_rng(0))


class TestSimulateBothAces:
    def test_close_to_exact(self):
        est = simulate_both_aces(N, np.random.default_rng(3))
        assert est == pytest.approx(1 / 221, abs=0.0015)

    def test_without_replacement(self):
        # with replacement the answer would be (4/52)^2 = 0.00592 instead of 0.00452
        est = simulate_both_aces(400_000, np.random.default_rng(4))
        assert abs(est - 1 / 221) < abs(est - (4 / 52) ** 2)

    def test_returns_probability(self):
        est = simulate_both_aces(1000, np.random.default_rng(5))
        assert isinstance(est, float)
        assert 0.0 <= est <= 1.0

    def test_invalid_trials_raises(self):
        with pytest.raises(ValueError):
            simulate_both_aces(-5, np.random.default_rng(0))


class TestSimulateKingGivenFace:
    def test_close_to_one_third(self):
        est = simulate_king_given_face(N, np.random.default_rng(6))
        assert est == pytest.approx(1 / 3, abs=0.015)

    def test_not_the_unconditional_probability(self):
        # P(king) = 1/13 ~ 0.077; dividing by all trials instead of face-card trials gives this
        est = simulate_king_given_face(N, np.random.default_rng(7))
        assert est > 0.25

    def test_returns_probability(self):
        est = simulate_king_given_face(1000, np.random.default_rng(8))
        assert isinstance(est, float)
        assert 0.0 <= est <= 1.0

    def test_invalid_trials_raises(self):
        with pytest.raises(ValueError):
            simulate_king_given_face(0, np.random.default_rng(0))