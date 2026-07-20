"""Gate Q13: approximate autonomous coarse laws and the coupling flow.

Gates Q01 and Q09 established an exact no-go: a two-qubit unitary admits an
*exact* autonomous reduced law under the partial trace only for the 36
non-interacting product unitaries; every entangling member fails outright.  That
exactness is also what makes the crucible sterile — real effective (renormalised)
dynamics is never exactly autonomous, only autonomous up to a controlled error.

Gate Q13 relaxes the demand ``E . B = B . U(.)U^dagger`` from *exact equality* to
*bounded misfit*.  For a microscopic unitary ``U`` and the partial trace ``B``,
write the two coarse-by-fine superoperators

    T = B                (trace)               : 16 fine op-entries -> 4 coarse
    M = B . U(.)U^dagger (evolve then trace)   : 16 fine op-entries -> 4 coarse

An autonomous coarse channel is a 4x4 (vectorised 2x2) map ``E`` with ``E T = M``.
When no exact ``E`` exists we take the exact least-squares surrogate

    E* = M T^dagger (T T^dagger)^{-1}          (T T^dagger is 4x4, full rank)

and define the **closure defect** as the exact squared Frobenius residual

    defect(U) = || M - E* T ||_F^2 = sum_{ij} |(M - E* T)_{ij}|^2  in  Q_{>=0}.

Everything stays an exact rational over Q(i).  The defect is the tightest possible
misfit of *any* linear autonomous law: if ``defect(U) > eps`` then no autonomous
coarse law reproduces the microscopic dynamics to Frobenius error ``eps``.

Two exact results follow (owned by ``tests/test_gate_q13_approximate_closure.py``):

* **Recovery of the exact no-go.** ``defect(U) == 0`` exactly for the 36 product
  unitaries and ``defect(U) > 0`` for all 108 entanglers, so ``eps -> 0`` reproduces
  Q01.  Raising the declared tolerance ``eps`` admits interacting unitaries, and the
  survivor count grows monotonically from 36 to 144 along the exact defect spectrum:
  *interaction is observer-consistent approximately, at a quantified cost.*

* **Coupling flow.** On the controlled-rotation family ``CROT(a, b) = |0><0| (x) I +
  |1><1| (x) R(a, b)`` with an exact Pythagorean rotation ``R``, the defect is a
  monotone function of the coupling ``b`` and flows to ``0`` as ``b -> 0``.  Weakly
  interacting microscopic dynamics is approximately autonomous, with the defect
  controlling the residual (the coarse law's failure to close).
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, NamedTuple, Tuple

from .coarse_graining import (
    _fine_basis_images,
    _superoperator,
    ensemble,
    partial_trace,
    reduced_channel,
)
from .gaussian import ONE, ZERO, Gaussian
from .linalg import Matrix, dagger, matmul, solve_columns

_COARSE = 2


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[r][c] for r in range(len(matrix)))
        for c in range(len(matrix[0]))
    )


def _superoperators(unitary: Matrix, traced: int = 1) -> Tuple[Matrix, Matrix]:
    """Return ``(T, M)``: the trace and evolve-then-trace superoperators (4x16)."""
    unitary_dagger = dagger(unitary)

    def trace(operator: Matrix) -> Matrix:
        return partial_trace(operator, traced)

    def evolve_then_trace(operator: Matrix) -> Matrix:
        return trace(matmul(matmul(unitary, operator), unitary_dagger))

    trace_super = _superoperator(_fine_basis_images(trace))
    evolve_super = _superoperator(_fine_basis_images(evolve_then_trace))
    return trace_super, evolve_super


def _best_fit_channel(trace_super: Matrix, evolve_super: Matrix) -> Matrix:
    """Exact least-squares ``E* = M T^dagger (T T^dagger)^{-1}`` over Q(i).

    ``T T^dagger`` is the 4x4 Gram matrix of the (full-rank) trace superoperator, so
    it is invertible and the surrogate is unique.  Solved by exact elimination.
    """
    t_dagger = dagger(trace_super)               # 16 x 4
    gram = matmul(trace_super, t_dagger)         # 4 x 4, Hermitian, full rank
    target = matmul(evolve_super, t_dagger)      # 4 x 4  (= M T^dagger)
    # Solve E gram = target for E:  gram^T E^T = target^T.
    channel_t = solve_columns(_transpose(gram), _transpose(target))
    if channel_t is None:  # pragma: no cover - gram is always invertible here
        raise ValueError("trace Gram matrix was singular; this cannot happen")
    return _transpose(channel_t)


def _frobenius_norm2(matrix: Matrix) -> Fraction:
    return sum(
        (entry.norm2() for row in matrix for entry in row), Fraction(0)
    )


def _subtract(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[r][c] - right[r][c] for c in range(len(left[0])))
        for r in range(len(left))
    )


def closure_defect(unitary: Matrix, traced: int = 1) -> Fraction:
    """Exact squared Frobenius residual of the best-fit autonomous coarse law.

    Zero iff an exact autonomous channel exists (Q01); otherwise a positive rational
    measuring the tightest achievable misfit of any linear autonomous coarse law.
    """
    trace_super, evolve_super = _superoperators(unitary, traced)
    channel = _best_fit_channel(trace_super, evolve_super)
    residual = _subtract(evolve_super, matmul(channel, trace_super))
    return _frobenius_norm2(residual)


class DefectRow(NamedTuple):
    tag: str
    defect: Fraction
    exactly_autonomous: bool


def defect_spectrum(traced: int = 1) -> Tuple[DefectRow, ...]:
    """The exact closure defect of every ensemble member, sorted ascending."""
    rows: List[DefectRow] = []
    for tag, unitary in ensemble():
        defect = closure_defect(unitary, traced)
        rows.append(DefectRow(tag=tag, defect=defect, exactly_autonomous=defect == 0))
    rows.sort(key=lambda row: (row.defect, row.tag))
    return tuple(rows)


class ToleranceLadder(NamedTuple):
    ensemble_size: int
    exact_survivors: int          # defect == 0 (recovers Q01)
    exact_are_all_local: bool
    entanglers_all_positive: bool
    ladder: Tuple[Tuple[Fraction, int, int], ...]  # (eps, survivors, interacting)
    monotone: bool


def tolerance_ladder(
    tolerances: Tuple[Fraction, ...], traced: int = 1
) -> ToleranceLadder:
    """Survivor counts as the declared closure tolerance ``eps`` is raised.

    ``exact_survivors`` (``eps = 0``) must be the 36 product unitaries, recovering the
    Q01 no-go.  As ``eps`` grows the survivor count is monotone non-decreasing and
    admits interacting unitaries: closure is a matter of budget, not impossibility.
    """
    rows = defect_spectrum(traced)
    ensemble_size = len(rows)
    exact = [row for row in rows if row.exactly_autonomous]
    exact_are_all_local = all(row.tag == "local" for row in exact)
    entanglers_all_positive = all(
        row.defect > 0 for row in rows if row.tag != "local"
    )

    ladder: List[Tuple[Fraction, int, int]] = []
    previous = -1
    monotone = True
    for eps in tolerances:
        survivors = [row for row in rows if row.defect <= eps]
        count = len(survivors)
        interacting = sum(1 for row in survivors if row.tag != "local")
        ladder.append((eps, count, interacting))
        if count < previous:
            monotone = False
        previous = count

    return ToleranceLadder(
        ensemble_size=ensemble_size,
        exact_survivors=len(exact),
        exact_are_all_local=exact_are_all_local,
        entanglers_all_positive=entanglers_all_positive,
        ladder=tuple(ladder),
        monotone=monotone,
    )


# --- The coupling flow: an exactly-unitary controlled-rotation family. -----------

def _g(real: int, imag: int = 0) -> Gaussian:
    return Gaussian(Fraction(real), Fraction(imag))


def controlled_rotation(a: Fraction, b: Fraction) -> Matrix:
    """``|0><0| (x) I + |1><1| (x) R(a, b)`` with ``R = [[a, -b], [b, a]]``.

    Requires ``a^2 + b^2 == 1`` so the target rotation, hence the whole gate, is
    exactly unitary over Q.  ``b`` is the coupling strength: ``b = 0`` gives the
    identity (a product unitary), larger ``b`` entangles a superposed control with
    the target.
    """
    if a * a + b * b != 1:
        raise ValueError("controlled_rotation needs a Pythagorean pair a^2 + b^2 = 1")
    ga, gb = Gaussian(a), Gaussian(b)
    return (
        (ONE, ZERO, ZERO, ZERO),
        (ZERO, ONE, ZERO, ZERO),
        (ZERO, ZERO, ga, -gb),
        (ZERO, ZERO, gb, ga),
    )


# Exact Pythagorean pairs (a, b) with a^2 + b^2 = 1, ordered by increasing coupling b.
COUPLINGS: Tuple[Tuple[int, int, int], ...] = (
    (1, 0, 1),      # b = 0      : identity, a product unitary
    (40, 9, 41),    # b = 9/41
    (24, 7, 25),    # b = 7/25
    (12, 5, 13),    # b = 5/13
    (4, 3, 5),      # b = 3/5
    (3, 4, 5),      # b = 4/5
)


class CouplingPoint(NamedTuple):
    coupling: Fraction         # b
    defect: Fraction
    exactly_autonomous: bool


class CouplingFlow(NamedTuple):
    points: Tuple[CouplingPoint, ...]
    zero_coupling_is_exact: bool          # defect(b = 0) == 0
    positive_coupling_is_inexact: bool    # defect(b > 0) > 0
    strictly_increasing: bool             # defect strictly grows with b
    flows_to_zero: bool                   # smallest positive b has the smallest defect


def coupling_flow(traced: int = 1) -> CouplingFlow:
    """The closure defect along the controlled-rotation coupling family.

    Establishes the renormalisation-flavoured statement: the defect vanishes at zero
    coupling, is positive for every nonzero coupling, and increases monotonically with
    the coupling ``b`` -- so weakly interacting microscopic dynamics is approximately
    autonomous, the residual controlled by the coupling.
    """
    points: List[CouplingPoint] = []
    for a_num, b_num, denom in COUPLINGS:
        a = Fraction(a_num, denom)
        b = Fraction(b_num, denom)
        defect = closure_defect(controlled_rotation(a, b), traced)
        points.append(
            CouplingPoint(coupling=b, defect=defect, exactly_autonomous=defect == 0)
        )

    zero_point = points[0]
    positive = points[1:]
    zero_exact = zero_point.coupling == 0 and zero_point.defect == 0
    positive_inexact = all(point.defect > 0 for point in positive)
    ordered_by_coupling = sorted(points, key=lambda p: p.coupling)
    strictly_increasing = all(
        ordered_by_coupling[i].defect < ordered_by_coupling[i + 1].defect
        for i in range(len(ordered_by_coupling) - 1)
    )
    flows_to_zero = min(positive, key=lambda p: p.coupling).defect == min(
        point.defect for point in positive
    )

    return CouplingFlow(
        points=tuple(points),
        zero_coupling_is_exact=zero_exact,
        positive_coupling_is_inexact=positive_inexact,
        strictly_increasing=strictly_increasing,
        flows_to_zero=flows_to_zero,
    )


def exact_defect_matches_reduced_channel(traced: int = 1) -> bool:
    """Cross-check: ``defect == 0`` iff :func:`reduced_channel` returns a channel."""
    for _, unitary in ensemble():
        has_exact = reduced_channel(unitary, traced) is not None
        if (closure_defect(unitary, traced) == 0) != has_exact:
            return False
    return True
