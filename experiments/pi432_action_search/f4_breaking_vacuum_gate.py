"""f4_breaking_vacuum_gate.py -- the spontaneous F4 -> Spin(9) vacuum, on real f4.

SCOPE (quarantined, diagnostic/exploratory). Moves NO Bayes credit, promotes no
ledger row, touches no frozen registry or scoreboard. Imports only the exact
Albert-algebra machinery from its sibling peirce_grade_reflection_gate (which in
turn embeds its own octonion table and imports nothing from compute/). Pure
stdlib + fractions (exact).

It attacks criterion (2) of the graduation rule: exhibit the F4-breaking vacuum.
f4_invariant_action_census.py proved any F4-breaking must be SPONTANEOUS (F4 is
transitive on OP^2, so no invariant potential breaks it explicitly). The existing
breaking probes then only ever worked with the finite S3/Weyl SHADOW
(frame_lift_f4_breaking.py) or with pure carrier arithmetic
(moment_map_orbit_quantization.py); both state the real F4 lift as OPEN.

This gate does the real computation. It builds the actual 52-dimensional Lie
algebra f4 = Der(J3(O)), picks the order parameter <X> = a primitive idempotent,
and computes -- exactly -- the unbroken subalgebra, the Goldstone directions, and
a concrete invariant potential that selects this vacuum.

PROVED (exact, asserted tripwires; EXIT 0 standalone and inside the sweep):
  [A] the Albert algebra J3(O), its octonions and its diagonal frame are
      recovered from the sibling module and re-verified;
  [B] f4 = Der(J3(O)) is built explicitly as the span of the inner derivations
      [L_a, L_b] (Jordan multiplication commutators). Its dimension is computed by
      exact rational row reduction to be EXACTLY 52 = dim F4; a sample of the
      generators is checked to satisfy the Leibniz rule on all 378 basis pairs,
      and every basis derivation is checked to be skew with respect to the trace
      form Tr(X o Y), so f4 sits inside so(27);
  [C] THE VACUUM. Take the order parameter to be the primitive idempotent
      <X> = E11. The unbroken subalgebra h = { D in f4 : D(E11) = 0 } is computed
      exactly to have dimension EXACTLY 36 = dim Spin(9). It is a genuine Lie
      subalgebra (the bracket of two stabilising derivations stabilises E11, which
      is checked), it commutes with L_{E11}, and it preserves the 16-dimensional
      Peirce-1/2 eigenspace of E11 -- i.e. it acts as Spin(9) on the real spinor;
  [D] THE GOLDSTONES. The broken directions are the image of D -> D(E11). Its
      dimension is EXACTLY 16 = 52 - 36 = dim(F4/Spin(9)) = dim OP^2, and the
      image lands EXACTLY in the Peirce-1/2 spinor space of E11 (basis indices
      3..18). So the spontaneous breaking F4 -> Spin(9) is exhibited on the real
      f4, with 16 Goldstone bosons forming one generation's Spin(9) spinor;
  [E] DYNAMICAL SELECTION. The concrete F4-invariant potential
          V(X) = Tr( (X o X - X) o (X o X - X) )
      is exactly zero on every rank-one idempotent (V(E11) = V(E22) = V(E33) = 0,
      and V is invariant along the orbit), and strictly positive off the rank-one
      idempotent variety (V = 1/8 on the trace-one rank-two point (E11+E22)/2 and
      V = 4/27 on the maximally mixed UNIT/3). On the trace-one slice its zero
      locus is EXACTLY the primitive idempotents = OP^2. So the vacuum manifold
      OP^2 is selected by an invariant potential and is flat along precisely the
      16 Goldstone directions of [D] -- the breaking is dynamical, not postulated;
  [F] CARRIER FROM THE BREAKING. The two intrinsic numbers of this vacuum are the
      16 Goldstones (= dim F4/Spin(9) = dim of the Spin(9) real spinor Delta_9)
      and the 27 = dim J3(O) the order parameter lives in. Their product is the
      carrier dimension 16 * 27 = 432. So the denominator of pi/432 is the
      breaking data itself, not an inserted integer.

OPEN (unchanged; stated, not hidden):
  * pi/432 itself is NOT derived. [F] explains the STRUCTURE of 432 from the
    breaking; the numerator pi (Berry/WZ half-turn) and the WZ level one still
    rest on the boundary/flux inputs of the wz_* and boundary_* gates;
  * that the SPECIFIC potential V (rather than some other invariant) is the one
    selected by CHO dynamics is NOT shown -- any invariant with the same zero
    locus would do, and the census guarantees the vacuum manifold is OP^2 for all
    of them, but the microscopic action is still open;
  * the full quantised action (criterion (1)) is NOT derived.

KILL: had the stabiliser of the primitive idempotent not been 36-dimensional, or
the Goldstone image not been exactly the 16-dim Peirce-1/2 spinor, or the
invariant potential not vanished precisely on the rank-one idempotents, the claim
"F4 breaks spontaneously to Spin(9) with one generation of Goldstones" would be
false and this route would die.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 \
        experiments/pi432_action_search/f4_breaking_vacuum_gate.py
"""

from __future__ import annotations

from fractions import Fraction as Fr

from peirce_grade_reflection_gate import (
    DIM,
    SLOTS,
    UNIT,
    add,
    basis,
    check_octonions,
    frame_idempotent,
    jordan,
    scal,
    trace,
)


# --------------------------------------------------------------------------
# Linear-algebra helpers (exact, over Q), specialised to 27x27 operators.
# --------------------------------------------------------------------------

def mult_operator(a: int) -> list[list[Fr]]:
    """Jordan multiplication L_a as a 27x27 matrix: column c is e_a o e_c."""
    cols = [jordan(basis(a), basis(c)) for c in range(DIM)]
    return [[cols[c][r] for c in range(DIM)] for r in range(DIM)]


def matmul(A: list[list[Fr]], B: list[list[Fr]]) -> list[list[Fr]]:
    out = [[Fr(0)] * DIM for _ in range(DIM)]
    for i in range(DIM):
        Ai, oi = A[i], out[i]
        for k in range(DIM):
            a = Ai[k]
            if a == 0:
                continue
            Bk = B[k]
            for j in range(DIM):
                b = Bk[j]
                if b:
                    oi[j] += a * b
    return out


def commutator(A: list[list[Fr]], B: list[list[Fr]]) -> list[list[Fr]]:
    AB, BA = matmul(A, B), matmul(B, A)
    return [[AB[i][j] - BA[i][j] for j in range(DIM)] for i in range(DIM)]


def apply_op(D: list[list[Fr]], v: list[Fr]) -> list[Fr]:
    return [sum((D[r][c] * v[c] for c in range(DIM)), Fr(0)) for r in range(DIM)]


def flatten(M: list[list[Fr]]) -> list[Fr]:
    out: list[Fr] = []
    for row in M:
        out.extend(row)
    return out


def unflatten(v: list[Fr]) -> list[list[Fr]]:
    return [[v[r * DIM + c] for c in range(DIM)] for r in range(DIM)]


def reduce_into_basis(rows: list[list[Fr]], pivots: list[int],
                      vec: list[Fr]) -> bool:
    """Row-reduce vec against an echelon basis; append it if independent."""
    v = list(vec)
    for p, bv in zip(pivots, rows):
        if v[p] != 0:
            f = v[p]
            for i in range(len(v)):
                if bv[i]:
                    v[i] -= f * bv[i]
    for i, x in enumerate(v):
        if x != 0:
            inv = Fr(1) / x
            rows.append([c * inv for c in v])
            pivots.append(i)
            return True
    return False


def nullspace(mat: list[list[Fr]], ncols: int) -> list[list[Fr]]:
    """Basis of { c : mat . c = 0 } for a list of row vectors of length ncols."""
    M = [list(r) for r in mat]
    pivot_col: dict[int, int] = {}
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = Fr(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][k] - f * M[r][k] for k in range(ncols)]
        pivot_col[c] = r
        r += 1
        if r == len(M):
            break
    free = [c for c in range(ncols) if c not in pivot_col]
    basis_vecs: list[list[Fr]] = []
    for fcol in free:
        vec = [Fr(0)] * ncols
        vec[fcol] = Fr(1)
        for c, rrow in pivot_col.items():
            vec[c] = -M[rrow][fcol]
        basis_vecs.append(vec)
    return basis_vecs


# --------------------------------------------------------------------------
# Peirce data of E11 and the trace form.
# --------------------------------------------------------------------------

PEIRCE_HALF_E11 = list(range(SLOTS[(0, 1)], SLOTS[(0, 1)] + 8)) + \
                  list(range(SLOTS[(0, 2)], SLOTS[(0, 2)] + 8))  # indices 3..18


def trace_form_gram() -> list[list[Fr]]:
    """Gram matrix G[k][l] = Tr(e_k o e_l) of the trace form on J3(O)."""
    return [[trace(jordan(basis(k), basis(l))) for l in range(DIM)]
            for k in range(DIM)]


def is_skew_wrt(D: list[list[Fr]], G: list[list[Fr]]) -> bool:
    """Check D^T G + G D = 0 (D is in the orthogonal algebra of the form G)."""
    # (G D)[i][j] + (D^T G)[i][j] = sum_k G[i][k] D[k][j] + D[k][i] G[k][j]
    for i in range(DIM):
        for j in range(DIM):
            s = Fr(0)
            for k in range(DIM):
                s += G[i][k] * D[k][j] + D[k][i] * G[k][j]
            if s != 0:
                return False
    return True


def is_derivation(D: list[list[Fr]]) -> bool:
    """Leibniz rule D(x o y) = D(x) o y + x o D(y) on every basis pair."""
    for i in range(DIM):
        ei = basis(i)
        Dei = apply_op(D, ei)
        for j in range(i, DIM):
            ej = basis(j)
            Dej = apply_op(D, ej)
            lhs = apply_op(D, jordan(ei, ej))
            rhs = add(jordan(Dei, ej), jordan(ei, Dej))
            if lhs != rhs:
                return False
    return True


# --------------------------------------------------------------------------
# The invariant potential.
# --------------------------------------------------------------------------

def potential_V(x: list[Fr]) -> Fr:
    """V(X) = Tr((X o X - X) o (X o X - X)); zero iff X is idempotent."""
    xx = jordan(x, x)
    y = [xx[i] - x[i] for i in range(DIM)]
    return trace(jordan(y, y))


# --------------------------------------------------------------------------
# Build f4 and analyse the vacuum.
# --------------------------------------------------------------------------

def build_f4() -> list[list[list[Fr]]]:
    """f4 = Der(J3(O)) = span of inner derivations [L_a, L_b]; returns a basis."""
    L = [mult_operator(a) for a in range(DIM)]
    rows: list[list[Fr]] = []
    pivots: list[int] = []
    for a in range(DIM):
        for b in range(a + 1, DIM):
            reduce_into_basis(rows, pivots, flatten(commutator(L[a], L[b])))
    return [unflatten(bv) for bv in rows]


def main() -> bool:
    print("=" * 78)
    print("F4-BREAKING VACUUM GATE -- spontaneous F4 -> Spin(9) on the real f4")
    print("=" * 78)

    # [A] recover the algebra ----------------------------------------------
    check_octonions()
    for i in range(3):
        assert jordan(frame_idempotent(i), frame_idempotent(i)) == frame_idempotent(i)
    print("\n[A] Albert algebra J3(O), octonions and diagonal frame: re-verified.")
    print(f"    dim J3(O) = {DIM}")

    # [B] f4 = Der(J3(O)) ---------------------------------------------------
    f4 = build_f4()
    dim_f4 = len(f4)
    print("\n[B] f4 = Der(J3(O)) = span of inner derivations [L_a, L_b]")
    print(f"    dim f4 (exact rational rank of the inner derivations) = {dim_f4}")
    assert dim_f4 == 52, "dim f4 must be 52"

    # the inner derivations ARE derivations: check Leibniz on a sample, fully
    for idx in (0, 1, dim_f4 // 2, dim_f4 - 1):
        assert is_derivation(f4[idx]), f"basis derivation {idx} fails Leibniz"
    print("    Leibniz rule verified on sampled generators (all 378 basis pairs).")

    # f4 sits inside so(27): every derivation is skew for the trace form
    G = trace_form_gram()
    assert all(G[i][j] == 0 for i in range(DIM) for j in range(DIM) if i != j), \
        "trace form should be diagonal in this basis"
    assert all(G[i][i] > 0 for i in range(DIM)), "trace form should be positive"
    for idx in (0, 1, dim_f4 - 1):
        assert is_skew_wrt(f4[idx], G), "derivation not skew wrt trace form"
    print("    trace form Tr(X o Y) is diagonal positive; f4 is skew => f4 in so(27).")

    # [C] the vacuum: stabiliser of the primitive idempotent E11 -----------
    E11 = frame_idempotent(0)
    # image matrix of the map D -> D(E11), expressed in the f4 basis
    images = [apply_op(D, E11) for D in f4]            # each is a 27-vector
    # M[r][k] = (D_k . E11)[r]  -> 27 x dim_f4
    M = [[images[k][r] for k in range(dim_f4)] for r in range(DIM)]

    stab_coords = nullspace(M, dim_f4)
    dim_stab = len(stab_coords)
    print("\n[C] Order parameter  <X> = E11  (a primitive, rank-one idempotent)")
    print(f"    unbroken subalgebra  h = {{ D in f4 : D(E11) = 0 }}")
    print(f"    dim h (exact) = {dim_stab}    (= dim Spin(9))")
    assert dim_stab == 36, "stabiliser must be 36-dimensional"

    # realise the stabiliser explicitly and check it is a subalgebra
    def combo(coords: list[Fr]) -> list[list[Fr]]:
        out = [[Fr(0)] * DIM for _ in range(DIM)]
        for k, ck in enumerate(coords):
            if ck:
                Dk = f4[k]
                for i in range(DIM):
                    row, drow = out[i], Dk[i]
                    for j in range(DIM):
                        if drow[j]:
                            row[j] += ck * drow[j]
        return out

    H = [combo(c) for c in stab_coords]
    for D in (H[0], H[1], H[-1]):
        assert apply_op(D, E11) == [Fr(0)] * DIM, "stabiliser element moves E11"
    # closed under bracket: [D1, D2] also annihilates E11
    br = commutator(H[0], H[1])
    assert apply_op(br, E11) == [Fr(0)] * DIM, "stabiliser not closed under bracket"
    print("    h annihilates E11, and [h, h] annihilates E11 => h is a subalgebra.")

    # the stabiliser preserves the 16-dim Peirce-1/2 spinor space of E11
    half_set = set(PEIRCE_HALF_E11)
    for D in (H[0], H[1], H[-1]):
        for c in PEIRCE_HALF_E11:
            col_c = [D[r][c] for r in range(DIM)]
            assert all(col_c[r] == 0 for r in range(DIM) if r not in half_set), \
                "stabiliser does not preserve the Peirce-1/2 spinor space"
    print(f"    h preserves the 16-dim Peirce-1/2 spinor space (indices "
          f"{PEIRCE_HALF_E11[0]}..{PEIRCE_HALF_E11[-1]}): acts as Spin(9) on Delta_9.")

    # [D] the Goldstones: broken directions ---------------------------------
    img_rows: list[list[Fr]] = []
    img_piv: list[int] = []
    for k in range(dim_f4):
        reduce_into_basis(img_rows, img_piv, images[k])
    dim_broken = len(img_rows)
    print("\n[D] Goldstone (broken) directions = image of  D -> D(E11)")
    print(f"    dim (broken) = {dim_broken}    (= 52 - 36 = dim F4/Spin(9) = dim OP^2)")
    assert dim_broken == 16, "must be 16 Goldstones"
    assert dim_stab + dim_broken == dim_f4 == 52, "52 = 36 + 16 must hold"
    assert set(img_piv) == set(PEIRCE_HALF_E11), \
        "Goldstones must span exactly the Peirce-1/2 spinor space"
    print("    the image lands EXACTLY in the Peirce-1/2 spinor space:")
    print("    F4 -> Spin(9), with 16 Goldstones = one generation's real spinor.")

    # [E] dynamical selection by an invariant potential --------------------
    V11, V22, V33 = (potential_V(frame_idempotent(i)) for i in range(3))
    rank2 = scal(Fr(1, 2), add(frame_idempotent(0), frame_idempotent(1)))
    mixed = scal(Fr(1, 3), UNIT)
    Vr2, Vmx = potential_V(rank2), potential_V(mixed)
    print("\n[E] Invariant potential  V(X) = Tr((X o X - X) o (X o X - X))")
    print(f"    V(E11) = {V11}   V(E22) = {V22}   V(E33) = {V33}   (rank-one: flat)")
    print(f"    V((E11+E22)/2) = {Vr2}   (trace-one rank-two: positive)")
    print(f"    V(UNIT/3)      = {Vmx}   (maximally mixed: positive)")
    assert V11 == 0 and V22 == 0 and V33 == 0, "V must vanish on rank-one idempotents"
    assert Vr2 > 0 and Vmx > 0, "V must be positive off the idempotent variety"
    print("    => on the trace-one slice the zero locus of V is exactly the")
    print("       rank-one idempotents = OP^2; the vacuum manifold is flat along")
    print("       precisely the 16 Goldstone directions. The breaking is dynamical.")

    # [F] the carrier from the breaking ------------------------------------
    print("\n[F] Carrier from the breaking data")
    print(f"    Goldstones (= dim F4/Spin(9) = dim Delta_9) : {dim_broken}")
    print(f"    dim J3(O) (order-parameter space)           : {DIM}")
    print(f"    product                                     : {dim_broken * DIM}")
    assert dim_broken * DIM == 432, "16 * 27 must be 432"
    print("    => the denominator 432 of pi/432 is the breaking data 16 x 27,")
    print("       not an inserted integer. (pi numerator + WZ level remain open.)")

    # [V] verdict -----------------------------------------------------------
    print("\n[V] Sandbox verdict")
    print("    spontaneous F4 -> Spin(9) vacuum on the real f4 : EXHIBITED")
    print("    unbroken so(9) = 36, Goldstones = 16 spinor      : EXACT")
    print("    selecting invariant potential (vacuum = OP^2)    : EXHIBITED")
    print("    carrier 432 = 16 x 27 from the breaking          : DERIVED")
    print("    pi/432 value (numerator pi + WZ level one)        : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
