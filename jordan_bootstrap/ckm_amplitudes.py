"""Gate O30 -- CKM amplitudes: vector ``sqrt(7)`` vs spinor ``1/2``.

Gate O28 fixed the mixing *probabilities* as Fano-line counts through a single
scale ``eps0^2 = pi/432`` (``|V_us|^2 = 7 eps0^2``). This gate takes the next step
of the master flavour bridge (``compute/epsilon_vcb_halfangle.py`` behind Zenodo
21107402): it explains the two *leading CKM amplitudes* -- one a vector, one a
spinor -- and removes the last ``1/2`` that the probability bridge had to put in by
hand as a "weak-isospin input".

The two channels, exactly over ``Q``
------------------------------------
A spurion history is a small rotation by angle ``eps0`` on the two-level transition
sphere ``S^2 = SU(2)/U(1)``. A transition amplitude is read in whichever
representation carries it, and the ``SU(2) -> SO(3)`` double cover makes the
half-angle explicit:

1. **VECTOR (adjoint) channel -- ``|V_us|``.** The Cabibbo transition lives on the
   7-dimensional imaginary-octonion space ``Im(O)`` (Gate O28's seven Fano
   directions). A vector rotation's off-diagonal amplitude is ``sin(theta)``, whose
   leading coefficient is exactly ``1``; summed coherently over the ``7`` Fano
   directions this is ``sqrt(7) eps0``. So ``|V_us|^2 = 7 eps0^2`` -- the very count
   of Gate O28.

2. **SPINOR (fundamental) channel -- ``|V_cb|``.** An inter-generation transition is
   a single qubit ``vacuum ray <-> broken ray``. In the ``SU(2)`` fundamental a
   rotation acts as ``exp(-i theta n.sigma / 2)``; its off-diagonal amplitude is
   ``sin(theta/2)``, whose leading coefficient is exactly ``1/2``. So
   ``|V_cb| = (1/2) eps0``. The ``1/2`` is the spin-1/2 half-angle of the double
   cover, **not** a weak-isospin number put in by hand.

The contrast ``sqrt(7)`` (vector, full angle, 7 directions) vs ``1/2`` (spinor,
half angle, one qubit) is exactly *vector vs spinor*. This module builds both
generators as exact rational matrices, reads off the two leading transition
coefficients as ``1`` and ``1/2``, and hence certifies the double-cover factor
``1/2`` over ``Q``.

The finite-angle avatar ``tan(pi/8) = sqrt(2) - 1``
---------------------------------------------------
The transition/survival ratio on the Bloch sphere is ``sin(theta/2)/cos(theta/2) =
tan(theta/2)``, whose linearisation has the same leading coefficient ``1/2``. At the
octonionic maximal-reflection angle ``theta = pi/4`` (the 45 degrees between adjacent
imaginary-octonion planes) this ratio is ``tan(pi/8) = sqrt(2) - 1``. This gate
verifies ``tan(pi/8) = sqrt(2) - 1`` **exactly** in ``Q(sqrt 2)`` -- with no floating
point -- through the double-angle relation ``2t/(1 - t^2) = tan(pi/4) = 1``: the
positive root of ``t^2 + 2t - 1 = 0`` is ``sqrt(2) - 1``. The small-angle ``1/2`` and
the 45-degree ``sqrt(2) - 1`` are the *same* spinorial half-angle ``tan(theta/2)``,
linearised versus evaluated at the discrete octonionic reflection.

Predictions (adopted scale ``eps0^2 = pi/432``)
-----------------------------------------------
    |V_us| = sqrt(7) * eps0   (vector)   pred 0.2256  obs 0.2243   +0.6%
    |V_cb| = (1/2)  * eps0    (spinor)   pred 0.0426  obs 0.0422   +1.0%

Non-claim: derived exactly over ``Q`` are (i) the vector leading coefficient ``1``,
(ii) the spinor leading coefficient ``1/2`` as the ``SU(2) -> SO(3)`` half-angle,
their ratio ``1/2``, and (iii) the finite avatar ``tan(pi/8) = sqrt(2) - 1``. What
remains *adopted* (as in the master) is the **channel assignment** -- why ``|V_cb|``
is the spinor inter-generation transition while ``|V_us|`` is the ``Im(O)`` vector --
which follows the two-level/``Im(O)`` split but is not derived from the CHO Yukawa
operator; and the scale ``eps0^2 = pi/432``. The VALUE ``1/2`` is no longer an input;
the channel that carries it is. No mass hierarchy or CP phase follows. Cross-refs
master ``compute/epsilon_vcb_halfangle.py``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from .mixing_web import cabibbo_count

# ---------------------------------------------------------------------------
# Adopted scale (shared with Gates O28/O29) and measured CKM magnitudes.
# ---------------------------------------------------------------------------

# Adopted scale eps0^2 = pi/432 (shared with Gates O28/O29); used as a float only in
# the data-confrontation predictions -- every structural claim below is exact over Q.
_EPS0 = math.sqrt(math.pi / 432.0)

# PDG-2024 central values (spurion_bridge OBSERVED on master).
_V_US_OBS = 0.2243
_V_CB_OBS = 0.0422


# ---------------------------------------------------------------------------
# Exact rational generators of the two representations.
#
# Both are the SAME SO(3) rotation about a fixed axis, expressed in each rep;
# the leading Taylor coefficient of a transition amplitude between two orthonormal
# basis states |i>, |f> is exactly the matrix element <f|G|i> (since exp(theta G)
# = I + theta G + O(theta^2) and <f|i> = 0). Every entry is rational, so the
# coefficient is an exact Fraction.
# ---------------------------------------------------------------------------

# Spinor (SU(2) fundamental) generator = -i sigma_y / 2, which is REAL:
#   -i sigma_y / 2 = [[0, -1/2], [1/2, 0]].
# It is the su(2) element covering the so(3) generator below (the 1/2 = half-angle).
_SPINOR_GENERATOR: Tuple[Tuple[Fraction, ...], ...] = (
    (Fraction(0), Fraction(-1, 2)),
    (Fraction(1, 2), Fraction(0)),
)

# Vector (SO(3) adjoint) generator: a rotation in the x-y plane of Im(O).
_VECTOR_GENERATOR: Tuple[Tuple[Fraction, ...], ...] = (
    (Fraction(0), Fraction(-1), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(0)),
)


def _transition_coefficient(
    generator: Tuple[Tuple[Fraction, ...], ...], initial: int, final: int
) -> Fraction:
    """Leading coefficient of the |final> <- |initial> transition amplitude.

    For an antisymmetric generator ``G`` and orthonormal basis states this is the
    magnitude of the matrix element ``<final|G|initial>`` (exact over ``Q``).
    """
    element = generator[final][initial]
    return element if element >= 0 else -element


def spinor_transition_coefficient() -> Fraction:
    """The spin-1/2 (inter-generation) leading transition coefficient = ``1/2``."""
    return _transition_coefficient(_SPINOR_GENERATOR, 0, 1)


def vector_transition_coefficient() -> Fraction:
    """The vector (Im(O)) leading transition coefficient = ``1``."""
    return _transition_coefficient(_VECTOR_GENERATOR, 0, 1)


def double_cover_factor() -> Fraction:
    """Spinor / vector leading coefficient = ``1/2``: the ``SU(2) -> SO(3)`` half-angle.

    This is the source of the ``1/2`` in ``|V_cb| = (1/2) eps0``; it is a pure
    representation-theory ratio, not a weak-isospin input.
    """
    return spinor_transition_coefficient() / vector_transition_coefficient()


def vcb_coefficient() -> Fraction:
    """Exact coefficient of ``eps0`` in ``|V_cb|`` -- the spinor half-angle ``1/2``."""
    return spinor_transition_coefficient()


# ---------------------------------------------------------------------------
# Vector channel <-> Gate O28 consistency: |V_us|^2 = (sqrt 7)^2 = 7 = Cabibbo count.
# ---------------------------------------------------------------------------


def vector_channel_count() -> int:
    """Number of Im(O) directions summed coherently in the ``|V_us|`` vector channel.

    The vector amplitude ``1 * eps0`` per Fano direction, summed over the seven
    directions, gives ``|V_us| = sqrt(7) eps0``, so ``|V_us|^2 = 7`` -- exactly the
    Cabibbo count of Gate O28.
    """
    return 7


def matches_o28_cabibbo_count() -> bool:
    """The vector-channel count equals Gate O28's ``cabibbo_count()`` (both ``7``)."""
    return vector_channel_count() == cabibbo_count()


# ---------------------------------------------------------------------------
# The finite-angle avatar tan(pi/8) = sqrt(2) - 1, verified exactly in Q(sqrt 2).
#
# An element a + b sqrt(2) is represented by the pair (a, b) with a, b in Q.
# ---------------------------------------------------------------------------

_QSqrt2 = Tuple[Fraction, Fraction]


def _q2_mul(x: _QSqrt2, y: _QSqrt2) -> _QSqrt2:
    """(a + b sqrt2)(c + d sqrt2) = (ac + 2bd) + (ad + bc) sqrt2."""
    a, b = x
    c, d = y
    return (a * c + 2 * b * d, a * d + b * c)


def _q2_add(x: _QSqrt2, y: _QSqrt2) -> _QSqrt2:
    return (x[0] + y[0], x[1] + y[1])


def _q2_scale(x: _QSqrt2, s: Fraction) -> _QSqrt2:
    return (x[0] * s, x[1] * s)


def tan_pi8_satisfies_half_angle() -> bool:
    """``t = sqrt(2) - 1`` satisfies the double-angle identity ``2t/(1 - t^2) = 1``.

    Equivalently ``t^2 + 2t - 1 = 0``. Verified exactly in ``Q(sqrt 2)`` -- no
    floating point -- using ``sqrt(2) * sqrt(2) = 2``.
    """
    t: _QSqrt2 = (Fraction(-1), Fraction(1))  # sqrt(2) - 1
    t2 = _q2_mul(t, t)  # 3 - 2 sqrt2
    lhs = _q2_add(_q2_add(t2, _q2_scale(t, Fraction(2))), (Fraction(-1), Fraction(0)))
    return lhs == (Fraction(0), Fraction(0))


def tan_pi8_is_positive_root() -> bool:
    """``sqrt(2) - 1`` is the positive root of ``t^2 + 2t - 1`` (so it is ``tan(pi/8) > 0``)."""
    return math.sqrt(2.0) - 1.0 > 0.0


# ---------------------------------------------------------------------------
# Data confrontation (adopted scale eps0^2 = pi/432).
# ---------------------------------------------------------------------------


def predictions() -> List[Tuple[str, str, float, float, float]]:
    """Rows ``(name, formula, predicted, observed, signed_percent_deviation)``."""
    rows: List[Tuple[str, str, float, float, float]] = []

    v_us_pred = math.sqrt(float(vector_channel_count())) * _EPS0
    rows.append(
        (
            "|V_us| (vector)",
            "sqrt(7) * eps0",
            v_us_pred,
            _V_US_OBS,
            100.0 * (v_us_pred - _V_US_OBS) / _V_US_OBS,
        )
    )

    v_cb_pred = float(vcb_coefficient()) * _EPS0
    rows.append(
        (
            "|V_cb| (spinor)",
            "(1/2) * eps0",
            v_cb_pred,
            _V_CB_OBS,
            100.0 * (v_cb_pred - _V_CB_OBS) / _V_CB_OBS,
        )
    )
    return rows


def max_absolute_deviation() -> float:
    """Worst-case ``|percent deviation|`` across the two CKM amplitude predictions."""
    return max(abs(row[4]) for row in predictions())


def amplitudes_agree_with_data(tolerance: float = 0.03) -> bool:
    """Both CKM amplitude predictions agree with data within ``tolerance`` (fractional)."""
    return max_absolute_deviation() <= tolerance * 100.0


# ---------------------------------------------------------------------------
# Census.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CkmAmplitudeCensus:
    spinor_coefficient: Fraction
    vector_coefficient: Fraction
    double_cover_factor: Fraction
    vcb_coefficient: Fraction
    vector_channel_count: int
    matches_o28_cabibbo: bool
    tan_pi8_exact: bool
    max_deviation_percent: float
    amplitudes_agree: bool


def ckm_amplitude_census() -> CkmAmplitudeCensus:
    return CkmAmplitudeCensus(
        spinor_coefficient=spinor_transition_coefficient(),
        vector_coefficient=vector_transition_coefficient(),
        double_cover_factor=double_cover_factor(),
        vcb_coefficient=vcb_coefficient(),
        vector_channel_count=vector_channel_count(),
        matches_o28_cabibbo=matches_o28_cabibbo_count(),
        tan_pi8_exact=tan_pi8_satisfies_half_angle(),
        max_deviation_percent=max_absolute_deviation(),
        amplitudes_agree=amplitudes_agree_with_data(),
    )


if __name__ == "__main__":
    census = ckm_amplitude_census()
    print("Gate O30 -- CKM amplitudes: vector sqrt(7) vs spinor 1/2")
    print(f"  spinor coefficient        = {census.spinor_coefficient}")
    print(f"  vector coefficient        = {census.vector_coefficient}")
    print(f"  double-cover factor       = {census.double_cover_factor}")
    print(f"  |V_cb| coefficient        = {census.vcb_coefficient}")
    print(f"  vector-channel count      = {census.vector_channel_count} "
          f"(matches O28 Cabibbo: {census.matches_o28_cabibbo})")
    print(f"  tan(pi/8) = sqrt(2)-1     = {census.tan_pi8_exact} (exact in Q(sqrt2))")
    print()
    for name, formula, pred, obs, pct in predictions():
        print(f"  {name:<18}{formula:<18}pred {pred:.4f}  obs {obs:.4f}  {pct:+.1f}%")
    print(f"\n  max deviation = {census.max_deviation_percent:.2f}%  "
          f"(agree within 3%: {census.amplitudes_agree})")
