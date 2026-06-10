"""
F4-BREAKING VACUUM-RELAXATION GATE -- a physical origin for memorylessness.
================================================================================

The repeated-measurement gate showed that the independent Bernoulli(d) ensemble is
the Born path measure of a *memoryless* re-prepared projective measurement, and that
this measure coincides exactly with the maximum-caliber and large-deviation measures.
It reduced "why MaxCal" to the more physical "why memoryless re-preparation". This
gate climbs underneath that and asks where memorylessness itself comes from.

Memorylessness is not a free assumption: it is the complete-relaxation limit of a
standard open-system dynamics whose stable fixed point is the vacuum primitive
idempotent P (the vacuum orbit established elsewhere in the project). Model the
inter-probe dynamics as a depolarizing-toward-P channel

    C_r(rho) = r P + (1 - r) rho ,

a valid trace-preserving channel that attracts every state to the vacuum source P
with relaxation fraction r in [0, 1]. After a projective measurement of the
primitive question Q,

    yes-post-state overlap with Q : Tr(Q o Q)       = 1
    no-post-state overlap with Q  : Tr(Q o (I - Q)) = 0   (Lueders orthogonality)
    vacuum source overlap with Q  : Tr(P o Q)       = d = pi/432 ,

the relaxed conditional yes-probabilities are

    p(yes | prev=yes) = r d + (1 - r) * 1 = 1 - r (1 - d)
    p(yes | prev=no ) = r d + (1 - r) * 0 = r d ,

which is a stationary two-state Markov chain with lag-1 correlation 1 - r and
stationary mean d for every r > 0. At r = 1 (complete vacuum relaxation) the two
conditionals collapse to the same value d: the process is memoryless and the path
measure is exactly the iid Bernoulli(d) = MaxCal = Born product measure. At r = 0
(no relaxation) it freezes into the persistent / quantum-Zeno chain.

The relaxation fraction is fixed by a timescale separation. For an exponential
relaxation law r = 1 - exp(-Delta_t / tau) with inter-probe interval Delta_t and
relaxation time tau, memorylessness is the Born-Markov limit Delta_t >> tau (slow
probing of a fast-relaxing source), while the Zeno limit Delta_t << tau recovers
persistence. The path-entropy rate increases monotonically with Delta_t / tau and
saturates the iid bound H(d).

What this proves
----------------
Memorylessness has a standard physical origin: complete relaxation of the probed
state back to the vacuum source P. The vacuum primitive idempotent is the unique
relaxation fixed point, and only relaxation toward it (overlap exactly d = pi/432)
reproduces the correct mean -- relaxing toward Q or its complement gives mean 1 or 0.
The memoryless ensemble is the Delta_t >> tau (Born-Markov) limit of this dynamics,
and it agrees exactly with the MaxCal and Born product measures.

What this still does not prove
------------------------------
This does not derive the relaxation channel, its time tau, the probe interval
Delta_t, or the separation Delta_t >> tau from CHO/F4-breaking dynamics; nor does it
derive why the vacuum source question Q has overlap d = pi/432. It converts the
abstract "memorylessness" into the concrete, standard condition of vacuum-relaxation
timescale separation, with the vacuum as the attractor.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_vacuum_relaxation_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from epsilon_action_selection import trace_form
from f4_breaking_binary_projector_history_gate import (
    identity_idempotent,
    projector_complement,
)
from f4_breaking_born_geometry_gate import transition_projectors
from f4_breaking_maxcal_ensemble_gate import (
    binary_entropy,
    maxcal_lagrange_multiplier,
    maxcal_probability_from_multiplier,
)
from f4_breaking_repeated_measurement_gate import markov_entropy_rate
from f4_breaking_seed_op2 import EPS0, EPS0_SQ
from f4_breaking_source_stationarity_gate import beta_for_source, model_probability


TOL = 1e-12
MATCH_TOL = 1e-14
ORTHO_TOL = 1e-12
ENTROPY_GAP_TOL = 1e-9


@dataclass(frozen=True)
class RelaxationRow:
    relaxation_fraction: float
    yes_after_yes: float
    yes_after_no: float
    correlation: float
    stationary_mean: float
    mean_error: float
    entropy_rate: float
    entropy_bound: float
    entropy_gap: float
    memoryless: bool


@dataclass(frozen=True)
class FixedPointRow:
    label: str
    fixed_overlap: float
    stationary_mean: float
    target_error: float
    matches_vacuum_source: bool
    interpretation: str


@dataclass(frozen=True)
class TimescaleRow:
    interval_over_tau: float
    relaxation_fraction: float
    correlation: float
    entropy_rate: float
    entropy_gap: float
    regime: str


@dataclass(frozen=True)
class VacuumRelaxationSelection:
    source_overlap: float
    yes_post_overlap: float
    no_post_overlap: float
    source_self_overlap: float
    question_trace: float
    memoryless_yes_after_yes: float
    memoryless_yes_after_no: float
    memoryless_stationary_mean: float
    memoryless_entropy_gap: float
    maxcal_probability: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    memoryless_from_full_relaxation: bool
    vacuum_is_relaxation_fixed_point: bool
    timescale_separation_controls_memory: bool
    relaxation_time_derived_from_cho: bool
    probe_interval_derived_from_cho: bool


def measured_overlaps() -> tuple[float, float, float, float, float]:
    """Born overlaps from the real F4 projectors: source d, yes 1, no 0, self, Tr(Q)."""
    _psi, _phi, source_projector, question_projector = transition_projectors(EPS0)
    identity = identity_idempotent()
    source_overlap = float(trace_form(source_projector, question_projector))
    yes_post_overlap = float(trace_form(question_projector, question_projector))
    no_post_overlap = float(trace_form(question_projector, projector_complement(question_projector)))
    source_self_overlap = float(trace_form(source_projector, source_projector))
    question_trace = float(trace_form(question_projector, identity))
    return source_overlap, yes_post_overlap, no_post_overlap, source_self_overlap, question_trace


def relaxation_conditionals(
    source_overlap: float,
    yes_post_overlap: float,
    no_post_overlap: float,
    relaxation_fraction: float,
) -> tuple[float, float]:
    """Yes-probabilities after the depolarizing-toward-P channel C_r acts on each post-state."""
    yes_after_yes = relaxation_fraction * source_overlap + (1.0 - relaxation_fraction) * yes_post_overlap
    yes_after_no = relaxation_fraction * source_overlap + (1.0 - relaxation_fraction) * no_post_overlap
    return yes_after_yes, yes_after_no


def stationary_yes_probability(yes_after_yes: float, yes_after_no: float) -> float:
    forward = yes_after_no
    backward = 1.0 - yes_after_yes
    if forward + backward == 0.0:
        return float("nan")
    return forward / (forward + backward)


def relaxation_rows() -> tuple[RelaxationRow, ...]:
    source_overlap, yes_post_overlap, no_post_overlap, _self, _trace = measured_overlaps()
    density = EPS0_SQ
    bound = binary_entropy(density)
    rows = []
    for relaxation_fraction in (1.0, 0.8, 0.5, 0.2, 0.05):
        yes_after_yes, yes_after_no = relaxation_conditionals(
            source_overlap, yes_post_overlap, no_post_overlap, relaxation_fraction
        )
        correlation = 1.0 - relaxation_fraction
        rate, _forward, _backward = markov_entropy_rate(density, correlation)
        stationary_mean = stationary_yes_probability(yes_after_yes, yes_after_no)
        rows.append(
            RelaxationRow(
                relaxation_fraction=float(relaxation_fraction),
                yes_after_yes=float(yes_after_yes),
                yes_after_no=float(yes_after_no),
                correlation=float(correlation),
                stationary_mean=float(stationary_mean),
                mean_error=abs(stationary_mean - density),
                entropy_rate=float(rate),
                entropy_bound=float(bound),
                entropy_gap=float(bound - rate),
                memoryless=relaxation_fraction >= 1.0 - TOL,
            )
        )
    return tuple(rows)


def fixed_point_rows() -> tuple[FixedPointRow, ...]:
    """Full relaxation (r=1) toward different attractors; only the vacuum source gives mean d."""
    source_overlap, yes_post_overlap, no_post_overlap, _self, _trace = measured_overlaps()
    density = EPS0_SQ
    specs = (
        ("vacuum source P (overlap d)", source_overlap, "relaxes to the vacuum primitive idempotent: mean d=pi/432, correct iid source"),
        ("question ray Q (overlap 1)", yes_post_overlap, "relaxes to the measured ray: absorbing 'always yes', mean 1, wrong"),
        ("complement Q_perp (overlap 0)", no_post_overlap, "relaxes to the orthogonal effect: absorbing 'always no', mean 0, wrong"),
    )
    rows = []
    for label, fixed_overlap, interpretation in specs:
        # full relaxation toward a state of overlap f gives iid Bernoulli(f): mean f
        yes_after_yes, yes_after_no = relaxation_conditionals(fixed_overlap, yes_post_overlap, no_post_overlap, 1.0)
        stationary_mean = stationary_yes_probability(yes_after_yes, yes_after_no)
        rows.append(
            FixedPointRow(
                label=label,
                fixed_overlap=float(fixed_overlap),
                stationary_mean=float(stationary_mean),
                target_error=abs(stationary_mean - density),
                matches_vacuum_source=abs(stationary_mean - density) < TOL,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def timescale_rows() -> tuple[TimescaleRow, ...]:
    """Exponential relaxation r = 1 - exp(-Delta_t/tau): memoryless emerges as Delta_t/tau -> inf."""
    density = EPS0_SQ
    bound = binary_entropy(density)
    specs = (
        (0.05, "Delta_t << tau: near-Zeno persistence (fast probing)"),
        (0.2, "sub-relaxation probing: strongly correlated"),
        (0.5, "comparable timescales: partially relaxed"),
        (1.0, "one relaxation time: moderately relaxed"),
        (2.0, "Delta_t > tau: well relaxed"),
        (5.0, "Delta_t >> tau: Born-Markov memoryless limit"),
    )
    rows = []
    for interval_over_tau, regime in specs:
        relaxation_fraction = 1.0 - math.exp(-interval_over_tau)
        correlation = 1.0 - relaxation_fraction
        rate, _forward, _backward = markov_entropy_rate(density, correlation)
        rows.append(
            TimescaleRow(
                interval_over_tau=float(interval_over_tau),
                relaxation_fraction=float(relaxation_fraction),
                correlation=float(correlation),
                entropy_rate=float(rate),
                entropy_gap=float(bound - rate),
                regime=regime,
            )
        )
    return tuple(rows)


def vacuum_relaxation_selection() -> VacuumRelaxationSelection:
    source_overlap, yes_post_overlap, no_post_overlap, source_self_overlap, question_trace = measured_overlaps()
    density = EPS0_SQ
    lagrange_multiplier = maxcal_lagrange_multiplier(density)
    beta = beta_for_source(density, power=2)
    yes_after_yes, yes_after_no = relaxation_conditionals(source_overlap, yes_post_overlap, no_post_overlap, 1.0)
    memoryless_mean = stationary_yes_probability(yes_after_yes, yes_after_no)
    rate, _forward, _backward = markov_entropy_rate(density, 0.0)
    bound = binary_entropy(density)
    timescale = timescale_rows()
    fixed_points = fixed_point_rows()
    vacuum_rows = [row for row in fixed_points if "vacuum" in row.label]
    return VacuumRelaxationSelection(
        source_overlap=float(source_overlap),
        yes_post_overlap=float(yes_post_overlap),
        no_post_overlap=float(no_post_overlap),
        source_self_overlap=float(source_self_overlap),
        question_trace=float(question_trace),
        memoryless_yes_after_yes=float(yes_after_yes),
        memoryless_yes_after_no=float(yes_after_no),
        memoryless_stationary_mean=float(memoryless_mean),
        memoryless_entropy_gap=float(bound - rate),
        maxcal_probability=float(maxcal_probability_from_multiplier(lagrange_multiplier)),
        stationary_beta=float(beta),
        stationary_amplitude=float(math.exp(-beta)),
        stationary_probability=float(model_probability(beta, power=2)),
        memoryless_from_full_relaxation=(
            abs(yes_after_yes - yes_after_no) < TOL and abs(memoryless_mean - density) < TOL
        ),
        vacuum_is_relaxation_fixed_point=(
            len(vacuum_rows) == 1 and vacuum_rows[0].matches_vacuum_source
        ),
        timescale_separation_controls_memory=(
            timescale[-1].entropy_gap < timescale[0].entropy_gap
            and all(timescale[i].entropy_gap > timescale[i + 1].entropy_gap for i in range(len(timescale) - 1))
        ),
        relaxation_time_derived_from_cho=False,
        probe_interval_derived_from_cho=False,
    )


def main() -> bool:
    relax_rows = relaxation_rows()
    fixed_points = fixed_point_rows()
    timescale = timescale_rows()
    selection = vacuum_relaxation_selection()
    target_beta = -math.log(EPS0)

    print("=" * 78)
    print("F4-BREAKING VACUUM-RELAXATION GATE")
    print("Does memorylessness come from complete relaxation to the vacuum source?")
    print("=" * 78)

    print("\n[A] Measured Born overlaps and the depolarizing-toward-P channel")
    print(f"  vacuum source overlap  Tr(P o Q)          : {selection.source_overlap:.15f}")
    print(f"  pi/432                                    : {EPS0_SQ:.15f}")
    print(f"  yes-post overlap       Tr(Q o Q)          : {selection.yes_post_overlap:.15f}")
    print(f"  no-post  overlap       Tr(Q o (I-Q))      : {selection.no_post_overlap:.2e}  (Lueders orthogonality)")
    print(f"  source self-overlap    Tr(P o P)          : {selection.source_self_overlap:.15f}")
    print(f"  question trace         Tr(Q)              : {selection.question_trace:.15f}  (channel trace-preserving)")
    print("  C_r(rho)=r P+(1-r) rho relaxes every post-state toward the vacuum source P.")

    print("\n[B] Relaxation fraction r -> stationary two-state chain (mean d preserved)")
    for row in relax_rows:
        print(
            f"  r={row.relaxation_fraction:.2f} "
            f"p(yes|yes)={row.yes_after_yes:.12f} p(yes|no)={row.yes_after_no:.12f} "
            f"corr={row.correlation:.2f} mean={row.stationary_mean:.12f} "
            f"H_rate={row.entropy_rate:.12f} gap={row.entropy_gap:.3e} memoryless={row.memoryless}"
        )
    print("  r=1 collapses p(yes|yes)=p(yes|no)=d: memoryless iid Bernoulli(d).")

    print("\n[C] Vacuum specificity: full relaxation toward different attractors")
    for row in fixed_points:
        print(
            f"  {row.label:<31} overlap={row.fixed_overlap:.12f} "
            f"mean={row.stationary_mean:.12f} err_vs_d={row.target_error:.3e} "
            f"matches_d={row.matches_vacuum_source}"
        )
        print(f"      {row.interpretation}")

    print("\n[D] Timescale separation r=1-exp(-Delta_t/tau): memoryless as Delta_t/tau -> inf")
    for row in timescale:
        print(
            f"  Delta_t/tau={row.interval_over_tau:<5} r={row.relaxation_fraction:.6f} "
            f"corr={row.correlation:.6f} H_rate={row.entropy_rate:.12f} gap={row.entropy_gap:.3e}"
        )
        print(f"      {row.regime}")

    print("\n  Memoryless anchor (r=1):")
    print(f"  stationary mean                           : {selection.memoryless_stationary_mean:.15f}")
    print(f"  MaxCal q(lambda)                          : {selection.maxcal_probability:.15f}")
    print(f"  stationary beta                           : {selection.stationary_beta:.12f}")
    print(f"  target beta=-log(eps0)                    : {target_beta:.12f}")
    print(f"  exp(-beta)                                : {selection.stationary_amplitude:.15f}")
    print(f"  exp(-2 beta)                              : {selection.stationary_probability:.15f}")

    print("\n[V] Verdict")
    print("  memorylessness = complete vacuum relaxation : YES, conditional")
    print("  vacuum primitive idempotent is fixed point  : YES")
    print("  memoryless = Born-Markov (Delta_t >> tau)    : YES")
    print("  relaxation time tau from CHO action         : NO")
    print("  probe interval / separation from CHO        : NO")
    print("  Bayes/scoreboard credit moved               : NO")
    print("=" * 78)

    density = EPS0_SQ
    bound = binary_entropy(density)

    # [A] overlaps from the real F4 projectors
    assert abs(selection.source_overlap - EPS0_SQ) < MATCH_TOL
    assert abs(selection.yes_post_overlap - 1.0) < TOL
    assert abs(selection.no_post_overlap) < ORTHO_TOL
    assert abs(selection.source_self_overlap - 1.0) < TOL
    assert abs(selection.question_trace - 1.0) < TOL

    # [B] every relaxation fraction preserves the marginal d; only r=1 is memoryless
    memoryless_relax = [row for row in relax_rows if row.memoryless]
    correlated_relax = [row for row in relax_rows if not row.memoryless]
    assert all(row.mean_error < TOL for row in relax_rows)
    assert all(abs(row.correlation - (1.0 - row.relaxation_fraction)) < TOL for row in relax_rows)
    assert len(memoryless_relax) == 1
    assert abs(memoryless_relax[0].yes_after_yes - density) < TOL
    assert abs(memoryless_relax[0].yes_after_no - density) < TOL
    assert memoryless_relax[0].entropy_gap < ENTROPY_GAP_TOL
    assert all(row.entropy_gap > ENTROPY_GAP_TOL for row in correlated_relax)
    ordered_by_r = sorted(relax_rows, key=lambda row: row.relaxation_fraction)
    gaps_desc = [row.entropy_gap for row in ordered_by_r]
    assert all(gaps_desc[i] > gaps_desc[i + 1] for i in range(len(gaps_desc) - 1))

    # [C] only relaxation toward the vacuum source (overlap d) gives the correct mean
    vacuum_rows = [row for row in fixed_points if row.matches_vacuum_source]
    assert len(vacuum_rows) == 1
    assert "vacuum" in vacuum_rows[0].label
    assert abs(vacuum_rows[0].stationary_mean - density) < TOL
    assert all(abs(row.stationary_mean - row.fixed_overlap) < TOL for row in fixed_points)
    assert any(abs(row.stationary_mean - 1.0) < TOL for row in fixed_points)
    assert any(abs(row.stationary_mean - 0.0) < TOL for row in fixed_points)

    # [D] entropy rate increases monotonically with Delta_t/tau and saturates H(d)
    rates = [row.entropy_rate for row in timescale]
    gaps = [row.entropy_gap for row in timescale]
    assert all(rates[i] < rates[i + 1] for i in range(len(rates) - 1))
    assert all(gaps[i] > gaps[i + 1] for i in range(len(gaps) - 1))
    assert timescale[-1].entropy_gap < timescale[0].entropy_gap
    assert all(row.entropy_rate <= bound + TOL for row in timescale)

    # anchors and honesty flags
    assert abs(selection.maxcal_probability - EPS0_SQ) < MATCH_TOL
    assert abs(selection.stationary_beta - target_beta) < MATCH_TOL
    assert abs(selection.stationary_amplitude - EPS0) < MATCH_TOL
    assert abs(selection.stationary_probability - EPS0_SQ) < MATCH_TOL
    assert selection.memoryless_from_full_relaxation
    assert selection.vacuum_is_relaxation_fixed_point
    assert selection.timescale_separation_controls_memory
    assert not selection.relaxation_time_derived_from_cho
    assert not selection.probe_interval_derived_from_cho
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
