"""Run every quarantined pi/432 sandbox probe."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
PROBES = (
    "moment_map_orbit_quantization.py",
    "anomaly_wz_inflow.py",
    "jordan_nonassoc_spectral_action.py",
    "wz_flux_normalization_gate.py",
    "wz_level_integrality_gate.py",
    "uniqueness_gate.py",
    "multi_factor_carrier_gate.py",
    "f4_invariant_action_census.py",
    "peirce_gap_derivation.py",
    "peirce_grade_reflection_gate.py",
    "seed_spectrum_reduction_gate.py",
    "entropy_principle_derivation.py",
    "frame_lift_f4_breaking.py",
    "f4_breaking_vacuum_gate.py",
    "unified_boundary_wz_jordan_action.py",
    "boundary_variation_gate.py",
    "boundary_metric_origin_gate.py",
    "oriented_wz_boundary_gate.py",
    "wz_chain_origin_gate.py",
    "action_origin_unification_gate.py",
    "candidate_wz_jordan_entropy_action.py",
    "exceptional_cs_higher_gauge.py",
    "freudenthal_unfolding.py",
    "exceptional_harmonic_analysis.py",
    "adelic_variational.py",
    "motivic_period_geometry.py",
    "topological_string_geometry.py",
    "exceptional_matrix_model.py",
    "categorical_state_sum.py",
)


def run_probe(path: Path) -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    print("=" * 78)
    print(f"RUNNING {path.name}")
    print("=" * 78)
    sys.stdout.flush()
    result = subprocess.run([sys.executable, str(path)], cwd=ROOT, env=env, text=True)
    print()
    return int(result.returncode)


def main() -> int:
    failures = []
    for probe in PROBES:
        code = run_probe(ROOT / probe)
        if code != 0:
            failures.append((probe, code))

    print("=" * 78)
    if failures:
        print("FULL SANDBOX SWEEP: FAIL")
        for probe, code in failures:
            print(f"  {probe}: exit {code}")
        return 1

    print("FULL SANDBOX SWEEP: PASS")
    print("No final derivation from full CHO dynamics yet. A unified boundary")
    print("CHO/Jordan/WZ action candidate now combines the gates: WZ-normalized")
    print("level-one Phi, F4-covariant ordered boundary pair, Jordan-frame completion,")
    print("Peirce grading, Gibbs entropy, and seed ratios. The boundary variation")
    print("gate forces an unordered orthogonal endpoint pair, and the metric-origin")
    print("gate identifies the overlap as the canonical F4 two-point contrast. The")
    print("oriented WZ gate supplies the sign that orders the grades, while the WZ-chain")
    print("origin gate identifies level one as the primitive integral CP1 class. WZ")
    print("integrality kills the continuous coefficient. The action-origin gate confirms the pieces")
    print("assemble as one effective boundary action, but the remaining theorem is")
    print("still to derive the F4-breaking oriented level-one boundary action, carrier,")
    print("and entropy principle from CHO dynamics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
