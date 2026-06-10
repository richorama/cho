"""Unified CHO/Jordan/WZ boundary free-energy action candidate.

This is the strongest quarantined candidate so far. It tries to put the gates in
one action instead of checking them separately.

Configuration data
------------------
* an ordered orthogonal boundary pair of primitive idempotents `(P_0, P_2)` in
  `OP^2 = F4/Spin(9)`;
* the unique Jordan-frame completion `P_1 = I - P_0 - P_2`;
* a probability vector `rho` on the ordered frame `(P_0, P_1, P_2)`;
* a minimal WZ/Berry disk spanning the ordered transition, with half-flux `pi`.

Candidate action
----------------
Let

    Phi(B) = (minimal WZ half-flux) / dim(Delta_9 x J3(O)) = pi / 432,
    N_B    = diag(0,1,2) on the boundary-completed Jordan frame,
    Delta  = -log(Phi) / 2.

Then

    S_B[rho] = Tr(rho log rho) + Delta Tr(rho N_B),   Tr rho = 1.

Euler-Lagrange gives the Gibbs seed spectrum

    rho_i/rho_0 = exp(-Delta i) = (1, sqrt(Phi), Phi).

What is genuinely new here
--------------------------
The boundary pair is F4-covariant: applying any `g in F4` sends
`(P_0,P_1,P_2)` to `(gP_0,gP_1,gP_2)`, and the completion identity
`P_1 = I - P_0 - P_2` is preserved. So the action is not written in a permanently
fixed frame; the ordered WZ boundary data breaks F4 to the stabilizer of the
boundary pair and carries the Peirce grading with it.

Honest status
-------------
This still does not prove the full theory. It supplies one coherent action
candidate whose pieces mutually fit. The remaining theorem is to derive this
boundary free-energy action itself from the full CHO dynamics, rather than taking
the ordered WZ boundary pair and entropy principle as the effective action.

No scipy. Uses existing compute/ F4/J3(O) machinery for the covariance check.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/unified_boundary_wz_jordan_action.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
COMPUTE = ROOT / "compute"
if str(COMPUTE) not in sys.path:
    sys.path.insert(0, str(COMPUTE))

from epsilon_orbit_selection import _diag, primitive_idempotents  # noqa: E402
from epsilon_action_selection import _f4_basis, random_automorphism, trace_form  # noqa: E402


TOL = 1e-8
PI = math.pi
CARRIER_DIM = 16 * 27
PHI = PI / CARRIER_DIM
DELTA = -0.5 * math.log(PHI)
GRADES = (0, 1, 2)


@dataclass(frozen=True)
class FrameData:
    low: np.ndarray
    mid: np.ndarray
    high: np.ndarray

    @property
    def ordered(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (self.low, self.mid, self.high)


def source_frame() -> FrameData:
    e1, e2, e3 = primitive_idempotents()
    return FrameData(low=e1, mid=e2, high=e3)


def complete_boundary_pair(low: np.ndarray, high: np.ndarray) -> np.ndarray:
    identity = _diag(1.0, 1.0, 1.0)
    return identity - low - high


def frame_completion_residual(frame: FrameData) -> float:
    return float(np.linalg.norm(complete_boundary_pair(frame.low, frame.high) - frame.mid))


def orthogonality_table(frame: FrameData) -> tuple[float, float, float]:
    low, mid, high = frame.ordered
    return (
        float(abs(trace_form(low, mid))),
        float(abs(trace_form(low, high))),
        float(abs(trace_form(mid, high))),
    )


def transformed_frame(g: np.ndarray, frame: FrameData) -> FrameData:
    return FrameData(low=g @ frame.low, mid=g @ frame.mid, high=g @ frame.high)


def covariance_residuals(samples: int = 8, seed: int = 123) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    f4 = _f4_basis()
    frame = source_frame()
    identity = _diag(1.0, 1.0, 1.0)
    worst_completion = 0.0
    worst_identity = 0.0
    worst_orthogonality = 0.0
    for _ in range(samples):
        g = random_automorphism(rng, f4, scale=0.65)
        moved = transformed_frame(g, frame)
        worst_completion = max(worst_completion, frame_completion_residual(moved))
        worst_identity = max(worst_identity, float(np.linalg.norm((g @ identity) - identity)))
        worst_orthogonality = max(worst_orthogonality, max(orthogonality_table(moved)))
    return worst_completion, worst_identity, worst_orthogonality


def seed_weights() -> tuple[float, float, float]:
    return tuple(math.exp(-DELTA * grade) for grade in GRADES)


def seed_distribution() -> tuple[float, float, float]:
    weights = seed_weights()
    partition = sum(weights)
    return tuple(weight / partition for weight in weights)


def free_energy(rho: tuple[float, float, float]) -> float:
    entropy_rate = sum(p * math.log(p) for p in rho if p > 0.0)
    grade_energy = sum(p * grade for p, grade in zip(rho, GRADES))
    return entropy_rate + DELTA * grade_energy


def stationarity_residuals(rho: tuple[float, float, float]) -> tuple[float, float, float]:
    raw = tuple(math.log(p) + 1.0 + DELTA * grade for p, grade in zip(rho, GRADES))
    mean = sum(raw) / len(raw)
    return tuple(value - mean for value in raw)


def main() -> bool:
    frame = source_frame()
    completion_residual = frame_completion_residual(frame)
    orthogonality = orthogonality_table(frame)
    covariance = covariance_residuals()
    weights = seed_weights()
    rho = seed_distribution()
    target = (1.0, math.sqrt(PHI), PHI)
    stationarity = stationarity_residuals(rho)

    print("=" * 78)
    print("UNIFIED BOUNDARY CHO/JORDAN/WZ ACTION CANDIDATE")
    print("=" * 78)

    print("\n[A] Action")
    print("  Boundary data B = ordered orthogonal primitive pair (P0, P2) in OP2")
    print("  Frame completion P1 = I - P0 - P2")
    print("  Phi(B) = WZ_half_flux(B) / dim(Delta_9 x J3(O)) = pi / 432")
    print("  N_B = diag(0,1,2) on the boundary-completed frame")
    print("  S_B[rho] = Tr(rho log rho) + Delta Tr(rho N_B), Delta=-log(Phi)/2")

    print("\n[B] Boundary frame checks")
    print(f"  completion residual        : {completion_residual:.3e}")
    print(f"  pairwise trace products    : {orthogonality}")

    print("\n[C] F4 covariance checks")
    print(f"  worst moved-frame completion residual : {covariance[0]:.3e}")
    print(f"  worst identity preservation residual  : {covariance[1]:.3e}")
    print(f"  worst moved-frame orthogonality       : {covariance[2]:.3e}")

    print("\n[D] WZ-normalized seed law")
    print(f"  carrier dimension          : {CARRIER_DIM}")
    print(f"  Phi                        : {PHI:.15f}")
    print(f"  Delta                      : {DELTA:.15f}")
    print(f"  unnormalized weights       : {weights}")
    print(f"  target weights             : {target}")
    print(f"  normalized rho             : {rho}")
    print(f"  free energy at rho         : {free_energy(rho):.15f}")
    print(f"  stationarity residuals     : {stationarity}")

    print("\n[E] What this candidate derives internally")
    print("  1. WZ normalization gives Phi = pi/432 once the carrier is Delta_9 x J3(O).")
    print("  2. Ordered boundary idempotents break F4 covariantly and complete to a frame.")
    print("  3. Rank-3 Peirce grading on that frame gives N_B=(0,1,2).")
    print("  4. Endpoint flux gives Delta=-log(Phi)/2.")
    print("  5. Gibbs/entropy variation gives seed ratios (1, sqrt(Phi), Phi).")

    print("\n[F] What remains open")
    print("  Derive this boundary free-energy action from the full CHO dynamics. In")
    print("  particular, prove that the WZ boundary pair, carrier normalization, and")
    print("  entropy principle are forced rather than effective postulates.")

    print("\n[V] Sandbox verdict")
    print("  one coherent action candidate : FOUND")
    print("  full derivation from CHO      : OPEN")
    print("=" * 78)

    assert CARRIER_DIM == 432
    assert completion_residual < TOL
    assert max(orthogonality) < TOL
    assert max(covariance) < 1e-6
    assert max(abs(a - b) for a, b in zip(weights, target)) < 1e-14
    assert max(abs(x) for x in stationarity) < 1e-14
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
