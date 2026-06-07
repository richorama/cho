"""
Inverse-spectral experiment II — the cross-generation 432 = 16 x 27 space.
=========================================================================

Why this module exists
----------------------
`spectral_action.py` ran the smallest honest go/no-go for the inverse-spectral
bet on ONE generation (the module C (x) O = C^8 = 16 real = T(OP^2)). Its result
was a clean, expected NEGATIVE: an algebra-internal, chirality-odd Dirac operator
on a single generation is isospectral (octonion left-multiplications have
eigenvalues +-i), so it carries chirality but NO mass hierarchy. Its closing note
spelled out the next step verbatim:

    "repeat the count on the full 432 space with J3(O) triality acting across the
     three idempotents and ask the same knobs_in vs constants_out question there."

This module is that next step — the single decisive swing at the dynamics
(Option B of the referee plan). It does NOT grind one bridge prefactor at a time
(bayesian_evidence.py proved that is a losing race at ~ -21 nats). It declares ONE
generative object on the generation factor and lets the algebra emit the spectrum
with the minimum number of knobs, then prints a strict KNOBS-IN vs CONSTANTS-OUT
verdict — the same accounting spectral_action.py uses.

Where the hierarchy must live
-----------------------------
The 432 trace space factorises as A_Weyl (x) J3(O) = 16 x 27 (SPURION_BRIDGE,
epsilon_weyl_isomorphism). spectral_action.py already showed the 16-real factor
(one Spin(9) spinor T(OP^2), one generation) is isospectral — it cannot be the
source of a hierarchy. By elimination, any algebra-internal generation spectrum
must come from the 27-dim J3(O) factor. The three generations are the three
primitive idempotents e1, e2, e3 of a maximal frame (three_generations_frame.py),
and the natural algebra-internal cross-generation Yukawa is Jordan LEFT-
MULTIPLICATION

    L_X : Y  |->  X o Y      on J3(O),     X Hermitian (an element of J3(O)).

L_X is self-adjoint for the trace form, so its 27 eigenvalues are real — they are
the candidate cross-generation mass spectrum. We build L_X directly from the
J3(O) structure tensor (epsilon_weyl_isomorphism.jordan_product_tensor) and ask:
is that spectrum FORCED?

The three regimes counted here
------------------------------
[A] GENERIC: X a free Hermitian element. By the Jordan spectral theorem the only
    spectral knobs are the three Freudenthal eigenvalues (a, b, c) of X; the
    off-diagonal octonionic entries are F4-rotated away and do not move the
    spectrum of L_X. So knobs_in = 3.

[B] STRUCTURE: we VERIFY (not assume) the spectrum of L_X from the structure
    tensor. It is rigid in FORM: the 27 eigenvalues are exactly

        {a, b, c}                                     (the 3 generation lines)
        {(a+b)/2, (b+c)/2, (c+a)/2}  each x 8         (the inter-generation blocks)

    i.e. every mixing level is the ARITHMETIC MEAN of two generation levels. That
    averaging law holds for ALL X — three parameter-free relations among the
    spectrum. This is the genuine "constants out": constants_out = 3.

[C] SPURION: the inner frame S3 (three_generations_frame.py PART A) is exact, so
    the unbroken seed a=b=c is totally degenerate (no hierarchy). The repo already
    breaks that S3 with ONE spurion, epsilon0^2 = pi/432 (SPURION_BRIDGE,
    prediction_registry). We seed the frame with that single knob and compare the
    forced ladder to the MEASURED charged-lepton hierarchy. This is the kill test
    for PHYSICAL content, reported strictly: a single eps0 ladder does NOT match
    the observed spectrum, so the absolute generation profile stays open.

Honest expected outcome
-----------------------
A sharp PARTIAL, and a STRICT improvement on the one-generation negative:
  * constants_out = 3 forced, parameter-free relations (the averaging law) —
    derived, not fitted;
  * the spurion reduces the generation knobs from 3 to 1;
  * but one geometric/arithmetic ladder in eps0 does not reproduce the measured
    fermion ratios, so the remaining gap is now exactly ONE seed function (the
    three diagonal eigenvalues' profile), not the whole spectrum.
That localisation — "the open problem is one scalar ladder seed, and the mixing
law is derived" — is the decisive result, and it points at the dynamical
selection principle as the one genuinely open research item.

No scipy. Reuses octonion_toolkit, jordan_eigenvalue_generations and
epsilon_weyl_isomorphism.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/spectral_action_432.py
"""

import numpy as np

from epsilon_weyl_isomorphism import jordan_product_tensor


PI = np.pi
EPS0_SQ = PI / 432.0                 # the single spurion knob (prediction_registry)
EPS0 = float(np.sqrt(EPS0_SQ))

# Measured charged-lepton masses (PDG, MeV) — the hierarchy the ladder must hit.
M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86


# --------------------------------------------------------------------------
# Jordan left-multiplication operator on J3(O) (the cross-generation Yukawa).
# --------------------------------------------------------------------------
def left_mult_operator(T, x):
    """27x27 matrix of L_X : Y -> X o Y, with X = sum_i x_i e_i.

    (L_X)[k, j] = sum_i x_i T[k, i, j], where T is the J3(O) structure tensor.
    """
    return np.einsum("i,kij->kj", x, T)


def diagonal_vector(a, b, c):
    """Coordinate vector of diag(a, b, c) in the 27-basis (first three coords)."""
    v = np.zeros(27)
    v[0], v[1], v[2] = a, b, c
    return v


def real_spectrum(M, tol=1e-9):
    """Sorted real eigenvalues of a (numerically self-adjoint) operator."""
    ev = np.linalg.eigvals(M)
    assert np.max(np.abs(ev.imag)) < 1e-6, "L_X spectrum is not real"
    return np.sort(ev.real)


def distinct_levels(spectrum, tol=1e-6):
    """Collapse a spectrum to distinct levels with multiplicities."""
    levels = []
    for val in spectrum:
        if levels and abs(levels[-1][0] - val) <= tol * max(1.0, abs(val)):
            levels[-1][1] += 1
        else:
            levels.append([val, 1])
    return [(round(v, 9), m) for v, m in levels]


# --------------------------------------------------------------------------
# [A]/[B] Structure: verify the averaging law from the structure tensor.
# --------------------------------------------------------------------------
def verify_averaging_law(T, rng, n_samples=200, tol=1e-7):
    """For random diagonal seeds (a, b, c) check that the 27 eigenvalues of L_X
    are exactly {a, b, c} and {(a+b)/2, (b+c)/2, (c+a)/2} (each x 8).

    Returns (max_residual, multiplicity_ok, sample_levels)."""
    worst = 0.0
    mult_ok = True
    sample_levels = None
    for s in range(n_samples):
        a, b, c = rng.standard_normal(3)
        L = left_mult_operator(T, diagonal_vector(a, b, c))
        spec = real_spectrum(L)
        predicted = np.sort(
            np.array([a, b, c] + [(a + b) / 2, (b + c) / 2, (c + a) / 2])
        )
        # measured distinct levels (values only) vs predicted distinct values
        meas = np.array([v for v, _ in distinct_levels(spec)])
        meas = np.sort(np.unique(np.round(meas, 7)))
        pred = np.sort(np.unique(np.round(predicted, 7)))
        # align lengths defensively (random seeds can make means coincide)
        if meas.size == pred.size:
            worst = max(worst, float(np.max(np.abs(meas - pred))))
        else:
            worst = max(worst, 1.0)
        # multiplicity pattern for a generic (non-degenerate) seed
        if s == 0:
            lv = distinct_levels(spec)
            sample_levels = lv
            mults = sorted(m for _, m in lv)
            # generic: three singlets (a,b,c) + three 8-fold blocks
            mult_ok = (mults == [1, 1, 1, 8, 8, 8])
    return worst, mult_ok, sample_levels


# --------------------------------------------------------------------------
# [C] Spurion: one-knob ladder vs the measured charged-lepton hierarchy.
# --------------------------------------------------------------------------
def ladder_seeds():
    """Single-knob (eps0) generation seeds the algebra can write down.

    Each returns the three diagonal generation eigenvalues as functions of the
    one spurion scale eps0^2 = pi/432. No per-generation knob is added."""
    g = EPS0          # ~0.0853
    return {
        "geometric (1, eps0, eps0^2)": (1.0, g, g * g),
        "arithmetic (1, 1-eps0, 1-2eps0)": (1.0, 1.0 - g, 1.0 - 2.0 * g),
    }


def hierarchy_ratios(triplet):
    """Generation eigenvalues normalised to the heaviest (descending)."""
    t = np.sort(np.abs(np.array(triplet)))[::-1]
    return t / t[0]


def measured_lepton_ratios():
    t = np.array([M_TAU, M_MU, M_E])
    return t / t[0]


def ladder_mismatch():
    """Compare each one-knob ladder to the measured lepton ratios; return the
    best ladder name and its worst log10 ratio mismatch."""
    meas = measured_lepton_ratios()           # (1, m_mu/m_tau, m_e/m_tau)
    results = {}
    for name, triplet in ladder_seeds().items():
        pred = hierarchy_ratios(triplet)
        # compare the two non-trivial ratios in log10 (hierarchy is multiplicative)
        d_mu = abs(np.log10(pred[1]) - np.log10(meas[1]))
        d_e = abs(np.log10(pred[2]) - np.log10(meas[2]))
        results[name] = {
            "pred": pred,
            "log10_miss_mu": float(d_mu),
            "log10_miss_e": float(d_e),
            "worst_log10_miss": float(max(d_mu, d_e)),
        }
    best = min(results, key=lambda k: results[k]["worst_log10_miss"])
    return best, results, meas


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    print("=" * 74)
    print("INVERSE-SPECTRAL EXPERIMENT II: cross-generation 432 = 16 x 27 space")
    print("=" * 74)
    print()
    print("Generation factor: J3(O) (dim 27). Generations = 3 primitive")
    print("idempotents e1,e2,e3. Algebra-internal Yukawa = Jordan L_X : Y -> X o Y.")
    print("(The 16-real T(OP^2) factor was shown isospectral in spectral_action.py.)")
    print()

    rng = np.random.default_rng(0)
    T = jordan_product_tensor()

    # ---- [A] generic knob count -----------------------------------------
    print("[A] GENERIC knobs (free Hermitian X)")
    print("    Jordan spectral theorem: the only spectral knobs are the three")
    print("    Freudenthal eigenvalues (a,b,c) of X.")
    generic_knobs = 3
    print("    knobs_in (generic generation spectrum):", generic_knobs)
    print()

    # ---- [B] structural constants: the averaging law --------------------
    worst, mult_ok, levels = verify_averaging_law(T, rng)
    print("[B] STRUCTURE verified from the J3(O) tensor (200 random seeds)")
    print("    spectrum of L_X = {a,b,c} u {(a+b)/2,(b+c)/2,(c+a)/2} (each x8)?")
    print("    max residual vs that law      :", f"{worst:.2e}")
    print("    multiplicity pattern [1,1,1,8,8,8] on a generic seed?", mult_ok)
    print("    -> mixing level = arithmetic mean of two generation levels")
    print("    constants_out (parameter-free forced relations):", 3)
    constants_out = 3
    print()

    print("[C] SPURION reduction (inner S3 broken by one knob eps0^2 = pi/432)")
    print(f"    eps0 = sqrt(pi/432) = {EPS0:.6f}")
    best, results, meas = ladder_mismatch()
    print("    measured lepton ratios (tau:mu:e) = "
          f"1 : {meas[1]:.4g} : {meas[2]:.4g}")
    for name, r in results.items():
        p = r["pred"]
        print(f"      {name:<28s} -> 1 : {p[1]:.4g} : {p[2]:.4g}"
              f"   worst log10 miss = {r['worst_log10_miss']:.2f}")
    print(f"    best single-knob ladder: {best}")
    print(f"    best worst-case miss   : {results[best]['worst_log10_miss']:.2f}"
          " decades")
    spurion_knobs = 1
    ladder_matches = results[best]["worst_log10_miss"] < 0.30   # < ~2x on every ratio
    print("    one-knob ladder reproduces the measured hierarchy?", ladder_matches)
    print()

    # ---- strict verdict -------------------------------------------------
    print("[D] VERDICT (a derivation requires constants_out > knobs_in AND the")
    print("    forced spectrum matching observation)")
    print("    generic knobs_in                 :", generic_knobs)
    print("    constants_out (averaging law)     :", constants_out)
    print("    spurion-reduced knobs_in          :", spurion_knobs)
    print("    forced ladder matches measured?   :", ladder_matches)
    print()
    if constants_out > generic_knobs and ladder_matches:
        verdict = ("DERIVATION: the 432 structure forces more relations than "
                   "knobs AND the spurion ladder reproduces the spectrum.")
    elif ladder_matches:
        verdict = ("STRONG PARTIAL: spurion ladder reproduces the measured "
                   "hierarchy with one knob; promote with a derived seed.")
    else:
        verdict = (
            "PARTIAL (strict improvement on the one-generation NEGATIVE): the "
            "432 = 16x27 structure DERIVES a parameter-free averaging law "
            "(mixing level = mean of two generation levels, constants_out = 3) "
            "and the inner-S3 spurion reduces the generation spectrum from 3 "
            "free eigenvalues to 1 scale eps0; but no single-knob ladder in "
            "eps0 reproduces the measured fermion ratios. The remaining open "
            "problem is now exactly ONE scalar seed function (the three diagonal "
            "eigenvalues' profile), not the whole Yukawa spectrum. This "
            "MOTIVATES a dynamical selection principle as the lone open item.")
    print("    -> " + verdict)
    print()
    print("=" * 74)
    print("HONEST READING")
    print("-" * 74)
    print("One-generation D was isospectral: 0 forced relations (spectral_action).")
    print("Cross-generation L_X on J3(O) forces 3 (the averaging law) and cuts the")
    print("generation knobs from 3 to 1 under the existing eps0 spurion. It does")
    print("NOT yet output the measured Yukawa eigenvalues -- a single geometric or")
    print("arithmetic ladder in eps0 misses the lepton hierarchy by ~1 decade on")
    print("the lightest state. Net: the open spectrum problem is localised to one")
    print("seed function; closing it needs a dynamical (variational) principle that")
    print("selects the three diagonal eigenvalues, which the algebra alone does not")
    print("supply. That is the single high-risk research item, stated plainly.")
    print("=" * 74)

    return {
        "generic_knobs": generic_knobs,
        "constants_out": constants_out,
        "spurion_knobs": spurion_knobs,
        "averaging_law_residual": float(worst),
        "multiplicity_ok": bool(mult_ok),
        "best_ladder": best,
        "best_worst_log10_miss": float(results[best]["worst_log10_miss"]),
        "ladder_matches": bool(ladder_matches),
        "verdict": verdict,
    }


if __name__ == "__main__":
    main()
