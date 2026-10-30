"""A/B test: does moving the first gate in Cookie Cats from level 30 to level 40 change retention?"""
import json, math, pathlib
import numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]

def ztest(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    pval = math.erfc(abs(z) / math.sqrt(2))
    se_d = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p1 - p2
    return {"p30": round(100 * p1, 2), "p40": round(100 * p2, 2), "diff_pp": round(100 * d, 2),
            "ci95_pp": [round(100 * (d - 1.96 * se_d), 2), round(100 * (d + 1.96 * se_d), 2)],
            "z": round(z, 2), "p_value": round(pval, 4)}

def test_metric(df, col):
    a, b = df[df.version == "gate_30"], df[df.version == "gate_40"]
    return ztest(a[col].sum(), len(a), b[col].sum(), len(b))

def bootstrap(df, col, n=2000, seed=7):
    rng = np.random.default_rng(seed)
    a = df.loc[df.version == "gate_30", col].to_numpy(float)
    b = df.loc[df.version == "gate_40", col].to_numpy(float)
    diffs = np.array([rng.choice(a, a.size).mean() - rng.choice(b, b.size).mean() for _ in range(n)])
    return {"prob_gate30_better_pct": round(100 * (diffs > 0).mean(), 1)}

def run():
    df = pd.read_csv(ROOT / "data/cookie_cats.csv")
    out = {"players": len(df), "split": df.version.value_counts().to_dict(),
           "srm_pct_gate30": round(100 * (df.version == "gate_30").mean(), 2)}
    n30 = int((df.version == "gate_30").sum()); exp = len(df) / 2
    chi2 = 2 * (n30 - exp) ** 2 / exp
    out["srm_chi2"] = round(chi2, 2); out["srm_p_value"] = round(math.erfc(math.sqrt(chi2 / 2)), 4)
    out["retention_1"] = test_metric(df, "retention_1")
    out["retention_7"] = test_metric(df, "retention_7")
    out["bootstrap_7"] = bootstrap(df, "retention_7")
    out["bootstrap_1"] = bootstrap(df, "retention_1")
    # sensitivity: does the answer hold under different population cuts?
    cuts = {
        "all players": df,
        "drop extreme outlier (max rounds)": df[df.sum_gamerounds < df.sum_gamerounds.max()],
        "only players who played 1+ round": df[df.sum_gamerounds > 0],
        "only players who reached round 30+": df[df.sum_gamerounds >= 30],
    }
    out["sensitivity_7"] = {k: {"n": len(v), **test_metric(v, "retention_7")} for k, v in cuts.items()}
    # business sizing: 7-day retained players per 100k installs under each gate, across uplift assumptions
    d7 = out["retention_7"]["diff_pp"] / 100
    lo, hi = [x / 100 for x in out["retention_7"]["ci95_pp"]]
    out["impact_per_100k_installs"] = {"point": round(100000 * d7), "ci_low": round(100000 * lo), "ci_high": round(100000 * hi)}
    return out

if __name__ == "__main__":
    r = run()
    (ROOT / "docs/results.json").write_text(json.dumps(r, indent=2))
    print(json.dumps(r, indent=2))
