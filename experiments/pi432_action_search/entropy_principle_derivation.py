"""Entropy/free-energy principle for the WZ/Jordan seed candidate.

This probe attacks the assumption that the seed action should contain

    Tr(rho log rho) + Delta Tr(rho N).

Conditional derivation:

* If seed weights are probabilities over mutually exclusive Jordan-frame levels,
  the large-deviation / maximum-entropy rate functional is relative entropy.
* Adding one linear Peirce-grade constraint gives the Gibbs variational problem.
* Its Euler-Lagrange equation is exactly the candidate seed law.

This still does not prove CHO dynamics must use this statistical action; it shows
that once the problem is formulated as a canonical large-deviation/free-energy
principle, the entropy term and Gibbs form are forced.
"""

from __future__ import annotations

from math import exp, log, pi, sqrt


PHI = pi / 432.0
DELTA = -0.5 * log(PHI)
GRADES = (0, 1, 2)


def gibbs_distribution(delta: float = DELTA) -> tuple[float, float, float]:
    weights = tuple(exp(-delta * grade) for grade in GRADES)
    partition = sum(weights)
    return tuple(weight / partition for weight in weights)


def free_energy(probabilities: tuple[float, float, float], delta: float = DELTA) -> float:
    entropy_rate = sum(p * log(p) for p in probabilities if p > 0.0)
    grade_energy = sum(p * grade for p, grade in zip(probabilities, GRADES))
    return entropy_rate + delta * grade_energy


def stationarity_residuals(probabilities: tuple[float, float, float]) -> tuple[float, float, float]:
    raw = tuple(log(p) + 1.0 + DELTA * grade for p, grade in zip(probabilities, GRADES))
    mean = sum(raw) / len(raw)
    return tuple(value - mean for value in raw)


def nearby_simplex_points(step: int = 20) -> list[tuple[float, float, float]]:
    points = []
    for i in range(1, step):
        for j in range(1, step - i):
            k = step - i - j
            if k > 0:
                points.append((i / step, j / step, k / step))
    return points


def main() -> bool:
    rho = gibbs_distribution()
    residuals = stationarity_residuals(rho)
    target_weights = (1.0, sqrt(PHI), PHI)
    actual_ratios = (1.0, rho[1] / rho[0], rho[2] / rho[0])
    sampled_min = min(free_energy(point) for point in nearby_simplex_points())

    print("=" * 78)
    print("ENTROPY/FREE-ENERGY PRINCIPLE")
    print("=" * 78)

    print("\n[A] Gibbs variational problem")
    print("  minimize F(rho) = sum rho_i log rho_i + Delta sum i rho_i")
    print("  subject to sum rho_i = 1, rho_i > 0")
    print(f"  grades                 : {GRADES}")
    print(f"  Delta                  : {DELTA:.15f}")

    print("\n[B] Stationary point")
    print(f"  rho                    : {rho}")
    print(f"  ratios rho_i/rho_0     : {actual_ratios}")
    print(f"  target ratios           : {target_weights}")
    print(f"  stationarity residuals  : {residuals}")
    print(f"  free energy at rho      : {free_energy(rho):.15f}")
    print(f"  best coarse grid F      : {sampled_min:.15f}")

    print("\n[C] What this proves")
    print("  Given the large-deviation/free-energy formulation and the Peirce grade")
    print("  constraint, the entropy functional and Gibbs seed law are forced. The")
    print("  remaining physics theorem is to derive why CHO/Jordan/WZ dynamics has")
    print("  this canonical free-energy form.")

    print("\n[V] Sandbox verdict")
    print("  entropy action from large-deviation principle : CONDITIONALLY DERIVED")
    print("  large-deviation principle from CHO dynamics   : OPEN")
    print("=" * 78)

    assert max(abs(value) for value in residuals) < 1e-14
    assert max(abs(a - b) for a, b in zip(actual_ratios, target_weights)) < 1e-14
    assert free_energy(rho) < sampled_min
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
