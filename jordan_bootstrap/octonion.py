"""Exact arithmetic on the real normed division algebras via Cayley-Dickson.

The classical campaign kept every amplitude in ``fractions.Fraction`` and the
amplitude campaign kept a complex amplitude as an exact pair of rationals over
``Q(i)``. This campaign changes exactly one premise again and walks the whole
division-algebra ladder ``R -> C -> H -> O`` (real, complex, quaternion,
octonion). The ladder *is* the code: a level-``k`` number is a flat tuple of
``2**k`` rationals, and multiplication is the Cayley-Dickson doubling

    (a, b)(c, d) = (a*c - conj(d)*b,  d*a + b*conj(c))

applied recursively down to the real base case. Every coordinate stays an exact
``Fraction`` so every norm, inverse, and associativity check below is decidable
and never depends on floating point.

Hurwitz's theorem (1898) says ``R, C, H, O`` are the *only* normed division
algebras: the norm form ``|x|^2 = x conj(x)`` is multiplicative exactly up to the
octonions and fails at the next doubling (the sedenions), which is the ladder's
declared kill condition and the reason the octonions are the last stop.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence, Tuple, Union

Rational = Union[int, Fraction]
Flat = Tuple[Fraction, ...]


def _conj(x: Flat) -> Flat:
    """Cayley-Dickson conjugate: ``(a, b)* = (a*, -b)`` down to ``r* = r``."""
    n = len(x)
    if n == 1:
        return x
    h = n // 2
    a, b = x[:h], x[h:]
    return _conj(a) + tuple(-v for v in b)


def _add(x: Flat, y: Flat) -> Flat:
    return tuple(p + q for p, q in zip(x, y))


def _sub(x: Flat, y: Flat) -> Flat:
    return tuple(p - q for p, q in zip(x, y))


def _mul(x: Flat, y: Flat) -> Flat:
    """Recursive Cayley-Dickson product on flat tuples of equal length ``2**k``."""
    n = len(x)
    if n != len(y):
        raise ValueError("Cayley-Dickson product needs equal levels")
    if n == 1:
        return (x[0] * y[0],)
    h = n // 2
    a, b = x[:h], x[h:]
    c, d = y[:h], y[h:]
    left = _sub(_mul(a, c), _mul(_conj(d), b))
    right = _add(_mul(d, a), _mul(b, _conj(c)))
    return left + right


def cd_mul(x: Flat, y: Flat) -> Flat:
    """Public Cayley-Dickson product, exposed for the ladder/kill-condition gate."""
    return _mul(x, y)


def cd_norm2(x: Flat) -> Fraction:
    """Exact squared norm ``sum x_i^2`` at any ladder level."""
    return sum((v * v for v in x), Fraction(0))


@dataclass(frozen=True)
class Octonion:
    """An exact octonion ``sum_{k=0}^{7} coords[k] * e_k`` over the rationals."""

    coords: Flat

    def __post_init__(self) -> None:
        if len(self.coords) != 8:
            raise ValueError("an octonion has exactly eight rational coordinates")
        object.__setattr__(
            self, "coords", tuple(Fraction(c) for c in self.coords)
        )

    def __add__(self, other: "Octonion") -> "Octonion":
        return Octonion(_add(self.coords, other.coords))

    def __sub__(self, other: "Octonion") -> "Octonion":
        return Octonion(_sub(self.coords, other.coords))

    def __mul__(self, other: "Octonion") -> "Octonion":
        return Octonion(_mul(self.coords, other.coords))

    def __neg__(self) -> "Octonion":
        return Octonion(tuple(-c for c in self.coords))

    def scaled(self, factor: Rational) -> "Octonion":
        """Multiply every coordinate by a rational scalar (real scaling)."""
        f = Fraction(factor)
        return Octonion(tuple(c * f for c in self.coords))

    def conjugate(self) -> "Octonion":
        return Octonion(_conj(self.coords))

    def norm2(self) -> Fraction:
        """Exact squared modulus ``|x|^2`` as a nonnegative rational."""
        return cd_norm2(self.coords)

    def is_zero(self) -> bool:
        return all(c == 0 for c in self.coords)

    def inverse(self) -> "Octonion":
        """Exact two-sided inverse ``conj(x) / |x|^2`` (octonions are a division algebra)."""
        denom = self.norm2()
        if denom == 0:
            raise ZeroDivisionError("the zero octonion is not invertible")
        conj = self.conjugate()
        return Octonion(tuple(c / denom for c in conj.coords))

    def is_unit(self) -> bool:
        return self.norm2() == 1


def octonion(*coords: Rational) -> Octonion:
    """Build an octonion from eight rational coordinates."""
    return Octonion(tuple(Fraction(c) for c in coords))


def basis(k: int) -> Octonion:
    """The unit basis octonion ``e_k`` for ``k`` in ``0..7``."""
    if not 0 <= k < 8:
        raise ValueError("octonion basis index must be in 0..7")
    return octonion(*(1 if i == k else 0 for i in range(8)))


# The eight imaginary/real basis units e_0..e_7 (e_0 = 1 is the real unit).
E = tuple(basis(k) for k in range(8))
ONE = E[0]
ZERO = octonion(0, 0, 0, 0, 0, 0, 0, 0)


def _axis_units() -> Tuple[Octonion, ...]:
    """The sixteen signed basis units ``+-e_k`` (the octonionic 'monomial' subgroup)."""
    units = []
    for k in range(8):
        units.append(basis(k))
        units.append(-basis(k))
    return tuple(units)


def _pythagorean_units() -> Tuple[Octonion, ...]:
    """Exact rational unit octonions that genuinely superpose two axes.

    Each places the rational Pythagorean pair ``(3/5, 4/5)`` into an ordered pair
    of distinct coordinates with independent signs. These are the octonionic echo
    of the exact ``(3,4,5)`` rotations that power the amplitude campaign's Born
    selection: every one has exact norm ``1`` yet mixes two basis directions.
    """
    three = Fraction(3, 5)
    four = Fraction(4, 5)
    units = []
    for p in range(8):
        for q in range(8):
            if p == q:
                continue
            for sp in (1, -1):
                for sq in (1, -1):
                    coords = [Fraction(0)] * 8
                    coords[p] = sp * three
                    coords[q] = sq * four
                    units.append(Octonion(tuple(coords)))
    return tuple(units)


# The declared, exhaustive census of exactly-representable unit-octonion
# representation changes: signed axes (relabelings + sign) and genuine
# two-axis superpositions. Frozen before inspection, like every project gate.
# (Its size happens to be 240; this is a coincidence of the construction and is
# NOT the E8 root system, whose 240 unit octonions have irrational coordinates.)
UNIT_OCTONIONS: Tuple[Octonion, ...] = _axis_units() + _pythagorean_units()


def census_states() -> Tuple[Octonion, ...]:
    """A frozen family of nonzero octonion states to test norm invariance on."""
    states = list(_axis_units())
    states.append(octonion(1, 1, 0, 0, 0, 0, 0, 0))
    states.append(octonion(1, 2, 3, 4, 0, 0, 0, 0))
    states.append(octonion(1, -1, 2, -2, 3, -3, 4, -4))
    states.append(octonion(Fraction(1, 2), Fraction(1, 3), 0, 0, 5, 0, 0, 7))
    return tuple(states)
