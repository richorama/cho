"""
F0 Schur witness: the 1/16 and 1/27 in epsilon0^2 = pi/432 are forced by
IRREDUCIBILITY, not chosen.

`epsilon_measure_audit.py` checks the *value* pi/432 and excludes nearby
alternatives. `epsilon_measure_witness.py` isolates the seam (H4) and keeps it
OPEN. This module attacks the *normalization half* of H4 with Schur's lemma.

The seam H4 reads:

    epsilon0^2 = (angular weight pi) x (normalized trace 1 / dim_phase_space)
               = pi x (1/16) x (1/27) = pi/432.

The angular pi is the Berry half-turn (epsilon_free_action). The open question
was the "1/dim" normalization: WHY is the invariant transition measure flat,
weight 1/dim per state, rather than some other invariant weighting?

Schur's lemma answers it. For a compact group G acting on a real module V of
dimension d, the unique G-invariant average of ANY rank-one projector P is

    <P>_G  =  (Reynolds projection of P onto the commutant of G).

If V is IRREDUCIBLE the commutant of symmetric operators is just {c*I}, so

    <P>_G  =  (tr P / d) * I  =  (1/d) * I        (flat, weight 1/d per state).

So "flat 1/dim" is a THEOREM whenever the module is irreducible -- nothing is
chosen. This module witnesses, with the project's own group-theory machinery:

  * SANITY  SO(5) on R^5 irreducible  -> average rank-1 projector = I/5.
  * 16 = Delta_9 under Spin(9) irreducible (commutant 1) -> weight 1/16.
  * 27 = J3(O) under F4 = Der(J3O) is REDUCIBLE (commutant 2, 27 = 1 + 26):
    F4 alone does NOT give a flat 1/27 -- the identity/trace direction keeps
    its own weight 1/3. F4 is insufficient.
  * 27 = J3(O) under the full E6 = f4 (+) traceless-L_X (dim 78, closes under
    bracket) is IRREDUCIBLE (commutant 1) -> flat weight 1/27. E6 is the
    reduced structure group preserving the cubic norm N3 (the Freudenthal
    determinant) -- the SAME invariant as the generation-cascade seesaw.

WHAT THIS CLOSES: the 1/16 and 1/27 normalizations are promoted from an
assumption (H4) to a Schur/irreducibility theorem. The flat measure is forced.

WHAT REMAINS OPEN (do not overclaim): why the transition phase space is the
PRODUCT Delta_9 (x) J3(O) with the two factors averaged independently. That is
a representation-identification, much sharper than "derive a measure", but it is
still the live F0 seam. F0 is NOT promoted to DERIVED by this module alone.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_measure_schur.py
"""

from dataclasses import dataclass
import math

import numpy as np

from epsilon_weyl_isomorphism import (
    jordan_product_tensor,
    derivation_algebra,
    closed_under_bracket,
    clifford9_generators,
    so9_from_clifford,
    _vec,
)
from epsilon_state_count import jordan_to_vec
from jordan_eigenvalue_generations import JordanElement

PI = math.pi
DIM_DELTA9 = 16
DIM_J3O = 27
DIM_F4 = 52
DIM_E6 = 78
TARGET = PI / (DIM_DELTA9 * DIM_J3O)   # = pi/432 = epsilon0^2
TOL = 1e-7


# --------------------------------------------------------------------------- #
#  Schur machinery: commutant + invariant (Reynolds) average                  #
# --------------------------------------------------------------------------- #
def commutant_basis(gens, d, tol=TOL):
    """Orthonormal basis of the commutant {X : [X, g] = 0 for all g}.

    Memory-cheap: accumulate the Gram G = sum_g B_g^T B_g on the d^2 space,
    where B_g vec(X) = vec(X g - g X) = (g^T (x) I - I (x) g) vec(X), then read
    off the null space.  Returns (orthonormal_matrices, sorted_eigenvalues).
    """
    eye = np.eye(d)
    gram = np.zeros((d * d, d * d))
    for g in gens:
        b = np.kron(g.T, eye) - np.kron(eye, g)
        gram += b.T @ b
    evals, evecs = np.linalg.eigh(gram)
    scale = max(evals[-1], 1.0)
    basis = [evecs[:, k].reshape(d, d) for k in range(d * d)
             if evals[k] <= tol * scale]
    # Frobenius orthonormalization
    onb = []
    for mat in basis:
        m = mat.astype(float).copy()
        for q in onb:
            m = m - np.sum(q * m) * q
        nrm = np.linalg.norm(m)
        if nrm > 1e-9:
            onb.append(m / nrm)
    return onb, evals


def reynolds_average(proj, onb):
    """Exact G-invariant average of `proj` = Frobenius projection onto the
    commutant span (Schur).  For an irreducible module this collapses to
    (tr proj / d) * I."""
    out = np.zeros_like(proj, dtype=float)
    for q in onb:
        out += np.sum(q * proj) * q
    return out


def _so5_generators():
    """The 10 antisymmetric basis matrices of so(5) acting on R^5 (irreducible)."""
    gens = []
    for i in range(5):
        for j in range(i + 1, 5):
            g = np.zeros((5, 5))
            g[i, j] = 1.0
            g[j, i] = -1.0
            gens.append(g)
    return gens


def _rank_one(d, idx=0):
    e = np.zeros(d)
    e[idx] = 1.0
    return np.outer(e, e)


# --------------------------------------------------------------------------- #
#  Witnesses                                                                   #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class WeightRow:
    module: str
    group: str
    commutant: int
    irreducible: bool
    weight: str
    note: str


def sanity_so5():
    """SO(5) on R^5 is irreducible -> average rank-one projector = I/5."""
    gens = _so5_generators()
    onb, _ = commutant_basis(gens, 5)
    avg = reynolds_average(_rank_one(5), onb)
    max_off = float(np.max(np.abs(avg - np.eye(5) / 5.0)))
    return len(onb), max_off


def weight_delta9():
    """16 = Delta_9 under Spin(9): irreducible -> flat 1/16."""
    gammas = clifford9_generators()
    so9 = so9_from_clifford(gammas)
    onb, _ = commutant_basis(so9, DIM_DELTA9)
    avg = reynolds_average(_rank_one(DIM_DELTA9), onb)
    mean_diag = float(np.mean(np.diag(avg)))
    max_off = float(np.max(np.abs(avg - np.eye(DIM_DELTA9) / DIM_DELTA9)))
    return len(onb), mean_diag, max_off


def _jordan_traceless_multiplications(tensor):
    """The 26 traceless Jordan left-multiplications L_X (X traceless in J3(O))."""
    dirs = []
    d1 = np.zeros(DIM_J3O); d1[0] = 1.0; d1[1] = -1.0; dirs.append(d1)
    d2 = np.zeros(DIM_J3O); d2[0] = 1.0; d2[1] = 1.0; d2[2] = -2.0; dirs.append(d2)
    for i in range(3, DIM_J3O):
        ei = np.zeros(DIM_J3O); ei[i] = 1.0; dirs.append(ei)
    return [np.einsum('i,kij->kj', x, tensor) for x in dirs]


def weight_j3o():
    """27 = J3(O): F4 alone is reducible (1 + 26); the full E6 is irreducible.

    Returns a dict with the F4 and E6 results plus the E6 closure checks.
    """
    tensor = jordan_product_tensor()
    f4, _ = derivation_algebra(tensor)
    l_traceless = _jordan_traceless_multiplications(tensor)
    e6 = list(f4) + l_traceless

    # E6 is genuinely the 78-dim Lie algebra: span + bracket closure
    e6_dim = int(np.linalg.matrix_rank(_vec(e6), tol=TOL))
    e6_bracket = float(closed_under_bracket(e6))

    proj = jordan_to_vec(JordanElement.diagonal(1.0, 0.0, 0.0))
    proj = np.outer(proj, proj) / float(proj @ proj)   # unit-trace rank one

    onb_f4, _ = commutant_basis(f4, DIM_J3O)
    avg_f4 = reynolds_average(proj, onb_f4)
    top_f4 = float(np.max(np.linalg.eigvalsh(avg_f4)))

    onb_e6, _ = commutant_basis(e6, DIM_J3O)
    avg_e6 = reynolds_average(proj, onb_e6)
    mean_e6 = float(np.mean(np.diag(avg_e6)))
    max_off_e6 = float(np.max(np.abs(avg_e6 - np.eye(DIM_J3O) / DIM_J3O)))

    return {
        "f4_commutant": len(onb_f4),
        "f4_top_weight": top_f4,
        "e6_commutant": len(onb_e6),
        "e6_mean_diag": mean_e6,
        "e6_max_off": max_off_e6,
        "e6_dim": e6_dim,
        "e6_bracket": e6_bracket,
    }


# --------------------------------------------------------------------------- #
#  Driver                                                                      #
# --------------------------------------------------------------------------- #
def main():
    so5_comm, so5_off = sanity_so5()
    d9_comm, d9_mean, d9_off = weight_delta9()
    j = weight_j3o()

    rows = [
        WeightRow("R^5  (sanity)", "SO(5)", so5_comm, so5_comm == 1,
                  "1/5", "textbook irreducible -> flat 1/5 (method check)"),
        WeightRow("Delta_9 = 16", "Spin(9)", d9_comm, d9_comm == 1,
                  "1/16", "chiral spinor irreducible -> flat 1/16"),
        WeightRow("J3(O) = 27", "F4 = Der", j["f4_commutant"],
                  j["f4_commutant"] == 1, "NOT flat",
                  f"reducible 1+26: identity keeps weight {j['f4_top_weight']:.3f}=1/3"),
        WeightRow("J3(O) = 27", "E6 (cubic)", j["e6_commutant"],
                  j["e6_commutant"] == 1, "1/27",
                  "irreducible -> flat 1/27 (full cubic-norm group)"),
    ]

    print("=" * 78)
    print("  F0 SCHUR WITNESS")
    print("  Are the 1/16 and 1/27 in epsilon0^2 = pi/432 FORCED by irreducibility?")
    print("=" * 78)
    print()
    print(f"  Schur: G-invariant average of a rank-one projector on an")
    print(f"         IRREDUCIBLE d-dim module = (tr/ d) * I = (1/d) * I  (flat).")
    print()
    print(f"  {'module':<14} {'group':<11} {'commutant':>9} {'irred':>6} "
          f"{'weight':>9}  note")
    print("  " + "-" * 74)
    for r in rows:
        print(f"  {r.module:<14} {r.group:<11} {r.commutant:>9} "
              f"{str(r.irreducible):>6} {r.weight:>9}  {r.note}")
    print()

    # E6 is genuinely the 78-dim Lie algebra
    print(f"  E6 closure:  dim span(f4 + traceless L_X) = {j['e6_dim']} "
          f"(= {DIM_E6}); bracket residual = {j['e6_bracket']:.1e}")
    print(f"  E6 average:  mean diag = {j['e6_mean_diag']:.6f}  "
          f"(1/27 = {1.0 / DIM_J3O:.6f}); max|<P> - I/27| = {j['e6_max_off']:.1e}")
    print(f"  Delta_9 avg: mean diag = {d9_mean:.6f}  "
          f"(1/16 = {1.0 / DIM_DELTA9:.6f}); max|<P> - I/16| = {d9_off:.1e}")
    print()

    product = (1.0 / DIM_DELTA9) * (1.0 / DIM_J3O)
    print(f"  PRODUCT:  pi x (1/16) x (1/27) = pi x {product:.8f} = "
          f"pi/{DIM_DELTA9 * DIM_J3O}")
    print(f"            = {PI * product:.8f}  ;  pi/432 = {TARGET:.8f}  "
          f"(= epsilon0^2)")
    print()

    checks = {
        "SO(5) sanity irreducible (commutant 1)": so5_comm == 1,
        "SO(5) average = I/5": so5_off < 1e-6,
        "Spin(9): Delta_9 irreducible (commutant 1)": d9_comm == 1,
        "Spin(9) forces flat 1/16": abs(d9_mean - 1.0 / DIM_DELTA9) < 1e-9
        and d9_off < 1e-9,
        "F4 reducible on 27 (commutant 2 = 1+26)": j["f4_commutant"] == 2,
        "F4 NOT flat (identity over-weighted ~1/3)": j["f4_top_weight"] > 0.3,
        "E6 = 78-dim Lie algebra (span + bracket)": j["e6_dim"] == DIM_E6
        and j["e6_bracket"] < 1e-7,
        "E6 irreducible on 27 (commutant 1)": j["e6_commutant"] == 1,
        "E6 forces flat 1/27": abs(j["e6_mean_diag"] - 1.0 / DIM_J3O) < 1e-9
        and j["e6_max_off"] < 1e-9,
        "product equals pi/432 = epsilon0^2": abs(PI * product - TARGET) < 1e-12,
    }
    width = max(len(k) for k in checks)
    for name, ok_ in checks.items():
        print(f"  [{'PASS' if ok_ else 'FAIL'}] {name:<{width}}")
    ok = all(checks.values())
    print()
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- the 1/16 and 1/27 are Schur theorems, not choices.")
    print("  THEOREM STATUS: H4 normalization CLOSED (irreducibility); the")
    print("                  product-phase-space identification Delta_9 (x) J3(O)")
    print("                  remains the live F0 seam. F0 not promoted here.")
    print()
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
