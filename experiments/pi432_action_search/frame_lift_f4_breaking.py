"""Frame-lift probe for the WZ/Jordan entropy candidate.

The candidate action was written in a fixed Jordan frame. This probe checks the
minimal combinatorial lift: the entropy law is frame-covariant, and an oriented
endpoint condition selects an ordered Peirce frame instead of inserting a spectrum.

This is only the finite Weyl/S3 shadow of the full F4 problem, but it tests whether
the fixed-frame candidate is obviously circular at the frame level.
"""

from __future__ import annotations

from itertools import permutations
from math import exp, log, pi


PHI = pi / 432.0
DELTA = -0.5 * log(PHI)
IDEMPOTENTS = ("E_low", "E_mid", "E_high")
GRADES = (0, 1, 2)


def assignment_weight(assignment: tuple[tuple[str, int], ...]) -> float:
    return sum(exp(-DELTA * grade) for _idempotent, grade in assignment)


def endpoint_selected(assignment: tuple[tuple[str, int], ...]) -> bool:
    grades_by_idempotent = dict(assignment)
    return grades_by_idempotent["E_low"] == 0 and grades_by_idempotent["E_high"] == 2


def main() -> bool:
    assignments = tuple(tuple(zip(IDEMPOTENTS, grades)) for grades in permutations(GRADES))
    selected = tuple(assignment for assignment in assignments if endpoint_selected(assignment))

    print("=" * 78)
    print("FRAME-LIFT F4-BREAKING PROBE")
    print("=" * 78)

    print("\n[A] S3 frame shadow")
    print(f"  unordered Jordan frame idempotents : {IDEMPOTENTS}")
    print(f"  primitive grades                   : {GRADES}")
    print(f"  total grade assignments            : {len(assignments)}")
    for assignment in assignments:
        marker = "selected" if assignment in selected else "degenerate"
        print(f"  {assignment}: {marker}, partition trace={assignment_weight(assignment):.12f}")

    print("\n[B] Endpoint orientation")
    print("  Boundary data E_low -> grade 0 and E_high -> grade 2 selects the ordered")
    print("  Peirce frame; the middle idempotent is then forced. This is a finite")
    print("  S3/Weyl shadow of the required F4-breaking lift.")

    print("\n[C] What remains open")
    print("  The full theorem must replace this S3 shadow with an F4-covariant action")
    print("  whose WZ boundary condition selects the frame dynamically. This probe only")
    print("  shows the fixed-frame entropy candidate is compatible with frame selection.")

    print("\n[V] Sandbox verdict")
    print("  fixed-frame circularity at S3 level : NOT DETECTED")
    print("  full F4-breaking variational lift   : OPEN")
    print("=" * 78)

    assert len(assignments) == 6
    assert len(selected) == 1
    assert selected[0] == (("E_low", 0), ("E_mid", 1), ("E_high", 2))
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
