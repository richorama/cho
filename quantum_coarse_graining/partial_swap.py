"""Sharp scalar reduction for the qubit partial-SWAP signalling defect."""

from __future__ import annotations

from fractions import Fraction
from typing import Tuple

from .cartan import CartanFactor, cartan_unitary
from .exact import (
    Gaussian,
    Matrix,
    add,
    conjugate_action,
    identity,
    partial_trace_b,
    scale,
    subtract,
)
from .swap import swap_unitary


def _validate(cosine: Fraction, sine: Fraction) -> None:
    if cosine * cosine + sine * sine != 1:
        raise ValueError("cosine and sine must lie on the unit circle")


def partial_swap_unitary(cosine: Fraction, sine: Fraction) -> Matrix:
    """The unitary ``cos(phi) I - i sin(phi) SWAP``."""
    cosine, sine = Fraction(cosine), Fraction(sine)
    _validate(cosine, sine)
    return add(
        scale(Gaussian(cosine), identity(4)),
        scale(Gaussian(0, -sine), swap_unitary()),
    )


def depolarizing_channel(operator: Matrix, shrinkage: Fraction) -> Matrix:
    """The covariant qubit channel ``lambda X+(1-lambda)Tr(X)I/2``."""
    shrinkage = Fraction(shrinkage)
    if not Fraction(-1, 3) <= shrinkage <= 1:
        raise ValueError("qubit depolarizing shrinkage must lie in [-1/3,1]")
    trace = operator[0][0] + operator[1][1]
    mixed = scale(trace / Gaussian(2), identity(2))
    return add(
        scale(Gaussian(shrinkage), operator),
        scale(Gaussian(1 - shrinkage), mixed),
    )


def partial_swap_residual(
    operator: Matrix,
    cosine: Fraction,
    sine: Fraction,
    shrinkage: Fraction,
) -> Matrix:
    """Residual for a depolarizing effective channel."""
    unitary = partial_swap_unitary(cosine, sine)
    evolved = partial_trace_b(conjugate_action(unitary, operator), 2, 2)
    coarse_input = partial_trace_b(operator, 2, 2)
    return subtract(
        evolved,
        depolarizing_channel(coarse_input, shrinkage),
    )


def equal_cartan_is_partial_swap(factor: CartanFactor) -> bool:
    """Exact channel identity for ``alpha=beta=gamma`` up to global phase."""
    cosine, sine = (Fraction(value) for value in factor)
    factor = (cosine, sine)
    _validate(cosine, sine)
    double_cosine = cosine * cosine - sine * sine
    double_sine = 2 * cosine * sine
    global_phase = Gaussian(cosine, sine)
    return cartan_unitary((factor, factor, factor)) == scale(
        global_phase,
        partial_swap_unitary(double_cosine, double_sine),
    )


def fixed_channel_terms(
    cosine: Fraction,
    sine: Fraction,
    shrinkage: Fraction,
) -> Tuple[Fraction, Fraction]:
    """Return ``a=(1-lambda)/3`` and the radical ``B`` in the exact norm."""
    cosine, sine = Fraction(cosine), Fraction(sine)
    shrinkage = Fraction(shrinkage)
    _validate(cosine, sine)
    if not Fraction(-1, 3) <= shrinkage <= 1:
        raise ValueError("qubit depolarizing shrinkage must lie in [-1/3,1]")
    a = (1 - shrinkage) / 3
    radical = (1 + shrinkage) ** 2 - 4 * shrinkage * cosine * cosine
    return a, radical


def fixed_channel_defect(
    cosine: Fraction,
    sine: Fraction,
    shrinkage: Fraction,
    radical_root: Fraction,
) -> Fraction:
    """Exact fixed-channel diamond norm when ``radical_root^2=B``.

    The symmetry-reduced SDP gives ``4a`` when ``B<=4a^2`` and
    ``B/(sqrt(B)-a)`` otherwise.
    """
    a, radical = fixed_channel_terms(cosine, sine, shrinkage)
    if radical_root < 0 or radical_root * radical_root != radical:
        raise ValueError("radical_root must be the nonnegative square root of B")
    if radical <= 4 * a * a:
        return 4 * a
    return radical / (radical_root - a)


def weak_partial_swap_defect(
    cosine: Fraction,
    sine: Fraction,
) -> Fraction:
    """Sharp branch ``delta=2 sin(phi)`` for ``0<=sin(phi)<=1/3``."""
    cosine, sine = Fraction(cosine), Fraction(sine)
    _validate(cosine, sine)
    if sine < 0 or sine > Fraction(1, 3) or cosine < 0:
        raise ValueError("outside the weak partial-SWAP branch")
    return 2 * sine


def strong_stationarity_holds(
    cosine: Fraction,
    sine: Fraction,
    shrinkage: Fraction,
    radical_root: Fraction,
) -> bool:
    """Check the unsquared stationarity equation for the strong branch."""
    shrinkage = Fraction(shrinkage)
    a, radical = fixed_channel_terms(cosine, sine, shrinkage)
    if radical_root < 0 or radical_root * radical_root != radical:
        return False
    if radical <= 4 * a * a:
        return False
    offset = 1 - 2 * cosine * cosine
    return (
        3 * (shrinkage + offset) * (radical_root - 2 * a)
        == radical
    )


def partial_swap_boundary_certificate() -> bool:
    """Exact weak and SWAP endpoint certificates for the scalar theorem."""
    weak_cosine = Fraction(40, 41)
    weak_sine = Fraction(9, 41)
    return (
        equal_cartan_is_partial_swap((Fraction(4, 5), Fraction(3, 5)))
        and weak_partial_swap_defect(weak_cosine, weak_sine)
        == Fraction(18, 41)
        and fixed_channel_defect(
            weak_cosine,
            weak_sine,
            Fraction(1),
            2 * weak_sine,
        )
        == Fraction(18, 41)
        and fixed_channel_defect(
            Fraction(0),
            Fraction(1),
            Fraction(0),
            Fraction(1),
        )
        == Fraction(3, 2)
        and strong_stationarity_holds(
            Fraction(0),
            Fraction(1),
            Fraction(0),
            Fraction(1),
        )
    )
