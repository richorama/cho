"""Gate O32 -- an exact go/no-go test for a canonical flavour operator.

The existing colour action is identical on all three adopted Jordan slots.
Consequently gauge equivariance leaves the full generation matrix algebra
unconstrained.  Retaining the unbroken frame permutation instead makes the
operator too symmetric: an invariant self-adjoint matrix has only a singlet and
a degenerate doublet.  Thus the present algebra supplies neither a unique
Yukawa operator nor three nondegenerate masses.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from typing import List, Sequence, Tuple

from .generation_bridge import (
    bridge_dimension_obstruction,
    colour_acts_identically_on_slots,
)

Matrix = Tuple[Tuple[Fraction, ...], ...]


def _matrix(rows: Sequence[Sequence[int]]) -> Matrix:
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def _identity(n: int) -> Matrix:
    return tuple(
        tuple(Fraction(int(i == j)) for j in range(n))
        for i in range(n)
    )


def _matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0])))
        for i in range(len(a))
    )


def _transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def _sub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(a[i][j] - b[i][j] for j in range(len(a[0])))
        for i in range(len(a))
    )


def _kron(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(a[i][j] * b[r][s] for j in range(len(a[0])) for s in range(len(b[0])))
        for i in range(len(a))
        for r in range(len(b))
    )


def _rank(rows: Sequence[Sequence[Fraction]]) -> int:
    work = [list(row) for row in rows]
    if not work:
        return 0
    pivot = 0
    for col in range(len(work[0])):
        selected = next((r for r in range(pivot, len(work)) if work[r][col]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        scale = work[pivot][col]
        work[pivot] = [x / scale for x in work[pivot]]
        for row in range(len(work)):
            if row != pivot and work[row][col]:
                factor = work[row][col]
                work[row] = [
                    x - factor * y for x, y in zip(work[row], work[pivot])
                ]
        pivot += 1
    return pivot


def symmetric_generation_basis() -> Tuple[Matrix, ...]:
    """Basis of the six-dimensional self-adjoint real generation operators."""
    basis: List[Matrix] = []
    for i in range(3):
        for j in range(i, 3):
            rows = [[0] * 3 for _ in range(3)]
            rows[i][j] = 1
            rows[j][i] = 1
            basis.append(_matrix(rows))
    return tuple(basis)


def gauge_equivariant_symmetric_dimension() -> int:
    """Dimension of a guaranteed gauge-equivariant symmetric generation subspace.

    O27 proves that colour acts identically on every slot. Conditional on that
    exact result, every ``A_generation (x) I_internal`` commutes with the
    slot-diagonal action ``I_generation (x) G``. This is a six-dimensional lower
    bound on the gauge commutant, not a claim that its full dimension is six.
    """
    if not colour_acts_identically_on_slots():
        return 0
    identity_generation = _identity(3)
    identity_internal = _identity(2)
    gauge_samples = (
        _matrix(((0, 1), (-1, 0))),
        _matrix(((1, 0), (0, -1))),
    )
    allowed = 0
    for candidate in symmetric_generation_basis():
        lifted_candidate = _kron(candidate, identity_internal)
        if all(
            _matmul(lifted_candidate, _kron(identity_generation, gauge))
            == _matmul(_kron(identity_generation, gauge), lifted_candidate)
            for gauge in gauge_samples
        ):
            allowed += 1
    return allowed


def _permutation_matrices() -> Tuple[Matrix, ...]:
    out = []
    for perm in permutations(range(3)):
        out.append(
            tuple(
                tuple(Fraction(int(perm[j] == i)) for j in range(3))
                for i in range(3)
            )
        )
    return tuple(out)


def permutation_invariant_symmetric_dimension() -> int:
    """Dimension of symmetric matrices invariant under the full frame ``S3``."""
    basis = symmetric_generation_basis()
    constraints: List[List[Fraction]] = []
    for perm in _permutation_matrices():
        perm_t = _transpose(perm)
        transformed = [
            _sub(_matmul(_matmul(perm, item), perm_t), item)
            for item in basis
        ]
        for i in range(3):
            for j in range(3):
                constraints.append([item[i][j] for item in transformed])
    return len(basis) - _rank(constraints)


def invariant_basis_is_identity_and_all_ones() -> bool:
    """``I`` and ``J`` are independent and invariant, exhausting the 2D commutant."""
    identity = _identity(3)
    all_ones = _matrix(((1, 1, 1), (1, 1, 1), (1, 1, 1)))
    invariant = all(
        _matmul(_matmul(perm, item), _transpose(perm)) == item
        for perm in _permutation_matrices()
        for item in (identity, all_ones)
    )
    flattened = [
        [entry for row in item for entry in row]
        for item in (identity, all_ones)
    ]
    return invariant and _rank(flattened) == 2 and permutation_invariant_symmetric_dimension() == 2


def invariant_operator_has_generation_degeneracy() -> bool:
    """No ``a I + b J`` has three distinct eigenvalues.

    For ``b != 0`` the sum-zero space is a degenerate doublet. For ``b = 0``
    the identity is threefold degenerate, which is an even stronger failure.
    """
    sum_zero_basis = (
        (Fraction(1), Fraction(-1), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(-1)),
    )
    all_ones = _matrix(((1, 1, 1), (1, 1, 1), (1, 1, 1)))
    return all(
        tuple(sum(all_ones[i][j] * vector[j] for j in range(3)) for i in range(3))
        == (Fraction(0), Fraction(0), Fraction(0))
        for vector in sum_zero_basis
    )


def genuine_three_generation_module_available() -> bool:
    """The O27 bridge must close before a physical three-generation Yukawa can act."""
    return not bridge_dimension_obstruction()


def canonical_yukawa_theorem_closed() -> bool:
    """Current verdict: freedom without frame symmetry, degeneracy with it."""
    return (
        genuine_three_generation_module_available()
        and gauge_equivariant_symmetric_dimension() == 1
        and not invariant_operator_has_generation_degeneracy()
    )


@dataclass(frozen=True)
class YukawaOperatorGateCensus:
    full_generation_module: bool
    gauge_equivariant_symmetric_dimension: int
    permutation_invariant_symmetric_dimension: int
    invariant_basis_complete: bool
    invariant_generation_degeneracy: bool
    theorem_closed: bool


def yukawa_operator_gate_census() -> YukawaOperatorGateCensus:
    return YukawaOperatorGateCensus(
        full_generation_module=genuine_three_generation_module_available(),
        gauge_equivariant_symmetric_dimension=gauge_equivariant_symmetric_dimension(),
        permutation_invariant_symmetric_dimension=permutation_invariant_symmetric_dimension(),
        invariant_basis_complete=invariant_basis_is_identity_and_all_ones(),
        invariant_generation_degeneracy=invariant_operator_has_generation_degeneracy(),
        theorem_closed=canonical_yukawa_theorem_closed(),
    )
