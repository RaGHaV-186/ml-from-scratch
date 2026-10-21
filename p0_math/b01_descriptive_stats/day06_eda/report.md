# EDA: Medical Cost dataset
Source: ___ (Kaggle page URL)
Licence: ___
Rows: ___

## Hypotheses (written before analysis, 21 Oct 2026)

H1. charges is right-skewed: mean > median by about 15%.
    Reason: most people pay little, a few pay a lot, and those few pull the mean up.

H2. Strongest Pearson r with charges: age.
    Reason: health problems increase with age, so charges rise with age;
    bmi is U-shaped, so its Pearson r stays small.

H3. age–charges: Spearman will be ___ (bigger / smaller) than Pearson.
    Reason: ___

H3b. bmi–charges is U-shaped (high and low BMI cost more),
     so Pearson r will be near 0 (|r| < 0.1).
     Reason: both underweight and overweight people have more health problems.

H3c. children → charges: no link (|r| < 0.1).
     Reason: a person's health problems do not depend on their number of children.

H4. Smokers are ___× as common in the top 25% of charges as overall.
    Reason: smoking causes expensive illnesses, so smokers pay more.

H5. Tukey flags more outliers in charges than |z| > 3.
    Reason: a few huge values inflate the mean and the std, so their own
    z-scores shrink and fewer pass |z| > 3 (masking).

H6. Men's smoker share is at least 40 percentage points higher than women's.
    Reason: I think men smoke more than women.

## Results
| H1 | mean > median by ~15% | mean 13,270 vs median 9,382: +41.4% | direction ✅, size ❌ |

## Hypotheses vs results
| H | Prediction | Result | ✅/❌ |
|---|---|---|---|

## Limitations
(after analysis)