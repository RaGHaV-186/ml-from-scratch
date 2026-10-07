def factorial(n):
    if n < 0:
        raise ValueError("The number must be greater than or equal to zero")
    fact = 1
    count = n
    while count > 1:
        fact = fact * count
        count = count - 1

    return fact

def permutations(n, k):
    if n < 0 or k < 0 or k > n:
        raise ValueError
    count = n
    res = 1
    while count > n-k:
        res = res * count
        count = count - 1

    return res



def combinations(n, k):
    return permutations(n,k)//factorial(k)


def p_exactly_k_heads(n, k):
    return combinations(n,k)/2**n


def p_at_least_one(p, n):
    if p < 0 or p > 1 or n < 0:
        raise ValueError

    return 1 - (1-p)**n

def simulate_at_least_one_six(n_rolls, n_trials, rng):
    raise NotImplementedError


def simulate_both_aces(n_trials, rng):
    raise NotImplementedError


def simulate_king_given_face(n_trials, rng):
    raise NotImplementedError