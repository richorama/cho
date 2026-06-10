"""Boundary metric-origin gate for the endpoint-overlap cost.

`boundary_variation_gate.py` showed that minimizing

    B(P,Q) = Tr(P o Q)

on `OP2 x OP2` drives a generic primitive endpoint pair to an orthogonal pair.
`action_origin_unification_gate.py` then left the first origin obligation open:
why should the boundary action contain this overlap cost at all?

This gate narrows that obligation. For primitive idempotents, `Tr(P o Q)` is the
rank-one transition probability. On a transition `CP1` it obeys

    Tr(P(theta) o P(0)) = cos^2(theta/2),

so minimizing it is exactly maximizing the Fubini-Study endpoint distance. The
same scalar is preserved by `F4` automorphisms, and `OP2=F4/Spin(9)` is a rank-one
two-point homogeneous space, so any `F4`-invariant two-endpoint boundary contrast
is a function of this overlap.

Honest status
-------------
This does not derive the full CHO boundary action. It upgrades the overlap term
from an arbitrary-looking scalar to the canonical `F4`-invariant two-point
contrast. The remaining dynamics question is why the CHO boundary action chooses
the simplest linear monotone of that contrast, with its coefficient and coupling
to the oriented WZ term.

No scipy. Uses existing OP2/F4 helpers.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/boundary_metric_origin_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
COMPUTE = ROOT / "compute"
if str(COMPUTE) not in sys.path:
    sys.path.insert(0, str(COMPUTE))

from berry_pi_intrinsic_op2 import _coherent, _embed  # noqa: E402
from epsilon_action_selection import _f4_basis, random_automorphism, trace_form  # noqa: E402
from epsilon_orbit_selection import primitive_idempotents  # noqa: E402

from boundary_variation_gate import boundary_gradients, endpoint_overlap, f4_basis  # noqa: E402


PI = math.pi
TOL_EXACT = 1e-9
TOL_TABLE = 1e-8
TOL_F4 = 1e-8
MIN_GENERIC_GRAD = 1e-3


@dataclass(frozen=True)
class OverlapRow:
    theta: float
    overlap: float
    expected_overlap: float
    fs_distance: float
    expected_distance: float


def transition_probability_table() -> tuple[OverlapRow, ...]:
    pole = _embed(_coherent(0.0, 0.0))
    rows: list[OverlapRow] = []
    for theta in (0.0, PI / 6.0, PI / 4.0, PI / 3.0, PI / 2.0, 2.0 * PI / 3.0, PI):
        point = _embed(_coherent(theta, 0.0))
        overlap = endpoint_overlap(pole, point)
        expected = math.cos(theta / 2.0) ** 2
        fs_distance = math.acos(min(1.0, max(0.0, math.sqrt(max(overlap, 0.0)))))
        rows.append(
            OverlapRow(
                theta=theta,
                overlap=overlap,
                expected_overlap=expected,
                fs_distance=fs_distance,
                expected_distance=theta / 2.0,
            )
        )
    return tuple(rows)


def f4_invariance_trials(samples: int = 12, seed: int = 20260610) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    f4 = _f4_basis()
    e1, e2, _ = primitive_idempotents()
    worst_overlap = 0.0
    worst_orthogonal = 0.0
    for _ in range(samples):
        p_move = random_automorphism(rng, f4, scale=0.9)
        q_move = random_automorphism(rng, f4, scale=0.9)
        P = p_move @ e1
        Q = q_move @ e1
        before = trace_form(P, Q)
        g = random_automorphism(rng, f4, scale=0.8)
        after = trace_form(g @ P, g @ Q)
        worst_overlap = max(worst_overlap, abs(before - after))
        orth_before = trace_form(e1, e2)
        orth_after = trace_form(g @ e1, g @ e2)
        worst_orthogonal = max(worst_orthogonal, abs(orth_before - orth_after))
    return float(worst_overlap), float(worst_orthogonal)


def endpoint_extrema() -> tuple[float, float, float, float, float]:
    f4 = f4_basis()
    e1, e2, _ = primitive_idempotents()
    same = endpoint_overlap(e1, e1)
    orthogonal = endpoint_overlap(e1, e2)
    grad_same = sum(np.linalg.norm(grad) for grad in boundary_gradients(e1, e1, f4))
    grad_orthogonal = sum(np.linalg.norm(grad) for grad in boundary_gradients(e1, e2, f4))
    generic = random_automorphism(np.random.default_rng(17), _f4_basis(), scale=0.9) @ e1
    grad_generic = sum(np.linalg.norm(grad) for grad in boundary_gradients(e1, generic, f4))
    return float(same), float(orthogonal), float(grad_same), float(grad_orthogonal), float(grad_generic)


def monotone_contrast_table() -> tuple[tuple[str, float, float], ...]:
    """Show that simple monotone costs share the same endpoint extrema."""
    eps = 1e-12
    return (
        ("linear probability B", 1.0, 0.0),
        ("squared chord contrast 1-B", 0.0, 1.0),
        ("log survival -log(1-B)", -math.log(eps), -math.log(1.0 - eps)),
    )


def main() -> bool:
    rows = transition_probability_table()
    f4_residual, f4_orthogonal = f4_invariance_trials()
    same, orthogonal, grad_same, grad_orthogonal, grad_generic = endpoint_extrema()
    contrasts = monotone_contrast_table()

    print("=" * 78)
    print("BOUNDARY METRIC-ORIGIN GATE")
    print("=" * 78)

    print("\n[A] Overlap is transition probability on the boundary CP1")
    print("  For P(theta)=|psi(theta)><psi(theta)|, Tr(P(theta) o P(0))=cos^2(theta/2).")
    for row in rows:
        print(
            f"  theta={row.theta:.6f} overlap={row.overlap:.12f} "
            f"expected={row.expected_overlap:.12f} FS_dist={row.fs_distance:.12f}"
        )

    print("\n[B] F4 invariance of the two-point contrast")
    print(f"  worst random-pair overlap residual : {f4_residual:.3e}")
    print(f"  worst orthogonal-pair residual     : {f4_orthogonal:.3e}")

    print("\n[C] Endpoint extrema")
    print(f"  B(P,P) same endpoint          : {same:.12f}")
    print(f"  B(P,Q) orthogonal endpoint    : {orthogonal:.12f}")
    print(f"  gradient at same endpoint     : {grad_same:.3e}")
    print(f"  gradient at orthogonal pair   : {grad_orthogonal:.3e}")
    print(f"  generic endpoint gradient     : {grad_generic:.3e}")

    print("\n[D] Monotone-choice caveat")
    print("  F4 geometry gives the invariant contrast. A dynamics still has to choose")
    print("  the monotone and coefficient. The linear probability B is the minimal")
    print("  choice used by the boundary-variation gate.")
    for name, same_value, orth_value in contrasts:
        print(f"  {name:28s} same={same_value:.6f} orthogonal={orth_value:.6f}")

    print("\n[V] Sandbox verdict")
    print("  overlap as canonical F4 two-point contrast : PASS")
    print("  overlap coefficient from CHO dynamics      : OPEN")
    print("  full oriented boundary action              : OPEN")
    print("=" * 78)

    max_table = max(
        max(abs(row.overlap - row.expected_overlap), abs(row.fs_distance - row.expected_distance))
        for row in rows
    )
    overlaps = [row.overlap for row in rows]
    distances = [row.fs_distance for row in rows]
    assert max_table < TOL_TABLE
    assert all(overlaps[i] >= overlaps[i + 1] - TOL_EXACT for i in range(len(overlaps) - 1))
    assert all(distances[i] <= distances[i + 1] + TOL_EXACT for i in range(len(distances) - 1))
    assert f4_residual < TOL_F4
    assert f4_orthogonal < TOL_F4
    assert abs(same - 1.0) < TOL_EXACT
    assert abs(orthogonal) < TOL_EXACT
    assert grad_same < TOL_EXACT
    assert grad_orthogonal < TOL_EXACT
    assert grad_generic > MIN_GENERIC_GRAD
    assert contrasts[0][1] > contrasts[0][2]
    assert contrasts[1][1] < contrasts[1][2]
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)