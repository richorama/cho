"""
F4-BREAKING COOLING-ARROW GATE -- where does the cooling direction come from?
================================================================================

The vacuum-purity gate showed that a COOLING (purity-increasing / entropy-decreasing)
flow plus a generic frame-breaking field forces the dissipative vacuum to be a
PRIMITIVE (rank-one) idempotent. But it took the cooling DIRECTION as an INPUT -- the
arrow-of-time / second-law assumption -- and flagged "derive the cooling direction
from a concrete CHO action" as its first open bridge. This gate climbs underneath that
input and asks the honest question: is the cooling direction a CONSEQUENCE of the CHO
Lindbladian dynamics, or a separate boundary condition?

It is a separate boundary condition. Generalise the CHO Lindbladian to a finite
"temperature" by adding the detailed-balance partner of the vacuum-damping jumps:

    L_down,k = sqrt(gamma (1 + nbar)) |p><e_k|     (de-excitation INTO the vacuum p)
    L_up,k   = sqrt(gamma  nbar    ) |e_k><p|      (excitation OUT OF the vacuum p)

where nbar >= 0 is the mean bath occupation (a Bose factor = the temperature). This is
the textbook generalised-amplitude-damping GKSL generator; nbar = 0 recovers exactly the
CHO Lindbladian gate's amplitude-damping-into-p dissipator. The unique steady state is the
thermal (Gibbs) state, and its purity is a strictly decreasing function of nbar:

    nbar = 0  (zero temperature)  -> steady state = the PURE primitive vacuum P (purity 1) ;
    nbar > 0  (finite temperature)-> steady state MIXED (purity < 1), NOT an idempotent ;
    nbar ->oo (infinite temperature)-> steady state = the maximally mixed I/d (purity 1/d:
              1/3 on the J3(O) slice -- exactly the vacuum-purity gate's HEATING attractor).

Two facts make the verdict honest and two-sided:

  (1) Relaxation TO the steady state is automatic -- a THEOREM. Spohn's H-theorem: the
      relative entropy S(rho_t || rho_ss) is monotone non-increasing under the semigroup
      for every nbar (verified numerically, 1.386 -> 0). So the dynamics ALWAYS relaxes;
      the only open choice is WHICH steady state -- pure (cooling) or mixed (heating).

  (2) That choice is set by the bath temperature nbar, NOT by the CHO/F4 algebra. The
      algebra is time-symmetric: the time-reversed generator (up-only jumps) is an equally
      valid GKSL semigroup that "cools" to the EXCITED anti-vacuum (purity 1, vacuum
      overlap 0). Only nbar = 0 toward p, together with the seed gate's frame-breaking
      field, selects the physical vacuum.

What this proves
----------------
The vacuum-purity gate's cooling input is exactly the zero-temperature limit nbar = 0 of
the (already established) CHO Lindbladian. Cooling toward a PURE primitive idempotent is
the zero-temperature boundary condition; finite or infinite temperature relaxes to a mixed
or maximally mixed vacuum. Relaxation itself is Spohn's theorem; the cooling DIRECTION is a
thermodynamic boundary condition (a low-entropy past), not an algebraic consequence.

What this still does not prove
------------------------------
This does NOT derive the cooling direction from the CHO action -- it RELOCATES it to the
zero-temperature / arrow-of-time boundary condition, which is DEEPER and more general than
pi/432. The cooling direction cannot be grounded in the CHO Lindbladian without circularity:
that generator's down-only jumps already ENCODE the nbar = 0 choice it would have to explain.
It does not derive nbar, gamma, the frame-breaking field, the generation assignment, or the
source overlap d = pi/432. This is the terminal rung of the dissipative ladder: the residual
that remains is the thermodynamic arrow of time, not a shallower sub-problem.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_cooling_arrow_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from f4_breaking_seed_op2 import EPS0_SQ
from f4_breaking_cho_lindbladian_gate import (
    _matrix_exponential,
    lindblad_generator,
    projector,
    question_ray,
    vacuum_ray,
)


GAMMA = 1.0
PURITY_TOL = 1e-9
GAP_TOL = 1e-9
EXACT_TOL = 1e-9
MONOTONE_TOL = 1e-7
LARGE_NBAR = 100.0          # finite proxy for the infinite-temperature limit
QUTRIT_MIXED_PURITY = 1.0 / 3.0
QUBIT_MIXED_PURITY = 1.0 / 2.0


@dataclass(frozen=True)
class TemperatureRow:
    n_bar: float
    label: str
    qubit_purity: float
    qutrit_purity: float
    qutrit_vacuum_overlap: float
    steady_manifold_dim: int
    spectral_gap: float
    selects_primitive_vacuum: bool


@dataclass(frozen=True)
class SpohnRow:
    time: float
    relative_entropy: float
    purity: float
    non_increasing: bool


@dataclass(frozen=True)
class DirectionControlRow:
    label: str
    steady_vacuum_overlap: float
    steady_purity: float
    reaches_primitive_vacuum: bool
    interpretation: str


@dataclass(frozen=True)
class CoolingArrowSelection:
    zero_temperature_purity: float
    finite_temperature_purity: float
    infinite_temperature_purity: float
    spohn_initial_entropy: float
    spohn_final_entropy: float
    time_reversed_vacuum_overlap: float
    source_overlap: float
    cooling_selects_primitive_vacuum: bool
    finite_temperature_selects_mixed_vacuum: bool
    infinite_temperature_selects_maximally_mixed: bool
    relaxation_to_steady_state_is_theorem: bool
    which_steady_state_set_by_temperature: bool
    cooling_is_zero_temperature_limit: bool
    algebra_is_time_symmetric: bool
    arrow_of_time_is_boundary_condition: bool
    cooling_direction_derived_from_cho: bool
    cooling_groundable_in_lindbladian_without_circularity: bool
    source_overlap_derived_from_cho: bool
    deeper_than_pi_over_432: bool


# --------------------------------------------------------------------------- #
#  Dimension-general superoperator / steady-state / relative-entropy helpers    #
# --------------------------------------------------------------------------- #
def _vec(matrix: np.ndarray) -> np.ndarray:
    return matrix.flatten()


def _unvec(vector: np.ndarray, dim: int) -> np.ndarray:
    return vector.reshape(dim, dim)


def _superoperator(generator, dim: int) -> np.ndarray:
    columns = []
    for row in range(dim):
        for col in range(dim):
            basis_matrix = np.zeros((dim, dim), dtype=complex)
            basis_matrix[row, col] = 1.0
            columns.append(_vec(generator(basis_matrix)))
    return np.array(columns).T


def _steady_state(generator, dim: int) -> tuple[int, float, np.ndarray]:
    """Return (steady-manifold dimension, spectral gap, unique steady state)."""
    super_matrix = _superoperator(generator, dim)
    eigenvalues, eigenvectors = np.linalg.eig(super_matrix)
    magnitudes = np.abs(eigenvalues)
    zero_mask = magnitudes < 1e-9
    manifold_dim = int(np.count_nonzero(zero_mask))
    decay_rates = -eigenvalues.real
    nonsteady = decay_rates[~zero_mask]
    spectral_gap = float(np.min(nonsteady)) if nonsteady.size else 0.0
    index = int(np.argmin(magnitudes))
    raw = _unvec(eigenvectors[:, index], dim)
    raw = 0.5 * (raw + raw.conj().T)
    trace = np.trace(raw)
    steady = raw / trace if abs(trace) > 1e-12 else raw
    return manifold_dim, spectral_gap, steady


def _relative_entropy(rho: np.ndarray, sigma: np.ndarray) -> float:
    """S(rho||sigma)=Tr(rho ln rho)-Tr(rho ln sigma); sigma assumed full rank here."""
    rho_eigs = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    self_term = sum(v * math.log(v) for v in rho_eigs if v > 1e-12)
    sig_eigs, sig_vecs = np.linalg.eigh(0.5 * (sigma + sigma.conj().T))
    log_diag = np.array([math.log(v) if v > 1e-12 else -700.0 for v in sig_eigs])
    log_sigma = (sig_vecs * log_diag) @ sig_vecs.conj().T
    cross_term = float(np.trace(rho @ log_sigma).real)
    return float(self_term - cross_term)


# --------------------------------------------------------------------------- #
#  Finite-temperature CHO Lindbladian                                           #
# --------------------------------------------------------------------------- #
def thermal_jump_operators(gamma: float, n_bar: float, dim: int) -> tuple[np.ndarray, ...]:
    """Detailed-balance jumps: de-excitation into the vacuum p plus its thermal partner.

    L_down,k = sqrt(gamma(1+nbar)) |p><e_k|,  L_up,k = sqrt(gamma nbar) |e_k><p|.
    nbar = 0 recovers the CHO Lindbladian gate's amplitude-damping-into-p generator.
    """
    ground = np.zeros(dim, dtype=complex)
    ground[0] = 1.0
    jumps: list[np.ndarray] = []
    for k in range(1, dim):
        excited = np.zeros(dim, dtype=complex)
        excited[k] = 1.0
        jumps.append(math.sqrt(gamma * (1.0 + n_bar)) * np.outer(ground, excited.conj()))
        if n_bar > 0.0:
            jumps.append(math.sqrt(gamma * n_bar) * np.outer(excited, ground.conj()))
    return tuple(jumps)


def steady_state_at_temperature(n_bar: float, dim: int) -> tuple[int, float, float, float]:
    """Return (manifold dim, spectral gap, purity, vacuum overlap) of the Gibbs steady state."""
    generator = lindblad_generator(thermal_jump_operators(GAMMA, n_bar, dim))
    manifold_dim, gap, rho = _steady_state(generator, dim)
    purity = float(np.trace(rho @ rho).real)
    vacuum_overlap = float(rho[0, 0].real)
    return manifold_dim, gap, purity, vacuum_overlap


def analytic_qubit_purity(n_bar: float) -> float:
    return ((1.0 + n_bar) ** 2 + n_bar ** 2) / (1.0 + 2.0 * n_bar) ** 2


def analytic_qutrit_purity(n_bar: float) -> float:
    x = n_bar / (1.0 + n_bar)
    return (1.0 + 2.0 * x ** 2) / (1.0 + 2.0 * x) ** 2


def temperature_rows() -> tuple[TemperatureRow, ...]:
    specs = (
        ("zero-T   nbar=0     (cooling)", 0.0),
        ("low-T    nbar=0.25", 0.25),
        ("mid-T    nbar=1", 1.0),
        ("high-T   nbar=4", 4.0),
        ("infinite-T nbar=100 (->I/d)", LARGE_NBAR),
    )
    rows = []
    for label, n_bar in specs:
        _, _, q2, _ = steady_state_at_temperature(n_bar, 2)
        m3, gap3, q3, ov3 = steady_state_at_temperature(n_bar, 3)
        rows.append(
            TemperatureRow(
                n_bar=float(n_bar),
                label=label,
                qubit_purity=q2,
                qutrit_purity=q3,
                qutrit_vacuum_overlap=ov3,
                steady_manifold_dim=m3,
                spectral_gap=gap3,
                selects_primitive_vacuum=bool(q3 > 1.0 - PURITY_TOL),
            )
        )
    return tuple(rows)


# --------------------------------------------------------------------------- #
#  Spohn H-theorem: relaxation to the steady state is automatic                 #
# --------------------------------------------------------------------------- #
def spohn_rows(n_bar: float = 0.5) -> tuple[SpohnRow, ...]:
    dim = 2
    generator = lindblad_generator(thermal_jump_operators(GAMMA, n_bar, dim))
    super_matrix = _superoperator(generator, dim)
    _, _, rho_ss = _steady_state(generator, dim)
    rho0 = np.zeros((dim, dim), dtype=complex)
    rho0[1, 1] = 1.0                       # pure excited: far from the warm steady state
    rows = []
    previous = math.inf
    for time in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        propagator = _matrix_exponential(time * super_matrix)
        rho_t = _unvec(propagator @ _vec(rho0), dim)
        rho_t = 0.5 * (rho_t + rho_t.conj().T)
        rel = _relative_entropy(rho_t, rho_ss)
        purity = float(np.trace(rho_t @ rho_t).real)
        rows.append(SpohnRow(float(time), rel, purity, bool(rel <= previous + MONOTONE_TOL)))
        previous = rel
    return tuple(rows)


# --------------------------------------------------------------------------- #
#  Direction controls: which steady state is reached                            #
# --------------------------------------------------------------------------- #
def direction_control_rows() -> tuple[DirectionControlRow, ...]:
    rows = []

    _, _, pur, ov = steady_state_at_temperature(0.0, 2)
    rows.append(DirectionControlRow(
        "cooling (zero-T, down-only)", ov, pur,
        bool(ov > 1.0 - PURITY_TOL and pur > 1.0 - PURITY_TOL),
        "selects the PRIMITIVE vacuum P (purity 1, overlap 1)"))

    _, _, pur, ov = steady_state_at_temperature(1.0, 2)
    rows.append(DirectionControlRow(
        "finite-T (nbar=1)", ov, pur, False,
        "MISS: mixed steady state, purity<1, not a primitive idempotent"))

    _, _, pur, ov = steady_state_at_temperature(LARGE_NBAR, 2)
    rows.append(DirectionControlRow(
        "infinite-T (nbar->inf)", ov, pur, False,
        "MISS: maximally mixed I/d -- the heating attractor"))

    ground = np.array([1.0, 0.0], dtype=complex)
    excited = np.array([0.0, 1.0], dtype=complex)
    up_only = math.sqrt(GAMMA) * np.outer(excited, ground.conj())   # |1><0|
    _, _, rho_up = _steady_state(lindblad_generator((up_only,)), 2)
    rows.append(DirectionControlRow(
        "time-reversed (up-only jumps)", float(rho_up[0, 0].real),
        float(np.trace(rho_up @ rho_up).real), False,
        "MISS: cools to the EXCITED anti-vacuum -- the algebra admits the reverse"))

    return tuple(rows)


def source_overlap() -> float:
    """The source overlap d=Tr(P o Q)=pi/432 stays an untouched input here."""
    p = projector(vacuum_ray())
    q = projector(question_ray(EPS0_SQ))
    return float(np.trace(p @ q).real)


def cooling_arrow_selection() -> CoolingArrowSelection:
    temps = temperature_rows()
    zero_t = [r for r in temps if r.n_bar == 0.0][0]
    finite_t = [r for r in temps if r.n_bar == 1.0][0]
    inf_t = [r for r in temps if r.n_bar == LARGE_NBAR][0]
    spohn = spohn_rows()
    controls = direction_control_rows()
    reversed_ctrl = [c for c in controls if "time-reversed" in c.label][0]

    return CoolingArrowSelection(
        zero_temperature_purity=zero_t.qutrit_purity,
        finite_temperature_purity=finite_t.qutrit_purity,
        infinite_temperature_purity=inf_t.qutrit_purity,
        spohn_initial_entropy=spohn[0].relative_entropy,
        spohn_final_entropy=spohn[-1].relative_entropy,
        time_reversed_vacuum_overlap=reversed_ctrl.steady_vacuum_overlap,
        source_overlap=source_overlap(),
        cooling_selects_primitive_vacuum=bool(zero_t.selects_primitive_vacuum),
        finite_temperature_selects_mixed_vacuum=bool(finite_t.qutrit_purity < 1.0 - PURITY_TOL),
        infinite_temperature_selects_maximally_mixed=bool(
            abs(inf_t.qutrit_purity - QUTRIT_MIXED_PURITY) < 1e-3),
        relaxation_to_steady_state_is_theorem=bool(all(r.non_increasing for r in spohn)),
        which_steady_state_set_by_temperature=True,
        cooling_is_zero_temperature_limit=True,
        algebra_is_time_symmetric=bool(reversed_ctrl.steady_vacuum_overlap < PURITY_TOL),
        arrow_of_time_is_boundary_condition=True,
        cooling_direction_derived_from_cho=False,
        cooling_groundable_in_lindbladian_without_circularity=False,
        source_overlap_derived_from_cho=False,
        deeper_than_pi_over_432=True,
    )


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def main() -> bool:
    temps = temperature_rows()
    spohn = spohn_rows()
    controls = direction_control_rows()
    selection = cooling_arrow_selection()

    print("=" * 78)
    print("  F4-BREAKING COOLING-ARROW GATE")
    print("  Where does the vacuum-purity gate's COOLING direction come from?")
    print("=" * 78)

    print("\n[A] Finite-temperature CHO Lindbladian: steady-state purity vs nbar")
    print("    L_down=sqrt(gamma(1+nbar))|p><e_k|, L_up=sqrt(gamma nbar)|e_k><p|; "
          "nbar=0 = the CHO gate")
    for r in temps:
        ana2 = analytic_qubit_purity(r.n_bar)
        ana3 = analytic_qutrit_purity(r.n_bar)
        print(
            f"  {r.label:30} dim1={r.steady_manifold_dim} gap={r.spectral_gap:7.3f} "
            f"qubit pi={r.qubit_purity:.6f}({ana2:.6f}) "
            f"qutrit pi={r.qutrit_purity:.6f}({ana3:.6f}) primitive={r.selects_primitive_vacuum}"
        )
    print(f"  nbar->inf limit (analytic): qubit pi->{QUBIT_MIXED_PURITY:.6f}, "
          f"qutrit pi->{QUTRIT_MIXED_PURITY:.6f} (the maximally mixed I/d)")

    print("\n[B] Spohn H-theorem: relaxation to the steady state is automatic (a THEOREM)")
    print("    relative entropy S(rho_t || rho_ss) at nbar=0.5, from the pure excited state")
    for r in spohn:
        print(f"  t={r.time:4.2f}  S(rho||ss)={r.relative_entropy:.8f}  "
              f"purity={r.purity:.6f}  non-increasing={r.non_increasing}")

    print("\n[C] The cooling direction = the zero-temperature limit nbar=0")
    zero_t = [r for r in temps if r.n_bar == 0.0][0]
    inf_t = [r for r in temps if r.n_bar == LARGE_NBAR][0]
    print(f"  nbar=0   : qutrit purity={zero_t.qutrit_purity:.6f} -> the PRIMITIVE vacuum "
          f"(vacuum-purity gate's cooling attractor)")
    print(f"  nbar=100 : qutrit purity={inf_t.qutrit_purity:.6f} -> I/3 "
          f"(vacuum-purity gate's HEATING attractor)")
    print(f"  the source overlap d=Tr(P o Q)={selection.source_overlap:.8f}=pi/432 stays an "
          f"untouched input (eps0^2={EPS0_SQ:.8f})")

    print("\n[D] Controls: which steady state is reached (the algebra is time-symmetric)")
    for c in controls:
        print(f"  {c.label:30} overlap_vac={c.steady_vacuum_overlap:.6f} "
              f"purity={c.steady_purity:.6f} vacuum={c.reaches_primitive_vacuum}  {c.interpretation}")

    print("\n[V] Verdict")
    print("  cooling (zero-T) selects the primitive vacuum            : YES")
    print("  finite-T selects a mixed vacuum (control miss)           : YES")
    print("  infinite-T selects the maximally mixed I/3 (heating)     : YES")
    print("  relaxation to the steady state is a theorem (Spohn)      : YES")
    print("  WHICH steady state is set by the bath temperature nbar   : YES")
    print("  cooling direction = zero-temperature limit = arrow of time: YES")
    print("  the CHO algebra is time-symmetric (reverse is admitted)  : YES")
    print("  cooling direction derived from the CHO action            : NO")
    print("  cooling groundable in the Lindbladian without circularity: NO")
    print("  source overlap d=pi/432 derived from the CHO action      : NO")
    print("  the residual is DEEPER than pi/432 (it is the arrow of time): YES")
    print("  Bayes/scoreboard credit moved                            : NO")
    print("=" * 78)

    # [A] finite-T steady-state purity matches analytics; monotone decrease in nbar
    by_n = {r.n_bar: r for r in temps}
    for r in temps:
        assert abs(r.qubit_purity - analytic_qubit_purity(r.n_bar)) < EXACT_TOL
        assert abs(r.qutrit_purity - analytic_qutrit_purity(r.n_bar)) < EXACT_TOL
        assert r.steady_manifold_dim == 1            # unique Gibbs steady state
        assert r.spectral_gap > GAP_TOL              # gapped relaxation at every temperature
    assert abs(by_n[0.0].qubit_purity - 1.0) < EXACT_TOL
    assert abs(by_n[0.0].qutrit_purity - 1.0) < EXACT_TOL
    assert by_n[0.0].selects_primitive_vacuum                       # cooling -> primitive
    assert by_n[1.0].qutrit_purity < 1.0 - 1e-3                     # finite-T -> mixed
    assert not by_n[1.0].selects_primitive_vacuum
    assert abs(by_n[LARGE_NBAR].qutrit_purity - QUTRIT_MIXED_PURITY) < 1e-3   # -> I/3
    assert abs(by_n[LARGE_NBAR].qubit_purity - QUBIT_MIXED_PURITY) < 1e-3
    # purity strictly decreasing with temperature on the J3(O) slice
    ordered = [by_n[n].qutrit_purity for n in (0.0, 0.25, 1.0, 4.0, LARGE_NBAR)]
    assert all(ordered[i] > ordered[i + 1] for i in range(len(ordered) - 1))

    # [B] Spohn H-theorem: monotone non-increasing relative entropy -> 0
    assert all(r.non_increasing for r in spohn)
    assert spohn[0].relative_entropy > 0.1                          # starts far from steady
    assert spohn[-1].relative_entropy < 1e-5                        # relaxes to the steady state
    for i in range(len(spohn) - 1):
        assert spohn[i + 1].relative_entropy <= spohn[i].relative_entropy + MONOTONE_TOL

    # [D] controls: cooling reaches the vacuum; finite/infinite-T and reversal miss
    by_label = {c.label: c for c in controls}
    assert by_label["cooling (zero-T, down-only)"].reaches_primitive_vacuum
    assert not by_label["finite-T (nbar=1)"].reaches_primitive_vacuum
    assert by_label["finite-T (nbar=1)"].steady_purity < 1.0 - 1e-3
    assert not by_label["infinite-T (nbar->inf)"].reaches_primitive_vacuum
    rev = by_label["time-reversed (up-only jumps)"]
    assert rev.steady_vacuum_overlap < PURITY_TOL                   # cools to the anti-vacuum
    assert abs(rev.steady_purity - 1.0) < PURITY_TOL                # a pure (wrong) pole

    # source overlap stays pi/432, untouched
    assert abs(selection.source_overlap - EPS0_SQ) < EXACT_TOL

    # honesty / humility tripwires
    assert selection.cooling_selects_primitive_vacuum
    assert selection.finite_temperature_selects_mixed_vacuum
    assert selection.infinite_temperature_selects_maximally_mixed
    assert selection.relaxation_to_steady_state_is_theorem
    assert selection.which_steady_state_set_by_temperature
    assert selection.cooling_is_zero_temperature_limit
    assert selection.algebra_is_time_symmetric
    assert selection.arrow_of_time_is_boundary_condition
    assert selection.deeper_than_pi_over_432
    assert not selection.cooling_direction_derived_from_cho
    assert not selection.cooling_groundable_in_lindbladian_without_circularity
    assert not selection.source_overlap_derived_from_cho
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
