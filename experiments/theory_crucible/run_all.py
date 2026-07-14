"""Run every dynamics-first theory-crucible gate."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
GATES = (
    "projector_rank_null.py",
    "fano_selection_no_go.py",
    "thermal_selection_tension.py",
    "observable_map_gate.py",
    "unitary_dynamics_gate.py",
    "projective_plane_census.py",
    "signed_fano_multiplication_census.py",
    "multiplication_stability_gate.py",
    "associator_discriminator_gate.py",
    "associator_quantum_measurement_gate.py",
    "associator_transport_dynamics_gate.py",
    "associator_quantum_control_gate.py",
    "octonion_symmetry_hamiltonian_gate.py",
)


def main() -> int:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    for gate in GATES:
        print(f"\n>>> {gate}", flush=True)
        result = subprocess.run(
            [sys.executable, str(ROOT / gate)],
            cwd=ROOT,
            env=environment,
            check=False,
        )
        if result.returncode != 0:
            print(f"\nTHEORY CRUCIBLE: FAIL ({gate}, exit {result.returncode})")
            return int(result.returncode)

    print("\n" + "=" * 74)
    print(f"THEORY CRUCIBLE: {len(GATES)}/{len(GATES)} GATES PASS")
    print("The associator controls generate u(7), but full symmetry selects only")
    print("a global phase; one oriented vacuum leaves two physical coefficients.")
    print("No CHO audit status, prediction hash, or Bayes credit was changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())