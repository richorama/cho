"""
F0 product-phase-space witness: why Delta_9 x J3(O), and what remains open.

`epsilon_measure_schur.py` closed the normalization half of H4:
  * Spin(9) irreducibility on Delta_9 forces 1/16,
  * E6 irreducibility on J3(O) forces 1/27,
  * so the flat weight is pi * (1/16) * (1/27) = pi/432.

The remaining F0 seam is not those weights; it is the PRODUCT identification:

    phase space = Delta_9 x J3(O)

rather than, say, one fused carrier, a direct sum, or a hand-picked subspace.

This module makes one explicit structural assumption and pressure-tests it:

  Assumption P (independent sectors):
      the transition operator is equivariant under commuting actions of
      gauge/internal Spin(9) on Delta_9 and flavour/cubic E6 on J3(O),
      with minimal multiplicity one in each sector.

Under P, the canonical carrier is the tensor product Delta_9 x J3(O), and the
invariant average of a product rank-one projector factorizes:

    <|u><u| x |v><v|> = <|u><u|>_Spin(9) x <|v><v|>_E6
                       = (I_16/16) x (I_27/27)
                       = I_432/432.

So pi/432 follows mechanically from irreducibility + sector independence.

What this closes:
  * the normalization and factorization ONCE independent commuting sectors are
    granted.

What remains open (honest):
  * derive Assumption P itself from the CHO action / one-operator construction,
    rather than taking it as representation architecture.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_phase_space_product.py
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
TARGET = PI / (DIM_DELTA9 * DIM_J3O)
TOL = 1e-7


@dataclass(frozen=True)
class ProductCandidate:
    name: str
    dim: int
    note: str


def _jordan_traceless_multiplications(tensor):
    dirs = []
    d1 = np.zeros(DIM_J3O); d1[0] = 1.0; d1[1] = -1.0; dirs.append(d1)
    d2 = np.zeros(DIM_J3O); d2[0] = 1.0; d2[1] = 1.0; d2[2] = -2.0; dirs.append(d2)
    for i in range(3, DIM_J3O):
        ei = np.zeros(DIM_J3O); ei[i] = 1.0; dirs.append(ei)
    return [np.einsum('i,kij->kj', x, tensor) for x in dirs]


def _rank_one(d, idx=0):
    e = np.zeros(d)
    e[idx] = 1.0
    return np.outer(e, e)


def _measure_sectors():
    """Build sector generators and irreducibility witnesses."""
    so9 = so9_from_clifford(clifford9_generators())
    comm16, _ = commutant_basis(so9, DIM_DELTA9, tol=TOL)

    tensor = jordan_product_tensor()
    f4, _ = derivation_algebra(tensor)
    e6 = list(f4) + _jordan_traceless_multiplications(tensor)
    comm27, _ = commutant_basis(e6, DIM_J3O, tol=TOL)

    return so9, e6, len(comm16), len(comm27)


def _factorized_reynolds():
    """Compute sector averages and their tensor-product consequence."""
    so9 = so9_from_clifford(clifford9_generators())
    tensor = jordan_product_tensor()
    f4, _ = derivation_algebra(tensor)
    e6 = list(f4) + _jordan_traceless_multiplications(tensor)

    onb16, _ = commutant_basis(so9, DIM_DELTA9, tol=TOL)
    onb27, _ = commutant_basis(e6, DIM_J3O, tol=TOL)

    p16 = _rank_one(DIM_DELTA9)
    p27 = _rank_one(DIM_J3O)

    avg16 = reynolds_average(p16, onb16)
    avg27 = reynolds_average(p27, onb27)
    avg_prod = np.kron(avg16, avg27)

    target16 = np.eye(DIM_DELTA9) / DIM_DELTA9
    target27 = np.eye(DIM_J3O) / DIM_J3O
    target432 = np.eye(DIM_DELTA9 * DIM_J3O) / (DIM_DELTA9 * DIM_J3O)

    return {
        "err16": float(np.max(np.abs(avg16 - target16))),
        "err27": float(np.max(np.abs(avg27 - target27))),
        "err432": float(np.max(np.abs(avg_prod - target432))),
        "mean16": float(np.mean(np.diag(avg16))),
        "mean27": float(np.mean(np.diag(avg27))),
        "mean432": float(np.mean(np.diag(avg_prod))),
    }


def _compare_phase_space_candidates():
    """Dimension-level pressure test under sector-independence semantics."""
    cands = [
        ProductCandidate("tensor product Delta_9 x J3(O)", 16 * 27,
                         "independent sectors, minimal multiplicity one each"),
        ProductCandidate("direct sum Delta_9 (+) J3(O)", 16 + 27,
                         "sectors coexist but no bilinear cross-sector states"),
        ProductCandidate("J3(O) alone", 27,
                         "drops gauge/internal sector carrier"),
        ProductCandidate("Delta_9 alone", 16,
                         "drops flavour/cubic sector carrier"),
    ]
    return cands


def main():
    so9, e6, comm16, comm27 = _measure_sectors()
    fact = _factorized_reynolds()

    print("=" * 78)
    print("  F0 PRODUCT-PHASE-SPACE WITNESS")
    print("  Is Delta_9 x J3(O) structurally forced once sectors are independent?")
    print("=" * 78)
    print()
    print("  Assumption P: commuting, independent sector actions with minimal")
    print("                multiplicity one in each sector.")
    print()

    print("  [A] Sector irreducibility (already established, rechecked here)")
    print(f"      dim so(9) generators on Delta_9   : {len(so9)}")
    print(f"      commutant dim on Delta_9 (16)     : {comm16}  (1 = irreducible)")
    print(f"      dim e6 generators on J3(O)        : {len(e6)}")
    print(f"      commutant dim on J3(O) (27)       : {comm27}  (1 = irreducible)")
    print()

    print("  [B] Factorized Reynolds average under Assumption P")
    print(f"      max|<P16>-I/16|                   : {fact['err16']:.2e}")
    print(f"      max|<P27>-I/27|                   : {fact['err27']:.2e}")
    print(f"      max|<P16 x P27>-I/432|            : {fact['err432']:.2e}")
    print(f"      mean diag <P16 x P27>             : {fact['mean432']:.8f}")
    print(f"      target 1/432                      : {1.0/(16*27):.8f}")
    print(f"      pi * 1/432                        : {PI/(16*27):.8f}")
    print(f"      target pi/432                     : {TARGET:.8f}")
    print()

    print("  [C] Alternative phase-space architectures (dimension pressure test)")
    cands = _compare_phase_space_candidates()
    print(f"      {'candidate':<34} {'dim':>6}  note")
    print("      " + "-" * 68)
    for c in cands:
        print(f"      {c.name:<34} {c.dim:>6}  {c.note}")
    print()
    print("      Under Assumption P (independent sector labels that both act),")
    print("      only the tensor product carries both labels simultaneously with")
    print("      minimal multiplicity; direct-sum/single-sector options remove")
    print("      cross-sector transition states and cannot represent a shared")
    print("      one-operator transition density over both sectors.")
    print()

    checks = {
        "Spin(9) irreducible on Delta_9 (commutant 1)": comm16 == 1,
        "E6 irreducible on J3(O) (commutant 1)": comm27 == 1,
        "factorized average gives I/16": fact["err16"] < 1e-9,
        "factorized average gives I/27": fact["err27"] < 1e-9,
        "product average gives I/432": fact["err432"] < 1e-9,
        "pi-weighted value equals pi/432": abs(PI * fact["mean432"] - TARGET) < 1e-12,
    }
    width = max(len(k) for k in checks)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:<{width}}")
    ok_all = all(checks.values())
    print()
    print("  AUDIT STATUS:", "PASS" if ok_all else "FAIL",
          "- under Assumption P, Delta_9 x J3(O) yields the exact 1/432 factor.")
    print("  THEOREM STATUS: NORMALIZATION + FACTORIZATION CLOSED under sector")
    print("                  independence; the live F0 seam is deriving Assumption P")
    print("                  from the CHO action / one-operator dynamics.")
    print()

    return ok_all


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
