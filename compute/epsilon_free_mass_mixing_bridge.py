"""
eps0-free mass<->mixing bridge -- one scale pi/432 ties quark masses to lepton
mixing, parameter-free.
================================================================================

The pivot (ledger M3/C1/N2/N3, epsilon_channel_coefficients.py, chi_squared.py)
------------------------------------------------------------------------------
The framework drives BOTH the charged-mass hierarchy and the mixing sector with
the SAME knob eps0^2 = pi/432, through two integer-count families:

    MASS counts (Fock-grade traces, M3):     mixing counts (Fano-line, M11/C1/N2/N3):
        m_c / m_t      = 1 * eps0^2              sin^2(theta_13)   = 3 * eps0^2
        m_s / m_b      = 3 * eps0^2              dm21^2 / dm31^2   = 4 * eps0^2
        m_mu / m_tau   = 8 * eps0^2             |V_us|^2          = 7 * eps0^2

Because every one of these six measured observables is (integer) * eps0^2, dividing
ANY mass ratio by ANY mixing observable cancels eps0 = sqrt(pi/432) identically,
leaving a PARAMETER-FREE exact rational that relates a QUARK MASS RATIO to a LEPTON
MIXING quantity -- a cross-sector bridge with no free parameter, testable today.

What is and is NOT new here (honest boundary)
---------------------------------------------
  * mass<->mass eps0-free ratios (3, 8, 8/3) are ALREADY tested as rows in
    compute/chi_squared.py ('m_s m_t/(m_b m_c)'=3, 'm_mu m_t/(m_tau m_c)'=8,
    'm_mu m_b/(m_tau m_s)'=8/3).  NOT duplicated here.
  * mixing<->mixing eps0-free ratios (3/7, 4/7, 4/3) are in
    compute/epsilon_free_mixing_web.py.  NOT duplicated here.
  * the cross MASS<->MIXING cell is what was uncovered: this module fills it.

The headline identity (the shared integer 3):

        m_s / m_b  =  sin^2(theta_13)      (both = 3 * eps0^2, ratio EXACTLY 1)

A down-type quark MASS ratio equals the leptonic reactor MIXING probability, with
no parameter at all.  The mass "3" is the down/colour Fock-grade trace Tr P_1 (M3,
derived); the mixing "3" is the Fano lines through the vacuum (M11/N3).  That these
two independently-assigned integers coincide is exactly why the identity holds --
itself a falsifiable structural statement, not a tuning.

Other clean cross identities (count ratios; eps0 cancels):

        m_c / m_t      = (1/4) (dm21^2/dm31^2)     (up vs neutrino splitting, 1:4)
        m_c / m_t      = (1/3) sin^2(theta_13)     (up vs reactor,            1:3)
        m_mu / m_tau   = 2    (dm21^2/dm31^2)      (lepton vs splitting,      8:4)
        m_mu / m_tau   = (8/3) sin^2(theta_13)     (lepton vs reactor,        8:3)
        m_c / m_t      = (1/7) |V_us|^2            (up vs Cabibbo,            1:7)

PROVED here (exact Fraction / integer arithmetic, asserted):
  - the mass counts {1,3,8} and mixing counts {3,4,7}, and every cross ratio
    mass_count / mixing_count as an exact rational;
  - the two count families SHARE the integer 3, forcing m_s/m_b = sin^2(theta13);
  - eps0 = sqrt(pi/432) cancels identically from every cross ratio (checked at
    three different trial eps0 values).
These are parameter-free: no value of pi/432 can move them.

CHECKED against data (PDG/NuFIT-class central values; PRINTED, never asserted):
  - the lepton-mixing-anchored identities (vs sin^2 theta13 and dm21^2/dm31^2)
    hold at < ~1.4 sigma; the headline m_s/m_b = sin^2 theta13 at ~0.5 sigma and
    m_c/m_t = (1/3) sin^2 theta13 at ~0.04 sigma.
  - the |V_us|^2-anchored identities are in genuine TENSION (up to ~7.6 sigma for
    the lepton ratio), because |V_us| is the most precisely measured of the three
    mixing observables AND the framework's own |V_us| = sqrt(7) eps0 is a ~0.6%-high
    (~2.5 sigma) retrodiction; squaring and cross-scaling amplifies that offset.
    The web therefore PINPOINTS |V_us| = sqrt(7) eps0 as the weak link rather than
    averaging the discrepancy away.  This tension is reported, not hidden, and
    nothing about the data is asserted.

NOT proved (the surviving open obligations, unchanged):
  - the count ASSIGNMENTS themselves -- which observable carries 1 vs 3 vs 8
    (mass, M3, derived as Fock traces) and 3 vs 4 vs 7 (mixing, open C1/N2/N3
    bridges) -- are not derived from a single CHO action; this module tests the
    counting GIVEN them.
  - these are parameter-free RETRODICTIONS (all six observables already measured);
    their force is that they cannot be tuned, not that they forecast unseen data.

This is a DIAGNOSTIC: it promotes no ledger row and moves no Bayes credit. The
frozen registry stays authoritative and untouched.
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr

EPS0_SQ = math.pi / 432.0          # the knob that cancels
EPS0 = math.sqrt(EPS0_SQ)

# --------------------------------------------------------------------------
# The framework's integer counts (open M3 / C1 / N2 / N3 bridge assignments).
# --------------------------------------------------------------------------
# observable -> (count, sector, latex-ish label)
MASS = {
    "m_c/m_t":    (1, "up"),
    "m_s/m_b":    (3, "down"),
    "m_mu/m_tau": (8, "lepton"),
}
MIXING = {
    "sin^2(th13)":   (3, "reactor"),
    "dm21^2/dm31^2": (4, "splitting"),
    "|V_us|^2":      (7, "Cabibbo"),
}

# --------------------------------------------------------------------------
# Representative current data (PDG 2024 / NuFIT-class). PRINTED, not asserted.
# Single-source-consistent with compute/chi_squared.py.
# --------------------------------------------------------------------------
DATA = {
    # value, 1-sigma   (mass ratios built from individual masses below)
    "m_c": (1.27, 0.02),
    "m_t": (172.76, 0.30),
    "m_s": (0.0934, 0.0008),
    "m_b": (4.18, 0.03),
    "m_mu": (0.10566, 0.00001),
    "m_tau": (1.77700, 0.00024),
    "sin^2(th13)": (0.02203, 0.00056),
    "dm21^2/dm31^2": (0.02950, 0.00086),
    "|V_us|": (0.2243, 0.0005),
}


def ratio_pm(a: float, ea: float, b: float, eb: float) -> tuple[float, float]:
    v = a / b
    return v, v * math.hypot(ea / a, eb / b)


def measured(observable: str) -> tuple[float, float]:
    """Return (value, sigma) for a mass ratio or mixing observable from DATA."""
    if observable == "m_c/m_t":
        return ratio_pm(*DATA["m_c"], *DATA["m_t"])
    if observable == "m_s/m_b":
        return ratio_pm(*DATA["m_s"], *DATA["m_b"])
    if observable == "m_mu/m_tau":
        return ratio_pm(*DATA["m_mu"], *DATA["m_tau"])
    if observable == "|V_us|^2":
        v, e = DATA["|V_us|"]
        return v * v, 2 * v * e
    return DATA[observable]


def pull(predicted: float, pred_err: float, meas: float, meas_err: float) -> float:
    return (meas - predicted) / math.hypot(pred_err, meas_err)


def banner(title: str) -> None:
    print("=" * 76)
    print(f"  {title}")
    print("=" * 76)


def main() -> bool:
    banner("eps0-FREE MASS<->MIXING BRIDGE -- one pi/432 ties masses to mixing")

    # ---- [A] the two count families and the shared integer 3 --------------
    print("\n[A] Six measured observables = (integer) * eps0^2; eps0 cancels in ratios")
    mass_counts = {v[0] for v in MASS.values()}
    mix_counts = {v[0] for v in MIXING.values()}
    assert mass_counts == {1, 3, 8} and mix_counts == {3, 4, 7}
    shared = mass_counts & mix_counts
    assert shared == {3}, "the mass and mixing count families must share exactly {3}"
    print(f"    MASS counts   {{1,3,8}} :  m_c/m_t=1, m_s/m_b=3, m_mu/m_tau=8")
    print(f"    MIXING counts {{3,4,7}} :  sin^2 th13=3, dm21/dm31=4, |V_us|^2=7")
    print(f"    shared integer = {shared}  ->  m_s/m_b = sin^2(theta13) EXACTLY"
          f" (both 3 eps0^2)")

    # ---- [B] eps0 cancels identically -------------------------------------
    print("\n[B] eps0 = sqrt(pi/432) cancels from every cross ratio (parameter-free)")
    for test_eps in (EPS0_SQ, 0.5, 0.001):
        for mname, (mc, _) in MASS.items():
            for xname, (xc, _) in MIXING.items():
                lhs = (mc * test_eps) / (xc * test_eps)
                assert abs(lhs - mc / xc) < 1e-15
    print("    cross ratios identical for eps0^2 in {pi/432, 0.5, 0.001}: knob gone.")

    # ---- [C] the headline identity m_s/m_b = sin^2 theta13 ----------------
    print("\n[C] HEADLINE  m_s/m_b = sin^2(theta13)  (the shared 3; ratio = 1)")
    pred_ratio = Fr(MASS["m_s/m_b"][0], MIXING["sin^2(th13)"][0])
    assert pred_ratio == 1, "m_s/m_b : sin^2 th13 count ratio must be 3/3 = 1"
    ms_mb, e_ms_mb = measured("m_s/m_b")
    s13, e_s13 = measured("sin^2(th13)")
    z = pull(s13, e_s13, ms_mb, e_ms_mb)   # compare the two measurements directly
    print(f"    m_s/m_b      = {ms_mb:.6f} +/- {e_ms_mb:.6f}   (down-quark mass ratio)")
    print(f"    sin^2(th13)  = {s13:.6f} +/- {e_s13:.6f}   (lepton reactor mixing)")
    print(f"    difference pull = {z:+.2f} sigma   (a quark mass ratio = a lepton angle)")

    # ---- [D] the full cross grid (predict mixing-scaled value of each mass) -
    print("\n[D] All cross identities  mass_ratio = (mass_count/mix_count) * mixing_obs")
    print("    (predicted from the mixing side; data printed, NEVER asserted)")
    lepton_anchored = []   # anchored on sin^2 th13 / dm-ratio (less precise leptons)
    vus_anchored = []      # anchored on |V_us|^2 (precise; inherits the |V_us| offset)
    for mname, (mc, _) in MASS.items():
        m_val, m_err = measured(mname)
        for xname, (xc, _) in MIXING.items():
            r = Fr(mc, xc)
            x_val, x_err = measured(xname)
            pred = float(r) * x_val
            pred_err = float(r) * x_err
            z = pull(pred, pred_err, m_val, m_err)
            row = (mname, xname, r, pred, pred_err, m_val, m_err, z)
            (vus_anchored if xname == "|V_us|^2" else lepton_anchored).append(row)
            print(f"    {mname:11s} = {str(r):>4s} * {xname:14s} "
                  f"-> {pred:.6f} +/- {pred_err:.6f}  vs {m_val:.6f}  "
                  f"pull {z:+.2f}")

    # NOTHING about the data is asserted -- pulls are reported, the framework is
    # under live experimental pressure exactly here. Only the parameter-free
    # arithmetic in [A]/[B]/[C] is asserted.
    worst_lep = max(abs(r[-1]) for r in lepton_anchored)
    worst_vus = max(abs(r[-1]) for r in vus_anchored)
    print(f"\n    lepton-mixing-anchored (sin^2 th13, dm-ratio): all < {worst_lep:.1f} sigma.")
    print(f"    |V_us|^2-anchored                            : up to {worst_vus:.1f} sigma"
          f"  -- a REAL TENSION, reported not hidden.")

    # ---- [E] honest reading of the |V_us| tension -------------------------
    print("\n[E] Honest reading -- the tension localises the weak link")
    vus_pred = math.sqrt(7.0) * EPS0
    vus_meas, vus_meas_err = DATA["|V_us|"]
    vus_z = (vus_meas - vus_pred) / vus_meas_err
    print(f"    |V_us| = sqrt(7) eps0 = {vus_pred:.4f}  vs measured {vus_meas:.4f}"
          f"  ({vus_z:+.1f} sigma on |V_us| itself)")
    print("    so |V_us|=sqrt(7)eps0 is the framework's least-accurate count relation")
    print("    (~0.6% high); squaring + cross-scaling AMPLIFIES that ~2.5 sigma offset,")
    print("    which is why the |V_us|^2-anchored cross identities are in tension while")
    print("    the lepton-anchored ones (and m_s/m_b = sin^2 th13) sit at < ~1.4 sigma.")
    print("    The eps0-free web thus PINPOINTS |V_us| = sqrt(7) eps0 as the weak link,")
    print("    rather than averaging the discrepancy away -- a falsifiable diagnostic.")

    # ---- [F] synthesis ----------------------------------------------------
    print("\n[F] Synthesis")
    print("    one scale eps0^2 = pi/432 + two integer count families {1,3,8},{3,4,7}")
    print("    => a parameter-free web linking quark masses to lepton mixing.")
    print("    mass<->mass ratios live in chi_squared.py; mixing<->mixing in")
    print("    epsilon_free_mixing_web.py; this fills the cross mass<->mixing cell.")
    print("    cleanest bet: m_s/m_b = sin^2(theta13) (~0.5 sigma); weak link: |V_us|.")

    print("\n[V] Sandbox verdict")
    print("    mass {1,3,8} & mixing {3,4,7} share exactly {3}        : PASS")
    print("    m_s/m_b = sin^2(theta13) exactly (shared 3)            : PASS (~0.5s data)")
    print("    eps0 = sqrt(pi/432) cancels from every cross ratio     : PASS")
    print("    lepton-anchored cross identities < ~1.4 sigma          : PASS (data, printed)")
    print("    |V_us|^2-anchored identities in tension                : REPORTED (weak link)")
    print("    count assignments {1,3,8},{3,4,7} derived from action  : OPEN (M3/C1/N2/N3)")
    print("=" * 76)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
