"""
F0 symplectic-volume route: pi/432 as ONE geometric-quantization object.

Motivation
----------
The F0 program reduced the seam behind `epsilon0^2 = pi/432` to a single live
question (see `f0_direction_gate.py` and `epsilon_product_irreducible.py`):

    why is the transition arena the PRODUCT  Delta_9 (x) J3(O)  (16 x 27),
    equivalently why is the symmetry the factor-wise product Spin(9) x E6?

`epsilon_measure_schur.py` forced the flat weights 1/16 and 1/27 by
irreducibility, and `epsilon_product_irreducible.py` removed the
separable-projector and minimal-multiplicity clauses. What stayed open was the
PRODUCT itself: those modules ASSUME the two commuting sector groups and read
off 16 x 27.

This module attacks that seam with a different lens -- the orbit method /
geometric quantization -- on the thesis (the project's own) that pi/432 should
be ONE geometric object, not an assembly of three chosen pieces. The new content:

  * 16 and 27 are not "chosen dimensions"; each is the Bohr-Sommerfeld /
    Kirillov state count (= the dimension, by Borel-Weil) of a single coadjoint
    orbit -- the Spin(9) spinor orbit and the E6 minimal orbit. We recompute
    both from scratch with the Weyl dimension formula (no representation library).

  * The PRODUCT 432 is then a THEOREM, not an assumption: a coadjoint orbit of a
    direct-product group G1 x G2 is the product orbit O1 x O2, its Liouville
    (symplectic) volume is the PRODUCT of the two volumes, and its quantization
    is the tensor product, dim = dim1 x dim2. We verify this multiplicativity of
    the quantization directly on small product root systems. So "the arena is a
    product" follows from "the symmetry is a product group" GEOMETRICALLY -- the
    factorization 432 = 16 x 27 is the volume of one product orbit.

  * The bare pi (not 2 pi) is the symplectic half-flux of the minimal transition
    orbit CP^1 = S^2 (the two-level Bloch sphere): one flux quantum gives area
    2 pi, and the Berry holonomy around its great circle encloses half of it,
    (1/2)(2 pi) = pi. This is the SAME pi that `action_derivation.py` selects as
    the great-circle Berry phase; we reuse that result and recast it as a flux.

So the synthesis is one geometric-quantization statement:

    epsilon0^2 = (half-flux of the minimal transition orbit)
                 x (1 / Liouville volume of the product coadjoint orbit)
               = pi x (1 / (16 x 27))
               = pi / 432.

Honest scope (what this does NOT close)
---------------------------------------
* OP^2 = F4/Spin(9) is NOT itself a symplectic homogeneous space (Spin(9) has no
  U(1) centre, OP^2 carries no invariant symplectic form). The symplectic
  carriers are the coadjoint ORBITS in so(9)^* and e6^* whose quantizations are
  the 16 and the 27, not OP^2 as a manifold. This module is explicit about that.
* It does NOT derive, from the CHO action, that the triality-breaking transition
  quantizes exactly these two orbits. That is the same live F0 bridge -- but it
  is now "which two coadjoint orbits does the action pick", with a positive
  geometric mechanism for the product, rather than an assumed commuting product.

F0 is NOT promoted to DERIVED by this module.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_symplectic_volume.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from action_derivation import derive_theta_from_action, solid_angle_of_latitude

PI = math.pi
DIM_DELTA9 = 16
DIM_J3O = 27
DIM_ARENA = DIM_DELTA9 * DIM_J3O          # 432
TARGET = PI / DIM_ARENA                    # = epsilon0^2 = pi/432
TOL = 1e-9


# --------------------------------------------------------------------------- #
#  Root systems and the Weyl dimension formula (= Bohr-Sommerfeld count)       #
# --------------------------------------------------------------------------- #
#
# By Borel-Weil, the dimension of the irrep with highest weight lambda equals
# the number of Bohr-Sommerfeld leaves of the coadjoint orbit O_{lambda+rho},
# i.e. the geometric-quantization "volume" of that orbit in units where each
# quantum state occupies one cell.  The Weyl dimension formula
#
#       dim V_lambda = prod_{alpha > 0}  <lambda + rho, alpha> / <rho, alpha>
#
# is scale-invariant in each root alpha, so it can be evaluated either with an
# explicit Euclidean realisation of the roots (used here for the non-simply-laced
# B4 = so(9)) or, for a simply-laced algebra (A, D, E -- including E6), purely
# from the integer root coordinates, since there <rho, alpha> = height(alpha) and
# <omega_m, alpha^vee> = (coefficient of simple root m in alpha).


def positive_roots_from_cartan(cartan):
    """Positive roots (integer coords in the simple-root basis) from a Cartan
    matrix, by the standard root-string construction.  Valid for any finite
    type; used here for simply-laced algebras."""
    n = len(cartan)
    simple = [tuple(1 if i == k else 0 for i in range(n)) for k in range(n)]
    roots = set(simple)
    changed = True
    while changed:
        changed = False
        for beta in list(roots):
            for j in range(n):
                gamma = tuple(beta[i] + (1 if i == j else 0) for i in range(n))
                if gamma in roots:
                    continue
                # p = how far the alpha_j-string runs DOWN from beta
                p = 0
                while True:
                    below = tuple(beta[i] - (p + 1) * (1 if i == j else 0)
                                  for i in range(n))
                    if any(below) and all(t >= 0 for t in below) and below in roots:
                        p += 1
                    else:
                        break
                pairing = sum(beta[i] * cartan[i][j] for i in range(n))
                # alpha_j-string: beta - p alpha_j ... beta + q alpha_j, p - q = pairing
                if p - pairing >= 1:
                    roots.add(gamma)
                    changed = True
    return sorted(roots)


def simply_laced_dim(positive_roots, highest_weight):
    """dim V_lambda for a simply-laced algebra, lambda given in the
    fundamental-weight basis (a tuple of non-negative integers).

    dim = prod_{alpha>0} (<lambda, alpha^vee> + ht(alpha)) / ht(alpha),
    with <lambda, alpha^vee> = sum_m lambda_m * (coeff of simple root m in alpha)
    and <rho, alpha^vee> = ht(alpha) = sum of coeffs.
    """
    num = 1.0
    den = 1.0
    for alpha in positive_roots:
        ht = sum(alpha)
        lam = sum(highest_weight[m] * alpha[m] for m in range(len(alpha)))
        num *= (lam + ht)
        den *= ht
    return num / den


def euclidean_dim(positive_roots, highest_weight):
    """dim V_lambda from an explicit Euclidean realisation of the roots.

    Uses dim = prod <lambda+rho, alpha> / <rho, alpha> with rho = half the sum
    of the positive roots.  Scale-invariance in alpha means the literal roots
    (not coroots) may be used.
    """
    roots = np.asarray(positive_roots, dtype=float)
    rho = 0.5 * roots.sum(axis=0)
    lr = np.asarray(highest_weight, dtype=float) + rho
    num = 1.0
    den = 1.0
    for alpha in roots:
        num *= float(lr @ alpha)
        den *= float(rho @ alpha)
    return num / den


def so9_positive_roots():
    """B4 = so(9) positive roots in R^4: the short e_i and the long e_i +- e_j."""
    roots = []
    for i in range(4):
        e = np.zeros(4)
        e[i] = 1.0
        roots.append(e)
    for i in range(4):
        for j in range(i + 1, 4):
            a = np.zeros(4); a[i] = 1.0; a[j] = 1.0
            b = np.zeros(4); b[i] = 1.0; b[j] = -1.0
            roots.append(a)
            roots.append(b)
    return roots


def e6_cartan():
    """E6 Cartan matrix (Bourbaki diagram: chain 0-2-3-4-5, node 1 on node 3)."""
    c = [[2 if i == j else 0 for j in range(6)] for i in range(6)]
    for a, b in [(0, 2), (2, 3), (3, 4), (4, 5), (1, 3)]:
        c[a][b] = -1
        c[b][a] = -1
    return c


def _onehot(n, k):
    v = [0] * n
    v[k] = 1
    return tuple(v)


# --------------------------------------------------------------------------- #
#  The two orbit quantizations: 16 and 27                                      #
# --------------------------------------------------------------------------- #
def spin9_spinor_count():
    """16 = Bohr-Sommerfeld count of the Spin(9) spinor coadjoint orbit, with
    the vector (9) and adjoint (36) as method checks."""
    roots = so9_positive_roots()
    spinor = euclidean_dim(roots, [0.5, 0.5, 0.5, 0.5])
    vector = euclidean_dim(roots, [1.0, 0.0, 0.0, 0.0])
    adjoint = euclidean_dim(roots, [1.0, 1.0, 0.0, 0.0])
    return {
        "n_pos_roots": len(roots),
        "spinor": round(spinor),
        "vector": round(vector),
        "adjoint": round(adjoint),
    }


def e6_minimal_count():
    """27 = Bohr-Sommerfeld count of the E6 minimal coadjoint orbit, with the
    adjoint (78) as a method check.  Node 0 (an end of a length-4 arm) carries
    the 27; node 1 (off the trivalent node) carries the adjoint 78."""
    cartan = e6_cartan()
    roots = positive_roots_from_cartan(cartan)
    dims = [round(simply_laced_dim(roots, _onehot(6, m))) for m in range(6)]
    return {
        "n_pos_roots": len(roots),
        "fundamental_27": round(simply_laced_dim(roots, _onehot(6, 0))),
        "adjoint_78": round(simply_laced_dim(roots, _onehot(6, 1))),
        "all_fundamental_dims": dims,
    }


def j3o_structural_dimension():
    """27 = dim J3(O): 3 real diagonal entries + 3 off-diagonal octonions x 8."""
    diagonal = 3
    off_diagonal = 3 * 8
    return diagonal + off_diagonal


# --------------------------------------------------------------------------- #
#  Multiplicativity of quantization over a direct-product group                #
# --------------------------------------------------------------------------- #
def _direct_sum_cartan(c1, c2):
    n1, n2 = len(c1), len(c2)
    n = n1 + n2
    c = [[0] * n for _ in range(n)]
    for i in range(n1):
        for j in range(n1):
            c[i][j] = c1[i][j]
    for i in range(n2):
        for j in range(n2):
            c[n1 + i][n1 + j] = c2[i][j]
    return c


def product_quantization_factorizes():
    """A coadjoint orbit of G1 x G2 is the product orbit; its quantization is the
    tensor product, dim = dim1 x dim2.  Verify on small simply-laced products
    that the Weyl dimension over the direct-sum root system is exactly the product
    of the per-factor dimensions (the Liouville volume of a product is the product
    of volumes)."""
    a1 = [[2]]
    a2 = [[2, -1], [-1, 2]]

    # A1 x A1: (omega, omega) -> 2 x 2 = 4
    c = _direct_sum_cartan(a1, a1)
    roots = positive_roots_from_cartan(c)
    d_a1a1 = round(simply_laced_dim(roots, (1, 1)))

    # A2 x A1: (omega_1, omega) -> 3 x 2 = 6
    c = _direct_sum_cartan(a2, a1)
    roots = positive_roots_from_cartan(c)
    d_a2a1 = round(simply_laced_dim(roots, (1, 0, 1)))

    # A2 x A2: (omega_1, omega_1) -> 3 x 3 = 9
    c = _direct_sum_cartan(a2, a2)
    roots = positive_roots_from_cartan(c)
    d_a2a2 = round(simply_laced_dim(roots, (1, 0, 1, 0)))

    return {
        "A1xA1": (d_a1a1, 2 * 2),
        "A2xA1": (d_a2a1, 3 * 2),
        "A2xA2": (d_a2a2, 3 * 3),
    }


# --------------------------------------------------------------------------- #
#  The bare pi: half-flux of the minimal transition orbit CP^1 = S^2           #
# --------------------------------------------------------------------------- #
def minimal_orbit_half_flux():
    """The minimal transition orbit is CP^1 = S^2 (the two-level Bloch sphere).
    One flux quantum gives total symplectic area 2 pi; the great-circle Berry
    holonomy encloses half of it -> pi.  We read the great-circle solid angle
    from `action_derivation` and cross-check theta = pi from the free action."""
    great_circle_solid_angle = solid_angle_of_latitude(PI / 2.0)   # = 2 pi
    half_flux = 0.5 * great_circle_solid_angle                      # = pi
    action = derive_theta_from_action()
    return {
        "great_circle_solid_angle": great_circle_solid_angle,
        "half_flux": half_flux,
        "action_theta_is_pi": bool(action.theta_is_pi),
        "action_geodesic_selected": bool(action.geodesic_selected),
    }


# --------------------------------------------------------------------------- #
#  Driver                                                                      #
# --------------------------------------------------------------------------- #
def main():
    spin9 = spin9_spinor_count()
    e6 = e6_minimal_count()
    j3o_struct = j3o_structural_dimension()
    prod = product_quantization_factorizes()
    flux = minimal_orbit_half_flux()

    bs_product = spin9["spinor"] * e6["fundamental_27"]
    eps0_sq = flux["half_flux"] / bs_product

    print("=" * 78)
    print("  F0 SYMPLECTIC-VOLUME ROUTE")
    print("  Is pi/432 ONE geometric-quantization object (orbit method)?")
    print("=" * 78)
    print()
    print("  16 and 27 as Bohr-Sommerfeld counts of single coadjoint orbits")
    print("  " + "-" * 74)
    print(f"  Spin(9) spinor orbit : dim = {spin9['spinor']:>3}   "
          f"(method checks: vector {spin9['vector']}, adjoint {spin9['adjoint']}; "
          f"{spin9['n_pos_roots']} pos roots)")
    print(f"  E6 minimal orbit     : dim = {e6['fundamental_27']:>3}   "
          f"(method check: adjoint {e6['adjoint_78']}; "
          f"{e6['n_pos_roots']} pos roots)")
    print(f"  E6 fundamental dims  : {e6['all_fundamental_dims']}")
    print(f"  cross-check 27 = dim J3(O) = 3 + 3x8 = {j3o_struct}")
    print()
    print("  Product orbit: quantization is multiplicative (Liouville volume of")
    print("  a product orbit = product of volumes)")
    print("  " + "-" * 74)
    for name, (got, want) in prod.items():
        print(f"  dim({name:<6}) = {got:>2}   (= product {want})  "
              f"{'OK' if got == want else 'MISMATCH'}")
    print(f"  => Spin(9)xE6 product orbit count = 16 x 27 = {bs_product}")
    print()
    print("  Bare pi: half-flux of the minimal transition orbit CP^1 = S^2")
    print("  " + "-" * 74)
    print(f"  great-circle solid angle  = {flux['great_circle_solid_angle']:.6f} "
          f"(= 2 pi = one flux quantum's area)")
    print(f"  Berry half-flux           = {flux['half_flux']:.6f} (= pi)")
    print(f"  free action selects theta = pi : {flux['action_theta_is_pi']} "
          f"(great circle: {flux['action_geodesic_selected']})")
    print()
    print("  Synthesis")
    print("  " + "-" * 74)
    print(f"  epsilon0^2 = (half-flux pi) x (1 / product-orbit volume {bs_product})")
    print(f"             = {flux['half_flux']:.6f} / {bs_product}")
    print(f"             = {eps0_sq:.10f}")
    print(f"  pi/432     = {TARGET:.10f}   (= epsilon0^2)")
    print()

    checks = {
        "Spin(9) spinor BS count = 16": spin9["spinor"] == DIM_DELTA9,
        "Spin(9) method checks (vector 9, adjoint 36)":
            spin9["vector"] == 9 and spin9["adjoint"] == 36,
        "E6 minimal coadjoint count = 27": e6["fundamental_27"] == DIM_J3O,
        "E6 method check (adjoint 78)": e6["adjoint_78"] == 78,
        "E6 carries two 27s (27 and 27-bar)":
            e6["all_fundamental_dims"].count(27) == 2,
        "structural 27 = dim J3(O) = 3 + 3x8": j3o_struct == DIM_J3O,
        "quantization multiplicative over direct product":
            all(got == want for got, want in prod.values()),
        "product-orbit count = 16 x 27 = 432": bs_product == DIM_ARENA,
        "minimal-orbit great circle solid angle = 2 pi":
            abs(flux["great_circle_solid_angle"] - 2.0 * PI) < TOL,
        "Berry half-flux = pi": abs(flux["half_flux"] - PI) < TOL,
        "action selects theta = pi (Berry)": flux["action_theta_is_pi"],
        "synthesis pi x (1/432) = pi/432 = epsilon0^2":
            abs(eps0_sq - TARGET) < 1e-12,
    }
    width = max(len(k) for k in checks)
    for name, ok_ in checks.items():
        print(f"  [{'PASS' if ok_ else 'FAIL'}] {name:<{width}}")
    ok = all(checks.values())
    print()
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- 16, 27 are single-orbit quantizations; 432 is one product orbit.")
    print("  THEOREM STATUS: the PRODUCT 432 = 16 x 27 is geometric (Liouville")
    print("                  volume of a product coadjoint orbit), not an assumed")
    print("                  commuting split; the live F0 seam becomes 'which two")
    print("                  orbits does the CHO action quantize'. F0 not promoted.")
    print()
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
