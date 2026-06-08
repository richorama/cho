"""
F0 product-irreducibility witness: the flat 1/432 does NOT need a separable
spurion. It removes the circular clauses of Assumption P.

Background
----------
`epsilon_measure_schur.py` proved the per-sector weights 1/16 (Spin(9) on
Delta_9) and 1/27 (E6 on J3(O)) are Schur-forced by irreducibility.
`epsilon_phase_space_product.py` then assembled pi/432 under

    Assumption P (original):
        the transition operator is equivariant under commuting Spin(9)/E6
        sector actions, with MINIMAL MULTIPLICITY one, and is a PRODUCT
        rank-one projector |u><u| (x) |v><v|.

`epsilon_assumption_p_gate.py` checks that the *scaffold* epsilon operator is
exactly product-separable -- but that operator was BUILT separable, so that gate
is partly circular: it confirms an input rather than deriving it.

What this module adds
---------------------
The "product projector" and "minimal multiplicity" clauses are REMOVABLE. For a
direct-product group G1 x G2 acting on irreducible modules V1, V2, the tensor
product V1 (x) V2 is itself IRREDUCIBLE, so by Schur the invariant average of
*any* operator -- separable OR maximally entangled -- is (tr / dim) * I:

    <P>_{Spin(9) x E6}  =  (tr P / 432) * I_432   for ANY rank-one P.

The product-group average factorizes through partial traces (no 432x432 group
element is ever built):

    <P>_{G1 x G2}  =  (1/16) I_16  (x)  < Tr_1 P >_{E6}
                   =  (1/16) I_16  (x)  (1/27) I_27  =  I_432 / 432.

Tests (all PASS)
----------------
[A] Sector irreducibility: commutant(so9,16)=1, commutant(e6,27)=1, and the
    F4 control commutant(f4,27)=2 (reducible 27 = 1 + 26).
[B] Entanglement-independence: a GENERIC ENTANGLED spurion (Schmidt rank 16)
    averages to I_432/432 to machine precision -- identical to a separable one.
[C] Separability is irrelevant: separable and entangled spurions give the SAME
    I_432/432, so the flat weight does NOT rest on the scaffold's separability
    (this is what breaks the circularity of `epsilon_assumption_p_gate.py`).
[D] Necessity: replacing the full E6 by its subgroup F4 BREAKS flatness on the
    27 leg (F4 is reducible there), so the factor-wise E6 invariance is doing
    real work -- the surviving assumption is non-vacuous.
[E] The pi weight: pi * (1/432) = pi/432 = epsilon0^2.

Net effect on the F0 ledger
---------------------------
Assumption P is REDUCED from three clauses to ONE:

    Assumption P (reduced):
        the transition measure is invariant under the factor-wise product group
        Spin(9) x E6 acting on Delta_9 (x) J3(O).

The separable-projector and minimal-multiplicity clauses are discharged; the
live seam is now exactly: derive that factor-wise product symmetry (equivalently
the 432-dimensional product arena) from the CHO action. The action S written in
foundations/02_action.md selects theta = pi on the two-level transition sphere
but does NOT supply the product arena, so this module does NOT promote F0 from
GEOMETRIC to DERIVED, and does NOT touch the scoreboard / model_complexity.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_product_irreducible.py
"""

from dataclasses import dataclass
import math

import numpy as np

from epsilon_measure_schur import commutant_basis, reynolds_average
from epsilon_weyl_isomorphism import (
    jordan_product_tensor,
    derivation_algebra,
    clifford9_generators,
    so9_from_clifford,
)

PI = math.pi
DIM_DELTA9 = 16
DIM_J3O = 27
DIM_BRIDGE = DIM_DELTA9 * DIM_J3O          # 432
TARGET = PI / DIM_BRIDGE                    # pi/432 = epsilon0^2
TOL = 1e-7
FLAT_TOL = 1e-9


@dataclass(frozen=True)
class GateRow:
    name: str
    passed: bool
    metric: str
    note: str


def _e6_generators(tensor):
    """E6 = Der(J3O) (=f4, dim 52) plus the 26 traceless Jordan left-mults."""
    f4, _ = derivation_algebra(tensor)
    dirs = []
    d1 = np.zeros(DIM_J3O); d1[0] = 1.0; d1[1] = -1.0; dirs.append(d1)
    d2 = np.zeros(DIM_J3O); d2[0] = 1.0; d2[1] = 1.0; d2[2] = -2.0; dirs.append(d2)
    for i in range(3, DIM_J3O):
        ei = np.zeros(DIM_J3O); ei[i] = 1.0; dirs.append(ei)
    traceless = [np.einsum('i,kij->kj', x, tensor) for x in dirs]
    return list(f4) + traceless, list(f4)


def _entangled_spurion(seed):
    """A normalized 432-vector whose (16x27) reshape has full Schmidt rank."""
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(DIM_BRIDGE)
    w /= np.linalg.norm(w)
    return w.reshape(DIM_DELTA9, DIM_J3O)


def _separable_spurion(seed):
    """A normalized 432-vector that is an exact product (Schmidt rank 1)."""
    rng = np.random.default_rng(seed)
    u = rng.standard_normal(DIM_DELTA9); u /= np.linalg.norm(u)
    v = rng.standard_normal(DIM_J3O); v /= np.linalg.norm(v)
    return np.outer(u, v)


def product_group_average(W, onb16, onb27):
    """Exact factor-wise (Spin(9) x E6)-invariant average of P = |w><w|.

    Uses the partial-trace factorization
        <P>_{G1 x G2} = (1/16) I_16 (x) <Tr_1 P>_{E6},
    so no 432x432 group element is constructed.  W is the (16 x 27) reshape of w.
    """
    reduced_27 = W.T @ W                       # Tr over the 16 leg -> 27 x 27
    avg27 = reynolds_average(reduced_27, onb27)
    return np.kron(np.eye(DIM_DELTA9) / DIM_DELTA9, avg27)


def main():
    tensor = jordan_product_tensor()
    so9 = so9_from_clifford(clifford9_generators())
    e6, f4 = _e6_generators(tensor)

    onb16, _ = commutant_basis(so9, DIM_DELTA9, tol=TOL)
    onb27_e6, _ = commutant_basis(e6, DIM_J3O, tol=TOL)
    onb27_f4, _ = commutant_basis(f4, DIM_J3O, tol=TOL)
    comm16, comm27_e6, comm27_f4 = len(onb16), len(onb27_e6), len(onb27_f4)

    I16 = np.eye(DIM_DELTA9) / DIM_DELTA9
    I27 = np.eye(DIM_J3O) / DIM_J3O
    I432 = np.eye(DIM_BRIDGE) / DIM_BRIDGE

    # Entangled spurion.
    W_ent = _entangled_spurion(seed=7)
    schmidt_ent = int(np.sum(np.linalg.svd(W_ent, compute_uv=False) > 1e-9))
    avg_ent = product_group_average(W_ent, onb16, onb27_e6)
    err_ent = float(np.max(np.abs(avg_ent - I432)))

    # Separable spurion (control).
    W_sep = _separable_spurion(seed=11)
    schmidt_sep = int(np.sum(np.linalg.svd(W_sep, compute_uv=False) > 1e-9))
    avg_sep = product_group_average(W_sep, onb16, onb27_e6)
    err_sep = float(np.max(np.abs(avg_sep - I432)))

    # Agreement between entangled and separable averages.
    err_match = float(np.max(np.abs(avg_ent - avg_sep)))

    # Per-leg Schur checks on the entangled spurion (both reductions average flat).
    red27 = W_ent.T @ W_ent
    red16 = W_ent @ W_ent.T
    err_leg27 = float(np.max(np.abs(reynolds_average(red27, onb27_e6) - I27)))
    err_leg16 = float(np.max(np.abs(reynolds_average(red16, onb16) - I16)))

    # Necessity: F4 (subgroup of E6) is reducible on 27, so it does NOT flatten.
    avg27_f4 = reynolds_average(red27, onb27_f4)
    err_f4 = float(np.max(np.abs(avg27_f4 - I27)))

    # pi weight.
    eps_sq = PI * float(np.mean(np.diag(avg_ent)))

    rows = [
        GateRow(
            "sectors irreducible (E6), F4 control reducible",
            comm16 == 1 and comm27_e6 == 1 and comm27_f4 == 2,
            f"commutant: so9/16={comm16}, e6/27={comm27_e6}, f4/27={comm27_f4}",
            "Spin(9) on Delta_9 and E6 on J3(O) irreducible; F4 splits 27 = 1 + 26",
        ),
        GateRow(
            "entangled spurion averages flat (1/432)",
            schmidt_ent > 1 and err_ent < FLAT_TOL,
            f"Schmidt rank={schmidt_ent}, max|<P>-I/432|={err_ent:.2e}",
            "a maximally entangled spurion still averages to I_432/432 by product irreducibility",
        ),
        GateRow(
            "separability is irrelevant (breaks circularity)",
            err_sep < FLAT_TOL and err_match < FLAT_TOL,
            f"sep err={err_sep:.2e}, |avg_ent-avg_sep|={err_match:.2e}",
            "separable and entangled spurions give the SAME flat average; the weight "
            "does not rest on the scaffold's built-in separability",
        ),
        GateRow(
            "per-leg Schur: both reductions flat",
            err_leg27 < FLAT_TOL and err_leg16 < FLAT_TOL,
            f"max|<Tr1 P>_E6-I/27|={err_leg27:.2e}, max|<Tr2 P>_Spin9-I/16|={err_leg16:.2e}",
            "the factorized average factor flattens each leg independently",
        ),
        GateRow(
            "necessity: F4 does NOT flatten the 27 leg",
            err_f4 > 1e-4,
            f"max|<Tr1 P>_F4-I/27|={err_f4:.2e}",
            "dropping E6 to its F4 subgroup breaks flatness, so factor-wise E6 invariance is required",
        ),
        GateRow(
            "pi weight gives pi/432",
            abs(eps_sq - TARGET) < 1e-12,
            f"pi*mean diag = {eps_sq:.10f}; target pi/432 = {TARGET:.10f}",
            "the Berry pi times the flat 1/432 reproduces epsilon0^2",
        ),
    ]

    print("=" * 78)
    print("  F0 PRODUCT-IRREDUCIBILITY WITNESS")
    print("  Removing the circular clauses of Assumption P")
    print("=" * 78)
    print()
    print("  Claim: Delta_9 (x) J3(O) is irreducible under the factor-wise product")
    print("  group Spin(9) x E6, so by Schur ANY rank-one spurion (separable or")
    print("  entangled) averages to I_432/432. The 'product projector' and 'minimal")
    print("  multiplicity' clauses of Assumption P are therefore removable.")
    print()
    print(f"  {'check':<48} {'status':<6} metric")
    print("  " + "-" * 74)
    for row in rows:
        print(f"  {row.name:<48} {'PASS' if row.passed else 'FAIL':<6} {row.metric}")
        print(f"      {row.note}")
    print()

    ok = all(row.passed for row in rows)
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- flat 1/432 holds for any spurion under factor-wise Spin(9) x E6.")
    print("  THEOREM STATUS: Assumption P REDUCED to one clause (factor-wise product")
    print("                  invariance). F0 NOT promoted: deriving that product arena")
    print("                  from the CHO action remains the live seam (foundations/02_action.md")
    print("                  selects theta=pi on the two-level sphere, not the 432 arena).")
    print()

    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
