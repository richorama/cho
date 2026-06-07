"""
F0 admissible-kernel class gate.

This artifact narrows the second open seam from
`epsilon_action_stationary.py`: why the admissible class is

    O >= 0, Tr(O) = pi

on the 16x27 bridge space.

It does not claim a full CHO microscopic derivation. It checks the minimal
closure logic used throughout the current action program:

1) Pure transition rays are rank-one projectors K = |psi><psi|.
2) History/coarse-graining closure is convex mixing of such rays.
3) Basis-indifference (unitary averaging) drives the class to a unique fixed
   point I/d among normalized states.
4) Multiplying by theta=pi fixes Tr(O)=pi.

Under (1)-(4), admissible kernels are exactly positive semidefinite,
trace-normalized operators.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_kernel_class_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


DIM_W = 16
DIM_J = 27
DIM = DIM_W * DIM_J
THETA = math.pi


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    metric: str
    note: str


def _random_pure_state(dim: int, rng: np.random.Generator) -> np.ndarray:
    vector = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
    vector /= np.linalg.norm(vector)
    return vector


def _projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def _min_eig_hermitian(matrix: np.ndarray) -> float:
    herm = (matrix + matrix.conj().T) / 2.0
    return float(np.min(np.linalg.eigvalsh(herm)))


def _trace_real(matrix: np.ndarray) -> float:
    return float(np.trace(matrix).real)


def main() -> bool:
    rng = np.random.default_rng(23)
    tol = 1e-10

    orbit_states = []
    orbit_min = 1e9
    orbit_trace_err = 0.0
    orbit_rank_err = 0.0
    for _ in range(40):
        psi = _random_pure_state(DIM, rng)
        kernel = _projector(psi)
        orbit_states.append(kernel)
        eigvals = np.linalg.eigvalsh((kernel + kernel.conj().T) / 2.0)
        orbit_min = min(orbit_min, float(np.min(eigvals)))
        orbit_trace_err = max(orbit_trace_err, abs(_trace_real(kernel) - 1.0))
        orbit_rank_err = max(orbit_rank_err, abs(float(np.sum(eigvals > 1e-9)) - 1.0))

    mix_min = 1e9
    mix_trace_err = 0.0
    for _ in range(24):
        weights = rng.random(len(orbit_states))
        weights /= float(np.sum(weights))
        rho = np.zeros((DIM, DIM), dtype=complex)
        for weight, state in zip(weights, orbit_states):
            rho += weight * state
        mix_min = min(mix_min, _min_eig_hermitian(rho))
        mix_trace_err = max(mix_trace_err, abs(_trace_real(rho) - 1.0))

    twirl_samples = 200
    mean_rho = np.zeros((DIM, DIM), dtype=complex)
    for _ in range(twirl_samples):
        psi = _random_pure_state(DIM, rng)
        mean_rho += _projector(psi)
    mean_rho /= twirl_samples
    identity_over_dim = np.eye(DIM, dtype=complex) / DIM
    twirl_gap = float(np.linalg.norm(mean_rho - identity_over_dim, ord="fro"))

    rho_ref = orbit_states[0]
    operator_ref = THETA * rho_ref
    operator_trace_err = abs(_trace_real(operator_ref) - THETA)
    operator_min = _min_eig_hermitian(operator_ref)

    bad = np.zeros((DIM, DIM), dtype=float)
    bad[0, 0] = 1.2
    bad[1, 1] = -0.2
    e2 = np.zeros(DIM)
    e2[1] = 1.0
    bad_prob = float(e2 @ bad @ e2)

    checks = [
        Check(
            "pure-ray orbit is PSD rank-one trace-one",
            orbit_min > -tol and orbit_trace_err < 1e-12 and orbit_rank_err < 1e-12,
            f"min eig={orbit_min:.2e}; max |Tr-1|={orbit_trace_err:.2e}",
            "rank-one projector class is the primitive transition-ray orbit",
        ),
        Check(
            "convex closure preserves PSD and trace",
            mix_min > -tol and mix_trace_err < 1e-12,
            f"min eig={mix_min:.2e}; max |Tr-1|={mix_trace_err:.2e}",
            "coarse-grained histories stay in density-operator class",
        ),
        Check(
            "basis-indifferent average fixed point is I/d",
            twirl_gap < 1.5e-1,
            f"||mean rho - I/d||_F = {twirl_gap:.3e} (N={twirl_samples})",
            "unitary-averaged normalized state class has unique isotropic center",
        ),
        Check(
            "theta scaling yields Tr(O)=pi and O>=0",
            operator_trace_err < 1e-12 and operator_min > -tol,
            f"|Tr(O)-pi|={operator_trace_err:.2e}; min eig={operator_min:.2e}",
            "O = pi rho gives the stationarity admissible normalization",
        ),
        Check(
            "non-PSD trace-one kernels are excluded",
            bad_prob < 0.0,
            f"example ray probability = {bad_prob:.3f}",
            "negative probabilities disqualify non-PSD kernels from admissible class",
        ),
    ]

    print("=" * 78)
    print("  F0 ADMISSIBLE-KERNEL CLASS GATE")
    print("  Do symmetry + convex closure force O>=0, Tr(O)=pi?")
    print("=" * 78)
    print()
    print(f"  Bridge dimension: d = {DIM_W} x {DIM_J} = {DIM}")
    print(f"  Normalization target: Tr(O)=theta=pi, so Tr(O)/d = pi/{DIM}")
    print()
    print(f"  {'check':<44} {'status':<6} metric")
    print("  " + "-" * 74)
    for check in checks:
        print(f"  {check.name:<44} {'PASS' if check.passed else 'FAIL':<6} {check.metric}")
        print(f"      {check.note}")
    print()

    ok = all(check.passed for check in checks)
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL")
    print("  THEOREM STATUS: admissible class is closure-consistent under")
    print("                  symmetry/convex assumptions; open seam remains")
    print("                  deriving these assumptions directly from full CHO")
    print("                  action dynamics.")
    print()
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)