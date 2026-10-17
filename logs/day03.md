# Day 3: Moving together

**Learned:** Covariance asks "when one is above its average, is the other one too?" Each point adds (x − x̄)(y − ȳ): positive if it agrees (both above or both below), negative if not, then divide by n − 1. Its sign gives the direction, but its size depends on the units. Pearson r divides by both stds, which removes the units and keeps it between −1 and +1. Spearman is Pearson on the ranks, so it measures any always-rising or always-falling relationship and ignores outliers.

**Why r is between −1 and +1:** r is the cosine of the angle between the centred data arrows (x − x̄ and y − ȳ). Dividing by the stds removes their lengths and leaves only the angle, and a cosine is always between −1 and +1. Arrows perfectly aligned means the points lie on a straight line.

**Surprised me:** r = 0 doesn't mean unrelated: y = x² has r = 0. And with only 5 points, about 1 in 5 completely random datasets shows |r| > 0.7 by chance.

**Mistakes:** Divided the covariance by n instead of n − 1 again (3 points, so ÷ 2). Wrote (−1) × (−3) = 4. Said r(x, 100y) = 80, but r can never be above 1, because the 100 cancels between cov and s_y. Mixed up covariance (any size) and r (−1 to +1). Called the firefighters example reverse causation; the main explanation is a confounder (city size, fire size).

**Built:** Interactive explainer: raghav-186.github.io/learn/day03-moving-together.html (students and zones, signed rectangles, the cosine angle, the y = x² trap, a chance simulator, and Spearman ranks). covariance, pearson and spearman are my own code; rank was written with AI help and is on my from-memory list for the Day 7 test.
