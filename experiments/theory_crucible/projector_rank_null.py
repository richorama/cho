"""Projector-rank null for the frozen theta23 = 4/7 prediction.

This is the first experiment in the dynamics-first successor program. It asks a
deliberately adversarial question: after the Fano plane selects the four lines
avoiding a vacuum point, does the resulting operator contain spectral information
that distinguishes it from an arbitrary rank-four projector on a seven-dimensional
space?

The answer is no. The Fano construction canonically selects a subspace, but every
rank-four orthogonal projector in dimension seven lies on the same O(7) conjugacy
orbit and has normalized trace 4/7. A Haar-random unit vector also has expected
weight 4/7 in any such subspace. Therefore 4/7 becomes physical only if dynamics
derive both the avoidance subspace and the map from its projector weight to the
atmospheric oscillation probability.

No CHO constants are inputs. No audit or prediction credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/projector_rank_null.py
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np


DIMENSION = 7
VACUUM_POINT = 7
FANO_LINES = (
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
)


def avoidance_mask(vacuum_point: int = VACUUM_POINT) -> np.ndarray:
    """Indicator of Fano lines not incident on ``vacuum_point``."""
    return np.array(
        [float(vacuum_point not in line) for line in FANO_LINES], dtype=float
    )


def fano_avoidance_projector(vacuum_point: int = VACUUM_POINT) -> np.ndarray:
    """Orthogonal projector onto the vacuum-avoiding line subspace."""
    return np.diag(avoidance_mask(vacuum_point))


def haar_orthogonal(rng: np.random.Generator, dimension: int) -> np.ndarray:
    """Sample an orthogonal matrix with Haar-distributed column frame."""
    matrix = rng.normal(size=(dimension, dimension))
    orthogonal, triangular = np.linalg.qr(matrix)
    signs = np.where(np.diag(triangular) < 0.0, -1.0, 1.0)
    return orthogonal @ np.diag(signs)


def random_rank_projector(
    rng: np.random.Generator, dimension: int, rank: int
) -> np.ndarray:
    """Return a Haar-conjugated coordinate projector of the requested rank."""
    orthogonal = haar_orthogonal(rng, dimension)
    frame = orthogonal[:, :rank]
    return frame @ frame.T


def random_state_weights(
    projector: np.ndarray, rng: np.random.Generator, samples: int
) -> np.ndarray:
    """Weights x^T P x for uniformly random real unit vectors x."""
    states = rng.normal(size=(samples, projector.shape[0]))
    states /= np.linalg.norm(states, axis=1, keepdims=True)
    return np.einsum("ni,ij,nj->n", states, projector, states)


def spectral_signature(projector: np.ndarray) -> tuple[float, ...]:
    """Sorted eigenvalues, rounded only for stable reporting."""
    return tuple(np.round(np.linalg.eigvalsh(projector), 12))


def main() -> None:
    rng = np.random.default_rng(20260714)
    fano_projector = fano_avoidance_projector()
    rank = int(round(np.trace(fano_projector)))
    target = Fraction(rank, DIMENSION)

    assert rank == 4
    assert np.linalg.norm(fano_projector @ fano_projector - fano_projector) < 1e-14
    assert sum(VACUUM_POINT in line for line in FANO_LINES) == 3
    assert sum(VACUUM_POINT not in line for line in FANO_LINES) == 4

    generic_projector = random_rank_projector(rng, DIMENSION, rank)
    conjugator = haar_orthogonal(rng, DIMENSION)
    conjugated_fano = conjugator @ fano_projector @ conjugator.T

    signatures = {
        spectral_signature(fano_projector),
        spectral_signature(generic_projector),
        spectral_signature(conjugated_fano),
    }
    assert len(signatures) == 1
    assert abs(np.trace(generic_projector) / DIMENSION - float(target)) < 1e-14
    assert abs(np.trace(conjugated_fano) / DIMENSION - float(target)) < 1e-14

    samples = 250_000
    fano_weights = random_state_weights(fano_projector, rng, samples)
    generic_weights = random_state_weights(generic_projector, rng, samples)
    standard_error = np.std(fano_weights, ddof=1) / np.sqrt(samples)
    mean_gap = abs(np.mean(fano_weights) - np.mean(generic_weights))
    tolerance = 6.0 * standard_error

    assert abs(np.mean(fano_weights) - float(target)) < tolerance
    assert abs(np.mean(generic_weights) - float(target)) < tolerance
    assert mean_gap < 2.0 * tolerance

    print("=" * 74)
    print("THEORY CRUCIBLE 01: PROJECTOR-RANK NULL")
    print("=" * 74)
    print(f"Fano incidence split                 : 3 through + {rank} avoiding")
    print(f"Fano projector spectrum             : {spectral_signature(fano_projector)}")
    print(f"generic rank-{rank} spectrum           : {spectral_signature(generic_projector)}")
    print(f"normalized trace, both              : {target} = {float(target):.12f}")
    print(f"Haar-state mean, Fano projector     : {np.mean(fano_weights):.12f}")
    print(f"Haar-state mean, generic projector  : {np.mean(generic_weights):.12f}")
    print(f"Monte Carlo comparison tolerance    : {tolerance:.3e}")
    print()
    print("PROVED")
    print("  * Fano incidence canonically selects four of seven line-basis states.")
    print("  * Its projector has the universal rank-four spectrum {1^4, 0^3}.")
    print("  * Every rank-four projector in dimension seven has trace/dimension = 4/7.")
    print("  * Isotropic random states have expected projector weight 4/7.")
    print()
    print("NOT PROVED")
    print("  * that atmospheric mixing is the normalized trace or isotropic mean;")
    print("  * that dynamics select the Fano avoidance subspace rather than another")
    print("    rank-four subspace;")
    print("  * that the upper-octant choice (avoiding, not through) is physical.")
    print()
    print("VERDICT: the subspace is Fano-specific; the number 4/7 is rank-generic.")
    print("         N5 needs a dynamical observable map to carry physics content.")


if __name__ == "__main__":
    main()