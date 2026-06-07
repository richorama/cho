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
AUDIT_CONTRACT = importlib.import_module("audit_contract")
PREDICTION_REGISTRY = importlib.import_module("prediction_registry")
PHYSICS_MAP_AUDIT = importlib.import_module("physics_map_audit")
RG_MATCHING_AUDIT = importlib.import_module("rg_matching_audit")


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


def run_audit_contract(timeout=ARTIFACT_TIMEOUT_SECONDS):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [PYTHON, "compute/audit_contract.py"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
    )


def run_python_script(script, *args, timeout=ARTIFACT_TIMEOUT_SECONDS):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [PYTHON, script, *args],
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
    def test_audit_contract_cli_completes(self):
        result = run_audit_contract(timeout=30)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-3000:],
        )
        self.assertIn("AUDIT STATUS: PASS", result.stdout)

    def test_audit_contract_json_cli_completes(self):
        result = run_python_script("compute/audit_contract.py", "--json", timeout=30)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-3000:],
        )
        self.assertIn('"audit_status": "PASS"', result.stdout)
        self.assertIn('"contracts"', result.stdout)

    def test_claim_status_report_cli_completes(self):
        result = run_python_script("compute/claim_status_report.py", timeout=30)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-3000:],
        )
        self.assertIn("CHO CLAIM STATUS REPORT", result.stdout)
        self.assertIn("OPEN_BRIDGE", result.stdout)

    def test_unknown_artifact_lists_available_artifacts(self):
        result = run_audit("not_a_real_artifact", timeout=30)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown artifact 'not_a_real_artifact'", result.stdout)
        self.assertIn("look_elsewhere", result.stdout)
        self.assertIn("scoreboard", result.stdout)


class AuditContractTests(unittest.TestCase):
    def test_contract_covers_registered_artifacts(self):
        artifact_names = [name for name, _, _ in AUDIT.ARTIFACTS]

        self.assertEqual(
            [],
            AUDIT_CONTRACT.validate_contracts(artifact_names),
        )

    def test_prediction_contract_matches_locked_registry(self):
        positive_prediction_names = tuple(
            entry.name
            for entry in PREDICTION_REGISTRY.FROZEN_ENTRIES
            if entry.category == "positive_quantitative"
        )
        bridge_sensitivity_names = tuple(
            entry.name
            for entry in PREDICTION_REGISTRY.FROZEN_ENTRIES
            if entry.category == "bridge_sensitivity"
        )

        self.assertEqual(
            [],
            AUDIT_CONTRACT.validate_prediction_contract(
                positive_prediction_names,
                bridge_sensitivity_names,
            ),
        )

    def test_contract_ledger_ids_exist(self):
        ledger_text = (ROOT / "DERIVATION_LEDGER.md").read_text()
        ledger_ids = set(re.findall(r"^\|\s*([A-Z]+[0-9]+)\s*\|", ledger_text, flags=re.MULTILINE))
        contract_ids = {
            ledger_id
            for contract in AUDIT_CONTRACT.CONTRACTS.values()
            for ledger_id in contract.ledger_ids
        }

        self.assertEqual(
            set(),
            contract_ids - ledger_ids,
            msg="Every contract ledger ID must exist in DERIVATION_LEDGER.md.",
        )

    def test_open_and_exploratory_contracts_have_kill_conditions(self):
        statuses = {
            AUDIT_CONTRACT.STATUS_OPEN_BRIDGE,
            AUDIT_CONTRACT.STATUS_EXPLORATORY,
        }
        missing = [
            contract.artifact
            for contract in AUDIT_CONTRACT.CONTRACTS.values()
            if contract.status in statuses and not contract.kill_conditions
        ]

        self.assertEqual([], missing)

    def test_epsilon_measure_remains_the_open_hinge(self):
        contract = AUDIT_CONTRACT.CONTRACTS["epsilon_measure_audit"]

        self.assertEqual(AUDIT_CONTRACT.STATUS_OPEN_BRIDGE, contract.status)
        self.assertEqual(AUDIT_CONTRACT.VERDICT_OPEN, contract.verdict)
        self.assertIn("F0", contract.ledger_ids)
        self.assertTrue(contract.open_bridges)
        self.assertIn("Bayes hinge", contract.public_claim_policy)

    def test_gravity_gate_keeps_gravity_out_of_scope(self):
        contract = AUDIT_CONTRACT.CONTRACTS["gravity_gate_audit"]

        self.assertEqual(AUDIT_CONTRACT.STATUS_OUT_OF_SCOPE, contract.status)
        self.assertEqual(AUDIT_CONTRACT.VERDICT_DEMOTED, contract.verdict)
        self.assertIn("GR1", contract.ledger_ids)
        self.assertTrue(contract.kill_conditions)
        self.assertIn("out of scope", contract.public_claim_policy)

    def test_one_operator_gate_remains_open(self):
        contract = AUDIT_CONTRACT.CONTRACTS["yukawa_operator_full"]

        self.assertEqual(AUDIT_CONTRACT.STATUS_OPEN_BRIDGE, contract.status)
        self.assertEqual(AUDIT_CONTRACT.VERDICT_OPEN, contract.verdict)
        self.assertIn("C4", contract.ledger_ids)
        self.assertTrue(contract.open_bridges)


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

    def test_prediction_registry_markdown_export(self):
        result = run_python_script("compute/prediction_registry.py", "--markdown", timeout=60)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout[-3000:],
        )
        self.assertIn("# Locked Prediction Registry Summary", result.stdout)
        self.assertIn("Positive Quantitative Predictions", result.stdout)
        self.assertIn("Bridge Sensitivities", result.stdout)
        self.assertIn("Sigma_m_nu", result.stdout)


class RobustnessTrackTests(unittest.TestCase):
    def test_rg_inverse_matches_are_not_labelled_derived(self):
        inverse_scales = [
            scale
            for scale in RG_MATCHING_AUDIT.candidate_scales()
            if "INVERSE" in scale.status
        ]

        self.assertTrue(inverse_scales)
        for scale in inverse_scales:
            with self.subTest(scale=scale.name):
                self.assertIn("target-implied", scale.name)
                self.assertNotIn("DERIVED", scale.status)

    def test_physics_map_tracks_three_frame_copies(self):
        copies = PHYSICS_MAP_AUDIT.generation_frame_copies()

        self.assertEqual(3, len(copies))
        self.assertEqual({16}, {copy.field_count for copy in copies})
        self.assertTrue(all("no per-field choices" in copy.map_status for copy in copies))


if __name__ == "__main__":
    unittest.main()
