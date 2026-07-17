"""Gate Q10: dimension robustness of the nested spatial recursion.

Gate Q06 established, on a three-qubit chain ``A-B-C``, that each nested spatial
blocking removes exactly the dynamics coupling across the newly erased boundary, that
only fully non-interacting products reach the bottom, and that the complex phase (Q07)
survives the recursion. A fair worry is that those findings are artefacts of the
smallest chain that admits a nested blocking. Gate Q10 reruns the identical machinery
on a *four*-qubit chain ``A-B-C-D`` with a genuine three-level recursion (trace ``D``,
then ``C``, then ``B``), and checks that the same three structural facts hold one
dimension up.

Nothing new is added to the reduction: :func:`spatial.reduce_map`,
:func:`spatial.partial_trace_qubit`, :func:`spatial._conjugation`, and
:func:`spatial._channel_action` are already defined for an arbitrary number of qubits,
so this module only assembles a four-qubit ensemble and drives the same nested
reduction. The one implementation concern is speed: exact Gaussian-rational elimination
on a sixteen-dimensional operator space is heavy, so the input-side partial traces
(which do not depend on the microscopic unitary) are computed once and shared across
the whole ensemble.
"""

from __future__ import annotations

from typing import Callable, Dict, List, NamedTuple, Optional, Tuple

from .gaussian import ONE, ZERO, Gaussian
from .linalg import Matrix, kron, matmul, solve_columns
from .spatial import (
    _basis_operator,
    _bit,
    _channel_action,
    _conjugation,
    _superoperator,
    _transpose,
    choi_rank,
    partial_trace_qubit,
    reduce_map,
)
from .coarse_graining import _I2, _S, _X

_CHAIN_QUBITS = 4
# I is the trivial real gate, S the phase gate (irreducibly complex), X a real flip.
_FOUR_GATES: Tuple[Matrix, ...] = (_I2, _S)


def _cnot_on(control: int, target: int, n_qubits: int = _CHAIN_QUBITS) -> Matrix:
    """An ``n``-qubit CNOT as an exact permutation over Q(i)."""
    dimension = 1 << n_qubits
    rows = []
    for i in range(dimension):
        control_bit = _bit(i, control, n_qubits)
        flipped = i ^ (control_bit << (n_qubits - 1 - target))
        rows.append(tuple(ONE if c == flipped else ZERO for c in range(dimension)))
    return tuple(rows)


def _kron4(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    return kron(kron(kron(a, b), c), d)


_IDENTITY16: Matrix = tuple(
    tuple(ONE if r == c else ZERO for c in range(16)) for r in range(16)
)
# One entangler per nearest-neighbour boundary of the chain.
_ENTANGLERS: Tuple[Tuple[str, Matrix], ...] = (
    ("chain_local", _IDENTITY16),
    ("cnot_ab", _cnot_on(0, 1)),
    ("cnot_bc", _cnot_on(1, 2)),
    ("cnot_cd", _cnot_on(2, 3)),
)


class ChainMember(NamedTuple):
    tag: str
    unitary: Matrix


def chain_ensemble() -> List[ChainMember]:
    """Every ``(a kron b kron c kron d) @ entangler`` four-qubit unitary."""
    members = []
    for a in _FOUR_GATES:
        for b in _FOUR_GATES:
            for c in _FOUR_GATES:
                for d in _FOUR_GATES:
                    product = _kron4(a, b, c, d)
                    for tag, entangler in _ENTANGLERS:
                        members.append(ChainMember(tag, matmul(product, entangler)))
    return members


# --- Cached top-level reduction (trace the last qubit of the four-qubit chain). ---

def _cached_input_super(n_qubits: int, qubit: int) -> Matrix:
    """The transposed coefficient matrix ``partial_trace o (.)`` on the fine basis.

    Independent of the microscopic unitary, so it is computed once and reused for
    every ensemble member at the top (four-qubit) level, where it dominates cost.
    """
    dimension = 1 << n_qubits
    traced_inputs: List[Matrix] = []
    for i in range(dimension):
        for j in range(dimension):
            operator = _basis_operator(dimension, i, j)
            traced_inputs.append(partial_trace_qubit(operator, n_qubits, qubit))
    return _transpose(_superoperator(traced_inputs))


def _reduce_top(
    apply_fn: Callable[[Matrix], Matrix], coefficient_t: Matrix, qubit: int
) -> Optional[Matrix]:
    """Autonomous coarse channel after tracing ``qubit``, reusing cached coefficients."""
    dimension = 1 << _CHAIN_QUBITS
    traced_outputs: List[Matrix] = []
    for i in range(dimension):
        for j in range(dimension):
            operator = _basis_operator(dimension, i, j)
            traced_outputs.append(
                partial_trace_qubit(apply_fn(operator), _CHAIN_QUBITS, qubit)
            )
    evolved = _superoperator(traced_outputs)
    solution = solve_columns(coefficient_t, _transpose(evolved))
    if solution is None:
        return None
    return _transpose(solution)


def _is_genuinely_complex(channel: Matrix) -> bool:
    return any(value.imag != 0 for row in channel for value in row)


class Recursion4Summary(NamedTuple):
    total: int
    level1_survivors: int
    level2_survivors: int
    level3_survivors: int
    interacting_reaching_level2: int
    interacting_reaching_level3: int
    level3_all_reversible: bool
    distinct_level1_channels: int
    distinct_level2_channels: int
    distinct_level3_channels: int
    complex_level3_channels: int


def recursion_summary() -> Recursion4Summary:
    """Coarse-grain the four-qubit chain three times, tracking every structural fact."""
    members = chain_ensemble()
    coefficient_t = _cached_input_super(_CHAIN_QUBITS, _CHAIN_QUBITS - 1)

    level1 = level2 = level3 = 0
    interacting_l2 = interacting_l3 = 0
    all_reversible = True
    l1c: set = set()
    l2c: set = set()
    l3c: set = set()

    for member in members:
        c1 = _reduce_top(_conjugation(member.unitary), coefficient_t, _CHAIN_QUBITS - 1)
        if c1 is None:
            continue
        level1 += 1
        l1c.add(c1)
        c2 = reduce_map(_channel_action(c1, 8), 3, 2)
        if c2 is None:
            continue
        level2 += 1
        l2c.add(c2)
        if member.tag != "chain_local":
            interacting_l2 += 1
        c3 = reduce_map(_channel_action(c2, 4), 2, 1)
        if c3 is None:
            continue
        level3 += 1
        l3c.add(c3)
        if member.tag != "chain_local":
            interacting_l3 += 1
        if choi_rank(c3, 2) != 1:
            all_reversible = False

    return Recursion4Summary(
        total=len(members),
        level1_survivors=level1,
        level2_survivors=level2,
        level3_survivors=level3,
        interacting_reaching_level2=interacting_l2,
        interacting_reaching_level3=interacting_l3,
        level3_all_reversible=all_reversible,
        distinct_level1_channels=len(l1c),
        distinct_level2_channels=len(l2c),
        distinct_level3_channels=len(l3c),
        complex_level3_channels=sum(1 for ch in l3c if _is_genuinely_complex(ch)),
    )
