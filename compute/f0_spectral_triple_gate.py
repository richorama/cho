"""
PHASE 1.1 GATE — assemble the finite spectral triple (A, H, D; J, gamma) and
test the Connes NCG axioms on the CHO 432-space.
=============================================================================

Why this module exists
----------------------
The gold-standard roadmap (ROBUSTNESS_ACTIONS.md) reduces the whole gap to ONE
make-or-break build: realise the CHO content as a finite real spectral triple
(A, H, D; J, gamma) and run a Connes-Chamseddine spectral action Tr f(D/Lambda).
Criteria 1 (a dynamical principle), 2 (parameters not fitted) and 3 (one
generative object) are all properties of THAT object. Before computing any heat-
kernel coefficient (Phase 1.2) or asking whether pi/432 is the a4/a2 ratio
(Phase 1.3, the decisive experiment), the triple must first EXIST: its operators
must satisfy the spectral-triple axioms. This module is Phase 1.1 — the existence
gate — and it reports the axiom ledger HONESTLY, pass and fail alike.

The pieces (all reused, none invented here)
-------------------------------------------
  * Octonion Clifford spin factor  C^8 = C (x) O, with
        gamma8 = i L_1...L_6     (chirality, gamma8^2 = +1, ko_dimension_chirality)
        J8     = complex conj    (the KO-dim-6 real structure, eps=+1, eps''=-1)
    This is the verified chirality-without-doubling brick (KO-dimension 6).
  * Cross-generation Jordan Yukawa  L_X : Y -> X o Y on J3(O) = R^27
    (spectral_action_432), the algebra-internal mass operator. L_X is self-
    adjoint with the averaging-law spectrum {a,b,c} u {(a+b)/2,...} (each x8).
  * Algebra  A = C (x) H (x) O  acting by octonion left-multiplication L_a on
    the spin factor.

What is ACTUALLY assembled and tested
-------------------------------------
[A] SPIN BRICK. gamma8, J8 -> verify gamma8^2=I, gamma8 Hermitian, and the
    KO-dim-6 signs (eps=+1, eps''=-1). This half is solid.

[B] FINITE YUKAWA AS A DIRAC. L_X is chirality-EVEN (its spectrum is not +-
    symmetric), so it cannot be a Dirac on the 27 by itself. The standard cure
    is particle/antiparticle doubling: on C^27 (+) C^27,
        D_F = [[0, L_X],[L_X, 0]],  gamma_F = diag(I,-I),  J_F = swap o conj.
    Verify D_F self-adjoint, gamma_F-odd, and the doubled factor's KO signs.

[C] PRODUCT TRIPLE. H = C^8 (x) C^54 (dim_R = 864 = 2 x 432, the 432 = 16x27
    A_Weyl (x) J3(O) trace space doubled for chirality). D = gamma8 (x) D_F,
    gamma = gamma8 (x) gamma_F, J = J8 (x) J_F. Verify D=D^dag, gamma^2=I,
    gamma D = -D gamma, J^2=+I. Report the product KO-dimension honestly:
    6 (x) 6 -> 12 = 4 (mod 8), NOT the 6 a single chiral generation needs — the
    first structural tension.

[D] ORDER-ZERO (the headline). The Connes axiom [a, b^o] = 0 (left action
    commutes with the opposite/right action) is, for octonion multiplication,
    exactly the associator:
        [L_a, R_b] x = a(x b) - (a x) b = -[a, x, b].
    Octonions are non-associative, so order-zero FAILS on O (residual ~ O(10)).
    Restricting the ALGEBRA alone to a quaternion subalgebra does NOT fix it
    (residual still ~ O(10)) because the module x still leaves the subalgebra;
    order-zero is recovered only on a genuine associative BIMODULE (algebra AND
    module both quaternionic, residual ~ 1e-15) or on the complex line where
    flexibility a(xa)=(ax)a saves it. Hence A = C(x)H(x)O on the octonion module
    cannot be the *-algebra of a spectral triple as it stands; the consistent
    geometry must use its associative / special-Jordan envelope — the second
    structural tension.

[E] ORDER-ONE. [[D, a], b^o] also fails on O (it presupposes order-zero), and
    holds on the associative subalgebra.

[F] VERDICT. The KO-dim-6 spin brick is a clean half of a spectral triple, but
    the full naive (A, H, D) is NOT yet a consistent finite spectral triple: the
    octonionic algebra violates order-zero (non-associativity) and the Jordan
    Yukawa needs a doubling that pushes the finite KO-dimension to 4 (mod 8).
    Both are KNOWN, repairable obstructions (associative/Jordan envelope; embed
    the Yukawa in the real structure rather than as an extra graded factor), so
    this is NOT the irreparable KILL. It LOCALISES the Phase-1.2 prerequisite and
    moves NO Bayes credit: F0 stays GEOMETRIC and open, eps0^2 = pi/432 is not
    promoted.

This is an OPEN_BRIDGE result under F0: it sharpens exactly what must be built
before a spectral action can be written, and it refuses to pretend the triple
already exists.

No scipy. Reuses octonion_toolkit, spectral_action (gamma8, L/R mult) and
epsilon_weyl_isomorphism (J3(O) structure tensor).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_spectral_triple_gate.py
"""

import numpy as np

from octonion_toolkit import OCT_MULT
from spectral_action import (
    left_mult_matrix,
    right_mult_matrix,
    grading_gamma,
)
from epsilon_weyl_isomorphism import jordan_product_tensor


# --------------------------------------------------------------------------
# Octonion left/right multiplication on C^8 (the spin factor).
# --------------------------------------------------------------------------
def L_oct(a):
    """Left multiplication x -> a x by octonion a (8-vector), 8x8 complex."""
    M = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        if a[i] != 0.0:
            M = M + a[i] * left_mult_matrix(i)
    return M


def R_oct(b):
    """Right multiplication x -> x b by octonion b (8-vector), 8x8 complex."""
    M = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        if b[i] != 0.0:
            M = M + b[i] * right_mult_matrix(i)
    return M


# --------------------------------------------------------------------------
# [A] Spin brick: gamma8, J8, KO-dimension 6.
# --------------------------------------------------------------------------
def spin_brick():
    """Return (gamma8, eps, eps_pp) for the octonion Clifford module C^8.

    J8 = complex conjugation (B = I), so J8^2 = +I (eps = +1) and
    J8 gamma8 J8^-1 = conj(gamma8). eps_pp is the sign in conj(gamma8) = eps_pp gamma8.
    """
    g8 = grading_gamma()
    eps = +1.0  # J8 = conj, B = I  ->  J8^2 = +I
    Jg8J = np.conjugate(g8)  # J8 gamma8 J8^-1 = B conj(gamma8) B = conj(gamma8)
    s = (np.vdot(g8.reshape(-1), Jg8J.reshape(-1))
         / np.vdot(g8.reshape(-1), g8.reshape(-1)))
    return g8, eps, s.real


# --------------------------------------------------------------------------
# [B] Finite Yukawa as a Dirac on the doubled J3(O).
# --------------------------------------------------------------------------
def jordan_left_mult(T, x27):
    """L_X : Y -> X o Y on J3(O) as a 27x27 matrix (X = sum x_i e_i)."""
    return np.einsum("i,kij->kj", x27, T).astype(complex)


def diag_seed(a, b, c):
    """diag(a,b,c) in the 27-coordinate basis (first three coords)."""
    v = np.zeros(27)
    v[0], v[1], v[2] = a, b, c
    return v


def doubled_generation_factor(LX):
    """Particle/antiparticle doubling of L_X into a chirality-odd Dirac.

    Returns (D_F, gamma_F, S) on C^54 = C^27 (+) C^27, with
        D_F = [[0, LX],[LX, 0]],  gamma_F = diag(I,-I),  J_F = S o conj.
    """
    I27 = np.eye(27, dtype=complex)
    Z = np.zeros((27, 27), dtype=complex)
    D_F = np.block([[Z, LX], [LX, Z]])
    gamma_F = np.block([[I27, Z], [Z, -I27]])
    S = np.block([[Z, I27], [I27, Z]])  # antilinear part of J_F: J_F M J_F^-1 = S conj(M) S
    return D_F, gamma_F, S


# --------------------------------------------------------------------------
# [D]/[E] Order-zero (associator) and order-one.
# --------------------------------------------------------------------------
def order_zero_residual(index_set, n_samples, rng, mod=8):
    """max ||[L_a, R_b]|| over random a,b supported on index_set, evaluated on the
    sub-module spanned by the first `mod` octonion units.

    For octonions [L_a, R_b] x = a(x b) - (a x) b = -(associator) [a, x, b], which
    vanishes for ALL module x only when a, x, b lie in a common associative
    subalgebra. Restricting the algebra alone (index_set) is NOT enough if the
    module x still ranges over all of O; the sub-module must be restricted too
    (mod < 8). The first-`mod` coordinate subspace is invariant under L_a, R_b for
    a, b supported there (the quaternion/complex subalgebras are closed), so its
    diagonal block is the genuine restricted commutator.
    """
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


def order_one_residual(D, index_set, n_samples, rng):
    """max ||[[D, pi(a)], rho(b)]|| with pi(a)=L_a (x) I, rho(b)=R_b (x) I.

    Order-one presupposes order-zero; on O it inherits the non-associativity.
    """
    I_gen = np.eye(D.shape[0] // 8, dtype=complex)
    worst = 0.0
    idx = list(index_set)
    for _ in range(n_samples):
        a = np.zeros(8)
        b = np.zeros(8)
        a[idx] = rng.standard_normal(len(idx))
        b[idx] = rng.standard_normal(len(idx))
        pa = np.kron(L_oct(a), I_gen)
        rb = np.kron(R_oct(b), I_gen)
        comm = D @ pa - pa @ D
        o1 = comm @ rb - rb @ comm
        worst = max(worst, float(np.max(np.abs(o1))))
    return worst


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(0)
    I8 = np.eye(8, dtype=complex)

    print("=" * 78)
    print(" PHASE 1.1 GATE — finite spectral triple (A,H,D;J,gamma) on the CHO")
    print(" 432-space, with an HONEST Connes-axiom ledger (pass AND fail).")
    print("=" * 78)

    # ---- [A] spin brick -------------------------------------------------
    g8, eps8, eps8_pp = spin_brick()
    g8_sq_ok = np.allclose(g8 @ g8, I8)
    g8_herm = np.allclose(g8, g8.conj().T)
    ko8 = 6 if (abs(eps8 - 1) < 1e-9 and abs(eps8_pp + 1) < 1e-9) else None
    print("\n[A] SPIN BRICK  C^8 = C (x) O   (octonion Clifford module)")
    print(f"    gamma8^2 = I            : {g8_sq_ok}")
    print(f"    gamma8 Hermitian        : {g8_herm}")
    print(f"    J8 = conj -> eps=+1, eps''={eps8_pp:+.3f}   => KO-dim {ko8} "
          f"(chirality without doubling)")

    # ---- [B] finite Yukawa as a Dirac -----------------------------------
    T = jordan_product_tensor()
    X = diag_seed(1.0, 0.6, 0.3)
    LX = jordan_left_mult(T, X)
    lx_herm = np.allclose(LX, LX.conj().T)
    evX = np.linalg.eigvalsh(LX)
    even_asym = float(np.min(np.abs(np.sort(evX) + np.sort(evX)[::-1])))  # +- symmetry defect
    D_F, gamma_F, S = doubled_generation_factor(LX)
    df_herm = np.allclose(D_F, D_F.conj().T)
    df_odd = np.allclose(gamma_F @ D_F, -D_F @ gamma_F)
    # KO signs of the doubled factor: J_F = S o conj
    JF_gamma = S @ np.conjugate(gamma_F) @ S
    epsF_pp = -1.0 if np.allclose(JF_gamma, -gamma_F) else (
        1.0 if np.allclose(JF_gamma, gamma_F) else float("nan"))
    JF_sq_ok = np.allclose(S @ np.conjugate(S), np.eye(54))
    print("\n[B] FINITE YUKAWA  L_X : Y -> X o Y  on J3(O) (X = diag(1,0.6,0.3))")
    print(f"    L_X self-adjoint        : {lx_herm}")
    print(f"    L_X chirality-EVEN (spectrum not +- symmetric): "
          f"defect ||sort(ev)+rev||_min = {even_asym:.3f}  (>0 => no native grading)")
    print("    -> realise as a Dirac by particle/antiparticle doubling on C^54:")
    print(f"       D_F self-adjoint     : {df_herm}")
    print(f"       gamma_F D_F = -D_F gamma_F : {df_odd}")
    print(f"       J_F^2 = +I           : {JF_sq_ok}    eps''_F = {epsF_pp:+.0f}")

    # ---- [C] product triple ---------------------------------------------
    D = np.kron(g8, D_F)
    gamma = np.kron(g8, gamma_F)
    SS = np.kron(I8, S)  # antilinear part of J = J8 (x) J_F
    D_herm = np.allclose(D, D.conj().T)
    g_sq = np.allclose(gamma @ gamma, np.eye(gamma.shape[0]))
    g_anti = np.allclose(gamma @ D, -D @ gamma)
    J_sq = np.allclose(SS @ np.conjugate(SS), np.eye(SS.shape[0]))
    dimC = D.shape[0]
    ko_prod = (6 + 6) % 8
    print("\n[C] PRODUCT TRIPLE  H = C^8 (x) C^54   (dim_C =", dimC,
          ", dim_R =", 2 * dimC, "= 2 x 432)")
    print(f"    D = gamma8 (x) D_F self-adjoint : {D_herm}")
    print(f"    gamma = gamma8 (x) gamma_F, gamma^2=I : {g_sq}")
    print(f"    gamma D = -D gamma              : {g_anti}")
    print(f"    J = J8 (x) J_F,  J^2 = +I        : {J_sq}")
    print(f"    TENSION 1: KO-dim adds, 6 (x) 6 -> {ko_prod} (mod 8), not the 6 a")
    print(f"               single chiral generation needs (doubling double-counts).")

    # ---- [D] order-zero = associator ------------------------------------
    o0_full = order_zero_residual(range(8), 60, rng, mod=8)        # O on full module
    o0_quat_alg = order_zero_residual(range(4), 60, rng, mod=8)    # H algebra, full module
    o0_quat_bi = order_zero_residual(range(4), 60, rng, mod=4)     # H algebra AND H module
    o0_cline = order_zero_residual(range(2), 60, rng, mod=8)       # C line (flexibility)
    print("\n[D] ORDER-ZERO  [a, b^o] = [L_a, R_b] = -(associator) [a,.,b]")
    print(f"    O algebra, full module   : max = {o0_full:.3e}   FAILS (non-associative)")
    print(f"    H algebra, full module   : max = {o0_quat_alg:.3e}   FAILS too "
          f"(restricting A alone is not enough)")
    print(f"    H algebra AND H module   : max = {o0_quat_bi:.3e}   holds (true bimodule)")
    print(f"    C line, full module      : max = {o0_cline:.3e}   holds (flexibility)")
    print("    => order-zero needs the WHOLE module to be an associative bimodule;")
    print("       A = C(x)H(x)O on the octonion module is NOT a spectral-triple")
    print("       *-algebra -- only its associative/special-Jordan envelope can be.")

    # ---- [E] order-one --------------------------------------------------
    o1_full = order_one_residual(D, range(8), 8, rng)
    print("\n[E] ORDER-ONE  [[D, a], b^o]")
    print(f"    O algebra, full module   : max = {o1_full:.3e}   FAILS (inherits order-zero)")

    # ---- [F] verdict ----------------------------------------------------
    print("\n[F] VERDICT")
    print("    PASS : KO-dim-6 spin brick (gamma8, J8); self-adjoint chirality-odd")
    print("           Dirac D; gamma^2=I; J^2=+I.  The metric/real-structure half")
    print("           of a finite spectral triple is consistent.")
    print("    OPEN : (1) order-zero fails on the non-associative A (associator),")
    print("           repaired only on the associative/Jordan envelope;")
    print("           (2) the Jordan Yukawa needs doubling -> finite KO-dim 4, not 6.")
    print("    => The naive (A,H,D) is NOT yet a consistent finite spectral triple.")
    print("       Both obstructions are known and repairable (NOT the irreparable")
    print("       KILL), so this LOCALISES the Phase-1.2 prerequisite and moves NO")
    print("       Bayes credit: F0 stays GEOMETRIC/open; eps0^2 = pi/432 not promoted.")
    print("=" * 78)

    # ---- stable assertions (audit.py ignores the return value) ----------
    # Solid metric/real-structure facts:
    assert g8_sq_ok and g8_herm, "spin brick gamma8 broken"
    assert ko8 == 6, "octonion factor is not KO-dimension 6"
    assert lx_herm, "L_X is not self-adjoint"
    assert even_asym > 1e-6, "L_X unexpectedly chirality-symmetric"
    assert df_herm and df_odd, "doubled finite Dirac broken"
    assert JF_sq_ok and abs(epsF_pp + 1.0) < 1e-9, "doubled factor KO signs broken"
    assert D_herm and g_sq and g_anti and J_sq, "product triple metric data broken"
    # The honest obstruction: order-zero fails for the octonion algebra (even when
    # restricted to a quaternion subalgebra) on the full module, and is recovered
    # only on a genuine associative bimodule (quaternion algebra AND quaternion
    # module) or on the complex line via flexibility.
    assert o0_full > 1.0, "order-zero unexpectedly held on full O (non-assoc lost?)"
    assert o0_quat_alg > 1.0, "restricting A alone unexpectedly fixed order-zero"
    assert o0_quat_bi < 1e-9, "order-zero failed on the associative quaternion bimodule"
    assert o0_cline < 1e-9, "order-zero failed on the complex line"
    assert o1_full > 1.0, "order-one unexpectedly held on full O"
    # KO addition tension (a stable arithmetic fact about the doubled construction):
    assert ko_prod == 4, "product KO-dimension bookkeeping changed"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
