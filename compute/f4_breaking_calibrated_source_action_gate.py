"""
F4-BREAKING CALIBRATED SOURCE-ACTION GATE -- is KL a fragile choice?
=============================================================================

The source-stationarity gate showed that a Bernoulli/KL source coupling selects

    q(beta) = exp(-2 beta) = d = pi/432,

and therefore beta=-log(eps0). This gate tests the next question: did that result
depend on the special logarithmic action, or only on the weaker source-calibration
principle that the action has a strict local minimum when the model probability
matches the source probability?

We test several local calibrated divergences:

    KL / log score,
    Brier / quadratic score,
    Hellinger distance,
    logit-coordinate quadratic divergence.

For each, the beta stationarity equation factors through dF/dq=0, so the same
projective channel q(beta)=exp(-2 beta) gives the same stationary beta. Improper
controls show why calibration matters: a linear probability reward and an
amplitude-calibrated square loss do not make the target beta stationary.

What this proves
----------------
The beta result is robust to the detailed choice of calibrated local source
functional. KL is not the unique possible action that selects beta; the narrower
condition is source calibration on the projective probability channel.

What this still does not prove
------------------------------
This still does not derive the CHO/F4-breaking action term, nor does it derive
why CHO dynamics must choose a calibrated source functional. The live bridge is
now the origin of source calibration itself.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_calibrated_source_action_gate.py
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import math

from f4_breaking_born_beta_map_gate import born_selection, gibbs_ratios
from f4_breaking_primitive_level_gate import CARRIER_DIM, half_turn_density
from f4_breaking_seed_op2 import EPS0, EPS0_SQ
from f4_breaking_source_stationarity_gate import beta_for_source, model_probability


TOL = 1e-12
MATCH_TOL = 1e-14
MISS_TOL = 1e-3
BETA_DELTA = 5e-2


@dataclass(frozen=True)
class SourceFunctional:
    label: str
    value: Callable[[float, float], float]
    q_gradient: Callable[[float, float], float]
    q_curvature: Callable[[float, float], float]
    interpretation: str


@dataclass(frozen=True)
class CalibratedActionRow:
    label: str
    value_at_stationary: float
    beta_derivative: float
    beta_curvature: float
    left_derivative: float
    right_derivative: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    target_error: float
    matches_target: bool
    interpretation: str


@dataclass(frozen=True)
class SourceControlRow:
    label: str
    source_density: float
    model_power: int
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    target_error: float
    matches_target: bool
    interpretation: str


@dataclass(frozen=True)
class ImproperActionRow:
    label: str
    derivative_at_target_beta: float
    curvature_at_target_beta: float
    target_is_stationary_minimum: bool
    interpretation: str


@dataclass(frozen=True)
class CalibratedSourceSelection:
    source_density: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    stationary_ratios: tuple[float, float, float]
    all_calibrated_actions_select_same_beta: bool
    kl_action_unique: bool
    source_calibration_derived: bool
    cho_action_coupling_derived: bool


def _check_probability(source_density: float, probability: float) -> None:
    if not (0.0 < source_density < 1.0 and 0.0 < probability < 1.0):
        raise ValueError("source and probability must lie in (0, 1)")


def _logit(x: float) -> float:
    if not 0.0 < x < 1.0:
        raise ValueError("logit input must lie in (0, 1)")
    return math.log(x / (1.0 - x))


def _kl_value(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (
        source_density * math.log(source_density / probability)
        + (1.0 - source_density) * math.log((1.0 - source_density) / (1.0 - probability))
    )


def _kl_q_gradient(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (probability - source_density) / (probability * (1.0 - probability))


def _kl_q_curvature(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return source_density / (probability * probability) + (1.0 - source_density) / ((1.0 - probability) ** 2)


def _brier_value(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (probability - source_density) ** 2


def _brier_q_gradient(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return 2.0 * (probability - source_density)


def _brier_q_curvature(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return 2.0


def _hellinger_value(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (
        (math.sqrt(source_density) - math.sqrt(probability)) ** 2
        + (math.sqrt(1.0 - source_density) - math.sqrt(1.0 - probability)) ** 2
    )


def _hellinger_q_gradient(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return -math.sqrt(source_density / probability) + math.sqrt((1.0 - source_density) / (1.0 - probability))


def _hellinger_q_curvature(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (
        0.5 * math.sqrt(source_density) / (probability ** 1.5)
        + 0.5 * math.sqrt(1.0 - source_density) / ((1.0 - probability) ** 1.5)
    )


def _logit_quadratic_value(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (_logit(probability) - _logit(source_density)) ** 2


def _logit_quadratic_q_gradient(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return 2.0 * (_logit(probability) - _logit(source_density)) / (probability * (1.0 - probability))


def _logit_quadratic_q_curvature(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    logit_gap = _logit(probability) - _logit(source_density)
    first = 2.0 / ((probability * (1.0 - probability)) ** 2)
    second = -2.0 * logit_gap * (1.0 - 2.0 * probability) / ((probability * (1.0 - probability)) ** 2)
    return first + second


def _linear_reward_value(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return -probability


def _linear_reward_q_gradient(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return -1.0


def _linear_reward_q_curvature(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return 0.0


def _amplitude_square_value(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (math.sqrt(probability) - source_density) ** 2


def _amplitude_square_q_gradient(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return (math.sqrt(probability) - source_density) / math.sqrt(probability)


def _amplitude_square_q_curvature(source_density: float, probability: float) -> float:
    _check_probability(source_density, probability)
    return source_density / (2.0 * probability ** 1.5)


def calibrated_source_functionals() -> tuple[SourceFunctional, ...]:
    return (
        SourceFunctional(
            "KL / logarithmic source",
            _kl_value,
            _kl_q_gradient,
            _kl_q_curvature,
            "proper log score; the previous source-stationarity gate used this action",
        ),
        SourceFunctional(
            "Brier / quadratic source",
            _brier_value,
            _brier_q_gradient,
            _brier_q_curvature,
            "proper quadratic score; no logarithm is used",
        ),
        SourceFunctional(
            "Hellinger source",
            _hellinger_value,
            _hellinger_q_gradient,
            _hellinger_q_curvature,
            "geometric probability-distance source on the Bernoulli simplex",
        ),
        SourceFunctional(
            "logit-quadratic source",
            _logit_quadratic_value,
            _logit_quadratic_q_gradient,
            _logit_quadratic_q_curvature,
            "coordinate-quadratic calibrated divergence; shows non-uniqueness beyond proper scores",
        ),
    )


def improper_source_functionals() -> tuple[SourceFunctional, ...]:
    return (
        SourceFunctional(
            "linear probability reward",
            _linear_reward_value,
            _linear_reward_q_gradient,
            _linear_reward_q_curvature,
            "improper: it drives q toward a boundary and is not stationary at q=d",
        ),
        SourceFunctional(
            "amplitude-calibrated square",
            _amplitude_square_value,
            _amplitude_square_q_gradient,
            _amplitude_square_q_curvature,
            "wrong target: it calibrates sqrt(q) to d, not q to d",
        ),
    )


def beta_gradient(functional: SourceFunctional, beta: float, source_density: float, power: int = 2) -> float:
    probability = model_probability(beta, power)
    return functional.q_gradient(source_density, probability) * (-float(power) * probability)


def beta_curvature(functional: SourceFunctional, beta: float, source_density: float, power: int = 2) -> float:
    probability = model_probability(beta, power)
    power_f = float(power)
    dq = -power_f * probability
    d2q = power_f * power_f * probability
    return functional.q_curvature(source_density, probability) * dq * dq + functional.q_gradient(source_density, probability) * d2q


def calibrated_action_rows() -> tuple[CalibratedActionRow, ...]:
    density = born_selection().selected_density
    beta = beta_for_source(density, power=2)
    probability = model_probability(beta, power=2)
    amplitude = math.exp(-beta)
    rows = []
    for functional in calibrated_source_functionals():
        derivative = beta_gradient(functional, beta, density, power=2)
        curvature = beta_curvature(functional, beta, density, power=2)
        left_derivative = beta_gradient(functional, beta - BETA_DELTA, density, power=2)
        right_derivative = beta_gradient(functional, beta + BETA_DELTA, density, power=2)
        target_error = abs(amplitude * amplitude - EPS0_SQ)
        rows.append(
            CalibratedActionRow(
                label=functional.label,
                value_at_stationary=float(functional.value(density, probability)),
                beta_derivative=float(derivative),
                beta_curvature=float(curvature),
                left_derivative=float(left_derivative),
                right_derivative=float(right_derivative),
                stationary_beta=float(beta),
                stationary_amplitude=float(amplitude),
                stationary_probability=float(probability),
                target_error=float(target_error),
                matches_target=target_error < MATCH_TOL,
                interpretation=functional.interpretation,
            )
        )
    return tuple(rows)


def source_control_rows() -> tuple[SourceControlRow, ...]:
    density = born_selection().selected_density
    controls = (
        (
            "projective probability source",
            density,
            2,
            "correct source/channel: q=exp(-2 beta)=projective probability",
        ),
        (
            "amplitude-as-probability channel",
            density,
            1,
            "wrong channel: calibrates exp(-beta) directly as probability",
        ),
        (
            "state-count-only source",
            1.0 / CARRIER_DIM,
            2,
            "wrong source: omits the Berry/WZ pi",
        ),
        (
            "level-two source",
            half_turn_density(2.0),
            2,
            "wrong source: uses the k=2 WZ sector",
        ),
    )
    rows = []
    for label, source_density, power, interpretation in controls:
        beta = beta_for_source(source_density, power)
        amplitude = math.exp(-beta)
        probability = model_probability(beta, power)
        target_error = abs(amplitude * amplitude - EPS0_SQ)
        rows.append(
            SourceControlRow(
                label=label,
                source_density=float(source_density),
                model_power=int(power),
                stationary_beta=float(beta),
                stationary_amplitude=float(amplitude),
                stationary_probability=float(probability),
                target_error=float(target_error),
                matches_target=target_error < MATCH_TOL,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def improper_action_rows() -> tuple[ImproperActionRow, ...]:
    density = born_selection().selected_density
    beta = beta_for_source(density, power=2)
    rows = []
    for functional in improper_source_functionals():
        derivative = beta_gradient(functional, beta, density, power=2)
        curvature = beta_curvature(functional, beta, density, power=2)
        rows.append(
            ImproperActionRow(
                label=functional.label,
                derivative_at_target_beta=float(derivative),
                curvature_at_target_beta=float(curvature),
                target_is_stationary_minimum=abs(derivative) < TOL and curvature > 0.0,
                interpretation=functional.interpretation,
            )
        )
    return tuple(rows)


def calibrated_source_selection() -> CalibratedSourceSelection:
    density = born_selection().selected_density
    beta = beta_for_source(density, power=2)
    amplitude = math.exp(-beta)
    probability = model_probability(beta, power=2)
    rows = calibrated_action_rows()
    return CalibratedSourceSelection(
        source_density=float(density),
        stationary_beta=float(beta),
        stationary_amplitude=float(amplitude),
        stationary_probability=float(probability),
        stationary_ratios=tuple(float(x) for x in gibbs_ratios(beta)),
        all_calibrated_actions_select_same_beta=all(row.matches_target for row in rows),
        kl_action_unique=False,
        source_calibration_derived=False,
        cho_action_coupling_derived=False,
    )


def main() -> bool:
    action_rows = calibrated_action_rows()
    control_rows = source_control_rows()
    improper_rows = improper_action_rows()
    selection = calibrated_source_selection()
    target_beta = -math.log(EPS0)

    print("=" * 78)
    print("F4-BREAKING CALIBRATED SOURCE-ACTION GATE")
    print("Does beta stationarity depend on choosing KL specifically?")
    print("=" * 78)

    print("\n[A] Calibrated local source actions")
    for row in action_rows:
        print(
            f"  {row.label:<31} F*={row.value_at_stationary:.2e} "
            f"dF={row.beta_derivative:+.2e} d2F={row.beta_curvature:.3e} "
            f"left={row.left_derivative:+.2e} right={row.right_derivative:+.2e} "
            f"beta={row.stationary_beta:.12f} match={row.matches_target}"
        )
        print(f"      {row.interpretation}")

    print("\n[B] Source/channel controls")
    for row in control_rows:
        print(
            f"  {row.label:<33} p={row.model_power} source={row.source_density:.12f} "
            f"beta={row.stationary_beta:.12f} amp={row.stationary_amplitude:.12f} "
            f"q={row.stationary_probability:.12f} |amp^2-target|={row.target_error:.3e} "
            f"match={row.matches_target}"
        )
        print(f"      {row.interpretation}")

    print("\n[C] Improper action controls at the target beta")
    for row in improper_rows:
        print(
            f"  {row.label:<31} dF={row.derivative_at_target_beta:+.3e} "
            f"d2F={row.curvature_at_target_beta:+.3e} "
            f"stationary_min={row.target_is_stationary_minimum}"
        )
        print(f"      {row.interpretation}")

    print("\n[D] Selected robust stationary solution")
    print(f"  source density d                         : {selection.source_density:.15f}")
    print(f"  stationary beta                          : {selection.stationary_beta:.12f}")
    print(f"  target beta=-log(eps0)                   : {target_beta:.12f}")
    print(f"  exp(-beta)                               : {selection.stationary_amplitude:.15f}")
    print(f"  eps0                                     : {EPS0:.15f}")
    print(f"  exp(-2 beta)                             : {selection.stationary_probability:.15f}")
    print(f"  pi/432                                   : {EPS0_SQ:.15f}")
    print(
        "  Gibbs/source ratios                       : "
        f"({selection.stationary_ratios[0]:.9f}, "
        f"{selection.stationary_ratios[1]:.9f}, "
        f"{selection.stationary_ratios[2]:.9f})"
    )

    print("\n[V] Verdict")
    print("  KL-specific tuning required               : NO")
    print("  calibrated source actions select beta     : YES, conditional")
    print("  source calibration derived from CHO        : NO")
    print("  CHO source-channel action derived          : NO")
    print("  Bayes/scoreboard credit moved             : NO")
    print("=" * 78)

    matching_controls = [row for row in control_rows if row.matches_target]
    misses = [row for row in control_rows if not row.matches_target]
    assert len(action_rows) >= 4
    assert all(abs(row.value_at_stationary) < TOL for row in action_rows)
    assert all(abs(row.beta_derivative) < TOL for row in action_rows)
    assert all(row.beta_curvature > 0.0 for row in action_rows)
    assert all(row.left_derivative < 0.0 for row in action_rows)
    assert all(row.right_derivative > 0.0 for row in action_rows)
    assert all(abs(row.stationary_beta - target_beta) < MATCH_TOL for row in action_rows)
    assert all(abs(row.stationary_amplitude - EPS0) < MATCH_TOL for row in action_rows)
    assert all(abs(row.stationary_probability - EPS0_SQ) < MATCH_TOL for row in action_rows)
    assert all(row.matches_target for row in action_rows)
    assert len(matching_controls) == 1
    assert matching_controls[0].label == "projective probability source"
    assert all(row.target_error > MISS_TOL for row in misses)
    assert all(not row.target_is_stationary_minimum for row in improper_rows)
    assert all(abs(row.derivative_at_target_beta) > MISS_TOL for row in improper_rows)
    assert abs(selection.source_density - EPS0_SQ) < MATCH_TOL
    assert abs(selection.stationary_beta - target_beta) < MATCH_TOL
    assert abs(selection.stationary_amplitude - EPS0) < MATCH_TOL
    assert abs(selection.stationary_probability - EPS0_SQ) < MATCH_TOL
    assert abs(selection.stationary_ratios[1] - EPS0) < MATCH_TOL
    assert abs(selection.stationary_ratios[2] - EPS0_SQ) < MATCH_TOL
    assert selection.all_calibrated_actions_select_same_beta
    assert not selection.kl_action_unique
    assert not selection.source_calibration_derived
    assert not selection.cho_action_coupling_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)