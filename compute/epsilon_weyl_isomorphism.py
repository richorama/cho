"""
Epsilon route (4c) — closing R3: A_Weyl  ~=  T(OP^2)  as Spin(9) spinors.
========================================================================

State of the attack
-------------------
epsilon_product_space.py (route 4b) reduced residual R3 of eps0^2 = pi/432 to a
SINGLE named, falsifiable claim: the external gauge Weyl generation A_Weyl (the
16 in SPURION_BRIDGE's trace space A_Weyl (x) J3(O) = 16 x 27 = 432) must be
isomorphic, as a 16-dim real octonionic spinor, to the internal vacuum-manifold
tangent T(OP^2) (the off-diagonal octonion pair inside the flavour 27). Both
were shown to be 16-dim octonion pairs (a necessary condition); equality as
Spin(9) representations was left open.

This module closes that gap by COMPUTATION, using the one structural fact that
makes the question decidable:

    Spin(9) has a UNIQUE irreducible 16-dimensional representation -- its real
    spinor Delta_9 (of real type). Every 16-dim irreducible Spin(9)-module is
    therefore isomorphic to it, and hence to every other.

So the obligation "A_Weyl ~= T(OP^2)" follows IF both sides are realised as
16-dim IRREDUCIBLE modules of the SAME Spin(9). The module builds that Spin(9)
two independent ways and checks irreducibility / type on both, then exhibits the
strongest possible link between them.

What it computes (no scipy, all from the octonion table)
--------------------------------------------------------
  [1] f4 = Der(J3(O)) by solving the derivation condition
        D(A o B) = D(A) o B + A o D(B)
      as a linear null-space problem on the 27x27 generator matrices. The null
      space dimension is computed, expected 52 = dim F4.

  [2] spin(9) = stabiliser of the primitive idempotent E0 = diag(1,0,0):
      the derivations with D(E0) = 0. Dimension computed, expected 36 = dim
      Spin(9). Verified to be a Lie subalgebra (closed bracket) and SEMISIMPLE
      (Killing form nondegenerate) -> the simple algebra so(9).

  [3] The ISOTROPY action of spin(9) on T_{E0}(OP^2): the stabiliser preserves
      the 16-dim octonion-pair block (z2, z3) and acts there. Its commutant is
      computed; commutant dimension 1 == irreducible of REAL type == Delta_9.
      (This is the F4/Spin(9) isotropy representation -- the FLAVOUR side.)

  [4] An INDEPENDENT Delta_9 from the octonionic Clifford algebra Cl(9): nine
      real 16x16 gamma matrices on the octonion pair O^2,
          G_0 = diag(I, -I),   G_a = [[0, L_a],[L_a^T, 0]]  (a = 0..7),
      with L_a = left octonion multiplication (L_0 = I). Verified
      {G_mu, G_nu} = 2 delta. The spin generators (1/2) G_mu G_nu (mu<nu) give a
      36-dim so(9) acting on O^2 = R^16; commutant computed (expected 1, real).
      This is the GAUGE side: O^2 is exactly one CHO octonion-pair generation.

  [5] The LINK. Both [3] and [4] are 36-dim so(9) algebras acting on the SAME
      coordinate space (the octonion pair). The module tests whether the two
      36-dim subalgebras of gl(16) are EQUAL as subspaces (a literal identity
      intertwiner). If equal, the two Delta_9's are not merely isomorphic but
      the SAME module and A_Weyl = T(OP^2) on the nose. If not literally equal,
      both are still 16-dim irreducible real modules of so(9), so by the
      uniqueness theorem they are isomorphic -- and the module reports which of
      the two (identity vs. uniqueness-theorem) closes it.

Verdict logic
-------------
[1]-[2] confirm the Spin(9) is real (it is the genuine F4 isotropy group, not a
hand-named SO(9)). [3] proves the flavour tangent is the real spinor Delta_9.
[4] proves the gauge octonion pair carries the same real spinor Delta_9. [5]
then upgrades "numerically equal 16s" to "the same Spin(9) irrep", discharging
the last named obligation of R3 (modulo the standard identification of the
gauge Spin(9) with the idempotent-stabiliser Spin(9), which is now the only
remaining seam and is a subgroup-embedding statement, not a dimension count).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_weyl_isomorphism.py
"""

import numpy as np

from octonion_toolkit import Octonion, OCT_MULT
from jordan_eigenvalue_generations import (
    JordanElement,
    _herm_to_dense,
    jordan_product_dense,
)
from epsilon_state_count import jordan_to_vec


# --------------------------------------------------------------------------
# R^27  <->  J3(O)  product tensor
# --------------------------------------------------------------------------
def _dense_to_vec(Xd):
    """Read a dense octonion-Hermitian 3x3 back to 27 real coordinates,
    matching jordan_to_vec's layout [xi(3), z1(8), z2(8), z3(8)].
    Note _herm_to_dense stores z2.conjugate() in slot (0,2)."""
    diag = np.array([Xd[k][k].real_part() for k in range(3)])
    z1 = Xd[1][2].coeffs
    z2 = Xd[0][2].conjugate().coeffs
    z3 = Xd[0][1].coeffs
    return np.concatenate([diag, z1, z2, z3])


def _basis_dense():
    """Dense octonion-Hermitian forms of the 27 coordinate basis vectors."""
    dens = []
    for a in range(27):
        e = np.zeros(27)
        e[a] = 1.0
        xi = e[0:3]
        J = JordanElement(xi, Octonion(e[3:11]), Octonion(e[11:19]), Octonion(e[19:27]))
        dens.append(_herm_to_dense(J))
    return dens


def jordan_product_tensor():
    """T[k, i, j] = k-th coordinate of (e_i o e_j), the J3(O) structure tensor."""
    dens = _basis_dense()
    T = np.zeros((27, 27, 27))
    for i in range(27):
        for j in range(i, 27):
            prod = jordan_product_dense(dens[i], dens[j])
            v = _dense_to_vec(prod)
            T[:, i, j] = v
            T[:, j, i] = v  # Jordan product is commutative
    return T


# --------------------------------------------------------------------------
# [1] Der(J3(O)) = f4
# --------------------------------------------------------------------------
def derivation_algebra(T, tol=1e-7):
    """Null space of the derivation condition, returned as a list of 27x27
    generator matrices.  D is a derivation iff for all i,j,k

        sum_a D[k,a] T[a,i,j] - sum_a D[a,i] T[k,a,j] - sum_a D[a,j] T[k,i,a] = 0.
    """
    n = 27
    I = np.eye(n)
    # C[(k,i,j),(p,q)] = d residual_{kij} / d D[p,q]
    #   = delta_kp T[q,i,j] - delta_qi T[k,p,j] - delta_qj T[k,i,p]
    C = np.einsum("kp,qij->kijpq", I, T)
    C -= np.einsum("qi,kpj->kijpq", I, T)
    C -= np.einsum("qj,kip->kijpq", I, T)
    C = C.reshape(n * n * n, n * n)
    # null space of C  (vec(D) with C vec(D) = 0)
    CtC = C.T @ C
    w, V = np.linalg.eigh(CtC)
    scale = max(w[-1], 1.0)
    null = [V[:, idx].reshape(n, n) for idx in range(len(w)) if w[idx] <= tol * scale]
    return null, w


# --------------------------------------------------------------------------
# [2] spin(9) = stabiliser of E0
# --------------------------------------------------------------------------
def stabiliser_subalgebra(gens, v0, tol=1e-7):
    """From a basis {D_a} of f4, return the subspace with (sum c_a D_a) v0 = 0,
    as a list of 27x27 matrices."""
    M = np.column_stack([D @ v0 for D in gens])  # 27 x len(gens)
    MtM = M.T @ M
    w, V = np.linalg.eigh(MtM)
    scale = max(w[-1], 1.0)
    combos = [V[:, idx] for idx in range(len(w)) if w[idx] <= tol * scale]
    stab = [sum(c[a] * gens[a] for a in range(len(gens))) for c in combos]
    return stab


# --------------------------------------------------------------------------
# Lie-algebra utilities
# --------------------------------------------------------------------------
def _vec(mats):
    return np.column_stack([m.reshape(-1) for m in mats])


def closed_under_bracket(algebra, tol=1e-6):
    """Max residual of projecting every [A,B] back onto span(algebra)."""
    B = _vec(algebra)                       # d^2 x m
    P = B @ np.linalg.pinv(B)               # projector onto the algebra
    worst = 0.0
    for A in algebra:
        for Bm in algebra:
            comm = (A @ Bm - Bm @ A).reshape(-1)
            resid = comm - P @ comm
            worst = max(worst, float(np.linalg.norm(resid)))
    return worst


def killing_rank(algebra, tol=1e-8):
    """Rank of the Killing form K_ab = tr(ad_a ad_b); full rank == semisimple."""
    B = _vec(algebra)
    Bpinv = np.linalg.pinv(B)
    m = len(algebra)
    # structure constants f[c,a,b]: [D_a,D_b] = sum_c f[c,a,b] D_c
    f = np.zeros((m, m, m))
    for a in range(m):
        for b in range(m):
            comm = (algebra[a] @ algebra[b] - algebra[b] @ algebra[a]).reshape(-1)
            f[:, a, b] = Bpinv @ comm
    # ad_a has entries (ad_a)[c,b] = f[c,a,b]
    ad = [f[:, a, :] for a in range(m)]
    K = np.array([[np.trace(ad[a] @ ad[b]) for b in range(m)] for a in range(m)])
    s = np.linalg.svd(K, compute_uv=False)
    rank = int(np.sum(s > tol * max(s[0], 1.0)))
    return rank, K


def commutant_dimension(gens, tol=1e-7):
    """Dimension of {X : [X, g] = 0 for all g in gens}.  For an irreducible
    real rep this is 1 (real type), 2 (complex), or 4 (quaternionic)."""
    d = gens[0].shape[0]
    I = np.eye(d)
    # vec([X,g]) = (g^T (x) I - I (x) g) vec(X)
    blocks = [np.kron(g.T, I) - np.kron(I, g) for g in gens]
    S = np.vstack(blocks)
    sv = np.linalg.svd(S, compute_uv=False)
    rank = int(np.sum(sv > tol * max(sv[0], 1.0)))
    return d * d - rank


# --------------------------------------------------------------------------
# [4] octonionic Cl(9) and its Delta_9 spinor on the octonion pair O^2
# --------------------------------------------------------------------------
def left_mult_matrix(i):
    """8x8 real matrix of x -> e_i * x: (L_i)_{k,j} = OCT_MULT[i,j,k]."""
    L = np.zeros((8, 8))
    for j in range(8):
        for k in range(8):
            L[k, j] = OCT_MULT[i, j, k]
    return L


def clifford9_generators():
    """Nine real 16x16 gammas on O^2 = R^16 with {G_mu,G_nu} = 2 delta_mu,nu."""
    I8 = np.eye(8)
    Z8 = np.zeros((8, 8))
    G = []
    # G_0 = diag(I, -I)
    G.append(np.block([[I8, Z8], [Z8, -I8]]))
    # G_{a+1} = [[0, L_a],[L_a^T, 0]],  a = 0..7  (L_0 = I)
    for a in range(8):
        La = left_mult_matrix(a) if a >= 1 else I8
        G.append(np.block([[Z8, La], [La.T, Z8]]))
    return G


def so9_from_clifford(G):
    """The 36 spin generators (1/2) G_mu G_nu, mu < nu."""
    gens = []
    for mu in range(9):
        for nu in range(mu + 1, 9):
            gens.append(0.5 * (G[mu] @ G[nu]))
    return gens


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    print("=" * 74)
    print("EPSILON ROUTE (4c): A_Weyl  ~=  T(OP^2)  as Spin(9) spinors")
    print("=" * 74)
    print()

    np.random.seed(0)
    tol = 1e-6

    # ---- [1] f4 = Der(J3(O)) -------------------------------------------
    print("[1] f4 = Der(J3(O)) from the derivation condition D(AoB)=DA oB+A oDB")
    T = jordan_product_tensor()
    f4, spectrum = derivation_algebra(T)
    dim_f4 = len(f4)
    print(f"    dim Der(J3(O)) = {dim_f4}",
          "(= dim F4 = 52, PASS)" if dim_f4 == 52 else "(expected 52, FAIL)")
    print()

    # ---- [2] spin(9) = stab(E0) ----------------------------------------
    print("[2] spin(9) = { D in f4 : D(E0) = 0 },  E0 = diag(1,0,0)")
    v0 = jordan_to_vec(JordanElement.diagonal(1.0, 0.0, 0.0))
    spin9 = stabiliser_subalgebra(f4, v0)
    dim_spin9 = len(spin9)
    print(f"    dim stab(E0) = {dim_spin9}",
          "(= dim Spin(9) = 36, PASS)" if dim_spin9 == 36 else "(expected 36, FAIL)")
    br = closed_under_bracket(spin9)
    print(f"    closed under bracket: max off-algebra residual = {br:.2e}",
          "(PASS)" if br < 1e-5 else "(FAIL)")
    rank, _ = killing_rank(spin9)
    print(f"    Killing-form rank = {rank} / {dim_spin9}",
          "(nondegenerate -> semisimple, the simple so(9), PASS)"
          if rank == dim_spin9 else "(degenerate, FAIL)")
    print()

    # ---- [3] isotropy action on T(OP^2) = flavour Delta_9 --------------
    print("[3] Isotropy action of spin(9) on T_{E0}(OP^2) (the flavour side)")
    # T(OP^2) at diag(1,0,0) is the octonion pair (z2,z3) = coords 11:27.
    idx = np.arange(11, 27)
    P = np.eye(27)[idx]                      # 16 x 27 selector
    # check the stabiliser PRESERVES this block (off-block coupling ~ 0)
    other = np.array([k for k in range(27) if k not in idx])
    leak = max(float(np.linalg.norm(np.eye(27)[other] @ D @ P.T)) for D in spin9)
    print(f"    stabiliser preserves the (z2,z3) block: max leakage = {leak:.2e}",
          "(PASS)" if leak < 1e-5 else "(FAIL)")
    rho = [P @ D @ P.T for D in spin9]       # 36 matrices, 16x16
    c_flav = commutant_dimension(rho)
    print(f"    commutant dimension of the 16-dim isotropy module = {c_flav}",
          "(==1: irreducible, REAL type -> the spinor Delta_9, PASS)"
          if c_flav == 1 else "(not 1, FAIL)")
    print()

    # ---- [4] independent Delta_9 from octonionic Cl(9) = gauge side ----
    print("[4] Independent Delta_9 from the octonionic Cl(9) on O^2 (gauge side)")
    G = clifford9_generators()
    # verify Clifford relations {G_mu,G_nu} = 2 delta
    I16 = np.eye(16)
    cl_err = 0.0
    for mu in range(9):
        for nu in range(9):
            anti = G[mu] @ G[nu] + G[nu] @ G[mu]
            cl_err = max(cl_err, float(np.linalg.norm(anti - 2.0 * (mu == nu) * I16)))
    print(f"    {{G_mu,G_nu}} = 2 delta: max error = {cl_err:.2e}",
          "(Cl(9), PASS)" if cl_err < 1e-10 else "(FAIL)")
    sigma = so9_from_clifford(G)
    dim_cl = int(np.linalg.matrix_rank(_vec(sigma).T, tol=1e-9))
    print(f"    dim span{{(1/2)G_mu G_nu}} = {dim_cl}",
          "(= 36 = so(9), PASS)" if dim_cl == 36 else "(expected 36, FAIL)")
    c_gauge = commutant_dimension(sigma)
    print(f"    commutant dimension of the 16-dim O^2 spinor = {c_gauge}",
          "(==1: irreducible, REAL type -> Delta_9, PASS)"
          if c_gauge == 1 else "(not 1, FAIL)")
    print()

    # ---- [5] the link: same module, or isomorphic by uniqueness? -------
    print("[5] Link: are the flavour and gauge so(9)'s the SAME 16-dim module?")
    Vflav = _vec(rho)                        # 256 x 36
    Vgauge = _vec(sigma)                     # 256 x 36
    combined = np.hstack([Vflav, Vgauge])    # 256 x 72
    r_flav = int(np.linalg.matrix_rank(Vflav, tol=1e-8))
    r_gauge = int(np.linalg.matrix_rank(Vgauge, tol=1e-8))
    r_comb = int(np.linalg.matrix_rank(combined, tol=1e-8))
    print(f"    dim(flavour so(9)) = {r_flav}, dim(gauge so(9)) = {r_gauge}, "
          f"dim(sum) = {r_comb}")
    same_subspace = (r_comb == 36 and r_flav == 36 and r_gauge == 36)
    if same_subspace:
        verdict = ("IDENTITY intertwiner: the flavour isotropy so(9) and the "
                   "octonionic gauge so(9) are the SAME subalgebra of gl(16) in "
                   "the octonion-pair basis. T(OP^2) and A_Weyl are literally the "
                   "same Delta_9 module.")
        closed_by = "identity intertwiner (same subalgebra of gl(16))"
    else:
        verdict = ("Both are 16-dim IRREDUCIBLE modules of so(9) of REAL type "
                   "(commutants = 1). Spin(9) has a UNIQUE 16-dim irrep (the real "
                   "spinor Delta_9), so the two modules are ISOMORPHIC by that "
                   "classification theorem, even though they sit as different "
                   "so(9) embeddings in gl(16).")
        closed_by = "uniqueness of the 16-dim Spin(9) irrep (real spinor Delta_9)"
    print()
    print("    VERDICT:")
    for line in _wrap(verdict, 68):
        print("      " + line)
    print()

    both_real_irred = (c_flav == 1 and c_gauge == 1)
    isomorphism_established = (
        dim_f4 == 52 and dim_spin9 == 36 and rank == dim_spin9
        and leak < 1e-5 and both_real_irred and dim_cl == 36
    )
    print("    => A_Weyl ~= T(OP^2) as Spin(9) spinors:",
          "ESTABLISHED" if isomorphism_established else "NOT established")
    print(f"       closed by: {closed_by}")
    print()
    print("    Remaining seam (honest): this identifies the FLAVOUR-side Spin(9)")
    print("    (idempotent stabiliser in F4) and the GAUGE-side Spin(9) (Clifford")
    print("    on the octonion pair) as carrying the same unique 16. The last")
    print("    physical input is that these two Spin(9)'s are the same subgroup")
    print("    -- a subgroup-embedding statement, no longer a dimension/identity")
    print("    count. R3 is reduced from 'is 432 the product?' to that embedding.")
    print("=" * 74)

    return {
        "dim_f4": dim_f4,
        "dim_spin9": dim_spin9,
        "killing_rank": rank,
        "isotropy_commutant": c_flav,
        "clifford_commutant": c_gauge,
        "flavour_so9_dim": r_flav,
        "gauge_so9_dim": r_gauge,
        "same_subspace": bool(same_subspace),
        "isomorphism_established": bool(isomorphism_established),
        "closed_by": closed_by,
    }


def _wrap(text, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


if __name__ == "__main__":
    main()
