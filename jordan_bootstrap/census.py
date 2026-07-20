"""Gate O00 census: unit-octonion multiplication is a norm-preserving relabeling.

The amplitude campaign's Gate Q00 showed that monomial unitaries (permutations
composed with unit phases) cannot move a Born probability. This is its octonionic
successor: the representation changes are now multiplications by exact rational
unit octonions, and the invariant they must preserve is the Born *norm*
``|x|^2``. By Hurwitz multiplicativity the norm is preserved exactly, so the
census reports zero operational mismatches, while genuine controls (non-unit
scalings) are rejected and the non-associativity of the algebra is exhibited but
irrelevant to the norm invariance.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .octonion import (
    E,
    UNIT_OCTONIONS,
    census_states,
    octonion,
)


@dataclass(frozen=True)
class OctonionInvarianceCensus:
    """Exact tallies for Gate O00, owned and asserted by the test contract."""

    unit_count: int
    state_count: int
    norm_preservation_checks: int
    norm_mismatches: int
    composition_checks: int
    composition_non_units: int
    nonunit_control_checks: int
    nonunit_control_rejections: int
    nonassociative_triples: int


def representation_invariance_census() -> OctonionInvarianceCensus:
    """Enumerate every declared unit-octonion representation change exactly."""
    units = UNIT_OCTONIONS
    states = census_states()

    # (1) Left multiplication by any unit octonion preserves the Born norm.
    norm_checks = 0
    norm_mismatches = 0
    for unit in units:
        for state in states:
            norm_checks += 1
            if (unit * state).norm2() != state.norm2():
                norm_mismatches += 1

    # (2) The product of two units is again a unit (the set is norm-closed).
    composition_checks = 0
    composition_non_units = 0
    for left in units:
        for right in units:
            composition_checks += 1
            if not (left * right).is_unit():
                composition_non_units += 1

    # (3) Control: a genuine non-unit scaling *does* move the norm and is rejected.
    nonunit_scalars = (
        octonion(2, 0, 0, 0, 0, 0, 0, 0),
        octonion(0, 3, 0, 0, 0, 0, 0, 0),
        octonion(1, 1, 1, 0, 0, 0, 0, 0),
    )
    nonunit_checks = 0
    nonunit_rejections = 0
    for scalar in nonunit_scalars:
        for state in states:
            if state.is_zero():
                continue
            nonunit_checks += 1
            if (scalar * state).norm2() != state.norm2():
                nonunit_rejections += 1

    # (4) The algebra is genuinely non-associative: count basis triples for which
    #     associativity fails. (The quaternion control in the ladder gate is 0.)
    nonassociative = 0
    for a in E:
        for b in E:
            for c in E:
                if (a * b) * c != a * (b * c):
                    nonassociative += 1

    return OctonionInvarianceCensus(
        unit_count=len(units),
        state_count=len(states),
        norm_preservation_checks=norm_checks,
        norm_mismatches=norm_mismatches,
        composition_checks=composition_checks,
        composition_non_units=composition_non_units,
        nonunit_control_checks=nonunit_checks,
        nonunit_control_rejections=nonunit_rejections,
        nonassociative_triples=nonassociative,
    )
