"""Gate Q06: genuine spatial recursion over a three-qubit chain.

Gate Q05 contracted parameters but under time-composition on two qubits, not under a
nested spatial blocking. Q06 supplies the real thing: three qubits are coarse-grained
by tracing the last qubit to a two-qubit effective channel, and that channel is
coarse-grained *again* by tracing its last qubit to a one-qubit channel. Two nested
blockings, each halving the resolution, is spatial recursion.

The reduction is defined for any completely-positive map, not only unitary conjugation,
so the second level acts on the effective channel produced by the first — the recursion
is honest. An autonomous law exists at a level exactly when the reduced dynamics factors
through the partial trace for every state, decided exactly over Q(i).

Convention: ``n`` qubits, index ``i`` with qubit ``0`` the most significant bit. Tracing
qubit ``t`` removes place value ``2 ** (n - 1 - t)``; tracing the last qubit is the chain
end. Effective channels are row-major vec-matrices of dimension ``(2 ** m) ** 2``.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, List, NamedTuple, Optional, Tuple

from .gaussian import ONE, ZERO, Gaussian
from .linalg import Matrix, dagger, kron, matmul, rank, solve_columns
from .coarse_graining import _CNOT, _CZ, _I2, _S, _X


def _basis_operator(dimension: int, row: int, col: int) -> Matrix:
    return tuple(
        tuple(ONE if (r == row and c == col) else ZERO for c in range(dimension))
        for r in range(dimension)
    )


def _vec(operator: Matrix) -> Tuple[Gaussian, ...]:
    return tuple(value for row in operator for value in row)


def _unvec(flat: Tuple[Gaussian, ...], dimension: int) -> Matrix:
    return tuple(
        tuple(flat[r * dimension + c] for c in range(dimension))
        for r in range(dimension)
    )


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[r][c] for r in range(len(matrix)))
        for c in range(len(matrix[0]))
    )


def _remove_bit(index: int, qubit: int, n_qubits: int) -> int:
    place = 1 << (n_qubits - 1 - qubit)
    return (index // (place * 2)) * place + (index % place)


def _bit(index: int, qubit: int, n_qubits: int) -> int:
    return (index >> (n_qubits - 1 - qubit)) & 1


def partial_trace_qubit(operator: Matrix, n_qubits: int, qubit: int) -> Matrix:
    """Trace out one qubit of an ``n``-qubit operator, keeping the rest in order."""
    dimension = 1 << n_qubits
    keep_dim = 1 << (n_qubits - 1)
    result = [[ZERO] * keep_dim for _ in range(keep_dim)]
    for i in range(dimension):
        for j in range(dimension):
            if _bit(i, qubit, n_qubits) != _bit(j, qubit, n_qubits):
                continue
            r = _remove_bit(i, qubit, n_qubits)
            c = _remove_bit(j, qubit, n_qubits)
            result[r][c] = result[r][c] + operator[i][j]
    return tuple(tuple(row) for row in result)


def _superoperator(images: List[Matrix]) -> Matrix:
    columns = [_vec(image) for image in images]
    coarse_dim = len(columns[0])
    return tuple(
        tuple(columns[fine][coarse] for fine in range(len(columns)))
        for coarse in range(coarse_dim)
    )


def reduce_map(
    apply_fn: Callable[[Matrix], Matrix], n_qubits: int, qubit: int
) -> Optional[Matrix]:
    """Autonomous coarse channel after tracing ``qubit``, or None if none exists.

    ``apply_fn`` is any operator map (unitary conjugation or a channel), so this same
    reduction drives every level of the recursion.
    """
    dimension = 1 << n_qubits
    traced_inputs: List[Matrix] = []
    traced_outputs: List[Matrix] = []
    for i in range(dimension):
        for j in range(dimension):
            operator = _basis_operator(dimension, i, j)
            traced_inputs.append(partial_trace_qubit(operator, n_qubits, qubit))
            traced_outputs.append(
                partial_trace_qubit(apply_fn(operator), n_qubits, qubit)
            )
    traced_super = _superoperator(traced_inputs)
    evolved = _superoperator(traced_outputs)
    solution = solve_columns(_transpose(traced_super), _transpose(evolved))
    if solution is None:
        return None
    return _transpose(solution)


def _conjugation(unitary: Matrix) -> Callable[[Matrix], Matrix]:
    unitary_dagger = dagger(unitary)

    def apply(operator: Matrix) -> Matrix:
        return matmul(matmul(unitary, operator), unitary_dagger)

    return apply


def _channel_action(channel: Matrix, dimension: int) -> Callable[[Matrix], Matrix]:
    def apply(operator: Matrix) -> Matrix:
        image = matmul(channel, tuple((value,) for value in _vec(operator)))
        return _unvec(tuple(row[0] for row in image), dimension)

    return apply


def choi_rank(channel: Matrix, coarse_dim: int) -> int:
    """Exact Choi-matrix rank of a channel on ``coarse_dim`` states; one iff unitary."""
    apply = _channel_action(channel, coarse_dim)
    size = coarse_dim * coarse_dim
    choi = [[ZERO] * size for _ in range(size)]
    for i in range(coarse_dim):
        for j in range(coarse_dim):
            image = apply(_basis_operator(coarse_dim, i, j))
            for p in range(coarse_dim):
                for q in range(coarse_dim):
                    choi[i * coarse_dim + p][j * coarse_dim + q] = image[p][q]
    return rank(tuple(tuple(row) for row in choi))


# --- Three-qubit chain ensemble over Q(i). -----------------------------------

_CHAIN_QUBITS = 3
_THREE_GATES: Tuple[Matrix, ...] = (_I2, _X, _S)


def _kron3(a: Matrix, b: Matrix, c: Matrix) -> Matrix:
    return kron(kron(a, b), c)


def _cnot_on(control: int, target: int) -> Matrix:
    """Three-qubit CNOT as an exact permutation over Q(i)."""
    dimension = 1 << _CHAIN_QUBITS
    rows = []
    for i in range(dimension):
        target_bit = _bit(i, target, _CHAIN_QUBITS)
        control_bit = _bit(i, control, _CHAIN_QUBITS)
        flipped = i ^ (control_bit << (_CHAIN_QUBITS - 1 - target))
        rows.append(tuple(ONE if c == flipped else ZERO for c in range(dimension)))
    return tuple(rows)


_IDENTITY8: Matrix = tuple(
    tuple(ONE if r == c else ZERO for c in range(8)) for r in range(8)
)
_CNOT_AB: Matrix = _cnot_on(0, 1)
_CNOT_BC: Matrix = _cnot_on(1, 2)
_ENTANGLERS: Tuple[Tuple[str, Matrix], ...] = (
    ("chain_local", _IDENTITY8),
    ("cnot_ab", _CNOT_AB),
    ("cnot_bc", _CNOT_BC),
)


class ChainMember(NamedTuple):
    tag: str
    unitary: Matrix


def chain_ensemble() -> List[ChainMember]:
    members = []
    for a in _THREE_GATES:
        for b in _THREE_GATES:
            for c in _THREE_GATES:
                product = _kron3(a, b, c)
                for tag, entangler in _ENTANGLERS:
                    members.append(ChainMember(tag, matmul(product, entangler)))
    return members


# --- Two-level spatial-recursion census. -------------------------------------

class RecursionSummary(NamedTuple):
    total: int
    level1_survivors: int
    level2_survivors: int
    level2_all_reversible: bool
    interacting_reaching_level2: int
    distinct_level1_channels: int
    distinct_level2_channels: int


def recursion_summary() -> RecursionSummary:
    """Coarse-grain the chain twice, tracking survival and parameter contraction."""
    members = chain_ensemble()
    level1_survivors = 0
    level2_survivors = 0
    level2_all_reversible = True
    interacting_reaching_level2 = 0
    level1_channels = set()
    level2_channels = set()
    for member in members:
        level1 = reduce_map(_conjugation(member.unitary), _CHAIN_QUBITS, 2)
        if level1 is None:
            continue
        level1_survivors += 1
        level1_channels.add(level1)
        level2 = reduce_map(_channel_action(level1, 4), 2, 1)
        if level2 is None:
            continue
        level2_survivors += 1
        level2_channels.add(level2)
        if member.tag != "chain_local":
            interacting_reaching_level2 += 1
        if choi_rank(level2, 2) != 1:
            level2_all_reversible = False
    return RecursionSummary(
        total=len(members),
        level1_survivors=level1_survivors,
        level2_survivors=level2_survivors,
        level2_all_reversible=level2_all_reversible,
        interacting_reaching_level2=interacting_reaching_level2,
        distinct_level1_channels=len(level1_channels),
        distinct_level2_channels=len(level2_channels),
    )
