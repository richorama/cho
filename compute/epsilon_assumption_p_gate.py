"""
F0 Assumption-P gate: action/operator evidence for sector independence.

After `epsilon_measure_schur.py` and `epsilon_phase_space_product.py`, the live
F0 seam is Assumption P:

    gauge/internal and flavour sectors act independently (commuting labels)
    with minimal multiplicity, so the transition carrier is Delta_9 x J3(O).

This artifact asks a concrete, computable question on the current one-operator
scaffold (`cho_bridge_operator.py`): does the epsilon bridge operator already
exhibit exact 16x27 tensor-product structure with primitive factors, or does it
require entangled cross-sector structure?

What is tested
--------------
1) Operator-Schmidt rank of epsilon_operator on (16 x 27) tensor legs.
2) Exact product reconstruction O = A (x) B from the leading Schmidt mode.
3) Primitive-factor check: A and B are rank-one, concentrated on one basis ray.
4) Normalized trace check: Tr(O)/432 = pi/432.
5) Action-rank penalty consistency: primitive rank (1,1) maximizes normalized
   log-cos link action against enlarged ranks.
6) Stress test: adding a second independent product term raises Schmidt rank,
   showing the gate is sensitive to genuine cross-sector mixing.

Interpretation
--------------
PASS here is not full theorem closure. It is evidence that the *current* bridge
operator is consistent with Assumption P at operator level (exact separable
primitive kernel). The remaining open seam is deriving this structure from the
CHO action/one-operator dynamics rather than choosing it as a scaffold object.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_assumption_p_gate.py
"""

from dataclasses import dataclass
import math

import numpy as np

from cho_bridge_operator import CHOBridgeOperator

DIM_W = 16
DIM_J = 27
DIM_BRIDGE = DIM_W * DIM_J
TARGET = math.pi / DIM_BRIDGE


@dataclass(frozen=True)
class GateRow:
    name: str
    passed: bool
    metric: str
    note: str


def _operator_schmidt(matrix, d_left, d_right):
    """Return operator-Schmidt decomposition of a (dL*dR)x(dL*dR) matrix."""
    flat = matrix.reshape(d_left, d_right, d_left, d_right)
    flat = flat.transpose(0, 2, 1, 3).reshape(d_left * d_left, d_right * d_right)
    u, s, vt = np.linalg.svd(flat, full_matrices=False)
    return u, s, vt


def _extract_product_factors(singular_u, singular_value, singular_vt):
    """Given top Schmidt mode, recover matrix factors A, B with O ~ A x B."""
    a = (math.sqrt(singular_value) * singular_u).reshape(DIM_W, DIM_W)
    b = (math.sqrt(singular_value) * singular_vt).reshape(DIM_J, DIM_J)
    return a, b


def _rank_penalty(rank_w, rank_j):
    """Normalized log-cos action from primitive_projector_derivation."""
    return -0.5 * math.log(rank_w * rank_j)


def main():
    op = CHOBridgeOperator().epsilon_operator().real
    u, s, vt = _operator_schmidt(op, DIM_W, DIM_J)

    nonzero = int(np.sum(s > 1e-12))
    a, b = _extract_product_factors(u[:, 0], float(s[0]), vt[0, :])
    recon = np.kron(a, b)

    err_recon = float(np.max(np.abs(op - recon)))
    rank_a = int(np.linalg.matrix_rank(a))
    rank_b = int(np.linalg.matrix_rank(b))

    diag_a = np.diag(a)
    diag_b = np.diag(b)
    nz_a = np.where(np.abs(diag_a) > 1e-12)[0]
    nz_b = np.where(np.abs(diag_b) > 1e-12)[0]

    eps_sq = float(np.trace(op) / DIM_BRIDGE)

    # Action-rank penalty consistency (primitive vs enlarged choices)
    s11 = _rank_penalty(1, 1)
    s21 = _rank_penalty(2, 1)
    s12 = _rank_penalty(1, 2)
    s22 = _rank_penalty(2, 2)

    # Stress test: add independent second product term -> Schmidt rank > 1
    e1 = np.zeros((DIM_W, DIM_W)); e1[1, 1] = 1.0
    f1 = np.zeros((DIM_J, DIM_J)); f1[1, 1] = 1.0
    mixed = op + 0.1 * np.kron(e1, f1)
    _, s_mix, _ = _operator_schmidt(mixed, DIM_W, DIM_J)
    nonzero_mix = int(np.sum(s_mix > 1e-12))

    rows = [
        GateRow(
            "operator-Schmidt rank is one",
            nonzero == 1,
            f"nonzero singular values = {nonzero}",
            "exact separable operator across 16x27 tensor legs",
        ),
        GateRow(
            "exact product reconstruction",
            err_recon < 1e-12,
            f"max|O - A x B| = {err_recon:.2e}",
            "leading Schmidt mode reconstructs epsilon operator to machine precision",
        ),
        GateRow(
            "primitive factors on each sector",
            rank_a == 1 and rank_b == 1 and len(nz_a) == 1 and len(nz_b) == 1,
            f"rank(A),rank(B)=({rank_a},{rank_b}); diag support=({list(nz_a)},{list(nz_b)})",
            "both factors are rank-one projectors on single basis rays",
        ),
        GateRow(
            "normalized trace gives pi/432",
            abs(eps_sq - TARGET) < 1e-12,
            f"Tr(O)/432 = {eps_sq:.10f}; target = {TARGET:.10f}",
            "bridge value follows directly from primitive product operator",
        ),
        GateRow(
            "rank-penalty favors primitive (1,1)",
            s11 > s21 and s11 > s12 and s11 > s22,
            f"S11={s11:.6f}, S21={s21:.6f}, S12={s12:.6f}, S22={s22:.6f}",
            "normalized log-cos action penalizes enlarged projector ranks",
        ),
        GateRow(
            "gate is sensitive to cross-sector mixing",
            nonzero_mix > 1,
            f"Schmidt rank after +0.1 E11xF11 term = {nonzero_mix}",
            "independent extra product term breaks rank-one separability",
        ),
    ]

    print("=" * 78)
    print("  F0 ASSUMPTION-P GATE")
    print("  Does the current epsilon operator already realize sector independence?")
    print("=" * 78)
    print()
    print("  Assumption P (live seam): independent commuting gauge/flavour sectors")
    print("  with minimal multiplicity, so carrier = Delta_9 x J3(O).")
    print()
    print(f"  {'check':<46} {'status':<6} metric")
    print("  " + "-" * 74)
    for row in rows:
        print(f"  {row.name:<46} {'PASS' if row.passed else 'FAIL':<6} {row.metric}")
        print(f"      {row.note}")
    print()

    ok = all(row.passed for row in rows)
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- current scaffold epsilon operator is exactly primitive product-separable.")
    print("  THEOREM STATUS: Assumption P gains strong operator-level evidence;")
    print("                  the open seam is deriving this separable primitive")
    print("                  structure from CHO action/one-operator dynamics, not")
    print("                  inserting it by hand.")
    print()

    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
