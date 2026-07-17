"""Gate Q12: the Born rule as a resolution-agreement (frame-function) theorem.

Gate Q11 showed that only the 2-norm is non-contextual, tested in dimension three. A
referee's first two questions are: does it survive higher dimension, and is this really
the project's own *resolution-agreement* principle rather than imported Gleason
machinery? Gate Q12 answers both by recasting the selection as an exact frame-function
consistency statement and running it in dimensions three and four.

A frame function for the ``r``-norm rule assigns each unit effect direction ``e`` the
weight ``|<e|s>|^r``. Observer-consistency across resolutions demands that the total
weight of a *complete* measurement — the sum over any orthonormal basis — be the same no
matter which basis (which maximal set of jointly measurable outcomes) the observer chose;
otherwise the total probability would depend on the arbitrary fine measurement frame. The
exact censuses below show, over Q(i):

* ``r = 2`` (Born): the frame sum equals ``<s|s>`` for *every* orthonormal basis, in both
  dimensions (Parseval). It is the unique exponent that is frame-consistent.
* ``r = 4`` and ``r = 6``: the frame sum depends on the basis for essentially every state,
  in both dimensions — the rule is not resolution-consistent.
* Only a genuinely *superposing* change of basis exposes the inconsistency; a classical
  relabelling (a permutation of outcomes) leaves the frame sum unchanged for every
  exponent, so superposition is what does the selecting.

Weights are kept exact: for an integer-scaled effect ``e`` the normalised weight
``|<e^|s>|^2 = |<e|s>|^2 / <e|e>`` is a rational, and ``r = 2p`` uses its ``p``-th power.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, NamedTuple, Tuple

from .census import census_state_vectors
from .gaussian import ONE, ZERO, Gaussian, Vector, inner_product, squared_norm

Basis = Tuple[Vector, ...]

_I = Gaussian(Fraction(0), Fraction(1))


def _g(real: int, imag: int = 0) -> Gaussian:
    return Gaussian(Fraction(real), Fraction(imag))


def _computational(dimension: int) -> Basis:
    return tuple(
        tuple(ONE if k == m else ZERO for k in range(dimension))
        for m in range(dimension)
    )


def _rotate_plane(
    dimension: int, i: int, j: int, a: Gaussian, b: Gaussian, c: Gaussian, d: Gaussian
) -> Basis:
    """The computational basis with the ``{i, j}`` plane sent through ``[[a, b], [c, d]]``.

    The two columns ``(a, c)`` and ``(b, d)`` must be orthonormal (up to a common scale)
    for the result to be an orthogonal basis; every rotation used here satisfies that
    exactly over Q(i).
    """
    vectors: List[Vector] = []
    for k in range(dimension):
        entries = [ZERO] * dimension
        if k == i:
            entries[i], entries[j] = a, c
        elif k == j:
            entries[i], entries[j] = b, d
        else:
            entries[k] = ONE
        vectors.append(tuple(entries))
    return tuple(vectors)


# Exact orthonormal bases per dimension: the computational basis plus genuinely
# superposing frames (real Pythagorean rotations in two disjoint planes, and a complex
# phase rotation). The permutation frame is the classical-relabelling control.
def _superposing_bases(dimension: int) -> Tuple[Basis, ...]:
    pyth = (_g(3), _g(-4), _g(4), _g(3))  # exact rational rotation
    phase = (ONE, _I, _I, ONE)  # <(1,i)|(i,1)> = 0, an exact complex frame
    if dimension == 3:
        return (
            _computational(3),
            _rotate_plane(3, 1, 2, *pyth),
            _rotate_plane(3, 0, 1, *pyth),
            _rotate_plane(3, 1, 2, *phase),
        )
    if dimension == 4:
        return (
            _computational(4),
            _rotate_plane(4, 0, 1, *pyth),
            _rotate_plane(4, 2, 3, *pyth),
            _rotate_plane(4, 1, 2, *phase),
        )
    raise ValueError("declared frames exist for dimensions 3 and 4")


def _permutation_basis(dimension: int) -> Basis:
    computational = _computational(dimension)
    order = list(range(dimension))
    for k in range(0, dimension - 1, 2):
        order[k], order[k + 1] = order[k + 1], order[k]
    return tuple(computational[k] for k in order)


def _normalised_weight(effect: Vector, state: Vector, power: int) -> Fraction:
    weight = inner_product(effect, state).norm2() / squared_norm(effect)
    return weight ** power


def _frame_sum(basis: Basis, state: Vector, power: int) -> Fraction:
    return sum((_normalised_weight(effect, state, power) for effect in basis), Fraction(0))


# Declared exponents: p = 1 is Born (r = 2); p = 2, 3 are the r = 4, 6 alternatives.
EXPONENTS: Tuple[int, ...] = (1, 2, 3)


def frame_inconsistency(bases: Tuple[Basis, ...], dimension: int, power: int) -> int:
    """States whose frame sum depends on which basis of ``bases`` is used."""
    inconsistent = 0
    for state in census_state_vectors(dimension):
        sums = {_frame_sum(basis, state, power) for basis in bases}
        if len(sums) > 1:
            inconsistent += 1
    return inconsistent


def born_is_exactly_parseval(dimension: int) -> bool:
    """For r = 2 every frame sum equals <s|s>, exactly, in every declared basis."""
    for basis in _superposing_bases(dimension):
        for state in census_state_vectors(dimension):
            if _frame_sum(basis, state, 1) != squared_norm(state):
                return False
    return True


class FrameConsistency(NamedTuple):
    dimension: int
    total_states: int
    born_inconsistent: int
    alternative_inconsistent: Tuple[Tuple[int, int], ...]
    relabelling_inconsistent: Tuple[Tuple[int, int], ...]
    born_is_uniquely_consistent: bool


def frame_consistency_census(dimension: int) -> FrameConsistency:
    """Exact frame-consistency profile of the r-norm rules in one dimension."""
    superposing = _superposing_bases(dimension)
    relabelling = (_computational(dimension), _permutation_basis(dimension))
    total = len(census_state_vectors(dimension))

    born_inconsistent = frame_inconsistency(superposing, dimension, 1)
    alternative: List[Tuple[int, int]] = []
    relabel: List[Tuple[int, int]] = []
    unique = born_inconsistent == 0
    for power in EXPONENTS:
        relabel.append((power, frame_inconsistency(relabelling, dimension, power)))
        if power == 1:
            continue
        count = frame_inconsistency(superposing, dimension, power)
        alternative.append((power, count))
        if count == 0:
            unique = False

    return FrameConsistency(
        dimension=dimension,
        total_states=total,
        born_inconsistent=born_inconsistent,
        alternative_inconsistent=tuple(alternative),
        relabelling_inconsistent=tuple(relabel),
        born_is_uniquely_consistent=unique,
    )


# --- Focused, exact certificates for the standalone Born-rule theorem. ------------
# See BORN_RULE_THEOREM.md. These realise the proof's three ingredients on a single
# explicit configuration, independent of the ensemble-wide censuses above.

_WITNESS_STATE: Vector = (ONE, ONE, ONE)  # genuine equal superposition in C^3
_WITNESS_SHARED: Vector = (ONE, ZERO, ZERO)
# Two orthonormal bases sharing the effect e0, differing only by a rational rotation
# of the orthogonal complement {1, 2}.
_WITNESS_A: Basis = (_WITNESS_SHARED, (ZERO, ONE, ZERO), (ZERO, ZERO, ONE))
_WITNESS_B: Basis = (_WITNESS_SHARED, (ZERO, _g(3), _g(4)), (ZERO, _g(-4), _g(3)))


def _monomial_image(
    basis: Basis, order: Tuple[int, ...], phases: Tuple[Gaussian, ...]
) -> Basis:
    """Relabel a basis by a permutation and multiply each vector by a unit phase."""
    return tuple(
        tuple(phases[k] * basis[order[k]][m] for m in range(len(basis)))
        for k in range(len(basis))
    )


class TheoremWitness(NamedTuple):
    parseval_constant: Fraction
    born_split_equal: bool
    alternative_split_totals: Tuple[Tuple[int, Fraction, Fraction], ...]
    monomial_invariant_for_all_exponents: bool


def theorem_witnesses() -> TheoremWitness:
    """Exact certificates for sufficiency, necessity, and the superposition control.

    * Sufficiency: for r = 2 the complement-split totals both equal ``<s|s>`` (Parseval).
    * Necessity: for r = 4 and r = 6 the two splits give different totals (contextual).
    * Superposition control: a permutation-with-phase (monomial) relabelling of a basis
      leaves the total unchanged for every exponent, so only genuine superposition can
      expose r != 2.
    """
    state = _WITNESS_STATE
    parseval = squared_norm(state)

    born_a = _frame_sum(_WITNESS_A, state, 1)
    born_b = _frame_sum(_WITNESS_B, state, 1)
    born_equal = born_a == born_b == parseval

    alternatives = tuple(
        (power, _frame_sum(_WITNESS_A, state, power), _frame_sum(_WITNESS_B, state, power))
        for power in (2, 3)
    )

    monomial = _monomial_image(
        _WITNESS_A, (2, 0, 1), (ONE, _I, Gaussian(Fraction(-1), Fraction(0)))
    )
    monomial_invariant = all(
        _frame_sum(monomial, state, power) == _frame_sum(_WITNESS_A, state, power)
        for power in EXPONENTS
    )

    return TheoremWitness(
        parseval_constant=parseval,
        born_split_equal=born_equal,
        alternative_split_totals=alternatives,
        monomial_invariant_for_all_exponents=monomial_invariant,
    )


class DimensionalWitness(NamedTuple):
    dimension: int
    parseval_constant: Fraction
    splits: Tuple[Tuple[int, Fraction, Fraction], ...]  # (r, split_A, split_B)


def dimensional_necessity_witnesses(
    dimensions: Tuple[int, ...] = (3, 4, 5),
) -> Tuple[DimensionalWitness, ...]:
    """Exact complement-split necessity certificate in several dimensions at once.

    For each dimension ``d >= 3`` it builds two orthonormal bases of ``C^d`` that share
    the effect ``e0`` and differ only by a rational (Pythagorean) rotation of the
    ``{1, 2}`` complement plane, evaluated on the equal superposition
    ``s = (1, 1, ..., 1)``. It returns, per dimension, the Parseval constant ``<s|s> = d``
    together with the two frame totals for ``r = 2, 4, 6``.

    For ``r = 2`` the two totals agree and equal ``d`` (Parseval / Born). For ``r = 4`` and
    ``r = 6`` they differ, so the necessity of the Born exponent is witnessed exactly in
    *every* listed dimension, not just ``d = 3`` — the ``d = 3`` case of this construction
    reproduces the split totals used by :func:`theorem_witnesses`.
    """
    rotation = (_g(3), _g(-4), _g(4), _g(3))  # exact rational rotation, columns orthogonal
    out: List[DimensionalWitness] = []
    for dimension in dimensions:
        if dimension < 3:
            raise ValueError("the complement-split witness needs dimension >= 3")
        basis_a = _computational(dimension)
        basis_b = _rotate_plane(dimension, 1, 2, *rotation)
        state = tuple(ONE for _ in range(dimension))
        splits = tuple(
            (2 * power, _frame_sum(basis_a, state, power), _frame_sum(basis_b, state, power))
            for power in EXPONENTS
        )
        out.append(
            DimensionalWitness(
                dimension=dimension,
                parseval_constant=squared_norm(state),
                splits=splits,
            )
        )
    return tuple(out)
