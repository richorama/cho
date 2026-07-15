"""Gate Q08: state-independent contextuality, and its fate under coarse-graining.

Gate Q07 found one nonclassical structure the recursion preserves: the irreducible
complex phase. Q08 adds a second, independent and sharper nonclassical fingerprint —
state-independent contextuality — and measures its opposite fate.

The Peres-Mermin magic square is nine two-qubit observables in a 3x3 grid. Every
observable is Hermitian and squares to the identity, so its values are dichotomic
``+/-1``. The three observables on each line (row or column) mutually commute and can be
measured together, and each line multiplies to ``+I`` except one, which multiplies to
``-I``. A noncontextual observer would assign every observable a fixed ``+/-1`` value
independent of which line it is measured in; the six line products then force an even
parity in one counting and an odd parity in another. Exactly zero of the ``512``
assignments satisfy all six lines, so no context-independent value assignment exists at
any state — a Kochen-Specker contradiction, exact over Q(i).

This contextuality is a fine-grained resource. Under the single-qubit coarse-graining
(partial trace over the erased qubit) seven of the nine observables collapse to the zero
operator — only the two that act trivially on the erased qubit survive — so every line is
destroyed and the coarse, single-qubit world carries no contextuality. Compared with the
complex phase of Q07, which survives the recursion, contextuality is resolution
dependent: it lives in the fine algebra and coarse-graining erases it.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from typing import Tuple

from .gaussian import ONE, ZERO, Gaussian
from .coarse_graining import _I2, _X, _Z, partial_trace
from .linalg import Matrix, dagger, identity, kron, matmul

# Pauli Y = [[0, -i], [i, 0]]: genuinely complex, exact over Q(i).
_Y: Matrix = (
    (ZERO, Gaussian(Fraction(0), Fraction(-1))),
    (Gaussian(Fraction(0), Fraction(1)), ZERO),
)

_I4: Matrix = identity(4)


def _neg(matrix: Matrix) -> Matrix:
    return tuple(tuple(ZERO - value for value in row) for row in matrix)


_NEG_I4: Matrix = _neg(_I4)

# The Peres-Mermin magic square over Q(i).
MAGIC_SQUARE: Tuple[Tuple[Matrix, ...], ...] = (
    (kron(_X, _I2), kron(_I2, _X), kron(_X, _X)),
    (kron(_I2, _Z), kron(_Z, _I2), kron(_Z, _Z)),
    (kron(_X, _Z), kron(_Z, _X), kron(_Y, _Y)),
)

# Line target: rows then columns; every line is +I except the third column.
LINE_SIGNS: Tuple[int, ...] = (1, 1, 1, 1, 1, -1)


def _lines() -> Tuple[Tuple[Tuple[int, int], ...], ...]:
    rows = tuple(tuple((i, j) for j in range(3)) for i in range(3))
    cols = tuple(tuple((i, j) for i in range(3)) for j in range(3))
    return rows + cols


def _cells() -> Tuple[Tuple[int, int], ...]:
    return tuple((i, j) for i in range(3) for j in range(3))


def observables_are_dichotomic() -> bool:
    """Every observable is Hermitian and squares to the identity."""
    for i, j in _cells():
        obs = MAGIC_SQUARE[i][j]
        if dagger(obs) != obs or matmul(obs, obs) != _I4:
            return False
    return True


def lines_are_jointly_measurable() -> bool:
    """The three observables on each line mutually commute."""
    for line in _lines():
        members = [MAGIC_SQUARE[i][j] for i, j in line]
        for a, b in combinations(members, 2):
            if matmul(a, b) != matmul(b, a):
                return False
    return True


def line_products_match_signs() -> bool:
    """Five lines multiply to +I and exactly one to -I."""
    for line, sign in zip(_lines(), LINE_SIGNS):
        a, b, c = (MAGIC_SQUARE[i][j] for i, j in line)
        product_matrix = matmul(matmul(a, b), c)
        target = _I4 if sign == 1 else _NEG_I4
        if product_matrix != target:
            return False
    return True


def noncontextual_assignment_count() -> int:
    """How many of the 512 fixed +/-1 assignments respect all six line signs."""
    cells = _cells()
    lines = _lines()
    count = 0
    for values in product((1, -1), repeat=9):
        assignment = {cell: values[k] for k, cell in enumerate(cells)}
        if all(
            assignment[line[0]] * assignment[line[1]] * assignment[line[2]] == sign
            for line, sign in zip(lines, LINE_SIGNS)
        ):
            count += 1
    return count


def kochen_specker_contradiction() -> bool:
    """True iff no context-independent value assignment exists (state-independent)."""
    return noncontextual_assignment_count() == 0


def _is_zero(matrix: Matrix) -> bool:
    return all(value == ZERO for row in matrix for value in row)


def coarse_grained_surviving_observables() -> int:
    """Observables that remain nonzero after tracing out the erased qubit."""
    survivors = 0
    for i, j in _cells():
        if not _is_zero(partial_trace(MAGIC_SQUARE[i][j], 1)):
            survivors += 1
    return survivors


def no_line_survives_coarse_graining() -> bool:
    """Every line loses at least one observable to the coarse-graining."""
    for line in _lines():
        if all(
            not _is_zero(partial_trace(MAGIC_SQUARE[i][j], 1)) for i, j in line
        ):
            return False
    return True
