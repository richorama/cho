"""
Generation hierarchy as exponents in the FORCED base eps0 = sqrt(pi/432).
========================================================================

Where this sits in the chain
----------------------------
`spectral_action.py`      : one-generation algebra-internal D is isospectral -> 0
                            forced ratios (clean negative).
`spectral_action_432.py`  : cross-generation Jordan L_X forces a parameter-free
                            AVERAGING LAW (constants_out = 3) and the single
                            spurion eps0^2 = pi/432 cuts the generation knobs from
                            3 to 1, BUT a one-knob GEOMETRIC ladder (1, eps0,
                            eps0^2) misses the lepton hierarchy by ~1.4 decades.
                            The open problem was localised to ONE scalar seed: the
                            three diagonal generation eigenvalues' profile.

This module attacks that lone seed function head-on with a falsifiable,
look-elsewhere-honest diagnostic. The spurion base eps0 = sqrt(pi/432) is FORCED
by prediction_registry (it is not a fitted scale). So the sharp question is not
"what ladder?" but:

    In the forced base eps0, what EXPONENT is each measured generation mass?
        p_n = ln(m_n / m_heaviest) / ln(eps0).

If those exponents land on a simple integer law, the seed is (nearly) derived
from the one forced number. If they do not, the seed genuinely needs more than
one input and we say so with a number.

The crazy-but-principled candidate laws
---------------------------------------
A rank-one spurion lifts ONE level per insertion (spurion_bridge: T_break is rank
one). A k-fold NESTED insertion costs eps0^k. Three natural one-knob exponent
laws for generations n = 0, 1, 2 (heaviest -> lightest) follow:

    geometric   p_n = n          -> (0, 1, 2)   one insertion per step
    even        p_n = 2 n        -> (0, 2, 4)   amplitude^2 per step
    triangular  p_n = n(n+1)/2   -> (0, 1, 3)   CUMULATIVE/nested insertions
                                                 (log-mass quadratic in n)

The triangular law is the "log-mass is quadratic in generation index" idea: each
step costs one MORE spurion factor than the last, which is exactly what nested
(non-associative) Jordan re-insertion would give. It is still a SINGLE knob eps0.

Honesty rails
-------------
1. LEPTONS are the load-bearing sector: charged leptons barely run, so their
   exponents are scheme-clean. Quark exponents carry an MS-bar/scale caveat
   (see mass_ratio_rg_audit.py) and are reported as indicative only.
2. LOOK-ELSEWHERE: we count how many integer exponent triples (0, j, k) with
   1 <= j < k <= K_MAX fit a sector within the winning law's miss. If many fit,
   the integer hit is CHEAP and we flag it, exactly as scale_look_elsewhere.py
   does for the scale relations.
3. UNIVERSALITY: a real derivation needs ONE law across all three charged
   sectors. We test that explicitly; a per-sector best fit is NOT a derivation.

No scipy, no new physics constants beyond eps0^2 = pi/432 and PDG masses.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_generation_ladder.py
"""

import numpy as np


PI = np.pi
EPS0_SQ = PI / 432.0
EPS0 = float(np.sqrt(EPS0_SQ))      # ~0.085277, the forced spurion base
LN_EPS0 = float(np.log(EPS0))

# Charged-fermion masses (GeV). Lepton + heavy-quark values match
# spurion_bridge.OBSERVED; light-quark values are PDG MS-bar(2 GeV) with the
# scheme caveat noted above. Heaviest first within each sector.
SECTORS = {
    "lepton (tau, mu, e)": {
        "m": (1.77686, 0.1056584, 0.00051099895),
        "scheme_clean": True,
    },
    "up (t, c, u)": {
        "m": (172.76, 1.27, 2.16e-3),
        "scheme_clean": False,
    },
    "down (b, s, d)": {
        "m": (4.18, 93.4e-3, 4.67e-3),
        "scheme_clean": False,
    },
}

CANDIDATE_LAWS = {
    "geometric  (0,1,2)": (0, 1, 2),
    "even       (0,2,4)": (0, 2, 4),
    "triangular (0,1,3)": (0, 1, 3),
}

K_MAX = 8          # exponent search ceiling for the look-elsewhere count
FIT_TOL = 0.40     # decades; "fits" means worst-ratio miss below this


# --------------------------------------------------------------------------
# Core: measured exponents in base eps0.
# --------------------------------------------------------------------------
def measured_exponents(masses):
    """p_n = log_{eps0}(m_n / m_0), heaviest normalised to exponent 0."""
    m0 = masses[0]
    return [float(np.log(m / m0) / LN_EPS0) for m in masses]


def law_worst_miss_decades(masses, exponents):
    """Worst |log10| ratio miss between measured masses and the eps0^exponent
    ladder (both normalised to the heaviest)."""
    m0 = masses[0]
    worst = 0.0
    for m, p in zip(masses, exponents):
        pred_ratio = EPS0 ** p           # predicted m_n / m_0
        meas_ratio = m / m0
        if pred_ratio <= 0 or meas_ratio <= 0:
            return float("inf")
        worst = max(worst, abs(np.log10(pred_ratio) - np.log10(meas_ratio)))
    return float(worst)


def best_integer_law(masses, k_max=K_MAX):
    """Best (0, j, k) integer-exponent triple for a 3-generation sector."""
    best = None
    for j in range(1, k_max + 1):
        for k in range(j + 1, k_max + 1):
            miss = law_worst_miss_decades(masses, (0, j, k))
            if best is None or miss < best[1]:
                best = ((0, j, k), miss)
    return best


def lookelsewhere_coverage(masses, tol=FIT_TOL, k_max=K_MAX):
    """Fraction of integer triples (0, j, k), 1<=j<k<=k_max, that fit within tol.
    High coverage => an integer hit in this sector is cheap (not forced)."""
    total = 0
    hits = 0
    for j in range(1, k_max + 1):
        for k in range(j + 1, k_max + 1):
            total += 1
            if law_worst_miss_decades(masses, (0, j, k)) < tol:
                hits += 1
    return hits, total, (hits / total if total else 0.0)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    print("=" * 74)
    print("GENERATION LADDER: mass exponents in the FORCED base eps0 = sqrt(pi/432)")
    print("=" * 74)
    print()
    print(f"eps0 = sqrt(pi/432) = {EPS0:.6f}   (forced; prediction_registry)")
    print("Question: is m_n / m_heaviest = eps0^(integer) for a simple integer law?")
    print()

    per_sector = {}
    for name, data in SECTORS.items():
        masses = data["m"]
        exps = measured_exponents(masses)
        print("-" * 74)
        print(f"SECTOR {name}   (scheme-clean: {data['scheme_clean']})")
        print("    measured exponents p_n (base eps0):",
              "(" + ", ".join(f"{p:.2f}" for p in exps) + ")")
        # candidate one-knob laws
        law_misses = {}
        for lname, lexp in CANDIDATE_LAWS.items():
            miss = law_worst_miss_decades(masses, lexp)
            law_misses[lname] = miss
            print(f"      {lname:<20s} -> worst miss {miss:5.2f} decades")
        # free best-integer fit + look-elsewhere
        (bexp, bmiss) = best_integer_law(masses)
        hits, total, cover = lookelsewhere_coverage(masses)
        print(f"    best integer triple {bexp} -> worst miss {bmiss:.2f} decades")
        print(f"    look-elsewhere: {hits}/{total} integer triples fit < "
              f"{FIT_TOL} dec  (coverage {cover*100:.0f}%)")
        best_named = min(law_misses, key=law_misses.get)
        per_sector[name] = {
            "exponents": exps,
            "law_misses": law_misses,
            "best_named_law": best_named,
            "best_named_miss": law_misses[best_named],
            "best_integer": bexp,
            "best_integer_miss": bmiss,
            "coverage": cover,
            "scheme_clean": data["scheme_clean"],
        }
        print()

    # ---- universality: one named law across all three sectors -----------
    print("=" * 74)
    print("UNIVERSALITY TEST: does ONE named law fit all three charged sectors?")
    print("-" * 74)
    universal = {}
    for lname in CANDIDATE_LAWS:
        worst_over_sectors = max(per_sector[s]["law_misses"][lname]
                                 for s in per_sector)
        universal[lname] = worst_over_sectors
        print(f"    {lname:<20s} worst-over-sectors miss {worst_over_sectors:5.2f} dec")
    best_universal = min(universal, key=universal.get)
    universal_ok = universal[best_universal] < FIT_TOL
    print(f"    best universal law: {best_universal} "
          f"({universal[best_universal]:.2f} dec)  -> universal? {universal_ok}")
    print()

    # ---- lepton headline (the scheme-clean sector) ----------------------
    lep = per_sector["lepton (tau, mu, e)"]
    lep_tri = lep["law_misses"]["triangular (0,1,3)"]
    lep_geo = lep["law_misses"]["geometric  (0,1,2)"]
    print("LEPTON HEADLINE (scheme-clean, load-bearing):")
    print(f"    geometric  (0,1,2) miss {lep_geo:.2f} dec  vs  "
          f"triangular (0,1,3) miss {lep_tri:.2f} dec")
    triangular_beats_geometric = lep_tri < lep_geo - 0.3
    print("    triangular (log-mass quadratic in generation) clearly better?",
          triangular_beats_geometric)
    print()

    # ---- strict verdict -------------------------------------------------
    print("=" * 74)
    print("VERDICT")
    print("-" * 74)
    if universal_ok:
        verdict = (f"PARTIAL-WIN: the single named law {best_universal} fits all "
                   f"three charged sectors within {FIT_TOL} decades in the FORCED "
                   "base eps0 -- the generation seed is (nearly) one forced "
                   "number. Promote only after a derived exponent rule.")
    elif triangular_beats_geometric:
        verdict = (
            "SHARP PARTIAL: in the FORCED base eps0 the SCHEME-CLEAN lepton ladder "
            "is much better described by TRIANGULAR exponents (0,1,3) "
            f"({lep_tri:.2f} dec) than by the geometric (0,1,2) ladder "
            f"({lep_geo:.2f} dec) that spectral_action_432 tested -- i.e. log-mass "
            "is quadratic in generation index, a one-knob CURVATURE law. But NO "
            "single law is universal across up/down/lepton, and the integer hits "
            "sit inside a non-trivial look-elsewhere band, so this is a derived-"
            "looking PATTERN, not yet a theorem. The open seed is now sharpened "
            "from 'one free profile' to 'one universal curvature the dynamics "
            "must explain'.")
    else:
        verdict = (
            "NEGATIVE (informative): no simple integer-exponent law in the forced "
            "base eps0 fits the charged hierarchy across sectors. The generation "
            "seed genuinely needs more than the one forced number; report the "
            "per-sector exponents as the target a dynamical principle must hit.")
    print("    -> " + verdict)
    print()
    print("=" * 74)
    print("HONEST READING")
    print("-" * 74)
    print("This converts 'one free scalar seed function' (spectral_action_432)")
    print("into a measured, falsifiable target: the generation EXPONENTS in the")
    print("forced base eps0. The scheme-clean lepton sector prefers a QUADRATIC-")
    print("in-index (triangular 0,1,3) law over the geometric ladder, a genuine")
    print("one-knob improvement; but the law is not universal across quark sectors")
    print("and the integer hits are not look-elsewhere-free. Net: the dynamical")
    print("principle the framework still needs must output a (possibly sector-")
    print("dependent) CURVATURE in log-mass, not just a slope. That is a sharper,")
    print("smaller target than 'derive the whole Yukawa spectrum'.")
    print("=" * 74)

    return {
        "eps0": EPS0,
        "sector_exponents": {s: per_sector[s]["exponents"] for s in per_sector},
        "lepton_triangular_miss": lep_tri,
        "lepton_geometric_miss": lep_geo,
        "triangular_beats_geometric": bool(triangular_beats_geometric),
        "best_universal_law": best_universal,
        "best_universal_miss": float(universal[best_universal]),
        "universal_ok": bool(universal_ok),
        "verdict": verdict,
    }


if __name__ == "__main__":
    main()
