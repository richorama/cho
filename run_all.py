"""Run every executable observer-consistency gate."""

from experiments.gate_00_representation_invariance import main as gate_00


def main() -> None:
    gate_00()
    print()
    print("BOOTSTRAP: 1/1 GATES PASS")


if __name__ == "__main__":
    main()