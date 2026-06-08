"""
Three theorems on the exceptional Jordan algebra J3(O), decoupled from physics.
==============================================================================

This module is the runnable companion to PAPER_JORDAN_THEOREMS.md.  Its sole
purpose is to state and machine-verify, as PURE MATHEMATICS, the three results
the project's external review flagged as worth extracting and publishing on their
own merit -- independently of, and logically prior to, any physical ("theory of
everything") interpretation.

Nothing below uses, asserts, or depends on a single physical notion.  There are
no generations, no masses, no Yukawa couplings, no spurion, and the number
pi/432 does not appear.  The objects are the rank-3 exceptional (Albert) Jordan
algebra J3(O) of 3x3 Hermitian octonionic matrices, its automorphism group
F4 = Aut(J3(O)), the isotropy group Spin(9), the reduced structure group
E6 (preserving the Freudenthal cubic norm), and elementary representation theory
(Schur's lemma) and polynomial algebra (Vieta).  A reader who rejects every
physical claim the wider project makes can still check every line here.

The three theorems
------------------
THEOREM A (inner frame symmetry).  The symmetric group S3 permuting the three
    primitive idempotents of a Jordan frame of J3(O) acts by INNER automorphisms:
    it lies in the connected group F4 = Aut(J3(O)), which has no outer
    automorphism.  Hence this S3 cannot carry an F4-module to an inequivalent
    one.  The three idempotents are F4-congruent points of the Cayley plane
    OP^2 = F4/Spin(9): each has isotropy subalgebra of dimension 36 = dim spin(9)
    and tangent space of dimension 16, the unique real Spin(9) spinor Delta_9
    (commutant dimension 1 = real type, hence self-conjugate).
    -> Contrast: the order-3 OUTER (Dynkin/triality) symmetry of D4 = Spin(8)
       permutes three INEQUIVALENT 8-dim modules (8v, 8s, 8c).  The frame S3 of
       J3(O) is a genuinely different, inner symmetry; an obstruction of "vector
       vs spinor / opposite-chirality mirror" type, which relies on outer
       triality, cannot be posed for it.

THEOREM B (Schur rigidity of the invariant mean).  For a compact group G acting
    irreducibly on a real module V of dimension d, the unique G-invariant mean of
    any rank-one orthogonal projector is (1/d) I.  Applied to the two J3(O)-derived
    modules:
      * Delta_9 (dim 16) is irreducible under Spin(9)        -> mean = (1/16) I;
      * J3(O)   (dim 27) is REDUCIBLE under F4 (27 = 1 + 26) -> mean NOT flat
        (the trace direction keeps weight 1/3), but is irreducible under the full
        cubic-norm group E6                                  -> mean = (1/27) I.
    Hence the product module has invariant mean (1/432) I.  The flat weights 1/16
    and 1/27 are forced theorems, not normalization choices, and the 1/27
    specifically requires the cubic-norm group E6, not its derivation subgroup F4.

THEOREM C (a seesaw identity for the Freudenthal cubic).  For X in J3(O) with
    characteristic cubic p(t) = t^3 - T1 t^2 + T2 t - N3 (coefficients the three
    F4 invariants: trace T1, quadratic form T2, cubic norm / Freudenthal
    determinant N3), the three eigenvalues m1 >= m2 >= m3 (by magnitude) obey
    Vieta's relation m1 m2 m3 = N3 exactly, hence
        m2 * m3 = |N3| / m1.
    The product of the two smaller eigenvalues is the cubic norm divided by the
    largest -- a "seesaw" depressing the smallest eigenvalue.  Corollary: if the
    subleading invariants are suppressed at integer orders ord(T2) = q,
    ord(N3) = Q in a small parameter, then in the seesaw regime 2q <= Q the
    eigenvalues sit at orders (0, q, Q - q).

What is classical and what is the contribution (stated honestly)
----------------------------------------------------------------
Every ingredient is classical: the Albert algebra and its frames (Jordan, von
Neumann, Wigner; Springer; McCrimmon); F4 = Aut(J3(O)) connected with no outer
automorphism, and OP^2 = F4/Spin(9) (Freudenthal; Yokota); the 16-dim real
Spin(9) spinor; E6 as the reduced structure group preserving the cubic norm and
the irreducible 27; Schur's lemma; and Vieta's formulae.  The contribution is the
ASSEMBLY plus three observations: (A) that the frame-permuting S3 being inner is
exactly what exempts the idempotent picture from an outer-triality obstruction;
(B) the crisp F4-reducible / E6-irreducible dichotomy that pins the flat 1/27 to
the cubic-norm group; and (C) reading Vieta on the cubic norm as a seesaw.  None
of these is claimed to be a deep new theorem; the value is in collecting
elementary facts into clean, checkable statements decoupled from any physics.

Reuses the project's verified linear-algebra witnesses (it does not re-implement
the hard constructions): F4 / Spin(9) / E6 from epsilon_weyl_isomorphism, the
Reynolds/Schur averages from epsilon_measure_schur, the inner-frame mechanics
from three_generations_frame, and the cubic-root machinery from
generation_cascade.  "Decoupled" refers to the THEOREMS and their proofs, not to
the code: the imported helpers are pure linear algebra with no physical content.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/jordan_standalone_theorems.py
"""

import math

import numpy as np

from jordan_eigenvalue_generations import JordanElement
from epsilon_weyl_isomorphism import (
    jordan_product_tensor,
    derivation_algebra,
    stabiliser_subalgebra,
    clifford9_generators,
    so9_from_clifford,
    commutant_dimension,
)
from epsilon_measure_schur import weight_delta9, weight_j3o
from three_generations_frame import all_frame_perms, apply_frame_perm
from generation_cascade import cubic_roots, random_hierarchical_element

TOL = 1e-9
DIM_F4 = 52
DIM_SPIN9 = 36
DIM_DELTA9 = 16
DIM_J3O = 27
DIM_E6 = 78


# --------------------------------------------------------------------------- #
#  THEOREM A — inner frame symmetry                                           #
# --------------------------------------------------------------------------- #
def _idempotent_vec(slot):
    v = np.zeros(DIM_J3O)
    v[slot] = 1.0
    return v


def inner_frame_symmetry(rng, n_samples=400, tol=TOL):
    """The 6 = |S3| frame permutations preserve the three F4 invariants (trace,
    quadratic form, cubic norm) of every element -> they are inner automorphisms
    in the connected group F4 = Aut(J3(O))."""
    perms = all_frame_perms()
    max_drift = 0.0
    for _ in range(n_samples):
        X = JordanElement.random_hermitian(rng)
        t0, q0, d0 = X.trace(), X.quadratic(), X.determinant()
        for sigma in perms:
            Y = apply_frame_perm(X, sigma)
            max_drift = max(max_drift,
                            abs(Y.trace() - t0),
                            abs(Y.quadratic() - q0),
                            abs(Y.determinant() - d0))
    return len(perms), max_drift


def op2_points():
    """Each primitive idempotent has F4-isotropy of dimension 36 (= spin(9)) and
    tangent dimension 16 -> three F4-congruent points of OP^2 = F4/Spin(9)."""
    f4, _ = derivation_algebra(jordan_product_tensor())
    isotropy, tangent = [], []
    for slot in (0, 1, 2):
        stab = stabiliser_subalgebra(f4, _idempotent_vec(slot))
        isotropy.append(len(stab))
        tangent.append(len(f4) - len(stab))
    return len(f4), isotropy, tangent


def delta9_real_spinor():
    """The 16-dim tangent is the real Spin(9) spinor Delta_9: commutant dimension
    1 (real type), so it is self-conjugate -- no inequivalent mirror partner."""
    gammas = clifford9_generators()
    so9 = so9_from_clifford(gammas)
    return gammas[0].shape[0], commutant_dimension(so9)


# --------------------------------------------------------------------------- #
#  THEOREM B — Schur rigidity of the invariant mean                          #
# --------------------------------------------------------------------------- #
def schur_weights():
    """Flat invariant means forced by irreducibility: 1/16 on Delta_9 under
    Spin(9), 1/27 on J3(O) under E6 (F4 alone leaves it reducible 1 + 26), and
    1/432 on the product."""
    d9_comm, d9_mean, d9_off = weight_delta9()
    j = weight_j3o()
    return {
        "d9_commutant": d9_comm,
        "d9_mean": d9_mean,
        "d9_off": d9_off,
        "f4_commutant": j["f4_commutant"],
        "f4_top_weight": j["f4_top_weight"],
        "e6_commutant": j["e6_commutant"],
        "e6_mean": j["e6_mean_diag"],
        "e6_off": j["e6_max_off"],
        "e6_dim": j["e6_dim"],
        "e6_bracket": j["e6_bracket"],
        "product": (1.0 / DIM_DELTA9) * (1.0 / DIM_J3O),
    }


# --------------------------------------------------------------------------- #
#  THEOREM C — Freudenthal-cubic seesaw                                       #
# --------------------------------------------------------------------------- #
def freudenthal_seesaw(rng, n_samples=2000):
    """Vieta on the Freudenthal cubic: m1 m2 m3 = N3 exactly, so the light pair
    product m2 m3 = |N3| / m1 (a cubic-norm seesaw). Also the heaviest eigenvalue
    tracks the trace in a strong hierarchy (a leading-order corollary)."""
    worst_vieta = 0.0
    worst_heaviest = 0.0
    for _ in range(n_samples):
        scale = 10.0 ** rng.uniform(-4.0, -1.0)
        X = random_hierarchical_element(rng, scale)
        T1, T2, N3 = X.trace(), X.quadratic(), X.determinant()
        m1, m2, m3 = cubic_roots(T1, T2, N3)
        if m1 < 1e-12:
            continue
        denom = abs(N3) / m1
        if denom > 1e-18:
            worst_vieta = max(worst_vieta, abs(m2 * m3 - denom) / denom)
        if scale < 1e-3:
            worst_heaviest = max(worst_heaviest, abs(m1 / abs(T1) - 1.0))
    return worst_vieta, worst_heaviest


def order_cascade(rng, base=0.1, n_samples=8000):
    """In a GENERIC small parameter `base` (an arbitrary mathematical parameter,
    not a physical constant), planting suppression orders ord(T2) = q and
    ord(N3) = Q yields eigenvalue orders (0, q, Q - q) in the seesaw regime
    2q <= Q (a leading-order corollary, with O(1) prefactor scatter)."""
    ln_base = math.log(base)
    worst = 0.0
    n_in = 0
    for _ in range(n_samples):
        q = int(rng.integers(1, 5))
        Q = q + int(rng.integers(1, 6))
        if 2 * q > Q:
            continue
        n_in += 1
        T1 = abs(rng.normal()) + 0.5
        T2 = (abs(rng.normal()) + 0.3) * base ** q
        N3 = (abs(rng.normal()) + 0.3) * base ** Q
        m = cubic_roots(T1, T2, N3)
        if m[0] < 1e-12:
            continue
        e = [math.log(x / m[0]) / ln_base for x in m]
        worst = max(worst, abs(e[1] - q), abs(e[2] - (Q - q)))
    return worst, n_in


# --------------------------------------------------------------------------- #
#  Driver                                                                      #
# --------------------------------------------------------------------------- #
def main():
    rng = np.random.default_rng(20260608)

    print("=" * 78)
    print("  THREE THEOREMS ON THE EXCEPTIONAL JORDAN ALGEBRA J3(O)")
    print("  Pure mathematics -- decoupled from every physical interpretation.")
    print("=" * 78)

    # ---- THEOREM A ------------------------------------------------------
    n_perms, drift = inner_frame_symmetry(rng)
    dim_f4, isotropy, tangent = op2_points()
    dim16, comm9 = delta9_real_spinor()
    print("\n  THEOREM A — inner frame symmetry (S3 < F4, no outer automorphism)")
    print("  " + "-" * 66)
    print(f"      |S3| frame perms = {n_perms};  max drift of (trace,quad,norm): {drift:.1e}")
    print( "      -> the frame S3 preserves all three F4 invariants => inner in F4")
    print(f"      dim F4 = Aut(J3O) = {dim_f4}  (expect {DIM_F4})")
    print(f"      isotropy at e1,e2,e3 = {isotropy}  (expect {DIM_SPIN9} = dim spin(9))")
    print(f"      tangent  at e1,e2,e3 = {tangent}  (expect {DIM_DELTA9} = dim Delta_9)")
    print(f"      Delta_9 dim = {dim16}, Spin(9) commutant = {comm9}"
          f"  (1 => real type, self-conjugate)")
    a_ok = (drift < TOL and dim_f4 == DIM_F4
            and isotropy == [DIM_SPIN9] * 3 and tangent == [DIM_DELTA9] * 3
            and dim16 == DIM_DELTA9 and comm9 == 1)
    print(f"      [{'PASS' if a_ok else 'FAIL'}] three F4-congruent OP^2 points, one real spinor each;")
    print( "             Spin(8)'s OUTER triality permutes inequivalent 8v,8s,8c --")
    print( "             this INNER S3 is categorically different (no such obstruction).")

    # ---- THEOREM B ------------------------------------------------------
    w = schur_weights()
    print("\n  THEOREM B — Schur rigidity: flat invariant means 1/16, 1/27, 1/432")
    print("  " + "-" * 66)
    print(f"      Delta_9 / Spin(9): commutant {w['d9_commutant']}, mean diag "
          f"{w['d9_mean']:.6f} (1/16={1 / DIM_DELTA9:.6f}), off {w['d9_off']:.1e}")
    print(f"      J3(O)   / F4     : commutant {w['f4_commutant']} (REDUCIBLE 1+26), "
          f"trace-dir weight {w['f4_top_weight']:.3f} (=1/3) -> NOT flat")
    print(f"      J3(O)   / E6     : commutant {w['e6_commutant']}, mean diag "
          f"{w['e6_mean']:.6f} (1/27={1 / DIM_J3O:.6f}), off {w['e6_off']:.1e}")
    print(f"      E6 closure: dim {w['e6_dim']} (={DIM_E6}), bracket {w['e6_bracket']:.1e}")
    print(f"      product (1/16)(1/27) = {w['product']:.8f} = 1/432")
    b_ok = (w["d9_commutant"] == 1 and abs(w["d9_mean"] - 1 / DIM_DELTA9) < TOL
            and w["d9_off"] < TOL and w["f4_commutant"] == 2
            and w["f4_top_weight"] > 0.3 and w["e6_commutant"] == 1
            and abs(w["e6_mean"] - 1 / DIM_J3O) < TOL and w["e6_off"] < TOL
            and w["e6_dim"] == DIM_E6 and abs(w["product"] - 1.0 / 432.0) < 1e-12)
    print(f"      [{'PASS' if b_ok else 'FAIL'}] 1/16 and 1/27 are forced by irreducibility;")
    print( "             the flat 1/27 needs the cubic-norm group E6, not subgroup F4.")

    # ---- THEOREM C ------------------------------------------------------
    vieta, heaviest = freudenthal_seesaw(rng)
    cascade, n_in = order_cascade(rng)
    c_exact = vieta < 1e-8
    print("\n  THEOREM C — Freudenthal-cubic seesaw (Vieta on the cubic norm)")
    print("  " + "-" * 66)
    print(f"      Vieta  |m2 m3 - |N3|/m1| / (|N3|/m1)  (EXACT theorem): {vieta:.1e}")
    print(f"      heaviest vs trace |m1/T1 - 1| (leading-order corollary): {heaviest:.1e}")
    print(f"      order cascade worst |exp-(0,q,Q-q)| over {n_in} (base 0.1, "
          f"leading order): {cascade:.3f}")
    print(f"      [{'PASS' if c_exact else 'FAIL'}] light-pair product = cubic norm / heaviest;")
    print( "             the smallest eigenvalue is a cubic-norm seesaw.")

    # ---- DECOUPLING + verdict ------------------------------------------
    print("\n  " + "-" * 74)
    print("  DECOUPLING (the point of this module)")
    print("      No generation, mass, Yukawa, spurion, or pi/432 appears above.")
    print("      The three results are theorems of J3(O), of F4/Spin(9)/E6")
    print("      representation theory, and of Vieta -- true regardless of any")
    print("      physical interpretation, which is developed and gated SEPARATELY")
    print("      and is NOT established by these theorems. See PAPER_JORDAN_THEOREMS.md.")

    ok = a_ok and b_ok and c_exact

    # Stable mathematical theorems -- a regression must crash the audit.  Only
    # the EXACT statements are asserted; the leading-order corollaries (heaviest
    # vs trace, order cascade) are reported as diagnostics, not gated.
    assert drift < TOL, "frame S3 must preserve the F4 invariants (inner)"
    assert isotropy == [DIM_SPIN9] * 3 and tangent == [DIM_DELTA9] * 3
    assert dim16 == DIM_DELTA9 and comm9 == 1, "Delta_9 is a real-type spinor"
    assert w["d9_commutant"] == 1 and abs(w["d9_mean"] - 1 / DIM_DELTA9) < TOL
    assert w["f4_commutant"] == 2, "J3(O) is F4-reducible (1 + 26)"
    assert w["e6_commutant"] == 1 and abs(w["e6_mean"] - 1 / DIM_J3O) < TOL
    assert abs(w["product"] - 1.0 / 432.0) < 1e-12, "1/16 x 1/27 = 1/432"
    assert vieta < 1e-8, "Vieta cubic-norm seesaw is exact"

    print("\n  RESULT:", "PASS" if ok else "FAIL",
          "- three decoupled J3(O) theorems verified.")
    print("=" * 78)
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
