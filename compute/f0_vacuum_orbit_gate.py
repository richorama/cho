"""
F0 vacuum-orbit gate: does the vacuum stabilizer select one transition-ray orbit?

This is the next closure-critical checkpoint after the action-stationarity gate.
It does not try to derive the full CHO action. It asks a narrower question:

    once the vacuum point is fixed, does the Fano-pair transition class collapse
    to a single stabilizer orbit, so the ray representative is no longer chosen
    by hand?

If this passes, the ray-selection seam is narrowed to the remaining CHO-action
derivation of the physical representative. If it fails, the current ray still
has more than one orbit representative and the seam is not yet closed enough to
carry forward.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_vacuum_orbit_gate.py
"""

from __future__ import annotations

from spurion_bridge import derive_vacuum_orbit


def main() -> bool:
    result = derive_vacuum_orbit()

    print("=" * 78)
    print("  F0 VACUUM-ORBIT GATE")
    print("  Does the fixed vacuum collapse the transition-ray degeneracy to one orbit?")
    print("=" * 78)
    print()
    print(f"  automorphism group order        : {result.automorphism_count}")
    print(f"  vacuum stabilizer order         : {result.stabilizer_order}")
    print(f"  full-group line-pair orbit sizes : {result.full_orbit_sizes}")
    print(f"  stabilizer orbit sizes          : {result.stabilizer_orbit_sizes}")
    print(f"  transition class size           : {result.transition_class_size}")
    print(f"  single stabilizer orbit         : {result.transition_is_single_orbit}")
    print()

    if result.transition_is_single_orbit:
        print("  PASS: fixing the vacuum reduces the transition class to one orbit.")
        print("  This selects the ray representative up to residual gauge, not by hand.")
        return True

    print("  FAIL: the transition class still splits into multiple stabilizer orbits.")
    print("  The ray representative remains underdetermined.")
    return False


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)