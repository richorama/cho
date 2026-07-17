"""Gate Q11: does observer-consistency select the Born rule? (2-norm as a holdout)

Every prior gate *assumes* the Born rule ``p = |<e|s>|^2 / ...``. Gate Q11 turns the
2-norm itself into an unselected holdout and asks whether observer-consistency forces
it. Consider the one-parameter family of ``r``-norm outcome rules for a complete
measurement ``{e_k}`` on a state ``s``:

    q_r(k) = |<e_k|s>|^r / sum_j |<e_j|s>|^r,          r in {2, 4, 6, ...}.

For ``r = 2`` this is Born. To keep every quantity an exact rational over Q(i) the
exponent is written ``r = 2p`` and the rule uses the exact Born weights
``t_k = born_probability(e_k, s)`` (already a rational), so ``q_r(k) = t_k^p / sum_j
t_j^p`` with ``p = 1`` recovering Born.

The observer-consistency demand is *non-contextuality*: an outcome direction ``e`` that
appears in two different complete measurements must be assigned the same probability,
because no internal observer can tell which surrounding measurement was used. Embedding a
shared effect ``e`` in two orthonormal bases of a three-dimensional space and comparing
``q_r(e)`` gives an exact, finite Gleason-style test. The findings, all exact over Q(i):

* ``r = 2`` (Born) is the unique exponent with *zero* contextual discrepancies — Parseval
  makes ``sum_j t_j = 1`` in every basis, so ``q_2(e) = t_e`` depends only on ``e`` and
  ``s``. Every ``r > 2`` is exposed as contextual.
* Only a *superposing* change of description exposes ``r > 2``. A classical relabelling
  (a permutation of outcomes) leaves the weight multiset unchanged, so it certifies
  nothing — it is the amplitude premise (genuine superposition) that does the selecting.
* The effect requires Hilbert dimension at least three: in a qubit the complement of a
  shared effect is forced, so no exponent can be distinguished. This is exactly the
  Gleason dimension threshold, recovered by finite enumeration.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, NamedTuple, Optional, Tuple

from .census import census_state_vectors
from .gaussian import ONE, ZERO, Gaussian, Vector, born_probability

Basis = Tuple[Vector, ...]

_I = Gaussian(Fraction(0), Fraction(1))


def _g(real: int, imag: int = 0) -> Gaussian:
    return Gaussian(Fraction(real), Fraction(imag))


# --- Exact three-dimensional orthonormal bases (unnormalised) sharing effect e0. ---
# born_probability normalises each effect, so integer-scaled vectors are exact and legal.

_E0: Vector = (ONE, ZERO, ZERO)

# Computational basis.
COMPUTATIONAL: Basis = (_E0, (ZERO, ONE, ZERO), (ZERO, ZERO, ONE))

# Real (Pythagorean) rotation of the {1, 2} plane: genuine superposition, exact over Q.
REAL_SUPERPOSED: Basis = (_E0, (ZERO, _g(3), _g(4)), (ZERO, _g(-4), _g(3)))

# Complex (phase) rotation of the {1, 2} plane: <(0,1,i)|(0,i,1)> = i - i = 0, exact.
PHASE_SUPERPOSED: Basis = (_E0, (ZERO, ONE, _I), (ZERO, _I, ONE))

# Classical relabelling control: same effects as the computational basis, reordered.
PERMUTED: Basis = (_E0, (ZERO, ZERO, ONE), (ZERO, ONE, ZERO))

SUPERPOSING_BASES: Tuple[Tuple[str, Basis], ...] = (
    ("real_superposed", REAL_SUPERPOSED),
    ("phase_superposed", PHASE_SUPERPOSED),
)

# Declared exponents: p = 1 is Born (r = 2); p = 2, 3 are the r = 4, 6 alternatives.
EXPONENTS: Tuple[int, ...] = (1, 2, 3)


def _weights(basis: Basis, state: Vector) -> List[Fraction]:
    return [born_probability(effect, state) for effect in basis]


def _q(basis: Basis, state: Vector, power: int, outcome: int = 0) -> Optional[Fraction]:
    weights = _weights(basis, state)
    denominator = sum((weight ** power for weight in weights), Fraction(0))
    if denominator == 0:
        return None
    return weights[outcome] ** power / denominator


def contextual_mismatches(
    basis_a: Basis, basis_b: Basis, power: int, dimension: int = 3
) -> int:
    """Count states where the shared effect's ``q_r`` differs between two bases."""
    mismatches = 0
    for state in census_state_vectors(dimension):
        value_a = _q(basis_a, state, power)
        value_b = _q(basis_b, state, power)
        if value_a is None or value_b is None:
            continue
        if value_a != value_b:
            mismatches += 1
    return mismatches


class BornSelection(NamedTuple):
    born_power: int
    born_mismatches_under_superposition: int
    alternative_mismatches_under_superposition: Tuple[Tuple[int, int], ...]
    born_is_uniquely_noncontextual: bool
    relabelling_exposes_nothing: bool


def born_selection_census() -> BornSelection:
    """Exact test that only the 2-norm survives non-contextuality under superposition."""
    born_power = 1

    born_super = sum(
        contextual_mismatches(COMPUTATIONAL, basis, born_power)
        for _, basis in SUPERPOSING_BASES
    )

    alternative: List[Tuple[int, int]] = []
    born_unique = True
    for power in EXPONENTS:
        total = sum(
            contextual_mismatches(COMPUTATIONAL, basis, power)
            for _, basis in SUPERPOSING_BASES
        )
        if power != born_power:
            alternative.append((power, total))
            if total == 0:
                born_unique = False
        elif total != 0:
            born_unique = False

    relabelling_clean = all(
        contextual_mismatches(COMPUTATIONAL, PERMUTED, power) == 0
        for power in EXPONENTS
    )

    return BornSelection(
        born_power=born_power,
        born_mismatches_under_superposition=born_super,
        alternative_mismatches_under_superposition=tuple(alternative),
        born_is_uniquely_noncontextual=born_unique,
        relabelling_exposes_nothing=relabelling_clean,
    )


def qubit_cannot_distinguish() -> bool:
    """In dimension two every exponent is non-contextual: selection needs dim >= 3."""
    shared: Vector = (ONE, ZERO)
    basis_a: Basis = (shared, (ZERO, ONE))
    basis_b: Basis = (shared, (ZERO, _I))
    for power in EXPONENTS:
        if contextual_mismatches(basis_a, basis_b, power, dimension=2) != 0:
            return False
    return True
