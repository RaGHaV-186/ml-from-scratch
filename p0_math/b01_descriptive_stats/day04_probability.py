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
    if n_trials <= 0:
        raise ValueError
    count = 0
    for _ in range(n_trials):
        rolls = rng.integers(1, 7, size=n_rolls)
        if 6 in rolls:
            count += 1

    return count/n_trials

def simulate_both_aces(n_trials, rng):
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    wins = 0
    for _ in range(n_trials):
        cards = rng.choice(52, size=2, replace=False)        # 2 DIFFERENT cards from 0..51
        if cards[0] % 13 == 0 and cards[1] % 13 == 0:      # rank 0 = ace
            wins += 1
    return wins / n_trials

def simulate_king_given_face(n_trials, rng):
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    face_count = 0
    king_count = 0
    for _ in range(n_trials):
        rank = rng.integers(0, 52) % 13      # 0 = A, 1..9 = 2..10, 10 = J, 11 = Q, 12 = K
        if rank >= 10:                       # face card → this trial is inside the "shrunk world"
            face_count += 1
            if rank == 12:                   # king, counted only inside that world
                king_count += 1
    return king_count / face_count           # divide by FACE cards, not by all trials