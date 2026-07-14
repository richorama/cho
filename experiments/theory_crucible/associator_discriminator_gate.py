"""Associator Gram-spectrum discriminator against all signed-Fano controls.

For each unordered imaginary basis pair (a,b), define the transport-defect map

    M_ab(x) = [x,a,b]

on the seven-dimensional imaginary space, and its basis-independent Gram operator
G_ab = M_ab^T M_ab. The standard octonion product gives

    spec(G_ab) = (0,0,0,4,4,4,4)

for every one of the 21 pairs. This gate computes the complete pair-spectrum
fingerprint for all 128 signed Fano products and asks whether any non-octonionic
orientation can imitate it.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/associator_discriminator_gate.py
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np

from signed_fano_multiplication_census import (
    basis_associator,
    multiplication_table,
    standard_signed_orbit,
)


EXPECTED_SPECTRUM = (0, 0, 0, 4, 4, 4, 4)


def transport_defect(table: np.ndarray, first: int, second: int) -> np.ndarray:
    """Matrix x -> [x,e_first,e_second] on the imaginary basis."""
    return np.column_stack(
        [basis_associator(table, source, first, second)[1:] for source in range(1, 8)]
    ).astype(np.int64)


def gram_fingerprint(table: np.ndarray) -> tuple[tuple[int, ...], ...]:
    """Sorted Gram spectra over all 21 unordered imaginary source pairs."""
    spectra = []
    for first, second in combinations(range(1, 8), 2):
        defect = transport_defect(table, first, second)
        gram = defect.T @ defect
        eigenvalues = tuple(
            int(value) for value in np.rint(np.linalg.eigvalsh(gram)).astype(int)
        )
        spectra.append(eigenvalues)
    return tuple(sorted(spectra))


def exact_octonion_gram(table: np.ndarray) -> bool:
    """Exact polynomial/rank test equivalent to spectrum {0^3,4^4} for each pair."""
    for first, second in combinations(range(1, 8), 2):
        defect = transport_defect(table, first, second)
        gram = defect.T @ defect
        if not np.array_equal(gram @ gram, 4 * gram):
            return False
        if int(np.trace(gram)) != 16:
            return False
        if np.linalg.matrix_rank(gram.astype(float), tol=1e-10) != 4:
            return False
    return True


def main() -> None:
    survivor_orbit = standard_signed_orbit()
    standard = multiplication_table((1,) * 7)
    reference_fingerprint = gram_fingerprint(standard)

    assert set(reference_fingerprint) == {EXPECTED_SPECTRUM}
    assert len(reference_fingerprint) == 21
    assert exact_octonion_gram(standard)

    fingerprint_matches = set()
    exact_matches = set()
    failing_pair_counts = []
    for signs in product((-1, 1), repeat=7):
        table = multiplication_table(signs)
        fingerprint = gram_fingerprint(table)
        if fingerprint == reference_fingerprint:
            fingerprint_matches.add(signs)
        if exact_octonion_gram(table):
            exact_matches.add(signs)
        if signs not in survivor_orbit:
            failing_pair_counts.append(
                sum(
                    gram_fingerprint_for_pair(table, first, second) != EXPECTED_SPECTRUM
                    for first, second in combinations(range(1, 8), 2)
                )
            )

    assert fingerprint_matches == set(survivor_orbit)
    assert exact_matches == set(survivor_orbit)
    assert len(failing_pair_counts) == 112
    assert min(failing_pair_counts) > 0

    print("=" * 74)
    print("THEORY CRUCIBLE 09: ASSOCIATOR DISCRIMINATOR")
    print("=" * 74)
    print(f"source pairs tested per product      : 21")
    print(f"octonion Gram spectrum, every pair   : {EXPECTED_SPECTRUM}")
    print(f"signed-Fano products tested          : 128")
    print(f"complete-fingerprint matches         : {len(fingerprint_matches)}")
    print(f"exact polynomial/rank matches        : {len(exact_matches)}")
    print(f"matches equal octonion orbit         : {exact_matches == set(survivor_orbit)}")
    print(f"fewest failed pairs among controls   : {min(failing_pair_counts)} / 21")
    print()
    print("PROVED WITHIN THE MATCHED SIGNED-FANO CENSUS")
    print("  * Every octonion source pair produces a rank-four transport defect")
    print("    with three flat and four equal-curvature directions.")
    print("  * The exact identities G^2=4G and Tr G=16 hold for all 21 pairs.")
    print("  * No non-octonionic line orientation reproduces the complete spectrum.")
    print("  * Unlike 4/7 incidence counting, this discriminator requires the")
    print("    multiplication and its nonzero associator.")
    print()
    print("NOT PROVED")
    print("  * that G_ab acts on spacetime, flavour, or any measured Hilbert space;")
    print("  * a Lorentzian metric or physical dynamics;")
    print("  * uniqueness against arbitrary products outside signed Fano support.")
    print()
    print("VERDICT: the associator Gram spectrum is a genuine octonionic invariant")
    print("         unavailable to incidence-only PG(2,2). It is a valid candidate")
    print("         carrier for the next physical-map test, not yet physics itself.")


def gram_fingerprint_for_pair(
    table: np.ndarray, first: int, second: int
) -> tuple[int, ...]:
    defect = transport_defect(table, first, second)
    gram = defect.T @ defect
    return tuple(int(value) for value in np.rint(np.linalg.eigvalsh(gram)).astype(int))


if __name__ == "__main__":
    main()