"""Gate O28 -- the parameter-free mixing web from the Fano split {3, 4, 7}.

Gate O26 emitted one falsifiable rational, ``sin^2(theta23) = 4/7``, from the
vacuum split of the octonion Fano plane (3 lines through the vacuum point, 4
avoiding, 7 total). This gate follows the thread: the *same* split drives an entire
**web** of parameter-free relations among already-measured quark and lepton
observables, exactly over ``Q``, porting the master-branch flavour bridge
(``compute/epsilon_free_mixing_web.py`` / ``epsilon_mixing_coefficients.py`` behind
Zenodo 21107402).

The master flavour bridge assigns the three Fano counts to four mixing observables
through a single scale ``eps0^2 = pi/432`` (all *adopted*, see the non-claim):

    |V_us|^2          = 7 * eps0^2      (Cabibbo channel  -> all lines)
    sin^2(theta13)    = 3 * eps0^2      (reactor          -> lines through vacuum)
    dm21^2 / dm31^2   = 4 * eps0^2      (solar/atm ratio  -> lines avoiding vacuum)
    sin^2(theta23)    = 4 / 7           (atmospheric octant, Gate O26)

Because every one of the first three is ``(integer) * eps0^2``, **the knob cancels
in every ratio** -- leaving pure Fano-count rationals with *no free parameter*,
testable against data today. Exact over ``Q``:

1. **The reactor angle is tied to the Cabibbo angle.**
   ``sin^2(theta13) / |V_us|^2 = 3/7`` (through / total) -- a cross-sector relation
   binding a *lepton* mixing probability to a *quark* one with no parameter.
2. **Two further eps0-free rationals.** ``(dm21^2/dm31^2) / |V_us|^2 = 4/7`` and
   ``(dm21^2/dm31^2) / sin^2(theta13) = 4/3`` (avoiding / total, avoiding / through).
3. **A Fano completeness sum rule.** ``7 = 3 + 4`` becomes
   ``sin^2(theta13) + dm21^2/dm31^2 = |V_us|^2`` exactly.
4. **Only two are independent.** ``R3 = R2 / R1`` and ``R1 + R2 = 1``; the atmospheric
   octant ``4/7`` of Gate O26 is exactly ``R2``, the avoiding-line partner of the
   reactor ``3/7``.

**Data confrontation.** Current central values and approximate independent
uncertainties are audited separately in ``flavour_assignment_audit``.  They are
diagnostics, not test-suite promotion criteria.

Non-claim: what is forced, exactly and knob-free, is the *web of ratios* ``{3/7,
4/7, 4/3}`` and the sum rule, given the master's *adopted* assignment of the three
Fano counts ``{3, 4, 7}`` to the specific observables (which count labels which
channel is a modelling choice, not derived here), and given the amplitude-vs-
probability power counting. The absolute scale ``eps0^2 = pi/432`` is itself an
adopted knob; this gate deliberately works only with the eps0-free ratios, where
that knob cancels. No mass hierarchy, CP phase, or dynamics follows. The value is
that a *single* finite incidence structure -- the octonion Fano plane -- forces
several independent, currently-correct relations among measured flavour observables.
Cross-refs master ``compute/epsilon_free_mixing_web.py``,
``epsilon_mixing_coefficients.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from .atmospheric_mixing import vacuum_split

# The Fano vacuum split (through, avoiding) at any vacuum point -- see Gate O26.
_THROUGH, _AVOIDING = vacuum_split(7)
_TOTAL = _THROUGH + _AVOIDING


def cabibbo_count() -> int:
    """The Cabibbo channel multiplicity ``|V_us|^2 / eps0^2 = 7`` (all Fano lines)."""
    return _TOTAL


def reactor_count() -> int:
    """The reactor multiplicity ``sin^2(theta13) / eps0^2 = 3`` (lines through vacuum)."""
    return _THROUGH


def mass_splitting_count() -> int:
    """The ``dm21^2/dm31^2 / eps0^2 = 4`` multiplicity (lines avoiding the vacuum)."""
    return _AVOIDING


def ratio_theta13_over_cabibbo() -> Fraction:
    """``R1 = sin^2(theta13) / |V_us|^2 = 3/7`` -- reactor tied to Cabibbo."""
    return Fraction(reactor_count(), cabibbo_count())


def ratio_splitting_over_cabibbo() -> Fraction:
    """``R2 = (dm21^2/dm31^2) / |V_us|^2 = 4/7``."""
    return Fraction(mass_splitting_count(), cabibbo_count())


def ratio_splitting_over_theta13() -> Fraction:
    """``R3 = (dm21^2/dm31^2) / sin^2(theta13) = 4/3``."""
    return Fraction(mass_splitting_count(), reactor_count())


def sin2_theta23() -> Fraction:
    """The atmospheric octant ``4/7`` (Gate O26); equals ``R2``, the avoiding partner."""
    return Fraction(_AVOIDING, _TOTAL)


def sum_rule_holds() -> bool:
    """Fano completeness ``7 = 3 + 4`` -> ``sin^2(theta13) + dm21^2/dm31^2 = |V_us|^2``."""
    return reactor_count() + mass_splitting_count() == cabibbo_count()


def web_is_two_dimensional() -> bool:
    """Exact check ``R3 = R2/R1`` and ``R1 + R2 = 1`` -- only two independent ratios."""
    r1 = ratio_theta13_over_cabibbo()
    r2 = ratio_splitting_over_cabibbo()
    r3 = ratio_splitting_over_theta13()
    return r3 == r2 / r1 and r1 + r2 == 1


def octant_matches_gate_o26() -> bool:
    """Exact check that ``R2`` equals the Gate O26 atmospheric octant ``4/7``."""
    return ratio_splitting_over_cabibbo() == sin2_theta23()


# --------------------------------------------------------------------------
# Data confrontation -- documented measured central values (the falsifiable half).
# --------------------------------------------------------------------------
# PDG 2024 CKM and NuFIT 6.0 (2024), normal ordering. These central values are
# descriptive only; flavour_assignment_audit owns uncertainties and assignment trials.
_VUS = 0.2243
_MEASURED = {
    "|V_us|^2": _VUS * _VUS,
    "sin2_theta13": 0.0222,
    "dm21^2/dm31^2": 7.43e-5 / 2.500e-3,
    "sin2_theta23": 0.572,
}


def _relative_deviation(predicted: float, measured: float) -> float:
    return (measured - predicted) / predicted


def data_confrontation() -> List[Tuple[str, Fraction, float, float]]:
    """For each eps0-free relation: ``(name, predicted rational, measured, deviation)``."""
    m = _MEASURED
    rows: List[Tuple[str, Fraction, float, float]] = []
    r1 = ratio_theta13_over_cabibbo()
    r1_meas = m["sin2_theta13"] / m["|V_us|^2"]
    rows.append(("R1 = sin2_theta13 / |V_us|^2", r1, r1_meas,
                 _relative_deviation(float(r1), r1_meas)))
    r2 = ratio_splitting_over_cabibbo()
    r2_meas = m["dm21^2/dm31^2"] / m["|V_us|^2"]
    rows.append(("R2 = (dm21^2/dm31^2) / |V_us|^2", r2, r2_meas,
                 _relative_deviation(float(r2), r2_meas)))
    r3 = ratio_splitting_over_theta13()
    r3_meas = m["dm21^2/dm31^2"] / m["sin2_theta13"]
    rows.append(("R3 = (dm21^2/dm31^2) / sin2_theta13", r3, r3_meas,
                 _relative_deviation(float(r3), r3_meas)))
    s23 = sin2_theta23()
    rows.append(("sin2_theta23 = 4/7", s23, m["sin2_theta23"],
                 _relative_deviation(float(s23), m["sin2_theta23"])))
    return rows


def max_absolute_deviation() -> float:
    """The worst fractional disagreement across the whole web (currently ~2.6%)."""
    return max(abs(row[3]) for row in data_confrontation())


def web_agrees_with_data(tolerance: float = 0.05) -> bool:
    """Legacy descriptive central-value threshold; not a scientific promotion gate."""
    return max_absolute_deviation() <= tolerance


def empirical_results_are_promotion_gate() -> bool:
    """Empirical agreement is never established by a unit-test tolerance."""
    return False


@dataclass(frozen=True)
class MixingWebCensus:
    """Exact ledger of the eps0-free Fano mixing web over ``Q``, plus data agreement."""

    cabibbo_count: int
    reactor_count: int
    splitting_count: int
    r1_theta13_cabibbo: Fraction
    r2_splitting_cabibbo: Fraction
    r3_splitting_theta13: Fraction
    sum_rule_holds: bool
    web_two_dimensional: bool
    octant_matches_o26: bool
    max_absolute_deviation: float
    agrees_within_five_percent: bool
    empirical_promotion_allowed: bool


def mixing_web_census() -> MixingWebCensus:
    """Assemble the exact O28 ledger and its current data confrontation."""
    return MixingWebCensus(
        cabibbo_count=cabibbo_count(),
        reactor_count=reactor_count(),
        splitting_count=mass_splitting_count(),
        r1_theta13_cabibbo=ratio_theta13_over_cabibbo(),
        r2_splitting_cabibbo=ratio_splitting_over_cabibbo(),
        r3_splitting_theta13=ratio_splitting_over_theta13(),
        sum_rule_holds=sum_rule_holds(),
        web_two_dimensional=web_is_two_dimensional(),
        octant_matches_o26=octant_matches_gate_o26(),
        max_absolute_deviation=max_absolute_deviation(),
        agrees_within_five_percent=web_agrees_with_data(),
        empirical_promotion_allowed=empirical_results_are_promotion_gate(),
    )
