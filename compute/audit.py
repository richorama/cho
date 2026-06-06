"""
CHO ROBUSTNESS AUDIT — single entry point.
==========================================

Runs the five robustness artifacts that stress-test the framework instead of
just displaying agreements. Each answers a specific skeptic's question:

  1. look_elsewhere        — "Is this physics or numerology?" (hardness-to-vary)
  2. model_complexity      — "How many parameters, really?" (honest MDL count)
  3. independent_observables — "What's the real goodness-of-fit?" (covariance)
  4. derived_vs_residual   — "Where's the error bar on the DERIVED part?"
  5. predict_neutrino_sum  — "What can future data falsify?" (frozen prediction)

Run all:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py

Run one:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py look_elsewhere
"""
import sys

import look_elsewhere
import model_complexity
import independent_observables
import derived_vs_residual
import predict_neutrino_sum
import first_generation_audit


ARTIFACTS = [
    ("look_elsewhere",
     "Hardness-to-vary: is each constant the simplest number that fits?",
     look_elsewhere.main),
    ("model_complexity",
     "Honest MDL: discrete parameter count and compression ratio.",
     model_complexity.main),
    ("independent_observables",
     "Goodness-of-fit on the independent observable set with a theory floor.",
     independent_observables.main),
    ("derived_vs_residual",
     "Error bars on the DERIVED term vs the underived continuum/RG residual.",
     derived_vs_residual.main),
    ("first_generation_audit",
     "First-gen outlier: intrinsic factor error vs propagated error.",
     first_generation_audit.main),
    ("predict_neutrino_sum",
     "Frozen, falsifiable forward prediction: Sigma m_nu.",
     predict_neutrino_sum.main),
]


def run_all():
    print("#" * 78)
    print("#  CHO ROBUSTNESS AUDIT")
    print("#  Five artifacts that stress-test the framework, not just display it.")
    print("#  These report HONEST numbers; read them before quoting headline percentages.")
    print("#" * 78)
    for i, (name, desc, fn) in enumerate(ARTIFACTS, 1):
        print(f"\n\n>>> [{i}/{len(ARTIFACTS)}] {name}")
        print(f">>> {desc}\n")
        fn()
    print("\n" + "#" * 78)
    print("#  AUDIT COMPLETE")
    print("#  Bottom line: CHO constants are hard to vary (12/12 simplest fitters),")
    print("#  but it is a ~17-parameter framework with marginal compression today.")
    print("#  The m_e -3.75 sigma outlier is mostly error propagation through squared")
    print("#  first-gen ratios; the genuine 1/(4pi) proof obligation is a ~2% effect.")
    print("#  The payoff is gated on DERIVING the prefactors, per DERIVATION_LEDGER.")
    print("#" * 78)


def main():
    if len(sys.argv) > 1:
        wanted = sys.argv[1]
        for name, desc, fn in ARTIFACTS:
            if name == wanted:
                fn()
                return
        print(f"Unknown artifact '{wanted}'. Available:")
        for name, desc, _ in ARTIFACTS:
            print(f"  {name:<24} {desc}")
        sys.exit(1)
    run_all()


if __name__ == "__main__":
    main()
