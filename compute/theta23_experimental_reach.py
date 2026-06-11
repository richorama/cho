"""
Item 7c -- the experimental confrontation of sin^2(theta23) = 4/7.
==================================================================

`theta23_octant_prediction.py` (Item 7) STAKES the bet: sin^2(theta23) = 4/7,
upper octant, the one exact eps0-independent mixing rational. It quotes a single
representative global-fit anchor and one prose line ("DUNE/Hyper-K pin sin^2 to
~+/-0.01"). This module does the QUANTITATIVE forward-reach forecast that the
prose only gestures at, and confronts 4/7 with the *current* data honestly --
including the central values that DISFAVOUR it.

The exact spine (this is what is asserted)
------------------------------------------
The two octant solutions and maximal mixing form an EXACT symmetric triplet:

        lower octant (mirror) :  sin^2 theta23 = 3/7 = 0.428571...
        maximal               :  sin^2 theta23 = 1/2 = 0.500000...
        upper octant (CHO)    :  sin^2 theta23 = 4/7 = 0.571428...

Because 3/7 + 4/7 = 1, maximal mixing is the EXACT arithmetic midpoint:
(3/7 + 4/7)/2 = 1/2. So each Fano solution sits exactly 1/14 from maximal, and
the two are 1/7 = 0.142857... apart. These are exact rationals -- no fit, no
eps0, no knob -- so the whole confrontation reduces to two fixed distances:

        gap to maximal  = 4/7 - 1/2 = 1/14 = 0.0714...   (the octant test)
        gap to mirror   = 4/7 - 3/7 = 1/7  = 0.1429...    (= 2 x the maximal gap)

A measurement of precision sigma therefore separates 4/7 from maximal at
(1/14)/sigma standard deviations and from the 3/7 mirror at (1/7)/sigma; and a
true-4/7 universe is resolved to the upper octant with probability Phi((1/14)/sigma).
Inverting, reaching an n-sigma octant verdict needs sigma = (1/14)/n. All exact.

Honest current status (printed, NEVER asserted -- the field is unresolved)
--------------------------------------------------------------------------
The octant is genuinely open and ORDERING-DEPENDENT. Representative recent
global fits (NuFIT-class) sit on BOTH sides of maximal:

  * Normal ordering: the GLOBAL chi^2 minimum often falls just BELOW maximal
    (sin^2 theta23 ~ 0.45, the 3/7 side), with a near-degenerate upper-octant
    LOCAL minimum (~0.56). Taken at face value this DISFAVOURS 4/7.
  * Inverted ordering: the best fit sits clearly in the UPPER octant
    (sin^2 theta23 ~ 0.57), essentially on top of 4/7.

So 4/7 is a real falsifiable bet under live tension, not a postdiction dressed
to fit. The chi^2 profiles are strongly non-Gaussian (double-welled in NO), so
the Gaussian pulls below are rough indicators for context only. The frozen
payload lives in `prediction_registry.py` (Q2, hash-locked); this module reads
it back read-only and does not move it.

What this module does NOT claim
-------------------------------
* It does not derive the physical N5 map "atmospheric mixing = avoiding/total";
  that bridge stays the open CHO-action obligation. 4/7 is exact GIVEN it.
* It is a forecast/confrontation DIAGNOSTIC: it promotes no ledger row and does
  not touch the Bayes factor. The forward bet itself is staked in Item 7.

No numpy / scipy. Standard-library `math` (erf for the normal CDF) and
`fractions` for the exact spine, plus the locked registry for the read-only
cross-check.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/theta23_experimental_reach.py
"""

from __future__ import annotations

import math
from fractions import Fraction

import prediction_registry


# ---- the exact spine (rationals; no fit, no eps0) -------------------------
SIN2_UPPER = Fraction(4, 7)        # CHO prediction, upper octant
SIN2_MAXIMAL = Fraction(1, 2)      # maximal mixing
SIN2_MIRROR = Fraction(3, 7)       # lower-octant mirror (4/7 + 3/7 = 1)
GAP_MAXIMAL = SIN2_UPPER - SIN2_MAXIMAL   # 1/14  -- the octant test
GAP_MIRROR = SIN2_UPPER - SIN2_MIRROR     # 1/7   -- the full octant span

TOL = 1e-12

# Projected single-measurement precisions on sin^2(theta23). The high-statistics
# long-baseline + atmospheric programmes (DUNE, Hyper-Kamiokande) target the
# ~0.005-0.01 band this decade; the looser rows show today's reach. CONTEXT
# anchors -- only the EXACT gap/sigma arithmetic on top of them is asserted.
PROJECTED_SIGMAS = (0.020, 0.015, 0.010, 0.005)
REFERENCE_SIGMA = 0.010            # representative DUNE/Hyper-K era precision

# Representative current global-fit anchors (NuFIT-class). Illustrative ONLY:
# printed, never asserted; chi^2 profiles are non-Gaussian. Deliberately spans
# the lower-octant NO global minimum that DISFAVOURS 4/7.
#   (label, sin2_bestfit, sigma_lo, sigma_hi, note)
GLOBAL_FITS = (
    ("NO global min  ", 0.450, 0.016, 0.020, "below maximal -> 3/7 side (disfavours 4/7)"),
    ("NO upper local ", 0.558, 0.020, 0.016, "near-degenerate upper local minimum"),
    ("IO best fit     ", 0.570, 0.021, 0.013, "upper octant, sits on 4/7"),
)


def banner(title: str) -> None:
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


def norm_cdf(z: float) -> float:
    """Standard normal CDF via the error function (stdlib only)."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


# ---------------------------------------------------------------------------
#  [A]  the exact symmetric triplet
# ---------------------------------------------------------------------------
def symmetric_triplet() -> dict:
    """The 3/7 | 1/2 | 4/7 triplet: maximal is the EXACT midpoint of the two."""
    midpoint = (SIN2_MIRROR + SIN2_UPPER) / 2
    return {
        "mirror": SIN2_MIRROR,
        "maximal": SIN2_MAXIMAL,
        "upper": SIN2_UPPER,
        "midpoint_is_maximal": midpoint == SIN2_MAXIMAL,
        "gap_maximal": GAP_MAXIMAL,            # 1/14
        "gap_mirror": GAP_MIRROR,              # 1/7
        "mirror_is_twice_maximal": GAP_MIRROR == 2 * GAP_MAXIMAL,
        "theta_upper_deg": math.degrees(math.asin(math.sqrt(float(SIN2_UPPER)))),
        "theta_maximal_deg": math.degrees(math.asin(math.sqrt(float(SIN2_MAXIMAL)))),
        "theta_mirror_deg": math.degrees(math.asin(math.sqrt(float(SIN2_MIRROR)))),
    }


# ---------------------------------------------------------------------------
#  [B]  forward reach: separation and octant-resolution probability vs sigma
# ---------------------------------------------------------------------------
def forward_reach(sigmas=PROJECTED_SIGMAS) -> list:
    """For each projected precision sigma, the separation (in sigma) of 4/7
    from maximal and from the 3/7 mirror, and the probability a true-4/7
    universe is resolved to the upper octant, Phi((1/14)/sigma)."""
    gap_max = float(GAP_MAXIMAL)
    gap_mir = float(GAP_MIRROR)
    rows = []
    for sigma in sigmas:
        sep_max = gap_max / sigma
        sep_mir = gap_mir / sigma
        rows.append({
            "sigma": sigma,
            "sep_from_maximal": sep_max,            # = (1/14)/sigma
            "sep_from_mirror": sep_mir,             # = (1/7)/sigma = 2 * sep_max
            "p_resolve_upper": norm_cdf(sep_max),   # P(measure > 1/2 | true 4/7)
        })
    return rows


def precision_for_separation(targets=(1.0, 3.0, 5.0)) -> list:
    """Invert the octant test: the precision sigma needed to separate 4/7 from
    maximal at n sigma is sigma = (1/14)/n (and from the mirror at (1/7)/n)."""
    gap_max = float(GAP_MAXIMAL)
    gap_mir = float(GAP_MIRROR)
    rows = []
    for n in targets:
        rows.append({
            "n_sigma": n,
            "sigma_vs_maximal": gap_max / n,
            "sigma_vs_mirror": gap_mir / n,
        })
    return rows


# ---------------------------------------------------------------------------
#  [C]  current data confrontation (context only; printed, never asserted)
# ---------------------------------------------------------------------------
def octant_upper_probability(bestfit: float, sigma_lo: float, sigma_hi: float) -> float:
    """One-sided Gaussian toy P(sin^2 theta23 > 1/2): use the error bar on the
    side facing maximal. At bestfit = 1/2 this is exactly 0.5 for any sigma."""
    if bestfit >= 0.5:
        z = (bestfit - 0.5) / sigma_lo
    else:
        z = (bestfit - 0.5) / sigma_hi
    return norm_cdf(z)


def current_confrontation() -> list:
    """Pull of 4/7 against each representative fit (error bar on the side facing
    4/7), and the toy upper-octant probability. ILLUSTRATIVE -- printed only."""
    upper = float(SIN2_UPPER)
    rows = []
    for label, bestfit, sig_lo, sig_hi, note in GLOBAL_FITS:
        # 4/7 is above every plausible central value -> use the upper error bar.
        sigma_face = sig_hi if upper >= bestfit else sig_lo
        pull = (upper - bestfit) / sigma_face
        rows.append({
            "label": label,
            "bestfit": bestfit,
            "pull_of_4_7": pull,
            "p_upper_octant": octant_upper_probability(bestfit, sig_lo, sig_hi),
            "note": note,
        })
    return rows


# ---------------------------------------------------------------------------
#  [D]  read-only registry cross-check
# ---------------------------------------------------------------------------
def registry_crosscheck() -> dict:
    """Confirm the locked Q2 payload still reads 4/7 / upper (read-only)."""
    payload = prediction_registry.theta23_octant_values()
    return {
        "payload": payload,
        "value_matches": abs(payload["sin2_theta23"] - float(SIN2_UPPER)) < TOL,
        "octant_matches": payload["octant"] == "upper",
    }


# ---------------------------------------------------------------------------
#  Reporting + tripwires
# ---------------------------------------------------------------------------
def main() -> bool:
    print("#" * 72)
    print("#  CHO ITEM 7c -- EXPERIMENTAL CONFRONTATION OF sin^2(theta23) = 4/7")
    print("#  Forward-reach forecast + honest current-data confrontation.")
    print("#  Diagnostic: stakes nothing new, promotes no row, moves no Bayes.")
    print("#" * 72)
    print()

    # ------------------------------------------------------------------
    tri = symmetric_triplet()
    banner("A  THE EXACT SYMMETRIC TRIPLET (maximal is the midpoint)")
    print(f"  lower octant (mirror) sin^2 = 3/7 = {float(tri['mirror']):.6f}"
          f"  -> theta23 = {tri['theta_mirror_deg']:.2f} deg")
    print(f"  maximal               sin^2 = 1/2 = {float(tri['maximal']):.6f}"
          f"  -> theta23 = {tri['theta_maximal_deg']:.2f} deg")
    print(f"  upper octant (CHO)    sin^2 = 4/7 = {float(tri['upper']):.6f}"
          f"  -> theta23 = {tri['theta_upper_deg']:.2f} deg")
    print(f"  (3/7 + 4/7)/2 == 1/2 (maximal is the EXACT midpoint) : "
          f"{tri['midpoint_is_maximal']}")
    print(f"  gap to maximal = 1/14 = {float(tri['gap_maximal']):.6f}  (octant test)")
    print(f"  gap to mirror  = 1/7  = {float(tri['gap_mirror']):.6f}"
          f"  (= 2 x maximal gap : {tri['mirror_is_twice_maximal']})")
    print()

    # ------------------------------------------------------------------
    reach = forward_reach()
    banner("B  FORWARD REACH -- separation of 4/7 vs sigma (exact gap/sigma)")
    print("    sigma     sep vs 1/2    sep vs 3/7    P(resolve upper | true 4/7)")
    print("    " + "-" * 64)
    for r in reach:
        print(f"    {r['sigma']:.3f}     {r['sep_from_maximal']:6.2f} s     "
              f"{r['sep_from_mirror']:6.2f} s     {r['p_resolve_upper']:.6f}")
    ref = next(r for r in reach if abs(r["sigma"] - REFERENCE_SIGMA) < TOL)
    print(f"  At the DUNE/Hyper-K-era sigma~{REFERENCE_SIGMA:.3f}: 4/7 stands "
          f"{ref['sep_from_maximal']:.1f}s from maximal, {ref['sep_from_mirror']:.1f}s "
          f"from the 3/7 mirror.")
    print()

    # ------------------------------------------------------------------
    inv = precision_for_separation()
    banner("C  PRECISION REQUIRED -- sigma to reach an n-sigma octant verdict")
    print("    target      sigma vs 1/2     sigma vs 3/7")
    print("    " + "-" * 48)
    for r in inv:
        print(f"    {r['n_sigma']:.0f} sigma       {r['sigma_vs_maximal']:.4f}"
              f"          {r['sigma_vs_mirror']:.4f}")
    print("  So a 5-sigma octant verdict on 4/7 vs maximal needs sigma <= "
          f"{inv[-1]['sigma_vs_maximal']:.4f} -- inside the DUNE/Hyper-K target band.")
    print()

    # ------------------------------------------------------------------
    conf = current_confrontation()
    banner("D  CURRENT DATA (representative NuFIT-class; PRINTED, NOT asserted)")
    print("    fit              best fit   pull of 4/7   P(upper octant)   note")
    print("    " + "-" * 78)
    for r in conf:
        print(f"    {r['label']}  {r['bestfit']:.3f}     {r['pull_of_4_7']:+5.1f} s      "
              f"{r['p_upper_octant']:.3f}          {r['note']}")
    print("  Honest read: the NO global minimum sits BELOW maximal and disfavours")
    print("  4/7 today; the IO best fit sits on it. The octant is genuinely open and")
    print("  ordering-dependent -- a live falsifiable bet, not a postdiction. (chi^2")
    print("  profiles are non-Gaussian; these Gaussian pulls are rough indicators.)")
    print()

    # ------------------------------------------------------------------
    banner("E  KILL CONDITION + LOCKED-REGISTRY CROSS-CHECK")
    print("  KILL: DUNE / Hyper-Kamiokande pin sin^2 theta23 to ~+/-0.005-0.01. A")
    print("        stable value below 1/2 (the 3/7 side) falsifies the Fano octant;")
    print("        an upper value pinned far from 4/7 falsifies the precise rational.")
    reg = registry_crosscheck()
    status = "LOCKED-MATCH" if (reg["value_matches"] and reg["octant_matches"]) else "DRIFT"
    print(f"  registry Q2 (Theta23_octant) cross-check: {status}")
    print(f"    payload = {reg['payload']}")
    print()

    print("-" * 72)
    print("  Reading guide: this is the QUANTIFIED reach around the Item 7 bet, plus")
    print("  an honest confrontation with current (partly unfavourable) data. It is a")
    print("  forecast DIAGNOSTIC: it stakes nothing new, promotes no ledger row, and")
    print("  does not move the Bayes factor. The N5 physical map stays the open seam.")

    # ---- assert ONLY the exact / structural spine (anchors never asserted) ----
    # [A] exact ordering and symmetric triplet
    assert SIN2_UPPER > SIN2_MAXIMAL > SIN2_MIRROR, "ordering 4/7 > 1/2 > 3/7 must hold"
    assert SIN2_UPPER + SIN2_MIRROR == 1, "octant mirror complementarity 4/7 + 3/7 = 1"
    assert tri["midpoint_is_maximal"], "maximal must be the EXACT midpoint of 3/7 and 4/7"
    assert GAP_MAXIMAL == Fraction(1, 14), "gap to maximal must be exactly 1/14"
    assert GAP_MIRROR == Fraction(1, 7), "gap to mirror must be exactly 1/7"
    assert tri["mirror_is_twice_maximal"], "mirror gap must be exactly twice the maximal gap"

    # [B] forward reach is exact gap/sigma, monotone, with mirror = 2 x maximal
    prev = None
    for r in reach:
        assert abs(r["sep_from_maximal"] - float(GAP_MAXIMAL) / r["sigma"]) < TOL, \
            "separation from maximal must equal (1/14)/sigma exactly"
        assert abs(r["sep_from_mirror"] - 2.0 * r["sep_from_maximal"]) < TOL, \
            "mirror separation must be exactly twice the maximal separation"
        if prev is not None:
            assert r["sep_from_maximal"] > prev, "separation must grow as sigma shrinks"
        prev = r["sep_from_maximal"]
    assert ref["sep_from_maximal"] > 5.0, "DUNE/HK-era sigma must clear 5s from maximal"
    assert ref["sep_from_mirror"] > 10.0, "DUNE/HK-era sigma must clear 10s from the mirror"
    assert ref["p_resolve_upper"] > 0.999, "true-4/7 octant resolution must exceed 0.999"

    # [C] precision inversion is exact and tighter for higher n
    prev_sigma = None
    for r in inv:
        assert abs(r["sigma_vs_maximal"] - float(GAP_MAXIMAL) / r["n_sigma"]) < TOL, \
            "required sigma vs maximal must equal (1/14)/n exactly"
        assert abs(r["sigma_vs_mirror"] - 2.0 * r["sigma_vs_maximal"]) < TOL, \
            "required sigma vs mirror must be exactly twice that vs maximal"
        if prev_sigma is not None:
            assert r["sigma_vs_maximal"] < prev_sigma, "higher n must demand tighter sigma"
        prev_sigma = r["sigma_vs_maximal"]

    # normal-CDF sanity + octant-probability toy boundary
    assert abs(norm_cdf(0.0) - 0.5) < TOL, "norm_cdf(0) must be 1/2"
    assert abs(octant_upper_probability(0.5, 0.02, 0.02) - 0.5) < TOL, \
        "a best fit exactly at maximal must give P(upper) = 1/2"

    # [E] locked registry still reads 4/7 / upper (read-only)
    assert reg["value_matches"] and reg["octant_matches"], \
        "locked registry Q2 payload must still read 4/7 / upper"

    print("\n  RESULT: PASS (forecast staked; diagnostic, no row promoted).")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
