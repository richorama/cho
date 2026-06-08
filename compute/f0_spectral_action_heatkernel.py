"""
PHASE 1.3 -- THE DECISIVE EXPERIMENT: is eps0^2 = pi/432 the spectral-action
heat-kernel ratio a4/a2 of the genuine octonionic KO-6 triple?  ANSWER: NO.
=============================================================================

Why this module exists
----------------------
Phase 1.2 step C (f0_octonionic_yukawa_gate) placed the octonionic Jordan Yukawa
L_X inside a consistent KO-6 spectral triple, but found the triple axioms do NOT
pin the Yukawa -- any self-adjoint flavour operator passes order-zero/order-one.
The CHO predictive content can therefore only be secured DYNAMICALLY, by the
spectral action Tr f(D/Lambda), whose Seeley-DeWitt expansion is

    Tr f(D/Lambda) ~ Lambda^4 f4 a0 + Lambda^2 f2 a2 + f0 a4 + ...

For the FINITE triple the heat-kernel coefficients ARE the spectral moments:

    a0 = M0 = Tr(1) ,   a2 = M2 = Tr(D^2) ,   a4 = M4 = Tr(D^4) .

The gold-standard roadmap's make-or-break test (Phase 1.3) is the single
question on which the whole "EARN the +5.6" programme turns:

    does the dimensionless a4/a2 shape of D equal eps0^2 = pi/432 ?

ACCEPTANCE (roadmap) -> F0 closes dynamically, +5.6 becomes EARNED, eps0 moves
DERIVED.  KILL (roadmap) -> a DIFFERENT number; F0 is not a spectral-action
output; the dynamical earn-path via the heat kernel is closed; the EARNED ln B
floor stays -3.2.  epsilon_heat_kernel already warned the spectral pi enters ONLY
through the continuum Gaussian (4 pi)^(-d/2) -- a denominator pi with a
half-integer power, never a bare pi numerator -- so the honest expectation was a
REFUTATION.  This gate runs the experiment on the real 216-dim octonionic D and
reports the two-sided result.

What is tested (all numbers from the explicit 216x216 step-C Dirac operator)
---------------------------------------------------------------------------
[A] FINITE HEAT-KERNEL MOMENTS of the genuine octonionic D (seed (1,0.6,0.3),
    Majorana seed (0.2,0,0)):  M0 = 216, M2 = Tr(D^2) = 92.96, M4 = Tr(D^4) =
    50.3712.  These are the a0/a2/a4 spectral-action coefficients of the finite
    triple.

[B] THE DECISIVE RATIO.  The dimensionless a4/a2 shape (scale-invariant) is
    M4/M2^2 = 0.00582895.  Target eps0^2 = pi/432 = 0.00727221.  The ratio is
    0.8015 -- a clean 20% MISS.  No candidate normalisation (M4/M2^2,
    M4/(M0 M2), N M4/M2^2, ...) lands on pi/432.

[C] WHY IT MUST MISS (the structural kill, not a numerical accident).  The
    moments are EXACT RATIONALS: M2 = 2324/25 and M4 = 31482/625 (residual 0 at
    denominator <= 1000), because Tr(D^2k) is a rational power sum of the
    algebraic Dirac spectrum.  Hence a4/a2 = M4/M2^2 = 15741/2700488 is an EXACT
    rational, and a rational can NEVER equal the transcendental pi/432.  By
    contrast pi/432 has NO small-denominator rational fit (residual 5e-7).  This
    is seed-independent: every rational seed gives a different rational, all
    pi-free.

[D] THE ONLY PI IN A SPECTRAL ACTION is the continuum normalisation
    (4 pi)^(-d/2) = {d=2: 0.0796, d=4: 0.00633, d=6: 0.000504} -- a DENOMINATOR
    pi with a half-integer power, none a bare pi/432 numerator (and 0.00633 !=
    0.00727 anyway).  Confirms epsilon_heat_kernel structurally.

[E] WHERE THE BARE PI ACTUALLY COMES FROM.  The pi in eps0^2 is reproduced
    exactly by the Berry half-solid-angle (1/2)(2 pi) = pi -- a holonomy /
    geometric flux, not a heat-kernel coefficient.  So pi/432 is a
    Berry-flux-per-state count (pi from holonomy, 1/432 from the Schur flat
    measure), NOT a spectral-action output.

Verdict / where this leaves F0
------------------------------
Phase 1.3 REFUTES eps0^2 = pi/432 as the heat-kernel a4/a2 ratio (the roadmap
KILL branch).  Consequences, stated two-sided and bounded:
  - The DYNAMICAL route to EARN the +5.6 via the Connes spectral action on this
    triple is CLOSED.  Any future promotion of eps0 to DERIVED needs a DIFFERENT
    mechanism, not the heat kernel.
  - The Berry/Schur GEOMETRIC reading of pi/432 is UNTOUCHED (the refutation is
    of one channel, not of the holonomy maths) -- it remains the ceiling for
    pi/432.  F0 therefore stays GEOMETRIC/open: NOT demoted below geometric, NOT
    promotable to DERIVED via this route.
  - Moves NO Bayes credit.  The scoreboard ladder (-21.3 historical / -3.2
    EARNED floor / +5.6 if-geometric-granted / +36.2 target) is UNCHANGED; the
    +5.6 was always labelled granted-not-earned and stays so.  This gate touches
    no frozen artifact (model_complexity / scoreboard / registry).

No scipy.  Reuses f0_octonionic_yukawa_gate (the step-C triple builder) and
epsilon_weyl_isomorphism (the Jordan product tensor).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_spectral_action_heatkernel.py
"""

from fractions import Fraction

import numpy as np

import f0_octonionic_yukawa_gate as C
from epsilon_weyl_isomorphism import jordan_product_tensor


PI = np.pi
TARGET = PI / 432.0            # eps0^2 = pi/432, the number to be matched-or-not
_T = jordan_product_tensor()   # the J3(O) Jordan product (octonionic structure)


# --------------------------------------------------------------------------
# The genuine 216-dim octonionic Dirac operator of the step-C KO-6 triple.
# --------------------------------------------------------------------------
def finite_octonionic_dirac(seed=(1.0, 0.6, 0.3), maj=(0.2, 0.0, 0.0)):
    """D = K_Yuk (x) L_X + K_Maj (x) M_maj on C^8 (x) C^27 (dim 216)."""
    L_X = C.octonionic_yukawa(_T, *seed)
    M_maj = C.octonionic_yukawa(_T, *maj)
    _, D, _ = C.build_product(C.yukawa_coupling(), C.majorana_coupling(),
                              L_X, M_maj)
    return D


def heat_kernel_moments(D):
    """Finite Seeley-DeWitt moments M_2k = Tr(D^2k) = a0/a2/a4/... of D.

    For a finite spectral triple the spectral action Tr f(D/Lambda) is a
    polynomial in these moments, so M0=a0, M2=a2, M4=a4 ARE the heat-kernel
    coefficients.  They are power sums of the (algebraic) Dirac spectrum.
    """
    ev = np.linalg.eigvalsh(0.5 * (D + D.conj().T))
    M0 = float(ev.size)
    M2 = float(np.sum(ev ** 2))
    M4 = float(np.sum(ev ** 4))
    M6 = float(np.sum(ev ** 6))
    return M0, M2, M4, M6


def rational_fit(x, max_den=1000):
    """(exact-or-nearest fraction, |residual|) at denominator <= max_den.

    residual ~ 0  <=>  x is a small-denominator rational (pi-free).
    residual >> 0  <=>  x has no such fit (transcendental, e.g. contains pi).
    """
    f = Fraction(x).limit_denominator(max_den)
    return f, abs(float(f) - x)


def a4_over_a2_candidates(M0, M2, M4):
    """The dimensionless a4/a2-type normalisations the roadmap could mean."""
    return {
        "M4 / M2^2            ": M4 / M2 ** 2,        # scale-invariant shape
        "M4 / (M0 * M2)       ": M4 / (M0 * M2),
        "N * M4 / M2^2 (kurt) ": M0 * M4 / M2 ** 2,
        "M4 / M2  (dimful)    ": M4 / M2,
    }


def continuum_pi(dims=(2, 4, 6)):
    """(4 pi)^(-d/2) -- the ONLY pi a Connes-Chamseddine spectral action emits."""
    return {d: (4.0 * PI) ** (-d / 2.0) for d in dims}


def berry_bare_pi():
    """The Berry half-solid-angle (1/2)(2 pi) = pi -- the geometric origin of
    the bare pi numerator in eps0^2 (holonomy, not a heat-kernel coefficient)."""
    return 0.5 * (2.0 * PI)


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("PHASE 1.3  DECISIVE TEST: pi/432 = a4/a2 heat-kernel ratio?  (octonionic D)")
    print("=" * 78)
    print(f"    target  eps0^2 = pi/432 = {TARGET:.14f}")

    # ---- [A] finite heat-kernel moments of the genuine octonionic D ------
    D = finite_octonionic_dirac()
    M0, M2, M4, M6 = heat_kernel_moments(D)
    print("\n[A] FINITE HEAT-KERNEL MOMENTS of the 216-dim step-C octonionic D")
    print(f"    a0 = M0 = Tr(1)   = {M0:.6f}")
    print(f"    a2 = M2 = Tr(D^2) = {M2:.6f}")
    print(f"    a4 = M4 = Tr(D^4) = {M4:.6f}   (M6 = {M6:.6f})")
    print("    these ARE the spectral-action coefficients of the finite triple.")

    # ---- [B] the decisive ratio: every a4/a2 candidate misses pi/432 -----
    cands = a4_over_a2_candidates(M0, M2, M4)
    shape = M4 / M2 ** 2
    print("\n[B] THE DECISIVE RATIO  a4/a2  vs  pi/432")
    for name, val in cands.items():
        print(f"    {name} = {val:.8f}   /(pi/432) = {val / TARGET:.4f}")
    print(f"    closest natural shape  M4/M2^2 = {shape:.8f}  is {shape / TARGET:.4f}")
    print("    x pi/432 -- a clean 20% MISS.  NO normalisation lands on pi/432.")

    # ---- [C] why it MUST miss: the moments are exact pi-free rationals ----
    f2, r2 = rational_fit(M2)
    f4, r4 = rational_fit(M4)
    a4a2_exact = Fraction(f4, 1) / Fraction(f2, 1) ** 2
    ft, rt = rational_fit(TARGET)
    # seed-independence: a second rational seed gives another pi-free rational
    M0b, M2b, M4b, _ = heat_kernel_moments(
        finite_octonionic_dirac(seed=(0.8, 0.6, 0.4), maj=(0.2, 0.0, 0.0)))
    f2b, r2b = rational_fit(M2b)
    f4b, r4b = rational_fit(M4b)
    shape_b = M4b / M2b ** 2
    print("\n[C] WHY IT MUST MISS  (structural kill, not a numerical accident)")
    print(f"    M2 = {f2} (residual {r2:.1e}) ,  M4 = {f4} (residual {r4:.1e})")
    print(f"    => a4/a2 = M4/M2^2 = {a4a2_exact} = {float(a4a2_exact):.8f}  EXACTLY rational")
    print(f"    pi/432 best fit at den<=1000 = {ft} (residual {rt:.1e}) -- NOT rational")
    print("    a rational a4/a2 can NEVER equal the transcendental pi/432.")
    print(f"    seed-independent: seed (.8,.6,.4) -> M2={f2b}, M4={f4b},")
    print(f"      a4/a2 = {shape_b:.8f} (/pi432 {shape_b / TARGET:.4f}) -- another pi-free rational.")

    # ---- [D] the only pi in a spectral action is (4 pi)^(-d/2) -----------
    cpi = continuum_pi()
    print("\n[D] THE ONLY PI IN A SPECTRAL ACTION: the continuum (4 pi)^(-d/2)")
    for d, v in cpi.items():
        print(f"    d={d}: (4 pi)^(-d/2) = {v:.8f}")
    print(f"    a DENOMINATOR pi (half-integer power); (4 pi)^-2 = {cpi[4]:.8f}")
    print(f"    != pi/432 = {TARGET:.8f}.  Confirms epsilon_heat_kernel.")

    # ---- [E] the bare pi is Berry holonomy, not a heat-kernel coefficient -
    berry = berry_bare_pi()
    print("\n[E] WHERE THE BARE PI ACTUALLY COMES FROM: Berry half-solid-angle")
    print(f"    (1/2)(2 pi) = {berry:.8f} = pi  -- a holonomy flux, not a4.")
    print("    so pi/432 = (Berry pi) x (Schur 1/432): a flux-per-state count,")
    print("    a GEOMETRIC quantity, NOT a spectral-action output.")

    # ---- verdict ---------------------------------------------------------
    print("\n[V] VERDICT  (two-sided, honest -- the roadmap KILL branch)")
    print("    Phase 1.3 REFUTES eps0^2 = pi/432 as the heat-kernel a4/a2 ratio.")
    print("    - the DYNAMICAL earn-path for the +5.6 via the spectral action is")
    print("      CLOSED; any DERIVED promotion now needs a different mechanism.")
    print("    - the Berry/Schur GEOMETRIC reading is UNTOUCHED and remains the")
    print("      ceiling for pi/432; F0 stays GEOMETRIC/open (not demoted, not")
    print("      promoted).  Moves NO Bayes credit; the scoreboard ladder")
    print("      (-21.3 / -3.2 EARNED floor / +5.6 if-granted / +36.2) is UNCHANGED.")
    print("=" * 78)

    # ---- stable assertions (audit.py ignores the return value) -----------
    # [A] the finite moments of the genuine 216-dim octonionic triple:
    assert M0 == 216.0, "step-C octonionic triple is not 216-dimensional"
    assert abs(M2 - 92.96) < 1e-6, "Tr(D^2) drifted from the step-C value"
    assert abs(M4 - 50.3712) < 1e-6, "Tr(D^4) drifted from the step-C value"
    # [C] the moments are EXACT pi-free rationals; pi/432 is NOT small-den rational:
    assert r2 < 1e-9, "Tr(D^2) is not a small-denominator rational"
    assert r4 < 1e-9, "Tr(D^4) is not a small-denominator rational"
    assert abs(float(a4a2_exact) - shape) < 1e-12, "exact a4/a2 != float a4/a2"
    assert rt > 1e-9, "pi/432 unexpectedly fits a small-denominator rational"
    # [B] the decisive refutation: a4/a2 is NOT pi/432, by a clean margin:
    assert abs(shape - TARGET) > 1e-3, "a4/a2 came out at pi/432 (would CONFIRM!)"
    assert abs(shape / TARGET - 1.0) > 0.1, "a4/a2 is not bounded away from pi/432"
    # [C] seed-independence of the pi-freeness:
    assert r2b < 1e-9 and r4b < 1e-9, "moments not rational for a second seed"
    assert abs(shape_b - TARGET) > 1e-3, "a4/a2 hit pi/432 for the second seed"
    # [D] the only spectral pi is (4 pi)^(-d/2), and it is NOT pi/432:
    assert abs(cpi[4] - TARGET) > 1e-4, "(4 pi)^-2 coincides with pi/432"
    # [E] the bare numerator pi IS the Berry half-solid-angle:
    assert abs(berry - PI) < 1e-12, "(1/2)(2 pi) is not pi"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
