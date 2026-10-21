"""Vendored chunkwise gated delta rule (PR #1870 + base-block fix) agrees with stock mlx-lm's per-token loop.

Needs the `mlx` dependency group (Apple Silicon); skipped elsewhere. Cases follow the PR's tests (mild and strong
decay, padding, grouped heads, gradients) plus correlated keys and the base-block inverse.
"""

import pytest

mx = pytest.importorskip("mlx.core")
pytest.importorskip("mlx_lm")

from orderslm.train import gated_delta_patch as gdp  # noqa: E402


def rel_l2(a, b) -> float:
    return (mx.linalg.norm((a - b).astype(mx.float32)) / mx.linalg.norm(b.astype(mx.float32))).item()


def normed(shape, d):
    x = mx.random.normal(shape)
    return x / mx.linalg.norm(x, axis=-1, keepdims=True) * d**-0.5


def inputs(B, T, Hk, Hv, Dk, Dv, decay, correlated=False):
    mx.random.seed(7)
    q = normed((B, T, Hk, Dk), Dk)
    if correlated:  # keys inside a chunk nearly identical (where powers of a 64×64 N blow up)
        base = mx.random.normal((B, 1, Hk, Dk))
        k = base + 0.01 * mx.random.normal((B, T, Hk, Dk))
        k = k / mx.linalg.norm(k, axis=-1, keepdims=True)
    else:
        k = normed((B, T, Hk, Dk), Dk)
    v = mx.random.normal((B, T, Hv, Dv))
    g = mx.exp(-mx.random.uniform(shape=(B, T, Hv)) * decay)
    beta = mx.random.uniform(shape=(B, T, Hv))
    state = mx.random.normal((B, Hv, Dv, Dk)) * 0.3
    mx.eval(q, k, v, g, beta, state)
    return q, k, v, g, beta, state


@pytest.mark.parametrize("n", [1, 2, 3, 8, 16, 64])
def test_unit_tri_inv_matches_dense_inverse(n):
    # entries like the real system's: beta (0..1) × key dot product (unit keys) × decay ratio (≤ 1)
    mx.random.seed(1)
    beta, ratio = mx.random.uniform(shape=(3, n, 1)), mx.random.uniform(shape=(3, n, n))
    keys = normed((3, n, 32), 1)
    m = mx.eye(n) + mx.tril(beta * (keys @ mx.swapaxes(keys, -1, -2)) * ratio, -1)
    want = mx.linalg.tri_inv(m, upper=False, stream=mx.cpu)
    assert rel_l2(gdp._unit_tri_inv(m), want) < 1e-5


@pytest.mark.parametrize("decay", [0.2, 4.0])
@pytest.mark.parametrize("T,chunk", [(128, 64), (96, 64), (64, 16), (200, 64)])
def test_chunkwise_matches_sequential(decay, T, chunk):
    args = inputs(1, T, 8, 16, 64, 64, decay)
    y_ref, s_ref = gdp.sequential()(*args, None)
    y, s = gdp.gated_delta_chunkwise(*args, None, chunk_size=chunk)
    assert rel_l2(y, y_ref) < 1e-5 and rel_l2(s, s_ref) < 1e-5


def test_correlated_keys_stay_finite_and_match():
    args = inputs(1, 128, 4, 8, 64, 64, 0.2, correlated=True)
    y_ref, s_ref = gdp.sequential()(*args, None)
    y, s = gdp.gated_delta_chunkwise(*args, None)
    assert mx.isfinite(y).all().item() and rel_l2(y, y_ref) < 1e-4 and rel_l2(s, s_ref) < 1e-4


def test_grouped_query_heads():
    args = inputs(2, 64, 4, 16, 64, 64, 0.5)
    y_ref, s_ref = gdp.sequential()(*args, None)
    y, s = gdp.gated_delta_chunkwise(*args, None, chunk_size=32)
    assert rel_l2(y, y_ref) < 1e-5 and rel_l2(s, s_ref) < 1e-5


def test_gradients_match_sequential():
    q, k, v, g, beta, state = inputs(1, 64, 2, 4, 32, 32, 0.5)
    w = mx.random.normal((1, 64, 4, 32))

    def make(fn, **kw):
        def loss(q, k, v, g, beta):
            y, s = fn(q, k, v, g, beta, state, None, **kw)
            return (y * w).sum() + (s * s).sum()

        return loss

    argnums = (0, 1, 2, 3, 4)
    ref = mx.grad(make(gdp.sequential()), argnums=argnums)(q, k, v, g, beta)
    got = mx.grad(make(gdp.gated_delta_chunkwise, chunk_size=16), argnums=argnums)(q, k, v, g, beta)
    for a, b in zip(ref, got, strict=True):
        assert rel_l2(b, a) < 1e-4


def test_install_routes_only_unmasked_scalar_gating():
    from mlx_lm.models import gated_delta

    gdp.install()
    gdp.install()  # idempotent: the reference stays the stock loop
    assert gated_delta.gated_delta_ops is not gdp.sequential()
    args = inputs(1, 33, 2, 4, 32, 32, 0.5)
    y, _ = gated_delta.gated_delta_ops(*args, None)
    y_ref, _ = gdp.sequential()(*args, None)
    assert rel_l2(y, y_ref) < 1e-5
    mask = mx.arange(33)[None] < 20
    y_m, _ = gated_delta.gated_delta_ops(*args, mask)  # masked: falls back to the loop
    y_m_ref, _ = gdp.sequential()(*args, mask)
    assert mx.array_equal(y_m, y_m_ref).item()
