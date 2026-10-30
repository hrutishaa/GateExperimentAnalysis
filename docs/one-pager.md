# Moving the first gate to level 40: executive one-pager

**Decision needed:** Should we move the first gate in Cookie Cats from level 30 to level 40?

**Recommendation:** No. Keep the gate at level 30.

## What we tested
We randomly assigned 90,189 new players to gate 30 or gate 40 and tracked whether they came back 1 day and 7 days after installing.

## What we found
- **7-day retention is lower with gate 40.** It was 18.20% vs. 19.02% with gate 30, a drop of 0.82 points (95% CI 0.31–1.33, p = 0.0016). A bootstrap puts the chance that gate 30 is better at 99.8%.
- **1-day retention also leans toward gate 30** (+0.59 points), but that difference isn't statistically significant (p = 0.074).
- **The result is robust.** It holds after removing outliers and after excluding players who never played.

## What it means
Each 100,000 installs on gate 40 would mean about **820 fewer players still active at day 7** (likely range 310–1,330). Since 7-day players are the base for long-term revenue, this is a loss we shouldn't accept.

## Risks and next steps
1. **Check assignment.** The groups are slightly uneven (49.56% / 50.44%, sample-ratio test p = 0.0086). Engineering should confirm the randomization before this result is final.
2. **Don't optimize retention alone.** Later gates may change in-app purchases, and that data wasn't in this test. If revenue is the goal, rerun the test with purchase tracking.
3. **Next test:** try an earlier gate (level 20–25) to see if the effect continues.
