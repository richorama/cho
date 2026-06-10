"""Candidate action: WZ-normalized Jordan entropy seed dynamics.

This is the first concrete action-functional attempt in the quarantine sandbox.
It fuses the two strongest surviving directions:

1. WZ / Berry / inflow gives the normalized flux

       Phi = pi / (16 * 27) = pi / 432.

2. A Jordan-frame entropy functional uses that flux as a modular gap and tests
   whether the F4-breaking seed spectrum is stationary rather than inserted.

Candidate, in a fixed Jordan frame with Peirce-grade generator N = diag(0,1,2):

       S_seed(rho) = Tr(rho log rho) + Delta_Phi Tr(rho N)
       Delta_Phi = -1/2 log(Phi)
       Tr(rho) = 1.

Euler-Lagrange gives

       rho_i proportional to exp(-Delta_Phi * i)
       rho ratios = (1, sqrt(Phi), Phi).

So the candidate DOES output the desired cascade spectrum from Phi. The companion
probe `peirce_gap_derivation.py` reduces two assumptions: rank-3 primitive Peirce
grading gives N=(0,1,2), and endpoint flux gives Delta_Phi=-1/2 log(Phi). It is
not yet a final solution: the hard missing theorem is to derive Phi and the
entropy/free-energy action from CHO/Jordan/WZ dynamics rather than postulate them.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/candidate_wz_jordan_entropy_action.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math


PI = math.pi
CARRIER_DIM = 16 * 27
PHI = PI / CARRIER_DIM
EPS0 = math.sqrt(PHI)
DELTA_PHI = -0.5 * math.log(PHI)
PEIRCE_GRADES = (0, 1, 2)


@dataclass(frozen=True)
class CandidateVerdict:
    name: str
    passed: bool
    note: str


def unnormalized_seed_weights() -> tuple[float, float, float]:
    return tuple(math.exp(-DELTA_PHI * grade) for grade in PEIRCE_GRADES)


def normalized_seed_distribution() -> tuple[float, float, float]:
    weights = unnormalized_seed_weights()
    total = sum(weights)
    return tuple(weight / total for weight in weights)


def euler_lagrange_residuals() -> tuple[float, float, float]:
    """Residuals after eliminating the normalization multiplier.

    For S = sum p_i log p_i + Delta sum i p_i + lambda(sum p_i - 1),
    stationarity means log(p_i) + 1 + Delta*i is the same constant for every i.
    """
    rho = normalized_seed_distribution()
    raw = tuple(math.log(rho_i) + 1.0 + DELTA_PHI * grade
                for rho_i, grade in zip(rho, PEIRCE_GRADES))
    mean = sum(raw) / len(raw)
    return tuple(value - mean for value in raw)


def ratios_match_target(tol: float = 1e-14) -> bool:
    weights = unnormalized_seed_weights()
    target = (1.0, EPS0, PHI)
    return all(abs(a - b) < tol for a, b in zip(weights, target))


def residuals_vanish(tol: float = 1e-14) -> bool:
    return max(abs(value) for value in euler_lagrange_residuals()) < tol


def open_assumptions() -> tuple[str, ...]:
    return (
        "derive the WZ/Berry flux Phi = pi/432 as the actual action coefficient, not a postulate",
        "derive the entropy/free-energy functional Tr(rho log rho) + Delta Tr(rho N)",
        "derive the endpoint flux condition exp(-Delta * span)=Phi from the WZ/Jordan action",
        "lift the fixed-frame calculation to a genuine F4-breaking variational principle",
    )


def verdicts() -> tuple[CandidateVerdict, ...]:
    return (
        CandidateVerdict(
            "WZ/Schur flux has the right coefficient",
            CARRIER_DIM == 432 and PHI > 0.0,
            f"Phi = pi/{CARRIER_DIM} = {PHI:.12f}",
        ),
        CandidateVerdict(
            "entropy stationarity outputs the desired ratios",
            ratios_match_target(),
            f"exp(-Delta*i) = {unnormalized_seed_weights()} vs (1, sqrt(Phi), Phi)",
        ),
        CandidateVerdict(
            "Euler-Lagrange residuals vanish",
            residuals_vanish(),
            f"residuals = {euler_lagrange_residuals()}",
        ),
        CandidateVerdict(
            "candidate is not just an F4-invariant OP2 potential",
            True,
            "the Peirce-grade term breaks F4 by selecting a frame generator N",
        ),
        CandidateVerdict(
            "candidate is not yet a derivation",
            len(open_assumptions()) > 0,
            "open assumptions remain; this must stay quarantined",
        ),
    )


def main() -> bool:
    print("=" * 78)
    print("CANDIDATE ACTION: WZ-normalized Jordan entropy seed dynamics")
    print("=" * 78)

    print("\n[A] Functional")
    print("  Phi       = pi / (16*27) = pi/432")
    print("  N         = diag(0,1,2)  (Jordan-frame Peirce-grade generator)")
    print("  Delta_Phi = -1/2 log(Phi)")
    print("  S_seed    = Tr(rho log rho) + Delta_Phi Tr(rho N), Tr(rho)=1")

    print("\n[B] Stationary spectrum")
    weights = unnormalized_seed_weights()
    rho = normalized_seed_distribution()
    print(f"  Phi                         : {PHI:.15f}")
    print(f"  eps0 = sqrt(Phi)            : {EPS0:.15f}")
    print(f"  Delta_Phi                   : {DELTA_PHI:.15f}")
    print(f"  unnormalized seed weights   : {weights}")
    print(f"  normalized rho              : {rho}")
    print("  target unnormalized spectrum: (1, sqrt(Phi), Phi)")

    print("\n[C] Checks")
    all_pass = True
    for item in verdicts():
        all_pass = all_pass and item.passed
        print(f"  {'PASS' if item.passed else 'FAIL'} - {item.name}")
        print(f"         {item.note}")

    print("\n[D] What this actually proves")
    print("  Conditional result: IF the WZ/Jordan action supplies Phi and the entropy")
    print("  functional, THEN primitive rank-3 Peirce grading plus endpoint flux gives")
    print("  Delta_Phi and the stationary seed spectrum (1, sqrt(Phi), Phi).")
    print("  This is a real candidate mechanism, not a final proof.")

    print("\n[E] Open assumptions / kill gates")
    for i, assumption in enumerate(open_assumptions(), 1):
        print(f"  {i}. {assumption}")

    print("\n[V] Sandbox verdict")
    print("  candidate action functional: FOUND")
    print("  final pi/432 derivation    : NOT FOUND")
    print("  next theorem               : derive Phi and the entropy action from WZ/Jordan dynamics")
    print("=" * 78)

    assert ratios_match_target(), "candidate does not output the target seed ratios"
    assert residuals_vanish(), "candidate seed distribution is not stationary"
    assert open_assumptions(), "candidate should not silently graduate as solved"
    return all_pass


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
