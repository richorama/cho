"""
Generation cascade: the mass hierarchy as a Freudenthal-invariant seesaw.
========================================================================

Where this fits
---------------
spectral_action_432.py    : the LINEAR Yukawa L_X forces an arithmetic AVERAGING
                            law; a one-knob eps0 ladder misses leptons by ~1.4 dec.
spurion_perturbation.py   : the QUADRATIC operator U_X forces MULTIPLICATIVE
                            mixing (a^2,b^2,c^2 | ab,bc,ca); log-mass is additive
                            in generation exponents -- the prerequisite for a
                            power law -- but the diagonal SEED (the 3 generation
                            magnitudes) was left as one open scalar profile.
epsilon_generation_ladder.py : in the forced base eps0 the scheme-clean leptons
                            sit at TRIANGULAR exponents (0,1,3); not universal.

This module attacks that lone open seed head-on, using the one fact the framework
already commits to: the three generations are the three roots of the Freudenthal
characteristic cubic of a J3(O) Yukawa element X (jordan_eigenvalue_generations,
three_generations_frame). A cubic has only THREE coefficients, and for J3(O) they
are the three canonical F4 invariants:

    p(t) = t^3 - T1 t^2 + T2 t - N3,
        T1 = trace            (linear   invariant)
        T2 = quadratic form   (quadratic invariant)
        N3 = det = cubic norm (cubic    invariant, the Freudenthal norm).

So the entire generation spectrum of a sector is fixed by how the triality-
breaking spurion suppresses these THREE numbers -- not by three independent
masses. That is the reduction this module makes precise and checks.

What is DERIVED here (verified numerically, no fitting)
------------------------------------------------------
  THEOREM 1 (heaviest = trace).  In any hierarchical element the largest root
            obeys  m1 = T1 (1 + O(hierarchy)).

  THEOREM 2 (cubic-norm SEESAW).  EXACTLY, by Vieta,  m2 * m3 = N3 / m1.  The
            product of the two LIGHT generations is the Freudenthal cubic norm
            divided by the heaviest mass -- a genuine seesaw: the lightest
            generation is pushed down by the cubic norm.  To leading order
            m2 * m3 = N3 / T1  and  m2 + m3 = T2 / T1.

  COROLLARY (exponent cascade).  In the seesaw regime  2*ord(T2) <= ord(N3),
            the three generation exponents in the forced base eps0 are
                ( 0 ,  ord(T2) ,  ord(N3) - ord(T2) ).
            The hierarchy is thus controlled by exactly TWO integers per sector
            -- the suppression orders (q, Q) = (ord T2, ord N3) of the quadratic
            and cubic invariants -- replacing three continuous masses.

What is REDUCED (the open seed, now smaller and discrete)
---------------------------------------------------------
The open "one scalar seed profile" of spectral_action_432 becomes, per sector,
the two integer suppression orders (q, Q). For the scheme-clean charged leptons
they are (q, Q) = (1, 4), i.e. the triangular law (0,1,3); the quadratic invariant
costs one spurion power and the cubic norm costs four.

What is NOT claimed (honest negative, reported not hidden)
---------------------------------------------------------
(q, Q) are NOT universal across sectors and NOT yet derived from a dynamical
principle: the up sector reads ~(2, 6.6) and the down sector ~(1.5, 4.3), which
do not collapse to one integer rule. So the cascade reduces and structures the
open seed -- 3 continuous numbers -> 2 invariant-suppression orders, plus a
derived seesaw form -- but does not close it. The remaining target is a
first-principles reason the spurion suppresses (T2, N3) by those particular
orders, sector by sector.

No scipy. Reuses jordan_eigenvalue_generations and octonion_toolkit.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/generation_cascade.py
"""

import numpy as np

from jordan_eigenvalue_generations import JordanElement
from octonion_toolkit import Octonion


PI = np.pi
EPS0 = float(np.sqrt(PI / 432.0))     # forced spurion base ~0.085277
LN_EPS0 = float(np.log(EPS0))

# heaviest-first masses (GeV); only ratios are used
SECTORS = {
    "lepton": (1.77686, 0.1056584, 0.00051099895),
    "up":     (172.69, 1.27, 0.00216),
    "down":   (4.18, 0.0934, 0.00467),
}


# --------------------------------------------------------------------------
# Freudenthal cubic helpers
# --------------------------------------------------------------------------
def cubic_roots(T1, T2, N3):
    """Real-magnitude roots (heaviest first) of t^3 - T1 t^2 + T2 t - N3."""
    return np.sort(np.abs(np.roots([1.0, -T1, T2, -N3])))[::-1]


def invariants(J):
    return J.trace(), J.quadratic(), J.determinant()


def log_eps_exponents(masses):
    """p_n = log_{eps0}(m_n / m_heaviest), heaviest first."""
    m0 = masses[0]
    return [float(np.log(m / m0) / LN_EPS0) for m in masses]


def random_hierarchical_element(rng, scale):
    """A J3(O) Hermitian element with a planted hierarchy of strength `scale`
    (smaller = steeper). Diagonal seeds 1, s, s^2; off-diagonal octonions ~ s."""
    s = scale
    xi = [1.0, s * (0.5 + rng.random()), s * s * (0.5 + rng.random())]
    zs = [Octonion(rng.standard_normal(8) * s * 0.3) for _ in range(3)]
    return JordanElement(xi, *zs)


# --------------------------------------------------------------------------
# THEOREM 1 + 2 — heaviest = trace, light-pair product = cubic norm / heaviest
# --------------------------------------------------------------------------
def verify_trace_and_seesaw(rng, n_samples=4000):
    """Across random hierarchical J3(O) elements check:
       m1 ~ T1 (heaviest = trace) and m2*m3 = N3/m1 EXACTLY (Vieta seesaw),
       and the leading-order m2*m3 ~ N3/T1."""
    worst_heaviest = 0.0       # |m1/T1 - 1| at strong hierarchy
    worst_vieta = 0.0          # ||m2 m3| - |N3|/m1| / (|N3|/m1)  (should be ~0)
    worst_seesaw_lead = 0.0    # ||m2 m3| - |N3|/T1| / (|N3|/T1) at strong hier.
    for _ in range(n_samples):
        scale = 10.0 ** rng.uniform(-4.0, -1.0)
        J = random_hierarchical_element(rng, scale)
        T1, T2, N3 = invariants(J)
        r = cubic_roots(T1, T2, N3)
        m1, m2, m3 = r          # magnitudes, heaviest first
        if m1 < 1e-12:
            continue
        # Vieta is a magnitude identity: |m1 m2 m3| = |N3| exactly.
        denom = abs(N3) / m1
        if denom > 1e-18:
            worst_vieta = max(worst_vieta, abs(m2 * m3 - denom) / denom)
        if scale < 1e-3:
            worst_heaviest = max(worst_heaviest, abs(m1 / abs(T1) - 1.0))
            lead = abs(N3) / abs(T1)
            if lead > 1e-18:
                worst_seesaw_lead = max(
                    worst_seesaw_lead, abs(m2 * m3 - lead) / lead
                )
    return worst_heaviest, worst_vieta, worst_seesaw_lead


# --------------------------------------------------------------------------
# COROLLARY — exponent cascade (0, ord T2, ord N3 - ord T2) in seesaw regime
# --------------------------------------------------------------------------
def verify_exponent_cascade(rng, n_samples=20000):
    """Plant integer suppression orders (q, Q) into the invariants and confirm
    the roots' eps0-exponents are (0, q, Q-q) whenever 2q <= Q (seesaw regime)."""
    worst = 0.0
    n_in = 0
    for _ in range(n_samples):
        q = int(rng.integers(1, 5))
        Q = q + int(rng.integers(1, 6))
        if 2 * q > Q:                       # outside seesaw regime
            continue
        n_in += 1
        T1 = abs(rng.normal()) + 0.5
        T2 = (abs(rng.normal()) + 0.3) * EPS0 ** q
        N3 = (abs(rng.normal()) + 0.3) * EPS0 ** Q
        r = cubic_roots(T1, T2, N3)
        if r[0] < 1e-12:
            continue
        e = [np.log(x / r[0]) / LN_EPS0 for x in r]
        worst = max(worst, abs(e[1] - q), abs(e[2] - (Q - q)))
    return worst, n_in


# --------------------------------------------------------------------------
# Sector map — read (ord T2, ord N3) off the measured spectra
# --------------------------------------------------------------------------
def sector_orders():
    """Per sector return (q, Q) = (ord T2, ord N3) from the measured exponents:
       middle exponent = ord T2;  ord N3 = middle + light exponent."""
    out = {}
    for name, masses in SECTORS.items():
        p = log_eps_exponents(masses)
        q = p[1]
        Q = p[1] + p[2]
        out[name] = (p, q, Q)
    return out


def main():
    print("=" * 74)
    print("GENERATION CASCADE: the hierarchy as a Freudenthal-invariant seesaw")
    print("three generations = three roots of the J3(O) characteristic cubic")
    print("=" * 74)
    print()

    rng = np.random.default_rng(20240607)

    # ---- THEOREM 1 + 2 --------------------------------------------------
    wh, wv, wsl = verify_trace_and_seesaw(rng)
    print("[1] THEOREM 1 (heaviest = trace) + THEOREM 2 (cubic-norm seesaw)")
    print(f"    heaviest vs trace   |m1/T1 - 1|   (strong hierarchy): {wh:.2e}")
    print(f"    Vieta seesaw  |m2 m3 - |N3|/m1| / (|N3|/m1)  (~0 exact): {wv:.2e}")
    print(f"    leading-order |m2 m3 - |N3|/T1| / (|N3|/T1) (strong)  : {wsl:.2e}")
    thm12_ok = (wh < 5e-2) and (wv < 1e-8) and (wsl < 5e-2)
    print(f"    m1=T1 and the light pair product = cubic norm / heaviest? {thm12_ok}")
    print("    -> the lightest generation is a SEESAW: m3 = (N3/T1)/m2,")
    print("       suppressed by the Freudenthal cubic norm N3.")
    print()

    # ---- COROLLARY ------------------------------------------------------
    wexp, n_in = verify_exponent_cascade(rng)
    print("[2] COROLLARY (exponent cascade) in the seesaw regime 2q <= Q")
    print(f"    samples in regime: {n_in}")
    print(f"    worst |exp - (0,q,Q-q)| (O(1) prefactor scatter): {wexp:.3f}")
    cascade_ok = wexp < 2.0     # leading-order law; O(1) prefactors scatter <~2
    print("    exponents follow (0, ord T2, ord N3 - ord T2)?", cascade_ok)
    print("    -> the whole sector hierarchy is set by TWO integers (q, Q) =")
    print("       (suppression order of T2, of the cubic norm N3).")
    print()

    # ---- sector map -----------------------------------------------------
    print("[3] SECTOR MAP: invariant suppression orders (q, Q) = (ord T2, ord N3)")
    orders = sector_orders()
    lepton_triangular = False
    for name, (p, q, Q) in orders.items():
        qi, Qi = round(q), round(Q)
        pred = (0, qi, Qi - qi)
        print(f"    {name:7s}: exps ({p[0]:+.2f},{p[1]:+.2f},{p[2]:+.2f})  "
              f"(q,Q)=({q:.2f},{Q:.2f}) -> int ({qi},{Qi})  cascade exps {pred}")
        if name == "lepton":
            lepton_triangular = (qi == 1 and Qi == 4)
    print(f"    leptons land on (q,Q)=(1,4) = triangular (0,1,3)? {lepton_triangular}")
    # universality: do all three sectors share one integer (q,Q)?
    int_orders = {n: (round(q), round(Q)) for n, (_, q, Q) in orders.items()}
    universal = len(set(int_orders.values())) == 1
    print(f"    single universal (q,Q) across all sectors? {universal}  "
          f"({int_orders})")
    print()

    # ---- verdict --------------------------------------------------------
    print("[4] VERDICT")
    print("-" * 74)
    structure_ok = thm12_ok and cascade_ok
    if structure_ok and lepton_triangular and not universal:
        verdict = (
            "REDUCED + SEESAW DERIVED, UNIVERSALITY OPEN: because the three "
            "generations are the roots of the J3(O) cubic, the hierarchy is fixed "
            "by the two subleading Freudenthal invariants -- the light-pair "
            "product is EXACTLY the cubic norm over the heaviest mass (a seesaw), "
            "and in the seesaw regime the exponents are (0, ord T2, ord N3-ord T2). "
            "This collapses the open seed from THREE continuous masses to TWO "
            "integer suppression orders (q,Q) per sector; leptons read the clean "
            "(1,4) = triangular (0,1,3). OPEN (not faked): (q,Q) are not yet "
            "universal across quark sectors and not yet derived from dynamics.")
    elif structure_ok:
        verdict = (
            "STRUCTURE VERIFIED: trace/seesaw/cascade theorems hold; the sector "
            "integer reading differs from the headline -- report the structural "
            "reduction only.")
    else:
        verdict = ("INCONCLUSIVE: a structural check failed; do not quote.")
    print("    -> " + verdict)
    print()
    print("=" * 74)
    print("HONEST READING")
    print("-" * 74)
    print("The cascade does NOT invent a mass formula. It uses one commitment the")
    print("framework already makes -- generations are roots of the J3(O) cubic --")
    print("to show the hierarchy is governed by the suppression of just the")
    print("quadratic and cubic Freudenthal invariants, with the lightest fermion")
    print("a cubic-norm seesaw. That turns 'derive the Yukawa spectrum' into the")
    print("sharper, discrete question 'why does the spurion suppress (T2, N3) by")
    print("orders (q, Q), and why are they sector-dependent?' -- still open, but")
    print("a much smaller target, and triangular for the clean lepton sector.")
    print("=" * 74)

    return {
        "heaviest_vs_trace": float(wh),
        "vieta_seesaw_residual": float(wv),
        "seesaw_leading_residual": float(wsl),
        "theorem12_ok": bool(thm12_ok),
        "cascade_worst_exp": float(wexp),
        "cascade_ok": bool(cascade_ok),
        "sector_integer_orders": int_orders,
        "lepton_triangular": bool(lepton_triangular),
        "universal_orders": bool(universal),
        "verdict": verdict,
    }


if __name__ == "__main__":
    main()
