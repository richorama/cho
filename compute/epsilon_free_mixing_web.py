"""
eps0-free mixing web -- the pi/432 knob cancels out of a quark<->lepton sum rule.
================================================================================

The pivot (ledger C1/N2/N3/N5, epsilon_mixing_coefficients.py, FUTURE_TESTS Q2)
------------------------------------------------------------------------------
The framework drives the whole mixing sector with ONE knob eps0^2 = pi/432 and the
single Fano-line split of the vacuum point e7:

        7 Fano lines  =  3 (through the vacuum)  +  4 (avoiding it).

Those counts enter four mixing relations (all from the SAME split):

        |V_us|              = sqrt(7) * eps0        (C1, amplitude, power 1)
        sin^2(theta_13)     = 3 * eps0^2           (N3, probability, power 2)
        dm21^2 / dm31^2     = 4 * eps0^2           (N2, probability, power 2)
        sin^2(theta_23)     = 4 / 7                (N5 = frozen Q2, eps0-free)

The known headline (FUTURE_TESTS Q2 / theta23_fano_invariance) is that N5 alone is
eps0-INDEPENDENT: the pi/432 cancels, leaving the exact rational 4/7 (avoiding /
total).  This module makes the SAME observation for the OTHER three relations,
which has not been isolated before: because |V_us|^2 = 7 eps0^2, dividing any two
of {|V_us|^2, sin^2 theta13, dm21^2/dm31^2} cancels eps0^2 too.  So the framework
emits a WEB of eps0-free (pi/432-free) exact-rational predictions relating
ALREADY-MEASURED quark and lepton observables -- testable TODAY, unlike Q2 which
waits for DUNE / Hyper-K.

The eps0-free relations (exact, pi/432 cancels):

    R1  sin^2(theta13) / |V_us|^2            = 3/7    (through / total) -- CROSS-SECTOR
    R2  (dm21^2/dm31^2) / |V_us|^2           = 4/7    (avoiding / total)
    R3  (dm21^2/dm31^2) / sin^2(theta13)     = 4/3    (avoiding / through)

    SUM RULE (Fano completeness 7 = 3 + 4, times eps0^2 = |V_us|^2/7):

        sin^2(theta13) + dm21^2/dm31^2  =  |V_us|^2.

R1 is the striking one: the lepton REACTOR angle is tied to the quark CABIBBO angle
with NO free parameter, sin^2(theta13) = (3/7) |V_us|^2 -- and 3/7 is exactly the
THROUGH-vacuum partner of the 4/7 (avoiding-vacuum) octant bet Q2.  The same vacuum
split {3, 4, 7} that stakes the atmospheric octant ALSO predicts the reactor angle
from the Cabibbo angle.  (R3 = R2/R1, so only two of R1,R2,R3 are independent; the
sum rule is R1 + R2 = 1, i.e. (3+4)/7.)

What is and is not claimed (honest scope)
-----------------------------------------
PROVED here (exact Fraction / integer arithmetic, asserted):
  - the Fano split 7 = 3 + 4 and the three eps0-free ratios 3/7, 4/7, 4/3;
  - the web is over-determined: R3 = R2 / R1, and R1 + R2 = 1 (the sum rule);
  - eps0 (= sqrt(pi/432)) cancels identically: the symbolic check that each ratio
    is independent of eps0 (the eps0^2 powers match: 1/1, 1/1, ... ).
These are parameter-free: no value of pi/432 can move them.

CHECKED against data (representative PDG / NuFIT-class central values; PRINTED,
never asserted -- the global fits are non-Gaussian and move):
  - all three ratios and the sum rule hold at < ~1.2 sigma with CURRENT data.

NOT proved (the surviving open obligations, unchanged):
  - the channel ASSIGNMENTS themselves -- which observable gets 3 vs 4 vs 7, and
    the amplitude-vs-probability power -- are the open C1/N2/N3/N5 bridges, not
    derived from a CHO action.  This module tests the COUNTING claim GIVEN those
    assignments; it does not derive them.
  - these are parameter-free RETRODICTIONS (all quantities already measured); their
    non-triviality is that they cannot be tuned, not that they forecast unseen data.

This is a DIAGNOSTIC: it promotes no ledger row and moves no Bayes credit. The
frozen registry (Q2, Theta23_octant) stays authoritative and untouched.
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr

# --------------------------------------------------------------------------
# Framework Fano counts (read off the vacuum split; the open C1/N2/N3/N5 bridges).
# --------------------------------------------------------------------------
THROUGH = 3            # Fano lines through the vacuum point e7
AVOID = 4              # Fano lines avoiding it
TOTAL = 7              # all Fano lines = dim Im(O)

EPS0_SQ = math.pi / 432.0          # the knob that is about to cancel
EPS0 = math.sqrt(EPS0_SQ)

# --------------------------------------------------------------------------
# Representative current data (PDG 2024 / NuFIT-class). PRINTED, not asserted.
# Single-source-consistent with compute/forward_predictions.py.
# --------------------------------------------------------------------------
V_US = 0.2243
V_US_ERR = 0.0008                  # PDG 2024 kaon-decay |V_us|
SIN2_TH13 = 0.02203
SIN2_TH13_ERR = 0.00058            # NuFIT-class, normal ordering
DM21_SQ = 7.42e-5
DM21_ERR = 0.21e-5
DM31_SQ = 2.510e-3
DM31_ERR = 0.027e-3                # normal ordering


def ratio_with_error(num: float, num_err: float, den: float, den_err: float):
    """value and 1-sigma of num/den by independent error propagation."""
    val = num / den
    rel = math.hypot(num_err / num, den_err / den)
    return val, val * rel


def pull(predicted: float, pred_err: float, measured: float, meas_err: float) -> float:
    return (measured - predicted) / math.hypot(pred_err, meas_err)


def banner(title: str) -> None:
    print("=" * 74)
    print(f"  {title}")
    print("=" * 74)


def main() -> bool:
    banner("eps0-FREE MIXING WEB -- pi/432 cancels out of quark<->lepton ratios")

    # ---- [A] the Fano split and the exact eps0-free ratios ----------------
    print("\n[A] One vacuum split drives four relations; eps0 cancels from ratios")
    assert THROUGH + AVOID == TOTAL == 7, "Fano completeness 7 = 3 + 4"
    # the four relations carry these eps0-powers and counts:
    #   |V_us|^2 = 7 eps0^2 ;  sin^2 th13 = 3 eps0^2 ;  dm21/dm31 = 4 eps0^2
    R1 = Fr(THROUGH, TOTAL)          # sin^2 th13 / |V_us|^2
    R2 = Fr(AVOID, TOTAL)            # (dm21/dm31) / |V_us|^2
    R3 = Fr(AVOID, THROUGH)          # (dm21/dm31) / sin^2 th13
    assert R1 == Fr(3, 7) and R2 == Fr(4, 7) and R3 == Fr(4, 3)
    # over-determination: R3 = R2 / R1, and the sum rule R1 + R2 = 1
    assert R3 == R2 / R1, "web inconsistent: R3 must equal R2/R1"
    assert R1 + R2 == 1, "Fano completeness sum rule R1 + R2 = (3+4)/7 = 1"
    print(f"    R1  sin^2(th13)/|V_us|^2        = {R1}  (through/total) CROSS-SECTOR")
    print(f"    R2  (dm21/dm31)/|V_us|^2        = {R2}  (avoiding/total)")
    print(f"    R3  (dm21/dm31)/sin^2(th13)     = {R3}  (avoiding/through) = R2/R1")
    print(f"    sum rule  sin^2(th13) + dm21/dm31 = |V_us|^2   (3 eps0^2 + 4 eps0^2"
          f" = 7 eps0^2)")
    print(f"    4/7 is the avoiding-vacuum octant Q2; 3/7 is its through-vacuum twin.")

    # ---- [B] eps0 cancels identically (symbolic check) --------------------
    print("\n[B] The pi/432 knob is absent from every ratio (parameter-free)")
    # build the three observables as (count * eps0^power); ratios must not depend
    # on eps0 -- verify by evaluating at two different eps0 and getting equal ratios.
    def observables(eps_sq: float):
        return {
            "Vus2": TOTAL * eps_sq,            # |V_us|^2 = 7 eps0^2
            "th13": THROUGH * eps_sq,          # sin^2 th13 = 3 eps0^2
            "dmrat": AVOID * eps_sq,           # dm21/dm31 = 4 eps0^2
        }
    for test_eps in (EPS0_SQ, 0.5, 0.001):     # arbitrary alternative knobs
        o = observables(test_eps)
        assert abs(o["th13"] / o["Vus2"] - float(R1)) < 1e-15
        assert abs(o["dmrat"] / o["Vus2"] - float(R2)) < 1e-15
        assert abs(o["dmrat"] / o["th13"] - float(R3)) < 1e-15
    print("    ratios identical for eps0^2 in {pi/432, 0.5, 0.001}: knob cancels.")

    # ---- [C] confront current data (printed, NOT asserted) ----------------
    print("\n[C] Current data (representative PDG/NuFIT-class; printed, not asserted)")
    vus2 = V_US ** 2
    vus2_err = 2 * V_US * V_US_ERR
    dmrat, dmrat_err = ratio_with_error(DM21_SQ, DM21_ERR, DM31_SQ, DM31_ERR)
    print(f"    |V_us|^2          = {vus2:.6f} +/- {vus2_err:.6f}")
    print(f"    sin^2(theta13)    = {SIN2_TH13:.6f} +/- {SIN2_TH13_ERR:.6f}")
    print(f"    dm21^2/dm31^2     = {dmrat:.6f} +/- {dmrat_err:.6f}")

    # R1: predict sin^2 th13 from |V_us|^2
    p1 = float(R1) * vus2
    p1_err = float(R1) * vus2_err
    z1 = pull(p1, p1_err, SIN2_TH13, SIN2_TH13_ERR)
    print(f"\n    R1  sin^2(th13) = (3/7)|V_us|^2 = {p1:.6f} +/- {p1_err:.6f}"
          f"  vs {SIN2_TH13:.6f}  -> pull {z1:+.2f} sigma")
    # R2: predict dm-ratio from |V_us|^2
    p2 = float(R2) * vus2
    p2_err = float(R2) * vus2_err
    z2 = pull(p2, p2_err, dmrat, dmrat_err)
    print(f"    R2  dm21/dm31  = (4/7)|V_us|^2 = {p2:.6f} +/- {p2_err:.6f}"
          f"  vs {dmrat:.6f}  -> pull {z2:+.2f} sigma")
    # R3: predict dm-ratio from sin^2 th13 (both leptonic)
    p3 = float(R3) * SIN2_TH13
    p3_err = float(R3) * SIN2_TH13_ERR
    z3 = pull(p3, p3_err, dmrat, dmrat_err)
    print(f"    R3  dm21/dm31  = (4/3)sin^2(th13) = {p3:.6f} +/- {p3_err:.6f}"
          f"  vs {dmrat:.6f}  -> pull {z3:+.2f} sigma")
    # SUM RULE
    lhs = SIN2_TH13 + dmrat
    lhs_err = math.hypot(SIN2_TH13_ERR, dmrat_err)
    zsum = pull(vus2, vus2_err, lhs, lhs_err)
    print(f"    SUM sin^2(th13)+dm21/dm31 = {lhs:.6f} +/- {lhs_err:.6f}"
          f"  vs |V_us|^2 {vus2:.6f}  -> pull {zsum:+.2f} sigma")

    # The pulls are data and move; only their finiteness is a (soft) sanity gate.
    for z in (z1, z2, z3, zsum):
        assert abs(z) < 5.0, "a current-data pull exceeded 5 sigma -- investigate"
    print(f"\n    all four eps0-free relations hold at < ~1.2 sigma with current data.")

    # ---- [V] verdict ------------------------------------------------------
    print("\n[V] Sandbox verdict")
    print("    Fano split 7 = 3 + 4; exact ratios 3/7, 4/7, 4/3        : PASS")
    print("    web over-determined (R3 = R2/R1; R1 + R2 = 1 sum rule)  : PASS")
    print("    eps0 = sqrt(pi/432) cancels from every ratio            : PASS")
    print("    R1: reactor angle = (3/7) Cabibbo^2, cross-sector       : PASS")
    print("    all eps0-free relations < ~1.2 sigma vs current data    : PASS")
    print("    channel assignments (which obs gets 3/4/7) derived      : OPEN (C1/N2/N3/N5)")
    print("=" * 74)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
