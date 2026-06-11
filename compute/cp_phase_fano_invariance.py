"""
C4 hardening — the CKM phase delta = arccos(1/3) is a Fano-incidence INVARIANT.
================================================================================

The pivot (ledger C3/C4, CHO_OPERATOR.md, flavour_derivation.py)
---------------------------------------------------------------
The framework's weak-CP input is a single geometric angle, stated in
CHO_OPERATOR.md as

        cos(delta) = dim(shared imaginary line) / dim(Fano line) = 1/3,
        delta_Fano = arccos(1/3)  (~= 70.5288 deg),

read as the angle between two "adjacent quaternionic subalgebras" -- i.e. two
Fano lines that share one imaginary unit.  This feeds the CKM unitary scaffold
(C1-C3) and the still-open Jarlskog phase-placement obligation (C4).

Until now the 1/3 was WRITTEN DOWN (strong_cp.py line 212, operator_gap_audit.py,
summary_table.py) rather than COMPUTED, so a referee could ask the value question:

        "Did you pick two particular lines (and a multiplication convention) to
         MANUFACTURE the 1/3 -- or is arccos(1/3) forced by the geometry?"

This module answers: the angle is FORCED, by proof, in exact arithmetic.  It
hardens the VALUE-source of C3/C4 from "written down" to "a single-orbit
invariant of the finite projective plane", reusing the automorphism group
already enumerated in spurion_bridge.  It does NOT close the physical bridge
(which monotone function of the angle is the physical phase, and which two lines
are the up/down channels) -- that stays C4, open.

  [A] No parallel lines.  In PG(2,2) = S(2,3,7) every pair of DISTINCT lines
      meets in exactly one point (projective duality of "two points determine a
      unique line").  So there is only one kind of line pair: every pair is
      "adjacent".  We verify all 21 unordered pairs share exactly 1 of 3 points.

  [B] The angle is 1/3, exactly, for EVERY pair.  Write each line as its 0/1
      indicator vector in 7-dim point space.  Two distinct lines have inner
      product |L cap M| = 1 and squared norm |L| = 3, so the incidence cosine is

          <L,M> / (||L|| ||M||) = 1 / (sqrt(3) sqrt(3)) = 1/3   (EXACT),

      which is literally the framework's "dim(shared)/dim(line)" formula.  We
      assert Fraction(1,3) for all 21 pairs.  Hence delta = arccos(1/3) is the
      unique inter-line incidence angle -- no pair gives anything else.

  [C] CONVENTION-INDEPENDENCE.  Aut(Fano) = PGL(3,2) = PSL(2,7), order 168, acts
      on lines by point-permutation (an orthogonal map), so it preserves every
      indicator inner product and norm -> preserves the cosine.  Moreover the 42
      ORDERED pairs of distinct lines form a SINGLE orbit (PSL(2,7) is 2-transitive
      on the 7 lines, dual to 2-transitive on the 7 points).  So 1/3 is a
      single-orbit class invariant: there is one inter-line angle, group-forced.
      No relabelling of the imaginary units can change arccos(1/3).

  [D] WHICH "angle"?  The honest reading distinction.  "Angle between two Fano
      lines" has (at least) two natural meanings, and only one gives 1/3:
        (a) INCIDENCE cosine of the two indicator vectors -> 1/3   <-- the claim.
        (b) PRINCIPAL ANGLES between the two 3-dim imaginary subspaces
            span{e_i,e_j,e_k} in Im(O): they share one basis vector and are
            otherwise orthonormal, so the principal cosines are {1, 0, 0}
            (angles {0,90,90} deg) -- NOT a single arccos(1/3).
      So the physics claim implicitly commits to reading (a).  This module proves
      (a) is the canonical, group-invariant reading; (b) is computed alongside to
      show the two readings genuinely differ.

  [E] The open physical bridge (C4).  GIVEN that delta is THIS angle, the value
      is forced and canonical.  NOT proved here: that the CKM phase equals it;
      WHICH monotone function does (the repo uses arccos(1/3) for CKM and
      pi+arccos(1/3) for PMNS as a scaffold convention -- FLAVOUR_DERIVATION.md);
      and the channel assignment (which two lines are up vs down).  The Jarlskog
      phase-placement J = 3.01e-5 is the explicit open C4 operator obligation.

PROVED here (exact, machine-checked):
  - every pair of distinct octonion-triple lines meets in exactly one point;
  - the incidence cosine is exactly 1/3 for ALL 21 unordered pairs;
  - Aut = PSL(2,7) of order 168 preserves the cosine and is transitive on the 42
    ordered distinct-line pairs (single orbit) -> arccos(1/3) is forced/canonical;
  - the subspace principal-angle reading gives {1,0,0}, so the two angle readings
    differ and the claim commits to the incidence reading.

NOT proved here (the surviving open obligation = C4):
  - the PHYSICAL map "CKM CP phase = (a monotone function of) this incidence angle";
  - which function (arccos(1/3) vs pi+arccos(1/3) -- a documented scaffold choice);
  - the channel assignment of lines to up/down sectors;
  - the Jarlskog target J = 3.01e-5 from a single charged diagonalization.

This is a DIAGNOSTIC hardening: it promotes no ledger row and moves no Bayes
credit.  The frozen registry stays authoritative (it holds no CP-phase row).

stdlib + spurion_bridge only (Fraction for exact arithmetic).  No numpy, no scipy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/cp_phase_fano_invariance.py
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import combinations

from spurion_bridge import FANO_LINES, VACUUM_POINT, fano_automorphisms, fano_line_sets


# --------------------------------------------------------------------------
# Shared facts
# --------------------------------------------------------------------------

POINTS = tuple(range(1, 8))                        # imaginary units e1..e7
LINE_SIZE = 3                                      # points per Fano line
TOTAL_LINES = len(FANO_LINES)                      # 7
N_ORDERED_PAIRS = TOTAL_LINES * (TOTAL_LINES - 1)  # 42 ordered distinct-line pairs
PSL27_ORDER = 168                                  # |PGL(3,2)| = |PSL(2,7)| = 2^3*3*7
COS_DELTA = Fraction(1, 3)                          # the claimed Fano incidence cosine


# --------------------------------------------------------------------------
# [A] No parallel lines: every two distinct lines meet in exactly one point.
# --------------------------------------------------------------------------


def pairwise_intersection_certificate() -> dict:
    """Certify that every pair of distinct lines shares exactly one point.

    In a projective plane PG(2,2) there are no parallel lines: two distinct
    lines meet in a unique point (dual to "two points lie on a unique line").
    This is what makes every line pair "adjacent" -- a single geometric type.
    """
    lines = [frozenset(ln) for ln in FANO_LINES]
    sizes = {len(ln) for ln in lines}
    shared = [len(a & b) for a, b in combinations(lines, 2)]
    return {
        "n_lines": len(lines),
        "all_lines_size_3": sizes == {LINE_SIZE},
        "n_unordered_pairs": len(shared),
        "every_pair_shares_exactly_one": set(shared) == {1},
        "shared_counts": shared,
    }


# --------------------------------------------------------------------------
# [B] The incidence angle is exactly arccos(1/3) for every pair.
# --------------------------------------------------------------------------


def line_indicator(line: frozenset[int]) -> tuple[int, ...]:
    """0/1 indicator vector of a Fano line in 7-dim point space."""
    return tuple(1 if p in line else 0 for p in POINTS)


def incidence_cosine(a: frozenset[int], b: frozenset[int]) -> Fraction:
    """Exact cosine of the angle between two line indicator vectors.

    <a,b> = |a cap b|;  ||a||^2 = ||b||^2 = 3.  Both norms are sqrt(3), so their
    product is exactly 3 and the cosine is the rational |a cap b| / 3.  This is
    the framework's cos(delta) = dim(shared)/dim(line).
    """
    dot = len(a & b)
    norm_sq_a = len(a)
    norm_sq_b = len(b)
    assert norm_sq_a == LINE_SIZE and norm_sq_b == LINE_SIZE
    # ||a|| ||b|| = sqrt(3)*sqrt(3) = 3 exactly, so the cosine is rational.
    return Fraction(dot, LINE_SIZE)


def all_incidence_cosines() -> list[Fraction]:
    lines = [frozenset(ln) for ln in FANO_LINES]
    return [incidence_cosine(a, b) for a, b in combinations(lines, 2)]


# --------------------------------------------------------------------------
# [C] Convention-independence: single automorphism orbit on ordered pairs.
# --------------------------------------------------------------------------


def image_line(line: frozenset[int], perm: dict[int, int]) -> frozenset[int]:
    """Image of a line under a point permutation (an automorphism)."""
    return frozenset(perm[p] for p in line)


def cosine_is_automorphism_invariant() -> bool:
    """Every automorphism preserves the incidence cosine of every line pair.

    Point permutations act on indicator vectors as orthogonal (permutation)
    matrices, so they preserve all inner products and norms.  We check it
    directly for all 21 pairs under all 168 automorphisms.
    """
    lines = [frozenset(ln) for ln in FANO_LINES]
    autos = fano_automorphisms()
    for perm in autos:
        for a, b in combinations(lines, 2):
            before = incidence_cosine(a, b)
            after = incidence_cosine(image_line(a, perm), image_line(b, perm))
            if before != after:
                return False
    return True


def ordered_pair_orbit() -> dict:
    """Orbit of one ordered distinct-line pair under the 168 automorphisms.

    PSL(2,7) is 2-transitive on the 7 lines, so all 42 ordered pairs of distinct
    lines form a single orbit.  A single orbit means there is exactly ONE
    inter-line angle, group-forced: arccos(1/3).
    """
    lines = fano_line_sets()
    index = {ln: i for i, ln in enumerate(lines)}
    autos = fano_automorphisms()

    seed = (0, 1)  # ordered pair of distinct line indices
    orbit = set()
    for perm in autos:
        ia = index[image_line(lines[seed[0]], perm)]
        ib = index[image_line(lines[seed[1]], perm)]
        orbit.add((ia, ib))

    return {
        "n_automorphisms": len(autos),
        "orbit_size": len(orbit),
        "n_ordered_pairs": N_ORDERED_PAIRS,
        "single_orbit": len(orbit) == N_ORDERED_PAIRS,
    }


# --------------------------------------------------------------------------
# [D] The honest reading distinction: incidence vs subspace principal angles.
# --------------------------------------------------------------------------


def subspace_principal_cosines(a: frozenset[int], b: frozenset[int]) -> tuple[int, ...]:
    """Principal-angle cosines between the two 3-dim COORDINATE subspaces.

    Each line spans a coordinate subspace span{e_i,e_j,e_k} in Im(O) = R^7.  For
    coordinate subspaces the principal angles are determined purely by index
    overlap: each shared basis vector contributes a principal cosine 1, each
    remaining (orthogonal) direction contributes 0.  No SVD needed -- exact.
    """
    shared = len(a & b)
    cosines = [1] * shared + [0] * (LINE_SIZE - shared)
    return tuple(sorted(cosines, reverse=True))


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def main() -> bool:
    ok = True
    delta_deg = math.degrees(math.acos(1.0 / 3.0))

    print("=" * 78)
    print("C4 HARDENING: delta = arccos(1/3) IS A FANO-INCIDENCE INVARIANT")
    print("=" * 78)
    print(f"FANO_LINES (octonion triples): {list(FANO_LINES)}")
    print(f"vacuum point e{VACUUM_POINT}; points e1..e7; {TOTAL_LINES} lines")
    print()

    # ---- [A] no parallel lines -------------------------------------------
    cert = pairwise_intersection_certificate()
    print("[A] No parallel lines (every distinct pair meets in one point)")
    print(f"    lines size 3 ............... {cert['all_lines_size_3']}")
    print(f"    unordered pairs ............ {cert['n_unordered_pairs']} (expect 21)")
    print(f"    each shares exactly 1 point  {cert['every_pair_shares_exactly_one']}")
    ok &= cert["all_lines_size_3"]
    ok &= cert["n_unordered_pairs"] == 21
    ok &= cert["every_pair_shares_exactly_one"]
    print()

    # ---- [B] the angle is 1/3, exactly, for every pair -------------------
    cosines = all_incidence_cosines()
    uniform = set(cosines) == {COS_DELTA}
    print("[B] Incidence cosine of every line pair (exact Fraction)")
    print(f"    cos(delta) = <L,M>/(||L|| ||M||) = |L cap M| / 3")
    print(f"    distinct values observed ... {sorted(set(cosines))}")
    print(f"    all equal 1/3 .............. {uniform}")
    print(f"    => delta = arccos(1/3) = {delta_deg:.4f} deg  (descriptive float)")
    ok &= uniform
    ok &= all(c == COS_DELTA for c in cosines)
    print()

    # ---- [C] convention-independence -------------------------------------
    inv = cosine_is_automorphism_invariant()
    orbit = ordered_pair_orbit()
    print("[C] Convention-independence (Aut = PSL(2,7), order 168)")
    print(f"    cosine invariant under all 168 autos  {inv}")
    print(f"    automorphisms .............. {orbit['n_automorphisms']} (expect 168)")
    print(f"    ordered distinct-line pairs  {orbit['n_ordered_pairs']} (expect 42)")
    print(f"    orbit of one pair size ..... {orbit['orbit_size']}")
    print(f"    single orbit (transitive) .. {orbit['single_orbit']}")
    ok &= inv
    ok &= orbit["n_automorphisms"] == PSL27_ORDER
    ok &= orbit["single_orbit"]
    print()

    # ---- [D] the honest reading distinction ------------------------------
    a, b = frozenset(FANO_LINES[0]), frozenset(FANO_LINES[1])
    principal = subspace_principal_cosines(a, b)
    incidence = incidence_cosine(a, b)
    readings_differ = set(principal) != {incidence}
    print("[D] Which 'angle'? Incidence cosine vs subspace principal angles")
    print(f"    sample lines {tuple(sorted(a))} and {tuple(sorted(b))}")
    print(f"    (a) incidence cosine ....... {incidence}  -> arccos(1/3)  [the claim]")
    print(f"    (b) subspace principal cos . {principal}  -> angles {{0,90,90}} deg")
    print(f"    the two readings differ .... {readings_differ}")
    ok &= principal == (1, 0, 0)
    ok &= readings_differ
    print()

    # ---- [E] the open physical bridge (C4) -------------------------------
    measured_delta_deg = 65.5  # PDG CKM CP phase ~ 1.144 rad (descriptive only)
    print("[E] Open physical bridge (ledger C4) -- NOT proved here")
    print("    PROVED above: arccos(1/3) is the forced, single-orbit incidence")
    print("    angle between any two adjacent Fano lines (quaternionic subalgebras).")
    print("    NOT proved:")
    print("      - that the CKM CP phase equals this angle;")
    print("      - which monotone function (arccos(1/3) for CKM vs pi+arccos(1/3)")
    print("        for PMNS -- a documented scaffold convention);")
    print("      - the up/down channel assignment of the two lines;")
    print("      - the Jarlskog target J = 3.01e-5 from one charged diagonalization.")
    print(f"    descriptive: arccos(1/3) = {delta_deg:.2f} deg vs measured CKM delta")
    print(f"    ~ {measured_delta_deg:.1f} deg (PDG ~1.14 rad) -> "
          f"~{100*(delta_deg-measured_delta_deg)/measured_delta_deg:.0f}% high; NOT asserted.")
    print()

    print("-" * 78)
    if ok:
        print("VERDICT: PROVED — arccos(1/3) is a single-orbit Fano-incidence invariant.")
        print("         The VALUE is forced; the PHYSICAL map to delta_CKM stays C4-open.")
        print("         DIAGNOSTIC: promotes no ledger row, moves no Bayes credit.")
    else:
        print("VERDICT: FAIL — an invariance tripwire did not hold (see above).")
    print("-" * 78)
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
