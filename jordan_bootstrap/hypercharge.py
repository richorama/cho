"""Gate O14 -- anomaly cancellation forces the Standard Model hypercharges.

This is the campaign's first attempt at a *number*, not a group. Gates O10-O13
recovered the Standard Model's gauge algebra and one generation's colour/isospin
representations from the division algebras. But representations are structure; the
hypercharges ``Y`` -- the ugly rationals ``1/6, -2/3, 1/3, -1/2, 1`` -- look
arbitrary. This gate shows, exactly over the rationals, that they are *forced*:
quantum consistency (anomaly cancellation) plus one charge normalisation leaves
no freedom at all. Charge quantisation is derived, and the weak mixing angle
``sin^2(theta_W) = 3/8`` drops out as an exact structural ratio.

A chiral gauge theory is only consistent if its gauge and mixed
gauge-gravitational anomalies cancel. For one generation of left-handed Weyl
fermions in the representations fixed by O10-O13 --

    Q = (3, 2, Y_Q),  u^c = (3bar, 1, Y_u),  d^c = (3bar, 1, Y_d),
    L = (1, 2, Y_L),  e^c = (1, 1, Y_e),

with electric charge ``Q = T_3 + Y`` -- the six anomaly conditions are computed
here *from the representation content itself* (not hard-coded) and every one
vanishes exactly for the Standard Model assignment:

* ``[SU(3)]^3``   (pure colour),
* ``[SU(3)]^2 U(1)``,
* ``[SU(2)]^2 U(1)``,
* ``[U(1)]^3``,
* ``[grav]^2 U(1)`` (the ``sum Y`` condition),
* Witten's global ``SU(2)`` (an even number of doublets).

The forcing is the point. Solving the three linear conditions leaves a
two-parameter family; fixing the overall ``U(1)`` scale by the single electric
charge that Gate O11 already derived (the up-type quark carries ``Q = 2/3``, so
``Y_Q = 1/6``) reduces the cubic ``[U(1)]^3`` condition to the quadratic

    -3 Y^2 - Y + 2/3 = -(1/3)(3Y - 1)(3Y + 2),

whose only roots are ``Y = 1/3`` and ``Y = -2/3`` -- exactly the down-type and
up-type hypercharges, the two roots being the physically irrelevant relabelling
``u <-> d``. So the entire hypercharge spectrum is pinned to the Standard Model,
up to that relabelling: **charge quantisation is a theorem, not an input.**

Finally the weak mixing angle in the grand-unified normalisation,

    sin^2(theta_W) = (sum T_3^2) / (sum Q^2) = 2 / (16/3) = 3/8,

an exact rational summed over the whole generation -- the value SU(5)/SO(10)
grand unification predicts at the unification scale.

Non-claim: this derives the *ratios* of the hypercharges from anomaly freedom and
one charge normalisation; it does not derive the electroweak scale, the running of
``sin^2(theta_W)`` down to laboratory energies (``~0.231``), or why nature is
anomaly-free. The ``3/8`` is the tree-level GUT value, not the measured
low-energy one.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

Rational = Fraction


@dataclass(frozen=True)
class WeylField:
    """A left-handed Weyl multiplet: colour dim, the SU(2) T_3 values, and Y."""

    name: str
    colour_dim: int          # 3 for triplet/antitriplet, 1 for colour singlet
    colour_anomaly: int      # +1 for 3, -1 for 3bar, 0 for singlet
    t3_values: Tuple[Rational, ...]  # the SU(2) isospin components
    hypercharge: Rational

    def electric_charges(self) -> Tuple[Rational, ...]:
        return tuple(t3 + self.hypercharge for t3 in self.t3_values)

    def weyl_count(self) -> int:
        return self.colour_dim * len(self.t3_values)


def standard_model_generation(
    y_q: Rational = Fraction(1, 6),
    y_u: Rational = Fraction(-2, 3),
    y_d: Rational = Fraction(1, 3),
    y_l: Rational = Fraction(-1, 2),
    y_e: Rational = Fraction(1),
) -> Tuple[WeylField, ...]:
    """One generation of left-handed Weyl fields in the reps fixed by O10-O13."""
    half = Fraction(1, 2)
    return (
        WeylField("Q", 3, +1, (half, -half), y_q),
        WeylField("u^c", 3, -1, (Fraction(0),), y_u),
        WeylField("d^c", 3, -1, (Fraction(0),), y_d),
        WeylField("L", 1, 0, (half, -half), y_l),
        WeylField("e^c", 1, 0, (Fraction(0),), y_e),
    )


# -- anomaly coefficients computed from the representation content ------------


def grav_u1_anomaly(fields: Tuple[WeylField, ...]) -> Rational:
    """Mixed gravitational-U(1): sum of Y over every Weyl fermion."""
    return sum(
        (f.colour_dim * len(f.t3_values) * f.hypercharge for f in fields),
        Fraction(0),
    )


def su3_sq_u1_anomaly(fields: Tuple[WeylField, ...]) -> Rational:
    """[SU(3)]^2 U(1): sum of Y over colour-triplet fermions (Dynkin factor common)."""
    return sum(
        (len(f.t3_values) * f.hypercharge for f in fields if f.colour_dim == 3),
        Fraction(0),
    )


def su2_sq_u1_anomaly(fields: Tuple[WeylField, ...]) -> Rational:
    """[SU(2)]^2 U(1): sum of Y over SU(2)-doublet fermions, weighted by colour."""
    return sum(
        (f.colour_dim * f.hypercharge for f in fields if len(f.t3_values) == 2),
        Fraction(0),
    )


def u1_cubed_anomaly(fields: Tuple[WeylField, ...]) -> Rational:
    """[U(1)]^3: sum of Y^3 over every Weyl fermion."""
    return sum(
        (f.colour_dim * len(f.t3_values) * f.hypercharge ** 3 for f in fields),
        Fraction(0),
    )


def su3_cubed_anomaly(fields: Tuple[WeylField, ...]) -> int:
    """[SU(3)]^3: sum of the colour anomaly (+1 for 3, -1 for 3bar) times SU(2) mult."""
    return sum(f.colour_anomaly * len(f.t3_values) for f in fields)


def witten_doublet_count(fields: Tuple[WeylField, ...]) -> int:
    """Number of SU(2) doublets; must be even for Witten global anomaly freedom."""
    return sum(f.colour_dim for f in fields if len(f.t3_values) == 2)


def weinberg_sin2(fields: Tuple[WeylField, ...]) -> Rational:
    """GUT-normalised weak mixing angle: (sum T_3^2) / (sum Q^2) over the generation."""
    sum_t3_sq = Fraction(0)
    sum_q_sq = Fraction(0)
    for f in fields:
        for t3, q in zip(f.t3_values, f.electric_charges()):
            sum_t3_sq += f.colour_dim * t3 * t3
            sum_q_sq += f.colour_dim * q * q
    return sum_t3_sq / sum_q_sq


# -- the forcing theorem -----------------------------------------------------


def anchored_family(y_dc: Rational) -> Tuple[WeylField, ...]:
    """The unique anomaly-linear generation with the O11 charge anchor Y_Q = 1/6.

    Solving the three linear anomaly conditions and fixing the U(1) scale by
    ``Y_Q = 1/6`` (up-type quark charge ``2/3``, from Gate O11) leaves a single
    free parameter ``Y_dc``. The remaining cubic condition then constrains it.
    """
    y_q = Fraction(1, 6)
    y_l = Fraction(-1, 2)
    y_e = Fraction(1)
    y_u = -y_dc - Fraction(1, 3)
    return standard_model_generation(y_q, y_u, y_dc, y_l, y_e)


def anchored_u1_cubed(y_dc: Rational) -> Rational:
    """The [U(1)]^3 anomaly along the anchored family, as a function of Y_dc."""
    return u1_cubed_anomaly(anchored_family(y_dc))


@dataclass(frozen=True)
class HyperchargeCensus:
    """Exact certificate that anomaly freedom forces the SM hypercharges."""

    all_six_anomalies_vanish: bool
    anomaly_values: Dict[str, Rational]
    cubic_collapses_to_quadratic: bool
    forcing_roots: Tuple[Rational, ...]
    roots_are_sm_up_to_relabelling: bool
    hypercharges_are_forced: bool
    weinberg_sin2: Rational


def _quadratic_form(y: Rational) -> Rational:
    return -Fraction(3) * y * y - y + Fraction(2, 3)


def hypercharge_census() -> HyperchargeCensus:
    sm = standard_model_generation()
    values = {
        "SU(3)^3": Fraction(su3_cubed_anomaly(sm)),
        "SU(3)^2 U(1)": su3_sq_u1_anomaly(sm),
        "SU(2)^2 U(1)": su2_sq_u1_anomaly(sm),
        "U(1)^3": u1_cubed_anomaly(sm),
        "grav^2 U(1)": grav_u1_anomaly(sm),
    }
    all_vanish = all(v == 0 for v in values.values()) and \
        witten_doublet_count(sm) % 2 == 0

    # Along the anchored family the cubic U(1)^3 anomaly is exactly the quadratic
    # -(1/3)(3Y-1)(3Y+2); verify as an identity on several exact points.
    test_points = [Fraction(n, d) for n in range(-6, 7) for d in (1, 2, 3)]
    collapses = all(
        anchored_u1_cubed(y) == _quadratic_form(y) for y in test_points
    )

    roots = tuple(y for y in (Fraction(1, 3), Fraction(-2, 3))
                  if anchored_u1_cubed(y) == 0)
    # both roots reproduce the SM assignment (up to u <-> d relabelling)
    sm_set = {f.hypercharge for f in sm}
    roots_are_sm = all(
        {f.hypercharge for f in anchored_family(r)} == sm_set for r in roots
    )
    forced = collapses and set(roots) == {Fraction(1, 3), Fraction(-2, 3)} \
        and roots_are_sm

    return HyperchargeCensus(
        all_six_anomalies_vanish=all_vanish,
        anomaly_values=values,
        cubic_collapses_to_quadratic=collapses,
        forcing_roots=roots,
        roots_are_sm_up_to_relabelling=roots_are_sm,
        hypercharges_are_forced=forced,
        weinberg_sin2=weinberg_sin2(sm),
    )
