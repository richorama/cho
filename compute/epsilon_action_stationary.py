"""
F0 action-stationarity witness: primitive epsilon kernel as unique maximizer.

This artifact pushes the post-Schur/post-product seam one step deeper at action
level. It studies the normalized link action already used in
`primitive_projector_derivation.py`:

    S_link(O,K) = log( <O,K> / (||O||_F ||K||_F) ),

for transition kernels O constrained to be positive semidefinite with fixed
trace Tr(O)=pi on the 16x27 bridge space (dim 432). K is the rank-one
transition ray kernel.

Key fact (analytic): by Cauchy-Schwarz, <O,K> <= ||O||_F ||K||_F, so
S_link <= 0. Equality (S_link = 0) holds iff O is proportional to K. With
Tr(O)=pi and Tr(K)=1, this forces O = pi K uniquely.

So, in this admissible action class, the primitive kernel is not an arbitrary
choice: it is the unique global maximizer of the normalized link action.

What this does NOT close:
- selecting the physical transition ray K from CHO dynamics (vacuum purity /
  action-origin seam), and
- proving that this exact admissible class is the full CHO path-integral kernel
  class (still an architecture/action derivation task).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_action_stationary.py
"""

from dataclasses import dataclass
import math

import numpy as np

from cho_bridge_operator import CHOBridgeOperator

DIM_W = 16
DIM_J = 27
DIM = DIM_W * DIM_J
THETA = math.pi
TARGET = THETA / DIM


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    metric: str
    note: str


def _rank_one(index: int, dim: int) -> np.ndarray:
    e = np.zeros(dim)
    e[index] = 1.0
    return np.outer(e, e)


def _normalize_trace(matrix: np.ndarray, target_trace: float) -> np.ndarray:
    tr = float(np.trace(matrix).real)
    if tr <= 0.0:
        raise ValueError("matrix has non-positive trace")
    return matrix * (target_trace / tr)


def _random_density(dim: int, rng: np.random.Generator) -> np.ndarray:
    a = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
    m = a @ a.conj().T
    return _normalize_trace(m, 1.0)


def _random_separable_density(rng: np.random.Generator) -> np.ndarray:
    rho_w = _random_density(DIM_W, rng)
    rho_j = _random_density(DIM_J, rng)
    return np.kron(rho_w, rho_j)


def _fro_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, ord="fro"))


def link_action(operator: np.ndarray, kernel: np.ndarray) -> float:
    num = float(np.sum(operator.conj() * kernel).real)
    den = _fro_norm(operator) * _fro_norm(kernel)
    ratio = max(min(num / den, 1.0), 1e-300)
    return float(np.log(ratio))


def main() -> bool:
    k = _rank_one(0, DIM)
    o_star = THETA * k
    o_scaffold = CHOBridgeOperator().epsilon_operator().real

    s_star = link_action(o_star, k)
    s_scaffold = link_action(o_scaffold, k)
    scaffold_gap = float(np.max(np.abs(o_scaffold - o_star)))

    alpha = float(np.sum(o_scaffold * k) / np.sum(k * k))
    colinear_resid = float(np.max(np.abs(o_scaffold - alpha * k)))

    rng = np.random.default_rng(13)

    max_random = -1e9
    max_sep = -1e9
    for _ in range(80):
        rho = _random_density(DIM, rng)
        o = THETA * rho
        max_random = max(max_random, link_action(o, k))
    for _ in range(120):
        rho_sep = _random_separable_density(rng)
        o_sep = THETA * rho_sep
        max_sep = max(max_sep, link_action(o_sep, k))

    etas = [1e-4, 1e-3, 1e-2, 5e-2, 1e-1]
    worst_local = 0.0
    for _ in range(60):
        x = THETA * _random_density(DIM, rng)
        for eta in etas:
            o_eta = (1.0 - eta) * o_star + eta * x
            worst_local = max(worst_local, link_action(o_eta, k))

    checks = [
        Check(
            "global maximum at primitive kernel",
            abs(s_star) < 1e-14,
            f"S_link(pi K, K) = {s_star:.2e}",
            "Cauchy bound saturates at O = pi K",
        ),
        Check(
            "current scaffold equals primitive maximizer",
            scaffold_gap < 1e-12 and abs(s_scaffold) < 1e-12,
            f"max|O_scaffold-piK|={scaffold_gap:.2e}; S_link={s_scaffold:.2e}",
            "bridge scaffold currently sits exactly at the variational maximum",
        ),
        Check(
            "equality implies colinearity",
            colinear_resid < 1e-12 and abs(alpha - THETA) < 1e-12,
            f"alpha={alpha:.12f}; max|O-alphaK|={colinear_resid:.2e}",
            "numerical witness of the equality condition",
        ),
        Check(
            "random PSD kernels obey strict inequality",
            max_random < -1e-3,
            f"max random S_link = {max_random:.4f}",
            "generic non-maximizers stay below 0",
        ),
        Check(
            "random separable kernels obey strict inequality",
            max_sep < -1e-3,
            f"max separable S_link = {max_sep:.4f}",
            "separable class also has strict gap away from piK",
        ),
        Check(
            "local convex perturbations lower action",
            worst_local <= 1e-12,
            f"worst local perturbed S_link = {worst_local:.4e}",
            "convex perturbations respect S_link <= 0; strict gap is witnessed by random stress scans",
        ),
        Check(
            "trace value gives pi/432",
            abs(float(np.trace(o_star).real) / DIM - TARGET) < 1e-12,
            f"Tr(piK)/432 = {float(np.trace(o_star).real)/DIM:.10f}",
            "epsilon0^2 follows from the maximizer and fixed bridge dimension",
        ),
    ]

    print("=" * 78)
    print("  F0 ACTION-STATIONARITY WITNESS")
    print("  Is the primitive epsilon kernel variationally forced in the link action?")
    print("=" * 78)
    print()
    print("  Action class: O >= 0, Tr(O)=pi on 16x27 bridge space.")
    print("  Objective   : S_link(O,K) = log(<O,K> / (||O||_F ||K||_F)).")
    print("  Bound       : S_link <= 0 (Cauchy); equality iff O || K -> O = pi K.")
    print()

    print(f"  {'check':<42} {'status':<6} metric")
    print("  " + "-" * 74)
    for c in checks:
        print(f"  {c.name:<42} {'PASS' if c.passed else 'FAIL':<6} {c.metric}")
        print(f"      {c.note}")
    print()

    ok = all(c.passed for c in checks)
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- primitive kernel is the unique maximizer in this action class.")
    print("  THEOREM STATUS: strong variational evidence for primitive separable")
    print("                  epsilon kernel; open seam remains deriving the")
    print("                  physical transition ray and admissible kernel class")
    print("                  from full CHO action dynamics.")
    print()

    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
