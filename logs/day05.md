# Day 5: Chance in numbers

**Learned:** Bayes flips a conditional: from P(flag given sycophantic) to P(sycophantic given flag). On a tree it's matching path ÷ all matching paths: multiply along, add across. A random variable X is a rule that turns each outcome into a number, and the question decides X. PMF = (outcomes with that x) ÷ (all outcomes); CDF = the running total, ending at 1. E[X] = Σ x·P(x), a weighted average. Var(X) = Σ (x − E)²·P(x). A Bernoulli (one yes/no try) has E = p and Var = p(1 − p), the same p(1 − p) that sits inside the SE of any eval rate.

**Surprised me:** A detector that catches 90% of sycophantic answers is right only 27% of the time when it flags, if just 2% of answers are sycophantic: 18 real catches vs 49 false alarms. With a 20% base rate it jumps to 82%. Evals must report the base rate.

**Mistakes:** Multiplied the two flagged paths instead of adding them. Said X = 4 / X = 3 instead of "X can be 1, 2 or 5". Used the die faces as X instead of the winnings. Thought two dice have 12 outcomes (it's 6² = 36). Subtracted E from the probability instead of the value, and paired each value with the wrong P. CDF boundaries: "2 or more" is 1 − F(1), not 1 − F(2). In code: assigned the result of list.append (it returns None), and wrote + prob instead of * prob.

**Test (Days 1–5): 8/10.** To fix: Tukey fences are 1.5 × IQR beyond Q1 and Q3 (not quartiles × 1.5); ice cream and sunburn is a confounder (weather); for "given" questions, write "room = ___" first (P(coffee given tea) = 8/18, not 8/26).

**Built:** Interactive explainer: raghav-186.github.io/learn/day05-chance-in-numbers.html. My code: bayes_posterior, cdf, expectation, variance (all mine). Still to add: input checks and the zip length check.
