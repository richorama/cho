"""
F0 action-ray derivation gate.

Goal
----
Turn "ray representative" into a direct action-level computation in the
current one-operator scaffold.

Method
------
Given the Hermitian action generator H (from the bridge operator), derive the
transition ray as the unique stationary maximizer of the Rayleigh functional

    R(psi) = <psi|H|psi>, ||psi||=1.

This is equivalent to solving the action stationarity equation

    H |tau> = lambda_max |tau>

and can be reached dynamically by normalized imaginary-time ascent

    d|psi>/dt = (H - <H>)|psi>.

What it closes
--------------
It gives an explicit dynamical derivation of the transition ray inside the
current action scaffold (instead of choosing a basis ray by hand).

What remains open
-----------------
Deriving this exact effective generator from full CHO microscopic dynamics.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_action_ray_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from cho_bridge_operator import CHOBridgeOperator


DIM_W = 16
DIM_J = 27
DIM = DIM_W * DIM_J


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    metric: str
    note: str


def _normalize(vector: np.ndarray) -> np.ndarray:
    return vector / np.linalg.norm(vector)


def _projector(vector: np.ndarray) -> np.ndarray:
    state = _normalize(vector)
    return np.outer(state, state.conj())


def _ray_fidelity(projector_a: np.ndarray, projector_b: np.ndarray) -> float:
    return float(np.trace(projector_a @ projector_b).real)


def _imaginary_time_flow(
    hamiltonian: np.ndarray,
    psi0: np.ndarray,
    *,
    dt: float = 0.2,
    steps: int = 220,
) -> np.ndarray:
    psi = _normalize(psi0)
    for _ in range(steps):
        energy = float(np.vdot(psi, hamiltonian @ psi).real)
        psi = psi + dt * (hamiltonian @ psi - energy * psi)
        psi = _normalize(psi)
    return psi


def main() -> bool:
    operator = CHOBridgeOperator().epsilon_operator().astype(complex)
    hamiltonian = (operator + operator.conj().T) / 2.0

    eigvals, eigvecs = np.linalg.eigh(hamiltonian)
    order = np.argsort(eigvals)
    top = int(order[-1])
    second = int(order[-2])

    lambda_max = float(eigvals[top].real)
    lambda_second = float(eigvals[second].real)
    gap = lambda_max - lambda_second

    tau = _normalize(eigvecs[:, top])
    tau_projector = _projector(tau)

    stationarity_resid = float(np.linalg.norm(hamiltonian @ tau - lambda_max * tau))
    rank_resid = float(np.linalg.norm(tau_projector @ tau_projector - tau_projector))

    rng = np.random.default_rng(31)
    worst_flow_fidelity = 1.0
    worst_energy_gap = 0.0
    for _ in range(20):
        seed = rng.standard_normal(DIM) + 1j * rng.standard_normal(DIM)
        flowed = _imaginary_time_flow(hamiltonian, seed)
        flow_projector = _projector(flowed)
        fidelity = _ray_fidelity(flow_projector, tau_projector)
        worst_flow_fidelity = min(worst_flow_fidelity, fidelity)
        energy = float(np.vdot(flowed, hamiltonian @ flowed).real)
        worst_energy_gap = max(worst_energy_gap, abs(lambda_max - energy))

    # In the current scaffold O = pi |tau><tau|, so normalized O gives the same ray.
    rho = operator / float(np.trace(operator).real)
    rho_match = float(np.linalg.norm(rho - tau_projector, ord="fro"))

    checks = [
        Check(
            "top eigenvalue is non-degenerate",
            gap > 1e-8,
            f"lambda_max-lambda_2 = {gap:.6e}",
            "unique spectral maximizer implies unique action-selected ray",
        ),
        Check(
            "stationarity equation is solved",
            stationarity_resid < 1e-10,
            f"||H|tau>-lambda|tau>|| = {stationarity_resid:.2e}",
            "direct Euler-Lagrange eigen-equation check",
        ),
        Check(
            "derived ray is rank-one projector",
            rank_resid < 1e-12,
            f"||K^2-K||_F = {rank_resid:.2e}",
            "primitive transition ray is projective/idempotent",
        ),
        Check(
            "imaginary-time action flow converges to same ray",
            worst_flow_fidelity > 1.0 - 1e-8 and worst_energy_gap < 1e-8,
            f"min fidelity={worst_flow_fidelity:.10f}; max energy gap={worst_energy_gap:.2e}",
            "independent initial conditions collapse to one stationary representative",
        ),
        Check(
            "normalized operator matches derived ray",
            rho_match < 1e-10,
            f"||O/Tr(O) - |tau><tau|||_F = {rho_match:.2e}",
            "bridge operator encodes the same action-derived transition ray",
        ),
    ]

    print("=" * 78)
    print("  F0 ACTION-RAY DERIVATION GATE")
    print("  Is the transition ray derived as an action stationary solution?")
    print("=" * 78)
    print()
    print(f"  Bridge dimension: {DIM_W} x {DIM_J} = {DIM}")
    print(f"  Rayleigh maximizer eigenvalue: lambda_max = {lambda_max:.12f}")
    print()
    print(f"  {'check':<44} {'status':<6} metric")
    print("  " + "-" * 74)
    for check in checks:
        print(f"  {check.name:<44} {'PASS' if check.passed else 'FAIL':<6} {check.metric}")
        print(f"      {check.note}")
    print()

    ok = all(check.passed for check in checks)
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL")
    print("  THEOREM STATUS: transition ray is action-derived in the current")
    print("                  effective one-operator dynamics; remaining seam is")
    print("                  deriving this generator from full CHO action.")
    print()
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)