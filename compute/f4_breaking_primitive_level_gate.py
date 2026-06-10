"""
F4-BREAKING PRIMITIVE LEVEL GATE -- can WZ integrality select k=1?
========================================================================

`f4_breaking_beta_selection_gate.py` left a discrete sub-bridge open. A Wess-Zumino
term can quantise the flux density to

    exp(-2 beta_k) = k*pi/432,

but level quantisation alone gives an integer family. This gate records the exact
part and the still-open part in the audited harness.

What is proved here
-------------------
For a CP^1 WZ disk action

    S_WZ = (k/2) * Omega,

changing the filling by a full sphere shifts the action by `2*pi*k`. Therefore
single-valuedness of `exp(i S_WZ)` forces `k` to be an integer. With the Schur
carrier weight `1/432`, the oriented half-turn density is `k*pi/432`.

What is not proved here
-----------------------
There are many admissible positive integer levels: `k=1,2,...,137` keep
`k*pi/432 < 1` and hence define positive Gibbs ratios. The target is exactly
the minimal positive, primitive level `k=1`, but the statement "the physical
sector is primitive level one" is a selection rule not derived by integrality
alone.

Net: continuous WZ normalization freedom is killed; discrete primitive-sector
selection remains open. No Bayes credit moves.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_primitive_level_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math

from f4_breaking_seed_op2 import EPS0, EPS0_SQ


PI = math.pi
CARRIER_DIM = 16 * 27
TARGET = PI / CARRIER_DIM
TOL_PHASE = 1e-12
TOL_TARGET = 1e-14


@dataclass(frozen=True)
class LevelRow:
    level: float
    full_sphere_jump: float
    phase_residual: float
    single_valued: bool
    density: float
    beta: float | None
    target_error: float


@dataclass(frozen=True)
class LevelFamily:
    min_positive: int
    max_positive_admissible: int
    count_positive_admissible: int
    primitive_density: float
    primitive_beta: float
    integrality_selects_unique_level: bool


def full_sphere_jump(level: float) -> float:
    return 2.0 * PI * level


def filling_phase_residual(level: float) -> float:
    return abs(cmath.exp(1j * full_sphere_jump(level)) - 1.0)


def half_turn_density(level: float, orientation: int = +1) -> float:
    if orientation not in (-1, +1):
        raise ValueError("orientation must be +1 or -1")
    return orientation * level * PI / CARRIER_DIM


def beta_from_density(density: float) -> float | None:
    if not (0.0 < density < 1.0):
        return None
    return -0.5 * math.log(density)


def level_rows() -> tuple[LevelRow, ...]:
    test_levels = (0.0, 0.5, math.sqrt(2.0), 1.0, 2.0, 3.0, 137.0, 138.0)
    rows = []
    for level in test_levels:
        residual = filling_phase_residual(level)
        density = half_turn_density(level)
        rows.append(
            LevelRow(
                level=float(level),
                full_sphere_jump=full_sphere_jump(level),
                phase_residual=float(residual),
                single_valued=residual < TOL_PHASE,
                density=float(density),
                beta=beta_from_density(density),
                target_error=abs(density - TARGET),
            )
        )
    return tuple(rows)


def level_family() -> LevelFamily:
    max_positive = int(math.floor((CARRIER_DIM - 1e-12) / PI))
    density = half_turn_density(1.0)
    beta = beta_from_density(density)
    assert beta is not None
    return LevelFamily(
        min_positive=1,
        max_positive_admissible=max_positive,
        count_positive_admissible=max_positive,
        primitive_density=float(density),
        primitive_beta=float(beta),
        integrality_selects_unique_level=(max_positive == 1),
    )


def main() -> bool:
    rows = level_rows()
    family = level_family()

    print("=" * 78)
    print("F4-BREAKING PRIMITIVE LEVEL GATE")
    print("Does WZ integrality select the level that fixes beta?")
    print("=" * 78)

    print("\n[A] Filling independence quantises the WZ level")
    print("  S_WZ=(k/2)Omega; changing disk filling by S^2 shifts S by 2*pi*k.")
    for row in rows:
        beta_str = "n/a" if row.beta is None else f"{row.beta:.12f}"
        print(
            f"  k={row.level:9.6f} jump={row.full_sphere_jump:12.6f} "
            f"phase_resid={row.phase_residual:.3e} single={row.single_valued} "
            f"density={row.density:.9f} beta={beta_str} |.-target|={row.target_error:.3e}"
        )

    print("\n[B] Positive integer level family")
    print(f"  positive admissible levels k*pi/432 < 1 : 1..{family.max_positive_admissible}")
    print(f"  count of positive admissible levels      : {family.count_positive_admissible}")
    print(f"  integrality selects unique level?        : {family.integrality_selects_unique_level}")

    print("\n[C] Primitive positive level")
    print(f"  primitive k                             : {family.min_positive}")
    print(f"  primitive density                       : {family.primitive_density:.15f}")
    print(f"  target pi/432                           : {TARGET:.15f}")
    print(f"  primitive beta                          : {family.primitive_beta:.12f}")
    print(f"  target beta                             : {-math.log(EPS0):.12f}")

    print("\n[V] Verdict")
    print("  continuous WZ coefficient freedom        : KILLED by integrality")
    print("  primitive k=1 gives beta target          : EXACT, conditional")
    print("  integrality alone selects k=1            : NO")
    print("  missing object                           : primitive-sector selection rule")
    print("  Bayes/scoreboard credit moved            : NO")
    print("=" * 78)

    integer_rows = [row for row in rows if abs(row.level - round(row.level)) < TOL_PHASE]
    noninteger_rows = [row for row in rows if abs(row.level - round(row.level)) >= TOL_PHASE]
    assert CARRIER_DIM == 432
    assert abs(TARGET - EPS0_SQ) < TOL_TARGET
    assert all(row.single_valued for row in integer_rows)
    assert all(not row.single_valued for row in noninteger_rows)
    assert family.count_positive_admissible > 1, "integrality alone must not select k=1"
    assert family.min_positive == 1
    assert not family.integrality_selects_unique_level
    assert abs(family.primitive_density - TARGET) < TOL_TARGET
    assert abs(family.primitive_beta + math.log(EPS0)) < TOL_TARGET
    assert rows[-2].beta is not None and rows[-1].beta is None, "k=137 is admissible but k=138 is not"
    derived_primitive_sector = False
    assert not derived_primitive_sector, "this gate must not promote primitive k=1 to a derived sector"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)