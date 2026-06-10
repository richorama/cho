"""
F4-BREAKING SOURCE STATIONARITY GATE -- when does beta become stationary?
============================================================================

The projective Born geometry gate hardened the local square-root map:

    Tr(P o Q) = |<psi|phi>|^2.

The remaining dynamical gap is sharper: why should the selected WZ/carrier
density source this projective transition channel, and why should beta be the
stationary coordinate?

This gate tests the next conditional rung. If the selected source density

    d = pi/432

is coupled to the projective transition probability

    q(beta) = exp(-2 beta),

then the Bernoulli/KL stationarity equation is

    d/dbeta CE(d, q(beta)) = 2 (d - q) / (1 - q) = 0,

so q=d uniquely and beta=-0.5 log(d)=-log(eps0). The wrong couplings miss:
treating exp(-beta) itself as the probability, omitting the Berry pi, or using
the k=2 density.

What this proves
----------------
Given the selected level-one WZ density and a source-channel coupling to the
projective probability, beta stationarity is no longer a free fit. The stationarity
equation outputs exp(-2 beta)=pi/432 and hence exp(-beta)=eps0.

What this still does not prove
------------------------------
This still does not derive the CHO action term that supplies the Bernoulli/KL
source coupling. It proves the conditional stationarity equation once that
coupling is granted. The live bridge is now the origin of the source-channel
coupling itself.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_source_stationarity_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from f4_breaking_born_beta_map_gate import born_selection, gibbs_ratios
from f4_breaking_born_geometry_gate import frame_probability_witness
from f4_breaking_primitive_level_gate import CARRIER_DIM, half_turn_density
from f4_breaking_seed_op2 import EPS0, EPS0_SQ


TOL = 1e-14
DERIV_TOL = 1e-12
MISS_TOL = 1e-3


@dataclass(frozen=True)
class SourceStationarityRow:
    label: str
    source_density: float
    model_power: int
    beta: float
    amplitude: float
    probability: float
    derivative: float
    curvature: float
    kl_value: float
    target_error: float
    matches_target: bool
    interpretation: str


@dataclass(frozen=True)
class SourceSelection:
    source_density: float
    source_probability_from_geometry: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    stationary_ratios: tuple[float, float, float]
    stationarity_equation_derived: bool
    source_coupling_derived: bool


def model_probability(beta: float, power: int = 2) -> float:
    return math.exp(-float(power) * beta)


def bernoulli_kl(source_density: float, probability: float) -> float:
    if not (0.0 < source_density < 1.0 and 0.0 < probability < 1.0):
        raise ValueError("source and probability must lie in (0, 1)")
    return (
        source_density * math.log(source_density / probability)
        + (1.0 - source_density) * math.log((1.0 - source_density) / (1.0 - probability))
    )


def source_stationarity_derivative(beta: float, source_density: float, power: int = 2) -> float:
    probability = model_probability(beta, power)
    return float(power) * (source_density - probability) / (1.0 - probability)


def source_stationarity_curvature(beta: float, source_density: float, power: int = 2) -> float:
    probability = model_probability(beta, power)
    return float(power * power) * probability * (1.0 - source_density) / ((1.0 - probability) ** 2)


def beta_for_source(source_density: float, power: int = 2) -> float:
    if not (0.0 < source_density < 1.0):
        raise ValueError("source_density must lie in (0, 1)")
    return -math.log(source_density) / float(power)


def stationarity_rows() -> tuple[SourceStationarityRow, ...]:
    selected = born_selection()
    density = selected.selected_density
    candidates = (
        (
            "projective probability source",
            density,
            2,
            "correct: source couples to q=exp(-2 beta)=|amplitude|^2",
        ),
        (
            "amplitude-as-probability source",
            density,
            1,
            "wrong: source couples to exp(-beta) as if amplitude were probability",
        ),
        (
            "state-count-only source",
            1.0 / CARRIER_DIM,
            2,
            "wrong: omits the Berry/WZ pi in the source density",
        ),
        (
            "level-two source",
            half_turn_density(2.0),
            2,
            "wrong carrier: k=2 gives a higher-state sector source",
        ),
    )
    rows = []
    for label, source_density, power, interpretation in candidates:
        beta = beta_for_source(source_density, power)
        amplitude = math.exp(-beta)
        probability = model_probability(beta, power)
        derivative = source_stationarity_derivative(beta, source_density, power)
        curvature = source_stationarity_curvature(beta, source_density, power)
        kl_value = bernoulli_kl(source_density, probability)
        ratio2 = amplitude * amplitude
        rows.append(
            SourceStationarityRow(
                label=label,
                source_density=float(source_density),
                model_power=int(power),
                beta=float(beta),
                amplitude=float(amplitude),
                probability=float(probability),
                derivative=float(derivative),
                curvature=float(curvature),
                kl_value=float(kl_value),
                target_error=abs(ratio2 - EPS0_SQ),
                matches_target=abs(ratio2 - EPS0_SQ) < TOL,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def source_selection() -> SourceSelection:
    selected = born_selection()
    geometry = frame_probability_witness()
    density = selected.selected_density
    beta = beta_for_source(density, power=2)
    amplitude = math.exp(-beta)
    probability = model_probability(beta, power=2)
    return SourceSelection(
        source_density=float(density),
        source_probability_from_geometry=float(geometry.target_probability),
        stationary_beta=float(beta),
        stationary_amplitude=float(amplitude),
        stationary_probability=float(probability),
        stationary_ratios=tuple(float(x) for x in gibbs_ratios(beta)),
        stationarity_equation_derived=True,
        source_coupling_derived=False,
    )


def main() -> bool:
    rows = stationarity_rows()
    selection = source_selection()
    target_beta = -math.log(EPS0)

    print("=" * 78)
    print("F4-BREAKING SOURCE STATIONARITY GATE")
    print("If the WZ density sources the projective probability, does beta stationarity follow?")
    print("=" * 78)

    print("\n[A] Bernoulli/KL source coupling")
    print("    CE(d,q) with q(beta)=exp(-p beta); stationarity gives q=d")
    for row in rows:
        print(
            f"  {row.label:<31} p={row.model_power} source={row.source_density:.12f} "
            f"beta={row.beta:.12f} amp={row.amplitude:.12f} q={row.probability:.12f} "
            f"dF={row.derivative:+.2e} d2F={row.curvature:.3f} "
            f"KL={row.kl_value:.2e} |amp^2-target|={row.target_error:.3e} "
            f"match={row.matches_target}"
        )
        print(f"      {row.interpretation}")

    print("\n[B] Selected stationary solution")
    print(f"  WZ source density d                     : {selection.source_density:.15f}")
    print(f"  projective geometry Tr(PQ)              : {selection.source_probability_from_geometry:.15f}")
    print(f"  stationary beta                         : {selection.stationary_beta:.12f}")
    print(f"  target beta=-log(eps0)                  : {target_beta:.12f}")
    print(f"  exp(-beta)                              : {selection.stationary_amplitude:.15f}")
    print(f"  eps0                                    : {EPS0:.15f}")
    print(f"  exp(-2 beta)                            : {selection.stationary_probability:.15f}")
    print(f"  pi/432                                  : {EPS0_SQ:.15f}")
    print(
        "  Gibbs/source ratios                      : "
        f"({selection.stationary_ratios[0]:.9f}, "
        f"{selection.stationary_ratios[1]:.9f}, "
        f"{selection.stationary_ratios[2]:.9f})"
    )

    print("\n[V] Verdict")
    print("  source-coupled stationarity gives beta   : YES, conditional")
    print("  beta=-log(eps0) follows from q=d         : YES")
    print("  source-channel coupling derived          : NO")
    print("  remaining object                         : derive the CHO term that supplies CE(d,q)")
    print("  Bayes/scoreboard credit moved            : NO")
    print("=" * 78)

    matching = [row for row in rows if row.matches_target]
    misses = [row for row in rows if not row.matches_target]
    assert len(matching) == 1
    assert matching[0].label == "projective probability source"
    assert all(abs(row.derivative) < DERIV_TOL for row in rows)
    assert all(row.curvature > 0.0 for row in rows)
    assert all(abs(row.kl_value) < TOL for row in rows)
    assert all(row.target_error > MISS_TOL for row in misses)
    assert abs(selection.source_density - EPS0_SQ) < TOL
    assert abs(selection.source_probability_from_geometry - EPS0_SQ) < TOL
    assert abs(selection.stationary_beta - target_beta) < TOL
    assert abs(selection.stationary_amplitude - EPS0) < TOL
    assert abs(selection.stationary_probability - EPS0_SQ) < TOL
    assert abs(selection.stationary_ratios[1] - EPS0) < TOL
    assert abs(selection.stationary_ratios[2] - EPS0_SQ) < TOL
    assert selection.stationarity_equation_derived
    assert not selection.source_coupling_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)