"""Gate Q16: block-spin coarse-graining does not rescue interaction either.

Gate Q15 traced the origin of interaction-irrelevance to a dimensional dilution: pure
decimation (the partial trace) contracts the closure defect by ``1/dim^2`` per traced
qubit, so no coupling can be relevant. The natural way to fight that is a *block-spin*
coarse-graining -- merge two qubits into one effective qubit through an isometry ``w``
(``w^dagger w = I``, a genuine scale transformation, not a bare trace) chosen to keep the
structure a partial trace would throw away. Does some isometry sustain an interaction?

Q16 answers no, and does so while confirming that block-spin is a *genuinely different*
coarse-graining from decimation. For a microscopic operator ``O`` the block-spin map is
``B_w(O) = w^dagger O w``; on a chain a layer ``W = w (x) w (x) ...`` merges every pair.
The exact least-squares closure defect (Gate Q13) is measured at each level.

The exact findings (owned by ``tests/test_gate_q16_block_spin.py``):

* **Block-spin is inequivalent to decimation.** ``CZ`` has a strictly positive decimation
  defect (``4`` in Gate Q13) but is *exactly autonomous* (defect ``0``) under the
  computational-basis block-spin isometries (``keep``, ``ghz``, ``sym``, ``bell``,
  ``phase``). A single blocking can therefore give a defect the trace cannot -- block-spin
  is a structurally distinct coarse-graining. (A generic entangling isometry ``gen``
  reintroduces a positive defect, so autonomy is a property of the aligned subfamily, not
  of every blocking.)

* **Interaction is still universally irrelevant.** Over a declared family of six exact
  isometries (real and complex over ``Q(i)``) and several entangling couplings, the
  two-level block-spin flow on a four-qubit chain strictly contracts at every step -- the
  worst contraction ratio across the whole sweep is below one. No isometry makes any
  coupling marginal or relevant.

* **The fixed point is robust, not an artefact of the trace.** The non-interacting
  fixed point of Gates Q01/Q09/Q14/Q15 survives a second, inequivalent, dimension-reducing
  coarse-graining. The only remaining escape route is an entangling MERA-style disentangler
  applied before blocking -- a genuinely larger premise this crucible has not yet changed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, List, NamedTuple, Optional, Tuple

from .coarse_graining import _CNOT, _CZ
from .gaussian import ONE, ZERO, Gaussian
from .interaction_relevance import _CROT, classify, gate_chain
from .linalg import Matrix, dagger, identity, kron, matmul, solve_columns

_I = Gaussian(Fraction(0), Fraction(1))


def _g(real: int, imag: int = 0) -> Gaussian:
    return Gaussian(Fraction(real), Fraction(imag))


# --- Declared family of exact block-spin isometries w: C^2 -> C^2 (x) C^2. --------
# Each is a 4x2 matrix with w^dagger w = I_2: two orthonormal fine columns spanning the
# retained coarse subspace. Real and complex (Q(i)) members are included.

def _iso(col0: Tuple[Gaussian, ...], col1: Tuple[Gaussian, ...]) -> Matrix:
    return tuple((col0[r], col1[r]) for r in range(4))


_E = lambda k: tuple(ONE if t == k else ZERO for t in range(4))  # noqa: E731
_R3, _R4 = _g(3, 0), _g(4, 0)
_THREE_FIFTHS, _FOUR_FIFTHS = Gaussian(Fraction(3, 5)), Gaussian(Fraction(4, 5))
_FOUR_FIFTHS_I = Gaussian(Fraction(0), Fraction(4, 5))

ISOMETRIES: Tuple[Tuple[str, Matrix], ...] = (
    # keep first qubit, force environment to |0>  (|0>->|00>, |1>->|10>)
    ("keep", _iso(_E(0), _E(2))),
    # aligned / GHZ embedding  (|0>->|00>, |1>->|11>)
    ("ghz", _iso(_E(0), _E(3))),
    # symmetric superposition  (|1>->(3|01>+4|10>)/5)
    ("sym", _iso(_E(0), (ZERO, _THREE_FIFTHS, _FOUR_FIFTHS, ZERO))),
    # Bell-like real rotation of the {|00>,|11>} plane
    (
        "bell",
        _iso(
            (_THREE_FIFTHS, ZERO, ZERO, _FOUR_FIFTHS),
            (_FOUR_FIFTHS, ZERO, ZERO, -_THREE_FIFTHS),
        ),
    ),
    # complex phase superposition  (|1>->(3|01>+4i|10>)/5)
    ("phase", _iso(_E(0), (ZERO, _THREE_FIFTHS, _FOUR_FIFTHS_I, ZERO))),
    # generic two-dimensional retained subspace
    (
        "gen",
        _iso(
            (_THREE_FIFTHS, ZERO, _FOUR_FIFTHS, ZERO),
            (ZERO, _THREE_FIFTHS, ZERO, _FOUR_FIFTHS),
        ),
    ),
)


def is_isometry(w: Matrix) -> bool:
    return matmul(dagger(w), w) == identity(2)


def block_spin_map(w: Matrix) -> Callable[[Matrix], Matrix]:
    """The operator block-spin ``O -> w^dagger O w``."""
    w_dagger = dagger(w)
    return lambda operator: matmul(matmul(w_dagger, operator), w)


# --- General exact least-squares closure defect for any coarse-graining. ----------

def _vec(operator: Matrix) -> Tuple[Gaussian, ...]:
    return tuple(value for row in operator for value in row)


def _basis_operator(dimension: int, row: int, col: int) -> Matrix:
    return tuple(
        tuple(ONE if (r == row and c == col) else ZERO for c in range(dimension))
        for r in range(dimension)
    )


def _superoperator(images: List[Matrix]) -> Matrix:
    columns = [_vec(image) for image in images]
    coarse_dim = len(columns[0])
    return tuple(
        tuple(columns[fine][coarse] for fine in range(len(columns)))
        for coarse in range(coarse_dim)
    )


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[r][c] for r in range(len(matrix)))
        for c in range(len(matrix[0]))
    )


def closure_defect_general(
    apply_fine: Callable[[Matrix], Matrix],
    coarse_grain: Callable[[Matrix], Matrix],
    fine_dim: int,
) -> Tuple[Optional[Matrix], Fraction]:
    """Exact least-squares defect of an autonomous coarse law for any blocking.

    Returns the best-fit coarse channel and the exact squared Frobenius residual
    ``|| M - E* T ||^2``, where ``T`` and ``M`` are the coarse-graining and
    coarse-grain-after-evolve superoperators built from ``coarse_grain``.
    """
    inputs: List[Matrix] = []
    outputs: List[Matrix] = []
    for i in range(fine_dim):
        for j in range(fine_dim):
            operator = _basis_operator(fine_dim, i, j)
            inputs.append(coarse_grain(operator))
            outputs.append(coarse_grain(apply_fine(operator)))
    trace_super = _superoperator(inputs)
    evolve_super = _superoperator(outputs)
    t_dagger = dagger(trace_super)
    gram = matmul(trace_super, t_dagger)
    target = matmul(evolve_super, t_dagger)
    solution = solve_columns(_transpose(gram), _transpose(target))
    if solution is None:  # pragma: no cover - Gram is full rank for these isometries
        return None, Fraction(-1)
    channel = _transpose(solution)
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


def _conjugation(unitary: Matrix) -> Callable[[Matrix], Matrix]:
    unitary_dagger = dagger(unitary)
    return lambda operator: matmul(matmul(unitary, operator), unitary_dagger)


def _channel_action(channel: Matrix, dimension: int) -> Callable[[Matrix], Matrix]:
    def apply(operator: Matrix) -> Matrix:
        image = matmul(channel, tuple((value,) for value in _vec(operator)))
        flat = [row[0] for row in image]
        return tuple(
            tuple(flat[r * dimension + c] for c in range(dimension))
            for r in range(dimension)
        )

    return apply


def single_block_defect(unitary: Matrix, w: Matrix) -> Fraction:
    """Block-spin defect of a two-qubit unitary merged to one coarse qubit."""
    _, defect = closure_defect_general(_conjugation(unitary), block_spin_map(w), 4)
    return defect


def two_level_flow(gate: Matrix, w: Matrix) -> Tuple[Fraction, Fraction]:
    """Two block-spin steps on a four-qubit chain: (defect_1, defect_2)."""
    unitary = gate_chain(gate, 4, 1)
    layer = kron(w, w)  # 16 x 4: merge (0,1) and (2,3)
    coarse1 = lambda operator: matmul(matmul(dagger(layer), operator), layer)  # noqa: E731
    channel1, defect1 = closure_defect_general(_conjugation(unitary), coarse1, 16)
    coarse2 = block_spin_map(w)
    _, defect2 = closure_defect_general(_channel_action(channel1, 4), coarse2, 4)
    return defect1, defect2


# --- Robustness census. ----------------------------------------------------------

COUPLINGS: Tuple[Tuple[str, Matrix], ...] = (
    ("cz", _CZ),
    ("cnot", _CNOT),
    ("crot", _CROT),
)


class BlockSpinRow(NamedTuple):
    coupling: str
    isometry: str
    defects: Tuple[Fraction, Fraction]
    ratio: Optional[Fraction]
    classification: str


def block_spin_census() -> Tuple[BlockSpinRow, ...]:
    """Two-level block-spin flow for every coupling/isometry pair."""
    rows: List[BlockSpinRow] = []
    for coupling_name, gate in COUPLINGS:
        for iso_name, w in ISOMETRIES:
            d1, d2 = two_level_flow(gate, w)
            ratio = (d2 / d1) if d1 != 0 else None
            rows.append(
                BlockSpinRow(
                    coupling=coupling_name,
                    isometry=iso_name,
                    defects=(d1, d2),
                    ratio=ratio,
                    classification=classify((d1, d2)),
                )
            )
    return tuple(rows)


class BlockSpinSummary(NamedTuple):
    all_isometries_valid: bool
    cz_autonomous_under_some_block_spin: bool  # some isometry sends CZ's defect to 0
    block_spin_differs_from_decimation: bool
    all_irrelevant: bool
    relevant_or_marginal: int
    worst_ratio: Fraction                  # largest contraction ratio in the sweep


def block_spin_summary() -> BlockSpinSummary:
    """Aggregate verdict: does any isometric block-spin rescue interaction?"""
    from .approximate_closure import closure_defect  # decimation defect (Gate Q13)

    rows = block_spin_census()
    valid = all(is_isometry(w) for _, w in ISOMETRIES)
    cz_autonomous = any(
        single_block_defect(_CZ, w) == 0 for _, w in ISOMETRIES
    )
    cz_decimation_positive = closure_defect(_CZ) > 0
    ratios = [row.ratio for row in rows if row.ratio is not None]
    worst = max(ratios) if ratios else Fraction(0)
    return BlockSpinSummary(
        all_isometries_valid=valid,
        cz_autonomous_under_some_block_spin=cz_autonomous,
        block_spin_differs_from_decimation=cz_autonomous and cz_decimation_positive,
        all_irrelevant=all(row.classification in ("irrelevant", "fixed_point") for row in rows),
        relevant_or_marginal=sum(
            1 for row in rows if row.classification in ("relevant", "marginal")
        ),
        worst_ratio=worst,
    )
