"""WZ level/integrality gate for the unified boundary action.

The previous gates established, conditionally:

* `boundary_variation_gate.py`: the boundary variation forces an unordered
  orthogonal endpoint pair.
* `oriented_wz_boundary_gate.py`: an oriented WZ boundary action distinguishes
  `+pi` from `-pi` and orders the Peirce grades.
* `wz_flux_normalization_gate.py`: once the WZ half-flux is `pi` and the carrier
  is `Delta_9 x J3(O)`, the flux density is `pi/432`.

This gate attacks the next coefficient question: is the WZ coefficient a free
real number, or an integral level?

Claim tested here
-----------------
For a WZ disk action

    S_WZ = (k/2) * Omega,

where `Omega` is oriented solid angle on the transition CP1, two fillings of the
same boundary differ by a full sphere:

    Delta S = (k/2) * 4 pi = 2 pi k.

Single-valuedness of `exp(i S)` under changing the filling requires `k` to be an
integer. The primitive nonzero sector is therefore `|k|=1`, and the oriented
half-turn gives `S = +/- pi`. Averaging over the Schur carrier then gives
`Phi = pi/432` for level one.

Honest scope
------------
This removes a continuous WZ coefficient from the sandbox candidate. It does not
prove that CHO dynamics supplies this WZ term, nor does it derive the full
`Delta_9 x J3(O)` carrier from the boundary action. It also leaves a discrete
level choice: `k=1` is the primitive/minimal nonzero level, not a consequence of
this gate alone.

No scipy. Pure arithmetic/phase check.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/wz_level_integrality_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

import numpy as np


PI = math.pi
CARRIER_DIM = 16 * 27
SCHUR_WEIGHT = Fraction(1, CARRIER_DIM)
TOL_PHASE = 1e-12


@dataclass(frozen=True)
class LevelRow:
    level: float
    full_sphere_jump: float
    phase_residual: float
    single_valued: bool
    half_turn_action: float
    normalized_density: float


def full_sphere_jump(level: float) -> float:
    return 2.0 * PI * level


def filling_phase_residual(level: float) -> float:
    return float(abs(np.exp(1j * full_sphere_jump(level)) - 1.0))


def is_single_valued(level: float) -> bool:
    return filling_phase_residual(level) < TOL_PHASE


def half_turn_action(level: float, orientation: int = +1) -> float:
    if orientation not in (-1, +1):
        raise ValueError("orientation must be +1 or -1")
    return orientation * PI * level


def normalized_density(level: float, orientation: int = +1) -> float:
    return half_turn_action(level, orientation) * float(SCHUR_WEIGHT)


def level_table() -> tuple[LevelRow, ...]:
    test_levels = (-2.0, -1.0, 0.0, 0.5, math.sqrt(2.0), 1.0, 2.0)
    rows = []
    for level in test_levels:
        residual = filling_phase_residual(level)
        rows.append(
            LevelRow(
                level=level,
                full_sphere_jump=full_sphere_jump(level),
                phase_residual=residual,
                single_valued=residual < TOL_PHASE,
                half_turn_action=half_turn_action(level),
                normalized_density=normalized_density(level),
            )
        )
    return tuple(rows)


def primitive_level() -> int:
    nonzero_integral_levels = [k for k in range(-4, 5) if k != 0]
    return min(nonzero_integral_levels, key=lambda k: abs(k))


def main() -> bool:
    rows = level_table()
    primitive = primitive_level()
    phi = normalized_density(abs(primitive))
    reverse_phi = normalized_density(abs(primitive), orientation=-1)

    print("=" * 78)
    print("WZ LEVEL / INTEGRALITY GATE")
    print("=" * 78)

    print("\n[A] Filling independence")
    print("  S_WZ = (k/2) Omega; changing disk filling by one sphere shifts S by 2*pi*k.")
    print("  exp(iS) is filling-independent only for integral k.")
    for row in rows:
        print(
            f"  k={row.level: .12f}  DeltaS={row.full_sphere_jump: .12f} "
            f"phase_resid={row.phase_residual:.3e} single_valued={row.single_valued}"
        )

    print("\n[B] Primitive nonzero level")
    print(f"  primitive level |k|       : {abs(primitive)}")
    print(f"  half-turn action          : {half_turn_action(abs(primitive)):.12f}")
    print(f"  reversed half-turn action : {half_turn_action(abs(primitive), -1):.12f}")

    print("\n[C] Carrier-normalized flux density")
    print(f"  carrier dimension         : {CARRIER_DIM}")
    print(f"  Schur carrier weight      : {SCHUR_WEIGHT}")
    print(f"  level-one density         : {phi:.15f}")
    print(f"  reversed density          : {reverse_phi:.15f}")

    print("\n[D] What this closes and what it does not")
    print("  Closed in sandbox: the WZ coefficient is an integer level, not a free real.")
    print("  Still open: derive the oriented WZ term, the carrier, and level-one")
    print("  primitiveness from full CHO dynamics.")

    print("\n[V] Sandbox verdict")
    print("  continuous WZ coefficient : KILLED")
    print("  primitive level-one flux  : PASS, conditional on WZ term + carrier")
    print("  full CHO derivation       : OPEN")
    print("=" * 78)

    integer_levels = [row for row in rows if abs(row.level - round(row.level)) < TOL_PHASE]
    noninteger_levels = [row for row in rows if abs(row.level - round(row.level)) >= TOL_PHASE]
    assert CARRIER_DIM == 432
    assert SCHUR_WEIGHT == Fraction(1, 432)
    assert all(row.single_valued for row in integer_levels)
    assert all(not row.single_valued for row in noninteger_levels)
    assert primitive in (-1, 1)
    assert abs(abs(half_turn_action(abs(primitive))) - PI) < TOL_PHASE
    assert abs(phi - PI / 432.0) < TOL_PHASE
    assert abs(reverse_phi + PI / 432.0) < TOL_PHASE
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
