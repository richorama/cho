"""
Sector projector derivation diagnostic.

This script extracts as much of the 1, 3, 8 sector multiplicity pattern as the
current codebase can justify from the C tensor O ladder/Fock representation.
It does not prove the final CHO Yukawa operator; it identifies exactly which
part of the sector projector story is now representation-theoretic and which
part remains a bridge assumption.
"""

from __future__ import annotations

from math import comb

import numpy as np


FANO_LINES = [
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
]

LADDER_PAIRS = {
    "alpha1": (5, 4),
    "alpha2": (3, 1),
    "alpha3": (6, 2),
}


def fano_lines_through(point: int) -> list[tuple[int, int, int]]:
    return [line for line in FANO_LINES if point in line]


def fock_grade_counts(n_ladders: int = 3) -> dict[int, int]:
    return {grade: comb(n_ladders, grade) for grade in range(n_ladders + 1)}


def sphere_volume(dim: int) -> float:
    if dim != 6:
        raise ValueError("Only S6 is needed in this diagnostic")
    return 16.0 * np.pi**3 / 15.0


def print_fock_derivation() -> None:
    print("SECTOR PROJECTORS FROM C tensor O LADDER GRADES")
    print("=" * 78)
    print("Chosen idempotent/vacuum: omega = (1 + i e7) / 2")
    print("This choice fixes e7 and leaves an SU(3) color stabilizer.")
    print()
    print("Fano lines through e7:")
    for line in fano_lines_through(7):
        print(f"  {line}")
    print("count = 3 color/stabilizer channels")
    print()
    print("Witt ladder pairs used in particle_states.py:")
    for name, pair in LADDER_PAIRS.items():
        print(f"  {name:<6} = 1/2(e{pair[0]} + i e{pair[1]})")
    print()
    print("Fock grade dimensions C(3,k):")
    counts = fock_grade_counts()
    for grade, count in counts.items():
        print(f"  grade {grade}: {count}")
    print(f"  total:   {sum(counts.values())}")
    print()
    print("Bridge multiplicity map now supported by this representation:")
    print("  up     -> grade-0 singlet rank 1")
    print("  down   -> grade-1 color triplet rank 3")
    print("  lepton -> full Fock trace rank 8, still an extra Yukawa-trace assumption")
    print()


def print_lepton_pi_gap() -> None:
    print("LEPTON 1/pi GAP")
    print("=" * 78)
    volume_s6 = sphere_volume(6)
    print(f"Vol(S6) = 16*pi^3/15 = {volume_s6:.6f}")
    print(f"1/Vol(S6) = {1.0 / volume_s6:.6f}")
    print(f"1/pi      = {1.0 / np.pi:.6f}")
    print()
    print("A flat geodesic-angle density on [0, pi] has density 1/pi, but that is a")
    print("one-dimensional measure assumption. The uniform S6 measure or volume")
    print("normalization does not by itself produce 1/pi.")
    print()
    print("Conclusion: the lepton shape factor 1/(4*pi) remains open until the CHO")
    print("Yukawa/coset measure is derived and shown to reduce to that angle density.")


def main() -> None:
    print_fock_derivation()
    print_lepton_pi_gap()


if __name__ == "__main__":
    main()
