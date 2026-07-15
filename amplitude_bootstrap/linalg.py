"""Exact matrix algebra over the Gaussian rationals Q(i).

Small, dependency-free routines used by the amplitude coarse-graining gates. All
arithmetic is exact, so rank, consistency, and channel identities are decided
rather than estimated.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from .gaussian import ONE, ZERO, Gaussian

Matrix = Tuple[Tuple[Gaussian, ...], ...]


def zeros(rows: int, cols: int) -> List[List[Gaussian]]:
    return [[ZERO for _ in range(cols)] for _ in range(rows)]


def identity(dimension: int) -> Matrix:
    return tuple(
        tuple(ONE if row == col else ZERO for col in range(dimension))
        for row in range(dimension)
    )


def matmul(left: Matrix, right: Matrix) -> Matrix:
    if len(left[0]) != len(right):
        raise ValueError("inner matrix dimensions differ")
    inner = len(right)
    result = zeros(len(left), len(right[0]))
    for i in range(len(left)):
        for k in range(inner):
            factor = left[i][k]
            if factor.is_zero():
                continue
            right_row = right[k]
            result_row = result[i]
            for j in range(len(right_row)):
                result_row[j] = result_row[j] + factor * right_row[j]
    return tuple(tuple(row) for row in result)


def dagger(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][col].conjugate() for row in range(len(matrix)))
        for col in range(len(matrix[0]))
    )


def kron(left: Matrix, right: Matrix) -> Matrix:
    rows_l, cols_l = len(left), len(left[0])
    rows_r, cols_r = len(right), len(right[0])
    result = zeros(rows_l * rows_r, cols_l * cols_r)
    for i in range(rows_l):
        for j in range(cols_l):
            scalar = left[i][j]
            for p in range(rows_r):
                for q in range(cols_r):
                    result[i * rows_r + p][j * cols_r + q] = scalar * right[p][q]
    return tuple(tuple(row) for row in result)


def matrices_equal(left: Matrix, right: Matrix) -> bool:
    return left == right


def solve_columns(
    coefficients: Matrix, target: Sequence[Sequence[Gaussian]]
) -> Optional[Tuple[Tuple[Gaussian, ...], ...]]:
    """Solve ``coefficients @ X = target`` exactly for ``X`` or return None.

    ``coefficients`` is ``rows x unknowns`` and ``target`` is ``rows x k``. Returns
    an ``unknowns x k`` solution when every column system is consistent, otherwise
    None. Handles over-determined systems by checking consistency exactly.
    """
    rows = len(coefficients)
    unknowns = len(coefficients[0]) if rows else 0
    width = len(target[0]) if target else 0

    augmented = [
        [coefficients[r][c] for c in range(unknowns)] + [target[r][t] for t in range(width)]
        for r in range(rows)
    ]

    pivot_columns: List[int] = []
    pivot_row = 0
    for col in range(unknowns):
        pivot = None
        for r in range(pivot_row, rows):
            if not augmented[r][col].is_zero():
                pivot = r
                break
        if pivot is None:
            continue
        augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        pivot_value = augmented[pivot_row][col]
        augmented[pivot_row] = [value / pivot_value for value in augmented[pivot_row]]
        for r in range(rows):
            if r != pivot_row and not augmented[r][col].is_zero():
                factor = augmented[r][col]
                augmented[r] = [
                    augmented[r][c] - factor * augmented[pivot_row][c]
                    for c in range(unknowns + width)
                ]
        pivot_columns.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break

    for r in range(pivot_row, rows):
        if all(augmented[r][c].is_zero() for c in range(unknowns)):
            if any(not augmented[r][unknowns + t].is_zero() for t in range(width)):
                return None

    solution = zeros(unknowns, width)
    for index, col in enumerate(pivot_columns):
        for t in range(width):
            solution[col][t] = augmented[index][unknowns + t]
    return tuple(tuple(row) for row in solution)


def rank(matrix: Matrix) -> int:
    """Exact rank over Q(i) by Gaussian elimination."""
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    cols = len(rows[0])
    pivot_row = 0
    for col in range(cols):
        pivot = None
        for r in range(pivot_row, len(rows)):
            if not rows[r][col].is_zero():
                pivot = r
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][col]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and not rows[r][col].is_zero():
                factor = rows[r][col]
                rows[r] = [rows[r][c] - factor * rows[pivot_row][c] for c in range(cols)]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row
