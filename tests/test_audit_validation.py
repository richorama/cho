import contextlib
import importlib
import io
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
COMPUTE_DIR = ROOT / "compute"
ARTIFACT_TIMEOUT_SECONDS = 180


def load_audit_module():
    compute_path = str(COMPUTE_DIR)
    if compute_path not in sys.path:
        sys.path.insert(0, compute_path)
    return importlib.import_module("audit")


AUDIT = load_audit_module()


def run_audit(*args, timeout=ARTIFACT_TIMEOUT_SECONDS):
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


def safe_test_suffix(name):
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_")


class AuditAssertions(unittest.TestCase):
    def assert_audit_success(self, result, tail=3000):
        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-tail:],
        )
        self.assertNotIn("Traceback", result.stdout)
        self.assertNotIn("Unknown artifact", result.stdout)


class AuditRegistryTests(unittest.TestCase):
    def test_artifact_entries_are_well_formed(self):
        for artifact_name, description, main in AUDIT.ARTIFACTS:
            with self.subTest(artifact=artifact_name):
                self.assertRegex(artifact_name, r"^[a-z0-9_]+$")
                self.assertTrue(description.strip())
                self.assertTrue(callable(main))

    def test_artifact_names_are_unique(self):
        artifact_names = [name for name, _, _ in AUDIT.ARTIFACTS]

        self.assertEqual(
            len(artifact_names),
            len(set(artifact_names)),
            msg="Audit artifact names must be unique for fine-grained validation.",
        )

    def test_run_all_dispatches_registered_artifacts(self):
        calls = []

        def make_probe(artifact_name):
            def probe():
                calls.append(artifact_name)

            return probe

        original_artifacts = AUDIT.ARTIFACTS
        probe_artifacts = [
            ("probe_alpha", "First probe artifact.", make_probe("probe_alpha")),
            ("probe_beta", "Second probe artifact.", make_probe("probe_beta")),
        ]
        try:
            AUDIT.ARTIFACTS = probe_artifacts
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                AUDIT.run_all()
        finally:
            AUDIT.ARTIFACTS = original_artifacts

        text = output.getvalue()
        self.assertEqual(calls, ["probe_alpha", "probe_beta"])
        self.assertIn(">>> [1/2] probe_alpha", text)
        self.assertIn(">>> [2/2] probe_beta", text)
        self.assertIn("AUDIT COMPLETE", text)


class AuditCliTests(AuditAssertions):
    def test_unknown_artifact_lists_available_artifacts(self):
        result = run_audit("not_a_real_artifact", timeout=30)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown artifact 'not_a_real_artifact'", result.stdout)
        self.assertIn("look_elsewhere", result.stdout)
        self.assertIn("scoreboard", result.stdout)


class AuditArtifactTests(AuditAssertions):
    pass


def make_artifact_test(artifact_name):
    def test_artifact(self):
        result = run_audit(artifact_name)

        self.assert_audit_success(result)

    test_artifact.__name__ = f"test_artifact_{safe_test_suffix(artifact_name)}"
    test_artifact.__qualname__ = f"AuditArtifactTests.{test_artifact.__name__}"
    return test_artifact


for name, _, _ in AUDIT.ARTIFACTS:
    setattr(
        AuditArtifactTests,
        f"test_artifact_{safe_test_suffix(name)}",
        make_artifact_test(name),
    )


class PredictionRegistryTests(AuditAssertions):
    def test_prediction_registry_is_locked(self):
        result = run_audit("prediction_registry")

        self.assert_audit_success(result)
        self.assertIn("AUDIT STATUS: PASS", result.stdout)
        self.assertIn("LOCKED", result.stdout)
        self.assertNotIn("DRIFT", result.stdout)

    def test_scoreboard_cli_reports_bottom_line(self):
        result = run_audit("scoreboard")

        self.assert_audit_success(result)
        self.assertIn("DERIVATION SCOREBOARD", result.stdout)


if __name__ == "__main__":
    unittest.main()
