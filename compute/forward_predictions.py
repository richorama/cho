"""
FROZEN FORWARD PREDICTIONS — three dated, falsifiable CHO targets.
==================================================================

Frozen date: 2026-06-06.  Companion to `predict_neutrino_sum.py` (which freezes
Sigma m_nu).  Roadmap item T2.1.  Do NOT silently retune after new data; log any
revision with a new dated entry.

A theory earns trust by what could KILL it, not by how many known constants it
reproduces. Most of the CHO audit table is postdiction. This module collects the
three sharpest things CHO says about NOT-YET-DECISIVELY-MEASURED quantities, each
with an explicit kill condition tied to a named experiment and reach.

  P1  m_nu3 vs the oscillation floor   -- an INTERNAL tension, the strongest test
  P2  Neutrinoless double-beta m_betabeta (effective Majorana mass)
  P3  Higgs self-coupling kappa_lambda from the CHO quartic lambda = pi/24

Each prediction prints (value/band, basis, date, kill condition). Inputs that are
already-measured experimental anchors (oscillation splittings, v, M_P) are
labelled as such; they are NOT counted as CHO predictions.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/forward_predictions.py
"""

import math


# --------------------------------------------------------------------------
# Shared inputs
# --------------------------------------------------------------------------

# CHO algebraic constants
EPS0_SQ = math.pi / 432.0          # triality-breaking knob (foundations/02_action.md)
EPS0 = math.sqrt(EPS0_SQ)
LAMBDA_CHO = math.pi / 24.0        # Higgs quartic from D4 root geometry (Paper 2)

# Dimensional inputs (measured anchors, not predictions)
M_P = 1.221e19                     # GeV, Planck mass
V_HIGGS = 246.22                   # GeV, electroweak vev
M_H_OBS = 125.09                   # GeV, measured Higgs mass (anchor)

# Oscillation anchors (already-known inputs, NOT predictions)
DM21_SQ = 7.42e-5                  # eV^2, solar splitting (NuFit-class)
DM31_SQ = 2.510e-3                 # eV^2, atmospheric splitting, normal ordering

# CHO seesaw heaviest neutrino state
M_R = M_P / 3.0**9                 # CHO right-handed scale
M_NU3_CHO = (V_HIGGS**2 / (2 * M_R)) * 1e9  # eV


def banner(title):
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


# --------------------------------------------------------------------------
# P1 — m_nu3 vs the oscillation floor (internal tension)
# --------------------------------------------------------------------------
#
# CHO's seesaw predicts m_nu3 from M_R = M_P/3^9 with NO neutrino-sector fit.
# Standard 3-flavour oscillations require m_nu3 >= sqrt(Delta m31^2). CHO's value
# sits BELOW that floor -- a genuine internal tension that future global fits can
# sharpen. This is the strongest CHO forward test precisely because it is not a
# postdiction: it is a place the framework is already in mild conflict with data.


def predict_p1():
    floor = math.sqrt(DM31_SQ) * 1e3            # meV
    cho = M_NU3_CHO * 1e3                        # meV
    tension_pct = (floor - cho) / floor * 100.0

    banner("P1  m_nu3 vs the oscillation floor  (internal tension)")
    print(f"  CHO seesaw m_nu3      = {cho:5.1f} meV   (from M_R = M_P/3^9, no nu fit)")
    print(f"  oscillation floor     = {floor:5.1f} meV   (sqrt(Delta m31^2), measured anchor)")
    print(f"  CHO sits BELOW floor by {tension_pct:.1f}%   ({floor - cho:.1f} meV)")
    print()
    print("  FROZEN STANCE (2026-06-06): CHO's bare seesaw scale undershoots the")
    print("  atmospheric splitting. The framework is viable ONLY if an O(few %)")
    print("  threshold/RG correction lifts m_nu3 onto the floor without a new knob.")
    print()
    print("  KILL CONDITION:")
    print("   * If global fits tighten sqrt(Delta m31^2) and the CHO seesaw")
    print("     normalization (M_P/3^9) is held fixed, and the gap GROWS beyond")
    print("     what a tree-level threshold correction (~few %) can absorb, the")
    print("     CHO neutrino sector is falsified.")
    print("   * Decisive: JUNO (ordering + precision Delta m31^2, ~2027-28).")
    print()
    return {"cho_m_nu3_meV": cho, "floor_meV": floor, "tension_pct": tension_pct}


# --------------------------------------------------------------------------
# P2 — Neutrinoless double-beta effective Majorana mass m_betabeta
# --------------------------------------------------------------------------
#
# m_betabeta = |sum_i U_ei^2 m_i|. CHO fixes the PMNS angles (theta12, theta13)
# and the mass ordering (normal) with a near-massless lightest state (m1 ~ 0).
# The only freedom left is the relative Majorana phase, which CHO does not yet
# fix -- so CHO predicts a BAND, not a point. The band is well below current
# reach but is a sharp, ordering-specific target for next-generation searches.


def predict_p2():
    # CHO-fixed mixing angles
    sin2_12 = 1.0 / (3.0 + math.sqrt(7.0) * EPS0)
    sin2_13 = 3.0 * EPS0_SQ
    cos2_13 = 1.0 - sin2_13

    # Normal ordering, lightest state ~ 0 (CHO hierarchy m1 << m2):
    m1 = 0.0                                   # eV (CHO: near-massless)
    m2 = math.sqrt(m1**2 + DM21_SQ)            # eV, tied by solar splitting
    m3 = math.sqrt(m1**2 + DM31_SQ)            # eV, tied by atmospheric splitting

    # Contributions to |sum U_ei^2 m_i| (m1 term ~ 0 drops out):
    term2 = sin2_12 * cos2_13 * m2             # eV
    term3 = sin2_13 * m3                       # eV

    # Unknown relative Majorana phase -> band [|t2 - t3|, t2 + t3]:
    mbb_lo = abs(term2 - term3) * 1e3          # meV
    mbb_hi = (term2 + term3) * 1e3             # meV

    banner("P2  neutrinoless double-beta m_betabeta")
    print(f"  CHO PMNS inputs: sin^2 th12 = {sin2_12:.3f}, sin^2 th13 = {sin2_13:.4f}")
    print(f"  ordering = NORMAL, lightest m1 ~ 0 (CHO hierarchy)")
    print(f"  m2 = {m2*1e3:.2f} meV, m3 = {m3*1e3:.1f} meV (oscillation anchors)")
    print()
    print(f"  contributions:  sin^2 th12 cos^2 th13 m2 = {term2*1e3:.2f} meV")
    print(f"                  sin^2 th13           m3   = {term3*1e3:.2f} meV")
    print()
    print(f"  FROZEN PREDICTION:  m_betabeta = {mbb_lo:.1f} - {mbb_hi:.1f} meV")
    print(f"  (band width is the undetermined Majorana phase; angles + ordering")
    print(f"   + light m1 are CHO-fixed)")
    print()
    print("  KILL CONDITION:")
    print("   * A confirmed 0nubetabeta signal implying m_betabeta > ~10 meV")
    print("     falsifies CHO: that requires inverted ordering or a heavy lightest")
    print("     state, both excluded by CHO's normal ordering + near-massless m1.")
    print("   * Decisive reach: LEGEND-1000 and nEXO target ~9-21 meV (this decade")
    print("     into next). A positive signal there kills the CHO neutrino sector;")
    print("     a null result is consistent (the CHO band sits below their reach).")
    print()
    return {"mbb_lo_meV": mbb_lo, "mbb_hi_meV": mbb_hi}


# --------------------------------------------------------------------------
# P3 — Higgs self-coupling kappa_lambda from lambda = pi/24
# --------------------------------------------------------------------------
#
# CHO derives the Higgs quartic lambda = pi/24 from D4 root geometry (Paper 2).
# In a single-doublet potential V = lambda (H^dag H - v^2/2)^2 the trilinear
# self-coupling is fixed by lambda. kappa_lambda is the ratio of the actual
# trilinear coupling to its SM value (defined with the MEASURED Higgs mass).
# CHO predicts kappa_lambda very close to 1 -- i.e. NO anomalous self-coupling,
# a sharp null-style prediction that HL-LHC and FCC will test.


def predict_p3():
    # SM quartic implied by the measured Higgs mass: lambda_SM = m_H^2 / (2 v^2)
    lambda_sm = M_H_OBS**2 / (2.0 * V_HIGGS**2)
    # CHO quartic
    lambda_cho = LAMBDA_CHO
    # In the single-doublet potential the trilinear coupling scales with lambda,
    # so kappa_lambda = lambda_cho / lambda_sm.
    kappa_lambda = lambda_cho / lambda_sm
    dev_pct = (kappa_lambda - 1.0) * 100.0
    # The equivalent CHO Higgs-mass prediction (consistency cross-check):
    m_h_cho = V_HIGGS * math.sqrt(math.pi / 12.0)

    banner("P3  Higgs self-coupling kappa_lambda from lambda = pi/24")
    print(f"  CHO quartic        lambda_CHO = pi/24 = {lambda_cho:.5f}")
    print(f"  SM quartic (m_H)   lambda_SM  = m_H^2/2v^2 = {lambda_sm:.5f}")
    print(f"  (cross-check: CHO m_H = v sqrt(pi/12) = {m_h_cho:.2f} GeV vs {M_H_OBS} GeV)")
    print()
    print(f"  FROZEN PREDICTION:  kappa_lambda = {kappa_lambda:.3f}  ({dev_pct:+.1f}% vs SM)")
    print("  i.e. CHO predicts a STANDARD-MODEL-LIKE Higgs self-coupling with NO")
    print("  large anomalous deviation (the single-doublet potential is rigid).")
    print()
    print("  KILL CONDITION:")
    print("   * HL-LHC will constrain kappa_lambda to roughly [0.5, 1.5]; FCC-ee/hh")
    print("     to a few percent. A measured |kappa_lambda - 1| >> few % (a large")
    print("     anomalous self-coupling, e.g. from an extended Higgs sector) would")
    print("     falsify the CHO single-doublet pi/24 quartic.")
    print()
    return {"kappa_lambda": kappa_lambda, "dev_pct": dev_pct}


def main():
    print("#" * 72)
    print("#  CHO FROZEN FORWARD PREDICTIONS (2026-06-06)")
    print("#  Three dated, falsifiable targets with explicit kill conditions.")
    print("#  Companion to predict_neutrino_sum.py (Sigma m_nu).")
    print("#" * 72)
    print()
    predict_p1()
    predict_p2()
    predict_p3()
    print("-" * 72)
    print("  Reading guide: these are the parts of CHO that future data can KILL.")
    print("  P1 is the strongest test (an existing internal tension); P2 and P3 are")
    print("  sharp, ordering/potential-specific targets below current reach. Revise")
    print("  ONLY by adding a new dated entry, never by silent retuning.")
    print()


if __name__ == "__main__":
    main()
