def factorial(n):
    if n < 0:
        raise ValueError("The number must be greater than or equal to zero")
    fact = 1
    count = n
    while count > 1:
        fact = fact * count
        count = count -1

    return fact

def permutations(n, k):
    raise NotImplementedError


def combinations(n, k):
    raise NotImplementedError


def p_exactly_k_heads(n, k):
    raise NotImplementedError


def p_at_least_one(p, n):
    raise NotImplementedError


def simulate_at_least_one_six(n_rolls, n_trials, rng):
    raise NotImplementedError


def simulate_both_aces(n_trials, rng):
    raise NotImplementedError


def simulate_king_given_face(n_trials, rng):
    raise NotImplementedError