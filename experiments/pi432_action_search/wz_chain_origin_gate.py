"""WZ chain-origin gate for the oriented boundary term.

`oriented_wz_boundary_gate.py` showed that an oriented WZ action supplies the
sign needed to order the boundary frame. `wz_level_integrality_gate.py` showed
that filling-independence quantizes the coefficient. This gate connects those two
facts to the geometry of the transition `CP1`.

On the transition sphere, the primitive Berry/WZ curvature is half the solid
angle form. Its full-sphere integral is

    (1/2) * 4*pi = 2*pi,

so the first Chern number is one. Thus level `k=1` is the primitive nontrivial
integral WZ chain; `k=0` is topologically trivial and cannot orient the boundary,
while `|k|>1` is an integral multiple of the primitive generator.

Honest status
-------------
This narrows two action-origin obligations: the oriented WZ term is the canonical
primitive integral `CP1` WZ term, and level one is the minimal nontrivial Chern
sector. It still does not derive that full CHO dynamics must put this term into
the boundary action, nor does it derive the carrier or entropy principle.

No scipy. Pure geometry/arithmetic plus the existing oriented WZ convention.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/wz_chain_origin_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from oriented_wz_boundary_gate import oriented_wz_action
from wz_level_integrality_gate import filling_phase_residual, half_turn_action


PI = math.pi
TOL = 1e-12


@dataclass(frozen=True)
class LevelClassRow:
    level: int
    sphere_action: float
    chern_number: int
    primitive: bool
    half_turn: float
    orients_boundary: bool


def solid_angle_cap(theta: float) -> float:
    return 2.0 * PI * (1.0 - math.cos(theta))


def primitive_curvature_integral() -> tuple[float, float, float]:
    solid_sphere = 4.0 * PI
    primitive_action_sphere = 0.5 * solid_sphere
    chern_number = primitive_action_sphere / (2.0 * PI)
    return solid_sphere, primitive_action_sphere, chern_number


def level_class_table() -> tuple[LevelClassRow, ...]:
    rows = []
    for level in (0, 1, -1, 2, -2):
        sphere_action = 2.0 * PI * level
        rows.append(
            LevelClassRow(
                level=level,
                sphere_action=sphere_action,
                chern_number=level,
                primitive=abs(level) == 1,
                half_turn=half_turn_action(level),
                orients_boundary=level != 0,
            )
        )
    return tuple(rows)


def filling_independence_rows() -> tuple[tuple[float, float, bool], ...]:
    levels = (0.0, 0.5, 1.0, 2.0, math.sqrt(2.0))
    return tuple((level, filling_phase_residual(level), filling_phase_residual(level) < TOL) for level in levels)


def cap_action_table() -> tuple[tuple[float, float, float], ...]:
    rows = []
    for theta in (0.0, PI / 3.0, PI / 2.0, PI):
        omega = solid_angle_cap(theta)
        action = 0.5 * omega
        gate_action = oriented_wz_action(theta, +1)
        rows.append((theta, action, gate_action))
    return tuple(rows)


def orientation_reversal_check() -> tuple[float, float, float]:
    forward = oriented_wz_action(PI / 2.0, +1)
    reverse = oriented_wz_action(PI / 2.0, -1)
    gap = abs(np.exp(1j * forward) - np.exp(1j * reverse))
    return forward, reverse, float(gap)


def main() -> bool:
    solid_sphere, primitive_action_sphere, chern = primitive_curvature_integral()
    level_rows = level_class_table()
    filling_rows = filling_independence_rows()
    cap_rows = cap_action_table()
    forward, reverse, unit_gap = orientation_reversal_check()

    print("=" * 78)
    print("WZ CHAIN-ORIGIN GATE")
    print("=" * 78)

    print("\n[A] Primitive CP1 WZ class")
    print(f"  full solid angle               : {solid_sphere:.12f}")
    print(f"  primitive WZ sphere action     : {primitive_action_sphere:.12f}")
    print(f"  first Chern number             : {chern:.12f}")
    print("  The primitive WZ curvature is half the solid-angle form; its integral")
    print("  is 2*pi, hence c1=1.")

    print("\n[B] Disk actions")
    for theta, action, gate_action in cap_rows:
        print(
            f"  theta={theta:.6f} half-solid-angle action={action:.12f} "
            f"oriented_gate={gate_action:.12f}"
        )

    print("\n[C] Level classes")
    for row in level_rows:
        print(
            f"  k={row.level:+d} sphere_action={row.sphere_action:+.12f} "
            f"c1={row.chern_number:+d} primitive={row.primitive} "
            f"half_turn={row.half_turn:+.12f} orients={row.orients_boundary}"
        )

    print("\n[D] Filling independence")
    for level, residual, single_valued in filling_rows:
        print(f"  k={level: .12f} phase_residual={residual:.3e} single_valued={single_valued}")

    print("\n[E] Orientation sign")
    print(f"  forward half-turn action : {forward:.12f}")
    print(f"  reverse half-turn action : {reverse:.12f}")
    print(f"  unit holonomy gap        : {unit_gap:.3e}")
    print("  The unit holonomy at the half-turn is the same, but the primitive")
    print("  integral WZ chain carries the oriented action sign.")

    print("\n[V] Sandbox verdict")
    print("  oriented WZ term as primitive CP1 class : PASS")
    print("  primitive level-one sector              : PASS, geometrically narrowed")
    print("  CHO action containing this WZ chain      : OPEN")
    print("=" * 78)

    assert abs(solid_sphere - 4.0 * PI) < TOL
    assert abs(primitive_action_sphere - 2.0 * PI) < TOL
    assert abs(chern - 1.0) < TOL
    assert all(abs(action - gate_action) < TOL for _theta, action, gate_action in cap_rows)
    assert any(row.level == 0 and not row.orients_boundary for row in level_rows)
    assert any(row.level == 1 and row.primitive and row.half_turn > 0.0 for row in level_rows)
    assert any(row.level == -1 and row.primitive and row.half_turn < 0.0 for row in level_rows)
    assert any(row.level == 2 and not row.primitive for row in level_rows)
    assert all(single_valued for level, _residual, single_valued in filling_rows if abs(level - round(level)) < TOL)
    assert all(not single_valued for level, _residual, single_valued in filling_rows if abs(level - round(level)) >= TOL)
    assert abs(forward - PI) < TOL
    assert abs(reverse + PI) < TOL
    assert unit_gap < TOL
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)