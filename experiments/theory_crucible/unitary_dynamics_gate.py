"""Classify stabilizer-invariant unitary dynamics on natural flavour targets.

For the irreducible three-dimensional representation of the vacuum stabilizer,
Schur's lemma forces every invariant Hermitian Hamiltonian to be a scalar. Its
evolution is a global phase and produces no flavour transitions.

For the reducible three-line permutation representation 1+2, every invariant
Hermitian Hamiltonian has two energies,

    H = energy_symmetric P_symmetric + energy_zero_sum P_zero_sum.

Between two distinct line-basis flavours its transition probability is

    4/9 sin^2((energy_symmetric-energy_zero_sum)t/2),

so its maximum is 4/9, below 4/7. Obtaining the frozen upper-octant value therefore
requires breaking the vacuum stabilizer, changing the target/map, or abandoning
this direct unitary interpretation.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/unitary_dynamics_gate.py
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from fano_selection_no_go import (
    VACUUM,
    act_on_line,
    act_on_point,
    automorphisms,
    fano_lines,
)
from observable_map_gate import (
    induced_permutation,
    intertwiner_dimension,
    permutation_matrix,
    zero_sum_basis,
)


def commutant_dimension(representations: tuple[np.ndarray, ...]) -> int:
    """Dimension of real matrices commuting with every representation matrix."""
    dimension = representations[0].shape[0]
    equations = [
        np.kron(representation.T, np.eye(dimension))
        - np.kron(np.eye(dimension), representation)
        for representation in representations
    ]
    singular_values = np.linalg.svd(np.vstack(equations), compute_uv=False)
    return int(np.count_nonzero(singular_values < 1e-10))


def permutation_hamiltonian(energy_symmetric: float, energy_zero_sum: float) -> np.ndarray:
    """Most general invariant Hermitian Hamiltonian on the three-line target."""
    symmetric_projector = np.ones((3, 3), dtype=complex) / 3.0
    zero_sum_projector = np.eye(3, dtype=complex) - symmetric_projector
    return energy_symmetric * symmetric_projector + energy_zero_sum * zero_sum_projector


def unitary_from_two_projectors(
    energy_symmetric: float, energy_zero_sum: float, time: float
) -> np.ndarray:
    symmetric_projector = np.ones((3, 3), dtype=complex) / 3.0
    zero_sum_projector = np.eye(3, dtype=complex) - symmetric_projector
    return (
        np.exp(-1j * energy_symmetric * time) * symmetric_projector
        + np.exp(-1j * energy_zero_sum * time) * zero_sum_projector
    )


def off_diagonal_probability(gap_time: float) -> float:
    """Exact functional form for one distinct-flavour transition."""
    return (4.0 / 9.0) * np.sin(gap_time / 2.0) ** 2


def main() -> None:
    lines = fano_lines()
    through = tuple(line for line in lines if VACUUM in line)
    avoiding = tuple(line for line in lines if VACUUM not in line)
    stabilizer = tuple(
        matrix
        for matrix in automorphisms()
        if act_on_point(matrix, VACUUM) == VACUUM
    )
    through_representations = tuple(
        permutation_matrix(induced_permutation(matrix, through))
        for matrix in stabilizer
    )
    avoiding_representations = tuple(
        permutation_matrix(induced_permutation(matrix, avoiding))
        for matrix in stabilizer
    )
    standard_basis = zero_sum_basis(4)
    standard_representations = tuple(
        standard_basis.T @ representation @ standard_basis
        for representation in avoiding_representations
    )

    through_commutant = commutant_dimension(through_representations)
    standard_commutant = commutant_dimension(standard_representations)
    assert through_commutant == 2
    assert standard_commutant == 1
    assert intertwiner_dimension(standard_representations, standard_representations) == 1

    identity = np.eye(3)
    standard_scalar_residual = max(
        np.linalg.norm(representation @ identity - identity @ representation)
        for representation in standard_representations
    )
    assert standard_scalar_residual < 1e-14

    energy_symmetric = 1.7
    energy_zero_sum = -0.4
    hamiltonian = permutation_hamiltonian(energy_symmetric, energy_zero_sum)
    invariant_residual = max(
        np.linalg.norm(hamiltonian @ representation - representation @ hamiltonian)
        for representation in through_representations
    )
    assert invariant_residual < 1e-12

    gap = energy_symmetric - energy_zero_sum
    times = np.linspace(0.0, 8.0 * np.pi / abs(gap), 4001)
    numerical_probabilities = []
    formula_probabilities = []
    unitarity_residual = 0.0
    for time in times:
        unitary = unitary_from_two_projectors(
            energy_symmetric, energy_zero_sum, time
        )
        numerical_probabilities.append(abs(unitary[1, 0]) ** 2)
        formula_probabilities.append(off_diagonal_probability(gap * time))
        unitarity_residual = max(
            unitarity_residual,
            np.linalg.norm(unitary.conj().T @ unitary - np.eye(3)),
        )

    maximum_probability = max(numerical_probabilities)
    formula_residual = max(
        abs(numerical - formula)
        for numerical, formula in zip(numerical_probabilities, formula_probabilities)
    )
    assert unitarity_residual < 1e-12
    assert formula_residual < 1e-12
    assert abs(maximum_probability - 4.0 / 9.0) < 1e-12
    assert Fraction(4, 9) < Fraction(4, 7)

    print("=" * 74)
    print("THEORY CRUCIBLE 05: STABILIZER-INVARIANT UNITARY DYNAMICS")
    print("=" * 74)
    print(f"commutant dimension, irreducible 3 : {standard_commutant}")
    print(f"commutant dimension, target 1+2    : {through_commutant}")
    print(f"invariant-Hamiltonian residual      : {invariant_residual:.3e}")
    print(f"unitarity residual                  : {unitarity_residual:.3e}")
    print(f"transition-formula residual         : {formula_residual:.3e}")
    print(f"maximum distinct-flavour probability: {Fraction(4, 9)}")
    print(f"frozen upper-octant target          : {Fraction(4, 7)}")
    print()
    print("PROVED FOR STABILIZER-INVARIANT UNITARY DYNAMICS")
    print("  * On the irreducible flavour 3, every invariant Hamiltonian is scalar;")
    print("    evolution is a global phase and produces no flavour oscillation.")
    print("  * On the permutation target 1+2, every invariant Hamiltonian has one")
    print("    physical energy gap and P(i->j)=4/9 sin^2(gap*t/2) for i != j.")
    print("  * Its maximum 4/9 is strictly below 4/7.")
    print()
    print("NOT PROVED")
    print("  * a no-go after explicit stabilizer breaking;")
    print("  * a no-go for open-system or nonlinear evolution;")
    print("  * that line-basis transitions are PMNS flavour transitions.")
    print()
    print("VERDICT: exact stabilizer symmetry plus direct three-flavour unitarity")
    print("         cannot produce the frozen 4/7 atmospheric value.")


if __name__ == "__main__":
    main()