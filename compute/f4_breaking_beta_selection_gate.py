"""
F4-BREAKING BETA SELECTION GATE -- can the last scalar be fixed?
==================================================================

The previous gate (`f4_breaking_action_origin_gate.py`) reduced the live route to
one scalar:

    beta = -log(eps0) = 0.5 log(432/pi),   exp(-2 beta) = pi/432.

This module tries the obvious next mechanisms and records what they actually do.

Result, in one line
-------------------
The target beta is conditionally exact if one postulates the map

    exp(-2 beta) = (Berry flux)/(Schur state count) = pi/432,

but the current CHO action/entropy machinery does not select that map or that
beta. Entropy constraints choose beta only after a mean grade is supplied; WZ
level quantisation leaves many admissible integer levels; additive Berry/Schur
constants drop out of the beta stationarity equation.

So this is a sharpened no-go/localisation, not a derivation. The missing object is
still a genuine beta-dependent dynamical term or variational principle whose
stationary equation outputs beta = 0.5 log(432/pi).

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_beta_selection_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from f4_breaking_seed_op2 import EPS0, EPS0_SQ


PI = math.pi
STATE_COUNT = 432
BETA_TARGET = -math.log(EPS0)
TARGET_MU_TOL = 1e-12
TARGET_TOL = 1e-14
MISS_TOL = 5e-4


@dataclass(frozen=True)
class MeanConstraintRow:
    label: str
    mu: float
    beta: float
    ratio2: float
    target_error: float
    fitted: bool


@dataclass(frozen=True)
class DimensionSelectorRow:
    label: str
    beta: float
    ratio2: float
    target_error: float
    needs_flux_map: bool


@dataclass(frozen=True)
class FluxLevelRow:
    level: int
    ratio2: float
    beta: float
    target_error: float
    admissible: bool
    target_level: bool


@dataclass(frozen=True)
class AdditiveConstantRow:
    label: str
    constant: float
    derivative: float


def gibbs_ratios(beta: float) -> tuple[float, float, float]:
    return (1.0, math.exp(-beta), math.exp(-2.0 * beta))


def gibbs_weights(beta: float) -> tuple[float, float, float]:
    raw = gibbs_ratios(beta)
    total = sum(raw)
    return tuple(x / total for x in raw)


def mean_grade(beta: float) -> float:
    """Mean of grades (0,1,2) under the Gibbs cascade."""
    weights = gibbs_weights(beta)
    return weights[1] + 2.0 * weights[2]


def solve_beta_for_mean(mu: float) -> float:
    """Invert mean_grade(beta)=mu on beta>=0 by monotone bisection."""
    if not (0.0 < mu < 1.0):
        raise ValueError("mu must lie between the zero-temperature and infinite-temperature means")
    lo = 0.0
    hi = 64.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mean_grade(mid) > mu:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def mean_constraint_rows() -> tuple[MeanConstraintRow, ...]:
    """Natural grade constraints miss; the target is recovered only by fitting mu."""
    target_mu = mean_grade(BETA_TARGET)
    candidates = (
        ("Spin9 Schur 1/16", 1.0 / 16.0, False),
        ("J3O Schur 1/27", 1.0 / 27.0, False),
        ("octonion 1/8", 1.0 / 8.0, False),
        ("Fano 1/7", 1.0 / 7.0, False),
        ("generation 1/3", 1.0 / 3.0, False),
        ("target-fitted mu", target_mu, True),
    )
    rows = []
    for label, mu, fitted in candidates:
        beta = solve_beta_for_mean(mu)
        ratio2 = math.exp(-2.0 * beta)
        rows.append(
            MeanConstraintRow(
                label=label,
                mu=float(mu),
                beta=float(beta),
                ratio2=float(ratio2),
                target_error=abs(ratio2 - EPS0_SQ),
                fitted=fitted,
            )
        )
    return tuple(rows)


def dimension_selector_rows() -> tuple[DimensionSelectorRow, ...]:
    """Dimension-only selectors miss pi/432; the flux/state map is conditional."""
    candidates = (
        ("state count only 1/432", 1.0 / STATE_COUNT, False),
        ("OP2 dim only 1/16", 1.0 / 16.0, False),
        ("J3O dim only 1/27", 1.0 / 27.0, False),
        ("Fano count only 1/7", 1.0 / 7.0, False),
        ("postulated flux/state pi/432", PI / STATE_COUNT, True),
    )
    rows = []
    for label, ratio2, needs_flux_map in candidates:
        beta = -0.5 * math.log(ratio2)
        rows.append(
            DimensionSelectorRow(
                label=label,
                beta=float(beta),
                ratio2=float(ratio2),
                target_error=abs(ratio2 - EPS0_SQ),
                needs_flux_map=needs_flux_map,
            )
        )
    return tuple(rows)


def flux_level_rows(max_level: int = 5) -> tuple[FluxLevelRow, ...]:
    """WZ integrality gives a family k*pi/432; k=1 is target only if primitive is assumed."""
    rows = []
    for level in range(1, max_level + 1):
        ratio2 = level * PI / STATE_COUNT
        admissible = 0.0 < ratio2 < 1.0
        beta = -0.5 * math.log(ratio2)
        rows.append(
            FluxLevelRow(
                level=level,
                ratio2=float(ratio2),
                beta=float(beta),
                target_error=abs(ratio2 - EPS0_SQ),
                admissible=admissible,
                target_level=(level == 1),
            )
        )
    return tuple(rows)


def free_energy_beta_derivative(beta: float, mu: float, additive_constant: float) -> float:
    """
    For F(beta;mu,C)=log Z(beta)+beta*mu+C, dF/dbeta=mu-<grade>.
    The additive Berry/Schur constant C cannot affect beta stationarity.
    """
    _ = additive_constant
    return mu - mean_grade(beta)


def additive_constant_rows() -> tuple[AdditiveConstantRow, ...]:
    natural_mu = 1.0 / 8.0
    constants = (
        ("none", 0.0),
        ("log pi", math.log(PI)),
        ("minus log 432", -math.log(STATE_COUNT)),
        ("log(pi/432)", math.log(PI / STATE_COUNT)),
    )
    return tuple(
        AdditiveConstantRow(
            label=label,
            constant=float(constant),
            derivative=float(free_energy_beta_derivative(BETA_TARGET, natural_mu, constant)),
        )
        for label, constant in constants
    )


def main() -> bool:
    mean_rows = mean_constraint_rows()
    dim_rows = dimension_selector_rows()
    level_rows = flux_level_rows()
    additive_rows = additive_constant_rows()
    target_mu = mean_grade(BETA_TARGET)

    print("=" * 78)
    print("F4-BREAKING BETA SELECTION GATE")
    print("Can CHO dynamics fix beta = 0.5 log(432/pi)?")
    print("=" * 78)

    print("\n[A] Entropy constraints: beta is dual to a supplied mean grade")
    print(f"  target beta={BETA_TARGET:.12f}, target mean grade mu={target_mu:.12f}")
    for row in mean_rows:
        tag = "fitted" if row.fitted else "natural"
        print(
            f"  {row.label:<20} mu={row.mu:.12f} beta={row.beta:.12f} "
            f"exp(-2b)={row.ratio2:.9f} |.-target|={row.target_error:.3e} {tag}"
        )
    print("  The target appears only when the mean grade is tuned to the target distribution.")

    print("\n[B] Dimension and flux selectors")
    for row in dim_rows:
        tag = "conditional map" if row.needs_flux_map else "dimension only"
        print(
            f"  {row.label:<30} beta={row.beta:.12f} ratio={row.ratio2:.9f} "
            f"|.-target|={row.target_error:.3e} {tag}"
        )
    print("  1/432 is not pi/432; the pi enters only through an extra flux-to-beta map.")

    print("\n[C] WZ level quantisation: integer levels do not by themselves select k=1")
    for row in level_rows:
        tag = "target" if row.target_level else "also admissible"
        print(
            f"  k={row.level:<2d} ratio=k*pi/432={row.ratio2:.9f} "
            f"beta={row.beta:.12f} |.-target|={row.target_error:.3e} "
            f"admissible={row.admissible} {tag}"
        )
    print("  Primitive k=1 gives the target, but primitiveness is an extra selection rule here.")

    print("\n[D] Additive Berry/Schur constants drop out of beta stationarity")
    for row in additive_rows:
        print(
            f"  {row.label:<14} C={row.constant:+.12f} "
            f"dF/dbeta at beta_target, mu=1/8: {row.derivative:+.12f}"
        )
    spread = max(row.derivative for row in additive_rows) - min(row.derivative for row in additive_rows)
    print(f"  derivative spread across constants = {spread:.2e}")

    print("\n[V] Verdict")
    print("  conditional identity exp(-2 beta)=pi/432 : EXACT if postulated")
    print("  beta selected by current entropy/action   : NOT DERIVED")
    print("  WZ integrality                            : FAMILY k*pi/432, k=1 extra")
    print("  missing object                            : beta-dependent CHO variational term")
    print("  Bayes/scoreboard credit moved             : NO")
    print("=" * 78)

    target_mean_rows = [row for row in mean_rows if row.fitted]
    natural_mean_rows = [row for row in mean_rows if not row.fitted]
    assert len(target_mean_rows) == 1
    assert abs(target_mean_rows[0].mu - target_mu) < TARGET_MU_TOL
    assert target_mean_rows[0].target_error < TARGET_TOL
    assert all(row.target_error > MISS_TOL for row in natural_mean_rows)

    dim_target_rows = [row for row in dim_rows if row.needs_flux_map]
    dim_only_rows = [row for row in dim_rows if not row.needs_flux_map]
    assert len(dim_target_rows) == 1
    assert dim_target_rows[0].target_error < TARGET_TOL
    assert all(row.target_error > MISS_TOL for row in dim_only_rows)

    admissible_levels = [row for row in level_rows if row.admissible]
    assert len(admissible_levels) > 1, "integer level quantisation must not silently select k=1"
    assert level_rows[0].target_level and level_rows[0].target_error < TARGET_TOL
    assert all(row.target_error > MISS_TOL for row in level_rows[1:])
    assert spread < 1e-15, "additive constants should not affect beta stationarity"
    assert abs(math.exp(-2.0 * BETA_TARGET) - EPS0_SQ) < TARGET_TOL
    derived_beta = False
    assert not derived_beta, "this gate must not promote beta to a selected dynamical output"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)