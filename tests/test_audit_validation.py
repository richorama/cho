import importlib
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run_audit(*args, timeout=600):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [PYTHON, "compute/audit.py", *args],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
    )


class AuditValidationTests(unittest.TestCase):
    def test_full_audit_completes(self):
        sys.path.insert(0, str(ROOT / "compute"))
        audit = importlib.import_module("audit")

        result = run_audit(timeout=900)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-5000:],
        )
        self.assertNotIn("Traceback", result.stdout)
        self.assertIn("AUDIT COMPLETE", result.stdout)
        self.assertEqual(
            result.stdout.count(">>> ["),
            len(audit.ARTIFACTS),
            msg="Full audit did not run the expected artifact count.",
        )

    def test_single_artifact_cli_completes(self):
        result = run_audit("scoreboard", timeout=180)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-3000:],
        )
        self.assertNotIn("Traceback", result.stdout)
        self.assertIn("DERIVATION SCOREBOARD", result.stdout)
        self.assertNotIn("Unknown artifact", result.stdout)

    def test_prediction_registry_is_locked(self):
        result = run_audit("prediction_registry", timeout=180)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-3000:],
        )
        self.assertIn("AUDIT STATUS: PASS", result.stdout)
        self.assertIn("LOCKED", result.stdout)
        self.assertNotIn("DRIFT", result.stdout)


if __name__ == "__main__":
    unittest.main()
