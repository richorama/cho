"""
N5 hardening — sin^2(theta23) = 4/7 is a Fano-plane INVARIANT, not a cherry-pick.
================================================================================

The pivot (ledger N5, theta23_octant_prediction.py, epsilon_mixing_coefficients.py)
----------------------------------------------------------------------------------
The sharpest falsifiable CHO bet is the atmospheric octant

        sin^2(theta23) = (Fano lines avoiding the vacuum) / (all Fano lines) = 4/7,

the only eps0-INDEPENDENT exact mixing rational the framework emits.  Until now
the integers 3 (through the vacuum point e7) and 4 (avoiding it) were simply READ
OFF the e7 row of the octonion incidence table -- so a referee could ask the only
question that matters for a value-claim:

        "Did you pick e7 (and a multiplication convention) to MANUFACTURE the 4?"

This module answers NO, by proof.  It hardens the VALUE-half of the N5 bridge from
"read off one row" to "a forced invariant of the finite projective plane", using
exact integer / Fraction arithmetic and the automorphism group already enumerated
in spurion_bridge.  Three independent senses of canonicity:

  [A] The 7 octonion multiplication triples are exactly PG(2,2) = the Fano plane =
      the unique Steiner system S(2,3,7): 7 points, 7 lines, every line 3 points,
      every point on 3 lines, every pair of points on a UNIQUE common line, every
      pair of lines meeting in a UNIQUE point.  So "the octonion Fano plane" is a
      theorem about the multiplication triples, not a drawing convention.

  [B] VACUUM-INDEPENDENCE.  In PG(2,2) every point lies on exactly 3 lines (order
      n=2  =>  n+1 = 3 lines per point), hence avoids exactly 7 - 3 = 4.  We verify
      this for ALL 7 points: the split is (3 through, 4 avoiding) for EVERY choice
      of vacuum point, so (avoiding/total) = 4/7 no matter which imaginary unit the
      vacuum omega=(1+i e_k)/2 happens to single out.  The 4 is NOT a property of e7.

  [C] CONVENTION-INDEPENDENCE.  Aut(Fano) = PGL(3,2) = PSL(2,7), order 168 = 2^3*3*7,
      acts TRANSITIVELY on the 7 points (the orbit of any point is all 7).  So any
      relabelling of the imaginary units that preserves the multiplication-triple
      structure carries one vacuum choice to any other while preserving the 3-through
      / 4-avoiding count.  No octonion labelling convention can change 4/7.

  [D] The octant and the falsifier.  The same partition offers exactly two octant
      candidates, complementary about maximal mixing: 4/7 (UPPER, avoiding/total,
      theta23 = 49.1 deg) and its mirror 3/7 (LOWER, through/total, 40.9 deg), with
      4/7 + 3/7 = 1 exactly.  CHO takes the BROKEN (avoiding) directions -> 4/7.
      A stable lower-octant resolution near 3/7 kills the octant choice.

PROVED here (exact, machine-checked):
  - the octonion triples are PG(2,2) / S(2,3,7);
  - the (3,4) split, hence 4/7, holds at EVERY point (vacuum-independent);
  - Aut = PSL(2,7) of order 168 is point-transitive (convention-independent);
  - the two octant candidates are exactly complementary (4/7 + 3/7 = 1).

NOT proved here (the surviving open obligation):
  - the PHYSICAL map "atmospheric mixing PROBABILITY = avoiding-lines / total-lines".
    That identification is the N5 bridge itself and stays an open CHO-action problem;
    this module only shows that GIVEN the map, the value is forced and canonical.

This is a DIAGNOSTIC hardening: it promotes no ledger row and moves no Bayes credit.
The frozen registry (Q2, Theta23_octant) stays authoritative.

stdlib + spurion_bridge only (Fraction for exact arithmetic).  No scipy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/theta23_fano_invariance.py
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import combinations

import prediction_registry
import theta23_octant_prediction
from spurion_bridge import FANO_LINES, VACUUM_POINT, fano_automorphisms


# --------------------------------------------------------------------------
# Shared facts
# --------------------------------------------------------------------------

POINTS = tuple(range(1, 8))                       # imaginary units e1..e7
TOTAL_LINES = len(FANO_LINES)                      # 7
PSL27_ORDER = 168                                  # |PGL(3,2)| = |PSL(2,7)| = 2^3*3*7
SIN2_UPPER = Fraction(4, 7)                        # avoiding / total  (upper octant)
SIN2_LOWER = Fraction(3, 7)                        # through  / total  (lower mirror)


# --------------------------------------------------------------------------
# [A] The octonion triples are PG(2,2) = S(2,3,7).
# --------------------------------------------------------------------------


def projective_plane_certificate() -> dict:
    """Certify that the 7 octonion multiplication triples form the Fano plane.

    Checks the defining axioms of PG(2,2) / the Steiner triple system S(2,3,7):
    point/line counts, line size 3, point degree 3, a unique line through any two
    points, and a unique intersection point of any two lines.
    """
    lines = [frozenset(ln) for ln in FANO_LINES]
    points = sorted({p for ln in lines for p in ln})

    line_sizes = {len(ln) for ln in lines}
    point_degree = {p: sum(1 for ln in lines if p in ln) for p in points}

    # Every pair of points lies on exactly one common line (S(2,3,7)).
    pair_counts = {
        pair: sum(1 for ln in lines if set(pair) <= ln)
        for pair in combinations(points, 2)
    }
    # Every pair of lines meets in exactly one point (projective dual).
    meet_counts = [len(a & b) for a, b in combinations(lines, 2)]

    return {
        "n_points": len(points),
        "n_lines": len(lines),
        "points_are_1_to_7": points == list(POINTS),
        "all_lines_size_3": line_sizes == {3},
        "every_point_degree_3": set(point_degree.values()) == {3},
        "unique_line_through_each_pair": set(pair_counts.values()) == {1},
        "lines_meet_in_one_point": set(meet_counts) == {1},
        "point_degree": point_degree,
    }


# --------------------------------------------------------------------------
# [B] Vacuum-independence: the (3,4) split holds at EVERY point.
# --------------------------------------------------------------------------


def split_at_point(point: int) -> tuple[int, int]:
    """(#lines through `point`, #lines avoiding `point`)."""
    through = sum(1 for ln in FANO_LINES if point in ln)
    return through, TOTAL_LINES - through


def vacuum_independence() -> dict:
    """Show (through, avoiding) = (3, 4) and ratio 4/7 for ALL 7 vacuum choices."""
    table = {p: split_at_point(p) for p in POINTS}
    ratios = {p: Fraction(avoid, TOTAL_LINES) for p, (_, avoid) in table.items()}
    return {
        "table": table,                                   # p -> (through, avoiding)
        "ratios": ratios,                                 # p -> avoiding/total
        "all_splits_3_4": set(table.values()) == {(3, 4)},
        "all_ratios_4_7": set(ratios.values()) == {SIN2_UPPER},
        "default_vacuum": VACUUM_POINT,                   # e7 is just the convention
    }


# --------------------------------------------------------------------------
# [C] Convention-independence: Aut = PSL(2,7) is point-transitive.
# --------------------------------------------------------------------------


def convention_independence() -> dict:
    """Aut(Fano) order 168, transitive on points, preserving the degree-3 split."""
    autos = fano_automorphisms()
    order = len(autos)

    # Orbit of the (conventional) vacuum point under the full group.
    orbit = {mapping[VACUUM_POINT] for mapping in autos}

    # Every automorphism carries "lines through p" to "lines through image(p)",
    # so the 3-through count is group-equivariant (sampled over all points/maps).
    degree_preserved = True
    for mapping in autos:
        for p in POINTS:
            through_p = split_at_point(p)[0]
            through_image = split_at_point(mapping[p])[0]
            if through_p != through_image:
                degree_preserved = False
                break
        if not degree_preserved:
            break

    return {
        "order": order,
        "order_is_168": order == PSL27_ORDER,
        "orbit_of_vacuum": orbit,
        "point_transitive": orbit == set(POINTS),
        "degree_preserved_under_group": degree_preserved,
    }


# --------------------------------------------------------------------------
# [D] Octant candidates and the falsifier.
# --------------------------------------------------------------------------


def octant_candidates() -> dict:
    """The two complementary octant candidates from the same Fano partition."""
    upper_deg = math.degrees(math.asin(math.sqrt(float(SIN2_UPPER))))
    lower_deg = math.degrees(math.asin(math.sqrt(float(SIN2_LOWER))))
    return {
        "upper": (SIN2_UPPER, upper_deg),                 # avoiding/total -> CHO pick
        "lower": (SIN2_LOWER, lower_deg),                 # through/total  -> mirror
        "complementary": SIN2_UPPER + SIN2_LOWER == 1,    # 4/7 + 3/7 = 1
        "gap_from_maximal": SIN2_UPPER - Fraction(1, 2),  # 1/14
        "gap_from_mirror": SIN2_UPPER - SIN2_LOWER,       # 1/7
    }


def registry_crosscheck() -> dict:
    """The frozen Q2 registry payload must still read exactly 4/7."""
    payload = prediction_registry.theta23_octant_values()
    registry_sin2 = payload["sin2_theta23"]
    return {
        "registry_sin2_theta23": registry_sin2,
        "registry_octant": payload["octant"],
        "matches_4_7": abs(registry_sin2 - float(SIN2_UPPER)) < 1e-12,
        "octant_upper": payload["octant"] == "upper",
    }


def prediction_module_crosscheck() -> dict:
    """Bind the bare Fano literals in the forward-test module to the PROVED split.

    `theta23_octant_prediction.py` re-states the counts (3, 4, 7) as standalone
    integer constants.  Anchor them to the invariant proved here so they cannot
    drift silently away from the geometry: if anyone edits those literals, this
    module's tripwire fires.  The proof becomes the single authority for 3/4/7.
    """
    through, avoiding = split_at_point(VACUUM_POINT)
    return {
        "total_matches": theta23_octant_prediction.FANO_TOTAL_LINES == TOTAL_LINES,
        "through_matches": theta23_octant_prediction.FANO_LINES_THROUGH_VACUUM == through,
        "avoiding_matches": theta23_octant_prediction.FANO_LINES_AVOIDING_VACUUM == avoiding,
        "ratio_matches": Fraction(
            theta23_octant_prediction.FANO_LINES_AVOIDING_VACUUM,
            theta23_octant_prediction.FANO_TOTAL_LINES,
        ) == SIN2_UPPER,
    }


# --------------------------------------------------------------------------
# Reporting + tripwires
# --------------------------------------------------------------------------


def main() -> bool:
    print("=" * 78)
    print("  N5 HARDENING — sin^2(theta23) = 4/7 IS A FANO-PLANE INVARIANT")
    print("=" * 78)
    print("  Goal: show the integers 3 (through vacuum) and 4 (avoiding) are FORCED")
    print("  by the projective geometry, not manufactured by the choice of e7 or of")
    print("  a multiplication convention. Value-half of the N5 bridge only; the")
    print("  physical atmospheric-angle map stays the open obligation.")
    print()

    # [A] PG(2,2) certificate -------------------------------------------------
    cert = projective_plane_certificate()
    print("-" * 78)
    print("  [A] THE OCTONION TRIPLES ARE PG(2,2) = S(2,3,7)")
    print("-" * 78)
    print(f"      points (imaginary units e1..e7) : {cert['n_points']}")
    print(f"      lines  (multiplication triples) : {cert['n_lines']}")
    print(f"      every line has 3 points         : {cert['all_lines_size_3']}")
    print(f"      every point lies on 3 lines     : {cert['every_point_degree_3']}")
    print(f"      unique line through any 2 points: {cert['unique_line_through_each_pair']}")
    print(f"      any 2 lines meet in 1 point     : {cert['lines_meet_in_one_point']}")
    pg_ok = (
        cert["n_points"] == 7 and cert["n_lines"] == 7
        and cert["points_are_1_to_7"] and cert["all_lines_size_3"]
        and cert["every_point_degree_3"] and cert["unique_line_through_each_pair"]
        and cert["lines_meet_in_one_point"]
    )
    print(f"      [{'PASS' if pg_ok else 'FAIL'}] the triples ARE the Fano plane (a theorem, not a picture)")
    print()

    # [B] Vacuum-independence -------------------------------------------------
    vac = vacuum_independence()
    print("-" * 78)
    print("  [B] VACUUM-INDEPENDENCE — the (3,4) split holds at EVERY point")
    print("-" * 78)
    print("      vacuum point p :  (through, avoiding)  ->  avoiding/total")
    for p in POINTS:
        through, avoid = vac["table"][p]
        mark = "  <- e7 (the conventional vacuum)" if p == VACUUM_POINT else ""
        print(f"        e{p}          :     ({through}, {avoid})        ->     "
              f"{vac['ratios'][p]}{mark}")
    print(f"      [{'PASS' if vac['all_ratios_4_7'] else 'FAIL'}] avoiding/total = 4/7 for ALL 7 vacuum choices "
          f"(the 4 is not a property of e7)")
    print()

    # [C] Convention-independence --------------------------------------------
    conv = convention_independence()
    print("-" * 78)
    print("  [C] CONVENTION-INDEPENDENCE — Aut(Fano) = PSL(2,7) is point-transitive")
    print("-" * 78)
    print(f"      |Aut(Fano)| = |PGL(3,2)| = |PSL(2,7)| : {conv['order']}  (= 2^3*3*7)")
    print(f"      orbit of the vacuum point under Aut   : {sorted(conv['orbit_of_vacuum'])}")
    print(f"      transitive on all 7 points            : {conv['point_transitive']}")
    print(f"      3-through count preserved by the group: {conv['degree_preserved_under_group']}")
    print(f"      [{'PASS' if conv['order_is_168'] and conv['point_transitive'] else 'FAIL'}] "
          f"every vacuum choice is equivalent => no labelling changes 4/7")
    print()

    # [D] Octant + falsifier --------------------------------------------------
    oct_ = octant_candidates()
    reg = registry_crosscheck()
    pred = prediction_module_crosscheck()
    print("-" * 78)
    print("  [D] THE TWO OCTANT CANDIDATES AND THE FALSIFIER")
    print("-" * 78)
    up_f, up_deg = oct_["upper"]
    lo_f, lo_deg = oct_["lower"]
    print(f"      UPPER (CHO pick, avoiding/total): sin^2 = {up_f} = {float(up_f):.6f}  "
          f"-> theta23 = {up_deg:.2f} deg")
    print(f"      LOWER (mirror,  through/total)  : sin^2 = {lo_f} = {float(lo_f):.6f}  "
          f"-> theta23 = {lo_deg:.2f} deg")
    print(f"      complementary 4/7 + 3/7 = 1     : {oct_['complementary']}  "
          f"(angles symmetric about 45 deg)")
    print(f"      gap from maximal (1/2)          : {oct_['gap_from_maximal']} = "
          f"{float(oct_['gap_from_maximal']):.5f}")
    print(f"      gap from the mirror octant      : {oct_['gap_from_mirror']} = "
          f"{float(oct_['gap_from_mirror']):.5f}")
    print(f"      frozen registry (Q2) still reads: sin^2 = {reg['registry_sin2_theta23']:.6f} "
          f"({reg['registry_octant']}) -> matches 4/7: {reg['matches_4_7']}")
    print(f"      forward-test literals 3/4/7     : guarded by this proof -> "
          f"through:{pred['through_matches']} avoiding:{pred['avoiding_matches']} "
          f"total:{pred['total_matches']} ratio:{pred['ratio_matches']}")
    print()
    print("      Illustrative reach (printed, not asserted): a DUNE/Hyper-K-class")
    print("      measurement at sigma ~ 0.01 on sin^2(theta23) separates 4/7 from")
    print("      maximal by ~7 sigma and from the 3/7 mirror by ~14 sigma.")
    print()

    # [Verdict] ---------------------------------------------------------------
    print("-" * 78)
    print("  VERDICT")
    print("-" * 78)
    print("  PROVED (exact): the octonion triples are PG(2,2)=S(2,3,7); the (3,4)")
    print("  split (hence 4/7) holds at every point (vacuum-independent); Aut=PSL(2,7)")
    print("  of order 168 is point-transitive (convention-independent); the two octant")
    print("  candidates 4/7 and 3/7 are exactly complementary.")
    print("  NOT proved: that the physical atmospheric mixing probability equals the")
    print("  avoiding/total ratio. That map is the N5 bridge and stays OPEN; this")
    print("  module hardens only the VALUE it would deliver. No row promoted; no")
    print("  Bayes credit moved.")
    print("=" * 78)

    # --- tripwires (fire even when run via audit.py, which ignores returns) ---
    assert pg_ok, "octonion triples failed the PG(2,2)/S(2,3,7) certificate"
    assert cert["point_degree"] == {p: 3 for p in POINTS}, "a point is not on exactly 3 lines"
    assert vac["all_splits_3_4"], "some vacuum point did not split 3-through/4-avoiding"
    assert vac["all_ratios_4_7"], "avoiding/total is not 4/7 at every point"
    assert set(vac["ratios"].values()) == {SIN2_UPPER}, "ratio drifted off 4/7"
    assert conv["order_is_168"], "Aut(Fano) is not order 168 (PSL(2,7))"
    assert conv["point_transitive"], "Aut(Fano) is not transitive on points"
    assert conv["degree_preserved_under_group"], "group did not preserve the 3-through count"
    assert oct_["complementary"], "4/7 and 3/7 are not complementary"
    assert oct_["gap_from_maximal"] == Fraction(1, 14), "gap from maximal is not 1/14"
    assert oct_["gap_from_mirror"] == Fraction(1, 7), "gap from mirror is not 1/7"
    assert SIN2_UPPER > Fraction(1, 2) > SIN2_LOWER, "octant ordering broke"
    assert reg["matches_4_7"] and reg["octant_upper"], "frozen registry no longer reads 4/7 upper"
    assert pred["total_matches"], "theta23_octant_prediction.FANO_TOTAL_LINES drifted off the proven 7"
    assert pred["through_matches"], "theta23_octant_prediction.FANO_LINES_THROUGH_VACUUM drifted off the proven 3"
    assert pred["avoiding_matches"], "theta23_octant_prediction.FANO_LINES_AVOIDING_VACUUM drifted off the proven 4"
    assert pred["ratio_matches"], "forward-test avoiding/total no longer equals 4/7"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
