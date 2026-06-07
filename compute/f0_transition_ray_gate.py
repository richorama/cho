"""
F0 transition-ray gate: consistency check for the physical ray representative.

This artifact does not claim to derive the transition ray from full CHO action
dynamics. It asks the next practical question after the vacuum-orbit and
action-stationarity gates:

1. Does the fixed vacuum collapse the Fano transition class to one stabilizer
   orbit?
2. Does the written-down free action select the great-circle holonomy theta=pi?
3. Is the trace space still uniquely A_Weyl x J3(O) (16 x 27)?

If all three pass, the remaining seam is a single named gap: the physical ray
representative is consistent with the orbit, the holonomy, and the trace space,
but still has to be derived from the full CHO dynamics rather than inserted.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_transition_ray_gate.py
"""

from __future__ import annotations

from action_derivation import derive_theta_from_action
from spurion_bridge import derive_trace_space, derive_vacuum_orbit


def main() -> bool:
    vacuum = derive_vacuum_orbit()
    action = derive_theta_from_action()
    trace_selected, _trace_candidates = derive_trace_space()

    print("=" * 78)
    print("  F0 TRANSITION-RAY CONSISTENCY GATE")
    print("  Vacuum orbit + free action + trace space: do they select one ray?")
    print("=" * 78)
    print()
    print(f"  vacuum stabilizer selects one orbit : {vacuum.transition_is_single_orbit}")
    print(f"  action-selected theta is pi         : {action.theta_is_pi}")
    print(f"  action-selected great circle        : {action.geodesic_selected}")
    print(f"  unique trace space                  : {trace_selected.is_selected}")
    print(f"  trace space dimension               : {trace_selected.dim}")
    print()

    all_pass = bool(
        vacuum.transition_is_single_orbit
        and action.theta_is_pi
        and action.geodesic_selected
        and trace_selected.is_selected
    )

    if all_pass:
        print("  PASS: the ray representative is consistent across orbit, holonomy,")
        print("  and trace-space checks.")
        print("  Residual seam: derive that representative directly from CHO dynamics.")
        return True

    print("  FAIL: at least one consistency check did not pass.")
    print("  The transition-ray representative is not yet stable enough to carry forward.")
    return False


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)