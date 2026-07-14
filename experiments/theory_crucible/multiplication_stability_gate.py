"""Local stability of octonionic signed-Fano products under continuous defects.

Replace each of the seven line signs by a real coefficient w_l while preserving
the Fano support, identity, imaginary squares, and anticommutativity. Define a
label-blind loss as the squared residual of norm composition and alternativity.

At every exact survivor from the signed census, this gate computes the Jacobian
of all residual equations with respect to the seven coefficients. Full rank means
the solution is locally isolated; positive eigenvalues of J^T J mean every small
non-coordinate coefficient perturbation raises the loss quadratically.

This tests robustness conditional on the algebraic objective. It does not explain
why physical dynamics should minimize that objective.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/multiplication_stability_gate.py
"""

from __future__ import annotations

from itertools import product

import numpy as np

from signed_fano_multiplication_census import (
    FANO_TRIPLES,
    alternativity_residual,
    composition_residual,
    multiplication_table,
    standard_signed_orbit,
)


def weighted_multiplication_table(weights: np.ndarray) -> np.ndarray:
    """Continuous Fano-supported product with seven real line coefficients."""
    if weights.shape != (7,):
        raise ValueError("weights must have shape (7,)")
    table = np.zeros((8, 8, 8), dtype=float)
    for index in range(8):
        table[0, index, index] = 1.0
        table[index, 0, index] = 1.0
    for index in range(1, 8):
        table[index, index, 0] = -1.0
    for weight, (left, right, result) in zip(weights, FANO_TRIPLES):
        for first, second, output in (
            (left, right, result),
            (right, result, left),
            (result, left, right),
        ):
            table[first, second, output] = weight
            table[second, first, output] = -weight
    return table


def continuous_associator(
    table: np.ndarray, first: int, second: int, third: int
) -> np.ndarray:
    left_associated = np.einsum(
        "m,mk->k", table[first, second], table[:, third]
    )
    right_associated = np.einsum(
        "m,mk->k", table[second, third], table[first]
    )
    return left_associated - right_associated


def defect_vector(weights: np.ndarray) -> np.ndarray:
    """All composition and alternativity residual components."""
    table = weighted_multiplication_table(weights)
    left = tuple(table[index].T for index in range(8))
    identity = np.eye(8)
    residuals = []

    for first in range(8):
        for second in range(first, 8):
            target = 2.0 * identity if first == second else np.zeros((8, 8))
            residuals.extend(
                (left[first].T @ left[second] + left[second].T @ left[first] - target).ravel()
            )

    for first in range(1, 8):
        for second in range(first, 8):
            for third in range(1, 8):
                residuals.extend(
                    continuous_associator(table, first, second, third)
                    + continuous_associator(table, second, first, third)
                )
                residuals.extend(
                    continuous_associator(table, first, second, third)
                    + continuous_associator(table, first, third, second)
                )
    return np.asarray(residuals)


def defect_loss(weights: np.ndarray) -> float:
    residual = defect_vector(weights)
    return float(residual @ residual)


def numerical_jacobian(weights: np.ndarray, step: float = 1e-6) -> np.ndarray:
    columns = []
    for index in range(len(weights)):
        shift = np.zeros_like(weights)
        shift[index] = step
        columns.append(
            (defect_vector(weights + shift) - defect_vector(weights - shift))
            / (2.0 * step)
        )
    return np.column_stack(columns)


def main() -> None:
    survivors = tuple(sorted(standard_signed_orbit()))
    ranks = []
    minimum_curvatures = []
    maximum_curvatures = []
    zero_losses = []

    for signs in survivors:
        weights = np.asarray(signs, dtype=float)
        loss = defect_loss(weights)
        jacobian = numerical_jacobian(weights)
        singular_values = np.linalg.svd(jacobian, compute_uv=False)
        gram_eigenvalues = np.linalg.eigvalsh(jacobian.T @ jacobian)
        ranks.append(int(np.count_nonzero(singular_values > 1e-7)))
        minimum_curvatures.append(float(gram_eigenvalues[0]))
        maximum_curvatures.append(float(gram_eigenvalues[-1]))
        zero_losses.append(loss)

    assert len(survivors) == 16
    assert max(zero_losses) < 1e-20
    assert set(ranks) == {7}
    assert min(minimum_curvatures) > 1.0

    rng = np.random.default_rng(20260714)
    reference = np.ones(7)
    perturbation_rows = []
    for scale in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2):
        normalized_losses = []
        for _ in range(40):
            direction = rng.normal(size=7)
            direction /= np.linalg.norm(direction)
            displacement = scale * direction
            normalized_losses.append(
                defect_loss(reference + displacement) / (scale * scale)
            )
        perturbation_rows.append(
            (scale, min(normalized_losses), float(np.mean(normalized_losses)))
        )

    assert all(minimum > 1.0 for _, minimum, _ in perturbation_rows)

    invalid_losses = []
    survivor_set = set(survivors)
    for signs in product((-1, 1), repeat=7):
        if signs not in survivor_set:
            invalid_losses.append(defect_loss(np.asarray(signs, dtype=float)))
            assert composition_residual(multiplication_table(signs)) > 0
            assert alternativity_residual(multiplication_table(signs)) > 0
    assert len(invalid_losses) == 112
    assert min(invalid_losses) > 1.0

    print("=" * 74)
    print("THEORY CRUCIBLE 08: MULTIPLICATION-STABILITY GATE")
    print("=" * 74)
    print(f"exact survivor minima tested         : {len(survivors)}")
    print(f"Jacobian ranks                       : {sorted(set(ranks))} / 7")
    print(f"minimum local curvature J^T J        : {min(minimum_curvatures):.6f}")
    print(f"maximum local curvature J^T J        : {max(maximum_curvatures):.6f}")
    print(f"minimum loss of 112 discrete controls: {min(invalid_losses):.6f}")
    print()
    print(" perturbation norm    min(loss/norm^2)    mean(loss/norm^2)")
    print(" -----------------    ----------------    -----------------")
    for scale, minimum, mean in perturbation_rows:
        print(f" {scale:>17.1e}    {minimum:>16.6f}    {mean:>17.6f}")
    print()
    print("PROVED WITHIN THE CONTINUOUS FANO-SUPPORTED FAMILY")
    print("  * All 16 octonionic coordinate copies are isolated zero-defect points.")
    print("  * The residual Jacobian has full rank seven at every copy.")
    print("  * Every sufficiently small coefficient perturbation raises the neutral")
    print("    composition-plus-alternativity loss quadratically.")
    print("  * All 112 non-octonionic discrete orientations have finite positive loss.")
    print()
    print("NOT PROVED")
    print("  * that this defect loss is a physical action or free energy;")
    print("  * attraction under a derived time evolution;")
    print("  * stability against products outside the fixed Fano support family.")
    print()
    print("VERDICT: octonionic multiplication is mathematically robust, not a fragile")
    print("         sign convention. Physical selection of this loss remains open.")


if __name__ == "__main__":
    main()