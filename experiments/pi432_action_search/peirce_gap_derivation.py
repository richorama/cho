"""Peirce-grade gap derivation for the WZ/Jordan entropy candidate.

This probe attacks two assumptions left open by
`candidate_wz_jordan_entropy_action.py`:

1. Why use the frame generator N = diag(0,1,2)?
2. Why set Delta_Phi = -1/2 log(Phi)?

Conditional derivation:

* J3(O) has rank 3, so a primitive Peirce/frame grading has three levels.
* Primitive grading means the levels are consecutive integers, up to affine
  rescaling and shift. With the minimum shifted to 0, rank 3 gives (0,1,2).
* If the WZ/Jordan action fixes the endpoint weight ratio highest/lowest to
  Phi = pi/432, then exp(-Delta * 2) = Phi, hence Delta = -1/2 log(Phi).

This removes the arbitrariness of N and Delta inside the entropy candidate, but
it still does NOT derive the endpoint flux Phi or the entropy action itself.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/peirce_gap_derivation.py
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from math import exp, gcd, log, pi, sqrt


RANK_J3O = 3
PHI = pi / 432.0


@dataclass(frozen=True)
class GradeTriple:
    grades: tuple[int, int, int]

    @property
    def shifted(self) -> tuple[int, int, int]:
        lo = min(self.grades)
        return tuple(g - lo for g in self.grades)

    @property
    def span(self) -> int:
        values = self.shifted
        return max(values) - min(values)

    @property
    def primitive(self) -> bool:
        values = self.shifted
        diffs = [abs(a - b) for i, a in enumerate(values) for b in values[i + 1:] if a != b]
        return bool(diffs) and reduce(gcd, diffs) == 1

    @property
    def consecutive(self) -> bool:
        values = sorted(self.shifted)
        return values == list(range(len(values)))


def primitive_rank_gradings(rank: int, max_grade: int) -> list[GradeTriple]:
    """Enumerate shifted primitive rank gradings up to a small search bound."""
    triples = []
    for a in range(max_grade + 1):
        for b in range(a + 1, max_grade + 1):
            for c in range(b + 1, max_grade + 1):
                triple = GradeTriple((a, b, c))
                if len(set(triple.shifted)) == rank and triple.primitive:
                    triples.append(triple)
    return triples


def canonical_peirce_grading(rank: int) -> GradeTriple:
    return GradeTriple(tuple(range(rank)))


def delta_from_endpoint_flux(phi: float, grading: GradeTriple) -> float:
    return -log(phi) / grading.span


def weights_from_delta(delta: float, grading: GradeTriple) -> tuple[float, ...]:
    return tuple(exp(-delta * grade) for grade in grading.shifted)


def main() -> bool:
    canonical = canonical_peirce_grading(RANK_J3O)
    delta = delta_from_endpoint_flux(PHI, canonical)
    weights = weights_from_delta(delta, canonical)
    target = (1.0, sqrt(PHI), PHI)

    print("=" * 78)
    print("PEIRCE-GRADE GAP DERIVATION")
    print("=" * 78)

    print("\n[A] Rank-3 primitive Peirce grading")
    print(f"  rank J3(O)                    : {RANK_J3O}")
    print(f"  canonical primitive grading    : {canonical.shifted}")
    print(f"  span                           : {canonical.span}")
    print(f"  primitive                      : {canonical.primitive}")
    print(f"  consecutive                    : {canonical.consecutive}")

    print("\n[B] Endpoint-flux gap law")
    print(f"  endpoint ratio fixed by Phi    : {PHI:.15f}")
    print("  exp(-Delta * span) = Phi")
    print(f"  Delta = -log(Phi)/2            : {delta:.15f}")

    print("\n[C] Output weights")
    print(f"  exp(-Delta * grades)           : {weights}")
    print(f"  target (1, sqrt(Phi), Phi)     : {target}")
    print(f"  max residual                   : {max(abs(a - b) for a, b in zip(weights, target)):.3e}")

    print("\n[D] Nearby alternatives")
    alternatives = primitive_rank_gradings(rank=RANK_J3O, max_grade=5)
    for triple in alternatives:
        alt_delta = delta_from_endpoint_flux(PHI, triple)
        alt_weights = weights_from_delta(alt_delta, triple)
        flag = "canonical" if triple.shifted == canonical.shifted else "nonconsecutive"
        print(f"  {triple.shifted}: {flag}, Delta={alt_delta:.6f}, weights={alt_weights}")

    print("\n[E] What is still open")
    print("  This derives N=(0,1,2) and Delta=-1/2 log(Phi) from rank-3 primitive")
    print("  Peirce grading plus endpoint flux. It does NOT yet derive Phi itself")
    print("  as the action coefficient, nor the entropy functional Tr(rho log rho).")

    print("\n[V] Sandbox verdict")
    print("  Peirce-grade generator : CONDITIONALLY DERIVED")
    print("  modular gap law        : CONDITIONALLY DERIVED")
    print("  final pi/432 action    : NOT FOUND")
    print("=" * 78)

    assert canonical.shifted == (0, 1, 2)
    assert canonical.primitive and canonical.consecutive
    assert abs(delta - (-0.5 * log(PHI))) < 1e-15
    assert max(abs(a - b) for a, b in zip(weights, target)) < 1e-14
    assert any(not triple.consecutive for triple in alternatives)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
