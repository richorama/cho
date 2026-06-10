"""
F4-BREAKING LARGE-DEVIATION SOURCE GATE -- where could the KL source term come from?
===================================================================================

The calibrated source-action gate narrowed the remaining assumption from a special
KL/log-score action to a calibrated source coupling on the projective probability

    q(beta) = exp(-2 beta).

This gate tries the next, more statistical-mechanical rung. If the projective
transition channel is sampled repeatedly as a two-outcome process, and the selected
WZ/carrier density is the empirical source frequency

    d = pi/432,

then binomial counting gives

    P(m successes in N trials | q) = C(N,m) q^m (1-q)^(N-m).

The relative negative log-likelihood density against its own empirical optimum is

    [-log P(m|q) + log P(m|d_hat)] / N = KL(d_hat || q),

exactly for d_hat=m/N. In the large-deviation limit d_hat -> d, the source action
is the Bernoulli KL term used by the stationarity gate. Stationarity then forces
q=d and beta=-log(eps0).

What this proves
----------------
KL is no longer merely a chosen calibrated functional: it is the universal rate
function for repeated projective-transition counts, conditional on treating the
selected WZ/Born density as an empirical source frequency for independent
two-outcome transition trials.

What this still does not prove
------------------------------
This does not derive from CHO dynamics why such an independent projective-transition
ensemble exists, why its empirical density is the selected WZ density, or why the
F4-breaking action must be the corresponding large-deviation action. The live bridge
is now the origin of that statistical ensemble/source interpretation.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_large_deviation_source_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from f4_breaking_born_beta_map_gate import born_selection, gibbs_ratios
from f4_breaking_primitive_level_gate import CARRIER_DIM, half_turn_density
from f4_breaking_seed_op2 import EPS0, EPS0_SQ
from f4_breaking_source_stationarity_gate import (
    bernoulli_kl,
    beta_for_source,
    model_probability,
    source_stationarity_curvature,
    source_stationarity_derivative,
)


TOL = 1e-12
MATCH_TOL = 1e-14
MISS_TOL = 1e-3
COUNTING_TOL = 1e-12


@dataclass(frozen=True)
class CountingIdentityRow:
    total_trials: int
    successes: int
    empirical_density: float
    probe_probability: float
    relative_rate: float
    kl_rate: float
    identity_error: float
    density_error: float
    stationary_beta: float
    beta_error: float


@dataclass(frozen=True)
class LargeDeviationStationarityRow:
    label: str
    source_density: float
    model_power: int
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    derivative: float
    curvature: float
    kl_value: float
    target_error: float
    matches_target: bool
    interpretation: str


@dataclass(frozen=True)
class LargeDeviationSelection:
    source_density: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    stationary_ratios: tuple[float, float, float]
    counting_derives_kl_rate: bool
    large_deviation_source_action_derived: bool
    independent_transition_ensemble_derived: bool
    cho_source_coupling_derived: bool


def _check_probability(probability: float) -> None:
    if not 0.0 < probability < 1.0:
        raise ValueError("probability must lie in (0, 1)")


def log_binomial_coefficient(total_trials: int, successes: int) -> float:
    if not 0 <= successes <= total_trials:
        raise ValueError("successes must lie between 0 and total_trials")
    return (
        math.lgamma(total_trials + 1.0)
        - math.lgamma(successes + 1.0)
        - math.lgamma(total_trials - successes + 1.0)
    )


def binomial_log_probability(total_trials: int, successes: int, probability: float) -> float:
    _check_probability(probability)
    return (
        log_binomial_coefficient(total_trials, successes)
        + successes * math.log(probability)
        + (total_trials - successes) * math.log(1.0 - probability)
    )


def empirical_density(total_trials: int, successes: int) -> float:
    if total_trials <= 0:
        raise ValueError("total_trials must be positive")
    if not 0 <= successes <= total_trials:
        raise ValueError("successes must lie between 0 and total_trials")
    density = successes / total_trials
    _check_probability(density)
    return density


def relative_log_likelihood_rate(total_trials: int, successes: int, probability: float) -> float:
    density = empirical_density(total_trials, successes)
    best_log_probability = binomial_log_probability(total_trials, successes, density)
    model_log_probability = binomial_log_probability(total_trials, successes, probability)
    return (best_log_probability - model_log_probability) / total_trials


def counting_identity_rows() -> tuple[CountingIdentityRow, ...]:
    target_density = born_selection().selected_density
    target_beta = beta_for_source(target_density, power=2)
    total_trials_list = (10_000, 100_000, 1_000_000)
    rows = []
    for total_trials in total_trials_list:
        successes = max(1, min(total_trials - 1, round(total_trials * target_density)))
        density = empirical_density(total_trials, successes)
        probe_probability = min(0.95, density * 1.7)
        relative_rate = relative_log_likelihood_rate(total_trials, successes, probe_probability)
        kl_rate = bernoulli_kl(density, probe_probability)
        beta = beta_for_source(density, power=2)
        rows.append(
            CountingIdentityRow(
                total_trials=int(total_trials),
                successes=int(successes),
                empirical_density=float(density),
                probe_probability=float(probe_probability),
                relative_rate=float(relative_rate),
                kl_rate=float(kl_rate),
                identity_error=abs(relative_rate - kl_rate),
                density_error=abs(density - target_density),
                stationary_beta=float(beta),
                beta_error=abs(beta - target_beta),
            )
        )
    return tuple(rows)


def large_deviation_stationarity_rows() -> tuple[LargeDeviationStationarityRow, ...]:
    selected_density = born_selection().selected_density
    candidates = (
        (
            "projective empirical source",
            selected_density,
            2,
            "correct: empirical frequency for q=exp(-2 beta) projective transitions",
        ),
        (
            "amplitude-count source",
            selected_density,
            1,
            "wrong channel: counts exp(-beta) amplitudes as if they were Bernoulli probabilities",
        ),
        (
            "state-count-only source",
            1.0 / CARRIER_DIM,
            2,
            "wrong source: empirical frequency omits the Berry/WZ pi",
        ),
        (
            "level-two empirical source",
            half_turn_density(2.0),
            2,
            "wrong source: empirical frequency comes from the k=2 WZ sector",
        ),
    )
    rows = []
    for label, source_density, model_power, interpretation in candidates:
        beta = beta_for_source(source_density, model_power)
        amplitude = math.exp(-beta)
        probability = model_probability(beta, model_power)
        derivative = source_stationarity_derivative(beta, source_density, model_power)
        curvature = source_stationarity_curvature(beta, source_density, model_power)
        kl_value = bernoulli_kl(source_density, probability)
        target_error = abs((amplitude * amplitude) - EPS0_SQ)
        rows.append(
            LargeDeviationStationarityRow(
                label=label,
                source_density=float(source_density),
                model_power=int(model_power),
                stationary_beta=float(beta),
                stationary_amplitude=float(amplitude),
                stationary_probability=float(probability),
                derivative=float(derivative),
                curvature=float(curvature),
                kl_value=float(kl_value),
                target_error=float(target_error),
                matches_target=target_error < MATCH_TOL,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def large_deviation_selection() -> LargeDeviationSelection:
    density = born_selection().selected_density
    beta = beta_for_source(density, power=2)
    amplitude = math.exp(-beta)
    probability = model_probability(beta, power=2)
    counting_rows = counting_identity_rows()
    return LargeDeviationSelection(
        source_density=float(density),
        stationary_beta=float(beta),
        stationary_amplitude=float(amplitude),
        stationary_probability=float(probability),
        stationary_ratios=tuple(float(value) for value in gibbs_ratios(beta)),
        counting_derives_kl_rate=all(row.identity_error < COUNTING_TOL for row in counting_rows),
        large_deviation_source_action_derived=True,
        independent_transition_ensemble_derived=False,
        cho_source_coupling_derived=False,
    )


def main() -> bool:
    counting_rows = counting_identity_rows()
    stationarity_rows = large_deviation_stationarity_rows()
    selection = large_deviation_selection()
    target_beta = -math.log(EPS0)

    print("=" * 78)
    print("F4-BREAKING LARGE-DEVIATION SOURCE GATE")
    print("Does repeated projective-transition counting force the KL source term?")
    print("=" * 78)

    print("\n[A] Exact finite-count identity")
    print("    [-log P(m|q)+log P(m|m/N)]/N = KL(m/N || q)")
    for row in counting_rows:
        print(
            f"  N={row.total_trials:<8} m={row.successes:<5} "
            f"d_hat={row.empirical_density:.12f} q_probe={row.probe_probability:.12f} "
            f"rate={row.relative_rate:.6e} KL={row.kl_rate:.6e} "
            f"identity_err={row.identity_error:.2e} "
            f"|d_hat-d|={row.density_error:.3e} beta_err={row.beta_error:.3e}"
        )

    print("\n[B] Large-deviation stationarity controls")
    for row in stationarity_rows:
        print(
            f"  {row.label:<29} p={row.model_power} source={row.source_density:.12f} "
            f"beta={row.stationary_beta:.12f} amp={row.stationary_amplitude:.12f} "
            f"q={row.stationary_probability:.12f} dF={row.derivative:+.2e} "
            f"d2F={row.curvature:.3f} KL={row.kl_value:.2e} "
            f"|amp^2-target|={row.target_error:.3e} match={row.matches_target}"
        )
        print(f"      {row.interpretation}")

    print("\n[C] Selected large-deviation source solution")
    print(f"  source density d                         : {selection.source_density:.15f}")
    print(f"  stationary beta                          : {selection.stationary_beta:.12f}")
    print(f"  target beta=-log(eps0)                   : {target_beta:.12f}")
    print(f"  exp(-beta)                               : {selection.stationary_amplitude:.15f}")
    print(f"  exp(-2 beta)                             : {selection.stationary_probability:.15f}")
    print(f"  pi/432                                   : {EPS0_SQ:.15f}")
    print(
        "  Gibbs/source ratios                       : "
        f"({selection.stationary_ratios[0]:.9f}, "
        f"{selection.stationary_ratios[1]:.9f}, "
        f"{selection.stationary_ratios[2]:.9f})"
    )

    print("\n[V] Verdict")
    print("  counting derives KL rate                  : YES, conditional")
    print("  KL source action merely chosen            : NO")
    print("  independent transition ensemble derived   : NO")
    print("  CHO source-channel coupling derived       : NO")
    print("  Bayes/scoreboard credit moved             : NO")
    print("=" * 78)

    matching = [row for row in stationarity_rows if row.matches_target]
    misses = [row for row in stationarity_rows if not row.matches_target]
    density_errors = [row.density_error for row in counting_rows]
    beta_errors = [row.beta_error for row in counting_rows]
    assert all(row.identity_error < COUNTING_TOL for row in counting_rows)
    assert density_errors[-1] < density_errors[0]
    assert beta_errors[-1] < beta_errors[0]
    assert len(matching) == 1
    assert matching[0].label == "projective empirical source"
    assert all(abs(row.derivative) < TOL for row in stationarity_rows)
    assert all(row.curvature > 0.0 for row in stationarity_rows)
    assert all(abs(row.kl_value) < TOL for row in stationarity_rows)
    assert all(row.target_error > MISS_TOL for row in misses)
    assert abs(selection.source_density - EPS0_SQ) < MATCH_TOL
    assert abs(selection.stationary_beta - target_beta) < MATCH_TOL
    assert abs(selection.stationary_amplitude - EPS0) < MATCH_TOL
    assert abs(selection.stationary_probability - EPS0_SQ) < MATCH_TOL
    assert abs(selection.stationary_ratios[1] - EPS0) < MATCH_TOL
    assert abs(selection.stationary_ratios[2] - EPS0_SQ) < MATCH_TOL
    assert selection.counting_derives_kl_rate
    assert selection.large_deviation_source_action_derived
    assert not selection.independent_transition_ensemble_derived
    assert not selection.cho_source_coupling_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)