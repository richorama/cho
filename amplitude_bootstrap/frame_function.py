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
