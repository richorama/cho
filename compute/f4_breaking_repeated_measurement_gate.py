"""
F4-BREAKING REPEATED-MEASUREMENT GATE -- a physical origin for independence.
================================================================================

The maximum-caliber gate derived the independent Bernoulli ensemble from Shannon
maximum caliber plus a single mean-count constraint. The binary-projector gate
derived the {0,1}^N history alphabet from a primitive projective question. Both
still imported the abstract MaxCal inference principle to get independence.

This gate climbs sideways and underneath that principle: it derives the SAME iid
ensemble from the quantum measurement structure itself, with no maximum-entropy
inference at all.

Repeated projective measurement of one primitive question Q on a RE-PREPARED
rank-one source P gives, by the Born rule,

    p_yes = Tr(P o Q) = d = pi/432

on every trial, and re-preparation makes each trial independent of the history.
The path measure is therefore exactly the product Bernoulli(d) measure -- which is
identical to the maximum-caliber measure exp(-lambda K)/Z and to the large-
deviation Bernoulli measure. Three independent constructions land on one measure.

The control is the PERSISTENT (no re-preparation) process. After a "yes" outcome
the post-measurement state is the question ray Q itself, and re-measuring Q is
certain:

    Tr(Q o Q) = 1   (quantum-Zeno absorption),

so without re-preparation the outcomes are a correlated two-state Markov chain, not
an iid sequence. A one-parameter family of stationary Markov chains with the same
marginal d shows that the memoryless (lag-1 correlation = 0) re-prepared process is
the unique one whose path-entropy rate saturates the iid bound H(d); every nonzero
correlation lowers the entropy rate. Memorylessness <=> maximum caliber.

What this proves
----------------
Independence is not only a least-biased inference: it is the Born-rule path measure
of a memoryless re-prepared projective measurement, and it coincides exactly with
the MaxCal and large-deviation measures. The persistent (non-re-prepared) process
is the correlated Markov alternative, with the quantum-Zeno absorption Tr(Q o Q)=1
as its degenerate all-or-none limit.

What this still does not prove
------------------------------
This does not derive from CHO/F4-breaking dynamics why the physical transition
process is memoryless (re-prepared) rather than persistent, nor why the primitive
question Q has mean d=pi/432. It reduces "why MaxCal" to the more physical "why
memoryless re-preparation (no measurement-history back-action)", which remains open.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_repeated_measurement_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from epsilon_action_selection import trace_form
from f4_breaking_binary_projector_history_gate import identity_idempotent
from f4_breaking_born_geometry_gate import transition_projectors
from f4_breaking_maxcal_ensemble_gate import (
    binary_entropy,
    maxcal_lagrange_multiplier,
    maxcal_probability_from_multiplier,
)
from f4_breaking_seed_op2 import EPS0, EPS0_SQ
from f4_breaking_source_stationarity_gate import beta_for_source, model_probability


TOL = 1e-12
MATCH_TOL = 1e-14
ENTROPY_GAP_TOL = 1e-6
ZENO_TOL = 1e-9


@dataclass(frozen=True)
class RouteAgreementRow:
    total_trials: int
    history_count: int
    max_product_maxcal_error: float
    probability_sum_error: float
    mean_density: float
    mean_error: float


@dataclass(frozen=True)
class MarkovControlRow:
    label: str
    correlation: float
    measured_correlation: float
    stay_yes_probability: float
    stay_no_probability: float
    stationary_mean: float
    mean_error: float
    entropy_rate: float
    entropy_bound: float
    entropy_gap: float
    memoryless: bool
    interpretation: str


@dataclass(frozen=True)
class RepeatedMeasurementSelection:
    source_density: float
    born_event_probability: float
    reprepared_conditional: float
    persistent_conditional: float
    maxcal_probability: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    independence_from_born_reprep: bool
    three_routes_agree: bool
    memoryless_maximizes_entropy_rate: bool
    reprep_principle_derived_from_cho: bool
    cho_source_question_derived: bool


def _popcount(value: int) -> int:
    return bin(value).count("1")


def born_event_probability() -> float:
    _psi, _phi, source_projector, question_projector = transition_projectors(EPS0)
    return float(trace_form(source_projector, question_projector))


def reprepared_conditional_probability() -> float:
    """After re-preparing the source P the Born probability is history-independent."""
    return born_event_probability()


def persistent_conditional_probability() -> float:
    """After a 'yes' collapse the state is the question ray Q; re-measuring Q is certain."""
    _psi, _phi, _source_projector, question_projector = transition_projectors(EPS0)
    return float(trace_form(question_projector, question_projector))


def route_agreement_rows() -> tuple[RouteAgreementRow, ...]:
    density = EPS0_SQ
    lagrange_multiplier = maxcal_lagrange_multiplier(density)
    exp_minus_multiplier = math.exp(-lagrange_multiplier)
    rows = []
    for total_trials in (4, 8, 12):
        partition = (1.0 + exp_minus_multiplier) ** total_trials
        history_count = 1 << total_trials
        max_product_maxcal_error = 0.0
        probability_sum = 0.0
        mean_density = 0.0
        for history in range(history_count):
            successes = _popcount(history)
            product_probability = (density ** successes) * ((1.0 - density) ** (total_trials - successes))
            maxcal_probability = math.exp(-lagrange_multiplier * successes) / partition
            max_product_maxcal_error = max(max_product_maxcal_error, abs(product_probability - maxcal_probability))
            probability_sum += product_probability
            mean_density += (successes / total_trials) * product_probability
        rows.append(
            RouteAgreementRow(
                total_trials=int(total_trials),
                history_count=int(history_count),
                max_product_maxcal_error=float(max_product_maxcal_error),
                probability_sum_error=abs(probability_sum - 1.0),
                mean_density=float(mean_density),
                mean_error=abs(mean_density - density),
            )
        )
    return tuple(rows)


def markov_entropy_rate(density: float, correlation: float) -> tuple[float, float, float]:
    """Stationary 2-state chain with marginal `density` and lag-1 correlation `correlation`."""
    forward = density * (1.0 - correlation)
    backward = (1.0 - density) * (1.0 - correlation)
    stationary_one = forward / (forward + backward)
    stationary_zero = 1.0 - stationary_one
    rate = stationary_zero * binary_entropy(forward) + stationary_one * binary_entropy(backward)
    return rate, forward, backward


def markov_control_rows() -> tuple[MarkovControlRow, ...]:
    density = EPS0_SQ
    bound = binary_entropy(density)
    specs = (
        (0.0, "memoryless re-preparation (Born)", "re-prepared source: each trial is independent, the product/MaxCal measure"),
        (0.3, "weakly sticky persistence", "partial memory: outcomes weakly persist, entropy rate below the iid bound"),
        (0.6, "sticky persistence", "stronger memory: longer runs of the same outcome, lower entropy rate"),
        (0.9, "strong persistence", "near-frozen runs: most of the iid path entropy is gone"),
        (0.99, "near-Zeno persistence", "approaching the Tr(Q o Q)=1 absorption: all-or-none histories"),
    )
    rows = []
    for correlation, label, interpretation in specs:
        rate, forward, backward = markov_entropy_rate(density, correlation)
        measured_correlation = 1.0 - forward - backward
        stationary_mean = forward / (forward + backward)
        rows.append(
            MarkovControlRow(
                label=label,
                correlation=float(correlation),
                measured_correlation=float(measured_correlation),
                stay_yes_probability=float(1.0 - backward),
                stay_no_probability=float(1.0 - forward),
                stationary_mean=float(stationary_mean),
                mean_error=abs(stationary_mean - density),
                entropy_rate=float(rate),
                entropy_bound=float(bound),
                entropy_gap=float(bound - rate),
                memoryless=abs(correlation) < TOL,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def repeated_measurement_selection() -> RepeatedMeasurementSelection:
    density = EPS0_SQ
    lagrange_multiplier = maxcal_lagrange_multiplier(density)
    beta = beta_for_source(density, power=2)
    route_rows = route_agreement_rows()
    control_rows = markov_control_rows()
    reprepared = reprepared_conditional_probability()
    persistent = persistent_conditional_probability()
    born = born_event_probability()
    memoryless_rows = [row for row in control_rows if row.memoryless]
    correlated_rows = [row for row in control_rows if not row.memoryless]
    return RepeatedMeasurementSelection(
        source_density=float(density),
        born_event_probability=float(born),
        reprepared_conditional=float(reprepared),
        persistent_conditional=float(persistent),
        maxcal_probability=float(maxcal_probability_from_multiplier(lagrange_multiplier)),
        stationary_beta=float(beta),
        stationary_amplitude=float(math.exp(-beta)),
        stationary_probability=float(model_probability(beta, power=2)),
        independence_from_born_reprep=(
            abs(reprepared - born) < TOL and persistent > 1.0 - ZENO_TOL
        ),
        three_routes_agree=all(row.max_product_maxcal_error < TOL for row in route_rows),
        memoryless_maximizes_entropy_rate=(
            len(memoryless_rows) == 1
            and memoryless_rows[0].entropy_gap < ENTROPY_GAP_TOL
            and all(row.entropy_gap > ENTROPY_GAP_TOL for row in correlated_rows)
        ),
        reprep_principle_derived_from_cho=False,
        cho_source_question_derived=False,
    )


def main() -> bool:
    route_rows = route_agreement_rows()
    control_rows = markov_control_rows()
    selection = repeated_measurement_selection()
    target_beta = -math.log(EPS0)

    print("=" * 78)
    print("F4-BREAKING REPEATED-MEASUREMENT GATE")
    print("Does memoryless projective re-measurement give the independent ensemble?")
    print("=" * 78)

    print("\n[A] Born repeated measurement: re-prepared vs persistent")
    print(f"  Born event probability Tr(P o Q)         : {selection.born_event_probability:.15f}")
    print(f"  pi/432                                    : {EPS0_SQ:.15f}")
    print(f"  re-prepared conditional p(yes | history)  : {selection.reprepared_conditional:.15f}")
    print(f"  persistent conditional Tr(Q o Q)          : {selection.persistent_conditional:.15f}")
    print("  re-preparation makes trials independent; persistence (Zeno) freezes to 'yes'.")

    print("\n[B] Three routes to the same product measure")
    for row in route_rows:
        print(
            f"  N={row.total_trials:<2} histories={row.history_count:<5} "
            f"|Born-MaxCal|={row.max_product_maxcal_error:.2e} "
            f"sum_err={row.probability_sum_error:.2e} "
            f"mean={row.mean_density:.15f} mean_err={row.mean_error:.2e}"
        )
    print("  Born re-prepared product = MaxCal exp(-lambda K)/Z = large-deviation Bernoulli.")

    print("\n[C] Persistence destroys independence (same marginal, lower entropy rate)")
    for row in control_rows:
        print(
            f"  {row.label:<33} corr={row.correlation:.2f} "
            f"meas_corr={row.measured_correlation:+.3e} mean={row.stationary_mean:.12f} "
            f"H_rate={row.entropy_rate:.12f} bound={row.entropy_bound:.12f} "
            f"gap={row.entropy_gap:.3e} memoryless={row.memoryless}"
        )
        print(f"      {row.interpretation}")

    print("\n[D] Selected memoryless measurement solution")
    print(f"  source density d                          : {selection.source_density:.15f}")
    print(f"  MaxCal q(lambda)                          : {selection.maxcal_probability:.15f}")
    print(f"  stationary beta                           : {selection.stationary_beta:.12f}")
    print(f"  target beta=-log(eps0)                    : {target_beta:.12f}")
    print(f"  exp(-beta)                                : {selection.stationary_amplitude:.15f}")
    print(f"  exp(-2 beta)                              : {selection.stationary_probability:.15f}")

    print("\n[V] Verdict")
    print("  iid ensemble from Born + re-preparation    : YES, conditional")
    print("  agrees with MaxCal and large deviations    : YES")
    print("  memorylessness = maximum entropy rate      : YES")
    print("  re-preparation principle from CHO action   : NO")
    print("  CHO source question / mean derived         : NO")
    print("  Bayes/scoreboard credit moved              : NO")
    print("=" * 78)

    memoryless_rows = [row for row in control_rows if row.memoryless]
    correlated_rows = [row for row in control_rows if not row.memoryless]
    gaps = [row.entropy_gap for row in control_rows]

    assert abs(selection.born_event_probability - EPS0_SQ) < MATCH_TOL
    assert abs(selection.reprepared_conditional - selection.born_event_probability) < TOL
    assert selection.persistent_conditional > 1.0 - ZENO_TOL
    assert all(row.max_product_maxcal_error < TOL for row in route_rows)
    assert all(row.probability_sum_error < TOL for row in route_rows)
    assert all(row.mean_error < TOL for row in route_rows)
    assert len(memoryless_rows) == 1
    assert memoryless_rows[0].entropy_gap < ENTROPY_GAP_TOL
    assert all(row.entropy_gap > ENTROPY_GAP_TOL for row in correlated_rows)
    assert all(row.mean_error < TOL for row in control_rows)
    assert all(abs(row.measured_correlation - row.correlation) < TOL for row in control_rows)
    assert gaps == sorted(gaps)
    assert all(gaps[i] < gaps[i + 1] for i in range(len(gaps) - 1))
    assert abs(selection.maxcal_probability - EPS0_SQ) < MATCH_TOL
    assert abs(selection.stationary_beta - target_beta) < MATCH_TOL
    assert abs(selection.stationary_amplitude - EPS0) < MATCH_TOL
    assert abs(selection.stationary_probability - EPS0_SQ) < MATCH_TOL
    assert selection.independence_from_born_reprep
    assert selection.three_routes_agree
    assert selection.memoryless_maximizes_entropy_rate
    assert not selection.reprep_principle_derived_from_cho
    assert not selection.cho_source_question_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
