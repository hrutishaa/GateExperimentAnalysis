from scripts.analyze import run, ztest

def test_ztest_symmetric():
    assert ztest(50, 100, 50, 100)["diff_pp"] == 0

def test_results():
    r = run()
    assert r["players"] == 90189
    assert r["retention_7"]["p_value"] < 0.01
    lo, hi = r["retention_7"]["ci95_pp"]
    assert lo > 0 and hi > lo
