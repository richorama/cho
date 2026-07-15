"""Exact precursor of observer consistency under microscopic relabeling."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from observer_bootstrap import FiniteExperiment, conjugate_experiment


def deterministic_preparation(dimension: int, state: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(index == state) for index in range(dimension))


def binary_effect(bits: tuple[int, ...]) -> tuple[Fraction, ...]:
    return tuple(Fraction(value) for value in bits)


def label_sensitive_score(experiment: FiniteExperiment) -> Fraction:
    """Deliberately invalid diagnostic that treats state names as magnitudes."""
    return sum(
        Fraction(index + 1) * probability
        for index, probability in enumerate(experiment.preparation)
    )


def run_gate() -> dict[str, int]:
    exact_checks = 0
    label_failures = 0
    for dimension in range(2, 6):
        all_permutations = tuple(permutations(range(dimension)))
        for update in all_permutations:
            for state in range(dimension):
                for effect_bits in product((0, 1), repeat=dimension):
                    experiment = FiniteExperiment(
                        deterministic_preparation(dimension, state),
                        update,
                        binary_effect(effect_bits),
                    )
                    for relabeling in all_permutations:
                        translated = conjugate_experiment(experiment, relabeling)
                        assert translated.probability() == experiment.probability()
                        exact_checks += 1
                        if label_sensitive_score(translated) != label_sensitive_score(experiment):
                            label_failures += 1

    assert exact_checks == 2_341_760
    assert label_failures > 0
    return {"exact_checks": exact_checks, "label_failures": label_failures}


def main() -> None:
    result = run_gate()
    print("=" * 72)
    print("BOOTSTRAP GATE 00: REPRESENTATION INVARIANCE")
    print("=" * 72)
    print(f"exact operational equalities checked : {result['exact_checks']}")
    print(f"label-sensitive discrepancies found  : {result['label_failures']}")
    print()
    print("PROVED")
    print("  * Jointly relabeling preparation, update, and effect preserves every")
    print("    enumerated operational probability exactly.")
    print("  * A diagnostic that assigns meaning to state labels is rejected.")
    print()
    print("NOT PROVED")
    print("  * consistency under information-losing coarse-graining;")
    print("  * emergence of quantum theory, locality, spacetime, or particles.")
    print()
    print("VERDICT: the representation-independence contract is executable. The")
    print("         first nontrivial target is agreement under coarse-graining.")


if __name__ == "__main__":
    main()