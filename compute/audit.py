"""
CHO ROBUSTNESS AUDIT — single entry point.
==========================================

Runs the robustness artifacts that stress-test the framework instead of just
displaying agreements. Each answers a specific skeptic's question:

  1. look_elsewhere        — "Is this physics or numerology?" (hardness-to-vary)
  2. model_complexity      — "How many parameters, really?" (honest MDL count)
  3. independent_observables — "What's the real goodness-of-fit?" (covariance)
  4. derived_vs_residual   — "Where's the error bar on the DERIVED part?"
  *  rg_matching_audit     — Phase 4 gate: are continuum/RG scales derived or inverse-matched?
  5. predict_neutrino_sum  — "What can future data falsify?" (frozen prediction)

plus the derivation-frontier experiments (the "can the algebra do more?" set):

  6. jordan_eigenvalue_generations — spectral route to three (Lever A)
  7. ko_dimension_chirality        — KO-dimension 6 chirality test (Lever B)
  8. ladder_charges                — SM charges {0,1/3,2/3,1} (Lever C)
  *  weak_isospin_hypercharge      — weak SU(2) + hypercharge Y (Lever D)
  *  chiral_projector             — chiral idempotent closes the B<->D seam (C)
  *  physics_map_audit             — one-generation quantum-number map + anomaly cancellation
  9. bayesian_evidence             — model-comparison Bayes factor vs a null
 10. spectral_action              — one algebra-internal Dirac operator (knobs)
 11. cross_generation_count       — inter-gen Yukawa knob count under triality
    *  yukawa_operator_full        — Phase 3 gate: one operator or explicit flavour demotions
  *  three_generations_frame      — N_gen=3 crack: generations = 3 OP^2 idempotents, inner frame S3
 12. epsilon_cubic_discriminant   — eps0 route 2: is the 27 the cubic discriminant?
 13. epsilon_heat_kernel          — eps0 route 1: which pi (Berry vs heat-kernel)?
 14. epsilon_state_count          — eps0 route 4: 432 as a geometric state count
 15. epsilon_product_space        — eps0 route 4b: is 432 a genuine product?
 16. epsilon_weyl_isomorphism     — eps0 route 4c: A_Weyl ~= T(OP^2) as Spin(9) spinors
 17. epsilon_spin9_embedding      — eps0 seam: gauge & flavour Spin(9) same subgroup
 18. epsilon_rank_one_kernel      — eps0 R1: rank-one kernel = primitive idempotent
 19. epsilon_free_action          — eps0 R2: free action forced by two-level symmetry
 20. epsilon_channel_coefficients — T1.3: mass-sector ranks (1,3,8) as Fock traces
 21. epsilon_mixing_coefficients  — M11: mixing counts (7,3,4,4/7) as Fano lines + 1/(4pi)
 22. epsilon_vcb_halfangle        — C2: |V_cb| coefficient 1/2 = SU(2) spinor half-angle
 23. epsilon_a4_two_level         — R2 origin: two-level symmetry = SU(2) closure of A4
 24. epsilon_measure_audit        — Phase 2 gate: pi/432 as one conditional transition measure
    *  epsilon_measure_witness      — F0 H4 witness: normalized-measure seam isolated
  *  gravity_curvature            — M-GRAV: emergent rank-2 metric from non-associativity
  *  gravity_gate_audit           — Phase 5 gate: gravity remains exploratory unless Lorentzian dynamics close
 25. prediction_registry           — Phase 6 locked prediction registry + update protocol
  *  scoreboard                    — does deriving prefactors move the Bayes factor? (the one-number bottom line; runs last)

Run all:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py

Run one:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py look_elsewhere
"""
import sys

import look_elsewhere
import scale_look_elsewhere
import model_complexity
import independent_observables
import covariance_gof
import derived_vs_residual
import rg_matching_audit
import mass_ratio_rg_audit
import predict_neutrino_sum
import forward_predictions
import first_generation_audit
import jordan_eigenvalue_generations
import ko_dimension_chirality
import ladder_charges
import weak_isospin_hypercharge
import chiral_projector
import physics_map_audit
import bayesian_evidence
import spectral_action
import spectral_action_432
import epsilon_generation_ladder
import spurion_perturbation
import generation_cascade
import cross_generation_count
import yukawa_operator_full
import three_generations_frame
import epsilon_cubic_discriminant
import epsilon_heat_kernel
import epsilon_state_count
import epsilon_product_space
import epsilon_weyl_isomorphism
import epsilon_spin9_embedding
import epsilon_rank_one_kernel
import epsilon_free_action
import epsilon_channel_coefficients
import epsilon_mixing_coefficients
import epsilon_vcb_halfangle
import epsilon_a4_two_level
import epsilon_measure_audit
import epsilon_measure_witness
import gravity_curvature
import gravity_gate_audit
import prediction_registry
import scoreboard


ARTIFACTS = [
    ("look_elsewhere",
     "Hardness-to-vary: is each constant the simplest number that fits?",
     look_elsewhere.main),
    ("scale_look_elsewhere",
     "Log-axis look-elsewhere: the power-of-three scale relations (M_W, M_R, Lambda) are cheap hits (~93% coverage).",
     scale_look_elsewhere.main),
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
    ("rg_matching_audit",
     "Phase 4 gate: continuum/RG matching scales, thresholds, and inverse matches made explicit.",
     rg_matching_audit.main),
    ("mass_ratio_rg_audit",
     "Per-relation scale audit: 5/6 mass relations are 1-loop RG-invariant; m_b/m_tau=7/3 is scale-dependent (holds at mu~m_b).",
     mass_ratio_rg_audit.main),
    ("first_generation_audit",
     "First-gen outlier: intrinsic factor error vs propagated error.",
     first_generation_audit.main),
    ("predict_neutrino_sum",
     "Frozen, falsifiable forward prediction: Sigma m_nu.",
     predict_neutrino_sum.main),
    ("forward_predictions",
        "Frozen future targets: m_betabeta prediction plus m_nu3/kappa bridge sensitivities.",
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
    ("weak_isospin_hypercharge",
     "Lever D: weak SU(2) from H + Gell-Mann-Nishijima Y=2(Q-T3) gives one generation's hypercharges.",
     weak_isospin_hypercharge.main),
    ("chiral_projector",
     "Lever B<->D seam: one KO-6 idempotent G_a=T_a(x)P_L gives doublet(L)+singlet(R), [Q,gamma_Q]=0.",
     chiral_projector.main),
    ("physics_map_audit",
     "Phase 1 repair: one-generation quantum-number map and anomaly cancellation.",
     physics_map_audit.main),
    ("bayesian_evidence",
     "Model-comparison Bayes factor: CHO vs an O(1)-numerology null.",
     bayesian_evidence.main),
    ("spectral_action",
     "Inverse-spectral: one algebra-internal Dirac operator, knobs vs forced ratios.",
     spectral_action.main),
    ("spectral_action_432",
     "Inverse-spectral II: cross-generation L_X on J3(O) forces the averaging law (3 relations) but one eps0 ladder misses the lepton hierarchy by ~1.4 decades.",
     spectral_action_432.main),
    ("epsilon_generation_ladder",
     "Generation masses as exponents in the FORCED base eps0=sqrt(pi/432): scheme-clean leptons prefer triangular (0,1,3) (0.33 dec, 1/28 look-elsewhere) but no law is universal across quark sectors.",
     epsilon_generation_ladder.main),
    ("spurion_perturbation",
     "Two theorems from the J3(O) tensor: a rank-one spurion lifts exactly one level per order (tiers are cumulative), and the canonical quadratic U_X gives multiplicative mixing {ab,bc,ca} -- the structure a power-law ladder needs.",
     spurion_perturbation.main),
    ("generation_cascade",
     "Generations as roots of the J3(O) cubic: the light-pair product is EXACTLY the Freudenthal cubic norm over the heaviest mass (a seesaw), collapsing the open seed to two invariant-suppression orders (q,Q); leptons read (1,4)=triangular, but (q,Q) is not universal across quark sectors.",
     generation_cascade.main),
    ("cross_generation_count",
     "Inverse-spectral: inter-generation Yukawa knob count under NNI + triality.",
     cross_generation_count.main),
    ("yukawa_operator_full",
     "Phase 3 gate: one composite Yukawa/seesaw operator with CKM/PMNS closure tests and explicit demotions.",
     yukawa_operator_full.main),
    ("three_generations_frame",
     "N_gen=3 crack: generations = 3 OP^2 idempotents permuted by the INNER frame S3 (count + chirality obstruction-free).",
     three_generations_frame.main),
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
    ("epsilon_mixing_coefficients",
     "M11: mixing multiplicities (7,3,4,4/7) as Fano-line counts; lepton 1/(4pi) as the sphere measure.",
     epsilon_mixing_coefficients.main),
    ("epsilon_vcb_halfangle",
     "C2: the |V_cb| coefficient 1/2 is the SU(2) spinor half-angle (sin(eps/2)); tan(pi/8)=sqrt(2)-1.",
     epsilon_vcb_halfangle.main),
    ("epsilon_a4_two_level",
     "R2 origin: the two-level symmetry is the SU(2) closure of A4 (Q8=lift of V4<A4; A4/V4=Z3).",
     epsilon_a4_two_level.main),
    ("epsilon_measure_audit",
     "Phase 2 gate: pi/432 as a conditional normalized transition trace; nearby alternatives excluded by named criteria.",
     epsilon_measure_audit.main),
    ("epsilon_measure_witness",
     "F0 witness: isolates H4, the invariant normalized-measure theorem seam.",
     epsilon_measure_witness.main),
    ("gravity_curvature",
     "M-GRAV: a symmetric, G2-covariant rank-2 metric (tr g = 16|a^b|^2) emerges from the octonionic associator; transverse rank-4 graviton mode, flat dirs = associative subalgebra.",
     gravity_curvature.main),
    ("gravity_gate_audit",
     "Phase 5 gate: tests for canonical 4D Lorentzian reduction and dynamics; keeps gravity out of scope if absent.",
     gravity_gate_audit.main),
    ("prediction_registry",
        "Phase 6 locked registry: prediction hashes, bridge sensitivities, and update protocol.",
     prediction_registry.main),
    ("scoreboard",
     "Bottom line: does the eps0 derivation work move ln B? before/now/target in one number.",
     scoreboard.main),
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
    print("#  Bottom line: the dimensionless coefficients are hard to vary (12/12")
    print("#  simplest fitters), BUT the power-of-three SCALE relations (M_W, M_R,")
    print("#  Lambda) are NOT: a simple prefactor x integer-exponent covers ~93% of")
    print("#  the log axis, so those hits are cheap (see scale_look_elsewhere; the")
    print("#  CC row is weakest). 5/6 mass relations are 1-loop RG-invariant, but")
    print("#  m_b/m_tau=7/3 is scale-dependent (mass_ratio_rg_audit). It is a")
    print("#  ~17-parameter framework with marginal compression today.")
    print("#  The m_e -3.75 sigma outlier is mostly error propagation through squared")
    print("#  first-gen ratios; the genuine 1/(4pi) proof obligation is a ~2% effect.")
    print("#  Derivation frontier (Levers A-C): 'three' is also the rank of J3(O)")
    print("#  (spectral, obstruction-free); the internal space sits at KO-dimension 6")
    print("#  (chirality without doubling); and the C x O number operator yields the")
    print("#  SM charges {0,1/3,2/3,1}. The model-comparison Bayes factor has moved")
    print("#  from ln B = -21 (only 8/3 closed) to -3 (today's closed theorems) to")
    print("#  +6 once the geometric pi/432 is credited (see the scoreboard artifact,")
    print("#  run: python3 compute/audit.py scoreboard): the verdict now HINGES on")
    print("#  whether pi/432 is geometrically forced, a single named seam rather than")
    print("#  a free knob, per DERIVATION_LEDGER.")
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
