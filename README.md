# Gate Experiment Analysis

Cookie Cats is a mobile puzzle game. Players hit a "gate" where they either wait or pay to keep going. The team tested moving the first gate from **level 30 to level 40** and wanted to know whether it changed retention. This repo is my analysis of that A/B test and the recommendation I'd bring to the product lead.

**Exec summary:** [docs/one-pager.md](docs/one-pager.md)

**Data:** Cookie Cats A/B test, 90,189 players, published by DataCamp/Kaggle ("Mobile Games A/B Testing with Cookie Cats"). Copy used here: https://github.com/ryanschaub/Mobile-Games-A-B-Testing-with-Cookie-Cats

## Approach

1. **Sanity checks**: group sizes and a sample-ratio-mismatch (SRM) test.
2. **Main test**: two-proportion z-test with 95% confidence intervals for 1-day and 7-day retention.
3. **Bootstrap** (2,000 resamples) as a second opinion on the 7-day result.
4. **Sensitivity**: rerun the 7-day test on different player cuts to see if the answer holds.
5. **Business sizing**: what the difference means per 100,000 installs.

## Results

| Metric | Gate 30 | Gate 40 | Difference | 95% CI | p-value |
|---|---|---|---|---|---|
| 1-day retention | 44.82% | 44.23% | +0.59 pp for gate 30 | −0.06 to +1.24 pp | 0.074 |
| 7-day retention | 19.02% | 18.20% | +0.82 pp for gate 30 | +0.31 to +1.33 pp | 0.0016 |

- The bootstrap puts a **99.8%** probability on gate 30 having higher 7-day retention.
- The result holds after dropping the one extreme outlier and after dropping players who never played a round. Among players who reached round 30+ the direction is the same (+0.87 pp) but no longer significant (p = 0.108), which is expected with a third of the sample.
- **Watch-out:** the split is 49.56% / 50.44%, and the SRM test flags it (χ² = 6.90, p = 0.0086). I'd check the assignment logic before trusting the result fully.
- Per 100,000 installs, gate 30 keeps about **820** more players at day 7 (range 310–1,330).

**Recommendation:** keep the gate at level 30, and don't roll out level 40.

## Run it

```bash
pip install -r requirements.txt
python scripts/analyze.py   # writes docs/results.json
python -m pytest -q
```
