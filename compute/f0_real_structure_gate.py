"""
PHASE 1.2 PREREQUISITE — the real-structure DICHOTOMY that order-zero forces,
and the associative (A (x) A^o) resolution.
=============================================================================

Why this module exists
----------------------
f0_spectral_triple_gate.py (Phase 1.1) assembled the naive finite triple and
flagged its HEADLINE obstruction: order-zero [a, b^o] = 0 fails because, for the
octonions, it literally evaluates the associator. That gate, however, contained
a hidden inconsistency it did not name: it checked the KO-dimension-6 signs with
J = complex CONJUGATION, but it checked order-zero against actual RIGHT
multiplication R_b. Those are TWO DIFFERENT real structures. A spectral triple
has only ONE J, and EVERY axiom (KO signs, order-zero, order-one) must hold for
that SAME J. This module closes the gap by testing both axioms against each
candidate J and reporting what a single J can and cannot do.

The result is a clean dichotomy plus its standard resolution -- both computed,
neither asserted by hand.

What is tested (all numbers come out of explicit 8x8 / 4x4 matrices)
-------------------------------------------------------------------
[A] J = complex conjugation  (the KO-dim-6 choice, B = I).
    For real left-multiplications L_a one has J L_a J^-1 = conj(L_a) = L_a, so
    the OPPOSITE algebra acts IDENTICALLY to A. Order-zero then collapses to
    [A, A] = 0: A must be COMMUTATIVE. Verified: the quaternion left-algebra
    L(H) (noncommutative) FAILS order-zero (~14), while the complex line L(C)
    (commutative) holds (~1e-16). So with the KO-6 real structure the largest
    order-zero-compatible algebra on one brick is ABELIAN -- no SU(2), no SU(3).

[B] J = octonion conjugation  (kappa . conj, B = diag(1,-1,...,-1)).
    Here J L_a J^-1 = -R_a: J implements genuine RIGHT multiplication, so
    order-zero becomes the associator and HOLDS on an associative bimodule (the
    quaternion sub-bimodule, ~1e-15) while a noncommutative algebra is allowed.
    BUT this J destroys the grading: J gamma J^-1 is NOT +-gamma (it equals
    -0.5 gamma, residual ~2), so the KO-dimension is undefined -- chirality is
    lost.

[C] THE DICHOTOMY. On a single irreducible octonion brick C^8 = C (x) O no
    single real structure J gives BOTH KO-dimension 6 AND a noncommutative
    order-zero algebra. The two requirements pull J in incompatible directions
    (conjugation vs octonion-conjugation). This is the SHARP form of the
    Phase-1.1 order-zero obstruction.

[D] THE RESOLUTION (standard Connes route, computed). Stop forcing the octonions
    to BE the order-zero algebra. Let an associative algebra A act on A (x) A^o:
    left multiplication and right multiplication on a matrix algebra COMMUTE
    regardless of how noncommutative A is, so order-zero holds BY CONSTRUCTION
    (residual exactly 0) for a genuinely nonabelian A (here A = H, ||[i,j]|| = 2).
    The octonions then GRADE the module (they supply gamma8 and the charges),
    they do not supply the order-zero *-algebra. This is exactly how Connes'
    Standard Model evades the associator.

Verdict / where this leaves F0
------------------------------
This neither closes nor advances F0's Bayes credit. It converts the Phase-1.1
order-zero FAIL into a precise statement (the real-structure dichotomy) and names
the concrete rebuild it demands: A = C (+) H (+) M_3(C) acting on A (x) A^o, with
the octonion brick relegated to grading/charges. Two open bridges remain before a
spectral action can be written -- (i) carry out that associative rebuild as a
genuine product triple that RESTORES KO-dim 6, and (ii) embed the chirality-even
Jordan Yukawa in the real-structure (Majorana) sector so the finite KO-dimension
does not drop from 6 to 4 (the second Phase-1.1 tension). Until both are done
eps0^2 = pi/432 stays GEOMETRIC and open; nothing here promotes it.

No scipy. Reuses octonion_toolkit and spectral_action (L/R mult, grading gamma).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_real_structure_gate.py
"""

import numpy as np

from spectral_action import (
    left_mult_matrix,
    right_mult_matrix,
    grading_gamma,
)


# --------------------------------------------------------------------------
# Octonion left/right multiplication on C^8 (vectors a, b are 8-component).
# --------------------------------------------------------------------------
def L_oct(a):
    """Left multiplication x -> a x, 8x8 complex."""
    M = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        if a[i] != 0.0:
            M = M + a[i] * left_mult_matrix(i)
    return M


def R_oct(b):
    """Right multiplication x -> x b, 8x8 complex."""
    M = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        if b[i] != 0.0:
            M = M + b[i] * right_mult_matrix(i)
    return M


# Octonion conjugation kappa(e_0)=e_0, kappa(e_i)=-e_i (i>=1) as an 8x8 matrix.
KAPPA = np.diag([1.0] + [-1.0] * 7).astype(complex)


# --------------------------------------------------------------------------
# [A] J = complex conjugation: opposite algebra equals A -> order-zero needs
#     commutativity.
# --------------------------------------------------------------------------
def opposite_equals_algebra_residual(n_samples, rng):
    """max || J L_a J^-1 - L_a || for J = conj (B = I).  conj(L_a) = L_a for real a."""
    worst = 0.0
    for _ in range(n_samples):
        a = rng.standard_normal(8)
        La = L_oct(a)
        worst = max(worst, float(np.max(np.abs(np.conjugate(La) - La))))
    return worst


def order_zero_conj_residual(index_set, n_samples, rng):
    """max ||[L_a, J L_b J^-1]|| with J = conj, i.e. [L_a, conj(L_b)] = [L_a, L_b]
    for real a, b supported on index_set.  Nonzero exactly when L(index_set) is
    noncommutative."""
    worst = 0.0
    idx = list(index_set)
    for _ in range(n_samples):
        a = np.zeros(8)
        b = np.zeros(8)
        a[idx] = rng.standard_normal(len(idx))
        b[idx] = rng.standard_normal(len(idx))
        La, Lb = L_oct(a), L_oct(b)
        c = La @ np.conjugate(Lb) - np.conjugate(Lb) @ La
        worst = max(worst, float(np.max(np.abs(c))))
    return worst


# --------------------------------------------------------------------------
# [B] J = octonion conjugation: implements right multiplication.
# --------------------------------------------------------------------------
def kappa_implements_right_residual():
    """max || KAPPA L_i KAPPA + R_i ||  (the identity KAPPA L_i KAPPA = -R_i,
    i.e. J L_a J^-1 = -R_a is genuine right multiplication)."""
    worst = 0.0
    for i in range(1, 8):
        lhs = KAPPA @ left_mult_matrix(i).astype(complex) @ KAPPA
        worst = max(worst, float(np.max(np.abs(lhs + right_mult_matrix(i)))))
    return worst


def order_zero_kappa_residual(index_set, n_samples, rng, mod):
    """max ||[L_a, R_b]|| (= associator) over a, b on index_set, on the first
    `mod` octonion coordinates (true sub-bimodule when mod matches the subalgebra)."""
    worst = 0.0
    idx = list(index_set)
    for _ in range(n_samples):
        a = np.zeros(8)
        b = np.zeros(8)
        a[idx] = rng.standard_normal(len(idx))
        b[idx] = rng.standard_normal(len(idx))
        c = (L_oct(a) @ R_oct(b) - R_oct(b) @ L_oct(a))[:mod, :mod]
        worst = max(worst, float(np.max(np.abs(c))))
    return worst


def kappa_grading_compatibility(g8):
    """For J = KAPPA . conj, return (eps, ratio, resid) where J^2 = eps I and
    J gamma J^-1 = ratio * gamma (ratio is a clean +-1 only if resid ~ 0)."""
    J2 = KAPPA @ np.conjugate(KAPPA)  # = KAPPA^2 = I
    eps = 1.0 if np.allclose(J2, np.eye(8)) else (
        -1.0 if np.allclose(J2, -np.eye(8)) else float("nan"))
    JgJ = KAPPA @ np.conjugate(g8) @ KAPPA
    ratio = (np.vdot(g8.reshape(-1), JgJ.reshape(-1))
             / np.vdot(g8.reshape(-1), g8.reshape(-1))).real
    resid = float(min(np.max(np.abs(JgJ - g8)), np.max(np.abs(JgJ + g8))))
    return eps, ratio, resid


# --------------------------------------------------------------------------
# [D] Resolution: associative A on A (x) A^o, order-zero by left-right commute.
# --------------------------------------------------------------------------
def quaternion_units():
    """1, i, j, k as 2x2 complex matrices (i*Pauli)."""
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return [np.eye(2, dtype=complex), 1j * sx, 1j * sy, 1j * sz]


def left_on_M2(q):
    """q acting on vec(M_2) = C^4 by M -> q M  (left regular representation)."""
    return np.kron(q, np.eye(2, dtype=complex))


def right_on_M2(q):
    """q acting on vec(M_2) = C^4 by M -> M q  (the opposite / right action)."""
    return np.kron(np.eye(2, dtype=complex), q.T)


def bimodule_order_zero_residual():
    """max ||[a_L, b_R]|| over the quaternion units: left and right multiplication
    on a matrix algebra commute, so this is exactly 0 even though A is nonabelian."""
    quat = quaternion_units()
    worst = 0.0
    for qa in quat:
        for qb in quat:
            c = left_on_M2(qa) @ right_on_M2(qb) - right_on_M2(qb) @ left_on_M2(qa)
            worst = max(worst, float(np.max(np.abs(c))))
    return worst


def algebra_noncommutativity():
    """||[i_L, j_L]|| -- witnesses that A acts genuinely nonabelianly."""
    quat = quaternion_units()
    c = (left_on_M2(quat[1]) @ left_on_M2(quat[2])
         - left_on_M2(quat[2]) @ left_on_M2(quat[1]))
    return float(np.max(np.abs(c)))


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(7)
    g8 = grading_gamma()

    print("=" * 78)
    print(" PHASE 1.2 PREREQUISITE — the real-structure dichotomy that order-zero")
    print(" forces on the octonion brick, and the (A (x) A^o) resolution.")
    print("=" * 78)

    # ---- [A] J = complex conjugation ------------------------------------
    opp = opposite_equals_algebra_residual(200, rng)
    o0_quat_conj = order_zero_conj_residual(range(4), 200, rng)   # L(H), noncommutative
    o0_cline_conj = order_zero_conj_residual(range(2), 200, rng)  # L(C), commutative
    print("\n[A] J = COMPLEX CONJUGATION  (the KO-dim-6 real structure, B = I)")
    print(f"    || J L_a J^-1 - L_a ||         : {opp:.3e}  => opposite algebra = A")
    print(f"    order-zero on L(H) (nonabelian): {o0_quat_conj:.3e}  FAILS")
    print(f"    order-zero on L(C) (abelian)   : {o0_cline_conj:.3e}  holds")
    print("    => with the KO-6 J, order-zero forces A COMMUTATIVE (no SU(2)/SU(3)).")

    # ---- [B] J = octonion conjugation -----------------------------------
    kap = kappa_implements_right_residual()
    o0_full_kappa = order_zero_kappa_residual(range(8), 200, rng, mod=8)  # full O
    o0_quat_kappa = order_zero_kappa_residual(range(4), 200, rng, mod=4)  # H bimodule
    eps_k, ratio_k, resid_k = kappa_grading_compatibility(g8)
    ko_kappa = 6 if (abs(eps_k - 1) < 1e-9 and abs(ratio_k + 1) < 1e-6
                     and resid_k < 1e-9) else None
    print("\n[B] J = OCTONION CONJUGATION  (kappa . conj, B = diag(1,-1,...,-1))")
    print(f"    || KAPPA L_i KAPPA + R_i ||    : {kap:.3e}  => J L_a J^-1 = -R_a (right mult)")
    print(f"    order-zero on full O           : {o0_full_kappa:.3e}  FAILS (associator)")
    print(f"    order-zero on H bimodule       : {o0_quat_kappa:.3e}  holds (associative)")
    print(f"    J^2 = {eps_k:+.0f} I ;  J gamma J^-1 = {ratio_k:+.3f} gamma  "
          f"(clean +-1? resid = {resid_k:.3e})")
    print(f"    => grading is NOT J-compatible: KO-dimension = {ko_kappa} (chirality lost).")

    # ---- [C] dichotomy --------------------------------------------------
    print("\n[C] DICHOTOMY  (single irreducible octonion brick C^8)")
    print("    J = conj         : KO-dim 6 YES, order-zero => A abelian.")
    print("    J = kappa . conj : order-zero noncommutative YES, KO-dim undefined.")
    print("    => NO single real structure gives BOTH KO-6 AND a noncommutative")
    print("       order-zero algebra on one brick. (Sharp form of the Phase-1.1 fail.)")

    # ---- [D] resolution -------------------------------------------------
    o0_bimod = bimodule_order_zero_residual()
    nc = algebra_noncommutativity()
    print("\n[D] RESOLUTION  A acting on  A (x) A^o  (standard Connes route)")
    print(f"    order-zero [a_L, b_R] for A = H : {o0_bimod:.3e}  holds BY left-right commute")
    print(f"    A genuinely nonabelian: ||[i_L,j_L]|| = {nc:.3f}")
    print("    => order-zero is RECOVERED for a noncommutative algebra once the")
    print("       octonions GRADE the module (gamma8, charges) instead of being the")
    print("       order-zero *-algebra.  Rebuild: A = C (+) H (+) M_3(C) on A (x) A^o.")

    # ---- verdict --------------------------------------------------------
    print("\n[V] VERDICT")
    print("    The Phase-1.1 order-zero FAIL is now a precise dichotomy, and its fix")
    print("    is named (associative algebra on A (x) A^o; octonions grade only).")
    print("    OPEN BRIDGES before a spectral action: (i) carry out that rebuild as a")
    print("    product triple that RESTORES KO-dim 6; (ii) embed the chirality-even")
    print("    Jordan Yukawa in the real-structure sector so finite KO-dim stays 6,")
    print("    not 4.  Moves NO Bayes credit: F0 stays GEOMETRIC/open; eps0^2 = pi/432")
    print("    is not promoted.")
    print("=" * 78)

    # ---- stable assertions (audit.py ignores the return value) ----------
    # [A] J = conj makes the opposite algebra coincide with A, so order-zero
    #     forces commutativity:
    assert opp < 1e-12, "J=conj opposite algebra no longer equals A"
    assert o0_quat_conj > 1.0, "L(H) unexpectedly satisfied order-zero under J=conj"
    assert o0_cline_conj < 1e-9, "L(C) failed order-zero under J=conj"
    # [B] J = kappa.conj implements right multiplication; order-zero is then the
    #     associator (fails on O, holds on the quaternion bimodule) but the
    #     grading is no longer J-compatible:
    assert kap < 1e-12, "KAPPA L_i KAPPA = -R_i identity broken"
    assert o0_full_kappa > 1.0, "associator unexpectedly vanished on full O"
    assert o0_quat_kappa < 1e-9, "order-zero failed on the quaternion bimodule"
    assert abs(eps_k - 1.0) < 1e-9, "J=kappa.conj is not J^2=+I"
    assert resid_k > 1e-6 and ko_kappa is None, "kappa.conj unexpectedly graded-compatible"
    # [C]/[D] the resolution: noncommutative order-zero holds on A (x) A^o:
    assert o0_bimod < 1e-12, "left-right multiplication failed to commute on A (x) A^o"
    assert nc > 1e-6, "the resolution algebra collapsed to abelian"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
