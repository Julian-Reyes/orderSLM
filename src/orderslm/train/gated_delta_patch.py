"""Chunkwise-parallel gated delta rule for training Qwen3.5 with mlx-lm (vendored patch, M6).

Stock mlx-lm 0.32.2 trains Qwen3.5's Gated DeltaNet layers through `gated_delta_ops`, a per-token loop that keeps
one state per token for the backward pass (the Metal kernel has no VJP): ~9.6 MB per token on Qwen3.5-0.8B, so
our rows (p50 3.2k, max 9.8k tokens) don't fit in 16 GB (runs/mlx-smoke/NOTES.md). This module swaps in the
chunkwise-parallel form (arXiv:2406.06484 §4, arXiv:2412.06464): per chunk of 64 tokens one unit lower-triangular
solve plus matmuls, keeping O(T / 64) states.

Source: `gated_delta_chunkwise` and `_unit_tri_inv` are from ml-explore/mlx-lm pull request #1870 by Aditya Karnam
("Chunkwise-parallel gated delta rule for training", open, not merged), head commit
3b04b9f1992fb83c4210228f7eb1c9dc72827e49 (adityak74/mlx-lm, file mlx_lm/models/gated_delta.py, git blob 7e35db6c).
mlx-lm is MIT-licensed:

    MIT License. Copyright © 2023 Apple Inc. Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute,
    sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions: The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT
    WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
    ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
    OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Our change: `_unit_tri_inv` stops its 2×2 block recursion at `BASE_BLOCK` (8) instead of 1×1 and inverts the base
blocks with the nilpotent product (I − N)(I + N²)(I + N⁴). Recursing to 1×1 makes ~1,000 small arrays per chunk and
exceeds Metal's resource limit (499,000 on the M1) at ~8k tokens (reported in the PR's comments); the product is
used only inside 8×8 blocks because powers of a full 64×64 N overflow when keys in a chunk are highly correlated.
Everything else is the PR's code unchanged; the dispatch is the PR's new `gated_delta_ops`.

    from orderslm.train import gated_delta_patch
    gated_delta_patch.install()   # before training; idempotent

Checked against stock `gated_delta_ops` in tests/test_gated_delta_patch.py (random inputs, strong decay,
correlated keys, gradients) and on real rows (`make mlx-smoke ARGS="... --check"`).
"""

from typing import Optional

import mlx.core as mx

PR_COMMIT = "3b04b9f1992fb83c4210228f7eb1c9dc72827e49"
BASE_BLOCK = 8
CHUNK_SIZE = 64


def _unit_tri_inv(m: mx.array) -> mx.array:
    """Inverse of a unit lower-triangular matrix, built from matmuls.

    ``mx.linalg.tri_inv`` is CPU-only and has no VJP, so it cannot appear in a
    training graph. The 2x2 block identity

        [A 0; C B]^-1 = [A^-1 0; -B^-1 C A^-1, B^-1]

    gives the inverse in log2(n) levels of batched matmuls, which autodiff
    handles natively and which parallelizes over the batch.
    """
    n = m.shape[-1]
    if n <= BASE_BLOCK:
        # OrderSLM change: m = I + N with N strictly lower (N^n = 0), so m^-1 = (I - N)(I + N^2)(I + N^4)...
        eye = mx.eye(n, dtype=m.dtype)
        power = eye - m
        inverse = eye + power
        span = 2
        while span < n:
            power = power @ power
            inverse = inverse @ (eye + power)
            span *= 2
        return inverse
    h = n // 2
    a, c, b = m[..., :h, :h], m[..., h:, :h], m[..., h:, h:]
    a_inv, b_inv = _unit_tri_inv(a), _unit_tri_inv(b)
    lower = -(b_inv @ c @ a_inv)
    zeros = mx.zeros_like(mx.swapaxes(lower, -1, -2))
    return mx.concatenate(
        [
            mx.concatenate([a_inv, zeros], axis=-1),
            mx.concatenate([lower, b_inv], axis=-1),
        ],
        axis=-2,
    )


def gated_delta_chunkwise(
    q: mx.array,
    k: mx.array,
    v: mx.array,
    g: mx.array,
    beta: mx.array,
    state: Optional[mx.array] = None,  # noqa: UP045 (kept as in the PR)
    mask: Optional[mx.array] = None,  # noqa: UP045
    chunk_size: int = CHUNK_SIZE,
) -> tuple[mx.array, mx.array]:
    """Chunkwise-parallel gated delta rule, for training.

    Equivalent to :func:`gated_delta_ops` but splits the sequence into chunks of
    ``chunk_size`` and evaluates each chunk with matmuls, so autograd retains
    O(T / chunk_size) states instead of one per timestep.

    Writing the recurrence as ``S_t = g_t S_{t-1} + u_t k_t^T`` with
    ``u_t = b_t (v_t - g_t S_{t-1} k_t)`` telescopes within a chunk::

        S_j = G_j S_0 + sum_{i<=j} (G_j / G_i) u_i k_i^T,  G_j = prod_{m<=j} g_m

    and the ``u_i`` satisfy a unit lower-triangular system solved once per
    chunk. Quantities are carried as ratios ``G_j / G_i`` (bounded by 1 for
    i <= j) rather than as ``G_j``, which underflows on strongly decaying heads
    and sends the intermediate writes to infinity.

    Scalar gating only; vectorized gating and masks fall back to the caller.

    Shapes match :func:`gated_delta_ops`.
    """
    B, T, Hk, Dk = q.shape
    Hv, Dv = v.shape[-2:]
    out_dtype = q.dtype
    if state is None:
        state = mx.zeros((B, Hv, Dv, Dk), dtype=mx.float32)

    if (repeat_factor := Hv // Hk) > 1:
        q = mx.repeat(q, repeat_factor, -2)
        k = mx.repeat(k, repeat_factor, -2)

    # [B, T, H, D] -> [B, H, T, D]; accumulate in fp32 as the kernels do
    q, k, v = (mx.swapaxes(x, 1, 2).astype(mx.float32) for x in (q, k, v))
    g = mx.swapaxes(g, 1, 2).astype(mx.float32)
    beta = mx.swapaxes(beta, 1, 2).astype(mx.float32)

    pad = (-T) % chunk_size
    if pad:
        # padding must neither decay the state (g = 1) nor write to it (beta = 0)
        widths = [(0, 0), (0, 0), (0, pad), (0, 0)]
        q, k, v = (mx.pad(x, widths) for x in (q, k, v))
        g = mx.pad(g, widths[:3], constant_values=1.0)
        beta = mx.pad(beta, widths[:3])

    T_pad = q.shape[2]
    n_chunks = T_pad // chunk_size
    shape = (B, Hv, n_chunks, chunk_size)
    q, k, v = (x.reshape(*shape, -1) for x in (q, k, v))
    g, beta = g.reshape(shape), beta.reshape(shape)

    cumulative = mx.cumsum(mx.log(mx.maximum(g, 1e-30)), axis=-1)
    causal = mx.tril(mx.ones((chunk_size, chunk_size), dtype=mx.bool_))
    strict = mx.tril(mx.ones((chunk_size, chunk_size), dtype=mx.bool_), -1)
    eye = mx.eye(chunk_size, dtype=mx.float32)

    # ratios[j, i] = G_j / G_i for i <= j, zero above the diagonal
    deltas = cumulative[..., :, None] - cumulative[..., None, :]
    ratios = mx.where(causal, mx.exp(mx.where(causal, deltas, -1e30)), 0.0)
    gammas = mx.exp(cumulative)

    ys = []
    s = state.astype(mx.float32)
    for c in range(n_chunks):
        q_c, k_c, v_c = q[:, :, c], k[:, :, c], v[:, :, c]
        beta_c, gamma_c, ratio_c = beta[:, :, c], gammas[:, :, c], ratios[:, :, c]
        k_t = mx.swapaxes(k_c, -1, -2)

        system = eye + mx.where(strict, beta_c[..., :, None] * (k_c @ k_t) * ratio_c, 0.0)
        u = _unit_tri_inv(system) @ (
            beta_c[..., None] * (v_c - gamma_c[..., None] * (k_c @ mx.swapaxes(s, -1, -2)))
        )

        attn = mx.where(causal, (q_c @ k_t) * ratio_c, 0.0)
        ys.append(gamma_c[..., None] * (q_c @ mx.swapaxes(s, -1, -2)) + attn @ u)

        tail = ratio_c[..., -1, :]  # G_C / G_i
        s = gamma_c[..., -1, None, None] * s + mx.swapaxes(tail[..., None] * u, -1, -2) @ k_c

    y = mx.stack(ys, axis=2).reshape(B, Hv, T_pad, Dv)
    if pad:
        y = y[:, :, :T]
    return mx.swapaxes(y, 1, 2).astype(out_dtype), s


_installed: dict = {}


def sequential():
    """Stock mlx-lm `gated_delta_ops` (the per-token reference loop), whether or not the patch is installed."""
    from mlx_lm.models import gated_delta

    return _installed.get("sequential", gated_delta.gated_delta_ops)


def install() -> None:
    """Route mlx-lm's ops path (used whenever the Metal kernel isn't: every training step) through the chunkwise
    form for scalar gating without a mask, as PR #1870's `gated_delta_ops` does; anything else keeps the loop."""
    from mlx_lm.models import gated_delta

    if _installed:
        return
    reference = gated_delta.gated_delta_ops

    def gated_delta_ops(q, k, v, g, beta, state=None, mask=None):
        if mask is None and g.ndim == 3:
            return gated_delta_chunkwise(q, k, v, g, beta, state)
        return reference(q, k, v, g, beta, state, mask)

    _installed["sequential"] = reference
    gated_delta.gated_delta_ops = gated_delta_ops
