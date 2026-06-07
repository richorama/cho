"""
Prediction registry -- locked pre-registration of frozen future tests.
=====================================================================

A future-facing prediction is useful only if it is still on the record when the
deciding measurement arrives. This module is the Phase 6 registry gate:

* positive quantitative targets are separated from bridge sensitivities;
* each entry records formula, frozen inputs, experimental channel, kill condition;
* each value payload has a stored SHA-256 digest;
* the manifest digest is locked, so silent retuning fails the audit.

Revision rule: add a NEW dated entry when data or theory force an update. Never
overwrite an old frozen entry.

No scipy. Standard library hashlib + json only, plus the prediction modules.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/prediction_registry.py
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import io
import json
import math
from contextlib import redirect_stdout

import forward_predictions
import predict_neutrino_sum


REGISTRY_VERSION = 2
UPDATE_PROTOCOL = (
    "New data or a theoretical revision creates a new dated registry entry; "
    "old frozen entries and hashes are never overwritten."
)


@dataclass(frozen=True)
class FrozenEntry:
    name: str
    frozen_date: str
    category: str
    source: str
    formula: str
    frozen_inputs: tuple[str, ...]
    experimental_channel: str
    kill_condition: str
    expected_digest: str
    value_fn: object


def _quiet(fn, *args, **kwargs):
    """Call fn while suppressing stdout; return its value."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        return fn(*args, **kwargs)


def _canon(obj):
    """Canonical JSON for hashing: sorted keys, fixed float formatting."""
    def fix(x):
        if isinstance(x, float):
            return float(f"{x:.10g}")
        if isinstance(x, dict):
            return {key: fix(value) for key, value in x.items()}
        if isinstance(x, (list, tuple)):
            return [fix(value) for value in x]
        return x

    return json.dumps(fix(obj), sort_keys=True, separators=(",", ":"))


def _digest(payload):
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _value_digest(entry, values):
    record = {
        "source": entry.source,
        "frozen_date": entry.frozen_date,
        "values": values,
    }
    return _digest(_canon(record))


def sigma_m_nu_values():
    """Sigma m_nu central band from predict_neutrino_sum (CHO-internal)."""
    sum_lo, _ = predict_neutrino_sum.cho_internal_sum(0.0)
    sum_hi, _ = predict_neutrino_sum.cho_internal_sum(0.005)
    return {
        "sum_lo_meV": sum_lo * 1e3,
        "sum_hi_meV": sum_hi * 1e3,
        "m_nu3_meV": predict_neutrino_sum.m_nu3_cho * 1e3,
        "ordering": "normal",
    }


def theta23_octant_values():
    """Phase 6 explicit theta23 octant target from the Fano-line count."""
    sin2_theta23 = 4.0 / 7.0
    return {
        "sin2_theta23": sin2_theta23,
        "theta23_deg": math.degrees(math.asin(math.sqrt(sin2_theta23))),
        "octant": "upper",
    }


def p1_values():
    return _quiet(forward_predictions.predict_p1)


def p2_values():
    return _quiet(forward_predictions.predict_p2)


def p3_values():
    return _quiet(forward_predictions.predict_p3)


FROZEN_ENTRIES = [
    FrozenEntry(
        name="Sigma_m_nu",
        frozen_date="2026-06-06",
        category="positive_quantitative",
        source="predict_neutrino_sum.py",
        formula=(
            "Normal ordering; m_nu3 = v^2/(2*(M_P/3^9)); "
            "m2 = sqrt(max(m_nu3^2 - Delta m31^2, 0) + Delta m21^2); "
            "Sigma = m1 + m2 + m3 for m1 in [0, 5] meV."
        ),
        frozen_inputs=(
            "M_P = 1.221e19 GeV",
            "v = 246.22 GeV",
            "Delta m21^2 = 7.42e-5 eV^2",
            "Delta m31^2 = 2.510e-3 eV^2",
            "lightest state m1 in [0, 5] meV",
        ),
        experimental_channel="DESI, Euclid, CMB-S4, LiteBIRD; JUNO/DUNE/Hyper-K for ordering",
        kill_condition=(
            "Inverted ordering, robust Sigma m_nu far outside the 57-62 meV band "
            "after systematics, or a terrestrial m_nu3 incompatible with the CHO seesaw scale."
        ),
        expected_digest="acfc9596b509cd0ec9e1a813f44f49bffa573247fbf373cd356d2e74cf32d86d",
        value_fn=sigma_m_nu_values,
    ),
    FrozenEntry(
        name="Theta23_octant",
        frozen_date="2026-06-07",
        category="positive_quantitative",
        source="epsilon_mixing_coefficients.py:Fano avoiding/total line count",
        formula="sin^2(theta23) = 4/7 from Fano lines avoiding the vacuum over all seven lines.",
        frozen_inputs=(
            "vacuum point fixed by omega = (1 + i e7)/2",
            "Fano lines avoiding the vacuum = 4",
            "total Fano lines = 7",
        ),
        experimental_channel="DUNE, Hyper-K, NuFit/global PMNS updates",
        kill_condition="Stable lower-octant theta23 or upper-octant value incompatible with 4/7 after global fits settle.",
        expected_digest="8d50b686829815414cc5847726b32c74fc140cf0dec6d3614782227afa448725",
        value_fn=theta23_octant_values,
    ),
    FrozenEntry(
        name="P2_m_betabeta",
        frozen_date="2026-06-06",
        category="positive_quantitative",
        source="forward_predictions.predict_p2",
        formula=(
            "m_betabeta = |sin^2(theta12) cos^2(theta13) m2 + "
            "exp(i alpha) sin^2(theta13) m3| with alpha free, normal ordering, m1 ~= 0."
        ),
        frozen_inputs=(
            "sin^2(theta12) = 1/(3 + sqrt(7)*epsilon0)",
            "sin^2(theta13) = 3*epsilon0^2",
            "epsilon0^2 = pi/432",
            "Delta m21^2 = 7.42e-5 eV^2",
            "Delta m31^2 = 2.510e-3 eV^2",
        ),
        experimental_channel="LEGEND-1000, nEXO, next-generation 0nu beta beta searches",
        kill_condition="Confirmed 0nu beta beta signal implying m_betabeta > ~10 meV.",
        expected_digest="40ca0216983340e59a3b9f713897179d614118cb21958d33109d02b5ddb464cd",
        value_fn=p2_values,
    ),
    FrozenEntry(
        name="P1_m_nu3_tension",
        frozen_date="2026-06-06",
        category="bridge_sensitivity",
        source="forward_predictions.predict_p1",
        formula="m_nu3 = v^2/(2*(M_P/3^9)) compared against sqrt(Delta m31^2).",
        frozen_inputs=(
            "M_P = 1.221e19 GeV",
            "v = 246.22 GeV",
            "Delta m31^2 = 2.510e-3 eV^2",
            "allowed uncomputed threshold/RG lift: O(few percent)",
        ),
        experimental_channel="JUNO, DUNE, Hyper-K, global oscillation fits",
        kill_condition="The m_nu3 floor gap grows beyond any few-percent threshold/RG correction without adding a new knob.",
        expected_digest="c1a30b6a7fffebcb50dd4bb5db759c68ff40e89d9567d3d46d050d62bc3c8a7e",
        value_fn=p1_values,
    ),
    FrozenEntry(
        name="P3_kappa_lambda",
        frozen_date="2026-06-06",
        category="bridge_sensitivity",
        source="forward_predictions.predict_p3",
        formula="kappa_lambda = (pi/24)/(m_H^2/(2 v^2)) at the CHO matching level.",
        frozen_inputs=(
            "lambda_CHO = pi/24",
            "m_H = 125.09 GeV",
            "v = 246.22 GeV",
            "threshold/RG matching still open",
        ),
        experimental_channel="HL-LHC, FCC-ee/hh, future Higgs factories",
        kill_condition="Large confirmed |kappa_lambda - 1| from an extended Higgs sector after matching uncertainties are settled.",
        expected_digest="1154d8bc36c30e0ca811d3463a87a13007f232fa23508475a4b04f13f08fc26e",
        value_fn=p3_values,
    ),
]


EXPECTED_MANIFEST_DIGEST = "21cba7701a8292bc96a44d96b7e13b66f6e21fcbd56595257a517ae47875836f"


def collect_predictions():
    """Backward-compatible tuple view used by older tooling."""
    return [(entry.name, entry.source, entry.value_fn()) for entry in FROZEN_ENTRIES]


def collect_registry_rows():
    rows = []
    for entry in FROZEN_ENTRIES:
        values = entry.value_fn()
        digest = _value_digest(entry, values)
        rows.append({"entry": entry, "values": values, "digest": digest})
    return rows


def manifest_digest(rows):
    manifest = {
        "registry_version": REGISTRY_VERSION,
        "update_protocol": UPDATE_PROTOCOL,
        "entries": [
            {
                "name": row["entry"].name,
                "frozen_date": row["entry"].frozen_date,
                "category": row["entry"].category,
                "source": row["entry"].source,
                "expected_digest": row["entry"].expected_digest,
            }
            for row in rows
        ],
    }
    return _digest(_canon(manifest))


def print_category(rows, category, title):
    selected = [row for row in rows if row["entry"].category == category]
    print(title)
    print("-" * 78)
    for row in selected:
        entry = row["entry"]
        values = row["values"]
        compact = ", ".join(
            f"{key}={value:.5g}" if isinstance(value, float) else f"{key}={value}"
            for key, value in values.items()
        )
        status = "LOCKED" if row["digest"] == entry.expected_digest else "DRIFT"
        print(f"{status:<6} {entry.name:<20} {entry.frozen_date:<10} {row['digest'][:16]}")
        print(f"       values: {compact}")
        print(f"       channel: {entry.experimental_channel}")
        print(f"       kill: {entry.kill_condition}")
    print()


def validate_rows(rows):
    failures = []
    for row in rows:
        entry = row["entry"]
        if row["digest"] != entry.expected_digest:
            failures.append((entry.name, entry.expected_digest, row["digest"]))
    current_manifest = manifest_digest(rows)
    if current_manifest != EXPECTED_MANIFEST_DIGEST:
        failures.append(("MANIFEST", EXPECTED_MANIFEST_DIGEST, current_manifest))
    return failures, current_manifest


def main():
    print("=" * 78)
    print("  CHO PREDICTION REGISTRY -- Phase 6 locked future-test manifest")
    print(f"  Registry version: {REGISTRY_VERSION}")
    print("=" * 78)
    print()
    print(f"UPDATE PROTOCOL: {UPDATE_PROTOCOL}")
    print()

    rows = collect_registry_rows()
    print_category(rows, "positive_quantitative", "POSITIVE QUANTITATIVE PREDICTIONS")
    print_category(rows, "bridge_sensitivity", "BRIDGE SENSITIVITIES / PRESSURE TESTS")

    print("FROZEN FORMULAS AND INPUTS")
    print("-" * 78)
    for row in rows:
        entry = row["entry"]
        print(f"{entry.name}:")
        print(f"  formula: {entry.formula}")
        print("  frozen inputs:")
        for item in entry.frozen_inputs:
            print(f"    - {item}")
    print()

    failures, current_manifest = validate_rows(rows)
    print("MANIFEST")
    print("-" * 78)
    print(f"expected: {EXPECTED_MANIFEST_DIGEST}")
    print(f"current : {current_manifest}")
    if failures:
        print()
        print("AUDIT STATUS: FAIL - frozen prediction drift detected.")
        for name, expected, current in failures:
            print(f"  {name}: expected {expected}, got {current}")
        print("Add a new dated registry entry for intentional revisions; do not overwrite old ones.")
        raise SystemExit(1)

    print()
    print("AUDIT STATUS: PASS - all frozen prediction hashes match the locked manifest.")
    print("NULL EXCLUSIONS: tracked separately in FUTURE_TESTS.md; they are not counted")
    print("as positive confirmations, only as future falsification windows.")
    print()
    return current_manifest


if __name__ == "__main__":
    main()
