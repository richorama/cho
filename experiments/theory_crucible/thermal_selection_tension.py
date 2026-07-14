"""Thermal-selection tension for a 3+4 Fano sector split.

After a vacuum choice, Fano symmetry permits a Hamiltonian

    H = energy_through P_through + energy_avoiding P_avoiding.

For a Gibbs state at inverse temperature beta, the avoiding-sector probability is

    p_avoiding = 4 exp(-beta energy_avoiding)
                 / (3 exp(-beta energy_through) + 4 exp(-beta energy_avoiding)).

It equals exactly 4/7 only when beta times the energy gap is zero. Thus ordinary
equilibrium selection cannot both energetically distinguish the sectors and retain
the exact state-count probability. The statement is about this minimal dynamics,
not a no-go for every quantum dynamical observable map.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/thermal_selection_tension.py
"""

from __future__ import annotations

import math


THROUGH_DEGENERACY = 3
AVOIDING_DEGENERACY = 4
STATE_COUNT_VALUE = AVOIDING_DEGENERACY / (
    THROUGH_DEGENERACY + AVOIDING_DEGENERACY
)


def avoiding_probability(beta_gap: float) -> float:
    """Gibbs probability of the avoiding sector for gap E_avoid - E_through."""
    relative_weight = math.exp(-beta_gap)
    return (AVOIDING_DEGENERACY * relative_weight) / (
        THROUGH_DEGENERACY + AVOIDING_DEGENERACY * relative_weight
    )


def beta_gap_for_probability(probability: float) -> float:
    """Invert the two-sector Gibbs law."""
    if not 0.0 < probability < 1.0:
        raise ValueError("probability must lie strictly between zero and one")
    relative_weight = (
        probability * THROUGH_DEGENERACY
        / (AVOIDING_DEGENERACY * (1.0 - probability))
    )
    return -math.log(relative_weight)


def main() -> None:
    assert abs(avoiding_probability(0.0) - STATE_COUNT_VALUE) < 1e-15
    assert abs(beta_gap_for_probability(STATE_COUNT_VALUE)) < 1e-15

    controls = tuple(
        (beta_gap, avoiding_probability(beta_gap))
        for beta_gap in (-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0)
    )
    probabilities = tuple(probability for _, probability in controls)
    assert all(left > right for left, right in zip(probabilities, probabilities[1:]))
    assert avoiding_probability(-1.0) > STATE_COUNT_VALUE
    assert avoiding_probability(1.0) < STATE_COUNT_VALUE

    finite_nonzero_gaps = (-8.0, -1.0, -0.1, 0.1, 1.0, 8.0)
    assert all(
        abs(avoiding_probability(gap) - STATE_COUNT_VALUE) > 1e-12
        for gap in finite_nonzero_gaps
    )

    print("=" * 74)
    print("THEORY CRUCIBLE 03: THERMAL-SELECTION TENSION")
    print("=" * 74)
    print(f"sector degeneracies                   : {THROUGH_DEGENERACY} + {AVOIDING_DEGENERACY}")
    print(f"equiprobable avoiding weight          : {STATE_COUNT_VALUE:.12f} = 4/7")
    print()
    print(" beta*(E_avoid-E_through)    p_avoiding")
    print(" ------------------------    ----------")
    for beta_gap, probability in controls:
        print(f" {beta_gap:>24.1f}    {probability:.10f}")
    print()
    print("PROVED FOR THE MINIMAL GIBBS DYNAMICS")
    print("  * p_avoiding = 4/7 iff beta*(E_avoid-E_through) = 0.")
    print("  * A finite-temperature energetic preference changes the probability")
    print("    away from the exact state-count ratio.")
    print("  * The upper-octant inequality p_avoiding > 4/7 requires the avoiding")
    print("    sector to have lower energy; symmetry does not fix that sign.")
    print()
    print("NOT PROVED")
    print("  * a no-go for non-equilibrium, coherent, or scattering observables;")
    print("  * that PMNS probabilities are Gibbs sector occupations;")
    print("  * that a derived dynamics could not output 4/7 by another mechanism.")
    print()
    print("VERDICT: in the minimal equilibrium model, exact 4/7 diagnoses no")
    print("         energetic sector selection, not a dynamically preferred sector.")


if __name__ == "__main__":
    main()