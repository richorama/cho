"""Gate Q15: is any coupling relevant? A sweep for interaction that escapes the flow.

Gate Q14 showed one coupling family (controlled rotations) is *irrelevant*: its closure
defect contracts under every spatial coarse-graining and renormalises to zero. The
make-or-break question for a would-be interacting theory is whether *any* coupling
escapes that flow -- a coupling whose defect stays constant (marginal) or grows
(relevant) under recursion would be the first candidate for genuinely emergent
interacting physics in this crucible.

Q15 answers it with a broad, declared sweep. A family of exactly-unitary, genuinely
entangling two-qubit generators over Q(i) is each laid down as a translation-invariant
nearest-neighbour coupling on a chain, optionally repeated to depth ``t`` (a growing
light cone), and coarse-grained by tracing the end qubit repeatedly. Every flow is
classified by its step-to-step contraction ratios.

The exact findings (owned by ``tests/test_gate_q15_interaction_relevance.py``):

* **Every generator is entangling yet irrelevant.** At depth one, every member of the
  declared family has a strictly positive level-one defect (it is genuinely
  interacting) and a defect flow that strictly contracts to zero -- classified
  irrelevant. No member is marginal or relevant.

* **Depth spreads interaction but does not make it relevant.** The ``iSWAP`` generator
  is a clean light-cone witness: the number of coarse-graining steps its defect
  survives grows with the circuit depth (``1 -> 2 -> 3`` steps at depth ``1 -> 2 ->
  3``), because the coupling transports correlations further. Yet each spatial
  decimation still contracts the defect, so the coupling stays irrelevant at every
  depth.

* **The dilution is dimensional.** The deep-recursion contraction is set by the Hilbert
  dimension of the traced factor (a step ratio of ``1/4 = 1/2^2`` for a qubit), so pure
  decimation can never sustain an interaction. A relevant coupling would require a
  coarse-graining that compensates this dimensional dilution -- the missing ingredient
  the sweep makes precise.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, NamedTuple, Optional, Tuple

from .gaussian import ONE, ZERO, Gaussian
from .linalg import Matrix, dagger, identity, kron, matmul
from .renormalization_flow import reduce_with_defect
from .spatial import _channel_action, _conjugation

_I = Gaussian(Fraction(0), Fraction(1))


def _g(real: int, imag: int = 0) -> Gaussian:
    return Gaussian(Fraction(real), Fraction(imag))


# --- A broad, declared family of exactly-unitary entangling two-qubit gates. ------

_CNOT: Matrix = (
    (ONE, ZERO, ZERO, ZERO),
    (ZERO, ONE, ZERO, ZERO),
    (ZERO, ZERO, ZERO, ONE),
    (ZERO, ZERO, ONE, ZERO),
)
_CZ: Matrix = tuple(
    tuple(_g(-1) if (r == 3 and c == 3) else (ONE if r == c else ZERO) for c in range(4))
    for r in range(4)
)
_SWAP: Matrix = (
    (ONE, ZERO, ZERO, ZERO),
    (ZERO, ZERO, ONE, ZERO),
    (ZERO, ONE, ZERO, ZERO),
    (ZERO, ZERO, ZERO, ONE),
)
_ISWAP: Matrix = (
    (ONE, ZERO, ZERO, ZERO),
    (ZERO, ZERO, _I, ZERO),
    (ZERO, _I, ZERO, ZERO),
    (ZERO, ZERO, ZERO, ONE),
)
_CS: Matrix = tuple(
    tuple(_I if (r == 3 and c == 3) else (ONE if r == c else ZERO) for c in range(4))
    for r in range(4)
)
# Controlled Pythagorean rotation: |0><0| (x) I + |1><1| (x) R(4/5, 3/5).
_CROT: Matrix = (
    (ONE, ZERO, ZERO, ZERO),
    (ZERO, ONE, ZERO, ZERO),
    (ZERO, ZERO, Gaussian(Fraction(4, 5)), Gaussian(Fraction(-3, 5))),
    (ZERO, ZERO, Gaussian(Fraction(3, 5)), Gaussian(Fraction(4, 5))),
)
# Double CNOT = CNOT . SWAP, a distinct permutation entangler.
_DCNOT: Matrix = matmul(_CNOT, _SWAP)

GATE_FAMILY: Tuple[Tuple[str, Matrix], ...] = (
    ("cnot", _CNOT),
    ("cz", _CZ),
    ("swap", _SWAP),
    ("iswap", _ISWAP),
    ("cs", _CS),
    ("crot", _CROT),
    ("dcnot", _DCNOT),
)

# A non-interacting control: a local product gate (no coupling), all-zero flow.
LOCAL_PRODUCT: Matrix = kron(
    ((ONE, ZERO), (ZERO, _I)), ((Gaussian(Fraction(3, 5)), Gaussian(Fraction(-4, 5))),
                                (Gaussian(Fraction(4, 5)), Gaussian(Fraction(3, 5))))
)


# --- Chain construction for an arbitrary two-qubit generator. --------------------

def _embed_pair(gate: Matrix, bond: int, n_qubits: int) -> Matrix:
    """Place a two-qubit ``gate`` on adjacent qubits ``(bond, bond + 1)``."""
    result = gate
    if bond > 0:
        result = kron(identity(1 << bond), result)
    tail = n_qubits - bond - 2
    if tail > 0:
        result = kron(result, identity(1 << tail))
    return result


def gate_chain(gate: Matrix, n_qubits: int, depth: int = 1) -> Matrix:
    """``depth`` layers of nearest-neighbour ``gate`` couplings on an ``n``-qubit chain."""
    if n_qubits < 2:
        raise ValueError("a chain needs at least two qubits")
    layer = _embed_pair(gate, 0, n_qubits)
    for bond in range(1, n_qubits - 1):
        layer = matmul(layer, _embed_pair(gate, bond, n_qubits))
    unitary = identity(1 << n_qubits)
    for _ in range(depth):
        unitary = matmul(unitary, layer)
    return unitary


def gate_defect_flow(gate: Matrix, n_qubits: int, depth: int = 1) -> Tuple[Fraction, ...]:
    """Closure defects from tracing the end qubit repeatedly, for any generator."""
    apply_fn = _conjugation(gate_chain(gate, n_qubits, depth))
    defects: List[Fraction] = []
    size = n_qubits
    for qubit in range(n_qubits - 1, 0, -1):
        channel, defect = reduce_with_defect(apply_fn, size, qubit)
        defects.append(defect)
        apply_fn = _channel_action(channel, 1 << (size - 1))
        size -= 1
    return tuple(defects)


# --- Relevance classification. ---------------------------------------------------

def _max_ratio(defects: Tuple[Fraction, ...]) -> Optional[Fraction]:
    """Largest step ratio ``d_{k+1}/d_k`` over levels with a positive predecessor.

    A defect that drops to zero contributes ratio ``0`` (an absorbing fixed point).
    Returns None when the flow is identically zero (already at the fixed point).
    """
    ratios: List[Fraction] = []
    for k in range(len(defects) - 1):
        if defects[k] == 0:
            continue
        ratios.append(defects[k + 1] / defects[k])
    return max(ratios) if ratios else None


def classify(defects: Tuple[Fraction, ...]) -> str:
    """Label a defect flow relevant / marginal / irrelevant / fixed_point."""
    if all(defect == 0 for defect in defects):
        return "fixed_point"
    largest = _max_ratio(defects)
    if largest is None or largest < 1:
        return "irrelevant"
    if largest == 1:
        return "marginal"
    return "relevant"


def _reach(defects: Tuple[Fraction, ...]) -> int:
    """Number of coarse-graining levels the defect survives (last positive index + 1)."""
    reach = 0
    for level, defect in enumerate(defects, start=1):
        if defect > 0:
            reach = level
    return reach


class RelevanceRow(NamedTuple):
    name: str
    defects: Tuple[Fraction, ...]
    level_one_positive: bool
    classification: str
    reach: int


def relevance_census(n_qubits: int = 3, depth: int = 1) -> Tuple[RelevanceRow, ...]:
    """Classify every declared entangling generator by its defect flow."""
    rows: List[RelevanceRow] = []
    for name, gate in GATE_FAMILY:
        defects = gate_defect_flow(gate, n_qubits, depth)
        rows.append(
            RelevanceRow(
                name=name,
                defects=defects,
                level_one_positive=defects[0] > 0,
                classification=classify(defects),
                reach=_reach(defects),
            )
        )
    return tuple(rows)


class SweepSummary(NamedTuple):
    family_size: int
    all_entangling: bool           # every generator has a positive level-one defect
    all_irrelevant: bool           # every generator's flow contracts to zero
    relevant_found: int
    marginal_found: int
    local_control_is_fixed_point: bool


def sweep_summary(n_qubits: int = 3, depth: int = 1) -> SweepSummary:
    """Aggregate verdict of the relevance sweep: does any coupling escape the flow?"""
    rows = relevance_census(n_qubits, depth)
    local_flow = gate_defect_flow(LOCAL_PRODUCT, n_qubits, depth)
    return SweepSummary(
        family_size=len(rows),
        all_entangling=all(row.level_one_positive for row in rows),
        all_irrelevant=all(row.classification == "irrelevant" for row in rows),
        relevant_found=sum(1 for row in rows if row.classification == "relevant"),
        marginal_found=sum(1 for row in rows if row.classification == "marginal"),
        local_control_is_fixed_point=classify(local_flow) == "fixed_point",
    )


def light_cone_reach(
    gate: Matrix, n_qubits: int, depths: Tuple[int, ...]
) -> Tuple[Tuple[int, int], ...]:
    """The defect reach at each circuit depth: how far interaction spreads with time."""
    return tuple(
        (depth, _reach(gate_defect_flow(gate, n_qubits, depth))) for depth in depths
    )
