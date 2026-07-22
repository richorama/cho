"""Gate O33 -- statistical and scale audit of the adopted flavour assignment.

This module does not promote or reject the model from a tolerance.  It records
the six possible assignments of the Fano counts ``{3, 4, 7}``, profiles one
common scale for each, and reports the fixed ``pi/432`` residuals.  Experimental
inputs are kept separate from exact algebraic claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import permutations
from typing import Tuple


@dataclass(frozen=True)
class Measurement:
    name: str
    value: float
    sigma: float
    source: str


@dataclass(frozen=True)
class AssignmentFit:
    counts: Tuple[int, int, int]
    fitted_scale: float
    chi_square: float


def measurements() -> Tuple[Measurement, ...]:
    """Current independent-input approximation used for the assignment audit.

    Correlations and asymmetric errors are not available in this lightweight
    gate, so its chi-square is diagnostic rather than publication-grade.
    """
    vus = 0.2243
    vus_sigma = 0.0005
    dm21, dm21_sigma = 7.43e-5, 0.05e-5
    dm3l, dm3l_sigma = 2.500e-3, 0.030e-3
    ratio = dm21 / dm3l
    ratio_sigma = ratio * math.sqrt(
        (dm21_sigma / dm21) ** 2 + (dm3l_sigma / dm3l) ** 2
    )
    return (
        Measurement("|V_us|^2", vus * vus, 2.0 * vus * vus_sigma, "PDG 2024"),
        Measurement("sin^2(theta13)", 0.0222, 0.0006, "NuFIT 6.0 (NO)"),
        Measurement("dm21^2/dm3l^2", ratio, ratio_sigma, "NuFIT 6.0 (NO)"),
    )


def fit_assignment(counts: Tuple[int, int, int]) -> AssignmentFit:
    data = measurements()
    weights = tuple(1.0 / item.sigma**2 for item in data)
    scale = sum(
        weight * count * item.value
        for weight, count, item in zip(weights, counts, data)
    ) / sum(weight * count * count for weight, count in zip(weights, counts))
    chi_square = sum(
        ((item.value - count * scale) / item.sigma) ** 2
        for item, count in zip(data, counts)
    )
    return AssignmentFit(counts, scale, chi_square)


def assignment_fits() -> Tuple[AssignmentFit, ...]:
    return tuple(
        sorted(
            (fit_assignment(tuple(counts)) for counts in permutations((3, 4, 7))),
            key=lambda fit: fit.chi_square,
        )
    )


def adopted_assignment() -> Tuple[int, int, int]:
    """Counts for ``(|V_us|^2, sin^2 theta13, dm ratio)``."""
    return (7, 3, 4)


def adopted_assignment_rank() -> int:
    fits = assignment_fits()
    return next(i for i, fit in enumerate(fits, 1) if fit.counts == adopted_assignment())


def profiled_p_value() -> float:
    """Approximate upper-tail probability for chi-square with two degrees of freedom."""
    chi_square = fit_assignment(adopted_assignment()).chi_square
    return math.exp(-chi_square / 2.0)


def look_elsewhere_p_value() -> float:
    """Conservative Bonferroni correction for inspecting all six assignments."""
    return min(1.0, 6.0 * profiled_p_value())


def fixed_scale_chi_square() -> float:
    scale = math.pi / 432.0
    return sum(
        ((item.value - count * scale) / item.sigma) ** 2
        for item, count in zip(measurements(), adopted_assignment())
    )


def mixed_scale_mass_inputs() -> Tuple[Tuple[str, str, bool], ...]:
    """Mass pairs used by O29 and whether both entries share one declared scale."""
    return (
        ("m_c(m_c)", "m_t(m_t)", False),
        ("m_s(2 GeV)", "m_b(m_b)", False),
        ("m_mu", "m_tau", True),
    )


def empirical_results_are_promotion_gate() -> bool:
    """Data comparisons must remain diagnostics until covariance and RG are supplied."""
    return False
