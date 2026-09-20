import numpy as np

from src.stats.statistical_tests import benjamini_hochberg, block_bootstrap_mean_ci, diebold_mariano


def test_bh_fdr() -> None:
    reject, q = benjamini_hochberg(np.array([0.001, 0.01, 0.8, 0.9]))
    assert reject[0]
    assert reject[1]
    assert q.shape == (4,)


def test_block_bootstrap_reproducible() -> None:
    x = np.arange(20.0)
    a = block_bootstrap_mean_ci(x, block_length=4, n_boot=100, seed=17)
    b = block_bootstrap_mean_ci(x, block_length=4, n_boot=100, seed=17)
    assert a == b
    assert a[1] <= a[0] <= a[2]


def test_dm_zero_difference() -> None:
    loss = np.array([1.0, 2.0, 3.0, 4.0])
    stat, p = diebold_mariano(loss, loss, max_lag=1)
    assert stat == 0.0
    assert p == 1.0
