"""Discover and run every observer-consistency scientific test contract."""

from pathlib import Path
import sys
import unittest


def main() -> int:
    root = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(
        str(root / "tests"), pattern="test_gate_*.py"
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())