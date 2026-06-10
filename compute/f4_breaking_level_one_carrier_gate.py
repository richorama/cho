"""
F4-BREAKING LEVEL-ONE CARRIER GATE -- does the two-level carrier select k=1?
================================================================================

`f4_breaking_primitive_level_gate.py` showed that WZ filling-independence forces
the level to be an integer, but does not by itself choose the primitive positive
level. This gate adds the next already-owned ingredient: the transition carrier
is the two-level CP^1/Bloch-sphere system from `epsilon_free_action.py` and
`epsilon_a4_two_level.py`.

For CP^1 with WZ level k, Borel-Weil/geometric quantization gives the SU(2)
representation of spin k/2, hence Hilbert dimension

    dim H_k = k + 1.

The A4/Q8 two-level carrier has dimension 2. Therefore matching the WZ
quantized carrier to the fundamental transition qubit selects k=1 uniquely.
Higher integer k are still valid WZ sectors, but they are higher-spin /
multi-state sectors with dimensions 3,4,..., not the fundamental two-state
transition used by the OP^2 Berry action.

What this proves
----------------
Given the already-audited two-level transition carrier, the discrete primitive
level is not an extra free integer: k=1 is the unique positive WZ level whose
quantization has dimension 2. Then the half-turn density is pi/432 and beta
matches -log(eps0).

What this still does not prove
------------------------------
This is not a beta variational principle. It does not derive the CHO term whose
stationarity equation identifies exp(-2 beta) with this WZ density, nor does it
derive the full F4-breaking action. It only removes the discrete level-selection
ambiguity once the fundamental two-state carrier is granted.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_level_one_carrier_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from epsilon_a4_two_level import (
    burnside_span_dimension,
    commutant_dimension,
    double_cover,
    klein_four_subgroup,
    su2_lie_algebra_dimension,
    tetrahedral_group,
)
from f4_breaking_primitive_level_gate import (
    CARRIER_DIM,
    PI,
    TARGET,
    beta_from_density,
    half_turn_density,
    level_family,
)
from f4_breaking_seed_op2 import EPS0, EPS0_SQ


TOL = 1e-12


@dataclass(frozen=True)
class TwoLevelWitness:
    a4_order: int
    v4_order: int
    q8_order: int
    commutant_dim: int
    burnside_span_dim: int
    su2_lie_dim: int
    carrier_dim: int
    passes: bool


@dataclass(frozen=True)
class CarrierLevelRow:
    level: int
    quantized_dimension: int
    matches_two_level_carrier: bool
    density: float
    beta: float | None
    positive_gibbs_admissible: bool


@dataclass(frozen=True)
class CarrierSelection:
    admissible_positive_levels: int
    two_state_matching_levels: tuple[int, ...]
    selected_level: int
    selected_density: float
    selected_beta: float
    level_one_selected_by_carrier: bool
    beta_variational_map_derived: bool


def two_level_witness() -> TwoLevelWitness:
    """Recover the fundamental two-state carrier from the A4 -> Q8 witness."""
    a4_group = tetrahedral_group()
    klein_four = klein_four_subgroup(a4_group)
    quaternion_group = double_cover(klein_four)
    span_dim = burnside_span_dimension(quaternion_group)
    carrier_dim = int(round(math.sqrt(span_dim)))
    witness = TwoLevelWitness(
        a4_order=len(a4_group),
        v4_order=len(klein_four),
        q8_order=len(quaternion_group),
        commutant_dim=commutant_dimension(quaternion_group),
        burnside_span_dim=span_dim,
        su2_lie_dim=su2_lie_algebra_dimension(quaternion_group),
        carrier_dim=carrier_dim,
        passes=(
            len(a4_group) == 12
            and len(klein_four) == 4
            and len(quaternion_group) == 8
            and commutant_dimension(quaternion_group) == 1
            and span_dim == 4
            and carrier_dim == 2
            and su2_lie_algebra_dimension(quaternion_group) == 3
        ),
    )
    return witness


def cp1_quantized_dimension(level: int) -> int:
    """Borel-Weil dimension for CP^1 with WZ/Chern level k: dim H_k = k+1."""
    if level < 0:
        raise ValueError("level must be non-negative")
    return level + 1


def carrier_level_rows(max_level: int = 6) -> tuple[CarrierLevelRow, ...]:
    carrier_dim = two_level_witness().carrier_dim
    rows = []
    for level in range(max_level + 1):
        density = half_turn_density(float(level))
        rows.append(
            CarrierLevelRow(
                level=level,
                quantized_dimension=cp1_quantized_dimension(level),
                matches_two_level_carrier=(cp1_quantized_dimension(level) == carrier_dim),
                density=float(density),
                beta=beta_from_density(density),
                positive_gibbs_admissible=(0.0 < density < 1.0),
            )
        )
    return tuple(rows)


def carrier_selection() -> CarrierSelection:
    witness = two_level_witness()
    family = level_family()
    matching_levels = tuple(
        level
        for level in range(1, family.max_positive_admissible + 1)
        if cp1_quantized_dimension(level) == witness.carrier_dim
    )
    assert matching_levels
    selected_level = matching_levels[0]
    density = half_turn_density(float(selected_level))
    beta = beta_from_density(density)
    assert beta is not None
    return CarrierSelection(
        admissible_positive_levels=family.count_positive_admissible,
        two_state_matching_levels=matching_levels,
        selected_level=selected_level,
        selected_density=float(density),
        selected_beta=float(beta),
        level_one_selected_by_carrier=(matching_levels == (1,)),
        beta_variational_map_derived=False,
    )


def main() -> bool:
    witness = two_level_witness()
    rows = carrier_level_rows()
    selection = carrier_selection()

    print("=" * 78)
    print("F4-BREAKING LEVEL-ONE CARRIER GATE")
    print("Does the two-level CP^1 carrier select the primitive WZ level?")
    print("=" * 78)

    print("\n[A] A4/Q8 witness for the fundamental two-state carrier")
    print(f"  |A4|                              : {witness.a4_order}")
    print(f"  |V4|                              : {witness.v4_order}")
    print(f"  |Q8|                              : {witness.q8_order}")
    print(f"  Q8 commutant dimension             : {witness.commutant_dim}")
    print(f"  Burnside span dimension            : {witness.burnside_span_dim} = dim M2(C)")
    print(f"  SU(2) Lie algebra dimension        : {witness.su2_lie_dim}")
    print(f"  transition carrier dimension       : {witness.carrier_dim}")

    print("\n[B] CP^1 Borel-Weil quantization by WZ level")
    print("  level k quantizes to spin k/2, hence dim H_k = k+1.")
    for row in rows:
        beta_str = "n/a" if row.beta is None else f"{row.beta:.12f}"
        print(
            f"  k={row.level:2d}  dim H_k={row.quantized_dimension:2d}  "
            f"two-state={row.matches_two_level_carrier!s:5s}  "
            f"density={row.density:.9f}  beta={beta_str}"
        )

    print("\n[C] Selection inside the previously admissible integer family")
    print(
        f"  positive WZ levels with k*pi/{CARRIER_DIM} < 1 : "
        f"{selection.admissible_positive_levels}"
    )
    print(f"  levels whose quantization is two-state         : {selection.two_state_matching_levels}")
    print(f"  selected level                                 : {selection.selected_level}")
    print(f"  selected density                               : {selection.selected_density:.15f}")
    print(f"  target pi/432                                  : {TARGET:.15f}")
    print(f"  selected beta                                  : {selection.selected_beta:.12f}")
    print(f"  target beta                                    : {-math.log(EPS0):.12f}")

    print("\n[V] Verdict")
    print("  integrality alone selects k=1                  : NO")
    print("  two-level carrier selects k=1                  : YES")
    print("  primitive density equals pi/432                : YES")
    print("  beta variational map derived                   : NO")
    print("  remaining object                               : beta-dependent F4-breaking action")
    print("  Bayes/scoreboard credit moved                  : NO")
    print("=" * 78)

    assert witness.passes
    assert witness.carrier_dim == 2
    assert CARRIER_DIM == 432
    assert abs(TARGET - EPS0_SQ) < TOL
    assert selection.admissible_positive_levels > 1, "integrality family must remain non-singleton"
    assert selection.two_state_matching_levels == (1,)
    assert selection.level_one_selected_by_carrier
    assert rows[1].matches_two_level_carrier
    assert not rows[0].positive_gibbs_admissible
    assert not rows[2].matches_two_level_carrier
    assert abs(selection.selected_density - TARGET) < TOL
    assert abs(selection.selected_beta + math.log(EPS0)) < TOL
    assert not selection.beta_variational_map_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)