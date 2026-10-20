# Day 4: Counting chances

**Learned:** When outcomes are equally likely, probability = favourable ÷ total, so it starts with counting. The swap test decides the tool: swap two things I placed; if the result changes it's a permutation, if not it's a combination (identical heads, ✓'s, chocolates, letters → C(n, k)). Exactly k heads = C(n, k) / 2ⁿ because I'm choosing which positions are H. "At least one" = 1 − P(none). "Or" = add, minus the overlap. "Given" shrinks the room: the given part is the bottom of the fraction. The chain rule multiplies step by step in the shrunk room.

**Independent vs exclusive:** Independent = knowing one doesn't change the other's chance (same chance in the small room as in the big room). Mutually exclusive = they can't both happen, which actually makes them dependent. Linked doesn't mean caused: height and basketball are dependent.

**Surprised me:** A jailbreak that works 5% of the time succeeds at least once in 20 tries 64% of the time. Adding gives 100%, which is impossible. And P(cricket given football) = 5/12 but P(football given cricket) = 5/8, from the same 5 students.

**Mistakes:** Added probabilities over repeated tries (5% × 20). Said "neither" = 0 because 12 + 8 = 20 looked like the whole class. Put 0.55 (car or bike) in the bottom instead of 0.40 (car) for a "given car" question. Removed the overlap twice (got 60 instead of 45). Called height/basketball and draws without replacement independent.

**Built:** Interactive explainer: raghav-186.github.io/learn/day04-counting-chances.html. My code: factorial, permutations, combinations, p_exactly_k_heads, p_at_least_one, simulate_at_least_one_six. simulate_both_aces and simulate_king_given_face were written with AI help. p_or and p_given are still on my from-memory list for the Day 7 test.
