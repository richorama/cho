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
  *  rg_scale_derivation   — Item 3: the EW matching scale is over-determined, not one derived number
  5. predict_neutrino_sum  — "What can future data falsify?" (frozen prediction)
  *  neutrino_floor_resolution — Item 4: the 4.6sigma floor deficit is 1.2sigma once tree-level theory error is folded
  *  theta23_octant_prediction — Item 7: the single sharpest falsifiable claim — sin^2(theta23)=4/7 (upper octant), the only eps0-independent exact mixing prediction; DUNE/Hyper-K resolve it

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
 21b.lepton_yukawa_action        — Item 2: ONE action -> ONE charged-lepton Yukawa, end-to-end
 21c.sector_sphere_dichotomy     — Item 2 seam: pi<=>continuous (lepton) vs rational<=>discrete (quark) shapes
 22. epsilon_vcb_halfangle        — C2: |V_cb| coefficient 1/2 = SU(2) spinor half-angle
 23. epsilon_a4_two_level         — R2 origin: two-level symmetry = SU(2) closure of A4
 24. epsilon_measure_audit        — Phase 2 gate: pi/432 as one conditional transition measure
    *  epsilon_measure_witness      — F0 H4 witness: normalized-measure seam isolated
    *  epsilon_measure_schur        — F0 Schur: 1/16 (Spin9) and 1/27 (E6) forced by irreducibility
    *  epsilon_orbit_selection      — F0 orbit-selection: which two orbits — the MINIMAL ones, forced by Spin(9)-transitivity (16) + action rank-one (27)
    *  epsilon_action_selection     — F0 action-selection: rank-one ray = global MINIMISER of the E6-invariant cubic N3 (X#=grad N3), an OUTPUT not an input
    *  f0_vacuum_majorization      — F0 robustness: rank-one ray is the majorization-MAXIMAL J3(O) state, so it extremises EVERY Schur-concave/convex action (cubic N3, entropies, AND the Connes spectral-action purity term) — vacuum not tied to one functional
    *  f0_spectral_triple_gate     — F0 Phase-1.1 gate: assembles (A,H,D;J,gamma) on the 432-space and reports the Connes-axiom ledger HONESTLY — KO-dim-6 spin brick + self-adjoint chirality-odd D pass, but order-zero = the octonion associator FAILS (A must be the associative/Jordan envelope) and the Jordan Yukawa needs doubling (KO-dim 4 not 6); triple does NOT yet exist, no Bayes credit
    *  f0_real_structure_gate      — F0 Phase-1.2 prerequisite: sharpens the Phase-1.1 order-zero FAIL into a real-structure DICHOTOMY — J=conj gives KO-dim 6 but makes the opposite algebra equal A so order-zero forces A abelian (no SU(2)/SU(3)); J=octonion-conj implements right-mult so order-zero is noncommutative but the grading is no longer J-compatible (KO-dim undefined). No single J on one brick gives both. RESOLUTION (computed): a nonabelian A on A(x)A^o satisfies order-zero by left-right commutation — octonions must GRADE the module, not be the order-zero algebra; rebuild A=C(+)H(+)M_3(C). No Bayes credit
    *  f0_associative_triple_gate  — F0 Phase-1.2 (proper): carries out the rebuild the prerequisite named — A=C(+)H(+)M_3(C) on A(x)A^o for the one-generation lepton sector. Order-zero holds exactly (~9e-16) for the NONCOMMUTATIVE algebra, KO-dim 6 is RESTORED (J^2=+I, JgammaJ^-1=-gamma; chirality without doubling), and an explicit Yukawa+Majorana (seesaw) Dirac is Hermitian, gamma-odd, J-real and satisfies order-one (~9e-16). The associative SKELETON EXISTS for ONE J — Phase-1.1's 'triple does not exist' is repaired at the skeleton level. HONEST: recovers the known Connes-Chamseddine-Marcolli skeleton (complement to the no-go, not new physics); octonionic Jordan L_X + full 432 (step C) and pi/432=a4/a2 (Phase 1.3) stay open. No Bayes credit
    *  f0_octonionic_yukawa_gate   — F0 Phase-1.2 step C: puts the SPECIFIC octonionic Jordan mass operator L_X (spectrum = averaging law {a,b,c}u{(a+b)/2,...}) into the step-B KO-6 triple as the flavour multiplier in the gamma1-odd Yukawa block K_Yuk(x)L_X on C^8(x)C^27. TWO-SIDED honest result: (POSITIVE) L_X needs NO doubling once chirality sits in the charge factor — D is self-adjoint/gamma-odd/J-real, KO-dim stays 6, order-zero/one ~1e-15 — so the Phase-1.1 'L_X chirality-even -> doubling -> KO-4' obstruction is DISSOLVED; (SOBERING) order-one factors through the charge sector (K_Yuk(x)random_flavour ~1e-14, K_Maj(x)random=0), so the gauge algebra sees flavour as pure multiplicity and ANY self-adjoint flavour op passes — the octonionic texture is ADMISSIBLE but NOT FORCED by the triple axioms. The CHO mass texture must come from the spectral ACTION (Phase 1.3), which epsilon_heat_kernel suggests won't yield bare pi. No Bayes credit
    *  f0_spectral_action_heatkernel — F0 Phase-1.3 DECISIVE TEST: is eps0^2=pi/432 the spectral-action heat-kernel ratio a4/a2 of the genuine 216-dim octonionic D? Computes the finite Seeley-DeWitt moments a0=M0=Tr(1)=216, a2=M2=Tr(D^2)=92.96, a4=M4=Tr(D^4)=50.3712 and the dimensionless shape M4/M2^2=0.005829 vs pi/432=0.007272 — a clean 20% MISS. STRUCTURAL KILL: the moments are EXACT rationals (M2=2324/25, M4=31482/625) so a4/a2=15741/2700488 is rational and can NEVER equal the transcendental pi/432 (seed-independent); the ONLY pi in a spectral action is the continuum (4pi)^(-d/2) — a denominator pi ((4pi)^-2=0.00633 != pi/432) — confirming epsilon_heat_kernel; the bare pi is the Berry half-solid-angle (1/2)(2pi)=pi (holonomy, not a4). VERDICT (roadmap KILL branch): REFUTES eps0^2=pi/432 as a4/a2 — the dynamical earn-path for the +5.6 via the spectral action is CLOSED, but the Berry/Schur GEOMETRIC reading is UNTOUCHED, so F0 stays GEOMETRIC/open (not demoted, not promoted); scoreboard ladder unchanged, no Bayes credit
  *  gravity_curvature            — M-GRAV: emergent rank-2 metric from non-associativity
  *  gravity_gate_audit           — Phase 5 gate: gravity remains exploratory unless Lorentzian dynamics close
  *  jordan_standalone_theorems   — Item 5: three J3(O) theorems published as standalone math, decoupled from physics
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
import per_row_theory_error
import rg_matching_audit
import rg_scale_derivation
import mass_ratio_rg_audit
import predict_neutrino_sum
import neutrino_floor_resolution
import forward_predictions
import theta23_octant_prediction
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
import cascade_universality
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
import lepton_yukawa_action
import sector_sphere_dichotomy
import epsilon_vcb_halfangle
import epsilon_a4_two_level
import epsilon_measure_audit
import epsilon_measure_witness
import epsilon_measure_schur
import epsilon_phase_space_product
import epsilon_product_irreducible
import epsilon_symplectic_volume
import epsilon_orbit_selection
import epsilon_factor_forcedness
import epsilon_assumption_p_gate
import epsilon_action_stationary
import epsilon_action_selection
import f0_vacuum_majorization
import f0_spectral_triple_gate
import f0_real_structure_gate
import f0_associative_triple_gate
import f0_octonionic_yukawa_gate
import f0_spectral_action_heatkernel
import f0_action_ray_gate
import f0_action_kernel_dynamics_gate
import f0_kernel_class_gate
import f0_vacuum_orbit_gate
import f0_transition_ray_gate
import f0_direction_gate
import gravity_curvature
import gravity_gate_audit
import jordan_standalone_theorems
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
    ("per_row_theory_error",
     "Item 6: theory error keyed to each row's derivation status (tighten per row, never one global floor); the exact 4/7 theorem earns a precision test, the eps0-ladder rows honestly stay ~1.5%.",
     per_row_theory_error.main),
    ("rg_matching_audit",
     "Phase 4 gate: continuum/RG matching scales, thresholds, and inverse matches made explicit.",
     rg_matching_audit.main),
    ("rg_scale_derivation",
     "Item 3: tests whether the EW matching scale is DERIVED. CHO's two boundaries (alpha_em^-1=128pi/3, sin^2=1/4) cannot both hold at one scale -- one-loop running needs scales ~1.8e4 apart; the lone sin^2=1/4 match sits at M_P/3^32.5 (non-integer) and no derived CHO scale lands at 1/4. KILL branch: scale not derived, S4/S5 stay open.",
     rg_scale_derivation.main),
    ("mass_ratio_rg_audit",
     "Per-relation scale audit: 5/6 mass relations are 1-loop RG-invariant; m_b/m_tau=7/3 is scale-dependent (holds at mu~m_b).",
     mass_ratio_rg_audit.main),
    ("first_generation_audit",
     "First-gen outlier: intrinsic factor error vs propagated error.",
     first_generation_audit.main),
    ("predict_neutrino_sum",
     "Frozen, falsifiable forward prediction: Sigma m_nu.",
     predict_neutrino_sum.main),
    ("neutrino_floor_resolution",
     "Item 4: the 4.6-sigma m_nu3 floor deficit is a 1.2-sigma undershoot once the tree-level seesaw theory error (M_W, m_t sisters) is folded in; N1 demoted, not falsified.",
     neutrino_floor_resolution.main),
    ("forward_predictions",
        "Frozen future targets: m_betabeta prediction plus m_nu3/kappa bridge sensitivities.",
     forward_predictions.main),
    ("theta23_octant_prediction",
     "Item 7: the single sharpest falsifiable claim -- sin^2(theta23)=4/7 (upper octant), the only eps0-independent exact mixing prediction; the Fano partition (4 avoiding > 3 through-vacuum) fixes the octant; DUNE/Hyper-K resolve it. Forward test, no row promoted.",
     theta23_octant_prediction.main),
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
    ("cascade_universality",
     "The cascade (q,Q) sector-dependence is derived flavour data, not new freedom: the universal seesaw skeleton is (0,2,4) and dividing the middle exponent by the independently-derived Georgi-Jarlskog factors {1,3,8} gives a universal 2.00; the residual non-universality is the already-open first-generation prefactors (lepton 1/(4pi)).",
     cascade_universality.main),
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
    ("lepton_yukawa_action",
     "Item 2: assembles the SINGLE charged-lepton Yukawa from ONE action's Bloch sphere -- the same S^2 whose hemisphere solid angle gives the Berry pi supplies the 1/(4pi) first-generation shape factor as its total-solid-angle (Schur invariant-average) normalization; the 8 is the derived Fock trace and the cascade square is the rank-one bottleneck. Upgrades 1/(4pi) from identified to forced; tau:mu:e at mu -2.2%, e -6.3% (known M11 outlier). OPEN: sphere-vs-discrete sector resolution, the trilinear from CHO EoM.",
     lepton_yukawa_action.main),
    ("sector_sphere_dichotomy",
     "Item 2 seam: isolates the discriminant behind the first-generation shapes (M9/M10/M11) -- pi appears IFF the transition averages over a CONTINUOUS manifold (the colourless lepton Bloch sphere S^2, 1/(4pi)) and is ABSENT (rational) IFF over a DISCRETE Fock grade (the coloured quarks). Verifies a finite group (Q8) averages to EXACTLY I/2 (rational) while the sphere gives 1/(4pi), and ties k_u=1/4=(Tr P_0/2)^2, k_d=9/4=(Tr P_1/2)^2=(1/4)N_c^2 to the derived Fock ranks. OPEN: deriving the colour-singlet->continuous selection; F0 not promoted.",
     sector_sphere_dichotomy.main),
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
    ("epsilon_measure_schur",
     "F0 Schur: the 1/16 (Spin(9) on Delta_9) and 1/27 (E6 on J3(O)) measure weights are forced by irreducibility; F4 alone is insufficient (27 = 1+26).",
     epsilon_measure_schur.main),
    ("epsilon_phase_space_product",
     "F0 product witness: under independent commuting Spin(9)/E6 sectors, the transition carrier is Delta_9 x J3(O), and the factorized invariant average gives exactly 1/432; live seam is deriving this sector-independence from the action.",
     epsilon_phase_space_product.main),
    ("epsilon_product_irreducible",
     "F0 product-irreducibility witness: Delta_9 x J3(O) is irreducible under factor-wise Spin(9) x E6, so by Schur ANY spurion (separable OR entangled) averages to I/432; removes the separable-projector and minimal-multiplicity clauses of Assumption P (breaking the assumption-gate circularity) and a F4 control shows factor-wise E6 is necessary.",
     epsilon_product_irreducible.main),
    ("epsilon_symplectic_volume",
     "F0 symplectic-volume route: 16 and 27 are Bohr-Sommerfeld counts of single Spin(9)-spinor and E6-minimal coadjoint orbits, so 432 is the Liouville volume of one PRODUCT orbit (factorization becomes a theorem of the orbit method, not an assumption); pi is the half-flux of the minimal transition orbit CP^1, giving pi/432; live seam is which two orbits the CHO action quantizes.",
     epsilon_symplectic_volume.main),
    ("epsilon_orbit_selection",
     "F0 orbit-selection route (answers symplectic_volume's 'which two orbits'): the two MINIMAL (coherent-state) coadjoint orbits, FORCED -- (16) Spin(9) acts TRANSITIVELY on the spinor sphere S^15 (orbit-tangent dim 15 everywhere, stabiliser 21=dim Spin(7)) so the spinor orbit is unique; (27) the E6 minimal orbit = the rank-one variety (Freudenthal X#=0), which is EXACTLY the action's own rank-one selection (epsilon_rank_one_kernel/action_stationary). Interlock: the f4-orbit OP^2 of a rank-one idempotent has tangent dim 16=Delta_9. Reduces 'which orbits (assumed)' to 'the minimal ones (forced)'; F0 not promoted.",
     epsilon_orbit_selection.main),
    ("epsilon_factor_forcedness",
     "F0 factorization-forcedness audit: among all ten factorizations of 432, 16x27 is the UNIQUE split whose both factors are independently-derived carriers (16=Delta_9=dim OP^2, 27=dim J3(O)), and 432 is a fundamental rep of no single simple group (G2..E8 scan) while being the Spin(9)xE6 bifundamental, so a product is forced; removes factorization freedom.",
     epsilon_factor_forcedness.main),
    ("epsilon_assumption_p_gate",
     "F0 Assumption-P gate: the current epsilon bridge operator has exact 16x27 product-separable (operator-Schmidt rank-1) primitive factors and pi/432 normalized trace; live seam is deriving this separable structure from CHO action dynamics.",
     epsilon_assumption_p_gate.main),
    ("epsilon_action_stationary",
     "F0 action stationarity: in the normalized link-action class (O>=0, Tr O=pi), the primitive kernel O=pi|tau><tau| is the unique global maximizer; current scaffold saturates this bound exactly.",
     epsilon_action_stationary.main),
    ("epsilon_action_selection",
     "F0 action-selection (removes action_stationary's rank-one INPUT on the config-space side): the Freudenthal sharp IS the gradient of the E6-invariant cubic norm, X#=grad N3 (finite-diff match ~1e-8), so the rank-one variety is the critical locus of N3; on the physical slice {X>=0,Tr X=1} N3 in [0,1/27] by AM-GM with rank-one idempotents the GLOBAL MINIMISERS (N3=0) and I/3 the unique maximiser (1/27), the minimum flat exactly along the f4-orbit OP^2 (dim 16). Same N3 has symmetry E6, whose irreducibility forces the flat 1/27 measure (epsilon_measure_schur). Reduces 'rank-one assumed' to 'rank-one = minimiser of the cubic potential'; potential-origin + kinetic coeff + EoM open; F0 not promoted.",
     epsilon_action_selection.main),
    ("f0_vacuum_majorization",
     "F0 vacuum robustness (strengthens epsilon_action_selection from one functional to a universality class): on the J3(O) state slice {O>=0, Tr O=1} the rank-one transition ray is the MAJORIZATION-MAXIMAL element — its spectrum (1,0,0) majorises every state and I/3 is majorised by every state. By Hardy-Littlewood-Polya this single order fixes the extremiser of the WHOLE Schur class: every Schur-concave action (cubic N3=det, von Neumann/Renyi entropy) is minimised at rank-one and every Schur-convex action (purity Tr O^2, AND the Connes finite-spectral-action term -a Tr Phi^2 + b Tr Phi^4) is extremised there, so a spectral action lands on the SAME rank-one vacuum (the same KO-dim-6 triple as ko_dimension_chirality/spectral_action). Honest corrective: the spectral potential is EVEN (deg 2/4) while N3 is deg 3 — different functionals, one vacuum. F0 not promoted; which action CHO realises, the kinetic coeff, and pi/432 stay open.",
     f0_vacuum_majorization.main),
    ("f0_spectral_triple_gate",
     "F0 Phase-1.1 spectral-triple gate (the make-or-break roadmap build): assembles the finite real triple (A,H,D;J,gamma) on the CHO 432-space — octonion Clifford spin brick C^8 with gamma8=i L_1..L_6 and J8=complex conjugation (KO-dim 6, eps=+1/eps''=-1), the chirality-even Jordan Yukawa L_X on J3(O) doubled to a chirality-odd Dirac D_F on C^54, product D=gamma8(x)D_F on H=C^8(x)C^54 (dim_R 864 = 2x432). Verifies the metric/real-structure HALF (D self-adjoint, gamma^2=I, gamma D=-D gamma, J^2=+I) but reports two HONEST obstructions: order-zero [a,b^o] equals the octonion associator and FAILS for A=C(x)H(x)O (~16; recovered only on a true associative bimodule ~1e-15 or the C-line), and the Yukawa doubling pushes the finite KO-dim to 6+6=4(mod8) not 6. The naive triple does NOT yet exist; both repairs (associative/Jordan envelope; Yukawa in the real structure) are known, so this is not the KILL but localises the Phase-1.2 prerequisite. F0 stays open; no Bayes credit.",
     f0_spectral_triple_gate.main),
    ("f0_real_structure_gate",
     "F0 Phase-1.2 prerequisite (sharpens the Phase-1.1 order-zero FAIL): a spectral triple has ONE real structure J, and every axiom must hold for that SAME J. Tests both KO signs and order-zero against each candidate J on the octonion brick C^8 and finds a DICHOTOMY: with J=complex conjugation (the KO-dim-6 choice, B=I) the opposite algebra J L_a J^-1 = L_a coincides with A, so order-zero [a,b^o]=[A,A]=0 forces A COMMUTATIVE (L(H) fails ~14, only the abelian L(C) holds ~1e-16) — no SU(2)/SU(3); with J=octonion conjugation (kappa.conj) one gets J L_a J^-1 = -R_a (genuine right mult) so order-zero is the associator (holds on the quaternion bimodule ~1e-15, allows a noncommutative A) BUT J gamma J^-1 = -0.5 gamma is not +-gamma, so the grading is not J-compatible and the KO-dimension is undefined. Hence NO single J on one irreducible brick gives BOTH KO-6 AND a noncommutative order-zero algebra. RESOLUTION (computed, standard Connes route): a nonabelian A=H acting on A(x)A^o satisfies order-zero EXACTLY (0) by left-right commutation while staying nonabelian (||[i,j]||=2) — the octonions must GRADE the module (gamma8, charges), not be the order-zero *-algebra; rebuild A=C(+)H(+)M_3(C). Converts the order-zero fail into a precise statement + named fix; F0 stays open, no Bayes credit.",
     f0_real_structure_gate.main),
    ("f0_associative_triple_gate",
     "F0 Phase-1.2 (proper) — carries out the associative rebuild that f0_real_structure_gate named. Builds the one-generation lepton finite geometry: H=C^8 [nuR,eR,nuL,eL | antiparticles], A=C(+)H acting on the left, J=(particle<->antiparticle swap).conj, gamma=chirality flipped on antiparticles. From explicit matrices: [A] order-zero [a_L,b_R]=0 on A(x)A^o for the NONCOMMUTATIVE summands H (~9e-16, ||[x,y]||=14.7) and M_3(C) (~2e-15, ||[x,y]||=15.3) and for the actual SM lepton rep (~9e-16) — the colour M_3(C) factor commutes by construction; [B] KO-dim 6 RESTORED — J^2=+I (eps=+1) and J gamma J^-1=-gamma (eps''=-1), chirality WITHOUT doubling, the grading the prerequisite's kappa.conj had destroyed; [C] an explicit physical Dirac with Dirac Yukawas (nuR<->nuL, eR<->eL) AND a Majorana mass (nuR<->nuRbar) is Hermitian, gamma-ODD, J-REAL (J D J^-1=D) and satisfies order-one [[D,a],b^o]=0 (~9e-16), so the seesaw lives in the real-structure sector and the finite KO-dim stays 6 (not 4). The associative SKELETON EXISTS for a SINGLE J: Phase-1.1's 'triple does not exist' is repaired at the skeleton level. HONEST CAVEAT: this is the known Connes-Chamseddine-Marcolli skeleton recovered constructively — the complement to the no-go, NOT new physics — and moves NO Bayes credit. Open CHO-specific bridges: step C (replace the generic Yukawa by the octonionic Jordan mass L_X and realise the full 432=16x27 module; only the 8-dim colour-singlet slice is built here) and Phase 1.3 (eps0^2=pi/432 as the spectral-action ratio a4/a2; epsilon_heat_kernel warns the spectral pi enters only via (4pi)^(-d/2), so a bare pi numerator is unlikely). F0 stays GEOMETRIC/open; no Bayes credit.",
     f0_associative_triple_gate.main),
    ("f0_octonionic_yukawa_gate",
     "F0 Phase-1.2 step C — puts the SPECIFIC octonionic Jordan mass operator L_X into the step-B KO-6 triple and asks whether the axioms FORCE its texture. Faithful SM finite geometry H=C^8(x)C^27 (step-B lepton charge factor (x) J3(O) flavour): the Yukawa is K_Yuk(x)L_X with the charge L<->R coupling K_Yuk gamma1-ODD and L_X the UNGRADED octonionic generation matrix (gamma=gamma1(x)I27, J=J1(x)conj). From explicit matrices: [A] L_X is the genuine averaging-law operator — spectrum = three singlets {1,0.6,0.3} (mult 1) and three octets {0.8,0.65,0.45} (mult 8), 27 total, self-adjoint to 0; [B] DOUBLING OBSTRUCTION DISSOLVED — because chirality sits in the charge factor, L_X needs no particle/antiparticle doubling: the product Dirac D=K_Yuk(x)L_X+K_Maj(x)M_maj is self-adjoint, gamma^2=I, gamma-ODD, J-REAL, KO signs eps=+1/eps''=-1 -> KO-dim 6 (the Phase-1.1 6(x)6->4 doubling that broke KO-6 is gone), with order-zero (~9e-16) and order-one (~9e-16) BOTH holding for the genuine octonionic D; [C] DECISIVE — order-one factors through the charge sector: each charge coupling tensored with a RANDOM Hermitian flavour operator still satisfies order-one (K_Yuk(x)random ~7e-15, K_Maj(x)random=0), so the gauge algebra sees flavour as pure multiplicity and ANY self-adjoint flavour op passes. TWO-SIDED VERDICT: POSITIVE — the octonionic L_X lives in a consistent KO-6 triple ungraded, carrying its averaging-law masses into D's spectrum (closes the second Phase-1.1 obstruction); SOBERING — the triple axioms (order-zero/one, KO-6) are NECESSARY but do NOT pin the Yukawa, so the CHO mass texture is NOT secured by the triple's existence — it must come from the spectral ACTION Tr f(D/Lambda) (Phase 1.3). epsilon_heat_kernel already warns the spectral pi enters only via the Gaussian (4pi)^(-d/2), so Phase 1.3 is more likely to REFUTE than confirm eps0^2=pi/432 as a4/a2. Moves NO Bayes credit: F0 stays GEOMETRIC/open.",
     f0_octonionic_yukawa_gate.main),
    ("f0_spectral_action_heatkernel",
     "F0 Phase-1.3 DECISIVE EXPERIMENT — runs the gold-standard make-or-break test on the genuine 216-dim octonionic step-C Dirac: does eps0^2=pi/432 equal the spectral-action heat-kernel ratio a4/a2? For the finite triple the Seeley-DeWitt coefficients ARE the spectral moments a0=M0=Tr(1)=216, a2=M2=Tr(D^2)=92.96, a4=M4=Tr(D^4)=50.3712. [A] the moments are computed from the explicit Dirac spectrum; [B] every dimensionless a4/a2 normalisation MISSES pi/432=0.00727221 — the closest natural shape M4/M2^2=0.00582895 is 0.80x target, a clean 20% miss; [C] the STRUCTURAL KILL: the moments are EXACT rationals (M2=2324/25, M4=31482/625, residual ~1e-14) because Tr(D^2k) is a rational power sum of the algebraic Dirac spectrum, so a4/a2=M4/M2^2=15741/2700488 is an EXACT rational and can NEVER equal the transcendental pi/432 (pi/432 has no small-denominator fit, residual 5e-7); seed-independent — seed (.8,.6,.4) gives M2=2002/25, M4=20584/625, another pi-free rational; [D] the ONLY pi a Connes-Chamseddine spectral action emits is the continuum (4pi)^(-d/2) (a DENOMINATOR pi with half-integer power; (4pi)^-2=0.00633257 != pi/432), confirming epsilon_heat_kernel; [E] the bare pi numerator is reproduced by the Berry half-solid-angle (1/2)(2pi)=pi — a holonomy flux, so pi/432=(Berry pi)x(Schur 1/432) is a flux-per-state count, a GEOMETRIC quantity not a spectral-action output. VERDICT (the roadmap KILL branch): Phase 1.3 REFUTES eps0^2=pi/432 as the heat-kernel a4/a2 — the DYNAMICAL earn-path for the +5.6 via the spectral action is CLOSED (any DERIVED promotion now needs a different mechanism), but the Berry/Schur GEOMETRIC reading is UNTOUCHED and remains the ceiling for pi/432, so F0 stays GEOMETRIC/open (NOT demoted below geometric, NOT promotable via this route). Moves NO Bayes credit; the scoreboard ladder (-21.3 historical / -3.2 EARNED floor / +5.6 if-granted / +36.2 target) is UNCHANGED and no frozen artifact is touched.",
     f0_spectral_action_heatkernel.main),
    ("f0_action_ray_gate",
     "F0 action-ray derivation gate: derives the transition ray as the unique stationary maximizer of the effective action generator, with dynamic flow convergence checks.",
     f0_action_ray_gate.main),
    ("f0_action_kernel_dynamics_gate",
     "F0 action-kernel dynamics gate: derives admissible kernels from action evolution closure (unitary flow + coarse-graining + theta normalization), yielding O>=0 and Tr(O)=pi.",
     f0_action_kernel_dynamics_gate.main),
    ("f0_kernel_class_gate",
     "F0 admissible-kernel class gate: checks that symmetry + convex closure + normalization consistently force O>=0, Tr(O)=pi on the 16x27 bridge space.",
     f0_kernel_class_gate.main),
    ("f0_vacuum_orbit_gate",
     "F0 vacuum-orbit gate: checks whether fixing the vacuum collapses the transition-ray degeneracy to one stabilizer orbit.",
     f0_vacuum_orbit_gate.main),
    ("f0_transition_ray_gate",
     "F0 transition-ray consistency gate: checks that vacuum orbit, action-selected holonomy, and trace space all point to the same ray representative.",
     f0_transition_ray_gate.main),
    ("f0_direction_gate",
     "F0 governance gate: reports whether the next step is closure-critical or should pivot away from theory-for-theory based on live F0 contracts and scoreboard state.",
     f0_direction_gate.main),
    ("gravity_curvature",
     "M-GRAV: a symmetric, G2-covariant rank-2 metric (tr g = 16|a^b|^2) emerges from the octonionic associator; transverse rank-4 graviton mode, flat dirs = associative subalgebra.",
     gravity_curvature.main),
    ("gravity_gate_audit",
     "Phase 5 gate: tests for canonical 4D Lorentzian reduction and dynamics; keeps gravity out of scope if absent.",
     gravity_gate_audit.main),
    ("jordan_standalone_theorems",
     "Item 5: three decoupled J3(O) theorems (inner frame S3, Schur-forced 1/16 & 1/27, Freudenthal seesaw) stated as standalone mathematics, no physics used.",
     jordan_standalone_theorems.main),
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
