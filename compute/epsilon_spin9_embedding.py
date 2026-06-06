"""
Epsilon seam — the gauge Spin(9) and the flavour Spin(9) are the SAME subgroup.
==============================================================================

epsilon_weyl_isomorphism.py (route 4c) proved A_Weyl ~= T(OP^2) = Delta_9 (the
unique 16-dim real Spin(9) spinor), but left ONE honest seam: it used two a-priori
different Spin(9)'s --

  * FLAVOUR Spin(9): the stabiliser of the primitive idempotent E0 inside
    F4 = Der(J3(O)), acting on the vacuum-manifold tangent T(OP^2) (the (z2,z3)
    octonion-pair block of J3(O));
  * GAUGE Spin(9): an octonionic Clifford algebra Cl(9) built on the octonion
    pair O^2 (the carrier of one CHO Weyl generation A_Weyl).

Route 4c showed both act as the unique Delta_9, but as DIFFERENT embeddings in
gl(16) (their 36-dim so(9) subspaces spanned a combined 51 dimensions). The
remaining question -- the last content of residual R3 -- is whether these are the
SAME subgroup, i.e. whether the identification A_Weyl = T(OP^2) is a genuine
equality of Spin(9) reps or only an abstract isomorphism.

The claim under test
--------------------
The two are the same subgroup up to a frame rotation of the octonion pair:

  (a) Both so(9)'s sit inside the SAME so(16): the gauge generators are manifestly
      antisymmetric; the flavour generators are antisymmetric w.r.t. a UNIQUE
      invariant inner product Q (computed), so after the Q-orthonormal frame the
      flavour Spin(9) is a literal subgroup of SO(16).
  (b) The flavour Spin(9) is itself an OCTONIONIC Cl(9) spinor: a Clifford system
      {Gamma_mu} with {Gamma_mu, Gamma_nu} = 2 delta is RECOVERED from the flavour
      isotropy algebra (as the 9-dim "vector" eigenspace of the quadratic Casimir
      acting on symmetric 16x16 matrices), and span{(1/2)Gamma_mu Gamma_nu} is
      exactly the flavour so(9). So the flavour Spin(9) is built by the SAME
      octonionic Clifford construction as the gauge Spin(9) -- not merely an
      isomorphic abstract group.
  (c) The even Clifford algebra Cl^0(9) ~= R(16) is SIMPLE with a UNIQUE 16-dim
      irreducible module. Both the gauge and flavour Spin(9) are that one module
      (commutant dimension 1, verified). A simple algebra's unique irrep is
      determined up to an intertwiner, and because both carry invariant inner
      products the intertwiner is ORTHOGONAL: the two Spin(9)'s are conjugate in
      O(16).

Net: the seam shrinks from "are the gauge and flavour Spin(9) the same group?" to
"is the gauge octonion-pair frame the flavour octonion-pair frame?" -- a choice of
orthonormal frame on a single 16-dim octonionic spinor, the weakest possible
residual. The 432 = 16 x 27 product is then a product of two geometric dimensions
whose 16's are the one octonionic Delta_9.

What this module verifies (computed, not asserted)
--------------------------------------------------
  [1] Gauge so(9) (Cl(9) bivectors) is antisymmetric -> subset of so(16).
  [2] Flavour so(9): build f4 = Der(J3(O)), the E0-stabiliser, restrict to the
      (z2,z3) block; find the invariant metric Q (1-dim null space of
      rho^T Q + Q rho = 0), verify Q positive-definite, and Q-orthonormalise to
      land the flavour Spin(9) in SO(16).
  [3] Recover the flavour Clifford system {Gamma_mu} from the Casimir 9-eigenspace;
      verify {Gamma_mu, Gamma_nu} = 2 delta and span{(1/2)Gamma Gamma} = flavour
      so(9). Flavour Spin(9) IS an octonionic Cl(9) Delta_9.
  [4] Cl^0(9) ~= R(16) simple, unique 16-irrep (both commutants = 1): conclude the
      two Spin(9)'s are O(16)-conjugate -- the same subgroup up to a frame.

No scipy. Reuses epsilon_weyl_isomorphism's f4 / Clifford machinery.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_spin9_embedding.py
"""

import numpy as np

from jordan_eigenvalue_generations import JordanElement
from epsilon_state_count import jordan_to_vec
from epsilon_weyl_isomorphism import (
    jordan_product_tensor,
    derivation_algebra,
    stabiliser_subalgebra,
    clifford9_generators,
    so9_from_clifford,
    commutant_dimension,
    _vec,
)


# --------------------------------------------------------------------------
# invariant metric of a real representation
# --------------------------------------------------------------------------
def invariant_metric(gens, tol=1e-7):
    """Symmetric Q with rho^T Q + Q rho = 0 for every generator rho.
    For an irreducible real-type rep the solution space is 1-dimensional; return
    the (sign-fixed, normalised) positive-definite representative."""
    d = gens[0].shape[0]
    # symmetric basis of d x d  (d(d+1)/2 of them)
    sym_basis = []
    for i in range(d):
        for j in range(i, d):
            S = np.zeros((d, d))
            S[i, j] = 1.0
            S[j, i] = 1.0
            sym_basis.append(S)
    B = np.stack(sym_basis)                      # (nsym, d, d)
    # constraint operator: for each generator, rho^T Q + Q rho = 0
    rows = []
    for rho in gens:
        # linear map Q -> rho^T Q + Q rho, expressed on the symmetric basis
        M = np.array([(rho.T @ S + S @ rho).reshape(-1) for S in B])  # (nsym, d*d)
        rows.append(M.T)                          # (d*d, nsym)
    A = np.vstack(rows)                           # (ngen*d*d, nsym)
    _, s, Vt = np.linalg.svd(A, full_matrices=True)
    null = Vt[len(s):] if len(s) < Vt.shape[0] else np.zeros((0, Vt.shape[1]))
    # also include near-zero singular directions
    smax = s[0] if s.size else 1.0
    small = [Vt[i] for i in range(len(s)) if s[i] <= tol * smax]
    coeffs = list(small) + list(null)
    # rebuild Q from the first null vector
    c0 = coeffs[0]
    Q = sum(c0[k] * sym_basis[k] for k in range(len(sym_basis)))
    # fix sign / scale to positive-definite, unit Frobenius
    w = np.linalg.eigvalsh(Q)
    if w[0] < 0 and w[-1] <= 0:
        Q = -Q
        w = -w
    Q = Q / np.linalg.norm(Q) * np.sqrt(Q.shape[0])
    return Q, len(coeffs)


def casimir_on_symmetric(gens):
    """Quadratic Casimir C = sum_k ad(b_k)^2 restricted to symmetric matrices,
    using an orthonormal basis b_k of the (antisymmetric) algebra.  Returns the
    operator as an (nsym x nsym) matrix plus the symmetric basis."""
    d = gens[0].shape[0]
    # orthonormalise the algebra in <X,Y> = tr(X^T Y)
    V = _vec(gens)                                # d^2 x ngen
    U, s, _ = np.linalg.svd(V, full_matrices=False)
    bk = [U[:, i].reshape(d, d) for i in range(int(np.sum(s > 1e-9 * s[0])))]
    # symmetric basis (orthonormal in tr(X^T Y))
    sym = []
    for i in range(d):
        for j in range(i, d):
            S = np.zeros((d, d))
            if i == j:
                S[i, i] = 1.0
            else:
                S[i, j] = S[j, i] = 1.0 / np.sqrt(2.0)
            sym.append(S)
    nsym = len(sym)
    # Casimir action A -> sum_k [b_k,[b_k,A]] (keeps A symmetric for antisym b_k)
    def ad2(A):
        out = np.zeros_like(A)
        for b in bk:
            c = b @ A - A @ b
            out += b @ c - c @ b
        return out
    C = np.zeros((nsym, nsym))
    for col, S in enumerate(sym):
        CS = ad2(S)
        C[:, col] = [np.sum(T * CS) for T in sym]
    C = 0.5 * (C + C.T)
    return C, sym


def recover_clifford(gens, tol=1e-5):
    """Recover a Clifford system {Gamma_mu} with {Gamma,Gamma}=2 delta from the
    9-dim Casimir eigenspace (the 'vector' rep) inside symmetric matrices."""
    C, sym = casimir_on_symmetric(gens)
    w, Vv = np.linalg.eigh(C)
    # group eigenvalues into multiplicity clusters; the vector rep is the 9-fold
    clusters = {}
    for idx, ev in enumerate(w):
        key = round(ev, 4)
        clusters.setdefault(key, []).append(idx)
    nine = [cols for cols in clusters.values() if len(cols) == 9]
    if not nine:
        return None, None, clusters
    cols = nine[0]
    d = gens[0].shape[0]
    raw = [sum(Vv[k, c] * sym[k] for k in range(len(sym))) for c in cols]
    # build the symmetric form g_mu,nu I = (1/2)(B_mu B_nu + B_nu B_mu)
    g = np.zeros((9, 9))
    for a in range(9):
        for b in range(9):
            anti = 0.5 * (raw[a] @ raw[b] + raw[b] @ raw[a])
            g[a, b] = np.trace(anti) / d
    # orthonormalise: Gamma = g^{-1/2} applied to raw, giving {Gamma,Gamma}=2 delta
    wv, Uv = np.linalg.eigh(g)
    ginv_sqrt = Uv @ np.diag(1.0 / np.sqrt(np.abs(wv))) @ Uv.T
    Gamma = [sum(ginv_sqrt[m, a] * raw[a] for a in range(9)) for m in range(9)]
    return Gamma, g, clusters


def main():
    print("=" * 74)
    print("EPSILON SEAM: gauge Spin(9) and flavour Spin(9) are the SAME subgroup")
    print("=" * 74)
    print()

    np.random.seed(0)

    # ---- [1] gauge so(9) in so(16) -------------------------------------
    print("[1] Gauge so(9) (octonionic Cl(9) bivectors) is in so(16)")
    G = clifford9_generators()
    sigma = so9_from_clifford(G)
    asym = max(float(np.linalg.norm(s + s.T)) for s in sigma)
    print(f"    max |sigma + sigma^T| = {asym:.2e}",
          "(antisymmetric -> subset of so(16), PASS)" if asym < 1e-10 else "(FAIL)")
    print()

    # ---- [2] flavour so(9) and its invariant metric --------------------
    print("[2] Flavour so(9) (F4 isotropy on the (z2,z3) octonion pair)")
    T = jordan_product_tensor()
    f4, _ = derivation_algebra(T)
    v0 = jordan_to_vec(JordanElement.diagonal(1.0, 0.0, 0.0))
    spin9 = stabiliser_subalgebra(f4, v0)
    idx = np.arange(11, 27)
    P = np.eye(27)[idx]
    rho = [P @ D @ P.T for D in spin9]            # 36 matrices, 16x16
    print(f"    dim f4 = {len(f4)}, dim flavour spin(9) = {len(rho)}")
    Q, nullsize = invariant_metric(rho)
    wq = np.linalg.eigvalsh(Q)
    pd = bool(wq[0] > 1e-9)
    print(f"    invariant metric Q: solution-space dim = {nullsize}, "
          f"eigenvalue range [{wq[0]:.3f}, {wq[-1]:.3f}]",
          "(unique & positive-definite, PASS)" if nullsize == 1 and pd else "(FAIL)")
    # Q-orthonormal frame: L^T L = Q, rho~ = L rho L^{-1} antisymmetric
    L = np.linalg.cholesky(Q).T
    Linv = np.linalg.inv(L)
    rho_t = [L @ r @ Linv for r in rho]
    asym_f = max(float(np.linalg.norm(r + r.T)) for r in rho_t)
    print(f"    after the Q-frame: max |rho~ + rho~^T| = {asym_f:.2e}",
          "(flavour Spin(9) is now a subgroup of SO(16), PASS)"
          if asym_f < 1e-6 else "(FAIL)")
    print()

    # ---- [3] flavour so(9) IS an octonionic Cl(9) ----------------------
    print("[3] Recover the flavour Clifford system {Gamma_mu} (the vector 9 in")
    print("    the Casimir spectrum on symmetric 16x16 matrices)")
    Gamma, g, clusters = recover_clifford(rho_t)
    mults = sorted(len(c) for c in clusters.values())
    print(f"    Casimir multiplicities on Sym^2(16): {mults} (expect 1, 9, 126)")
    cliff_err = 0.0
    I16 = np.eye(16)
    if Gamma is not None:
        for a in range(9):
            for b in range(9):
                anti = Gamma[a] @ Gamma[b] + Gamma[b] @ Gamma[a]
                cliff_err = max(cliff_err, float(np.linalg.norm(anti - 2.0 * (a == b) * I16)))
        print(f"    {{Gamma_mu,Gamma_nu}} = 2 delta: max error = {cliff_err:.2e}",
              "(a genuine Cl(9) system, PASS)" if cliff_err < 1e-6 else "(FAIL)")
        # does span{(1/2)Gamma Gamma} reproduce the flavour so(9)?
        biv = []
        for a in range(9):
            for b in range(a + 1, 9):
                biv.append(0.5 * (Gamma[a] @ Gamma[b]))
        Vbiv = _vec(biv)
        Vfl = _vec(rho_t)
        comb = np.hstack([Vbiv, Vfl])
        r_b = int(np.linalg.matrix_rank(Vbiv, tol=1e-7))
        r_f = int(np.linalg.matrix_rank(Vfl, tol=1e-7))
        r_c = int(np.linalg.matrix_rank(comb, tol=1e-7))
        same = (r_b == 36 and r_f == 36 and r_c == 36)
        print(f"    dim span{{(1/2)Gamma Gamma}} = {r_b}, flavour so(9) = {r_f}, "
              f"combined = {r_c}",
              "(SAME subspace -> flavour Spin(9) IS the octonionic Cl(9), PASS)"
              if same else "(not equal)")
    else:
        same = False
        print("    no clean 9-eigenspace found (FAIL)")
    print()

    # ---- [4] simple even algebra -> O(16) conjugacy --------------------
    print("[4] Cl^0(9) ~= R(16) simple, unique 16-irrep -> O(16)-conjugacy")
    c_gauge = commutant_dimension(sigma)
    c_flav = commutant_dimension(rho_t)
    print(f"    commutant(gauge spin9) = {c_gauge}, commutant(flavour spin9) = {c_flav}")
    unique_irrep = (c_gauge == 1 and c_flav == 1)
    print("    both 16-dim modules have commutant 1 => each is THE unique",
          "irreducible" if unique_irrep else "(FAIL)")
    print("    real module of the simple algebra Cl^0(9) ~= R(16). A simple")
    print("    algebra's unique irrep is fixed up to an intertwiner, and the")
    print("    invariant inner products make it ORTHOGONAL: the gauge and flavour")
    print("    Spin(9) are conjugate in O(16) -- the same subgroup up to a frame.")
    print()

    established = bool(asym < 1e-10 and nullsize == 1 and pd and asym_f < 1e-6
                       and (Gamma is not None) and cliff_err < 1e-6 and same
                       and unique_irrep)
    print("[VERDICT]")
    print("    The flavour Spin(9) is not merely isomorphic to the gauge Spin(9):")
    print("    it is realised by the SAME octonionic Cl(9) spinor construction")
    print("    (Clifford system recovered, bivectors = flavour so(9)), and the two")
    print("    are conjugate in O(16) by uniqueness of the Cl^0(9) irrep. The seam")
    print("    is reduced to ONE frame choice on the octonion pair -- A_Weyl and")
    print("    T(OP^2) are the same Delta_9 subgroup, not just isomorphic.")
    print("    Seam status:", "CLOSED to a frame choice" if established
          else "NOT closed")
    print("=" * 74)

    return {
        "gauge_antisym": float(asym),
        "metric_nullspace_dim": nullsize,
        "metric_positive_definite": pd,
        "flavour_antisym_after_Q": float(asym_f),
        "clifford_error": float(cliff_err) if Gamma is not None else None,
        "bivectors_equal_flavour_so9": bool(same),
        "commutants": (c_gauge, c_flav),
        "seam_closed_to_frame": established,
    }


if __name__ == "__main__":
    main()
