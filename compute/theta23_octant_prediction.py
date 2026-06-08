"""
Item 7 -- the single sharpest falsifiable claim: the theta23 octant.
====================================================================

Roadmap Item 7 asks the framework to STAKE one sharp, falsifiable claim on an
UNMEASURED quantity. Of everything CHO says, exactly one mixing prediction is

    (a) an EXACT rational, with no free parameter and no fitted prefactor;
    (b) INDEPENDENT of the open eps0^2 = pi/432 seam (the Bayes sign-flip hinge);
    (c) a clean PASS at experimental precision in the per-row audit (Item 6,
        `per_row_theory_error.py`: pull -0.02 against the exact value); and
    (d) a verdict on a binary that is CURRENTLY UNRESOLVED by experiment.

That claim is the atmospheric mixing angle:

        sin^2(theta23) = 4/7 = 0.571428...   ->   theta23 = 49.1 deg
        => the UPPER octant (sin^2 theta23 > 1/2).

Every other neutrino-sector number CHO quotes leans on eps0 or on the seesaw
normalization: sin^2 theta13 = 3 eps0^2, sin^2 theta12 = 1/(3 + sqrt7 eps0),
m_betabeta and Sigma m_nu through eps0 and M_R. Only sin^2 theta23 = 4/7 is a
bare integer ratio, so it is the one place the framework cannot hide behind an
un-derived knob. That makes the octant the sharpest bet in the whole table.

The octant is the Fano discriminator
-------------------------------------
The oscillation octant degeneracy is *exactly* the sin^2 <-> cos^2 ambiguity:

        upper octant:  sin^2 theta23 = 4/7  (theta23 = 49.1 deg)
        lower octant:  sin^2 theta23 = 3/7  (theta23 = 40.9 deg)   [the mirror]

and 4/7 + 3/7 = 1. In the CHO derivation (N5, `epsilon_mixing_coefficients.py`)
these two numbers are the two classes of the octonion Fano plane once the vacuum
omega = (1 + i e7)/2 fixes the point e7: the 7 lines split into 3 THROUGH the
vacuum (the SU(3) colour/stabiliser triplet) and 4 AVOIDING it. The atmospheric
angle is (avoiding)/(total) = 4/7, so the *same* integers that fix the value also
fix the octant: 4 (avoiding) > 3 (through) IS the statement "upper octant".
Resolving the octant therefore directly tests which Fano class controls theta23.

Honest scope (what this does and does NOT claim)
------------------------------------------------
* The map "sin^2 theta23 = (avoiding lines)/(all lines)" is a DERIVED BRIDGE /
  Fano count (ledger N5), not a hand-proven CHO-action theorem. The value 4/7 is
  exact GIVEN that bridge; the bridge itself is the open obligation.
* The octant is currently UNRESOLVED (T2K/NOvA show mild tension; global fits
  carry a near-degenerate lower-octant local minimum), so this is a genuine
  PRE-REGISTERED prediction, not a postdiction. The frozen payload lives in
  `prediction_registry.py` (Q2, hash-locked); this module is the quantified
  analysis around it and cross-checks that locked value read-only.
* Experimental anchors below are representative NuFIT-class normal-ordering
  numbers for CONTEXT only; they are printed, never asserted (they will move).

Kill condition
--------------
A stable resolution to the LOWER octant (sin^2 theta23 < 1/2, the 3/7 side) at
high confidence falsifies the Fano assignment. An upper-octant value pinned far
from 4/7 (beyond the few-percent bridge error) falsifies the precise value while
leaving the octant. Decisive reach: DUNE and Hyper-Kamiokande this decade resolve
the octant and pin sin^2 theta23 to ~+/-0.01, far inside the 0.143 gap between
the 4/7 and 3/7 solutions.

No numpy. Standard-library `math` only, plus the locked registry for the
read-only cross-check.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/theta23_octant_prediction.py
"""

from __future__ import annotations

import math

import prediction_registry


# Octonion Fano-plane line counts once the vacuum fixes e7 (N5; documented in
# epsilon_mixing_coefficients.py -- read off the incidence table, not fitted).
FANO_TOTAL_LINES = 7
FANO_LINES_THROUGH_VACUUM = 3      # SU(3) colour/stabiliser triplet  -> cos^2 side
FANO_LINES_AVOIDING_VACUUM = 4     # broken directions                -> sin^2 side

# CHO triality-breaking knob (only used to DEMONSTRATE that theta23 does NOT
# depend on it; sin^2 theta13 does).
EPS0_SQ = math.pi / 432.0
EPS0 = math.sqrt(EPS0_SQ)

MAXIMAL = 0.5                      # maximal mixing, sin^2 theta23 = 1/2
TOL = 1e-12

# Representative current global-fit anchors (NuFIT-class, NORMAL ordering).
# CONTEXT ONLY -- printed, never asserted; the octant is unresolved.
NO_BESTFIT_SIN2 = 0.55            # upper-octant-side global best fit
NO_SIGMA_SIN2 = 0.02             # representative 1 sigma
NO_LOWER_OCTANT_LOCALMIN = 0.47  # near-degenerate lower-octant minimum


def banner(title: str) -> None:
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


def fano_octant_partition() -> dict:
    """The Fano line partition and the two octant solutions it labels."""
    total = FANO_TOTAL_LINES
    through = FANO_LINES_THROUGH_VACUUM
    avoiding = FANO_LINES_AVOIDING_VACUUM
    sin2 = avoiding / total
    cos2 = through / total
    return {
        "total": total,
        "through_vacuum": through,
        "avoiding_vacuum": avoiding,
        "partition_ok": through + avoiding == total,
        "sin2_theta23": sin2,            # 4/7, upper octant
        "cos2_theta23": cos2,            # 3/7, lower-octant mirror
        "upper_octant": sin2 > MAXIMAL,
        "avoiding_gt_through": avoiding > through,
    }


def the_claim() -> dict:
    """The frozen sharp claim, in value and angle form."""
    part = fano_octant_partition()
    sin2 = part["sin2_theta23"]
    return {
        "sin2_theta23": sin2,
        "theta23_deg": math.degrees(math.asin(math.sqrt(sin2))),
        "theta23_mirror_deg": math.degrees(math.asin(math.sqrt(part["cos2_theta23"]))),
        "octant": "upper" if part["upper_octant"] else "lower",
        "sep_from_maximal": sin2 - MAXIMAL,
        "sep_from_mirror": sin2 - part["cos2_theta23"],
    }


def eps0_independence(scales=(0.80, 0.90, 1.00, 1.10, 1.20)) -> dict:
    """sin^2 theta23 = 4/7 is flat in eps0; sin^2 theta13 = 3 eps0^2 is not.

    This is the structural reason the octant is the sharpest claim: it does not
    move when the open pi/432 seam moves, so it carries no hidden knob.
    """
    sin2_23 = FANO_LINES_AVOIDING_VACUUM / FANO_TOTAL_LINES
    rows = []
    theta23_values = []
    sin2_13_values = []
    for s in scales:
        eps = EPS0 * s
        sin2_13 = 3.0 * eps * eps
        rows.append((s, sin2_23, sin2_13))
        theta23_values.append(sin2_23)
        sin2_13_values.append(sin2_13)
    theta23_spread = max(theta23_values) - min(theta23_values)
    sin2_13_spread = max(sin2_13_values) - min(sin2_13_values)
    return {
        "rows": rows,
        "theta23_spread": theta23_spread,   # exactly 0
        "sin2_13_spread": sin2_13_spread,   # > 0
    }


def registry_crosscheck() -> dict:
    """Read-only confirmation that the locked Q2 payload still says 4/7 / upper."""
    payload = prediction_registry.theta23_octant_values()
    sin2 = FANO_LINES_AVOIDING_VACUUM / FANO_TOTAL_LINES
    expected_deg = math.degrees(math.asin(math.sqrt(sin2)))
    return {
        "payload": payload,
        "value_matches": abs(payload["sin2_theta23"] - sin2) < TOL,
        "octant_matches": payload["octant"] == "upper",
        "angle_matches": abs(payload["theta23_deg"] - expected_deg) < 1e-9,
    }


def discriminating_power() -> dict:
    """How decisively a future octant measurement tests the claim (context)."""
    claim = the_claim()
    sin2 = claim["sin2_theta23"]
    pull_vs_upper = (sin2 - NO_BESTFIT_SIN2) / NO_SIGMA_SIN2
    return {
        "cho_sin2": sin2,
        "no_bestfit": NO_BESTFIT_SIN2,
        "no_sigma": NO_SIGMA_SIN2,
        "lower_octant_localmin": NO_LOWER_OCTANT_LOCALMIN,
        "pull_vs_upper_bestfit": pull_vs_upper,
        "gap_to_lower_octant": sin2 - NO_LOWER_OCTANT_LOCALMIN,
        "mirror_gap": claim["sep_from_mirror"],
    }


def main() -> bool:
    print("#" * 72)
    print("#  CHO ITEM 7 -- THE SHARPEST FALSIFIABLE CLAIM: the theta23 octant")
    print("#  sin^2(theta23) = 4/7, UPPER octant. Frozen, eps0-independent, exact.")
    print("#" * 72)
    print()

    # ------------------------------------------------------------------
    part = fano_octant_partition()
    claim = the_claim()
    banner("A  THE CLAIM")
    print(f"  sin^2(theta23) = {part['avoiding_vacuum']}/{part['total']}"
          f" = {claim['sin2_theta23']:.6f}")
    print(f"  theta23        = {claim['theta23_deg']:.2f} deg   ->  UPPER octant"
          f" (sin^2 > 1/2)")
    print(f"  lower-octant mirror would be 3/7 = {part['cos2_theta23']:.6f}"
          f"  (theta23 = {claim['theta23_mirror_deg']:.2f} deg)")
    print()

    # ------------------------------------------------------------------
    banner("B  WHY THIS IS THE SHARPEST CHO CLAIM (eps0-independent, exact)")
    indep = eps0_independence()
    print("  Among CHO mixing predictions only sin^2 theta23 = 4/7 is a bare")
    print("  rational. Scan eps0 +/- 20%: theta23 is flat, theta13 is not.")
    print(f"    {'eps0 scale':>11} {'sin^2 th23':>12} {'sin^2 th13':>12}")
    for s, s23, s13 in indep["rows"]:
        print(f"    {s:>11.2f} {s23:>12.6f} {s13:>12.6f}")
    print(f"  sin^2 theta23 spread over the scan = {indep['theta23_spread']:.1e}"
          f"  (exactly zero)")
    print(f"  sin^2 theta13 spread over the scan = {indep['sin2_13_spread']:.1e}"
          f"  (moves with the open pi/432 seam)")
    print("  Per-row audit (Item 6): the exact 4/7 passes at experimental")
    print("  precision (pull -0.02); it is the one mixing row that earns a")
    print("  precision test rather than an inflated theory error.")
    print()

    # ------------------------------------------------------------------
    banner("C  THE OCTANT IS THE FANO DISCRIMINATOR")
    print(f"  total Fano lines           = {part['total']}")
    print(f"  through the vacuum (e7)     = {part['through_vacuum']}"
          f"   -> cos^2 side (3/7, lower octant)")
    print(f"  avoiding the vacuum         = {part['avoiding_vacuum']}"
          f"   -> sin^2 side (4/7, upper octant)")
    print(f"  partition closes (3+4=7)    : {part['partition_ok']}")
    print(f"  upper octant <=> avoiding({part['avoiding_vacuum']})"
          f" > through({part['through_vacuum']}) : {part['avoiding_gt_through']}")
    print("  So the SAME integers that fix the value fix the octant: the octant")
    print("  measurement is a direct test of which Fano class controls theta23.")
    print()

    # ------------------------------------------------------------------
    banner("D  CURRENT STATUS + DISCRIMINATING POWER (context, not asserted)")
    disc = discriminating_power()
    print(f"  representative NuFIT-class NO best fit ~ {disc['no_bestfit']:.3f}"
          f" +/- {disc['no_sigma']:.3f} (upper-octant side)")
    print(f"  near-degenerate lower-octant local min ~ {disc['lower_octant_localmin']:.3f}"
          f"  (octant UNRESOLVED)")
    print(f"  CHO 4/7 = {disc['cho_sin2']:.3f}:"
          f" pull vs upper best fit ~ {disc['pull_vs_upper_bestfit']:+.2f} sigma"
          f" (consistent)")
    print(f"  gap 4/7 -> lower-octant min = {disc['gap_to_lower_octant']:+.3f};"
          f"  4/7 -> 3/7 mirror = {disc['mirror_gap']:.3f}")
    print(f"  separation from maximal (0.5) = {claim['sep_from_maximal']:.4f}"
          f"  (DUNE/Hyper-K pin sin^2 to ~+/-0.01)")
    print()

    # ------------------------------------------------------------------
    banner("E  KILL CONDITION + LOCKED-REGISTRY CROSS-CHECK")
    print("  KILL: a stable lower-octant resolution (sin^2 theta23 < 1/2) at high")
    print("        confidence falsifies the Fano assignment; an upper-octant value")
    print("        pinned far from 4/7 (beyond the few-percent N5 bridge error)")
    print("        falsifies the precise value. Decisive: DUNE, Hyper-Kamiokande.")
    cross = registry_crosscheck()
    status = "LOCKED-MATCH" if (cross["value_matches"] and cross["octant_matches"]
                                and cross["angle_matches"]) else "DRIFT"
    print(f"  registry Q2 (Theta23_octant) cross-check: {status}")
    print(f"    payload = {cross['payload']}")
    print()

    print("-" * 72)
    print("  Reading guide: this is a PRE-REGISTERED bet on an unresolved binary,")
    print("  resting on the one exact eps0-independent rational in the table. It")
    print("  is a forward test, NOT new evidence: it does not promote any ledger")
    print("  row and does not move the Bayes factor.")

    # ---- assert only STABLE facts (exact arithmetic / logic) ----
    sin2 = part["sin2_theta23"]
    assert abs(sin2 - 4.0 / 7.0) < TOL, "sin^2 theta23 must equal 4/7 exactly"
    assert sin2 > MAXIMAL, "4/7 must lie in the UPPER octant"
    assert abs(part["cos2_theta23"] - 3.0 / 7.0) < TOL, "mirror must be 3/7"
    assert part["partition_ok"], "Fano partition 3 + 4 = 7 must close"
    assert part["avoiding_gt_through"], "upper octant <=> 4 avoiding > 3 through"
    assert indep["theta23_spread"] == 0.0, "theta23 must be eps0-independent"
    assert indep["sin2_13_spread"] > 0.0, "theta13 must move with eps0 (control)"
    assert abs(claim["sep_from_mirror"] - 1.0 / 7.0) < TOL, "mirror gap = 1/7"
    assert claim["sep_from_maximal"] > 0.05, "must be resolvably non-maximal"
    assert cross["value_matches"] and cross["octant_matches"] and cross["angle_matches"], \
        "locked registry Q2 payload must still read 4/7 / upper octant"

    print("\n  RESULT: PASS (claim staked; forward test, no row promoted).")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
