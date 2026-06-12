"""Flux-normalization uniqueness gate -- what forces the 1/432 in Phi = pi/432.

SCOPE (diagnostic / exploratory, QUARANTINED). The companion gates fixed the two
factors of the seed coupling:

    numerator   pi   -- exact Berry half-turn        (berry_halfturn_pi_gate.py)
    denominator 432  -- exact F4 -> Spin(9) breaking  (f4_breaking_vacuum_gate.py)

What was never analysed is the *division*: why is the coupling the flux divided by
the FULL carrier dimension 432, and not by some other normalisation? The existing
`wz_flux_normalization_gate.py` simply declared a "Schur weight 1/432" and admitted
"the hard theorem is still to show that the action normalises by the full carrier
rather than by a chosen trace." This gate proves -- exactly -- precisely what is and
is not forced, and corrects that earlier loose labelling.

The result splits cleanly:

  * The 1/16 IS forced by symmetry alone (Schur). The Spin(9) spinor Delta_9 is
    irreducible, so the ONLY Spin(9)-invariant normalised functional on End(Delta_9)
    is the trace Tr/16 -- invariance and traciality coincide.

  * The 1/27 is NOT forced by symmetry. J3(O) is REDUCIBLE under Spin(9)
    (= 1 + 1 + 9 + 16), so its commutant is 6-dimensional and there is a whole
    5-parameter family of Spin(9)-invariant normalised functionals on End(J3(O)).
    The democratic Tr/27 is singled out among them by being the unique TRACIAL one
    (a central density => scalar). Traciality (= full unitary invariance = the
    maximally-mixed carrier state = maximal entropy) is a strictly stronger,
    distinct principle from mere Spin(9) invariance.

  * On the whole carrier End(C) = M_432 the unique normalised tracial state is
    Tr/432 (unique-trace theorem: the commutators span the codimension-one traceless
    subspace). So once "democracy" is adopted the value pi/432 has no remaining free
    continuous parameter.

PROVED (exact, asserted; standalone EXIT 0; full sweep PASS):
  [A] On M_n the span of commutators is exactly the traceless subspace (dim n^2-1),
      verified for n=2..6; hence the normalised tracial functional is unique = Tr/n.
  [C] Delta_9 (the 16-dim Peirce-1/2 space of E11) is irreducible under Spin(9):
      its commutant is exactly 1-dimensional -> 1/16 is Schur-forced.
  [D] J3(O) (27) is reducible under Spin(9): commutant dimension exactly 6, with
      exactly 2 invariant vectors (E11 and E22+E33) -> 1/27 is NOT Schur-forced and
      needs the traciality/democracy principle.
  [E] Phi = pi * (1/432); 16 Schur-forced, 27 (hence 432) tracial/democracy-forced.

OPEN: that CHO dynamics SELECTS the democratic (tracial / maximally-mixed) trace
over the other 5 parameters of Spin(9)-invariant normalisations. This gate pins the
residual freedom in the *value* down to exactly that ONE named principle.

KILL: had Delta_9's commutant not been 1 (16 not Schur-forced) or had J3(O)'s
commutant been 1 (27 already forced by invariance, making democracy unnecessary),
the clean "16 = Schur, 27 = democracy" split would be false.

Diagnostic only; moves no Bayes credit; the scoreboard stays parked.
"""

from __future__ import annotations

from fractions import Fraction as Fr
from math import pi

from f4_breaking_vacuum_gate import (
    DIM,
    apply_op,
    build_f4,
    frame_idempotent,
    nullspace,
    PEIRCE_HALF_E11,
    reduce_into_basis,
)

SPIN9_SPINOR_DIM = 16
J3O_DIM = 27
CARRIER_DIM = SPIN9_SPINOR_DIM * J3O_DIM   # 432


# --------------------------------------------------------------------------
# [A] The unique-trace theorem core.
# --------------------------------------------------------------------------

def commutator_span_dim(n: int) -> int:
    """Dimension of span{ [A, B] : A, B in M_n }.

    Uses the matrix units: [E_ij, E_kl] = d_jk E_il - d_li E_kj.  The off-diagonal
    units E_il (i != l) appear as [E_ij, E_jl], and the traceless diagonals
    E_ii - E_jj appear as [E_ij, E_ji]; Tr([A,B]) = 0 always.  So the span is the
    traceless subspace, of dimension n^2 - 1.
    """
    rows: list[list[Fr]] = []
    pivots: list[int] = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    vec = [Fr(0)] * (n * n)
                    if j == k:
                        vec[i * n + l] += Fr(1)
                    if l == i:
                        vec[k * n + j] -= Fr(1)
                    reduce_into_basis(rows, pivots, vec)
    return len(rows)


# --------------------------------------------------------------------------
# [B] Spin(9) = stabiliser of the primitive idempotent E11 in F4 = Der(J3(O)).
# --------------------------------------------------------------------------

def build_spin9() -> list[list[list[Fr]]]:
    """The 36-dim unbroken subalgebra h = { D in f4 : D(E11) = 0 } as 27x27 gens.

    Reconstructed from the exposed f4_breaking primitives (the stabiliser itself is
    built inside that module's main()); see f4_breaking_vacuum_gate.py for the full
    spontaneous F4 -> Spin(9) analysis this relies on.
    """
    f4 = build_f4()
    e11 = frame_idempotent(0)
    images = [apply_op(D, e11) for D in f4]
    image_map = [[images[k][r] for k in range(len(f4))] for r in range(DIM)]
    stab_coords = nullspace(image_map, len(f4))
    gens: list[list[list[Fr]]] = []
    for coords in stab_coords:
        acc = [[Fr(0)] * DIM for _ in range(DIM)]
        for k, ck in enumerate(coords):
            if ck:
                Dk = f4[k]
                for i in range(DIM):
                    row, drow = acc[i], Dk[i]
                    for j in range(DIM):
                        if drow[j]:
                            row[j] += ck * drow[j]
        gens.append(acc)
    return gens


# --------------------------------------------------------------------------
# Commutant and invariants of a set of generators on a (sub)space.
# --------------------------------------------------------------------------

def commutant_dim(gens: list[list[list[Fr]]], sub: list[int]) -> int:
    """dim { M on span(sub) : [G, M] = 0 for all generators G }.

    sub indexes an invariant coordinate subspace; the constraint [G, M]_ij = 0
    expands to  sum_a G_ia M_aj - sum_b M_ib G_bj = 0.  The commutant dimension is
    |sub|^2 minus the rank of all such constraint rows.  (The identity always
    commutes, so the rank never exceeds |sub|^2 - 1; we stop early there.)
    """
    d = len(sub)
    rows: list[list[Fr]] = []
    pivots: list[int] = []
    ceiling = d * d - 1
    for G in gens:
        g = [[G[a][b] for b in sub] for a in sub]
        for i in range(d):
            for j in range(d):
                row = [Fr(0)] * (d * d)
                for a in range(d):
                    row[a * d + j] += g[i][a]
                for b in range(d):
                    row[i * d + b] -= g[b][j]
                reduce_into_basis(rows, pivots, row)
        if len(rows) >= ceiling:
            break
    return d * d - len(rows)


def invariant_vectors(gens: list[list[list[Fr]]]) -> list[list[Fr]]:
    """Basis of { v : G v = 0 for all generators G } -- the trivial isotypic part."""
    stacked: list[list[Fr]] = []
    for G in gens:
        stacked.extend(G)
    return nullspace(stacked, DIM)


def main() -> bool:
    print("=" * 78)
    print("FLUX-NORMALIZATION UNIQUENESS GATE -- what forces the 1/432")
    print("=" * 78)

    # [A] unique normalised trace -----------------------------------------
    print("\n[A] Unique normalised trace on M_n (the democracy principle)")
    for n in (2, 3, 4, 5, 6):
        d = commutator_span_dim(n)
        assert d == n * n - 1, f"commutator span for n={n} is {d}, expected {n*n-1}"
        print(f"    n={n:>2}: dim span[A,B] = {d:>3} = n^2-1  (commutators = traceless)")
    print("    => the only normalised tracial functional on M_n is Tr/n.")
    print(f"    => on End(carrier) = M_{CARRIER_DIM} the unique tracial state is "
          f"Tr/{CARRIER_DIM}")
    print("       (= the maximally-mixed carrier state = equal weight on all modes).")

    # [B] Spin(9) generators ----------------------------------------------
    print("\n[B] Spin(9) = Stab(E11) in F4 = Der(J3(O))")
    spin9 = build_spin9()
    assert len(spin9) == 36, f"Spin(9) should be 36-dimensional, got {len(spin9)}"
    assert frame_idempotent(0) == [Fr(1)] + [Fr(0)] * (DIM - 1)
    print(f"    built {len(spin9)} generators (dim Spin(9) = 36); E11 = e_0.")

    # [C] the 16 is Schur-forced ------------------------------------------
    print("\n[C] The 16 (Delta_9) is Schur-forced")
    spinor_comm = commutant_dim(spin9, PEIRCE_HALF_E11)
    assert spinor_comm == 1, f"Delta_9 commutant should be 1, got {spinor_comm}"
    print(f"    Delta_9 = Peirce-1/2 of E11 (indices {PEIRCE_HALF_E11[0]}.."
          f"{PEIRCE_HALF_E11[-1]}), commutant dim = {spinor_comm}")
    print("    => Delta_9 is irreducible; invariance ALONE forces the trace Tr/16")
    print("       (invariant and tracial functionals coincide). The 1/16 is forced.")

    # [D] the 27 is NOT Schur-forced --------------------------------------
    print("\n[D] The 27 (J3(O)) is NOT Schur-forced")
    inv = invariant_vectors(spin9)
    assert len(inv) == 2, f"J3(O) should have 2 invariant vectors, got {len(inv)}"
    supports = []
    for v in inv:
        supports.append([i for i in range(DIM) if v[i] != 0])
    j3o_comm = commutant_dim(spin9, list(range(DIM)))
    assert j3o_comm == 6, f"J3(O) commutant should be 6, got {j3o_comm}"
    print(f"    invariant vectors = {len(inv)}  (supports {supports[0]} and "
          f"{supports[1]} = E11 and E22+E33)")
    print(f"    commutant dim = {j3o_comm} = 2^2+1^2+1^2  => J3(O) = 1 + 1 + 9 + 16")
    print("    => J3(O) is reducible; Spin(9)-invariant normalised functionals form")
    print(f"       a {j3o_comm - 1}-parameter family. The democratic Tr/27 is the")
    print("       UNIQUE tracial one (a central density is scalar). 1/27 needs")
    print("       traciality/democracy, NOT just invariance.")

    # [E] synthesis -------------------------------------------------------
    weight = Fr(1, CARRIER_DIM)
    print("\n[E] The coefficient")
    print(f"    half-turn flux (berry_halfturn)      : pi")
    print(f"    carrier 16 x 27 (f4_breaking_vacuum) : {CARRIER_DIM}")
    print(f"    unique tracial normalisation         : 1/{CARRIER_DIM}")
    print(f"    Phi = pi * {weight}  (16 Schur-forced; 27 democracy-forced)")
    assert weight == Fr(1, 432)
    assert SPIN9_SPINOR_DIM * J3O_DIM == 432

    print("\n[V] Sandbox verdict")
    print("    commutators span traceless (unique trace Tr/n)    : PASS")
    print("    Delta_9 irreducible (commutant 1) => 1/16 Schur    : PASS")
    print("    J3(O) reducible (commutant 6) => 1/27 needs democ. : PASS")
    print("    value pi/432 has no free continuous parameter      : given democracy")
    print("    CHO dynamics selects the democratic trace          : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
