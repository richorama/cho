"""
F0 normalized-measure witness: put the live H4 seam on trial.

`epsilon_measure_audit.py` checks the value and nearby alternatives. This witness
isolates the remaining theorem question: whether the normalized invariant
transition measure is forced by the already-named CHO ingredients, or still has
to be chosen. The current result is deliberately conservative: the witness is
coherent, but H4 remains OPEN.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_measure_witness.py
"""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MeasureCheck:
    name: str
    status: str
    value: str
    note: str


DIM_A_WEYL = 16
DIM_J3O = 27
TARGET = math.pi / (DIM_A_WEYL * DIM_J3O)


def measure_checks():
    return [
        MeasureCheck(
            "phase-space object",
            "PASS",
            "A_Weyl x J3(O)",
            "dimension 16 x 27 is supplied by the Spin(9) and Jordan witnesses",
        ),
        MeasureCheck(
            "rank-one kernel",
            "PASS",
            "rank = 1",
            "primitive idempotent / pure-generation vacuum is the active kernel",
        ),
        MeasureCheck(
            "angular weight",
            "PASS",
            "theta = pi",
            "Berry half-turn from the action/free-action two-level argument",
        ),
        MeasureCheck(
            "normalization rule H4",
            "OPEN",
            "Tr_transition / dim_phase_space",
            "invariant normalized measure is named but not yet derived from the action",
        ),
        MeasureCheck(
            "trace value under H4",
            "CONDITIONAL",
            f"{TARGET:.10f}",
            "equals pi/432 only if the H4 normalization rule is theorem-level",
        ),
    ]


def main():
    checks = measure_checks()
    print("=" * 78)
    print("  F0 NORMALIZED-MEASURE WITNESS")
    print("  Does the current structure force H4, or merely name it?")
    print("=" * 78)
    print()
    print(f"{'check':<28} {'status':<12} {'value':<28} note")
    print("-" * 78)
    for check in checks:
        print(f"{check.name:<28} {check.status:<12} {check.value:<28} {check.note}")
    print()
    print("AUDIT STATUS: PASS - H4 is isolated as the single normalized-measure seam.")
    print("THEOREM STATUS: OPEN - F0 is not promoted; demote if H4 remains chosen.")
    print()


if __name__ == "__main__":
    main()