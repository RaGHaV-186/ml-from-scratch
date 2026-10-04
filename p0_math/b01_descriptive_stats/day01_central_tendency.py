import math
import statistics

import numpy as np


def mean(xs: list[float]) -> float:
    if len(xs) == 0:
        raise ValueError("mean() requires at least one value")
    return sum(xs) / len(xs)


def median(xs: list[float]) -> float:
    if len(xs) == 0:
        raise ValueError("median() requires at least one value")
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    else:
        return (s[mid - 1] + s[mid]) / 2


def mode(xs: list[float]) -> list[float]:
    if len(xs) == 0:
        raise ValueError("mode() requires at least one value")
    counts = {}
    for num in xs:
        if num not in counts:
            counts[num] = 1
        else:
            counts[num] += 1

    highest = max(counts.values())
    return [num for num, c in counts.items() if c == highest]


if __name__ == "__main__":
    # --- Commute data ---
    commute = [12, 15, 15, 18, 20, 22, 95]
    assert math.isclose(mean(commute), 197 / 7), f"mean gave {mean(commute)}"
    assert median(commute) == 18, f"median gave {median(commute)}"
    assert mode(commute) == [15], f"mode gave {mode(commute)}"

    # --- Even-length median ---
    assert median([1, 2, 3, 4]) == 2.5, f"median gave {median([1, 2, 3, 4])}"

    # --- Mode with a tie ---
    assert sorted(mode([1, 1, 2, 2, 3])) == [1, 2], f"mode gave {mode([1, 1, 2, 2, 3])}"

    # --- Self-check lists ---
    assert median([4, 8, 6, 2]) == 5          # sorted [2,4,6,8] -> (4+6)/2
    assert median([7, 7, 7, 10]) == 7         # (7+7)/2
    assert median([100, 1, 50]) == 50         # sorted [1,50,100] -> middle
    assert math.isclose(mean([7, 7, 7, 10]), 7.75)
    assert mode([7, 7, 7, 10]) == [7]
    assert sorted(mode([100, 1, 50])) == [1, 50, 100]   # all appear once -> all are modes

    # --- Single value ---
    assert mean([5]) == 5 and median([5]) == 5 and mode([5]) == [5]

    # --- Empty list must raise ValueError ---
    for fn in (mean, median, mode):
        try:
            fn([])
            assert False, f"{fn.__name__}([]) should have raised ValueError"
        except ValueError:
            pass

    print("all hand-picked tests passed")

    # --- Random comparison vs NumPy / statistics ---
    rng = np.random.default_rng(42)
    trials = 1000
    passed_mean = passed_median = passed_mode = 0

    for _ in range(trials):
        n = rng.integers(1, 51)                     # length 1..50 (51 is excluded)
        xs = rng.integers(0, 10, size=n).tolist()   # values 0..9, so repeats happen

        if np.isclose(mean(xs), np.mean(xs)):
            passed_mean += 1
        if np.isclose(median(xs), np.median(xs)):
            passed_median += 1
        if sorted(mode(xs)) == sorted(statistics.multimode(xs)):
            passed_mode += 1

    print(f"mean:   {passed_mean}/{trials}")
    print(f"median: {passed_median}/{trials}")
    print(f"mode:   {passed_mode}/{trials}")