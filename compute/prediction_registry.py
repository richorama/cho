"""
Prediction registry — tamper-evident pre-registration of the frozen falsifiers.
===============================================================================

A forward prediction is only worth credit if it is on the record BEFORE the
deciding measurement. This module turns the frozen CHO predictions into a
tamper-evident manifest: it recomputes each prediction's numbers from the live
code, serialises them canonically, and prints a SHA-256 digest per prediction
plus a single manifest digest over all of them, stamped with the frozen date.

Commit the printed digest (e.g. in git, or publicly) on the frozen date. If any
prediction is silently retuned later, its recomputed digest will no longer match
the committed one -- the change becomes detectable instead of deniable. This is
the discipline that separates a genuine prediction from a postdiction.

Covered predictions (all dated 2026-06-06):
  Sigma m_nu        — predict_neutrino_sum.py
  P1 m_nu3 tension  — forward_predictions.predict_p1
  P2 m_betabeta     — forward_predictions.predict_p2
  P3 kappa_lambda   — forward_predictions.predict_p3

No scipy. Standard library hashlib + json only (plus the prediction modules).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/prediction_registry.py
"""

import hashlib
import io
import json
from contextlib import redirect_stdout

import forward_predictions
import predict_neutrino_sum


FROZEN_DATE = "2026-06-06"


def _quiet(fn, *args, **kwargs):
    """Call fn while suppressing its stdout; return its value."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        return fn(*args, **kwargs)


def _canon(obj):
    """Canonical JSON for hashing: sorted keys, fixed float formatting."""
    def fix(x):
        if isinstance(x, float):
            return float(f"{x:.10g}")
        if isinstance(x, dict):
            return {k: fix(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [fix(v) for v in x]
        return x

    return json.dumps(fix(obj), sort_keys=True, separators=(",", ":"))


def _digest(payload):
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def collect_predictions():
    """Recompute every frozen prediction's numbers from the live code."""
    p1 = _quiet(forward_predictions.predict_p1)
    p2 = _quiet(forward_predictions.predict_p2)
    p3 = _quiet(forward_predictions.predict_p3)

    # Sigma m_nu central band from predict_neutrino_sum (CHO-internal).
    s_lo, _ = predict_neutrino_sum.cho_internal_sum(0.0)
    s_hi, _ = predict_neutrino_sum.cho_internal_sum(0.005)
    sigma_mnu = {
        "sum_lo_meV": s_lo * 1e3,
        "sum_hi_meV": s_hi * 1e3,
        "m_nu3_meV": predict_neutrino_sum.m_nu3_cho * 1e3,
        "ordering": "normal",
    }

    return [
        ("Sigma_m_nu", "predict_neutrino_sum.py", sigma_mnu),
        ("P1_m_nu3_tension", "forward_predictions.predict_p1", p1),
        ("P2_m_betabeta", "forward_predictions.predict_p2", p2),
        ("P3_kappa_lambda", "forward_predictions.predict_p3", p3),
    ]


def main():
    print("=" * 78)
    print("  CHO PREDICTION REGISTRY — tamper-evident pre-registration")
    print(f"  Frozen date: {FROZEN_DATE}")
    print("  Commit these digests publicly; a later silent retune will not match.")
    print("=" * 78)

    preds = collect_predictions()
    manifest = {"frozen_date": FROZEN_DATE, "predictions": {}}

    print(f"\n  {'prediction':<20}{'source':<34}{'sha256 (first 16)':>18}")
    print("  " + "-" * 72)
    for name, source, values in preds:
        record = {"source": source, "frozen_date": FROZEN_DATE, "values": values}
        payload = _canon(record)
        d = _digest(payload)
        manifest["predictions"][name] = {"digest": d, "values": _canon(values)}
        print(f"  {name:<20}{source:<34}{d[:16]:>18}")

    manifest_payload = _canon(manifest)
    manifest_digest = _digest(manifest_payload)

    print("  " + "-" * 72)
    print("\n  Per-prediction frozen values:")
    for name, source, values in preds:
        compact = ", ".join(
            f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}"
            for k, v in values.items()
        )
        print(f"    {name:<20} {compact}")

    print(f"\n  MANIFEST SHA-256 (over all predictions + frozen date):")
    print(f"    {manifest_digest}")
    print("\n  Verification: re-run this module on any later commit. A matching")
    print("  manifest digest proves the frozen predictions were not altered; a")
    print("  mismatch localises exactly which prediction changed (per-row digests")
    print("  above). Record any intentional revision as a NEW dated entry, never")
    print("  by overwriting a frozen one.")
    print()
    return manifest_digest


if __name__ == "__main__":
    main()
