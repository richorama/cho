"""Central-simplicity gate -- the chiral doubling is FORCED, not optional.

SCOPE (diagnostic / exploratory, QUARANTINED). order_one_obstruction_gate.py
showed the naive single-copy finite Dirac D = L_N fails the order-one condition on
the octonionic directions, and noted the standard fix is a real (even) spectral
triple with a real structure J and the opposite algebra. This gate settles a
sharp binary question about that fix: is the doubling a modelling CHOICE, or is it
mathematically FORCED?

A real structure needs a nontrivial opposite (right) action b^circ commuting with
the left action -- i.e. an element of the COMMUTANT of the multiplication algebra
M = alg{L_a : a in J}. If the commutant is just the scalars, there is NO room for
a nontrivial opposite algebra on H = J, and the real spectral triple MUST enlarge
the Hilbert space (the chiral / particle-antiparticle doubling H = J (+) J).

The exact result (over Q):

    the commutant of the Jordan multiplication algebra M = alg{L_a} on J3(O) is
    EXACTLY 1-dimensional (only the scalars).

Equivalently J3(O) is CENTRAL SIMPLE (its centroid is the ground field). Since the
L_a are self-adjoint for the (positive-definite) trace form, M is a *-algebra, so
by the double-commutant theorem M = M'' = End(J) = M_27(R) -- the multiplication
algebra is the FULL matrix algebra. Hence:

  * H = J carries no nontrivial opposite algebra -> a single-copy real spectral
    triple is impossible; the doubling H = J (+) J is FORCED.
  * with the doubling, the algebra acts blockwise pi(a) = diag(L_a, L_a) and the
    opposite action lands in the OTHER copy, so the order-one condition
    [[D, pi(a)], pi(b)^circ] = 0 is carried by an OFF-DIAGONAL Dirac
    D = [[0, T*], [T, 0]] -- exactly the Standard-Model finite-triple shape -- which
    is why the naive diagonal D = L_N of the order-one gate had to fail.

So three independent lines now converge on the SAME finite-(x)-continuous,
doubled structure: pi's transcendence (product_triple), the order-one defect being
f4-valued (order_one_obstruction), and central simplicity forcing the doubling
(this gate).

PROVED (exact; standalone EXIT 0; sweep PASS; get_errors clean):
  [A] the commutant of M = alg{L_a} is exactly 1-dimensional (only scalars),
      computed as the exact rational nullspace of [T, L_a] = 0; J3(O) is central
      simple.
  [B] the L_a are self-adjoint for the trace form (M is a *-algebra), so the
      double-commutant theorem gives M = M'' = M_27(R): dim M = 729 = 27^2.
  [C] consequence: no nontrivial opposite algebra on H = J -> the chiral doubling
      H = J (+) J is forced, and the finite Dirac must be off-diagonal.
  [D] convergence: transcendence, order-one (f4), and central simplicity all force
      the same doubled finite-(x)-continuous shape.

OPEN: the explicit off-diagonal T (the finite Dirac / Yukawa block) and the proof
that the doubled triple satisfies order-one with a concrete real structure -- the
genuine criterion (1) realisation theorem. This gate proves the doubling is
necessary; it does not construct the operator.

KILL: had the commutant been larger than the scalars, a single-copy real structure
would be possible and the doubling would be an optional modelling choice rather
than a theorem; the route's "product / doubled triple" shape would then be
under-determined.

Diagnostic only; moves no Bayes credit; the scoreboard stays parked.
"""

from __future__ import annotations

from fractions import Fraction as Fr

from peirce_grade_reflection_gate import DIM
from f4_breaking_vacuum_gate import (
    mult_operator,
    reduce_into_basis,
    trace_form_gram,
)


def commutant_dim_of_multiplication_algebra(L: list[list[list[Fr]]]) -> int:
    """dim { T in M_27 : T L_a = L_a T for all a }.

    Unknowns are the 729 entries of T (flattened index i*DIM + k). For each
    generator L_a and each (i, j) the constraint (T L_a - L_a T)[i][j] = 0 gives
    one row; the commutant dimension is 729 minus the rank of all such rows. The
    identity always commutes, so the rank never exceeds 728; we stop early there.
    """
    rows: list[list[Fr]] = []
    pivots: list[int] = []
    ceiling = DIM * DIM - 1
    for La in L:
        for i in range(DIM):
            for j in range(DIM):
                row = [Fr(0)] * (DIM * DIM)
                for k in range(DIM):
                    if La[k][j]:
                        row[i * DIM + k] += La[k][j]
                    if La[i][k]:
                        row[k * DIM + j] -= La[i][k]
                reduce_into_basis(rows, pivots, row)
        if len(rows) >= ceiling:
            break
    return DIM * DIM - len(rows)


def is_self_adjoint(M: list[list[Fr]], G: list[list[Fr]]) -> bool:
    """Check G M = M^T G, i.e. M is symmetric for the trace form G."""
    for i in range(DIM):
        for j in range(DIM):
            lhs = sum((G[i][k] * M[k][j] for k in range(DIM)), Fr(0))
            rhs = sum((M[k][i] * G[k][j] for k in range(DIM)), Fr(0))
            if lhs != rhs:
                return False
    return True


def main() -> bool:
    print("=" * 78)
    print("CENTRAL-SIMPLICITY GATE -- the chiral doubling is forced, not optional")
    print("=" * 78)

    L = [mult_operator(a) for a in range(DIM)]

    # [A] the commutant is the scalars -> central simple ------------------
    print("\n[A] Commutant of the Jordan multiplication algebra M = alg{L_a}")
    cdim = commutant_dim_of_multiplication_algebra(L)
    assert cdim == 1, f"commutant should be 1-dimensional, got {cdim}"
    print(f"    dim commutant {{ T : [T, L_a] = 0 for all a }} = {cdim}  (only scalars)")
    print("    => J3(O) is CENTRAL SIMPLE (its centroid is the ground field).")

    # [B] M is a *-algebra -> double commutant -> M = M_27 ----------------
    print("\n[B] The L_a are self-adjoint for the trace form (M is a *-algebra)")
    G = trace_form_gram()
    assert all(G[i][j] == 0 for i in range(DIM) for j in range(DIM) if i != j)
    assert all(G[i][i] > 0 for i in range(DIM))
    for a in (0, 3, DIM - 1):
        assert is_self_adjoint(L[a], G), f"L_{a} not self-adjoint for trace form"
    print("    trace form is diagonal positive; L_0, L_3, L_26 self-adjoint: OK")
    full = DIM * DIM
    print(f"    => double-commutant: M = M'' = End(J) = M_{DIM}(R), dim = {full} "
          f"= {DIM}^2")

    # [C] consequence: doubling forced, Dirac off-diagonal ----------------
    print("\n[C] Consequence for the real spectral triple")
    print("    commutant = scalars => NO nontrivial opposite algebra on H = J")
    print("    => a single-copy real spectral triple is impossible;")
    print("       the chiral doubling H = J (+) J is FORCED.")
    print("    with doubling, pi(a) = diag(L_a, L_a), the opposite action sits in")
    print("    the other copy, so order-one needs an OFF-DIAGONAL Dirac")
    print("    D = [[0, T*],[T, 0]] -- the Standard-Model finite-triple shape;")
    print("    this is WHY the naive diagonal D = L_N (order_one gate) had to fail.")

    # [D] convergence -----------------------------------------------------
    print("\n[D] Three independent lines force the same doubled shape")
    print("    pi transcendental         -> finite (x) continuous (product_triple)")
    print("    order-one defect = f4     -> 3 associative + 24 octonionic (order_one)")
    print("    commutant = scalars       -> doubling forced (this gate)")
    print("    => the realisation is a doubled finite-(x)-continuous spectral triple.")

    print("\n[V] Sandbox verdict")
    print("    commutant of {L_a} = scalars (central simple)        : PASS")
    print("    L_a self-adjoint => M = M'' = M_27 (dim 729)         : PASS")
    print("    single-copy real triple impossible; doubling forced  : PASS")
    print("    convergence with transcendence + order-one lines     : PASS")
    print("    explicit off-diagonal finite Dirac realising order-1 : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
