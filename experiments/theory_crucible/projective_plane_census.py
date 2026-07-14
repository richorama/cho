"""Matched incidence-geometry census containing the Fano plane as q=2.

For each prime q, construct PG(2,q) directly from one-dimensional subspaces of
GF(q)^3. Every point lies on q+1 lines and avoids q^2 lines among
q^2+q+1 total, giving the generic projector fraction

    q^2 / (q^2 + q + 1).

The Fano value 4/7 is therefore the smallest member (q=2) of an infinite
projective-plane family. A minimum-size objective selects q=2, but it selects the
ordinary finite field GF(2) construction just as well as an octonionic reading.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/projective_plane_census.py
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


PRIMES = (2, 3, 5, 7)


def inverse_mod(value: int, prime: int) -> int:
    """Multiplicative inverse in a prime field."""
    return pow(value, prime - 2, prime)


def canonical_projective_vector(vector: tuple[int, int, int], prime: int) -> tuple[int, int, int]:
    """Normalize the first nonzero coordinate to one."""
    for value in vector:
        if value % prime:
            inverse = inverse_mod(value % prime, prime)
            return tuple((coordinate * inverse) % prime for coordinate in vector)
    raise ValueError("the zero vector is not a projective point")


def projective_vectors(prime: int) -> tuple[tuple[int, int, int], ...]:
    """One representative for every point of PG(2, prime)."""
    representatives = {
        canonical_projective_vector(vector, prime)
        for vector in product(range(prime), repeat=3)
        if any(vector)
    }
    return tuple(sorted(representatives))


def dot_mod(
    left: tuple[int, int, int], right: tuple[int, int, int], prime: int
) -> int:
    return sum(a * b for a, b in zip(left, right)) % prime


def incidence_matrix(prime: int) -> tuple[tuple[int, ...], ...]:
    """Point-line incidence; dual vectors label projective lines."""
    points = projective_vectors(prime)
    lines = projective_vectors(prime)
    return tuple(
        tuple(1 if dot_mod(point, line, prime) == 0 else 0 for line in lines)
        for point in points
    )


def verify_projective_plane(prime: int) -> dict[str, int | Fraction]:
    points = projective_vectors(prime)
    incidence = incidence_matrix(prime)
    total = prime * prime + prime + 1
    through = prime + 1
    avoiding = prime * prime

    assert len(points) == total
    assert len(incidence) == total
    assert all(sum(row) == through for row in incidence)
    assert all(sum(incidence[row][column] for row in range(total)) == through for column in range(total))

    for first in range(total):
        for second in range(first + 1, total):
            common_lines = sum(
                incidence[first][column] * incidence[second][column]
                for column in range(total)
            )
            assert common_lines == 1

    for first in range(total):
        for second in range(first + 1, total):
            common_points = sum(
                incidence[row][first] * incidence[row][second]
                for row in range(total)
            )
            assert common_points == 1

    return {
        "q": prime,
        "points": total,
        "through": through,
        "avoiding": avoiding,
        "fraction": Fraction(avoiding, total),
    }


def main() -> None:
    rows = tuple(verify_projective_plane(prime) for prime in PRIMES)
    fano = rows[0]

    assert fano == {
        "q": 2,
        "points": 7,
        "through": 3,
        "avoiding": 4,
        "fraction": Fraction(4, 7),
    }
    assert all(
        row["through"] + row["avoiding"] == row["points"] for row in rows
    )
    assert all(
        row["fraction"]
        == Fraction(int(row["q"]) ** 2, int(row["q"]) ** 2 + int(row["q"]) + 1)
        for row in rows
    )
    assert min(rows, key=lambda row: int(row["points"])) == fano

    print("=" * 74)
    print("THEORY CRUCIBLE 06: MATCHED PROJECTIVE-PLANE CENSUS")
    print("=" * 74)
    print(" q    total lines    through    avoiding    avoiding/total")
    print("--    -----------    -------    --------    --------------")
    for row in rows:
        print(
            f"{int(row['q']):>2}    {int(row['points']):>11}    "
            f"{int(row['through']):>7}    {int(row['avoiding']):>8}    "
            f"{str(row['fraction']):>14}"
        )
    print()
    print("PROVED")
    print("  * Every PG(2,q) control has the same structural split")
    print("    (q+1 through) + (q^2 avoiding) = q^2+q+1.")
    print("  * The normalized avoidance trace is generically q^2/(q^2+q+1).")
    print("  * Fano 4/7 is exactly the q=2 member and the minimum-size member.")
    print("  * The projective-plane axioms alone reproduce the split without")
    print("    division algebras or exceptional groups.")
    print()
    print("NOT PROVED")
    print("  * that nature minimizes q or incidence-space size;")
    print("  * that the q=2 plane's octonionic realization is physically selected;")
    print("  * that any avoidance fraction is a neutrino observable.")
    print()
    print("VERDICT: 4/7 is minimal projective-plane incidence, not an")
    print("         exceptional-geometry discriminator. Octonionic content would")
    print("         need an observable unavailable to the matched PG(2,q) controls.")


if __name__ == "__main__":
    main()