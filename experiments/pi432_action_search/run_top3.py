"""Run the quarantined top-three pi/432 action-search probes.

This runner is intentionally outside the core audit harness. It is a convenience
script for sandbox exploration only.
"""

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
        print("SANDBOX RESULT: FAIL")
        for probe, code in failures:
            print(f"  {probe}: exit {code}")
        return 1

    print("SANDBOX RESULT: PASS")
    print("Meaning: the top-three probes passed their cheap exact gates.")
    print("Not meaning: pi/432 has been derived.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
