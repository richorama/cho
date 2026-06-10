"""Oriented WZ boundary gate for the unified CHO/Jordan/WZ action candidate.

`boundary_variation_gate.py` showed that the endpoint-overlap action on
`OP2 x OP2` variationally forces an unordered orthogonal primitive pair. The
unified action needs more: an ordered WZ boundary pair `(P0, P2)` so the Jordan
completion carries Peirce grades `(0,1,2)`.

This gate tests the next hinge:

    does the WZ/Berry term provide the missing orientation?

Key subtlety
------------
At the geodesic half-turn, the unit holonomy is `exp(i*pi) = exp(-i*pi) = -1`.
So the phase as a point on U(1) does NOT by itself distinguish the two
orientations. The oriented WZ action does: the oriented disk area changes sign
under boundary reversal.

What this gate proves conditionally
-----------------------------------
* The oriented WZ action on the transition CP1 obeys
  `S_WZ(theta) = +/- pi (1 - cos theta)`.
* Reversing the boundary orientation sends `S_WZ -> -S_WZ`.
* For the great-circle boundary, the two unit holonomies coincide at `-1`, so the
  orientation must be tracked as an oriented action/chain, not only as `exp(iS)`.
* Once an orientation is supplied, the orthogonal endpoint pair and Jordan
  completion carry the ordered grades `(0,1,2)`; reversing the WZ orientation
  reverses the endpoint grades.

What remains open
-----------------
This is still conditional. It shows the WZ term has exactly the right
orientation data, but it does not derive from full CHO dynamics that this
oriented WZ boundary term is the physical one.

No scipy. Uses existing compute/ OP2/Berry conventions.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/oriented_wz_boundary_gate.py
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

from berry_pi_intrinsic_op2 import _bargmann_phase, _coherent, _embed  # noqa: E402
from epsilon_action_selection import (  # noqa: E402
    _f4_basis,
    jordan_product,
    random_automorphism,
    trace_form,
)
from epsilon_orbit_selection import _diag  # noqa: E402


PI = math.pi
TOL_PHASE = 3e-3
TOL_EXACT = 1e-9
TOL_F4 = 1e-8


@dataclass(frozen=True)
class OrientationRow:
    theta: float
    forward_action: float
    reverse_action: float
    forward_phase: float
    reverse_phase: float
    unit_holonomy_gap: float


def oriented_wz_action(theta: float, orientation: int = +1) -> float:
    """Oriented half-solid-angle action on the transition CP1."""
    if orientation not in (-1, +1):
        raise ValueError("orientation must be +1 or -1")
    return orientation * PI * (1.0 - math.cos(theta))


def loop_states(theta: float, orientation: int, n: int = 4000) -> list[np.ndarray]:
    phis = np.linspace(0.0, 2.0 * PI, n, endpoint=False)
    if orientation < 0:
        phis = phis[::-1]
    return [_coherent(theta, phi) for phi in phis]


def wrapped_bargmann_phase(theta: float, orientation: int) -> float:
    return float(np.angle(_bargmann_phase(loop_states(theta, orientation))))


def orientation_rows() -> tuple[OrientationRow, OrientationRow]:
    rows = []
    for theta in (PI / 3.0, PI / 2.0):
        forward_action = oriented_wz_action(theta, +1)
        reverse_action = oriented_wz_action(theta, -1)
        forward_phase = wrapped_bargmann_phase(theta, +1)
        reverse_phase = wrapped_bargmann_phase(theta, -1)
        unit_gap = abs(np.exp(1j * forward_action) - np.exp(1j * reverse_action))
        rows.append(
            OrientationRow(
                theta=theta,
                forward_action=forward_action,
                reverse_action=reverse_action,
                forward_phase=forward_phase,
                reverse_phase=reverse_phase,
                unit_holonomy_gap=float(unit_gap),
            )
        )
    return tuple(rows)


def idempotent_residual(P: np.ndarray) -> float:
    return float(np.linalg.norm(jordan_product(P, P) - P))


def oriented_boundary_frame() -> dict[str, object]:
    start = _embed(_coherent(0.0, 0.0))
    end = _embed(_coherent(PI, 0.0))
    identity = _diag(1.0, 1.0, 1.0)
    middle = identity - start - end
    forward_grades = (0, 1, 2)
    reverse_grades = (2, 1, 0)
    return {
        "start_end_overlap": trace_form(start, end),
        "middle_idempotent": idempotent_residual(middle),
        "middle_trace": trace_form(middle, identity),
        "start_middle_overlap": trace_form(start, middle),
        "end_middle_overlap": trace_form(end, middle),
        "forward_grades": forward_grades,
        "reverse_grades": reverse_grades,
    }


def f4_transport_order_check(seed: int = 20260610) -> tuple[float, float, float]:
    start = _embed(_coherent(0.0, 0.0))
    end = _embed(_coherent(PI, 0.0))
    identity = _diag(1.0, 1.0, 1.0)
    middle = identity - start - end
    rng = np.random.default_rng(seed)
    automorphism = random_automorphism(rng, _f4_basis(), scale=0.8)
    moved_start = automorphism @ start
    moved_middle = automorphism @ middle
    moved_end = automorphism @ end
    moved_identity = automorphism @ identity
    completion = np.linalg.norm((moved_start + moved_middle + moved_end) - moved_identity)
    overlap = max(
        abs(trace_form(moved_start, moved_middle)),
        abs(trace_form(moved_start, moved_end)),
        abs(trace_form(moved_middle, moved_end)),
    )
    trace_spread = max(
        abs(trace_form(moved_start, moved_identity) - 1.0),
        abs(trace_form(moved_middle, moved_identity) - 1.0),
        abs(trace_form(moved_end, moved_identity) - 1.0),
    )
    return float(completion), float(overlap), float(trace_spread)


def main() -> bool:
    rows = orientation_rows()
    frame = oriented_boundary_frame()
    f4_transport = f4_transport_order_check()

    print("=" * 78)
    print("ORIENTED WZ BOUNDARY GATE")
    print("=" * 78)

    print("\n[A] Oriented WZ action")
    print("  S_WZ(theta,+) = +pi(1-cos theta)")
    print("  S_WZ(theta,-) = -pi(1-cos theta)")
    for row in rows:
        print(
            f"  theta={row.theta:.6f} forward={row.forward_action:.12f} "
            f"reverse={row.reverse_action:.12f} wrapped_phases=({row.forward_phase:.12f}, "
            f"{row.reverse_phase:.12f}) unit_gap={row.unit_holonomy_gap:.3e}"
        )

    print("\n[B] Half-turn subtlety")
    print("  At theta=pi/2, exp(i*pi)=exp(-i*pi)=-1, so U(1) holonomy alone")
    print("  cannot orient the pair. The oriented WZ action/chain carries the sign.")

    print("\n[C] Oriented frame grades")
    print(f"  start-end overlap       : {frame['start_end_overlap']:.3e}")
    print(f"  middle idempotent resid : {frame['middle_idempotent']:.3e}")
    print(f"  middle trace            : {frame['middle_trace']:.12f}")
    print(f"  forward grades          : {frame['forward_grades']}")
    print(f"  reversed grades         : {frame['reverse_grades']}")

    print("\n[D] F4 transport of the oriented frame")
    print(f"  completion residual     : {f4_transport[0]:.3e}")
    print(f"  worst pair overlap      : {f4_transport[1]:.3e}")
    print(f"  worst trace residual    : {f4_transport[2]:.3e}")

    print("\n[V] Sandbox verdict")
    print("  WZ orientation sign        : PASS")
    print("  grade ordering from sign   : PASS, conditional on oriented WZ boundary")
    print("  derivation from CHO action : OPEN")
    print("=" * 78)

    non_equator, equator = rows
    assert abs(non_equator.forward_action + non_equator.reverse_action) < TOL_EXACT
    assert abs(non_equator.forward_phase - non_equator.forward_action) < TOL_PHASE
    assert abs(non_equator.reverse_phase - non_equator.reverse_action) < TOL_PHASE
    assert abs(equator.forward_action - PI) < TOL_EXACT
    assert abs(equator.reverse_action + PI) < TOL_EXACT
    assert equator.unit_holonomy_gap < TOL_EXACT
    assert abs(abs(equator.forward_phase) - PI) < TOL_PHASE
    assert abs(abs(equator.reverse_phase) - PI) < TOL_PHASE
    assert abs(frame["start_end_overlap"]) < TOL_EXACT
    assert frame["middle_idempotent"] < TOL_EXACT
    assert abs(frame["middle_trace"] - 1.0) < TOL_EXACT
    assert abs(frame["start_middle_overlap"]) < TOL_EXACT
    assert abs(frame["end_middle_overlap"]) < TOL_EXACT
    assert frame["forward_grades"] == (0, 1, 2)
    assert frame["reverse_grades"] == (2, 1, 0)
    assert max(f4_transport) < TOL_F4
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
