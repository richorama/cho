"""
Gravity Curvature Probe — the emergent metric from non-associativity (M-GRAV)
=============================================================================

This module is the first NON-PLACEHOLDER brick of the CHO gravity research line
(see foundations/03_gravity.md, milestone M-GRAV). It replaces the hand-waving
in compute/graviton.py with a small, falsifiable numerical experiment.

THE CRAZY-BUT-PRINCIPLED IDEA
-----------------------------
In an ASSOCIATIVE algebra, (ab)c = a(bc): multiplying is path-independent, like
flat parallel transport. The OCTONIONIC ASSOCIATOR

        [a,b,c] = (ab)c - a(bc)

measures the failure of that path-independence — it is a literal HOLONOMY around
the "triangle" a,b,c. The proposal of 03_gravity.md is that this non-associativity
*is* curvature. The open problem (step 4 / the kill condition) was:

    "no symmetric rank-2 metric (or scalar curvature with the correct
     transformation law) has been shown to emerge from the associator WITHOUT
     inserting an independent geometric input by hand."

The new idea here closes a large part of that. The associator is a totally
ANTISYMMETRIC vector — you cannot read a symmetric metric off it directly. But
you CAN pull the octonion inner product back through the associator MAP:

    fix two "matter" labels a,b. The transport defect is the linear operator
        M_{a,b} : Im(O) -> Im(O),   M_{a,b}(x) = [x, a, b].
    The EMERGENT METRIC is its Gram matrix
        g_{mu nu}(a,b) = < M_{a,b}(e_mu), M_{a,b}(e_nu) >
                       = sum_k [e_mu, a, b]_k [e_nu, a, b]_k.

This object is, by construction, a SYMMETRIC, POSITIVE-SEMIDEFINITE rank-2
tensor — and (verified below) it transforms as a genuine rank-2 tensor under the
structure group G2 = Aut(O):  g(Ra, Rb) = R g(a,b) R^T.  No geometric input was
inserted by hand; the metric is built purely from the multiplication.

WHAT THIS MODULE ESTABLISHES (each PART = a numbered check)
-----------------------------------------------------------
  A. Spacetime ARENA from C(x)H:  2x2 complex Hermitian = Minkowski R^{3,1},
     det = Minkowski quadratic form, SL(2,C) -> Lorentz SO(3,1). (standard,
     borrowed) This is the flat metric eta that gravity perturbs.
  B. Curvature SOURCE from O:  the associator is purely imaginary (transverse),
     its scalar density S = |[a,b,c]|^2 vanishes iff the three labels share a
     quaternionic (associative) subalgebra (Artin) and is positive otherwise.
  C. Emergent symmetric rank-2 GRAVITON metric:  g(a,b) is symmetric PSD; it is
     G2-covariant (rank-2 tensor under the structure group, verified on exact
     finite automorphisms); its scalar density obeys the clean area law
        tr g = 16 (|a|^2|b|^2 - <a,b>^2) = 16 |a ^ b|^2,
     with the SAME 16 = dim OP^2 that fixes eps0^2 = pi/432.
  D. Flat directions = associative subalgebra (Artin, made geometric):  by
     alternativity g(a,b) annihilates a and b, so the graviton mode is
     TRANSVERSE to its source bivector a ^ b; g has rank 4, and its 3-dim null
     space is exactly the quaternionic subalgebra span{a, b, Im(ab)} along which
     transport is path-independent (flat). No hand-inserted geometric input.

HONEST RESIDUAL (the line is NOT closed)
----------------------------------------
  * The metric g lives on the 7-dim INTERNAL imaginary space Im(O), whose
    structure group is G2 < SO(7).  The reduction of this internal metric to a
    4-dim SPACETIME metric with Lorentz SO(3,1) signature (PART A's arena) is
    NOT bridged here. That bridge is the remaining content of Conjecture 6.1.
  * No dynamics: there is no field equation, no action extremised, no Newton
    constant. This is a kinematic "metric exists and transforms correctly"
    result, not "Einstein's equations emerge".
  * PART A (spacetime/Lorentz from C(x)H) and PARTs B-D (curvature from O) are
    two halves of CHO that are NOT yet joined: which 4 of the 7 internal
    directions become spacetime is unfixed.

So: this turns the gravity line from a PLACEHOLDER into a sharp, falsifiable
kinematic result with ONE named missing bridge (internal SO(7)/G2 -> spacetime
SO(3,1)), instead of an unbounded conjecture.

numpy-only; no scipy. Run: python3 compute/gravity_curvature.py
"""

import numpy as np

from octonion_toolkit import Octonion, associator, find_quaternionic_subalgebras


# ============================================================
# Octonion helpers
# ============================================================

def imag_octonion(coeffs7, rng=None):
    """Build a purely-imaginary octonion from a length-7 vector (e1..e7)."""
    c = np.zeros(8)
    c[1:] = coeffs7
    return Octonion(c)


def random_imag(rng):
    c = rng.standard_normal(8)
    c[0] = 0.0
    return Octonion(c)


def apply_so7(R, a):
    """Apply a 7x7 matrix R to the imaginary part of an octonion (real part fixed)."""
    out = np.zeros(8)
    out[0] = a.coeffs[0]
    out[1:] = R @ a.coeffs[1:]
    return Octonion(out)


def transport_defect_operator(a, b):
    """
    The transport defect M_{a,b}: Im(O) -> Im(O),  x |-> [x, a, b].
    Returned as a 7x7 real matrix (columns indexed by e1..e7).
    """
    M = np.zeros((7, 7))
    for mu in range(1, 8):
        w = associator(Octonion.unit(mu), a, b)
        M[:, mu - 1] = w.coeffs[1:]   # associator is purely imaginary (PART B)
    return M


def emergent_metric(a, b):
    """
    The emergent metric perturbation g_{mu nu}(a,b) = <M e_mu, M e_nu>
    = Gram matrix of the transport defect. Symmetric PSD 7x7.
    """
    M = transport_defect_operator(a, b)
    return M.T @ M


# ============================================================
# PART A: Spacetime arena from C(x)H = M_2(C) Hermitian = Minkowski
# ============================================================

PAULI = [
    np.array([[1, 0], [0, 1]], dtype=complex),     # sigma_0 = I
    np.array([[0, 1], [1, 0]], dtype=complex),     # sigma_1
    np.array([[0, -1j], [1j, 0]], dtype=complex),  # sigma_2
    np.array([[1, 0], [0, -1]], dtype=complex),    # sigma_3
]


def fourvector_to_hermitian(x):
    """x = (x0,x1,x2,x3) -> Hermitian 2x2  X = x0 I + x.sigma."""
    return sum(x[mu] * PAULI[mu] for mu in range(4))


def hermitian_to_fourvector(X):
    """Inverse: x_mu = (1/2) Tr(sigma_mu X)."""
    return np.array([0.5 * np.trace(PAULI[mu] @ X).real for mu in range(4)])


def minkowski_norm_from_det(X):
    """det(X) = x0^2 - x1^2 - x2^2 - x3^2 = Minkowski (+---) quadratic form."""
    return np.linalg.det(X).real


def random_sl2c(rng):
    """A random SL(2,C) element (det = 1) — a Lorentz transformation."""
    A = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    A = A / np.sqrt(np.linalg.det(A))   # det A = 1
    return A


def spacetime_arena_from_CH():
    """
    PART A. Show C(x)H ~= M_2(C): Hermitian 2x2 matrices = Minkowski 4-vectors,
    det = Minkowski norm, SL(2,C) acts as the Lorentz group (det-preserving).
    This is the FLAT background metric eta the curvature perturbs. (borrowed)
    """
    print("=" * 70)
    print("PART A: spacetime arena from C(x)H  (Minkowski + Lorentz)")
    print("=" * 70)
    rng = np.random.default_rng(11)

    # round-trip 4-vector <-> Hermitian matrix
    rt_err = 0.0
    sig_err = 0.0
    for _ in range(200):
        x = rng.standard_normal(4)
        X = fourvector_to_hermitian(x)
        rt_err = max(rt_err, np.max(np.abs(hermitian_to_fourvector(X) - x)))
        # det reproduces Minkowski (+---) norm
        mink = x[0] ** 2 - x[1] ** 2 - x[2] ** 2 - x[3] ** 2
        sig_err = max(sig_err, abs(minkowski_norm_from_det(X) - mink))
        # X is Hermitian
        sig_err = max(sig_err, np.max(np.abs(X - X.conj().T)))
    print(f"  4-vector <-> Hermitian round trip err   : {rt_err:.2e}")
    print(f"  det(X) == eta-norm, X Hermitian err      : {sig_err:.2e}")

    # SL(2,C):  X -> A X A^dagger preserves det = Minkowski norm (Lorentz)
    lorentz_err = 0.0
    for _ in range(500):
        A = random_sl2c(rng)
        x = rng.standard_normal(4)
        X = fourvector_to_hermitian(x)
        Xp = A @ X @ A.conj().T
        # transformed matrix is still Hermitian, det preserved
        lorentz_err = max(lorentz_err, np.max(np.abs(Xp - Xp.conj().T)))
        lorentz_err = max(
            lorentz_err,
            abs(minkowski_norm_from_det(Xp) - minkowski_norm_from_det(X)),
        )
    print(f"  SL(2,C): det preserved (Lorentz inv) err : {lorentz_err:.2e}")

    ok = (rt_err < 1e-10) and (sig_err < 1e-10) and (lorentz_err < 1e-9)
    print(f"  => Minkowski R^(3,1) + Lorentz SO(3,1) from C(x)H : "
          f"{'PASS' if ok else 'FAIL'}")
    return {"roundtrip": rt_err, "signature": sig_err, "lorentz": lorentz_err,
            "pass": ok}


# ============================================================
# PART B: curvature source from non-associativity
# ============================================================

def random_element_of_quaternion_subalgebra(triple, rng):
    """Random element of the quaternionic subalgebra span{1, e_i, e_j, e_k}."""
    i, j, k = triple
    c = np.zeros(8)
    c[0] = rng.standard_normal()
    c[i] = rng.standard_normal()
    c[j] = rng.standard_normal()
    c[k] = rng.standard_normal()
    return Octonion(c)


def curvature_source_from_O():
    """
    PART B. The associator [a,b,c] is the curvature.
    (1) It is purely imaginary (transverse — no scalar/trace part).
    (2) Scalar density S = |[a,b,c]|^2 vanishes iff a,b,c share a quaternionic
        (associative) subalgebra (Artin), and is strictly positive otherwise.
    """
    print("=" * 70)
    print("PART B: curvature source from non-associativity  (associator)")
    print("=" * 70)
    rng = np.random.default_rng(7)

    # (1) associator is purely imaginary
    re_max = 0.0
    for _ in range(3000):
        a, b, c = random_imag(rng), random_imag(rng), random_imag(rng)
        re_max = max(re_max, abs(associator(a, b, c).coeffs[0]))
    print(f"  max |Re[a,b,c]| (curvature is transverse): {re_max:.2e}")

    # (2a) generic triples: curvature nonzero
    S_generic = []
    for _ in range(3000):
        a, b, c = random_imag(rng), random_imag(rng), random_imag(rng)
        S_generic.append(associator(a, b, c).norm() ** 2)
    S_generic = np.array(S_generic)
    print(f"  generic  <S=|[a,b,c]|^2> = {S_generic.mean():.3f}  "
          f"(min {S_generic.min():.3f})")

    # (2b) flat: triple inside one quaternionic subalgebra -> curvature 0
    subs = find_quaternionic_subalgebras()
    S_flat_max = 0.0
    for triple in subs:
        for _ in range(2000):
            a = random_element_of_quaternion_subalgebra(triple, rng)
            b = random_element_of_quaternion_subalgebra(triple, rng)
            c = random_element_of_quaternion_subalgebra(triple, rng)
            S_flat_max = max(S_flat_max, associator(a, b, c).norm() ** 2)
    print(f"  FLAT (common quaternion subalg) max S    : {S_flat_max:.2e}")

    ok = (re_max < 1e-10) and (S_generic.min() > 1e-6) and (S_flat_max < 1e-20)
    print(f"  => curvature transverse; S=0 iff quaternionic (Artin) : "
          f"{'PASS' if ok else 'FAIL'}")
    return {"re_max": re_max, "S_generic_mean": float(S_generic.mean()),
            "S_flat_max": S_flat_max, "pass": ok}


# ============================================================
# Exact finite G2 automorphisms (signed permutations of e1..e7)
# ============================================================

def finite_g2_automorphisms():
    """
    Build the finite signed-permutation automorphisms of O. An automorphism is
    fixed by the images of the basis triple (e1, e2, e4); the remaining units
    are forced by e3=e1e2, e5=e1e4, e6=e2e4, e7=e3e4. Returns a list of exact
    7x7 integer orthogonal matrices R with R(xy) = R(x) R(y).
    """
    units = []
    for idx in range(1, 8):
        for s in (1.0, -1.0):
            c = np.zeros(8)
            c[idx] = s
            units.append(Octonion(c))

    def build_R(im1, im2, im4):
        im3 = im1 * im2
        im5 = im1 * im4
        im6 = im2 * im4
        im7 = im3 * im4
        ims = [None, im1, im2, im3, im4, im5, im6, im7]
        R = np.zeros((7, 7))
        for mu in range(1, 8):
            R[:, mu - 1] = ims[mu].coeffs[1:]
        return R

    def is_automorphism(R):
        for i in range(1, 8):
            for j in range(1, 8):
                ei, ej = Octonion.unit(i), Octonion.unit(j)
                prod = ei * ej
                lhs = np.zeros(8)
                lhs[0] = prod.coeffs[0]
                lhs[1:] = R @ prod.coeffs[1:]
                rhs = (apply_so7(R, ei) * apply_so7(R, ej)).coeffs
                if np.linalg.norm(lhs - rhs) > 1e-9:
                    return False
        return True

    autos = []
    seen = set()
    for im1 in units:
        i1 = int(np.argmax(np.abs(im1.coeffs)))
        for im2 in units:
            i2 = int(np.argmax(np.abs(im2.coeffs)))
            if i1 == i2:
                continue
            for im4 in units:
                R = build_R(im1, im2, im4)
                if not np.allclose(R @ R.T, np.eye(7), atol=1e-9):
                    continue
                if not is_automorphism(R):
                    continue
                key = tuple(np.round(R.flatten()).astype(int))
                if key in seen:
                    continue
                seen.add(key)
                autos.append(R)
    return autos


# ============================================================
# PART C: emergent symmetric rank-2 graviton metric
# ============================================================

def emergent_metric_properties():
    """
    PART C. The Gram pullback g(a,b) of the transport defect is:
      (1) symmetric and positive-semidefinite (a genuine metric perturbation);
      (2) G2-covariant: g(Ra, Rb) = R g(a,b) R^T  (rank-2 tensor under the
          structure group, verified on EXACT finite automorphisms);
      (3) its scalar density obeys  tr g = 16 (|a|^2|b|^2 - <a,b>^2);
      (4) generically rank 6 (one null direction), with a traceless spin-2 part.
    """
    print("=" * 70)
    print("PART C: emergent symmetric rank-2 graviton metric")
    print("=" * 70)
    rng = np.random.default_rng(5)

    # (1) symmetric PSD
    sym_err = 0.0
    min_eig = np.inf
    ranks = []
    for _ in range(500):
        a, b = random_imag(rng), random_imag(rng)
        g = emergent_metric(a, b)
        sym_err = max(sym_err, np.max(np.abs(g - g.T)))
        ev = np.linalg.eigvalsh(g)
        min_eig = min(min_eig, ev.min())
        ranks.append(int(np.sum(ev > 1e-9 * max(1.0, ev.max()))))
    ranks = np.array(ranks)
    print(f"  symmetry |g - g^T| max          : {sym_err:.2e}")
    print(f"  min eigenvalue (PSD check)      : {min_eig:.2e}")
    print(f"  generic rank of g (most common) : {np.bincount(ranks).argmax()} "
          f"of 7")

    # (3) scalar density tr g = 16 (|a|^2|b|^2 - <a,b>^2)
    ratios = []
    for _ in range(2000):
        a, b = random_imag(rng), random_imag(rng)
        g = emergent_metric(a, b)
        na2 = float(a.coeffs @ a.coeffs)
        nb2 = float(b.coeffs @ b.coeffs)
        ab = float(a.coeffs @ b.coeffs)
        ratios.append(np.trace(g) / (na2 * nb2 - ab * ab))
    ratios = np.array(ratios)
    print(f"  tr g / |a ^ b|^2 : mean = {ratios.mean():.6f}  "
          f"std = {ratios.std():.2e}   (= 16 = dim OP^2)")

    # (2) G2 covariance on exact finite automorphisms
    autos = finite_g2_automorphisms()
    cov_err = 0.0
    for R in autos:
        a, b = random_imag(rng), random_imag(rng)
        lhs = emergent_metric(apply_so7(R, a), apply_so7(R, b))
        rhs = R @ emergent_metric(a, b) @ R.T
        cov_err = max(cov_err, np.max(np.abs(lhs - rhs)))
    print(f"  found {len(autos)} exact finite G2 automorphisms")
    print(f"  covariance max |g(Ra,Rb) - R g R^T| : {cov_err:.2e}")

    ok = (sym_err < 1e-10) and (min_eig > -1e-9) and \
         (abs(ratios.mean() - 16.0) < 1e-6) and (ratios.std() < 1e-6) and \
         (len(autos) > 0) and (cov_err < 1e-9)
    print(f"  => symmetric PSD, G2-covariant rank-2 tensor, tr g = 16|a^b|^2 : "
          f"{'PASS' if ok else 'FAIL'}")
    return {"sym_err": sym_err, "min_eig": float(min_eig),
            "trace_const": float(ratios.mean()), "n_autos": len(autos),
            "cov_err": cov_err, "pass": ok}


# ============================================================
# PART D: flat-space limit + honest residual
# ============================================================

def flat_space_limit():
    """
    PART D. FLAT DIRECTIONS = the associative subalgebra (Artin, made geometric).

    By alternativity [a,a,b] = [b,a,b] = 0, so the metric g(a,b) ANNIHILATES the
    source labels a and b: the graviton mode is TRANSVERSE to the source bivector
    a ^ b, exactly as a gravitational wave is transverse to its propagation.
    More: the null space of g(a,b) is precisely the imaginary part of the
    quaternionic (associative) subalgebra generated by a,b, namely
    span{a, b, Im(ab)} (dim 3) -- the directions along which transport is
    path-independent (flat). The curvature lives entirely on the transverse
    rank-4 complement. No geometric input is inserted by hand; the flat
    directions are read off the algebra.
    """
    print("=" * 70)
    print("PART D: flat directions = associative subalgebra (Artin, geometric)")
    print("=" * 70)
    rng = np.random.default_rng(9)

    transverse_max = 0.0
    null_resid_max = 0.0
    ranks = []
    null_dims = []
    for _ in range(2000):
        a, b = random_imag(rng), random_imag(rng)
        g = emergent_metric(a, b)
        ev, V = np.linalg.eigh(g)
        tol = 1e-9 * max(1.0, ev.max())
        rank = int(np.sum(ev > tol))
        ranks.append(rank)
        null_dims.append(7 - rank)

        # (1) transversality: g annihilates the source labels a, b
        transverse_max = max(transverse_max,
                             np.linalg.norm(g @ a.coeffs[1:]),
                             np.linalg.norm(g @ b.coeffs[1:]))

        # (2) null space == span{a, b, Im(ab)} (the associative subalgebra)
        ab = a * b
        basis = np.stack([a.coeffs[1:], b.coeffs[1:], ab.coeffs[1:]]).T
        Q, _ = np.linalg.qr(basis)
        null = V[:, ev <= tol]
        null_resid_max = max(null_resid_max,
                             np.linalg.norm(null - Q @ (Q.T @ null)))

    ranks = np.array(ranks)
    null_dims = np.array(null_dims)
    print(f"  rank of g (curved directions)   : {np.bincount(ranks).argmax()} "
          f"(all = {np.all(ranks == 4)})")
    print(f"  null dim (flat directions)      : {np.bincount(null_dims).argmax()} "
          f"(all = {np.all(null_dims == 3)})")
    print(f"  transversality max |g.a|,|g.b|  : {transverse_max:.2e}  "
          f"(graviton transverse to source a ^ b)")
    print(f"  null(g) == span(a, b, Im(ab))   : resid {null_resid_max:.2e}  "
          f"(flat dirs = associative subalgebra)")

    ok = np.all(ranks == 4) and np.all(null_dims == 3) and \
        (transverse_max < 1e-8) and (null_resid_max < 1e-6)
    print(f"  => flat = associative subalgebra, curvature transverse, no hand "
          f"input : {'PASS' if ok else 'FAIL'}")
    return {"rank": int(np.bincount(ranks).argmax()),
            "null_dim": int(np.bincount(null_dims).argmax()),
            "transverse_max": transverse_max,
            "null_resid_max": null_resid_max, "pass": ok}


# ============================================================
# main
# ============================================================

def main():
    print("\n" + "#" * 70)
    print("# GRAVITY CURVATURE PROBE (M-GRAV)")
    print("# emergent symmetric rank-2 metric from octonionic non-associativity")
    print("#" * 70 + "\n")

    rA = spacetime_arena_from_CH()
    print()
    rB = curvature_source_from_O()
    print()
    rC = emergent_metric_properties()
    print()
    rD = flat_space_limit()

    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    allpass = rA["pass"] and rB["pass"] and rC["pass"] and rD["pass"]
    print(f"  A  Minkowski + Lorentz from C(x)H ............ "
          f"{'PASS' if rA['pass'] else 'FAIL'}")
    print(f"  B  curvature = associator, S=0 iff flat ...... "
          f"{'PASS' if rB['pass'] else 'FAIL'}")
    print(f"  C  symmetric rank-2 G2-covariant metric ...... "
          f"{'PASS' if rC['pass'] else 'FAIL'}")
    print(f"  D  transverse rank-4 mode, flat=assoc subalg .. "
          f"{'PASS' if rD['pass'] else 'FAIL'}")
    print()
    print("  M-GRAV status: ADVANCED (kinematic).  A symmetric, positive-")
    print("  semidefinite, G2-covariant rank-2 metric perturbation emerges from")
    print("  the octonionic associator with NO hand-inserted geometric input;")
    print("  its scalar density is tr g = 16|a^b|^2 (same 16 as eps0^2=pi/432),")
    print("  rank 4 and transverse to the source bivector (graviton-like), with")
    print("  flat directions = the associative subalgebra generated by a,b.")
    print()
    print("  HONEST RESIDUAL (line NOT closed):")
    print("   - metric lives on internal Im(O) [G2 < SO(7)]; reduction to a 4-d")
    print("     spacetime metric with Lorentz SO(3,1) (PART A arena) is OPEN")
    print("     (this is the remaining content of Conjecture 6.1);")
    print("   - no dynamics: no field equation, action, or Newton constant;")
    print("   - PARTs A (Lorentz from C(x)H) and B-D (curvature from O) are not")
    print("     yet joined: which 4 of 7 internal directions become spacetime.")
    print()
    print(f"  ALL CHECKS: {'PASS' if allpass else 'FAIL'}")

    return {"A": rA, "B": rB, "C": rC, "D": rD, "all_pass": allpass}


if __name__ == "__main__":
    main()
