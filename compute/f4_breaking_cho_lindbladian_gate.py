"""
F4-BREAKING CHO LINDBLADIAN GATE -- a generator for the relaxation channel.
================================================================================

The vacuum-relaxation gate modelled the inter-probe dynamics as an *abstract*
depolarizing-toward-P channel C_r(rho) = r P + (1 - r) rho and showed memorylessness
is its complete-relaxation (r -> 1) / Born-Markov limit. That channel was assumed,
not generated. This gate climbs underneath it and writes down an actual generator
of dynamics whose finite-time propagator IS that channel.

Take the standard GKSL (Lindblad) dissipator that damps every basis direction into
the vacuum ray p (P = |p><p|), with jump operators

    L_k = sqrt(gamma) |p><e_k|   (amplitude damping into the vacuum) ,

so that

    L(rho) = sum_k ( L_k rho L_k^dag - 1/2 { L_k^dag L_k, rho } )
           = gamma ( Tr(rho) P - rho ) .

This is a genuine completely-positive trace-preserving (CPTP) semigroup generator.
Its finite-time propagator is exactly the depolarizing-toward-P channel,

    exp(t L)(rho) = e^{-gamma t} rho + (1 - e^{-gamma t}) P = C_{r(t)}(rho),
    r(t) = 1 - exp(-gamma t),   tau = 1 / gamma ,

with a UNIQUE steady state P (the vacuum primitive idempotent) and spectral gap
gamma. Feeding r(t) into the vacuum-relaxation conditionals reproduces the mean
d = pi/432 for every probe interval and the memoryless Born-Markov limit as
gamma * Delta_t -> infinity.

The dynamics is verified on a faithful two-level (qubit) representation of the
{vacuum P, question Q} effect statistics: the relevant repeated yes/no readout
lives on the qubit spanned by the two rays, where |<p|q>|^2 = Tr(P o Q) = d exactly
(cross-checked against the Jordan trace form). The matrix exponential is computed
independently (scaling-and-squaring Taylor series, no SciPy) so the semigroup match
is a real verification, not an identity.

What this proves
----------------
The relaxation channel assumed by the vacuum-relaxation gate is the exact CPTP
semigroup of a concrete Lindblad generator whose unique steady state is the vacuum
P and whose relaxation is exponential with time tau = 1/gamma. Controls fail
cleanly: a unitary-only generator does not relax (degenerate steady manifold, zero
spectral gap), a wrong-target dissipator relaxes to Q (mean -> 1), and a
dephasing-only dissipator relaxes to a mixed non-vacuum state (mean != d).

What this still does not prove
------------------------------
This does not derive the jump rate gamma (hence tau), the vacuum-damping jump
operators, or the probe interval Delta_t from the CHO/F4-breaking action; nor does
it derive why the vacuum source question Q has overlap d = pi/432. It reduces "why
the depolarizing-toward-P relaxation channel" to "why this Lindblad jump structure
and rate from CHO dynamics".

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_cho_lindbladian_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from f4_breaking_seed_op2 import EPS0, EPS0_SQ
from f4_breaking_source_stationarity_gate import beta_for_source, model_probability
from f4_breaking_vacuum_relaxation_gate import (
    measured_overlaps,
    relaxation_conditionals,
    stationary_yes_probability,
)


TOL = 1e-12
MATCH_TOL = 1e-13
GENERATOR_TOL = 1e-12
CHOI_TOL = 1e-12
SEMIGROUP_TOL = 1e-9
GAMMA = 1.0


@dataclass(frozen=True)
class SemigroupRow:
    gamma: float
    time: float
    relaxation_fraction: float
    semigroup_error: float
    choi_min_eigenvalue: float
    trace_error: float


@dataclass(frozen=True)
class ConditionalRow:
    interval: float
    relaxation_fraction: float
    yes_after_yes: float
    yes_after_no: float
    stationary_mean: float
    mean_error: float
    memoryless_gap: float


@dataclass(frozen=True)
class GeneratorControlRow:
    label: str
    steady_manifold_dim: int
    spectral_gap: float
    steady_mean: float
    unique_vacuum_steady_state: bool
    reaches_vacuum: bool
    interpretation: str


@dataclass(frozen=True)
class LindbladianSelection:
    qubit_overlap: float
    jordan_overlap: float
    generator_identity_error: float
    steady_manifold_dim: int
    spectral_gap: float
    steady_overlap_with_vacuum: float
    relaxation_time: float
    memoryless_mean: float
    stationary_beta: float
    stationary_amplitude: float
    stationary_probability: float
    relaxation_is_gksl_semigroup: bool
    vacuum_is_unique_steady_state: bool
    relaxation_is_exponential: bool
    jump_rate_derived_from_cho: bool
    jump_operators_derived_from_cho: bool
    source_overlap_derived_from_cho: bool


def _vec(matrix: np.ndarray) -> np.ndarray:
    return matrix.flatten()


def _unvec(vector: np.ndarray) -> np.ndarray:
    return vector.reshape(2, 2)


def _matrix_exponential(matrix: np.ndarray, taylor_terms: int = 32) -> np.ndarray:
    """Independent scaling-and-squaring Taylor matrix exponential (no SciPy)."""
    frobenius_norm = float(np.linalg.norm(matrix))
    squarings = 0
    if frobenius_norm > 0.5:
        squarings = int(math.ceil(math.log2(frobenius_norm / 0.5)))
    scaled = matrix / (2 ** squarings)
    dimension = matrix.shape[0]
    result = np.eye(dimension, dtype=complex)
    term = np.eye(dimension, dtype=complex)
    for order in range(1, taylor_terms + 1):
        term = term @ scaled / order
        result = result + term
    for _ in range(squarings):
        result = result @ result
    return result


def vacuum_ray() -> np.ndarray:
    return np.array([1.0, 0.0], dtype=complex)


def question_ray(density: float) -> np.ndarray:
    return np.array([math.sqrt(density), math.sqrt(1.0 - density)], dtype=complex)


def projector(ray: np.ndarray) -> np.ndarray:
    return np.outer(ray, ray.conj())


def vacuum_jump_operators(gamma: float, target: np.ndarray) -> tuple[np.ndarray, ...]:
    """L_k = sqrt(gamma) |target><e_k|: damp every basis direction into the target ray."""
    basis = (np.array([1.0, 0.0], dtype=complex), np.array([0.0, 1.0], dtype=complex))
    return tuple(math.sqrt(gamma) * np.outer(target, e_k.conj()) for e_k in basis)


def lindblad_generator(jump_operators: tuple[np.ndarray, ...], hamiltonian: np.ndarray | None = None):
    """Return the GKSL generator L(rho) for the given jumps and optional Hamiltonian."""

    def generator(rho: np.ndarray) -> np.ndarray:
        result = np.zeros_like(rho, dtype=complex)
        if hamiltonian is not None:
            result = result - 1j * (hamiltonian @ rho - rho @ hamiltonian)
        for jump in jump_operators:
            jump_dag = jump.conj().T
            result = result + jump @ rho @ jump_dag
            result = result - 0.5 * (jump_dag @ jump @ rho + rho @ jump_dag @ jump)
        return result

    return generator


def superoperator(generator) -> np.ndarray:
    """4x4 matrix of the generator acting on vectorized 2x2 matrices."""
    columns = []
    for row in range(2):
        for col in range(2):
            basis_matrix = np.zeros((2, 2), dtype=complex)
            basis_matrix[row, col] = 1.0
            columns.append(_vec(generator(basis_matrix)))
    return np.array(columns).T


def steady_states(generator) -> tuple[int, float, np.ndarray | None]:
    """Return (steady-manifold dimension, spectral gap, unique steady state or None)."""
    super_matrix = superoperator(generator)
    eigenvalues, eigenvectors = np.linalg.eig(super_matrix)
    magnitudes = np.abs(eigenvalues)
    zero_mask = magnitudes < 1e-9
    manifold_dim = int(np.count_nonzero(zero_mask))
    # spectral gap = slowest decay rate among non-steady modes (purely imaginary
    # eigenvalues oscillate without relaxing and contribute zero decay).
    decay_rates = -eigenvalues.real
    nonsteady = decay_rates[~zero_mask]
    spectral_gap = float(np.min(nonsteady)) if nonsteady.size else 0.0
    steady = None
    if manifold_dim == 1:
        index = int(np.argmin(magnitudes))
        raw = _unvec(eigenvectors[:, index])
        raw = 0.5 * (raw + raw.conj().T)
        trace = np.trace(raw)
        if abs(trace) > 1e-12:
            steady = raw / trace
    return manifold_dim, spectral_gap, steady


def depolarizing_channel(relaxation_fraction: float, vacuum_projector: np.ndarray, rho: np.ndarray) -> np.ndarray:
    return relaxation_fraction * vacuum_projector + (1.0 - relaxation_fraction) * rho


def choi_matrix(relaxation_fraction: float, vacuum_projector: np.ndarray) -> np.ndarray:
    choi = np.zeros((4, 4), dtype=complex)
    for row in range(2):
        for col in range(2):
            basis_matrix = np.zeros((2, 2), dtype=complex)
            basis_matrix[row, col] = 1.0
            image = depolarizing_channel(relaxation_fraction, vacuum_projector, basis_matrix)
            choi += np.kron(basis_matrix, image)
    return choi


def semigroup_rows() -> tuple[SemigroupRow, ...]:
    density = EPS0_SQ
    vacuum_projector = projector(vacuum_ray())
    rho_probe = projector(question_ray(density))
    rows = []
    for gamma in (GAMMA, 2.0):
        generator = lindblad_generator(vacuum_jump_operators(gamma, vacuum_ray()))
        super_matrix = superoperator(generator)
        for time in (0.25, 0.5, 1.0, 2.0, 5.0):
            propagator = _matrix_exponential(time * super_matrix)
            evolved = _unvec(propagator @ _vec(rho_probe))
            relaxation_fraction = 1.0 - math.exp(-gamma * time)
            channel_image = depolarizing_channel(relaxation_fraction, vacuum_projector, rho_probe)
            semigroup_error = float(np.linalg.norm(evolved - channel_image))
            choi = choi_matrix(relaxation_fraction, vacuum_projector)
            choi_eigenvalues = np.linalg.eigvalsh(0.5 * (choi + choi.conj().T))
            rows.append(
                SemigroupRow(
                    gamma=float(gamma),
                    time=float(time),
                    relaxation_fraction=float(relaxation_fraction),
                    semigroup_error=semigroup_error,
                    choi_min_eigenvalue=float(np.min(choi_eigenvalues.real)),
                    trace_error=abs(float(np.trace(evolved).real) - 1.0),
                )
            )
    return tuple(rows)


def conditional_rows() -> tuple[ConditionalRow, ...]:
    density = EPS0_SQ
    source_overlap, yes_post_overlap, no_post_overlap, _self, _trace = measured_overlaps()
    bound = -(density * math.log(density) + (1.0 - density) * math.log(1.0 - density))
    rows = []
    for interval in (0.25, 0.5, 1.0, 2.0, 5.0, 10.0):
        relaxation_fraction = 1.0 - math.exp(-GAMMA * interval)
        yes_after_yes, yes_after_no = relaxation_conditionals(
            source_overlap, yes_post_overlap, no_post_overlap, relaxation_fraction
        )
        stationary_mean = stationary_yes_probability(yes_after_yes, yes_after_no)
        forward = yes_after_no
        backward = 1.0 - yes_after_yes
        stationary_one = forward / (forward + backward)
        stationary_zero = 1.0 - stationary_one
        rate = stationary_zero * _binary_entropy(yes_after_no) + stationary_one * _binary_entropy(yes_after_yes)
        rows.append(
            ConditionalRow(
                interval=float(interval),
                relaxation_fraction=float(relaxation_fraction),
                yes_after_yes=float(yes_after_yes),
                yes_after_no=float(yes_after_no),
                stationary_mean=float(stationary_mean),
                mean_error=abs(stationary_mean - density),
                memoryless_gap=float(bound - rate),
            )
        )
    return tuple(rows)


def _binary_entropy(probability: float) -> float:
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return -(probability * math.log(probability) + (1.0 - probability) * math.log(1.0 - probability))


def generator_control_rows() -> tuple[GeneratorControlRow, ...]:
    density = EPS0_SQ
    vacuum = vacuum_ray()
    question = question_ray(density)
    question_projector = projector(question)
    rows = []

    # correct: amplitude damping into the vacuum
    vacuum_generator = lindblad_generator(vacuum_jump_operators(GAMMA, vacuum))
    rows.append(_build_control_row(
        "vacuum damping (L_k=|p><e_k|)", vacuum_generator, question_projector,
        "relaxes to the unique vacuum primitive idempotent P: steady mean d=pi/432, correct",
    ))

    # wrong target: damp into the question ray Q
    question_generator = lindblad_generator(vacuum_jump_operators(GAMMA, question))
    rows.append(_build_control_row(
        "wrong-target damping (-> Q)", question_generator, question_projector,
        "relaxes to the measured ray Q: steady mean 1, wrong attractor",
    ))

    # unitary only: no dissipation
    hamiltonian = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    unitary_generator = lindblad_generator((), hamiltonian=hamiltonian)
    rows.append(_build_control_row(
        "unitary only (-i[H,rho])", unitary_generator, question_projector,
        "no dissipation: degenerate steady manifold, zero spectral gap, never relaxes",
    ))

    # dephasing only: kills coherences, not amplitude
    dephasing_jump = (math.sqrt(GAMMA) * np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex),)
    dephasing_generator = lindblad_generator(dephasing_jump)
    rows.append(_build_control_row(
        "dephasing only (L=Z)", dephasing_generator, question_projector,
        "kills coherences only: degenerate diagonal steady manifold, never reaches pure vacuum",
    ))
    return tuple(rows)


def _build_control_row(label, generator, question_projector, interpretation) -> GeneratorControlRow:
    density = EPS0_SQ
    vacuum_projector = projector(vacuum_ray())
    manifold_dim, spectral_gap, steady = steady_states(generator)
    if steady is not None:
        steady_mean = float(np.trace(question_projector @ steady).real)
        overlap_with_vacuum = float(np.trace(vacuum_projector @ steady).real)
        reaches_vacuum = abs(overlap_with_vacuum - 1.0) < 1e-9
        unique_vacuum = manifold_dim == 1 and reaches_vacuum and abs(steady_mean - density) < 1e-9
    else:
        steady_mean = float("nan")
        reaches_vacuum = False
        unique_vacuum = False
    return GeneratorControlRow(
        label=label,
        steady_manifold_dim=int(manifold_dim),
        spectral_gap=float(spectral_gap),
        steady_mean=float(steady_mean),
        unique_vacuum_steady_state=bool(unique_vacuum),
        reaches_vacuum=bool(reaches_vacuum),
        interpretation=interpretation,
    )


def survival_composition_error() -> float:
    """Survival fractions multiply: (1-r(s))(1-r(t)) = 1-r(s+t)."""
    worst = 0.0
    for first in (0.3, 0.7, 1.3):
        for second in (0.2, 0.9, 2.1):
            survive_first = math.exp(-GAMMA * first)
            survive_second = math.exp(-GAMMA * second)
            survive_total = math.exp(-GAMMA * (first + second))
            worst = max(worst, abs(survive_first * survive_second - survive_total))
    return worst


def lindbladian_selection() -> LindbladianSelection:
    density = EPS0_SQ
    vacuum = vacuum_ray()
    vacuum_projector = projector(vacuum)
    question = question_ray(density)
    jordan_overlap = measured_overlaps()[0]
    qubit_overlap = float(np.trace(vacuum_projector @ projector(question)).real)

    generator = lindblad_generator(vacuum_jump_operators(GAMMA, vacuum))
    rng = np.random.default_rng(20260610)
    identity_error = 0.0
    for _ in range(6):
        hermitian = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
        hermitian = hermitian + hermitian.conj().T
        expected = GAMMA * (np.trace(hermitian) * vacuum_projector - hermitian)
        identity_error = max(identity_error, float(np.linalg.norm(generator(hermitian) - expected)))

    manifold_dim, spectral_gap, steady = steady_states(generator)
    overlap_with_vacuum = float(np.trace(vacuum_projector @ steady).real) if steady is not None else 0.0

    source_overlap, yes_post_overlap, no_post_overlap, _self, _trace = measured_overlaps()
    yes_after_yes, yes_after_no = relaxation_conditionals(source_overlap, yes_post_overlap, no_post_overlap, 1.0)
    memoryless_mean = stationary_yes_probability(yes_after_yes, yes_after_no)
    beta = beta_for_source(density, power=2)

    return LindbladianSelection(
        qubit_overlap=float(qubit_overlap),
        jordan_overlap=float(jordan_overlap),
        generator_identity_error=float(identity_error),
        steady_manifold_dim=int(manifold_dim),
        spectral_gap=float(spectral_gap),
        steady_overlap_with_vacuum=float(overlap_with_vacuum),
        relaxation_time=float(1.0 / GAMMA),
        memoryless_mean=float(memoryless_mean),
        stationary_beta=float(beta),
        stationary_amplitude=float(math.exp(-beta)),
        stationary_probability=float(model_probability(beta, power=2)),
        relaxation_is_gksl_semigroup=(identity_error < GENERATOR_TOL),
        vacuum_is_unique_steady_state=(manifold_dim == 1 and abs(overlap_with_vacuum - 1.0) < 1e-9),
        relaxation_is_exponential=(abs(spectral_gap - GAMMA) < 1e-9),
        jump_rate_derived_from_cho=False,
        jump_operators_derived_from_cho=False,
        source_overlap_derived_from_cho=False,
    )


def main() -> bool:
    semigroup = semigroup_rows()
    conditionals = conditional_rows()
    controls = generator_control_rows()
    selection = lindbladian_selection()
    composition_error = survival_composition_error()
    target_beta = -math.log(EPS0)

    print("=" * 78)
    print("F4-BREAKING CHO LINDBLADIAN GATE")
    print("Is the relaxation channel the propagator of a concrete Lindblad generator?")
    print("=" * 78)

    print("\n[A] Concrete GKSL generator L(rho)=gamma(Tr(rho)P - rho)")
    print(f"  qubit overlap |<p|q>|^2                   : {selection.qubit_overlap:.15f}")
    print(f"  Jordan Tr(P o Q)                          : {selection.jordan_overlap:.15f}")
    print(f"  pi/432                                    : {EPS0_SQ:.15f}")
    print(f"  GKSL identity error (random rho)          : {selection.generator_identity_error:.2e}")
    print("  jump operators L_k=sqrt(gamma)|p><e_k| (amplitude damping into the vacuum).")

    print("\n[B] Unique steady state and spectral gap")
    print(f"  steady-manifold dimension                 : {selection.steady_manifold_dim}")
    print(f"  steady overlap with vacuum Tr(P rho_ss)   : {selection.steady_overlap_with_vacuum:.15f}")
    print(f"  spectral gap (= gamma = 1/tau)            : {selection.spectral_gap:.15f}")
    print(f"  relaxation time tau                       : {selection.relaxation_time:.15f}")

    print("\n[C] Exact semigroup exp(tL) = depolarizing-toward-P channel C_{r(t)}")
    for row in semigroup:
        print(
            f"  gamma={row.gamma:.1f} t={row.time:<4} r(t)={row.relaxation_fraction:.12f} "
            f"|exp(tL)-C_r|={row.semigroup_error:.2e} choi_min={row.choi_min_eigenvalue:+.2e} "
            f"trace_err={row.trace_error:.2e}"
        )
    print(f"  survival composition (1-r(s))(1-r(t))=1-r(s+t) error: {composition_error:.2e}")

    print("\n[D] r(Delta_t)=1-exp(-gamma Delta_t) into vacuum-relaxation conditionals")
    for row in conditionals:
        print(
            f"  Delta_t={row.interval:<5} r={row.relaxation_fraction:.12f} "
            f"p(yes|yes)={row.yes_after_yes:.12f} p(yes|no)={row.yes_after_no:.12f} "
            f"mean={row.stationary_mean:.12f} mean_err={row.mean_error:.2e} gap={row.memoryless_gap:.3e}"
        )
    print("  mean is d for every Delta_t; gap -> 0 (memoryless) as gamma Delta_t -> inf.")

    print("\n[E] Generator controls (only vacuum damping reaches the vacuum at mean d)")
    for row in controls:
        print(
            f"  {row.label:<31} dim_ss={row.steady_manifold_dim} gap={row.spectral_gap:.6f} "
            f"mean={row.steady_mean:.12f} unique_vacuum={row.unique_vacuum_steady_state} "
            f"reaches_vacuum={row.reaches_vacuum}"
        )
        print(f"      {row.interpretation}")

    print("\n  Memoryless anchor (r=1):")
    print(f"  stationary mean                           : {selection.memoryless_mean:.15f}")
    print(f"  stationary beta                           : {selection.stationary_beta:.12f}")
    print(f"  target beta=-log(eps0)                    : {target_beta:.12f}")
    print(f"  exp(-beta)                                : {selection.stationary_amplitude:.15f}")
    print(f"  exp(-2 beta)                              : {selection.stationary_probability:.15f}")

    print("\n[V] Verdict")
    print("  relaxation channel = GKSL semigroup exp(tL) : YES, conditional")
    print("  unique vacuum steady state P                : YES")
    print("  exponential law r=1-exp(-t/tau)             : YES")
    print("  jump rate gamma=1/tau from CHO action       : NO")
    print("  vacuum jump operators from CHO action       : NO")
    print("  Bayes/scoreboard credit moved               : NO")
    print("=" * 78)

    density = EPS0_SQ

    # [A] concrete GKSL generator faithfully reproduces the Jordan overlap
    assert abs(selection.qubit_overlap - selection.jordan_overlap) < MATCH_TOL
    assert abs(selection.qubit_overlap - EPS0_SQ) < MATCH_TOL
    assert selection.generator_identity_error < GENERATOR_TOL

    # [B] unique vacuum steady state with gap gamma
    assert selection.steady_manifold_dim == 1
    assert abs(selection.steady_overlap_with_vacuum - 1.0) < 1e-9
    assert abs(selection.spectral_gap - GAMMA) < 1e-9
    assert abs(selection.relaxation_time - 1.0 / GAMMA) < TOL

    # [C] exp(tL) equals the depolarizing channel, CPTP, trace preserving
    for row in semigroup:
        assert row.semigroup_error < SEMIGROUP_TOL
        assert row.choi_min_eigenvalue > -CHOI_TOL
        assert row.trace_error < SEMIGROUP_TOL
        assert abs(row.relaxation_fraction - (1.0 - math.exp(-row.gamma * row.time))) < TOL
    assert composition_error < TOL

    # [D] every probe interval preserves mean d; gap shrinks monotonically to memoryless
    assert all(row.mean_error < TOL for row in conditionals)
    gaps = [row.memoryless_gap for row in conditionals]
    assert all(gaps[i] > gaps[i + 1] for i in range(len(gaps) - 1))
    assert gaps[-1] < gaps[0]

    # [E] only vacuum damping is a unique vacuum attractor at mean d
    vacuum_controls = [row for row in controls if row.unique_vacuum_steady_state]
    assert len(vacuum_controls) == 1
    assert "vacuum damping" in vacuum_controls[0].label
    assert abs(vacuum_controls[0].steady_mean - density) < 1e-9
    assert abs(vacuum_controls[0].spectral_gap - GAMMA) < 1e-9
    wrong_target = [row for row in controls if "wrong-target" in row.label][0]
    assert wrong_target.steady_manifold_dim == 1 and abs(wrong_target.steady_mean - 1.0) < 1e-9
    unitary = [row for row in controls if "unitary" in row.label][0]
    assert unitary.steady_manifold_dim > 1 and unitary.spectral_gap < 1e-9
    dephasing = [row for row in controls if "dephasing" in row.label][0]
    assert dephasing.steady_manifold_dim > 1 and not dephasing.reaches_vacuum

    # anchors and honesty flags
    assert abs(selection.memoryless_mean - density) < TOL
    assert abs(selection.stationary_beta - target_beta) < MATCH_TOL
    assert abs(selection.stationary_amplitude - EPS0) < MATCH_TOL
    assert abs(selection.stationary_probability - EPS0_SQ) < MATCH_TOL
    assert selection.relaxation_is_gksl_semigroup
    assert selection.vacuum_is_unique_steady_state
    assert selection.relaxation_is_exponential
    assert not selection.jump_rate_derived_from_cho
    assert not selection.jump_operators_derived_from_cho
    assert not selection.source_overlap_derived_from_cho
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
