"""
Epsilon route (4) — 432 as a geometric STATE COUNT (the flux-per-state reframe).
================================================================================

Routes (1) and (2) returned converging negatives that pin down the structure of
eps0^2 = pi/432:

  * epsilon_heat_kernel.py : the pi is a BARE Berry flux (half-solid-angle
    (1/2)(2 pi) = pi), NOT a heat-kernel (4 pi)^(-d/2) factor. Geometric origin
    ruled IN, spectral-action origin ruled OUT.
  * epsilon_cubic_discriminant.py : the 27 is the DIMENSION of J3(O) (a trace /
    state count), NOT the universal 27 of the cubic discriminant (a rank-one
    breaking has a double root, Delta = 0).

Both point at the same reframe:

    eps0^2 = pi / 432 = (Berry flux through the minimal transition 2-cycle)
                         / (number of quantum states) ,

i.e. eps0^2 is a CHERN / FLUX-PER-STATE density. The numerator pi is already
action-selected (foundations/02_action.md). This module attacks the denominator:
is 432 a forced GEOMETRIC state count, closing residual R3?

The geometric claim under test
------------------------------
432 = 16 x 27 with BOTH factors geometric, not chosen:

  * 27 = dim J3(O): the ambient exceptional Jordan algebra -- the flavour
    "phase space" of the framework.
  * 16 = dim_R(OP^2): the real dimension of the Cayley projective plane
    OP^2 = F4 / Spin(9), which is PRECISELY the manifold of rank-one (primitive)
    idempotents of J3(O) -- the space of triality-breaking vacuum rays |tau>.

So eps0 lives on OP^2 (the 16-dim manifold of triality vacua) embedded in J3(O)
(its 27-dim ambient algebra), and 432 = dim(OP^2) x dim(J3(O)) is the total
phase-space dimension the rank-one spurion sweeps. Both 16 and 27 are then
DIMENSIONS (Bohr-Sommerfeld / Weyl state counts), consistent with route (1)'s
verdict that the 432 must be a state count.

What this module verifies (computed, not asserted)
--------------------------------------------------
  A. 16 = dim F4 - dim Spin(9) = 52 - 36, the coset dimension of OP^2
     = F4/Spin(9) (pure arithmetic of the isometry/isotropy groups).
  B. The points of OP^2 ARE the rank-one idempotents of J3(O): build the
     idempotent variety { X in J3(O) : X o X = X, Tr X = 1 } near a primitive
     idempotent and measure the DIMENSION of its tangent space numerically
     (nullity of the Jacobian of the idempotent equations on the 27 real
     coordinates). The connected component through a primitive idempotent should
     come out 16 = dim OP^2 -- derived, not input.
  C. Assemble eps0^2 = pi / (dim OP^2 x dim J3(O)) = pi/432 and state plainly
     which factors are now geometric and which assumption remains.

If B returns 16 from the Jacobian rank, the 27 (ambient) and the 16 (vacuum
manifold) are both honest dimensions and the 432 is a forced phase-space count
rather than a hand multiplication of "16 x 27".

No scipy. Uses octonion_toolkit + the J3(O) Jordan-product machinery in
jordan_eigenvalue_generations.py. Jacobian by finite differences.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_state_count.py
"""

import numpy as np

from octonion_toolkit import Octonion
from jordan_eigenvalue_generations import (
    JordanElement,
    _herm_to_dense,
    jordan_product_dense,
)


# Lie-group dimensions (compact real forms) -- standard, used only for the
# coset arithmetic of OP^2 = F4/Spin(9).
DIM_F4 = 52
DIM_SPIN9 = 36


# --------------------------------------------------------------------------
# Coordinate map  R^27  <->  J3(O)
# --------------------------------------------------------------------------
def vec_to_jordan(p):
    """27 real coordinates -> JordanElement.
    Layout: p[0:3] diagonal xi; p[3:11], p[11:19], p[19:27] the three octonions.
    """
    xi = p[0:3]
    z1 = Octonion(np.array(p[3:11], dtype=float))
    z2 = Octonion(np.array(p[11:19], dtype=float))
    z3 = Octonion(np.array(p[19:27], dtype=float))
    return JordanElement(xi, z1, z2, z3)


def jordan_to_vec(J):
    return np.concatenate([J.xi, J.z1.coeffs, J.z2.coeffs, J.z3.coeffs])


def idempotent_residual(p):
    """R(p) = (X o X - X) flattened to 27 reals, where X = vec_to_jordan(p).
    Zero exactly on the idempotent variety X o X = X."""
    X = vec_to_jordan(p)
    Xd = _herm_to_dense(X)
    XoX = jordan_product_dense(Xd, Xd)
    # XoX is a dense 3x3 octonion-Hermitian matrix; subtract X and read its 27
    # independent real coordinates back out.
    diff_xi = np.array([XoX[k][k].real_part() - X.xi[k] for k in range(3)])
    # off-diagonal entries: (1,2)->z1, (0,2)->conj(z2), (0,1)->z3
    # (see _herm_to_dense: the (0,2) slot stores z2.conjugate()).
    d_z1 = (XoX[1][2] + (-1.0) * X.z1).coeffs
    d_z2 = (XoX[0][2].conjugate() + (-1.0) * X.z2).coeffs
    d_z3 = (XoX[0][1] + (-1.0) * X.z3).coeffs
    return np.concatenate([diff_xi, d_z1, d_z2, d_z3])


def numerical_jacobian(f, p0, h=1e-6):
    n = p0.size
    f0 = f(p0)
    m = f0.size
    J = np.zeros((m, n))
    for j in range(n):
        pp = p0.copy()
        pp[j] += h
        J[:, j] = (f(pp) - f0) / h
    return J


def tangent_dimension(p0, tol=1e-5):
    """Dimension of the idempotent variety at p0 = nullity of the Jacobian of
    the idempotent equations (= 27 - rank)."""
    J = numerical_jacobian(idempotent_residual, p0)
    s = np.linalg.svd(J, compute_uv=False)
    smax = s[0] if s.size else 0.0
    rank = int(np.sum(s > tol * max(smax, 1.0)))
    return 27 - rank, s


def main():
    print("=" * 74)
    print("EPSILON ROUTE (4): 432 as a geometric STATE COUNT (flux per state)")
    print("=" * 74)
    print()

    # ---- A. 16 = dim OP^2 = dim F4 - dim Spin(9) -----------------------
    dim_op2 = DIM_F4 - DIM_SPIN9
    print("[A] Cayley plane OP^2 = F4 / Spin(9)")
    print(f"    dim OP^2 = dim F4 - dim Spin(9) = {DIM_F4} - {DIM_SPIN9} = {dim_op2}")
    print("    -> 16 (PASS)" if dim_op2 == 16 else "    -> NOT 16 (FAIL)")
    print()

    # ---- B. rank-one idempotent variety has dimension 16 ---------------
    print("[B] Points of OP^2 = rank-one idempotents of J3(O)")
    e1 = JordanElement.diagonal(1.0, 0.0, 0.0)
    Xd = _herm_to_dense(e1)
    XoX = jordan_product_dense(Xd, Xd)
    # confirm e1 is genuinely idempotent and primitive (spectrum (1,0,0))
    res0 = np.linalg.norm(idempotent_residual(jordan_to_vec(e1)))
    ev = np.sort(np.real(e1.eigenvalues()))
    print("    base point E0 = diag(1,0,0): |X o X - X| =", f"{res0:.2e}",
          " spectrum", np.array2string(ev, precision=3))
    dim_tan, svals = tangent_dimension(jordan_to_vec(e1))
    print("    tangent-space dimension at E0 (27 - rank Jacobian):", dim_tan)
    print("    smallest 12 singular values of Jacobian:")
    print("    ", np.array2string(np.sort(svals)[:12], precision=3,
                                  suppress_small=True))
    match16 = (dim_tan == 16)
    print("    -> idempotent manifold is 16-dimensional = dim OP^2 (PASS)"
          if match16 else
          f"    -> dimension {dim_tan}, not 16 (see note)")
    print()

    # sanity: check at a couple of other primitive idempotents (rotated)
    print("    cross-check at diag(0,1,0) and diag(0,0,1):")
    for d in [(0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]:
        e = JordanElement.diagonal(*d)
        dt, _ = tangent_dimension(jordan_to_vec(e))
        print(f"      diag{d}: tangent dim =", dt)
    print()

    # ---- C. assemble ---------------------------------------------------
    n_states = dim_op2 * 27
    eps0_sq = np.pi / n_states
    print("[C] Flux-per-state assembly")
    print("    numerator   : Berry flux pi   (action-selected, 02_action.md)")
    print(f"    denominator : dim OP^2 x dim J3(O) = {dim_op2} x 27 = {n_states}")
    print(f"    eps0^2 = pi / {n_states} = {eps0_sq:.8f}")
    print(f"    target pi/432         = {np.pi/432:.8f}")
    print("    match:", np.isclose(eps0_sq, np.pi / 432))
    print()

    print("[D] VERDICT — what route (4) closes and what remains")
    if match16:
        print("    * 27 = dim J3(O): the flavour phase space (a dimension).")
        print("    * 16 = dim OP^2 = F4/Spin(9): DERIVED numerically as the")
        print("      dimension of the rank-one idempotent manifold of J3(O)")
        print("      (the manifold of triality vacua |tau>), not chosen.")
        print("    * So 432 = dim(OP^2) x dim(J3(O)) is the phase-space the rank-")
        print("      one spurion sweeps: vacuum-manifold x ambient algebra. Both")
        print("      factors are geometric dimensions -> R3 reframed from a hand")
        print("      '16 x 27' into a forced (vacuum manifold) x (ambient) count.")
        print()
        print("    REMAINING (honest): the trace normalization eps0^2 =")
        print("    Tr(T_break)/dim must be shown to run over EXACTLY this product")
        print("    phase space (the Bohr-Sommerfeld measure on OP^2 times the")
        print("    J3(O) trace), i.e. that the spurion's quantum-state count is")
        print("    dim(OP^2) x dim(J3(O)) and not dim(OP^2) alone or J3(O) alone.")
        print("    That is the single remaining state-count assumption; it is now")
        print("    a sharp geometric question, not a free integer choice.")
    else:
        print("    The idempotent manifold did not return 16 numerically; the")
        print("    geometric state-count identification is NOT confirmed by this")
        print("    computation and must be revisited (check the coordinate map and")
        print("    the Jordan-product residual). Reported honestly, not patched.")
    print("=" * 74)

    return {
        "dim_op2_coset": dim_op2,
        "idempotent_manifold_dim": dim_tan,
        "matches_16": bool(match16),
        "eps0_sq": float(eps0_sq),
    }


if __name__ == "__main__":
    main()
