"""Gate Q14: the renormalisation flow of the closure defect.

Gate Q13 relaxed exact autonomy to a bounded misfit (the *closure defect*) and showed
interaction survives coarse-graining approximately, with the defect of a single
controlled-rotation coupling equal to ``4 b^2``. The decisive question for a would-be
theory is what happens under *repeated* coarse-graining: does a fixed microscopic
coupling become more visible (relevant), stay put (marginal), or wash out (irrelevant)
as resolution is thrown away step by step?

Q14 answers it exactly. A chain of ``n`` qubits carries a translation-invariant
nearest-neighbour coupling ``CROT(a, b) = |0><0| (x) I + |1><1| (x) R(a, b)`` between
each adjacent pair (an exactly unitary gate over Q(i) whenever ``a^2 + b^2 = 1``). The
chain is coarse-grained by tracing the end qubit, then the end qubit of the resulting
effective channel, and so on -- the same honest spatial recursion as Gate Q06, but now
recording the exact least-squares closure defect at every level rather than only
whether an exact autonomous law exists.

The exact findings (owned by ``tests/test_gate_q14_renormalization_flow.py``):

* **Zero coupling is a fixed point.** ``b = 0`` gives defect ``0`` at every level: the
  non-interacting product is exactly autonomous under the whole recursion.

* **Interaction is visible at every finite scale.** For ``b > 0`` the defect is strictly
  positive at every level, so Q13's approximate interaction is not an artefact of a
  single blocking.

* **The coupling is irrelevant.** The defect *contracts* at every coarse-graining step:
  the boundary step (across the coupled cut) multiplies the defect by exactly
  ``a^2 / 4`` and every deeper step by exactly ``1/4``. Both are ``<= 1/4 < 1``, so the
  defect decays geometrically and the coarse world flows to the non-interacting
  (autonomous) fixed point. This *derives* the Q01/Q09 exact no-go as the endpoint of
  the flow: interaction is real at every finite resolution but renormalises to zero.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, NamedTuple, Tuple

from .gaussian import ONE, ZERO, Gaussian
from .linalg import Matrix, dagger, identity, kron, matmul, solve_columns
from .spatial import (
    _basis_operator,
    _channel_action,
    _conjugation,
    _superoperator,
    _transpose,
    partial_trace_qubit,
)


# --- Exactly-unitary nearest-neighbour controlled-rotation chain over Q(i). -------

def _single(operator: Matrix, qubit: int, n_qubits: int) -> Matrix:
    """Embed a one-qubit operator on ``qubit`` of an ``n``-qubit register."""
    factor = identity(2)
    result = operator if qubit == 0 else factor
    for k in range(1, n_qubits):
        result = kron(result, operator if k == qubit else factor)
    return result


def _projector(bit: int, qubit: int, n_qubits: int) -> Matrix:
    block: Matrix = ((ONE, ZERO), (ZERO, ZERO)) if bit == 0 else ((ZERO, ZERO), (ZERO, ONE))
    return _single(block, qubit, n_qubits)


def _rotation(a: Fraction, b: Fraction) -> Matrix:
    return ((Gaussian(a), Gaussian(-b)), (Gaussian(b), Gaussian(a)))


def controlled_rotation(
    control: int, target: int, a: Fraction, b: Fraction, n_qubits: int
) -> Matrix:
    """``|0><0|_c (x) I + |1><1|_c (x) R(a, b)_t`` on an ``n``-qubit register."""
    if a * a + b * b != 1:
        raise ValueError("controlled_rotation needs a Pythagorean pair a^2 + b^2 = 1")
    zero_branch = _projector(0, control, n_qubits)
    one_branch = matmul(
        _projector(1, control, n_qubits), _single(_rotation(a, b), target, n_qubits)
    )
    dimension = 1 << n_qubits
    return tuple(
        tuple(zero_branch[r][c] + one_branch[r][c] for c in range(dimension))
        for r in range(dimension)
    )


def coupling_chain(n_qubits: int, a: Fraction, b: Fraction) -> Matrix:
    """Product of nearest-neighbour ``CROT`` gates along an ``n``-qubit chain."""
    if n_qubits < 2:
        raise ValueError("a chain needs at least two qubits")
    chain = controlled_rotation(0, 1, a, b, n_qubits)
    for k in range(1, n_qubits - 1):
        chain = matmul(chain, controlled_rotation(k, k + 1, a, b, n_qubits))
    return chain


def is_unitary(matrix: Matrix) -> bool:
    return matmul(dagger(matrix), matrix) == identity(len(matrix))


# --- Least-squares reduction with an exact defect at each level. -----------------

def reduce_with_defect(apply_fn, n_qubits: int, qubit: int) -> Tuple[Matrix, Fraction]:
    """Best-fit autonomous coarse channel after tracing ``qubit``, and its defect.

    ``apply_fn`` is any operator map (unitary conjugation or a channel), so the same
    reduction drives every level of the recursion. Returns the exact least-squares
    channel ``E* = M T^dagger (T T^dagger)^{-1}`` and the exact squared Frobenius
    residual ``|| M - E* T ||^2``.
    """
    dimension = 1 << n_qubits
    inputs: List[Matrix] = []
    outputs: List[Matrix] = []
    for i in range(dimension):
        for j in range(dimension):
            operator = _basis_operator(dimension, i, j)
            inputs.append(partial_trace_qubit(operator, n_qubits, qubit))
            outputs.append(partial_trace_qubit(apply_fn(operator), n_qubits, qubit))
    trace_super = _superoperator(inputs)
    evolve_super = _superoperator(outputs)
    t_dagger = dagger(trace_super)
    gram = matmul(trace_super, t_dagger)
    target = matmul(evolve_super, t_dagger)
    channel = _transpose(solve_columns(_transpose(gram), _transpose(target)))
    fitted = matmul(channel, trace_super)
    defect = sum(
        (
            (evolve_super[r][c] - fitted[r][c]).norm2()
            for r in range(len(evolve_super))
            for c in range(len(evolve_super[0]))
        ),
        Fraction(0),
    )
    return channel, defect


def defect_flow(n_qubits: int, a: Fraction, b: Fraction) -> Tuple[Fraction, ...]:
    """Closure defects from tracing the end qubit repeatedly down to one qubit."""
    unitary = coupling_chain(n_qubits, a, b)
    apply_fn = _conjugation(unitary)
    defects: List[Fraction] = []
    size = n_qubits
    for qubit in range(n_qubits - 1, 0, -1):
        channel, defect = reduce_with_defect(apply_fn, size, qubit)
        defects.append(defect)
        apply_fn = _channel_action(channel, 1 << (size - 1))
        size -= 1
    return tuple(defects)


# --- Renormalisation classification. ---------------------------------------------

# Exact Pythagorean couplings (a, b) with a^2 + b^2 = 1.
COUPLINGS: Tuple[Tuple[int, int, int], ...] = (
    (1, 0, 1),
    (24, 7, 25),
    (12, 5, 13),
    (4, 3, 5),
)


class RGFlow(NamedTuple):
    n_qubits: int
    coupling: Fraction                       # b
    defects: Tuple[Fraction, ...]
    ratios: Tuple[Fraction, ...]             # d_{k+1} / d_k
    positive_at_every_level: bool
    strictly_contracting: bool               # every ratio < 1
    boundary_ratio_is_a2_over_4: bool        # first ratio == a^2 / 4
    deep_ratios_are_quarter: bool            # every later ratio == 1/4
    classification: str                      # "irrelevant" | "marginal" | "relevant"


def renormalization_flow(n_qubits: int, a: Fraction, b: Fraction) -> RGFlow:
    """Classify a nearest-neighbour coupling by its closure-defect flow."""
    defects = defect_flow(n_qubits, a, b)

    if all(defect == 0 for defect in defects):
        return RGFlow(
            n_qubits=n_qubits,
            coupling=b,
            defects=defects,
            ratios=tuple(Fraction(0) for _ in defects[1:]),
            positive_at_every_level=False,
            strictly_contracting=True,
            boundary_ratio_is_a2_over_4=True,
            deep_ratios_are_quarter=True,
            classification="fixed_point",
        )

    ratios = tuple(
        defects[k + 1] / defects[k] for k in range(len(defects) - 1)
    )
    positive = all(defect > 0 for defect in defects)
    contracting = all(ratio < 1 for ratio in ratios)
    boundary = bool(ratios) and ratios[0] == a * a / 4
    deep = all(ratio == Fraction(1, 4) for ratio in ratios[1:])

    if contracting:
        classification = "irrelevant"
    elif all(ratio == 1 for ratio in ratios):
        classification = "marginal"
    else:
        classification = "relevant"

    return RGFlow(
        n_qubits=n_qubits,
        coupling=b,
        defects=defects,
        ratios=ratios,
        positive_at_every_level=positive,
        strictly_contracting=contracting,
        boundary_ratio_is_a2_over_4=boundary,
        deep_ratios_are_quarter=deep,
        classification=classification,
    )
