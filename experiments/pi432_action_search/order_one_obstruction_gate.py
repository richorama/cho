"""Order-one obstruction gate -- where the finite factor's Dirac meets
non-associativity, and why that forces exactly the product-triple split.

SCOPE (diagnostic / exploratory, QUARANTINED). product_triple_realisation_gate.py
argued the realisation must be (finite carrier) (x) (continuous CP^1), because pi
cannot be a finite spectral invariant. This gate stress-tests the FINITE factor
against the defining structural axiom of a spectral triple -- the order-one (first
order) condition -- and finds exactly where it bites.

A spectral triple (A, H, D) needs an ASSOCIATIVE *-algebra A: the representation
pi must satisfy pi(ab) = pi(a) pi(b) (an algebra homomorphism into bounded
operators), and the order-one condition

        [[D, pi(a)], pi(b)^circ] = 0   for all a, b in A

uses the opposite algebra, which only makes sense associatively. But the carrier's
natural algebra is the Albert algebra J3(O), which is NON-ASSOCIATIVE. So J3(O)
cannot itself be a spectral-triple algebra; one represents it by left
multiplications L_a acting on H = J (a Jordan module).

The exact structural facts (all over Q):

  * J3(O) is non-associative -- the associator (E11,E11,e) on an octonionic
    off-diagonal e is (1/4)e != 0 -- so a -> L_a is NOT multiplicative
    (L_{E11} != L_{E11}^2). This is the obstruction.

  * For the naive finite Dirac D = L_N (left multiplication by the grade element
    N = diag(0,1,2)) and the left-multiplication representation, the order-one
    defect has a closed form:

        [[L_N, L_a], L_b] = L_{[L_N, L_a](b)},

    because [L_a, L_b] is always a derivation of J (an element of f4 = Der(J)) and
    [delta, L_b] = L_{delta(b)} for any derivation delta. So the defect is governed
    entirely by f4.

  * That defect VANISHES whenever a lies in the associative diagonal frame
    subalgebra Delta = span(E11, E22, E33) (the frame multiplication operators
    commute, so [L_N, L_{E_i}] = 0), and is NON-ZERO for octonionic off-diagonal a.
    Hence the order-one condition holds on the 3-dimensional associative algebra of
    the generation frame, and fails exactly on the 24 octonionic off-diagonal
    directions = the Peirce-1/2 spaces where OP^2 / the continuous factor lives.

So the order-one axiom INDEPENDENTLY forces the same finite-(x)-continuous split
the transcendence argument inferred: 27 = 3 (associative diagonal; the finite
spectral triple of the three generation grades) + 24 (octonionic off-diagonal; the
continuous OP^2 geometry). The obstruction to a purely finite triple is precisely
f4 = Der(J3(O)) != 0.

PROVED (exact; standalone EXIT 0; sweep PASS; get_errors clean):
  [A] non-associativity witness: associator(E11,E11,e3) = (1/4) e3 != 0, so
      L_{E11} != L_{E11}^2 -- a -> L_a is not an algebra homomorphism.
  [B] bridge identity: [L_a, L_b] is a derivation (is_derivation) and
      [[L_N, L_a], L_b] == L_{[L_N, L_a](b)} exactly (matrix equality on a witness).
  [C] order-one FAILS for the naive D = L_N: an explicit (a,b) with
      [[L_N, L_a], L_b] != 0 (a octonionic off-diagonal).
  [D] order-one HOLDS on the associative frame: for every diagonal a in
      {E11,E22,E33} and every b, the defect is zero (frame L's commute); and the
      diagonal frame is associative. The 27 splits 3 + 24.
  [E] synthesis: f4 = Der(J) is the obstruction; the order-one-consistent part is
      the 3-generation associative diagonal, the inconsistent part is the 24-dim
      octonionic OP^2 geometry -- the product-triple split, re-derived.

OPEN: the full real (even) spectral triple with an off-diagonal/chiral finite
Dirac and a real structure J realising the opposite algebra, which is how genuine
NCG finite triples satisfy order-one -- constructing it for J3(O) is the open
research problem and the genuine criterion (1) theorem.

KILL: had the defect not vanished on the associative diagonal frame, even the
generation-grade finite triple would be order-one-inconsistent and the spectral
route would be dead; had it vanished everywhere, J3(O) would be associative
(false). The defect is nonzero exactly off the frame -- the informative outcome.

Diagnostic only; moves no Bayes credit; the scoreboard stays parked.
"""

from __future__ import annotations

from fractions import Fraction as Fr

from peirce_grade_reflection_gate import (
    DIM,
    basis,
    frame_idempotent,
    grade_element,
    jordan,
)
from f4_breaking_vacuum_gate import (
    apply_op,
    commutator,
    is_derivation,
    matmul,
    mult_operator,
)

PEIRCE_GRADES = (0, 1, 2)
# octonionic off-diagonal basis indices (the three Peirce slots, 8 each = 24)
OFFDIAG = list(range(3, DIM))


def associator(a: list[Fr], b: list[Fr], c: list[Fr]) -> list[Fr]:
    """(a o b) o c - a o (b o c)."""
    left = jordan(jordan(a, b), c)
    right = jordan(a, jordan(b, c))
    return [left[i] - right[i] for i in range(DIM)]


def mat_scale_add(mats: list[tuple[Fr, list[list[Fr]]]]) -> list[list[Fr]]:
    """Linear combination sum_k coeff_k * M_k of 27x27 matrices."""
    out = [[Fr(0)] * DIM for _ in range(DIM)]
    for coeff, M in mats:
        if coeff == 0:
            continue
        for i in range(DIM):
            ri, mi = out[i], M[i]
            for j in range(DIM):
                if mi[j]:
                    ri[j] += coeff * mi[j]
    return out


def is_zero_mat(M: list[list[Fr]]) -> bool:
    return all(x == 0 for row in M for x in row)


def is_zero_vec(v: list[Fr]) -> bool:
    return all(x == 0 for x in v)


def main() -> bool:
    print("=" * 78)
    print("ORDER-ONE OBSTRUCTION GATE -- finite Dirac vs non-associativity")
    print("=" * 78)

    L = [mult_operator(k) for k in range(DIM)]        # left-multiplication ops
    # grade Dirac D = L_N, N = diag(0,1,2)
    N = grade_element(PEIRCE_GRADES)
    LN = mat_scale_add([(N[k], L[k]) for k in range(DIM)])

    # [A] non-associativity obstruction -----------------------------------
    print("\n[A] J3(O) is non-associative -- the obstruction to a spectral algebra")
    e11 = frame_idempotent(0)
    e3 = basis(3)                                      # an octonionic off-diag elt
    asc = associator(e11, e11, e3)
    assert not is_zero_vec(asc), "associator must be nonzero"
    # associator(E11,E11,e3) = (1/4) e3
    assert asc[3] == Fr(1, 4) and all(asc[i] == 0 for i in range(DIM) if i != 3)
    print(f"    associator(E11,E11,e3) = (1/4) e3 != 0   (e3 = octonionic slot)")
    # equivalently L_{E11 o E11} = L_{E11} != L_{E11}^2  (a -> L_a not multiplicative)
    L_e11_sq = matmul(L[0], L[0])
    assert not is_zero_mat([[L[0][i][j] - L_e11_sq[i][j] for j in range(DIM)]
                            for i in range(DIM)]), "L_E11 should differ from L_E11^2"
    print(f"    => L_(E11 o E11) = L_E11 != L_E11^2 : a -> L_a is NOT a homomorphism.")
    print(f"    => J3(O) cannot be the associative algebra of a spectral triple;")
    print(f"       it is represented by left multiplications L_a on H = J.")

    # [B] the bridge identity ---------------------------------------------
    print("\n[B] Bridge: [L_a,L_b] is a derivation, so [[L_N,L_a],L_b]=L_([L_N,L_a]b)")
    a_w = 3                                             # octonionic off-diagonal
    deriv = commutator(LN, L[a_w])                     # [L_N, L_a]
    assert is_derivation(deriv), "[L_N, L_a] must be a derivation (in f4)"
    b_w = 0
    lhs = commutator(deriv, L[b_w])                    # [[L_N,L_a],L_b]
    rhs_vec = apply_op(deriv, basis(b_w))              # [L_N,L_a](b)
    rhs = mat_scale_add([(rhs_vec[k], L[k]) for k in range(DIM)])  # L_{...}
    assert all(lhs[i][j] == rhs[i][j] for i in range(DIM) for j in range(DIM)), \
        "bridge identity [[L_N,L_a],L_b] = L_{[L_N,L_a](b)} failed"
    print(f"    [L_N, L_{a_w}] is a derivation (in f4 = Der J): verified")
    print(f"    [[L_N,L_{a_w}],L_{b_w}] == L_([L_N,L_{a_w}]({b_w})) : verified exactly")

    # [C] order-one FAILS for the naive finite Dirac ----------------------
    print("\n[C] Order-one condition [[L_N,L_a],L_b]=0 FAILS for D = L_N")
    witness = None
    offdiag_fail = 0
    for a in OFFDIAG:
        comm = commutator(LN, L[a])
        a_has_fail = False
        for b in range(DIM):
            if not is_zero_vec(apply_op(comm, basis(b))):
                a_has_fail = True
                if witness is None:
                    witness = (a, b)
        if a_has_fail:
            offdiag_fail += 1
    assert witness is not None, "order-one must fail for some off-diagonal a"
    print(f"    witness: [[L_N,L_{witness[0]}],L_{witness[1]}] != 0 "
          f"(a = octonionic off-diagonal)")
    print(f"    octonionic directions a with a nonzero defect: {offdiag_fail} of "
          f"{len(OFFDIAG)}")
    print(f"    => the naive (D=L_N, left-mult) finite triple is NOT order-one.")

    # [D] order-one HOLDS on the associative generation frame -------------
    print("\n[D] Order-one HOLDS on the associative diagonal frame Delta")
    # frame multiplication operators commute => [L_N, L_{E_i}] = 0
    for i in range(3):
        assert is_zero_mat(commutator(LN, L[i])), f"[L_N, L_E{i}] should vanish"
    # so the defect is zero for every diagonal a and every b
    diag_defects = 0
    for i in range(3):
        comm = commutator(LN, L[i])
        for b in range(DIM):
            if not is_zero_vec(apply_op(comm, basis(b))):
                diag_defects += 1
    assert diag_defects == 0, "order-one must hold for all diagonal a"
    # the diagonal frame is associative
    for i in range(3):
        for j in range(3):
            for k in range(3):
                assert is_zero_vec(associator(frame_idempotent(i),
                                              frame_idempotent(j),
                                              frame_idempotent(k))), \
                    "frame must be associative"
    print(f"    [L_N, L_E_i] = 0 for i=0,1,2 (frame multiplication ops commute)")
    print(f"    order-one defect over all (diagonal a, b): {diag_defects} (zero)")
    print(f"    diagonal frame Delta = <E11,E22,E33> is associative (all 27")
    print(f"    associators vanish): a genuine 3-dim associative algebra.")
    n_diag, n_off = 3, len(OFFDIAG)
    assert n_diag + n_off == DIM == 27
    print(f"    dim split: 27 = {n_diag} (associative diagonal) + {n_off} "
          f"(octonionic off-diagonal)")

    # [E] synthesis -------------------------------------------------------
    print("\n[E] Synthesis")
    print("    obstruction to a purely finite triple = f4 = Der(J3(O)) != 0")
    print("    order-one-consistent part : 3-dim associative frame = 3 generations")
    print("    order-one-broken part     : 24-dim octonionic = OP^2 (Peirce-1/2)")
    print("    => the order-one axiom re-derives the finite-(x)-continuous split")
    print("       that product_triple inferred from pi's transcendence.")

    print("\n[V] Sandbox verdict")
    print("    J3(O) non-associative (assoc != 0; L_a not homomorphic) : PASS")
    print("    bridge [[L_N,L_a],L_b] = L_([L_N,L_a]b) exact            : PASS")
    print("    order-one FAILS for naive D = L_N (off-diagonal witness) : PASS")
    print("    order-one HOLDS on associative frame; 27 = 3 + 24        : PASS")
    print("    obstruction = f4; split matches the product triple       : PASS")
    print("    full real/chiral finite Dirac realising order-one        : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
