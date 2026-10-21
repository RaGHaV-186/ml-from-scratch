# EDA: Medical Cost dataset
Source: https://www.kaggle.com/datasets/mirichoi0218/insurance
Licence: ___ (copy from the Kaggle page)
Rows: 1338

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

**Centre.** charges: mean 13,270, median 9,382; the mean is 41.4% above
the median (strong right skew). age and bmi are roughly symmetric
(mean ≈ median). 20.5% of people smoke (274 of 1,338). Regions are balanced
(324–364 each).

**Spread & outliers.** Tukey fences for charges: −13,109 to 34,489.
All 139 Tukey outliers are above the upper fence (charges can't be negative).
|z| > 3 flags only 7, because the large values inflate the std (masking).
Sturges suggests 12 histogram bins, Freedman–Diaconis 30.

**Relationships.** (Section D)

**Probability.** (Section E)

## Hypotheses vs results
| H | Prediction | Result | ✅/❌ |
|---|---|---|---|
| H1 | mean > median by ~15% | +41.4% (13,270 vs 9,382) | direction ✅, size ❌ |
| H2 | strongest Pearson r: age | | |
| H3 | Spearman < Pearson (age–charges) | | |
| H3b | bmi–charges Pearson \|r\| < 0.1 | | |
| H3c | children–charges \|r\| < 0.1 | | |
| H4 | smokers ~4× as common in top 25% | | |
| H5 | Tukey > z-score | Tukey 139 vs z 7 | ✅ |
| H6 | men's smoker share ≥ 40 pp higher | | |

## Limitations
- 1 exact duplicate row (195 and 581, all 7 columns identical), found via the
  mode of charges; kept because ___.
- Section C uses functions from day02_spread.py (written with AI help).
- Observational data: correlations here do not show causes.