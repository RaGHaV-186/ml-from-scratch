# EDA: Medical Cost dataset (Day 6)

Source: Kaggle, "Medical Cost Personal Datasets" — https://www.kaggle.com/datasets/mirichoi0218/insurance
Licence: ___ (copy from the Kaggle page)
Rows: 1338 · Columns: 7 (age, sex, bmi, children, smoker, region, charges)
Code: eda.py (analysis), check_vs_library.py (verification), make_figures.py (figures)
Explainer: https://raghav-186.github.io/learn/day06-what-drives-medical-costs.html

## Hypotheses (written before analysis, 21 Oct 2026)

H1. charges is right-skewed: mean > median by about 15%.
    Reason: most people pay little, a few pay a lot, and those few pull the mean up.

H2. Strongest Pearson r with charges: age.
    Reason: health problems increase with age, so charges rise with age;
    bmi is U-shaped, so its Pearson r stays small.

H3. age–charges: Spearman will be smaller than Pearson.
    Reason: charges grow linearly with age.
    (Added 22 Oct 00:30, before Section D was run.)

H3b. bmi–charges is U-shaped (high and low BMI cost more),
     so Pearson r will be near 0 (|r| < 0.1).
     Reason: both underweight and overweight people have more health problems.

H3c. children → charges: no link (|r| < 0.1).
     Reason: a person's health problems do not depend on their number of children.

H4. Smokers are about 4× as common in the top 25% of charges as overall
    (almost all smokers are in the top 25%).
    Reason: smoking causes expensive illnesses, so smokers pay more.
    (Added 22 Oct 00:30, before Section E was run.)

H5. Tukey flags more outliers in charges than |z| > 3.
    Reason: a few huge values inflate the mean and the std, so their own
    z-scores shrink and fewer pass |z| > 3 (masking).

H6. Men's smoker share is at least 40 percentage points higher than women's.
    Reason: I think men smoke more than women.

## Results

**Data types.** 3 categorical (sex, smoker, region), 2 discrete (age, children),
2 continuous (bmi, charges). Rule: text → categorical; all whole numbers →
discrete; otherwise continuous.

**Centre.** charges: mean 13,270, median 9,382, so the mean is 41.4% above
the median (strong right skew). A typical person pays about $9,400; the mean
is what the insurer pays per person on average. age (mean 39.21, median 39)
and bmi (30.66 vs 30.40) are roughly symmetric. children: mean 1.09,
median 1, mode 0 (most policies have no children on them).
20.5% of people smoke (274 of 1,338). Regions are balanced (324–364 each).

**Duplicate.** The mode of charges is 1,639.5631, which appears twice. Rows
195 and 581 are identical in all 7 columns, so this is one record entered
twice. For continuous data, the mode is useless as a centre but useful as a
duplicate detector.

**Spread & outliers.** Q1 = 4,740, Q3 = 16,640. Tukey fences: −13,109 to
34,489. All 139 Tukey outliers are above the upper fence (charges can't be
negative). |z| > 3 flags only 7, because the large values inflate the mean
and the std (masking). 139 is about 10% of all rows, which suggests the tail
is a separate group, not errors. Sturges suggests 12 histogram bins,
Freedman–Diaconis 30.

**Relationships.**
| Variable vs charges | Pearson | Spearman |
|---|---|---|
| age | 0.299 | 0.534 |
| bmi | 0.198 | 0.119 |
| children | 0.068 | 0.133 |

Age has the strongest link. For age, Spearman is almost double Pearson:
charges tend to rise with age, but not along a straight line. Age explains
only r² ≈ 9% of the variation in charges in a straight-line sense. All of
these are weak to moderate correlations in observational data, so none of
them shows a cause.

**Probability.**
- P(smoker | male) = 23.5% (159 of 676), P(smoker | female) = 17.4%
  (115 of 662): a gap of 6.1 percentage points.
- The top 25% of charges (above Q3 = 16,640) holds 335 people, of whom
  255 smoke: P(smoker | top 25%) = 76.1%, which is 3.7× the overall 20.5%.
  255 of the 274 smokers (93%) are in the top 25%.
- Computed two ways, direct counting and bayes_posterior with prior
  P(smoker) = 274/1338, P(top | smoker) = 255/274 and
  P(top | non-smoker) = 80/1064. Both give 0.7612.
- ECDF: P(charges ≤ 10,000) = 0.532, just above 0.5 because 10,000 is
  slightly above the median.

## Hypotheses vs results
| H | Prediction | Result | ✅/❌ |
|---|---|---|---|
| H1 | mean > median by ~15% | +41.4% (13,270 vs 9,382) | direction ✅, size ❌ |
| H2 | strongest Pearson r: age | age 0.299 > bmi 0.198 > children 0.068 | ✅ |
| H3 | Spearman < Pearson (age–charges) | Spearman 0.534 vs Pearson 0.299 | ❌ |
| H3b | bmi–charges Pearson \|r\| < 0.1 (U-shape) | 0.198; no U visible in the scatter | ❌ |
| H3c | children–charges \|r\| < 0.1 | Pearson 0.068, Spearman 0.133 | ✅ Pearson / ❌ Spearman |
| H4 | smokers ~4× as common in top 25% | 76.1% vs 20.5% = 3.7×; 93% of smokers in top 25% | ✅ |
| H5 | Tukey > z-score | Tukey 139 vs z 7 | ✅ |
| H6 | men's smoker share ≥ 40 pp higher | 23.5% vs 17.4% = 6.1 pp | ❌ |

Score: 3 held, 2 partly, 3 failed.

## What the misses taught me
- **H1:** the expensive tail is much heavier than I expected (41% vs 15%).
- **H3:** Spearman ≫ Pearson means the relationship is monotonic but not
  linear. A separate high-cost band (mostly smokers) breaks the straight line.
- **H3b:** a correlation coefficient can't show a shape; only the scatter
  plot can. Neither Pearson nor Spearman detects a U.
- **H6:** my guess had no data behind it. Even the 6.1 pp gap needs a
  chi-square test (Day 10) before I can say it's more than chance.

## Exploratory findings (not pre-registered)
Found while making the figures, so these are leads to test later, not results:
- 136 of the 139 Tukey outliers are smokers.
- Within non-smokers only, age–charges: Pearson 0.628, Spearman 0.821.
  Mixing in the smokers' higher band drags the overall Pearson down to 0.299.
- Within smokers only, bmi–charges Pearson is 0.806, and charges appear to
  jump around BMI 30 (median 20,167 below 30 vs 40,904 at 30 or above).
  BMI matters a lot for smokers, but in a step, not a U.
(These subgroup numbers were computed with AI help, not in eda.py.)

## Verification
check_vs_library.py compares every hand-coded number (mean, median,
percentiles, fences, outlier counts, bins, Pearson, Spearman, contingency
counts, conditional probabilities, Bayes, ECDF) with NumPy, SciPy and pandas.
All checks passed.

## Figures (figures/)
- 01_charges_histogram.png: charges with FD bins, mean and median marked
- 02_charges_by_smoker_boxplot.png: charges, smokers vs non-smokers
- 03_age_vs_charges.png: age vs charges, coloured by smoker
- 04_bmi_vs_charges.png: bmi vs charges, coloured by smoker (H3b)

## Mistakes during the analysis
- Q3 first computed with the wrong percentile scale (0.75 instead of 75),
  giving 1,242. Both Bayes methods still agreed on the wrong answer. Caught
  because Q3 didn't match the value implied by the Tukey fences (≈ 16,640).
  Lesson: two methods agreeing proves the formula, not the input.
- Bayes likelihoods first divided by all 1,338 people instead of the 274
  smokers / 1,064 non-smokers. In P(A | B), the denominator is everyone with B.
- Called a long right tail "left-skewed". Skew is named after the tail.
- Twice put new code inside a for loop, so results printed 7 times.

## Limitations
- Observational data: smoking is strongly associated with high charges here,
  but this dataset alone can't show that it causes them.
- No uncertainty yet: no confidence intervals (Day 9) or significance tests
  (Day 10) on any of these numbers.
- 1 exact duplicate row (195 and 581, all 7 columns identical), found via the
  mode of charges; kept because it changes the mean by about 0.07% and age–charges
  Pearson by 0.0007, and I don't change raw data silently.
- How this dataset was collected isn't verified, so the results describe this
  dataset only, not any real population.
- H3 and H4 were filled in on 22 Oct, after Sections A–C had run but before
  Sections D and E.

## AI help (honest disclosure)
- Mine: load_columns, frequency_table, the if/elif/else structure of
  column_type, all calls and calculations in eda.py, all hypotheses and
  interpretations.
- Written with AI help: the two conditions in column_type, ecdf, the Day 2
  functions imported here (day02_spread.py), make_figures.py,
  check_vs_library.py, and the subgroup numbers in "Exploratory findings".