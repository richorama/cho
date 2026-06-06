"""
CHO ROBUSTNESS AUDIT — single entry point.
==========================================

Runs the robustness artifacts that stress-test the framework instead of just
displaying agreements. Each answers a specific skeptic's question:

  1. look_elsewhere        — "Is this physics or numerology?" (hardness-to-vary)
  2. model_complexity      — "How many parameters, really?" (honest MDL count)
  3. independent_observables — "What's the real goodness-of-fit?" (covariance)
  4. derived_vs_residual   — "Where's the error bar on the DERIVED part?"
  5. predict_neutrino_sum  — "What can future data falsify?" (frozen prediction)

plus the derivation-frontier experiments (the "can the algebra do more?" set):

  6. jordan_eigenvalue_generations — spectral route to three (Lever A)
  7. ko_dimension_chirality        — KO-dimension 6 chirality test (Lever B)
  8. ladder_charges                — SM charges {0,1/3,2/3,1} (Lever C)
  9. bayesian_evidence             — model-comparison Bayes factor vs a null
 10. spectral_action              — one algebra-internal Dirac operator (knobs)
 11. cross_generation_count       — inter-gen Yukawa knob count under triality
 12. epsilon_cubic_discriminant   — eps0 route 2: is the 27 the cubic discriminant?
 13. epsilon_heat_kernel          — eps0 route 1: which pi (Berry vs heat-kernel)?
 14. epsilon_state_count          — eps0 route 4: 432 as a geometric state count
 15. epsilon_product_space        — eps0 route 4b: is 432 a genuine product?
 16. epsilon_weyl_isomorphism     — eps0 route 4c: A_Weyl ~= T(OP^2) as Spin(9) spinors
 17. epsilon_spin9_embedding      — eps0 seam: gauge & flavour Spin(9) same subgroup
 18. epsilon_rank_one_kernel      — eps0 R1: rank-one kernel = primitive idempotent
 19. epsilon_free_action          — eps0 R2: free action forced by two-level symmetry
 20. epsilon_channel_coefficients — T1.3: mass-sector ranks (1,3,8) as Fock traces
 21. prediction_registry           — tamper-evident pre-registration hashes

Run all:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py

Run one:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py look_elsewhere
"""
import sys

import look_elsewhere
import model_complexity
import independent_observables
import covariance_gof
import derived_vs_residual
import predict_neutrino_sum
import forward_predictions
import first_generation_audit
import jordan_eigenvalue_generations
import ko_dimension_chirality
import ladder_charges
import bayesian_evidence
import spectral_action
import cross_generation_count
import epsilon_cubic_discriminant
import epsilon_heat_kernel
import epsilon_state_count
import epsilon_product_space
import epsilon_weyl_isomorphism
import epsilon_spin9_embedding
import epsilon_rank_one_kernel
import epsilon_free_action
import epsilon_channel_coefficients
import prediction_registry


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
    ("covariance_gof",
     "Covariance GoF: effective N_eff observables and correlated chi-square.",
     covariance_gof.main),
    ("derived_vs_residual",
     "Error bars on the DERIVED term vs the underived continuum/RG residual.",
     derived_vs_residual.main),
    ("first_generation_audit",
     "First-gen outlier: intrinsic factor error vs propagated error.",
     first_generation_audit.main),
    ("predict_neutrino_sum",
     "Frozen, falsifiable forward prediction: Sigma m_nu.",
     predict_neutrino_sum.main),
    ("forward_predictions",
     "Three more frozen falsifiers: m_nu3 tension, m_betabeta, Higgs self-coupling.",
     forward_predictions.main),
    ("jordan_eigenvalue_generations",
     "Lever A: spectral route to three (degree of the J3(O) cubic norm).",
     jordan_eigenvalue_generations.main),
    ("ko_dimension_chirality",
     "Lever B: KO-dimension 6 test -- chirality without fermion doubling.",
     ko_dimension_chirality.main),
    ("ladder_charges",
     "Lever C: SM charges {0,1/3,2/3,1} from the C x O number operator.",
     ladder_charges.main),
    ("bayesian_evidence",
     "Model-comparison Bayes factor: CHO vs an O(1)-numerology null.",
     bayesian_evidence.main),
    ("spectral_action",
     "Inverse-spectral: one algebra-internal Dirac operator, knobs vs forced ratios.",
     spectral_action.main),
    ("cross_generation_count",
     "Inverse-spectral: inter-generation Yukawa knob count under NNI + triality.",
     cross_generation_count.main),
    ("epsilon_cubic_discriminant",
     "Eps0 route 2: tests whether the 27 in pi/432 is the Freudenthal-cubic discriminant.",
     epsilon_cubic_discriminant.main),
    ("epsilon_heat_kernel",
     "Eps0 route 1: which pi -- bare Berry flux vs heat-kernel (4pi)^(-d/2).",
     epsilon_heat_kernel.main),
    ("epsilon_state_count",
     "Eps0 route 4: 432 = dim(OP^2) x dim(J3(O)) as a geometric state count.",
     epsilon_state_count.main),
    ("epsilon_product_space",
     "Eps0 route 4b: stratify 27=1+16+10; is 432 a genuine product? names the open isomorphism.",
     epsilon_product_space.main),
    ("epsilon_weyl_isomorphism",
     "Eps0 route 4c: A_Weyl ~= T(OP^2) -- both are the unique 16-dim real Spin(9) spinor.",
     epsilon_weyl_isomorphism.main),
    ("epsilon_spin9_embedding",
     "Eps0 seam: gauge & flavour Spin(9) are the same subgroup (octonionic Cl(9), O(16)-conjugate).",
     epsilon_spin9_embedding.main),
    ("epsilon_rank_one_kernel",
     "Eps0 R1: the rank-one kernel is a primitive idempotent = pure single-generation vacuum.",
     epsilon_rank_one_kernel.main),
    ("epsilon_free_action",
     "Eps0 R2: the free action + topological term is the unique two-level-symmetric action.",
     epsilon_free_action.main),
    ("epsilon_channel_coefficients",
     "T1.3: mass-sector ranks (1,3,8) as number-operator Fock-grade traces (closes M3).",
     epsilon_channel_coefficients.main),
    ("prediction_registry",
     "Tamper-evident pre-registration: SHA-256 digests of the frozen predictions.",
     prediction_registry.main),
]


def run_all():
    print("#" * 78)
    print("#  CHO ROBUSTNESS AUDIT")
    print("#  Artifacts that stress-test the framework, not just display it.")
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
    print("#  Derivation frontier (Levers A-C): 'three' is also the rank of J3(O)")
    print("#  (spectral, obstruction-free); the internal space sits at KO-dimension 6")
    print("#  (chirality without doubling); and the C x O number operator yields the")
    print("#  SM charges {0,1/3,2/3,1}. But the model-comparison Bayes factor still")
    print("#  favours an O(1) null until the prefactors are DERIVED, not chosen.")
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
