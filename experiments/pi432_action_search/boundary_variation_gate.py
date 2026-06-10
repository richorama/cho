"""Boundary-variation gate for the unified CHO/Jordan/WZ action candidate.

The unified boundary action currently assumes an ordered orthogonal primitive
boundary pair `(P0, P2)` in OP2. This gate tests the next hinge directly:

    can a boundary variational term force the orthogonal pair?

Candidate boundary term
-----------------------
On `OP2 x OP2`, take the endpoint-overlap functional

    B(P, Q) = Tr(P o Q),

where P and Q are primitive idempotents. Minimizing B maximizes endpoint contrast.
For primitive idempotents, B is in [0,1]. The global minima are orthogonal pairs,
B=0, and then the Jordan completion R = I - P - Q is the third primitive
idempotent of the frame.

What this gate proves conditionally
-----------------------------------
* The F4-orbit gradient of B vanishes at equal endpoints (maximum) and orthogonal
  endpoints (minimum).
* Random endpoint pairs flow monotonically to B ~ 0 under boundary-gradient
  descent on OP2 x OP2.
* The descended endpoints complete to a primitive Jordan frame.

What this gate does NOT prove
-----------------------------
The overlap term is symmetric: B(P,Q)=B(Q,P). It forces an unordered orthogonal
pair, not the ordered WZ boundary pair. The orientation/order still has to come
from the WZ term, a descent construction, or another dynamical input.

No scipy. Uses existing compute/ F4/J3(O) machinery.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/boundary_variation_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
COMPUTE = ROOT / "compute"
if str(COMPUTE) not in sys.path:
    sys.path.insert(0, str(COMPUTE))

from epsilon_action_selection import (  # noqa: E402
    _expm,
    _f4_basis,
    jordan_product,
    random_automorphism,
    trace_form,
)
from epsilon_orbit_selection import _diag, primitive_idempotents  # noqa: E402


TOL_EXACT = 1e-9
TOL_FLOW = 1e-8
MIN_RANDOM_GRAD = 1e-3
FLOW_STEPS = 500
FLOW_DT = 0.4


@dataclass(frozen=True)
class FlowRow:
    seed: int
    initial_overlap: float
    final_overlap: float
    monotone: bool
    completion_idempotent_residual: float
    completion_trace_residual: float
    completion_pair_overlap: float


def f4_basis() -> list[np.ndarray]:
    return [np.asarray(D).real for D in _f4_basis()]


def endpoint_overlap(P: np.ndarray, Q: np.ndarray) -> float:
    return float(trace_form(P, Q))


def boundary_gradients(P: np.ndarray, Q: np.ndarray, f4: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    grad_P = np.array([trace_form(D @ P, Q) for D in f4])
    grad_Q = np.array([trace_form(P, D @ Q) for D in f4])
    return grad_P, grad_Q


def gradient_norm(P: np.ndarray, Q: np.ndarray, f4: list[np.ndarray]) -> float:
    grad_P, grad_Q = boundary_gradients(P, Q, f4)
    return float(np.linalg.norm(grad_P) + np.linalg.norm(grad_Q))


def random_op2_point(seed: int, f4: list[np.ndarray]) -> np.ndarray:
    E1, _, _ = primitive_idempotents()
    rng = np.random.default_rng(seed)
    return random_automorphism(rng, f4, scale=1.0) @ E1


def descent_flow(P: np.ndarray, Q: np.ndarray, f4: list[np.ndarray],
                 steps: int = FLOW_STEPS, dt: float = FLOW_DT) -> tuple[np.ndarray, np.ndarray, list[float]]:
    history: list[float] = []
    for _ in range(steps):
        history.append(endpoint_overlap(P, Q))
        grad_P, grad_Q = boundary_gradients(P, Q, f4)
        if np.linalg.norm(grad_P) + np.linalg.norm(grad_Q) < 1e-13:
            break
        gen_P = sum(g * D for g, D in zip(grad_P, f4))
        gen_Q = sum(g * D for g, D in zip(grad_Q, f4))
        P = _expm(-dt * gen_P) @ P
        Q = _expm(-dt * gen_Q) @ Q
    history.append(endpoint_overlap(P, Q))
    return P, Q, history


def idempotent_residual(P: np.ndarray) -> float:
    return float(np.linalg.norm(jordan_product(P, P) - P))


def frame_completion_diagnostics(P: np.ndarray, Q: np.ndarray) -> tuple[float, float, float]:
    identity = _diag(1.0, 1.0, 1.0)
    R = identity - P - Q
    idem = idempotent_residual(R)
    trace_residual = abs(trace_form(R, identity) - 1.0)
    pair_overlap = max(abs(endpoint_overlap(P, R)), abs(endpoint_overlap(Q, R)))
    return idem, trace_residual, pair_overlap


def critical_point_table(f4: list[np.ndarray]) -> dict[str, tuple[float, float]]:
    E1, E2, _ = primitive_idempotents()
    random_P = random_op2_point(0, f4)
    random_Q = random_op2_point(1, f4)
    return {
        "same endpoint (maximum)": (endpoint_overlap(E1, E1), gradient_norm(E1, E1, f4)),
        "orthogonal endpoints (minimum)": (endpoint_overlap(E1, E2), gradient_norm(E1, E2, f4)),
        "generic endpoints": (endpoint_overlap(random_P, random_Q), gradient_norm(random_P, random_Q, f4)),
    }


def flow_trials(f4: list[np.ndarray], seeds: tuple[int, ...] = (0, 1, 2, 3)) -> tuple[FlowRow, ...]:
    rows: list[FlowRow] = []
    for seed in seeds:
        P = random_op2_point(10 + 2 * seed, f4)
        Q = random_op2_point(11 + 2 * seed, f4)
        P_final, Q_final, history = descent_flow(P, Q, f4)
        monotone = all(history[i + 1] <= history[i] + 1e-12 for i in range(len(history) - 1))
        completion = frame_completion_diagnostics(P_final, Q_final)
        rows.append(
            FlowRow(
                seed=seed,
                initial_overlap=history[0],
                final_overlap=history[-1],
                monotone=monotone,
                completion_idempotent_residual=completion[0],
                completion_trace_residual=completion[1],
                completion_pair_overlap=completion[2],
            )
        )
    return tuple(rows)


def orientation_obstruction() -> tuple[float, bool]:
    E1, E2, _ = primitive_idempotents()
    symmetry_residual = abs(endpoint_overlap(E1, E2) - endpoint_overlap(E2, E1))
    ordering_still_external = True
    return symmetry_residual, ordering_still_external


def main() -> bool:
    f4 = f4_basis()
    table = critical_point_table(f4)
    rows = flow_trials(f4)
    symmetry_residual, ordering_still_external = orientation_obstruction()

    print("=" * 78)
    print("BOUNDARY VARIATION GATE")
    print("=" * 78)

    print("\n[A] Boundary functional")
    print("  B(P,Q) = Tr(P o Q) on OP2 x OP2")
    print("  Descent of B forces endpoint contrast; B=0 means orthogonal endpoints.")

    print("\n[B] Critical endpoint pairs")
    for name, (value, grad) in table.items():
        print(f"  {name:32s} overlap={value:.12f}  gradient_norm={grad:.3e}")

    print("\n[C] Descent from generic boundary pairs")
    for row in rows:
        print(
            f"  seed={row.seed} initial={row.initial_overlap:.6f} "
            f"final={row.final_overlap:.3e} monotone={row.monotone} "
            f"completion_idem={row.completion_idempotent_residual:.3e}"
        )

    print("\n[D] Jordan-frame completion")
    print("  For descended endpoints, R = I - P - Q is primitive and orthogonal.")
    print(f"  worst completion idempotent residual : {max(r.completion_idempotent_residual for r in rows):.3e}")
    print(f"  worst completion trace residual      : {max(r.completion_trace_residual for r in rows):.3e}")
    print(f"  worst completion pair overlap        : {max(r.completion_pair_overlap for r in rows):.3e}")

    print("\n[E] Orientation obstruction")
    print(f"  B(P,Q)-B(Q,P) residual : {symmetry_residual:.3e}")
    print("  The overlap variation is symmetric. It forces an unordered orthogonal pair,")
    print("  but the WZ orientation/order still has to be derived separately.")

    print("\n[V] Sandbox verdict")
    print("  orthogonal boundary pair from variation : PASS")
    print("  ordered WZ boundary pair                : OPEN")
    print("  full boundary action from CHO dynamics  : OPEN")
    print("=" * 78)

    same_value, same_grad = table["same endpoint (maximum)"]
    orth_value, orth_grad = table["orthogonal endpoints (minimum)"]
    generic_value, generic_grad = table["generic endpoints"]
    assert abs(same_value - 1.0) < TOL_EXACT
    assert same_grad < TOL_EXACT
    assert abs(orth_value) < TOL_EXACT
    assert orth_grad < TOL_EXACT
    assert 0.0 < generic_value < 1.0
    assert generic_grad > MIN_RANDOM_GRAD
    assert all(row.monotone for row in rows)
    assert max(row.final_overlap for row in rows) < TOL_FLOW
    assert max(row.completion_idempotent_residual for row in rows) < TOL_FLOW
    assert max(row.completion_trace_residual for row in rows) < TOL_FLOW
    assert max(row.completion_pair_overlap for row in rows) < TOL_FLOW
    assert symmetry_residual < TOL_EXACT
    assert ordering_still_external
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
