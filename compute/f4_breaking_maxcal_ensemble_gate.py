"""
F4-BREAKING MAXIMUM-CALIBER ENSEMBLE GATE -- can independence be forced?
================================================================================

The large-deviation source gate showed that if projective transitions are sampled
as independent two-outcome trials, finite binomial counting gives the KL source
action and stationarity selects

    q(beta) = exp(-2 beta) = d = pi/432.

This gate climbs one rung higher: can the independent Bernoulli ensemble be made
the least-biased lift of a weaker datum rather than assumed directly?

Consider binary histories x in {0,1}^N recording whether the projective transition
occurs on each trial. If the only constrained history observable is the mean
transition count

    E[sum_i x_i] / N = d,

then maximizing Shannon path entropy gives the canonical maximum-caliber measure

    P_lambda(x) = exp(-lambda sum_i x_i) / Z(lambda),
    Z(lambda) = (1 + exp(-lambda))^N.

This factorizes exactly into independent Bernoulli trials with

    q = 1 / (1 + exp(lambda)).

Thus, conditional on the MaxCal/least-biased-history principle and the imported
projective mean constraint d=pi/432, the iid ensemble used by the large-deviation
gate is derived as a variational consequence.

What this proves
----------------
The independent Bernoulli counting ensemble is not an extra choice once binary
projective histories, the single mean-count constraint, and Shannon maximum
caliber are granted. Correlated same-mean controls have strictly lower entropy per
trial.

What this still does not prove
------------------------------
This does not derive from CHO/F4-breaking dynamics why the physical path measure
must obey Shannon maximum caliber, why the only constraint is the selected mean
projective transition density, or why that inference principle is the microscopic
action. The live bridge moves to the origin of the MaxCal principle and the source
constraint in the CHO action.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_maxcal_ensemble_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from f4_breaking_born_beta_map_gate import born_selection, gibbs_ratios
from f4_breaking_large_deviation_source_gate import (
    large_deviation_stationarity_rows,
    log_binomial_coefficient,
)
from f4_breaking_seed_op2 import EPS0, EPS0_SQ
from f4_breaking_source_stationarity_gate import beta_for_source, model_probability


TOL = 1e-12
MATCH_TOL = 1e-14
ENTROPY_GAP_TOL = 1e-5


@dataclass(frozen=True)
class MaxCalFactorizationRow:
    total_trials: int
    source_density: float
    lagrange_multiplier: float
    partition_direct: float
    partition_closed: float
    partition_error: float
    normalization_error: float
    mean_density: float
    mean_error: float
    factorization_error: float
    marginal_error: float
    covariance_error: float
    entropy_per_trial: float
    bernoulli_entropy: float
    entropy_error: float


@dataclass(frozen=True)
class EntropyControlRow:
    label: str
    total_trials: int
    mean_density: float
    entropy_per_trial: float
    entropy_bound: float
    entropy_gap: float
    pair_correlation: float
    lower_than_maxcal: bool
    interpretation: str


@dataclass(frozen=True)
class MaxCalSelection:
    source_density: float
    lagrange_multiplier: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    stationary_ratios: tuple[float, float, float]
    maxcal_factorization_verified: bool
    correlated_controls_lower_entropy: bool
    iid_ensemble_derived_from_maxcal: bool
    maxcal_principle_derived_from_cho: bool
    cho_mean_constraint_derived: bool
    cho_source_coupling_derived: bool


def _check_probability(probability: float) -> None:
    if not 0.0 < probability < 1.0:
        raise ValueError("probability must lie in (0, 1)")


def _popcount(value: int) -> int:
    return bin(value).count("1")


def binary_entropy(probability: float) -> float:
    _check_probability(probability)
    return -probability * math.log(probability) - (1.0 - probability) * math.log(1.0 - probability)


def maxcal_lagrange_multiplier(mean_density: float) -> float:
    _check_probability(mean_density)
    return math.log((1.0 - mean_density) / mean_density)


def maxcal_probability_from_multiplier(lagrange_multiplier: float) -> float:
    exp_minus_multiplier = math.exp(-lagrange_multiplier)
    return exp_minus_multiplier / (1.0 + exp_minus_multiplier)


def maxcal_factorization_row(total_trials: int, source_density: float) -> MaxCalFactorizationRow:
    _check_probability(source_density)
    if total_trials < 2:
        raise ValueError("total_trials must be at least 2")

    lagrange_multiplier = maxcal_lagrange_multiplier(source_density)
    exp_minus_multiplier = math.exp(-lagrange_multiplier)
    partition_closed = (1.0 + exp_minus_multiplier) ** total_trials
    history_count = 1 << total_trials

    partition_direct = 0.0
    for history in range(history_count):
        successes = _popcount(history)
        partition_direct += math.exp(-lagrange_multiplier * successes)

    normalization = 0.0
    mean_count = 0.0
    entropy = 0.0
    first_marginal = 0.0
    second_marginal = 0.0
    pair_marginal = 0.0
    factorization_error = 0.0
    for history in range(history_count):
        successes = _popcount(history)
        probability = math.exp(-lagrange_multiplier * successes) / partition_direct
        factor_probability = (source_density ** successes) * ((1.0 - source_density) ** (total_trials - successes))
        normalization += probability
        mean_count += probability * successes
        entropy -= probability * math.log(probability)
        if history & 1:
            first_marginal += probability
        if history & 2:
            second_marginal += probability
        if (history & 1) and (history & 2):
            pair_marginal += probability
        factorization_error = max(
            factorization_error,
            abs(math.log(probability) - math.log(factor_probability)),
        )

    mean_density = mean_count / total_trials
    entropy_per_trial = entropy / total_trials
    entropy_bound = binary_entropy(source_density)
    return MaxCalFactorizationRow(
        total_trials=int(total_trials),
        source_density=float(source_density),
        lagrange_multiplier=float(lagrange_multiplier),
        partition_direct=float(partition_direct),
        partition_closed=float(partition_closed),
        partition_error=abs(partition_direct - partition_closed),
        normalization_error=abs(normalization - 1.0),
        mean_density=float(mean_density),
        mean_error=abs(mean_density - source_density),
        factorization_error=float(factorization_error),
        marginal_error=max(abs(first_marginal - source_density), abs(second_marginal - source_density)),
        covariance_error=abs(pair_marginal - first_marginal * second_marginal),
        entropy_per_trial=float(entropy_per_trial),
        bernoulli_entropy=float(entropy_bound),
        entropy_error=abs(entropy_per_trial - entropy_bound),
    )


def maxcal_factorization_rows() -> tuple[MaxCalFactorizationRow, ...]:
    source_density = born_selection().selected_density
    return tuple(maxcal_factorization_row(total_trials, source_density) for total_trials in (4, 8, 12))


def entropy_control_rows() -> tuple[EntropyControlRow, ...]:
    source_density = born_selection().selected_density
    history_trials = 64
    entropy_bound = binary_entropy(source_density)

    all_or_none_entropy = entropy_bound / history_trials
    all_or_none_correlation = source_density * (1.0 - source_density)

    pair_block_entropy = entropy_bound / 2.0
    pair_block_correlation = source_density * (1.0 - source_density)

    fixed_count_trials = 10_000
    fixed_count_successes = round(fixed_count_trials * source_density)
    fixed_count_density = fixed_count_successes / fixed_count_trials
    fixed_count_entropy_bound = binary_entropy(fixed_count_density)
    fixed_count_entropy = log_binomial_coefficient(fixed_count_trials, fixed_count_successes) / fixed_count_trials
    fixed_count_correlation = -fixed_count_density * (1.0 - fixed_count_density) / (fixed_count_trials - 1.0)

    candidates = (
        (
            "all-or-none history",
            history_trials,
            source_density,
            all_or_none_entropy,
            entropy_bound,
            all_or_none_correlation,
            "same mean count, but every trial is locked to every other trial",
        ),
        (
            "paired-block history",
            history_trials,
            source_density,
            pair_block_entropy,
            entropy_bound,
            pair_block_correlation,
            "same mean count, but transitions arrive in perfectly correlated pairs",
        ),
        (
            "fixed-count microcanonical",
            fixed_count_trials,
            fixed_count_density,
            fixed_count_entropy,
            fixed_count_entropy_bound,
            fixed_count_correlation,
            "exact count constraint creates exchangeable anti-correlations at finite N",
        ),
    )

    rows = []
    for label, total_trials, mean_density, entropy_per_trial, bound, pair_correlation, interpretation in candidates:
        entropy_gap = bound - entropy_per_trial
        rows.append(
            EntropyControlRow(
                label=label,
                total_trials=int(total_trials),
                mean_density=float(mean_density),
                entropy_per_trial=float(entropy_per_trial),
                entropy_bound=float(bound),
                entropy_gap=float(entropy_gap),
                pair_correlation=float(pair_correlation),
                lower_than_maxcal=entropy_gap > ENTROPY_GAP_TOL,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def maxcal_selection() -> MaxCalSelection:
    source_density = born_selection().selected_density
    factorization_rows = maxcal_factorization_rows()
    control_rows = entropy_control_rows()
    lagrange_multiplier = maxcal_lagrange_multiplier(source_density)
    stationary_beta = beta_for_source(source_density, power=2)
    stationary_amplitude = math.exp(-stationary_beta)
    stationary_probability = model_probability(stationary_beta, power=2)
    return MaxCalSelection(
        source_density=float(source_density),
        lagrange_multiplier=float(lagrange_multiplier),
        stationary_beta=float(stationary_beta),
        stationary_amplitude=float(stationary_amplitude),
        stationary_probability=float(stationary_probability),
        stationary_ratios=tuple(float(value) for value in gibbs_ratios(stationary_beta)),
        maxcal_factorization_verified=all(
            row.partition_error < TOL
            and row.normalization_error < TOL
            and row.mean_error < TOL
            and row.factorization_error < TOL
            and row.marginal_error < TOL
            and row.covariance_error < TOL
            and row.entropy_error < TOL
            for row in factorization_rows
        ),
        correlated_controls_lower_entropy=all(row.lower_than_maxcal for row in control_rows),
        iid_ensemble_derived_from_maxcal=True,
        maxcal_principle_derived_from_cho=False,
        cho_mean_constraint_derived=False,
        cho_source_coupling_derived=False,
    )


def main() -> bool:
    factorization_rows = maxcal_factorization_rows()
    control_rows = entropy_control_rows()
    stationarity_rows = large_deviation_stationarity_rows()
    selection = maxcal_selection()
    target_beta = -math.log(EPS0)
    target_lagrange_multiplier = math.log((1.0 - EPS0_SQ) / EPS0_SQ)

    print("=" * 78)
    print("F4-BREAKING MAXIMUM-CALIBER ENSEMBLE GATE")
    print("Does a least-biased path measure force the independent counting ensemble?")
    print("=" * 78)

    print("\n[A] MaxCal factorization from one mean-count constraint")
    print("    P_lambda(history) = exp(-lambda K)/Z = product Bernoulli(q)")
    for row in factorization_rows:
        print(
            f"  N={row.total_trials:<2} lambda={row.lagrange_multiplier:.12f} "
            f"Z_err={row.partition_error:.2e} norm_err={row.normalization_error:.2e} "
            f"mean={row.mean_density:.15f} mean_err={row.mean_error:.2e} "
            f"fact_err={row.factorization_error:.2e} cov_err={row.covariance_error:.2e} "
            f"H/N={row.entropy_per_trial:.12f} H_B={row.bernoulli_entropy:.12f}"
        )

    print("\n[B] Same-mean correlated controls")
    for row in control_rows:
        print(
            f"  {row.label:<26} N={row.total_trials:<5} mean={row.mean_density:.12f} "
            f"H/N={row.entropy_per_trial:.12f} bound={row.entropy_bound:.12f} "
            f"gap={row.entropy_gap:.3e} corr={row.pair_correlation:+.3e} "
            f"lower={row.lower_than_maxcal}"
        )
        print(f"      {row.interpretation}")

    print("\n[C] Reconnect MaxCal mean to beta stationarity")
    for row in stationarity_rows:
        print(
            f"  {row.label:<29} p={row.model_power} source={row.source_density:.12f} "
            f"beta={row.stationary_beta:.12f} amp={row.stationary_amplitude:.12f} "
            f"q={row.stationary_probability:.12f} match={row.matches_target}"
        )

    print("\n[D] Selected MaxCal source solution")
    print(f"  source density d                         : {selection.source_density:.15f}")
    print(f"  MaxCal lambda=log((1-d)/d)               : {selection.lagrange_multiplier:.12f}")
    print(f"  target lambda                            : {target_lagrange_multiplier:.12f}")
    print(f"  stationary beta                          : {selection.stationary_beta:.12f}")
    print(f"  target beta=-log(eps0)                   : {target_beta:.12f}")
    print(f"  exp(-beta)                               : {selection.stationary_amplitude:.15f}")
    print(f"  exp(-2 beta)                             : {selection.stationary_probability:.15f}")
    print(
        "  Gibbs/source ratios                       : "
        f"({selection.stationary_ratios[0]:.9f}, "
        f"{selection.stationary_ratios[1]:.9f}, "
        f"{selection.stationary_ratios[2]:.9f})"
    )

    print("\n[V] Verdict")
    print("  iid ensemble from MaxCal                  : YES, conditional")
    print("  correlated same-mean controls excluded    : YES, by entropy")
    print("  MaxCal principle derived from CHO action  : NO")
    print("  CHO mean/source constraint derived        : NO")
    print("  Bayes/scoreboard credit moved             : NO")
    print("=" * 78)

    matching = [row for row in stationarity_rows if row.matches_target]
    misses = [row for row in stationarity_rows if not row.matches_target]
    assert all(row.partition_error < TOL for row in factorization_rows)
    assert all(row.normalization_error < TOL for row in factorization_rows)
    assert all(row.mean_error < TOL for row in factorization_rows)
    assert all(row.factorization_error < TOL for row in factorization_rows)
    assert all(row.marginal_error < TOL for row in factorization_rows)
    assert all(row.covariance_error < TOL for row in factorization_rows)
    assert all(row.entropy_error < TOL for row in factorization_rows)
    assert all(row.lower_than_maxcal for row in control_rows)
    assert len(matching) == 1
    assert matching[0].label == "projective empirical source"
    assert all(row.target_error > 1e-3 for row in misses)
    assert abs(maxcal_probability_from_multiplier(selection.lagrange_multiplier) - EPS0_SQ) < MATCH_TOL
    assert abs(selection.source_density - EPS0_SQ) < MATCH_TOL
    assert abs(selection.lagrange_multiplier - target_lagrange_multiplier) < MATCH_TOL
    assert abs(selection.stationary_beta - target_beta) < MATCH_TOL
    assert abs(selection.stationary_amplitude - EPS0) < MATCH_TOL
    assert abs(selection.stationary_probability - EPS0_SQ) < MATCH_TOL
    assert selection.maxcal_factorization_verified
    assert selection.correlated_controls_lower_entropy
    assert selection.iid_ensemble_derived_from_maxcal
    assert not selection.maxcal_principle_derived_from_cho
    assert not selection.cho_mean_constraint_derived
    assert not selection.cho_source_coupling_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)