"""Exact complex arithmetic over the Gaussian rationals Q(i).

The classical campaign kept every amplitude in ``fractions.Fraction`` so that no
scientific claim ever depended on floating-point rounding. The amplitude campaign
keeps that discipline: a complex amplitude is an exact pair of rationals, so Born
probabilities are exact rationals and every census below is decidable.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple, Union

Rational = Union[int, Fraction]


@dataclass(frozen=True)
class Gaussian:
    """An exact element ``real + imag * i`` of Q(i)."""

    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "real", Fraction(self.real))
        object.__setattr__(self, "imag", Fraction(self.imag))

    def __add__(self, other: "Gaussian") -> "Gaussian":
        return Gaussian(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: "Gaussian") -> "Gaussian":
        return Gaussian(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other: "Gaussian") -> "Gaussian":
        return Gaussian(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def __neg__(self) -> "Gaussian":
        return Gaussian(-self.real, -self.imag)

    def __truediv__(self, other: "Gaussian") -> "Gaussian":
        denominator = other.norm2()
        if denominator == 0:
            raise ZeroDivisionError("division by the zero Gaussian rational")
        numerator = self * other.conjugate()
        return Gaussian(numerator.real / denominator, numerator.imag / denominator)

    def conjugate(self) -> "Gaussian":
        return Gaussian(self.real, -self.imag)

    def norm2(self) -> Fraction:
        """The exact squared modulus ``|z|^2`` as a nonnegative rational."""
        return self.real * self.real + self.imag * self.imag

    def is_zero(self) -> bool:
        return self.real == 0 and self.imag == 0


ZERO = Gaussian(Fraction(0), Fraction(0))
ONE = Gaussian(Fraction(1), Fraction(0))
I = Gaussian(Fraction(0), Fraction(1))

# The four fourth roots of unity: the exact unit-modulus phases available in Q(i).
FOURTH_ROOTS: Tuple[Gaussian, ...] = (
    Gaussian(Fraction(1), Fraction(0)),
    Gaussian(Fraction(0), Fraction(1)),
    Gaussian(Fraction(-1), Fraction(0)),
    Gaussian(Fraction(0), Fraction(-1)),
)


Vector = Tuple[Gaussian, ...]


def from_int_pairs(pairs: Tuple[Tuple[int, int], ...]) -> Vector:
    """Build a state vector from ``(real, imag)`` integer pairs."""
    return tuple(Gaussian(Fraction(r), Fraction(m)) for r, m in pairs)


def inner_product(bra: Vector, ket: Vector) -> Gaussian:
    """The Hermitian inner product ``<bra|ket> = sum conj(bra_k) * ket_k``."""
    if len(bra) != len(ket):
        raise ValueError("inner product needs vectors of one common dimension")
    total = ZERO
    for left, right in zip(bra, ket):
        total = total + left.conjugate() * right
    return total


def squared_norm(vector: Vector) -> Fraction:
    """The exact squared norm ``<vector|vector>`` as a positive rational."""
    return sum((amplitude.norm2() for amplitude in vector), Fraction(0))


def born_probability(effect: Vector, state: Vector) -> Fraction:
    """Exact Born rule for the projective effect ``|effect><effect|``.

    Returns ``|<effect|state>|^2 / (<effect|effect> <state|state>)`` in ``[0, 1]``.
    Neither vector needs prior normalisation; the denominator does it exactly.
    """
    effect_norm = squared_norm(effect)
    state_norm = squared_norm(state)
    if effect_norm == 0 or state_norm == 0:
        raise ValueError("effect and state vectors must be nonzero")
    return inner_product(effect, state).norm2() / (effect_norm * state_norm)
