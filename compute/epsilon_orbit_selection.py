"""
F0 orbit-selection route: WHICH TWO coadjoint orbits does the action quantize?

Motivation
----------
`epsilon_symplectic_volume.py` recast pi/432 as ONE geometric-quantization
object: 16 and 27 are the Bohr-Sommerfeld counts of a Spin(9)-spinor and an
E6-minimal coadjoint orbit, and 432 is the Liouville volume of their PRODUCT
orbit. That module closed "why a product" (multiplicativity of quantization) but
left one explicit seam:

    which two orbits does the CHO action quantize -- why the spinor orbit for
    Spin(9) and the MINIMAL orbit for E6, rather than some other pair?

This module attacks that seam with the coherent-state lens. A coherent-state
(Perelomov) quantization picks, for each factor, the orbit of LOWEST symplectic
volume compatible with the symmetry -- the MINIMAL orbit. The new content here is
that for BOTH factors the minimal orbit is not a free choice but is FORCED, by two
independent facts the project already owns:

  [16] Spin(9) acts TRANSITIVELY on the spinor sphere S^15 = unit Delta_9. So
       there is exactly ONE spinor orbit; "which spinor orbit" has no freedom.
       We verify transitivity directly: the orbit-tangent space span{A_a v} at a
       unit spinor v has dimension 15 (= dim S^15) at every point, with stabiliser
       dimension 36 - 15 = 21 = dim Spin(7) (the known isotropy, Spin(9)/Spin(7)
       = S^15). Transitive => unique orbit => the 16 is forced.

  [27] The E6 MINIMAL orbit is exactly the RANK-ONE variety of J3(O): the
       Freudenthal sharp map X# = X o X - tr(X) X + sigma2(X) I vanishes precisely
       on rank-one elements. And rank-one is EXACTLY the condition the CHO action
       already selects: `epsilon_rank_one_kernel.py` shows the triality-breaking
       vacuum is a primitive (rank-one) idempotent (= one generation = pure state),
       and `epsilon_action_stationary.py` shows the stationary link kernel is the
       rank-one pi|tau><tau|. So the action's own rank-one condition PICKS the E6
       minimal orbit -- "which E6 orbit" is answered by the action, not assumed.

A bridge between the two factors falls out for free: the f4-orbit (= F4/Spin(9)
= OP^2) of a rank-one idempotent has tangent space of dimension 16 = Delta_9. So
the 16 is literally the tangent space at a point of the 27's minimal orbit, with
isotropy Spin(9) -- the same Spin(9) whose spinor sphere is the 16. The two
"minimal orbits" are geometrically interlocked, not two independent guesses.

Synthesis
---------
    epsilon0^2 = pi / (vol of the PRODUCT of the two MINIMAL coadjoint orbits),
    where 'minimal' is forced by  (16) Spin(9)-transitivity on S^15  and
    (27) the action's rank-one selection = E6 minimal (sharp-zero) orbit.

Honest scope (what this does NOT close)
---------------------------------------
* The action's rank-one selection is established at the level of the transition
  KERNEL (epsilon_rank_one_kernel, epsilon_action_stationary). Deriving from the
  FULL CHO dynamics that the transition LOCALIZES to a coherent (minimal-orbit)
  state -- i.e. the coherent-state hypothesis itself -- remains open.
* The identification of the external Delta_9 (the gauge-spinor 16) with this
  internal tangent space is route 4c (epsilon_weyl_isomorphism); it is an
  isomorphism of Spin(9) modules, not yet a dynamical identity.
* "Minimal = coherent" is the standard coherent-state principle; this module does
  not re-derive geometric quantization. It shows that, GIVEN coherent-state
  quantization, the two minimal orbits are forced rather than chosen.

F0 is NOT promoted to DERIVED by this module. It converts the open bridge
"which two orbits (assumed)" into "the two MINIMAL orbits, forced by transitivity
(16) and the action's rank-one condition (27)".

Reuses the Spin(9)/J3(O) machinery; no scipy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_orbit_selection.py
"""

from __future__ import annotations

import math

import numpy as np

from epsilon_weyl_isomorphism import (
    clifford9_generators,
    so9_from_clifford,
    jordan_product_tensor,
    derivation_algebra,
)
from epsilon_symplectic_volume import spin9_spinor_count, e6_minimal_count

PI = math.pi
DIM_DELTA9 = 16
DIM_J3O = 27
DIM_ARENA = DIM_DELTA9 * DIM_J3O          # 432
TOL = 1e-7


# --------------------------------------------------------------------------- #
#  [16]  Spin(9) is transitive on the spinor sphere S^15 -> unique orbit       #
# --------------------------------------------------------------------------- #
def spin9_spinor_transitive(n_points: int = 8, seed: int = 0):
    """span{A_a v} at a unit spinor v is the orbit tangent; its dimension is 15
    (= dim S^15) at every point, so Spin(9) acts transitively on S^15 and the
    spinor orbit is UNIQUE (the 16 carries no 'which orbit' freedom).

    Returns (tangent_dims, stabiliser_dims, n_generators)."""
    so9 = np.asarray(so9_from_clifford(clifford9_generators())).real  # (36,16,16)
    n_gen = so9.shape[0]
    rng = np.random.default_rng(seed)
    tangent_dims = []
    for _ in range(n_points):
        v = rng.standard_normal(16)
        v /= np.linalg.norm(v)
        tangent = np.array([so9[a] @ v for a in range(n_gen)])      # (36,16)
        tangent_dims.append(int(np.linalg.matrix_rank(tangent, tol=1e-9)))
    stabiliser_dims = [n_gen - d for d in tangent_dims]
    return tangent_dims, stabiliser_dims, n_gen


# --------------------------------------------------------------------------- #
#  [27]  E6 minimal orbit = rank-one variety (Freudenthal sharp X# = 0)        #
# --------------------------------------------------------------------------- #
#
# Convention (epsilon_weyl_isomorphism.jordan_product_tensor): a J3(O) element is
# a 27-vector whose three diagonal real entries sit at indices 0,1,2; the
# identity is e0+e1+e2.  The Jordan product is (X o Y)_k = sum_ij T[k,i,j] X_i Y_j.
_T = jordan_product_tensor()
_IDENT = np.zeros(27)
_IDENT[0] = _IDENT[1] = _IDENT[2] = 1.0


def _jordan_square(x):
    return np.einsum("kij,i,j->k", _T, x, x)


def _trace(x):
    return x[0] + x[1] + x[2]


def freudenthal_sharp(x):
    """X# = X o X - tr(X) X + sigma2(X) I, with sigma2 = (tr(X)^2 - tr(X o X))/2.
    For a 3x3 Jordan algebra X# is (up to transpose) the matrix of cofactors, so
    X# = 0 iff X has rank <= 1.  This is the algebraic equation of the E6 minimal
    (rank-one) orbit -- the closure of the highest-weight orbit in the 27."""
    xsq = _jordan_square(x)
    t1 = _trace(x)
    sigma2 = 0.5 * (t1 * t1 - _trace(xsq))
    return xsq - t1 * x + sigma2 * _IDENT


def _diag(a, b, c):
    v = np.zeros(27)
    v[0], v[1], v[2] = a, b, c
    return v


def primitive_idempotents():
    """The three diagonal primitive (rank-one) idempotents E1,E2,E3 of J3(O).
    These are the three generations (epsilon_rank_one_kernel, Lever A): each is
    rank one, mutually orthogonal, and E1+E2+E3 = I."""
    return [_diag(1, 0, 0), _diag(0, 1, 0), _diag(0, 0, 1)]


def sharp_rank_one_table():
    """|X#| on representatives of each Jordan rank.  Rank one (the minimal orbit,
    = the action's selected primitive idempotents) gives X# = 0; higher ranks do
    not."""
    reps = {
        "E1 = diag(1,0,0)  rank1": _diag(1, 0, 0),
        "diag(2,0,0)       rank1": _diag(2, 0, 0),
        "diag(1,1,0)       rank2": _diag(1, 1, 0),
        "I = diag(1,1,1)   rank3": _diag(1, 1, 1),
    }
    return {name: float(np.linalg.norm(freudenthal_sharp(x))) for name, x in reps.items()}


# --------------------------------------------------------------------------- #
#  Orbit-tangent dimensions: rank-one is the MINIMAL orbit; f4-tangent = 16     #
# --------------------------------------------------------------------------- #
def _left_mult(x):
    """(L_X)_{k,j} = sum_i T[k,i,j] X_i, the Jordan left-multiplication matrix."""
    return np.einsum("kij,i->kj", _T, x)


def _e6_generators():
    """A basis of the reduced structure algebra e6(-26) = der(J) (+) {L_X : trX=0}
    acting on the real 27: 52 derivations (f4) plus 26 traceless left-multiplications."""
    f4, _ = derivation_algebra(_T)
    f4 = [np.asarray(g) for g in f4]
    traceless_dirs = [_diag(1, -1, 0), _diag(1, 1, -2)]
    traceless_dirs += [np.eye(27)[i] for i in range(3, 27)]
    boosts = [_left_mult(x) for x in traceless_dirs]
    return f4 + boosts, f4


def orbit_tangent_dim(generators, x):
    tangent = np.array([g @ x for g in generators])
    return int(np.linalg.matrix_rank(tangent, tol=1e-7))


def e6_orbit_dimensions():
    """Orbit-tangent dimensions under e6 and under f4 at rank-one vs higher rank.
    Rank-one is the MINIMAL nonzero e6-orbit, and the f4-orbit (OP^2 = F4/Spin(9))
    of a rank-one idempotent has tangent dimension 16 = Delta_9."""
    e6, f4 = _e6_generators()
    rank_one = _diag(1, 0, 0)
    rank_three = _diag(1, 1, 1)
    return {
        "n_e6": len(e6),
        "n_f4": len(f4),
        "e6_tangent_rank_one": orbit_tangent_dim(e6, rank_one),
        "e6_tangent_rank_three": orbit_tangent_dim(e6, rank_three),
        "f4_tangent_rank_one": orbit_tangent_dim(f4, rank_one),
    }


# --------------------------------------------------------------------------- #
#  Driver                                                                      #
# --------------------------------------------------------------------------- #
def main() -> bool:
    tangent_dims, stab_dims, n_gen = spin9_spinor_transitive()
    spin9 = spin9_spinor_count()
    e6 = e6_minimal_count()
    sharp = sharp_rank_one_table()
    orb = e6_orbit_dimensions()
    primitives = primitive_idempotents()

    # the action's selected vacua (rank-one primitive idempotents) all sit on the
    # E6 minimal (sharp-zero) orbit, and resolve the identity:
    prim_sharp = [float(np.linalg.norm(freudenthal_sharp(E))) for E in primitives]
    prim_sum = sum(primitives)
    prim_idempotent = [float(np.linalg.norm(_jordan_square(E) - E)) for E in primitives]

    bs_product = spin9["spinor"] * e6["fundamental_27"]

    print("=" * 78)
    print("  F0 ORBIT-SELECTION ROUTE")
    print("  WHICH two coadjoint orbits does the action quantize?")
    print("=" * 78)
    print()
    print("  [16]  Spin(9) is TRANSITIVE on the spinor sphere S^15  =>  one orbit")
    print("  " + "-" * 74)
    print(f"  orbit-tangent dim span{{A_a v}} over {len(tangent_dims)} unit spinors : {tangent_dims}")
    print(f"  stabiliser dim 36 - 15 = {n_gen} - 15                      : {stab_dims}")
    print(f"  15 = dim S^15, stabiliser 21 = dim Spin(7)  (Spin(9)/Spin(7) = S^15)")
    print(f"  => transitive => UNIQUE spinor orbit; the 16 is forced, not chosen.")
    print(f"  Bohr-Sommerfeld spinor count = {spin9['spinor']:>3}  "
          f"(checks: vector {spin9['vector']}, adjoint {spin9['adjoint']})")
    print()
    print("  [27]  E6 minimal orbit = rank-one variety (Freudenthal X# = 0)")
    print("  " + "-" * 74)
    width = max(len(k) for k in sharp)
    for name, val in sharp.items():
        flag = "X# = 0  (minimal orbit)" if val < TOL else "X# != 0"
        print(f"  |X#|  {name:<{width}} = {val:.3e}   {flag}")
    print(f"  the action's selected vacua = the 3 primitive idempotents E1,E2,E3:")
    print(f"     |E_i#|             = {[f'{v:.1e}' for v in prim_sharp]}  (all on minimal orbit)")
    print(f"     |E_i o E_i - E_i|  = {[f'{v:.1e}' for v in prim_idempotent]}  (idempotent)")
    print(f"     |E1+E2+E3 - I|     = {np.linalg.norm(prim_sum - _IDENT):.1e}  (resolve identity)")
    print(f"  rank-one is the action's OWN condition (epsilon_rank_one_kernel,")
    print(f"  epsilon_action_stationary): so 'which E6 orbit' is answered, not assumed.")
    print(f"  Bohr-Sommerfeld minimal count = {e6['fundamental_27']:>3}  (check: adjoint {e6['adjoint_78']})")
    print()
    print("  Interlock: the f4-orbit OP^2 = F4/Spin(9) of a rank-one idempotent")
    print("  " + "-" * 74)
    print(f"  e6-orbit tangent dim @ rank-one  = {orb['e6_tangent_rank_one']:>2}   (MINIMAL nonzero orbit)")
    print(f"  e6-orbit tangent dim @ rank-three= {orb['e6_tangent_rank_three']:>2}   (generic, larger)")
    print(f"  f4-orbit tangent dim @ rank-one  = {orb['f4_tangent_rank_one']:>2}   = dim Delta_9 = 16")
    print(f"  => the 16 is the tangent space at a point of the 27's minimal orbit,")
    print(f"     with isotropy Spin(9): the two minimal orbits are interlocked.")
    print()
    print("  Synthesis")
    print("  " + "-" * 74)
    print(f"  product of the two MINIMAL orbit counts = 16 x 27 = {bs_product}")
    print(f"  epsilon0^2 = pi / {bs_product} = {PI / bs_product:.10f}  (= pi/432)")
    print()

    checks = {
        "Spin(9) orbit-tangent dim = 15 at every point (transitive on S^15)":
            all(d == 15 for d in tangent_dims),
        "Spin(9) stabiliser dim = 21 = dim Spin(7) at every point":
            all(s == 21 for s in stab_dims),
        "Spin(9) spinor Bohr-Sommerfeld count = 16": spin9["spinor"] == DIM_DELTA9,
        "Spin(9) method checks (vector 9, adjoint 36)":
            spin9["vector"] == 9 and spin9["adjoint"] == 36,
        "Freudenthal sharp vanishes on rank-one (minimal orbit)":
            sharp["E1 = diag(1,0,0)  rank1"] < TOL and sharp["diag(2,0,0)       rank1"] < TOL,
        "Freudenthal sharp non-zero on rank-two and rank-three":
            sharp["diag(1,1,0)       rank2"] > TOL and sharp["I = diag(1,1,1)   rank3"] > TOL,
        "the 3 action-selected primitive idempotents are on the minimal orbit":
            all(v < TOL for v in prim_sharp),
        "the 3 primitive idempotents resolve the identity E1+E2+E3 = I":
            np.linalg.norm(prim_sum - _IDENT) < TOL,
        "E6 minimal coadjoint count = 27": e6["fundamental_27"] == DIM_J3O,
        "E6 method check (adjoint 78)": e6["adjoint_78"] == 78,
        "rank-one is the MINIMAL nonzero e6-orbit (17 < 26)":
            orb["e6_tangent_rank_one"] < orb["e6_tangent_rank_three"],
        "rank-one e6-orbit tangent dim = 17": orb["e6_tangent_rank_one"] == 17,
        "f4-orbit (OP^2) tangent at rank-one = 16 = dim Delta_9":
            orb["f4_tangent_rank_one"] == DIM_DELTA9,
        "product of minimal-orbit counts = 16 x 27 = 432": bs_product == DIM_ARENA,
    }
    width = max(len(k) for k in checks)
    for name, ok_ in checks.items():
        print(f"  [{'PASS' if ok_ else 'FAIL'}] {name:<{width}}")
    ok = all(checks.values())
    print()
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- the two orbits are the MINIMAL (coherent-state) orbits.")
    print("  BRIDGE STATUS: 'which two orbits (assumed)' is reduced to 'the two")
    print("                 minimal orbits, FORCED by Spin(9)-transitivity on S^15")
    print("                 (16) and the action's rank-one condition = E6 minimal")
    print("                 orbit (27)'. STILL OPEN: deriving coherent-state")
    print("                 localization from full CHO dynamics; the external-16")
    print("                 (Delta_9) identification. F0 NOT promoted.")
    print()

    # Stable arithmetic / geometric theorems (regression guards):
    assert all(d == 15 for d in tangent_dims)
    assert all(s == 21 for s in stab_dims)
    assert spin9["spinor"] == 16 and spin9["vector"] == 9 and spin9["adjoint"] == 36
    assert sharp["E1 = diag(1,0,0)  rank1"] < TOL
    assert sharp["diag(2,0,0)       rank1"] < TOL
    assert sharp["diag(1,1,0)       rank2"] > TOL
    assert sharp["I = diag(1,1,1)   rank3"] > TOL
    assert all(v < TOL for v in prim_sharp)
    assert np.linalg.norm(prim_sum - _IDENT) < TOL
    assert e6["fundamental_27"] == 27 and e6["adjoint_78"] == 78
    assert orb["e6_tangent_rank_one"] == 17
    assert orb["f4_tangent_rank_one"] == 16
    assert orb["e6_tangent_rank_one"] < orb["e6_tangent_rank_three"]
    assert bs_product == 432
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
