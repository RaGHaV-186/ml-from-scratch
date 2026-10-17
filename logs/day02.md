# Day 2: Measuring spread

**Learned:** The mean says *where* the data is; the standard deviation says *how wide* it is: the typical distance of a value from the mean. Two buses can both be 4 minutes late on average, but one lands within a minute of that every day (std 0.82) and the other doesn't (std 2.58). A z-score is how many of those std steps a value is from the mean, which lets you compare things on different scales. Percentiles walk along the sorted data with h = (n − 1)·q, and the IQR is the width of the middle half.

**Why n − 1:** The sample mean sits in the middle of the sample, so distances from it come out too small. Once the mean is known, only n − 1 distances are free, so on average the sum of squares is (n − 1) × the true variance. Dividing by n − 1 fixes it.

**Surprised me:** With 6 values, the "|z| > 3" outlier rule can never fire. The outlier drags the mean and stretches the std it is measured with, so its z gets stuck at (n − 1)/√n = 5/√6 ≈ 2.04, however extreme it is. Tukey's fences use quartiles, which the outlier can't stretch, so they still catch it.

**Mistakes:** Copied numbers wrong twice: used Q1 = 10 instead of 20 for the Tukey fence, and answered about 55/70 instead of 75/−5. Also wrote 6.6 instead of rounding 20/3 to 6.67. Found that my zscore_outliers used the population std (ddof=0) while its docstring assumed the sample std. Fixed it to ddof=1.

**Built:** Interactive explainer: raghav-186.github.io/learn/day02-measuring-spread.html (buses, the crowd width, an n − 1 dice simulator, the std ruler for z-scores, percentiles, Tukey vs z, and Welford). Day 2 code was written with AI help; percentile and welford are still on my from-memory list for the Day 7 test.
