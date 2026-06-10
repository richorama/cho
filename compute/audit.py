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
    *  f0_phase1_closeout          — F0 PHASE 1 CLOSEOUT: the make-or-break gate is fully executed (1.1 obstructions -> 1.2 associative rebuild + octonionic L_X -> 1.3 heat-kernel refutation -> 1.4 spectrum localisation); this gate consolidates the TWO independent decisive results and records their convergence. [A] PREFACTOR route (Phase 1.3, re-derived from the genuine D): a4/a2=M4/M2^2=0.00582895 is a pi-free rational != pi/432=0.00727221, so pi/432 is NOT a spectral-action output; [B] RATIO route (Phase 1.4, imported from spectral_action_432): the L_X averaging-law spectrum's best single-knob eps0 ladder MISSES the measured lepton hierarchy by 1.40 decades, so the spectrum forces STRUCTURE not the absolute profile; [C] CONVERGENCE — prefactor (a transcendental constant) and ratios (multiplicative) are independent tests yet BOTH localise the entire remaining F0 gap to the SAME missing object: a DYNAMICAL/VARIATIONAL action that would have to produce pi/432 [refuted] AND select the three seed eigenvalues [open] — gold-standard criterion 1, ABSENT. FORK OUTCOME (bounded): F0 stays GEOMETRIC/open (Berry/Schur reading survives, mass STRUCTURE derived), neither pi/432 nor the hierarchy promotable without the action; Phase 2 GATED on it; no Bayes credit moves; scoreboard ladder + frozen registry untouched. NOT an invariance witness — it closes that phase
    *  f0_theta_reality_gate       — F0 THETA-REALITY: tests the 'mind-bending' TOPOLOGICAL route to close the gate Phase 1.3/1.4 left open — is pi/432 = theta/dim with theta = pi*nu a Z2 angle QUANTIZED by the KO-6 real structure J (and CHO in the nu=1 class)? A theta-term is NON-perturbative (never in the rational Seeley-DeWitt moments), so it is a genuinely DIFFERENT channel from 1.3's a4/a2. On the genuine 216-dim octonionic D all THREE natural sources of a theta=pi vanish, for every seed and Majorana setting: [A] spectral-asymmetry (eta) theta — gamma D=-D gamma forces a +/- symmetric spectrum (108/108, no zero modes) so eta=0 identically; [B] chiral mod-2 index — the H+->H- block is full rank (108), zero kernel, nu=0; [C] Kramers/Fu-Kane Z2 — KO-6 has J^2=+1 (real class) so the time-reversal theta=pi invariant is not even defined (needs J^2=-1). VERDICT: theta=0, so pi*nu/432=0 != pi/432 — the topological route is CLOSED, a THIRD independent converging-negative (with the 1.3 prefactor and 1.4 ratios); all three are KINEMATICS/TOPOLOGY and the gap is DYNAMICS. pi/432 stays the Berry half-solid-angle holonomy of the CONTINUOUS vacuum sphere (the missing action), not a topological invariant of D. F0 stays GEOMETRIC/open; no Bayes credit moves; scoreboard + frozen registry untouched
    *  gold_standard_closeout      — PROGRAM CLOSEOUT: the program-level analogue of f0_phase1_closeout — consolidates the WHOLE seven-point gold-standard scorecard into one executable, tamper-evident statement and asserts the honest-null standing position against its source-of-truth modules. Imports scoreboard.scoreboard() (the ln B ladder -21.3 historical -> -3.2 EARNED floor -> +5.6 if pi/432 GRANTED -> +36.2 target; the sign flips ONLY on the grant, so on earned credit the null still wins), audit_contract.CONTRACTS (rigour census: >=1 THEOREM, the headline F0/one-operator contracts still OPEN), prediction_registry (frozen digest MATCH), and re-runs f0_phase1_closeout's two routes (criterion 1 re-verified ABSENT). CONVERGENCE: criteria 1, 3 and the open half of 2 all localise to the SAME missing derived dynamical action; the external criteria (4 DUNE, 7 peer review) and the falsified single scale (6) are not closable by internal work. Standing position: the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null. Moves NO Bayes credit; asserts the scoreboard floor + frozen registry so the position is drift-proof; touches no frozen artifact
  *  gravity_curvature            — M-GRAV: emergent rank-2 metric from non-associativity
  *  gravity_gate_audit           — Phase 5 gate: gravity remains exploratory unless Lorentzian dynamics close
  *  jordan_standalone_theorems   — Item 5: three J3(O) theorems published as standalone math, decoupled from physics
  *  padic_hierarchy              — BIG-BETS Bet 1 (EXPLORATORY): are the mass-hierarchy exponents {9,36,64} arithmetic (3-adic) not analytic? They are perfect squares whose increments are consecutive arena dims (+27=dim J3(O), +28=dim so(8)); 3-adically the EW hierarchy is unit-scale, so the hierarchy 'problem' is an archimedean artefact (why the real-analytic spectral action could never emit these scales). A look-elsewhere null leaves the pattern SUGGESTIVE-only (corrected p~0.018, above the promotion bar): exponents stay CHOSEN, no Bayes credit moves.
  *  causal_set_lambda           — BIG-BETS Bet 2 (EXPLORATORY): does Sorkin's causal-set law Lambda~1/sqrt(V) give the CC exponent 64 a dynamical origin? CHO's Lambda^(1/4)~M_P/3^64 is equivalent (via Lambda^(1/4)~V^(-1/8), 1/8=fourth-root x Sorkin-sqrt, NOT dim(O)) to a cosmic 4-volume V~3^512~10^244 — the observed value. So 64~(1/8)log_3(V_obs) recovers the largest CHOSEN chunk as a volume-fluctuation scale, supplying the counting-dynamics the static algebra lacked. Honest: recovered to +/-0.5 across 4-volume conventions, uses observed V as input (trades 'why 64' for 'why now'), base 3 unforced here (base 8 fits the volume better). Sharp falsifier: CHO (Lambda constant, w=-1) vs Sorkin (everpresent Lambda, w(t)!=-1), DESI/Euclid discriminate. EXPLORATORY: exponent stays CHOSEN, no Bayes credit moves.
  *  entropic_gravity_cho        — BIG-BETS Bet 2 (EXPLORATORY): the OTHER thing CHO gated out — gravity. Jacobson's dQ=TdS + Bekenstein-Hawking S=A/4 yields the Einstein equations; the 1/4 (=1/4G) is the pure number the static algebra cannot emit. Counting CHO microstates (dim d) on horizon cells gives S~A (area law, automatic) — the dynamics-from-counting prerequisite — but matching S=A/4 only RELOCATES the coefficient into a_cell=4 ln d, and the exact bit-bookkeeping identity N_cells*log2(d)=N_bits shows the CHO dimension is pure bookkeeping for it: a DECISIVE negative (counting touches the form, never the value of G). Sharp cross-module tension: the SAME Planck-density causal set that nails Lambda would overcount black-hole entropy by 4 ln d~13x (d=27=J3(O)) unless the internal state is horizon-unresolved. EXPLORATORY: no prediction promoted, no Bayes credit moves.
  *  everpresent_lambda_tracking — BIG-BETS Bet 2a deepening (EXPLORATORY): invests in causal_set_lambda's biggest debit (it trades 'why 64' for 'why now') by taking Sorkin's everpresent Lambda~1/sqrt(V(t))~H(t)^2 as DYNAMICAL dark energy. Two readings of the SAME exponent: CHO-static (Lambda fixed, w=-1, Omega_L(z)=Omega_L,0/E(z)^2 dilutes to 0 at high z) vs Sorkin-everpresent (Lambda~H^2 tracks rho_crit, Omega_L(z)~O(1) always). First dividend: tracking partly repays the why-now debit ('O(1) now' becomes 'O(1) always'). Second dividend: the constant-vs-dynamical falsifier is now COMPUTED — the readings diverge as Om_ever/Om_static=E(z)^2 (~3 at z=1, ~6e8 at recombination); DESI/Euclid measure this, and the 2024-25 evolving-DE hints point away from w=-1. Honest core: the entire time-structure is CAUSAL-SET content (the divergence SHAPE is invariant under the CHO exponent, asserted) — CHO is a SPECTATOR in the dynamics, so a confirmed evolving-DE signal supports Sorkin over CHO-static (CHO's own w=-1 is the casualty). Caveat kept: smooth Lambda~H^2 is degenerate with rescaled G, the real DE lives in sign fluctuations not simulated here. EXPLORATORY: no prediction promoted, no Bayes credit moves.
  *  causal_growth_index          — BIG-BETS Bet 2 CRUX (EXPLORATORY): the make-or-break test the Lambda/gravity probes deferred — does the causal-set GROWTH dynamics SEE an internal CHO index and thereby force the generation count N=3? Rideout-Sorkin classical sequential growth (transitive percolation, i.i.d. pre-closure pair inclusions + transitive closure, so both CSG axioms are explicit) with an index s_i in {1..N} coupling via a pairwise inclusion probability p(s_i,s_j). EXACT facts (asserted): index-blind growth is covariant on every poset — counting supplies a genuine measure on histories (gold-standard criterion A, the object the static algebra lacked); discrete general covariance is equivalent to a SYMMETRIC coupling (an asymmetric coupling splits the two birth orders of the V poset 0.042 vs 0.126, a symmetric one collapses them); covariance imposes C(N,2) symmetry equations and leaves an N(N+1)/2 family that is NEVER empty, so a covariant non-spectator coupling exists for N in {2,3,4,5,6} and N=3 is NOT singled out; the index-blind causet marginal is exactly N-independent (the SPECTATOR limit, TV=0); Bell causality is automatic (the measure factorises over pairs) — also blind to N; and even a non-trivial inheritance (child index = product of parents) is covariant for every N (Z/N), so the exceptional rank-3 Albert algebra needs the NON-ASSOCIATIVE octonionic input — a kinematic (Hurwitz/Jordan) fact, not dynamics. So counting gives the FORM (a covariant, Bell-causal measure) but never the CONTENT (N=3): the Bet-2 crux resolves NEGATIVE, the same boundary the Lambda and gravity probes drew. EXPLORATORY: N=3 stays a kinematic input (G1), no Bayes credit moves.
  *  statistical_flavour_ensemble — BIG-BETS Bet 3 (EXPLORATORY): the honest fallback for the losing one-number game — stop predicting single Yukawas, predict their DISTRIBUTION. Four 3x3 complex-Yukawa ensembles (CKM = U_u^dag U_d): A anarchy (Ginibre, symmetry-BLIND), B Froggatt-Nielsen hierarchy eps^(qi+qj) only, C NNI texture zeros (1,1),(1,3), D the triality-DERIVED (1,3) zero only. EXACT facts (asserted): (+) the REAL WIN — distributions DECISIVELY falsify symmetry-blind anarchy for quarks (anarchy median sin^2 ~ 0.3-0.5, and P(all three CKM moduli as small as observed) ~ 0) while the SAME anarchy stays viable for the anarchic lepton sector (a PMNS-sized theta13 a few % of the time) — the observed quark/lepton dichotomy falls straight out; (-) the HONEST NULL — the discriminator is the mass HIERARCHY, not the CHO texture: the famous GST correlation corr(|V_us|, sqrt(m_d/m_s)) is ~0 for anarchy but ~+0.48 for the Froggatt-Nielsen hierarchy ALONE (both scale as eps^(q1-q2)), and CHO's DERIVED triality zero lifts it only ~+0.07 more (hierarchy increment strictly exceeds texture increment, asserted). What beats symmetry-blindness is the eps-ladder (the same charged input the scoreboard already debits, F0), and NNI is emitted by every Froggatt-Nielsen model. So distributions give the FORM (a sharp many-observable falsification) but not the CONTENT (a CHO-specific texture that beats same-hierarchy symmetry-blindness). EXPLORATORY: the single-value C1..C4 bridges are untouched, no Bayes credit moves.
  *  positive_geometry_cluster   — BIG-BETS Bet 4 (EXPLORATORY): does the positive geometry FORCE the CHO arena, or merely host it? The amplitude is the canonical form of a positive geometry (dynamics from geometry, no Lagrangian); its computable skeleton is the cluster algebra (Fomin-Zelevinsky finite-type <-> Dynkin), and the exceptional types CHO privileges already surface in amplitudes (Gr(3,6)~D4 = triality = 3 generations; Gr(3,7)/Gr(4,7)~E6 = J3(O)). EXACT facts from the Dynkin degree tables (asserted): (+) HOSTING is exact — D4 (triality) has 16 cluster variables (= dim C(x)H) and dim 28 (= so(8)); E6 (J3(O)) has 36 positive roots (the repo's own M_W exponent label) and minuscule 27 (= dim J3(O) = 27 lines on a cubic surface, |W(E6)|/|W(D5)|); the hierarchy increments {27,28} = {dim J3(O), dim so(8)} = {E6 minuscule, D4 adjoint}; and E6 is the UNIQUE exceptional with a Z/3 centre, so base-3 is structurally distinguished for exactly CHO's algebra (criterion B passes cleanly). (-) but HOSTING is not FORCING — the cluster-specific invariant (the cell count = associahedron vertices) is NEVER a CHO integer and NEVER 3, so the geometry does not force the generation count; the matches are non-unique (27 is also the A6 cluster-variable count) and multi-hosted (D4, E6, F4, G2 all carry a CHO integer, so the arena is NOT selected — humility tripwire); the seductive products are near-miss traps (432=16*27 vs A6 cells 429; 64 vs E7 roots 63); the Z/3 centre lives in E6 rep theory (a CHO input), not the canonical-form dynamics, and is not the triality/generation Z/3; and the actual octonionic positive geometry is NOT constructed (non-associativity obstructs the standard totally-positive cluster coordinates — the open frontier). So counting the cells gives the FORM (a skeleton that contains CHO's integers) but never the CONTENT (a geometry that forces them): the fifth face of the same FORM-not-CONTENT boundary. EXPLORATORY: no constant promoted to derived, no Bayes credit moves.
  *  adelic_constant_relation    — BIG-BETS Bet 1 SECOND probe (EXPLORATORY): the Moonshine follow-on padic_hierarchy named — where #77 read the three hierarchy EXPONENTS additively (perfect squares, increment ladder), this reads the CONSTANTS THEMSELVES MULTIPLICATIVELY (prime factorisation) and asks whether the WHOLE predictive set is ONE arithmetic object. EXACT facts (asserted): (+) every constant that ENTERS a CHO prediction is an S-unit over the SAME three octonion primes {2,3,7} — 432 = 2^4*3^3 = 16*27 (v2=4=dim H, v3=3=generations), the only eps0-free mixing prediction sin^2(theta23)=4/7 (cos^2=3/7) is the Fano line-count split 7=4(avoid vacuum)+3(through), the power-of-three exponents 9,36,64 and arena dims 16,27,28,14 all factor on {2,3,7}, and |Aut(Fano)|=|PSL(2,7)|=168=2^3*3*7 has prime support EXACTLY {2,3,7}; the three primes are precisely the octonion-distinguished ones (2 Cayley-Dickson doubling, 3 triality/rank-3/generations, 7 Im(O)/Fano) — the adelic reading extends #77 from the exponents to the whole multiplicative set (why a real-analytic action over R cannot emit them). (-) but HOSTING is not FORCING — {2,3,7}-smoothness is GENERIC for small integers (~11-40% below a few hundred), it BREAKS inside CHO's own vocabulary (dim F4=52=2^2*13, dim E6=78=2*3*13, dim E7=133=7*19, dim E8=248=2^3*31 carry primes 13,19,31 — so the SUBSET entering predictions is {2,3,7}-smooth, not the theory), and NO single arithmetic relation generates the set (432 is not a j-function/Monster coefficient — the Moonshine 196884=196883+1 has no 432 analogue; the only S-unit equations are trivial, 7=4+3 and the additive ladder already in #77). The factorisation re-expresses the arena CHO already ingests; nothing is derived. The sixth face of the FORM-not-CONTENT boundary. EXPLORATORY: exponents/mixing stay CHOSEN, no Bayes credit moves.
  *  big_bets_closeout           — BIG-BETS CLOSEOUT (EXPLORATORY): the capstone over the whole `big-bets` branch — the analogue of gold_standard_closeout for the internal program. Consolidates the four ranked bets / eight EXPLORATORY modules (#77-#84) into the SIX FORM-not-CONTENT faces — Lambda (causal_set_lambda, everpresent_lambda_tracking), gravity/G (entropic_gravity_cho), N=3 (causal_growth_index), flavour texture (statistical_flavour_ensemble), the exceptional arena (positive_geometry_cluster), the constants (padic_hierarchy, adelic_constant_relation) — and asserts the one finding they triangulate: EVERY bet supplied the FORM the static algebra lacked (a counting measure / an automatic area law / a covariant Bell-causal growth law / a sharp distributional falsifier / an exact positive-geometry host / an adelic reframing) but NONE forced the CONTENT (the exponent 64 / the 1/4 / the 3 / a CHO texture / arena selection / the specific values). Six outside directions, one boundary — which CONFIRMS gold_standard_closeout from new directions: the lone missing object is SINGULAR (a derived dynamical action that selects the seed/value). Source-of-truth tripwires (asserted): all 8 probes still STATUS_EXPLORATORY/VERDICT_OPEN and still humble (>=1 open bridge + >=1 kill condition), the six faces partition exactly those 8 modules, and the EARNED scoreboard floor is still ln B=-3.2<0 (the whole arc moved NO credit). The one keeper is a DIAGNOSIS, not a derivation (the constants are arithmetic objects a real-analytic action over R can't emit — why Phase 1 hit its wall). A REPORTER: grants no Bayes credit, forbids only SILENT drift.
  *  berry_sigma_model_op2      — DECISIVE topological-route test for pi/432 (EXPLORATORY): the one internal experiment that could flip the scoreboard sign WITHOUT a grant. Phase 1.3 refuted the analytic route (the spectral-action ratio a4/a2=0.00582895 is a pi-FREE rational, never pi/432); this assembles the alternative the triangulation points at — a Berry/WZ sigma-model on the triality-vacuum manifold OP^2 (rank-one J3(O) idempotents, dim 16 = E6 minimal orbit) with the E6-invariant cubic norm N3 as potential, S=(Berry/WZ kinetic)-(N3 potential) — and tests BOTH halves. [FORM] PASSES: the Berry holonomy of the minimal great-circle (geodesic) loop of ACTUAL rank-one J3(O) idempotents is pi (= 1/2 * 2pi solid angle; cross-checked vs the source-of-truth great-circle phase; a non-geodesic latitude loop gives pi/2, so pi is geodesic-selected) — the topological kinetic term EMITS pi exactly where the analytic spectral action provably cannot. [CONTENT] FAILS, structurally: N3=det=0 on ALL of OP^2 and the J3(O) spectrum is identically (1,0,0), so N3 — and EVERY F4-invariant, since F4 preserves the spectrum — is CONSTANT on the vacuum manifold; the measured charged-lepton hierarchy is a non-symmetric triple that is NOT an N3 critical point (the global maximum 1/27 is the all-EQUAL anti-hierarchy), and the single-knob eps0 ladder misses by ~1.40 decades. NET: the sigma-model SEPARATES pi/432 — FORM (the pi) is reachable by the topological route (the kinetic term is settled), CONTENT (the seeds) is NOT reachable from any F4-invariant potential and REQUIRES an F4-BREAKING term (a NEW symmetry no-go). The sign does NOT flip (CONTENT failed): pi/432 is NOT promoted, no Bayes credit moves, F0 stays GEOMETRIC/open. Confirms Phase 1.4 (structure forced, seed open) from an independent dynamical direction.
  *  berry_pi_intrinsic_op2     — HARDENS the FORM (the pi) of pi/432 (EXPLORATORY): the pi that berry_sigma_model_op2 emitted was measured on ONE associative CP^1 slice; this proves it INTRINSIC to OP^2 and explains WHY it is a half-turn. [A] the transition-sphere's two antipodal POLES are ORTHOGONAL primitive idempotents E1,E2 (Tr(E1 o E2)=0 — two of the three generations), the Berry phase obeys gamma(theta)=pi(1-cos theta) EXACTLY, and the great circle (the unique closed geodesic, the locus EQUIDISTANT from the two orthogonal generations) encloses the hemisphere Omega=2pi and gives gamma=pi — a non-geodesic latitude gives <pi, so pi is the holonomy that SEPARATES two orthogonal generations, not an input. [B] pi is F4-INTRINSIC, not a slice artifact: F4=Aut(J3(O)) is an ISOMETRY of the trace metric (verified ~1e-13), so transporting the great-circle loop by a random automorphism keeps it rank-one idempotents (PoP=P, N3=0), preserves EVERY consecutive overlap Tr(P_i o P_{i+1}) (the full metric data the Berry phase=1/2*area depends on), yet moves it into GENUINELY OCTONIONIC directions (e2..e7 ~0.2, zero on the slice); OP^2=F4/Spin(9) is two-point-homogeneous, so every geodesic 2-sphere is an F4-image of the base CP^1 and the isometry-invariant phase is the SAME pi. [C] the half-turn is the SU(2) sign flip: the great-circle Bargmann product is real-NEGATIVE (e^{i pi}=-1, the vacuum ray returns to MINUS itself; cf. epsilon_vcb_halfangle tan(pi/8)). Hardens the kinetic term against the octonionic directions WITHOUT evaluating an ill-defined octonionic Bargmann product (it proves the phase-determining trace data is F4-invariant). CONTENT (the three seeds) stays open (berry_sigma_model_op2: every F4-invariant flat, needs an F4-BREAKING term); no Bayes credit moves, pi/432 NOT promoted, F0 stays GEOMETRIC/open.
  *  f4_breaking_seed_op2       — LOCALIZES the CONTENT (the three seeds) of pi/432 (EXPLORATORY): berry_sigma_model_op2 proved seed-selection needs an F4-BREAKING term (N3 and every F4-invariant flat on OP^2); this tests whether the framework's OWN canonical F4-breaking object — the rank-one triality-breaking vacuum spurion |tau><tau| (epsilon_rank_one_kernel, spurion_bridge) — supplies it, and finds a TWO-SIDED result. [POSITIVE / no-go EVADED] the linear frame-breaking height V_A(P)=Tr(P o A) has, on OP^2, critical points EXACTLY at the three primitive idempotents E1,E2,E3 of A's eigenframe (standard Morse theory of a height function on the flag manifold F4/Spin(9)): the F4-gradient g_D=Tr((D.P) o A) vanishes (~1e-16) at all three generations for frame-diagonal A, gradient ASCENT from random OP^2 points flows to the top generation (overlap 1.0000), and the control A=I (F4-invariant) is flat (V=Tr P=1, grad ~1e-15 — reproduces the no-go). So the three generations ARE the critical set of the canonical frame-breaking potential, and the DIRECTION is frame-canonical NOT circular — any distinct-spectrum A in the generation frame gives the SAME three critical points (only the values change). [HONEST OPEN] the critical VALUES are V_A(E_i)=spec(A): the seed MAGNITUDES are the spurion spectrum (the input), and the canonical vacuum spurion is RANK-ONE, lifting EXACTLY ONE level (V(E_tau)=1, the whole OP^1 orthogonal to E_tau degenerate at 0 — geometric spurion_perturbation FACT 1), so three ISOLATED tiers require CUMULATIVE orders A=E1+eps0 E2+eps0^2 E3 whose spectrum (1,eps0,eps0^2) reproduces the cascade ladder, leaving the absolute scale eps0^2=pi/432 (the measure) as the lone surviving input. NET: tightens "needs an F4-breaking term" into "the F4-breaking term IS the rank-one vacuum spurion; it makes the three generations the critical points (real, non-circular direction), rank-one-ness forces the cascade, the lone open scalar is eps0^2=pi/432". CONTENT LOCALIZED not closed; no Bayes credit moves, pi/432 NOT promoted, F0 stays GEOMETRIC/open.
  *  f0_sigma_model_closeout    — F0 SIGMA-MODEL CLOSEOUT (EXPLORATORY): a REPORTER (re-derives nothing, grants no Bayes credit) consolidating the three OP^2 Berry/WZ sigma-model modules (#86 berry_sigma_model_op2, #87 berry_pi_intrinsic_op2, #88 f4_breaking_seed_op2) and recording the route as the FOURTH independent converging-negative on the one missing dynamical action — alongside the prefactor (f0_spectral_action_heatkernel: a4/a2 a pi-FREE rational), the ratios (spectral_action_432: ~1.40-decade miss) and the topological-theta (f0_theta_reality_gate: theta=0) routes. The one genuinely-new thing it adds is what KIND of action is missing: #86's no-go (N3 and every F4-invariant flat on OP^2) forces the missing action to BREAK F4, and #88 shows the canonical F4-breaking rank-one vacuum spurion supplies the DIRECTION (the three generations = Morse critical points of V_A(P)=Tr(P o A)) but NOT the MAGNITUDE (values=spec(A); absolute scale eps0^2=pi/432, the lone surviving input) — so 'need a derived action' sharpens to 'need a derived F4-BREAKING action whose flux is pi/432 and whose spectrum is the seed': DIRECTION solved, MAGNITUDE open. Tripwires (asserted): the three sigma-model probes stay STATUS_EXPLORATORY/VERDICT_OPEN and humble (>=1 open bridge + >=1 kill condition), the four converging-negative routes are all real audited contracts, and the EARNED floor stays ln B=-3.2<0 (the whole route moved NO credit). The sign does NOT flip; pi/432 stays Berry/Schur GEOMETRIC, F0 GEOMETRIC/open. Further internal pi/432 derivations are the treadmill; the live external lever is sin^2 theta23=4/7 (DUNE/Hyper-K).
    *  theory_probation_closeout  — governance reporter: preserve the theorem-level core, archive failed routes as null records, and keep only the derived F4-breaking action route on probation
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
import f0_phase1_closeout
import f0_theta_reality_gate
import gold_standard_closeout
import f0_action_ray_gate
import f0_action_kernel_dynamics_gate
import f0_kernel_class_gate
import f0_vacuum_orbit_gate
import f0_transition_ray_gate
import f0_direction_gate
import gravity_curvature
import gravity_gate_audit
import jordan_standalone_theorems
import padic_hierarchy
import causal_set_lambda
import entropic_gravity_cho
import everpresent_lambda_tracking
import causal_growth_index
import statistical_flavour_ensemble
import positive_geometry_cluster
import adelic_constant_relation
import big_bets_closeout
import berry_sigma_model_op2
import berry_pi_intrinsic_op2
import f4_breaking_seed_op2
import f0_sigma_model_closeout
import f4_breaking_action_origin_gate
import f4_breaking_beta_selection_gate
import f4_breaking_primitive_level_gate
import f4_breaking_level_one_carrier_gate
import f4_breaking_born_beta_map_gate
import f4_breaking_born_geometry_gate
import f4_breaking_source_stationarity_gate
import f4_breaking_calibrated_source_action_gate
import f4_breaking_large_deviation_source_gate
import theory_probation_closeout
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
    ("f0_phase1_closeout",
     "F0 PHASE 1 CLOSEOUT — the make-or-break finite-spectral-triple gate is fully executed (1.1 obstructions -> 1.2 associative rebuild + octonionic Yukawa L_X -> 1.3 heat-kernel refutation -> 1.4 spectrum localisation), and this artifact consolidates its TWO independent decisive results into one falsifiable statement of where F0 stands. It is NOT another invariance witness (the roadmap warns ~24 of those is past diminishing returns) — it is the opposite, the closeout that records the decision point, by importing the two source-of-truth numbers. [A] PREFACTOR route (Phase 1.3, re-derived from the genuine 216-dim step-C Dirac via f0_spectral_action_heatkernel): a2=Tr(D^2)=92.96=2324/25, a4=Tr(D^4)=50.3712=31482/625, so a4/a2=M4/M2^2=0.00582895 is a pi-FREE rational and can never equal the transcendental pi/432=0.00727221 (gap 0.00144) — pi/432 is NOT a spectral-action output (the only spectral pi is the continuum (4pi)^(-d/2)). [B] RATIO route (Phase 1.4, imported from spectral_action_432.ladder_mismatch): the octonionic L_X forces the averaging law {a,b,c}u{(a+b)/2,...} (constants_out=3, mixing=arithmetic mean) but the best single-knob eps0 ladder (1,eps0,eps0^2) MISSES the measured charged-lepton hierarchy by 1.40 decades — the spectrum forces the STRUCTURE but not the absolute generation profile (one open scalar seed function). [C] CONVERGENCE: the prefactor (a single transcendental constant) and the ratios (a set of multiplicative ratios) are INDEPENDENT tests, yet BOTH localise the entire remaining F0 gap to the SAME missing object — a DYNAMICAL/VARIATIONAL principle (an ACTION) that would have to (i) PRODUCE pi/432 as a spectral-action output [refuted in 1.3] AND (ii) SELECT the three diagonal seed eigenvalues [the lone open function in 1.4]. The algebra + symmetry + spectral triple supply NEITHER, which is exactly gold-standard criterion 1 (action -> EoM -> vacuum -> spectrum), listed ABSENT; foundations/02_action.md is a candidate, not a derivation. [D] FORK OUTCOME (bounded, moves no credit): Phase 1's decisive experiment landed on the KILL side for the DYNAMICAL route, bounded — F0 stays GEOMETRIC/open: the Berry/Schur pi/432 reading SURVIVES (not demoted), the mass STRUCTURE (averaging law, the (0,2,4) seesaw skeleton, the GJ {1,3,8} prefactors) is derived, but neither pi/432 nor the absolute hierarchy is promotable to DERIVED without the missing action. PHASE 2 (one operator -> masses+CKM+PMNS) is GATED on this same dynamical seed selection. No Bayes credit moves; the scoreboard ladder (-21.3 historical / -3.2 EARNED floor / +5.6 if-granted / +36.2 target) and the frozen registry are untouched. Standing position: the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null until the action is derived.",
     f0_phase1_closeout.main),
    ("f0_theta_reality_gate",
     "F0 THETA-REALITY GATE — records the TOPOLOGICAL attempt to close the gate that Phase 1.3 (heat-kernel a4/a2) and Phase 1.4 (spectrum ratios) left open, so the route is never re-attempted. The candidate identity is pi/432 = theta/dim with theta = pi*nu, nu in {0,1} a Z2 index QUANTIZED by the real structure J (the KO-6 reality), and CHO sitting in the nu=1 class. This is a genuinely DIFFERENT channel from Phase 1.3: a theta-term is NON-perturbative — it never appears in the rational Seeley-DeWitt moments Tr(D^2k) — so 1.3's rational-moment kill does not touch it, and a first-power pi in the NUMERATOR (which pi/432 has) is exactly the holonomy/topological signature. On the genuine 216-dim octonionic KO-6 Dirac D, all THREE natural sources of a theta=pi vanish, robustly across every seed and with the Majorana sector on or off: [A] SPECTRAL-ASYMMETRY (eta) theta = pi*eta(D) — but D is gamma-ODD (gamma D = -D gamma, residual 0), so its spectrum is EXACTLY +/- symmetric (108/108, no zero modes) and eta = #(lambda>0)-#(lambda<0) = 0 identically; the very grading that DEFINES chirality forces the spectral-asymmetry theta to zero; [B] CHIRAL mod-2 INDEX nu = dim ker(D:H+->H-) mod 2 — the chiral block is FULL RANK (rank 108, zero kernel) so nu=0, no protected Z2; [C] KRAMERS/FU-KANE Z2 — the time-reversal topological-insulator theta=pi invariant requires J^2=-1 (Kramers, class AII), but KO-6 has J^2=+1 (the REAL class) so this invariant is not even defined. VERDICT: theta = pi*nu = 0 across all cases, so the candidate pi*nu/432 = 0 != pi/432 = 0.00727221 — the topological-theta route is CLOSED. This is the THIRD independent converging-negative (joining the Phase-1.3 prefactor and the Phase-1.4 ratios): all three localise the remaining F0 gap to the SAME object and for the SAME reason — each is KINEMATICS/TOPOLOGY, and the gap is DYNAMICS. The pi the program legitimately has is the Berry half-solid-angle (1/2)(2 pi) = pi, a holonomy of the CONTINUOUS vacuum-selection Bloch sphere (a property of the still-missing action that picks the vacuum direction), NOT a topological invariant of the finite operator D. So pi/432 is not a theta-angle of D either; it stays the Berry/Schur GEOMETRIC quantity it always was. Scope is honest: this refutes theta=pi for THIS finite KO-6 triple via its three natural sources, not for every conceivable construction — but it closes the concrete route proposed. F0 stays GEOMETRIC/open (not demoted — the geometric reading is untouched; not promoted — no new earn-path opened); no Bayes credit moves; the scoreboard ladder (-21.3 / -3.2 / +5.6 / +36.2) and the frozen registry are untouched.",
     f0_theta_reality_gate.main),
    ("gold_standard_closeout",
     "PROGRAM CLOSEOUT — the program-level analogue of f0_phase1_closeout: it consolidates the WHOLE seven-point gold-standard scorecard (ROBUSTNESS_ACTIONS.md) into one executable, tamper-evident statement and ASSERTS the honest-null standing position against its source-of-truth modules, so the Fail-branch position cannot silently drift into over-claim. It is NOT a new physics result and NOT another invariance witness; it is the capstone that records where the INTERNAL program terminates. [1] HEADLINE: imports scoreboard.scoreboard() and freezes the ln B credit ladder — historical -21.3 (pre-eps0, 8/3 only) -> closed-theorem floor -3.2 (today's EARNED position) -> +5.6 if the geometric pi/432 is GRANTED -> +36.2 if the program completes — asserting it is strictly monotone with the SIGN FLIP located exactly at the pi/432 grant, i.e. on EARNED credit the numerology null still wins (floor < 0). [2] SCORECARD: prints all seven criteria, each tied to its source, with a rigour census from audit_contract.CONTRACTS (>=1 THEOREM, ~30 OPEN_BRIDGE) and a guard that the headline F0 closeout and the one-operator gate are still OPEN_BRIDGE (not silently promoted), plus the frozen prediction_registry digest MATCH. [3] CONVERGENCE: re-runs f0_phase1_closeout's prefactor + ratio routes to re-verify criterion 1 ABSENT, and records that criteria 1, 3 and the open half of 2 all localise to the SAME missing derived dynamical action, while the external criteria (4 DUNE/Hyper-K, 7 peer review) and the falsified single UV scale (6) are not closable by more internal work. [4] STANDING POSITION: ship the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null; this gate moves NO Bayes credit and touches no frozen artifact.",
     gold_standard_closeout.main),
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
    ("padic_hierarchy",
     "BIG-BETS Bet 1 (EXPLORATORY): reads the three power-of-three mass-hierarchy exponents arithmetically. EXACT facts (asserted): 9,36,64 are perfect squares whose consecutive increments are +27=dim J3(O) and +28=dim so(8) — a homogeneous ladder where the repo's labels were heterogeneous (|roots+E6|, dim A, 'seesaw'); 3-adically each ratio is unit-ordinary (|.|_3=3^e, adelic product=1) so the ~1e-17 electroweak smallness is purely an archimedean artefact, reframing WHY a real-analytic spectral action (over R) could never emit these scales. The EW hierarchy sits within 0.01 of an exact power of 3 (base-3-clean; non-power-of-3 bases are not), but CC needs the sqrt2*12/11 prefactor and is NOT base-3-clean — reported honestly. A seeded look-elsewhere Monte-Carlo null leaves the {perfect-square + increments-in-catalogue} conjunction SUGGESTIVE-ONLY (corrected p~0.018, above the 0.001 promotion bar). VERDICT: exponents stay CHOSEN, no Bayes credit moves; the module asserts the exact arithmetic AND a humility tripwire that the corrected p stays above the bar so it cannot silently become a 'result'.",
     padic_hierarchy.main),
    ("causal_set_lambda",
     "BIG-BETS Bet 2 (EXPLORATORY): bridges CHO's cosmological-constant exponent to Sorkin's causal-set heuristic Lambda~1/sqrt(V) (a Poisson fluctuation of the spacetime-atom count, the one pre-data causal-set success: it predicted Lambda~10^-122 before 1998). EXACT facts (asserted): Sorkin V=Lambda^-2 round-trips exactly; CHO's Lambda/M_P^4 is NOT exactly 3^-256 (the (11/12)/sqrt2 prefactor shifts log_3 to -257.6, the SAME CC contamination Bet 1 found); the observed cosmic 4-volume sits at 10^244 for every standard convention (Hubble, age, particle horizon); and Lambda^(1/4)~V^(-1/8) with 1/8=(1/4 fourth-root)x(1/2 Sorkin) recovers the CHOSEN exponent 64 to within 1 (63.85-64.39 across conventions, spread 0.54). So the single largest CHOSEN chunk in model_complexity gets a candidate STATISTICAL-DYNAMICAL origin (atom-count fluctuation) given base 3 (from Bet 1) + the observed volume. Honest negatives: the 1/8=dim(O) match is a coincidence not leaned on; base 3 is unforced here (base 8 fits the volume better, dist 0.02 vs 0.40); it uses observed V as INPUT, trading 'why 64' for the cosmic-coincidence 'why now'. Sharp falsifier (the payoff): CHO says Lambda is a fixed algebraic constant (w=-1) while Sorkin's everpresent Lambda is dynamical (w(t)!=-1) — incompatible except at the present epoch, so DESI/Euclid w0-wa discriminate; KILL if dark energy is confirmed an exact constant. VERDICT: EXPLORATORY — the exponent stays CHOSEN, CC1/S1 untouched, no Bayes credit moves; the module asserts the exact arithmetic AND a humility tripwire that the convention spread stays wide enough that the bridge cannot be silently promoted to 'derived'.",
     causal_set_lambda.main),
    ("entropic_gravity_cho",
     "BIG-BETS Bet 2 (EXPLORATORY): asks whether counting gives GRAVITY — the other thing CHO gated out — a dynamical origin, via Jacobson 1995 (dQ=TdS + Bekenstein-Hawking S=A/(4G)=A/4 => Einstein's equations as an equation of state). The coefficient 1/4 (= Newton's G) is the pure number the static algebra cannot emit (cf. Lambda, pi/432). EXACT facts (asserted): tiling a horizon with cells of CHO internal dimension d gives S=(A/a_cell)ln d ~ A (the area law is automatic — the structural prerequisite Jacobson needs, the dynamics-from-counting win); matching S=A/4 forces a_cell=4 ln d (d=2 reproduces the textbook it-from-bit 4 ln 2=2.77 Planck-areas/bit); the bit-bookkeeping identity N_cells*log2(d)=N_bits holds exactly for every d, so the CHO dimension is PURE BOOKKEEPING for the coefficient; one CHO state per Planck area overcounts (ln d > 1/4 for every d, the species problem) and the naive match needs d=e^(1/4)=1.28 — no integer/quantum solution. So counting touches only the FORM (area law) and never the CONTENT (the value of G): a cleaner, more decisive negative than the Lambda probe. The sharp payoff is a cross-module tension: the SAME Planck-density causal set that reproduces Lambda (causal_set_lambda) would, via Dou-Sorkin horizon molecules, overcount black-hole entropy by 4 ln d ~ 13x (d=27=J3(O)) UNLESS the CHO internal state is horizon-unresolved (a definite prediction). VERDICT: EXPLORATORY — Newton's G is NOT derived (relocated to a_cell=4 ln d), no prediction promoted, no Bayes credit moves; the module asserts the exact bookkeeping AND a humility tripwire (the required cell area spreads too widely over the CHO menu to pick a unique horizon cell).",
     entropic_gravity_cho.main),
    ("everpresent_lambda_tracking",
     "BIG-BETS Bet 2a deepening (EXPLORATORY): invests in causal_set_lambda's biggest debit (the bridge consumes the OBSERVED 4-volume, trading 'why 64' for the cosmic-coincidence 'why now') by taking Sorkin's EVERPRESENT reading seriously as a DYNAMICAL dark energy. Two readings of the SAME exponent: CHO-static (Lambda a fixed algebraic constant, w=-1 exactly, so Omega_Lambda(z)=Omega_L,0/E(z)^2 dilutes to zero at high z) vs Sorkin-everpresent (Lambda ~ +/- 1/sqrt(V(t)) ~ H(t)^2 tracks the critical density, Omega_Lambda(z) ~ O(1) at every epoch). EXACT facts (asserted): the present-epoch anchors land (Hubble 4-volume today ~10^244, Lambda_everpresent today = H0^2 ~ 10^-122); the everpresent fraction is epoch-independent by the Sorkin scaling while the static fraction dilutes (Omega_static(z=1100) < Omega_L/3); the two readings diverge as Om_ever/Om_static = E(z)^2, reaching ~6e8 at recombination; and the redshift SHAPE of that divergence is INVARIANT under the CHO normalization/exponent (it cancels in the ratio). So the deepening (a) partly repays the why-now debit ('O(1) now' becomes 'O(1) always' — a property of the counting law, not CHO) and (b) turns the constant-vs-dynamical hook into a COMPUTED, live falsifier (DESI/Euclid w0-wa tomography; the 2024-25 evolving-DE hints point away from w=-1). Honest core: the entire testable time-structure is CAUSAL-SET content — CHO is a SPECTATOR in the dynamics (it sets only today's normalization), so a confirmed evolving-DE signal would support SORKIN over the CHO-STATIC reading, making CHO's own w=-1 the casualty. Caveat kept in view: a strictly smooth Lambda~H^2 is degenerate with a rescaled Newton constant, and the genuine dark-energy content lives in the sign fluctuations (Ahmed et al. 2004; Zwane et al. 2018) not simulated here — the magnitudes are heuristic, not a fit. VERDICT: EXPLORATORY — no prediction promoted, no Bayes credit moves; the module asserts the exact anchors, the computed divergence, and a CHO-spectator tripwire (the divergence shape is independent of the CHO exponent) so the deepening cannot be silently read as CHO predicting dark-energy evolution.",
     everpresent_lambda_tracking.main),
    ("causal_growth_index",
     "BIG-BETS Bet 2 CRUX (EXPLORATORY): the make-or-break test — does causal-set GROWTH dynamics SEE an internal CHO index and force the generation count N=3? Rideout-Sorkin classical sequential growth (the transitive-percolation case, i.i.d. pre-closure pair inclusions + transitive closure, so both CSG axioms are explicit) with an index s_i in {1..N} coupling via a pairwise inclusion probability p(s_i,s_j). EXACT facts (asserted): index-blind growth is covariant on every poset — counting supplies a genuine measure on histories (gold-standard criterion A, the object the static algebra lacked); discrete general covariance is equivalent to the coupling being SYMMETRIC (a related pair always has its lower element born first, so its factor is birth-order independent automatically, while an incomparable pair {a,b} appears as 1-p(s_a,s_b) in one birth order and 1-p(s_b,s_a) in another — verified: an asymmetric 2x2 coupling splits the two extensions of the V poset 0.042 vs 0.126, a symmetric one collapses them); covariance therefore imposes C(N,2) symmetry equations and leaves an N(N+1)/2-parameter family that is NEVER empty, so a covariant NON-spectator coupling exists for N in {2,3,4,5,6} and N=3 is NOT singled out; the index-blind causet marginal is exactly N-independent (the SPECTATOR limit, TV=0 for N=1..5); Bell causality is automatic in the independent-pair model (the growth probability factorises over pairs) for every N — also blind to the cardinality; and even CHO's best shot, a non-trivial inheritance (child index = product of parent indices), is covariant+commutative+associative for EVERY N (Z/N), so the exceptional rank-3 Albert algebra is singled out only by the NON-ASSOCIATIVE octonionic composition — a kinematic (Hurwitz/Jordan classification) input, not something the order-theoretic growth provides. So counting gives the FORM (a covariant, Bell-causal measure on histories) but never the CONTENT (N=3): the Bet-2 crux resolves NEGATIVE, the same FORM-not-CONTENT boundary the Lambda and gravity probes drew. VERDICT: EXPLORATORY — N=3 is NOT derived from dynamics, the generation count stays a kinematic input (G1), no prediction promoted, no Bayes credit moves; the module asserts the covariance obstruction, the exact N-blindness, and a humility tripwire (more than one N admits a covariant non-spectator coupling, so the dynamics cannot be said to 'pick 3').",
     causal_growth_index.main),
    ("statistical_flavour_ensemble",
     "BIG-BETS Bet 3 (EXPLORATORY): the honest fallback for the losing one-number game — stop predicting single Yukawas, predict their DISTRIBUTION. Four 3x3 complex-Yukawa ensembles (CKM = U_u^dag U_d): A anarchy (Ginibre, symmetry-BLIND), B Froggatt-Nielsen hierarchy eps^(qi+qj) only, C NNI texture zeros (1,1),(1,3),(3,1), D the triality-DERIVED (1,3),(3,1) zero only. EXACT facts (asserted): (+) the REAL WIN — distributions DECISIVELY falsify the symmetry-blind null for quarks (anarchy gives LARGE mixing, median sin^2 (12,23,13) ~ (0.51,0.50,0.29), and P(all three CKM moduli <= the observed quark values) ~ 0) while the SAME anarchy stays viable for the anarchic lepton sector (it reaches a PMNS-sized sin^2 theta13 <= 0.022 a few % of the time, but a quark-sized one ~ never) — the observed quark/lepton dichotomy ('anarchy with structure') falls straight out, content the single-number predictions never had; (-) the HONEST NULL — what beats anarchy is the mass HIERARCHY, not the CHO texture: the Gatto-Sartori-Tonin correlation corr(|V_us|, sqrt(m_d/m_s)) (the observed coincidence 0.2243 ~ 0.2236) is ~0 for anarchy but ~+0.48 for the Froggatt-Nielsen hierarchy ALONE (in FN both |V_us| and sqrt(m_d/m_s) scale as eps^(q1-q2)), and adding CHO's DERIVED triality zero lifts it only ~+0.07 more — the hierarchy's contribution to the correlation STRICTLY exceeds the texture zero's (asserted humility tripwire). The discriminator is the eps-ladder (the same charged input the scoreboard already debits via F0), and the NNI texture is emitted by every Froggatt-Nielsen model, not uniquely CHO. So counting the distribution gives the FORM (a sharp many-observable falsification that kills anarchy) but not the CONTENT (a CHO-specific texture that beats same-hierarchy symmetry-blindness): the same FORM-not-CONTENT boundary the Lambda, gravity, and growth-index probes drew, now on the flavour-statistics face. EXPLORATORY: the single-value C1..C4 bridges are untouched; NO Bayes credit moves.",
     statistical_flavour_ensemble.main),
    ("positive_geometry_cluster",
     "BIG-BETS Bet 4 (EXPLORATORY): does the positive geometry FORCE the CHO arena, or merely host it? The amplitude is the canonical form of a positive geometry (dynamics from geometry, no Lagrangian); its computable skeleton is the cluster algebra (Fomin-Zelevinsky finite-type <-> Dynkin diagrams), and the exceptional types CHO privileges already surface in amplitudes (the Gr(3,6) cluster algebra is type D4 = so(8) = triality = the 3-generation symmetry; Gr(3,7) and Gr(4,7) are type E6 = the reduced structure group of J3(O)). EXACT facts, all exact integer arithmetic from the Dynkin degree tables (asserted as tripwires): (+) HOSTING is real and exact — D4 (triality) has exactly 16 cluster variables (almost-positive roots = dim C(x)H, the recurring Spin(9) spinor 16) and dim 28 (= dim so(8)); E6 (J3(O)) has exactly 36 positive roots (the repo's own M_W = M_P/3^36 exponent label '||Roots+(E6)||') and its minuscule rep is the 27 (= dim J3(O) = the 27 lines on a cubic surface = |W(E6)|/|W(D5)|); the hierarchy-exponent increments {27,28} = {36-9, 64-36} = {dim J3(O)=E6 minuscule, dim so(8)=D4 adjoint}; and E6 is the UNIQUE exceptional group with a Z/3 centre, so base-3 is structurally distinguished for exactly the algebra CHO uses — criterion B (reuse) passes cleanly. (-) but HOSTING is not FORCING — those integers (16,27,28,36) are root-system / representation data CHO ALREADY ingests, not a new forcing or prediction; the genuinely cluster-SPECIFIC invariant, the cluster count = the number of cells of the positive geometry, is NEVER a CHO integer and in particular is NEVER the generation count 3; the matches are non-unique (27 is also the A6 cluster-variable count, not E6-unique) and multi-hosted (D4, E6, F4, G2 each carry some CHO integer, so the machinery does not SELECT the CHO arena — a humility tripwire); the seductive products are near-miss traps (432 = 16*27 vs the A6 cell count 429; 64 vs the E7 positive-root count 63 — exactly the coincidence-hunting the scoreboard punishes); the Z/3 centre that distinguishes base-3 lives in E6 representation theory (a CHO input), not in the canonical-form dynamics, and is NOT the triality/generation Z/3 (which permutes the three J3(O) blocks inside F4); and the actual octonionic positive geometry (a canonical form whose cells ARE the three generations) is NOT constructed — octonion non-associativity obstructs the standard commutative, totally-positive cluster-coordinate construction, which is precisely why the bet is highest build cost / fuzziest near-term kill. So counting the cells gives the FORM (a combinatorial skeleton that happily contains CHO's integers) but never the CONTENT (a geometry that FORCES them): the fifth face of the same FORM-not-CONTENT boundary the Lambda, gravity, growth-index, and flavour-statistics probes drew. EXPLORATORY: no constant promoted from CHOSEN to derived; the hosting is a consistency, not a derivation; NO Bayes credit moves.",
     positive_geometry_cluster.main),
    ("adelic_constant_relation",
     "BIG-BETS Bet 1 SECOND probe (EXPLORATORY): the Moonshine follow-on padic_hierarchy named — where #77 read the three hierarchy EXPONENTS additively (perfect squares, increment ladder), this reads the CONSTANTS THEMSELVES MULTIPLICATIVELY (prime factorisation) and asks whether the WHOLE predictive set is ONE arithmetic object. EXACT facts (asserted as tripwires): (+) every constant that ENTERS a CHO prediction is an S-unit over the SAME three primes {2,3,7} — 432 = 2^4*3^3 = 16*27 (so v2(432)=4=dim H, v3(432)=3=generations), the only eps0-free mixing prediction sin^2(theta23)=4/7 (cos^2=3/7) is the Fano line-count split 7 lines = 4 (avoid the vacuum) + 3 (through it), the power-of-three exponents 9,36,64 and the arena dims 16,27,28,14 all factor on {2,3,7}, and the octonion/Fano automorphism order |Aut(Fano)|=|PSL(2,7)|=|GL(3,2)|=168=2^3*3*7 has prime support EXACTLY {2,3,7}; and those three primes are precisely the octonion-distinguished ones (2 = Cayley-Dickson doubling / div-algebra dims 2^k, 3 = triality / Jordan rank 3 / three generations, 7 = Im(O)=R^7 / the 7 Fano points = 7 lines). So the adelic reading is internally coherent and EXTENDS padic_hierarchy from the exponents to the whole multiplicative set — the same reason a real-analytic spectral action over R could never emit these numbers. (-) but HOSTING is not FORCING: {2,3,7}-smoothness is GENERIC for small integers (base rate ~0.41 below 50, ~0.12 below 512, far above any promotion bar), it BREAKS inside CHO's OWN vocabulary — the dimensions of the very structure groups CHO is built on are not {2,3,7}-smooth (dim F4=52=2^2*13, dim E6=78=2*3*13, dim E7=133=7*19, dim E8=248=2^3*31 bring in primes 13,19,31), so smoothness is a property of the SUBSET entering numerical predictions, not a theory-wide law (if the arithmetic were FORCED, F4 and E6 would obey it); and NO single arithmetic relation generates the set — 432 is not a j-function or Monster coefficient (the genuine Moonshine anchor 196884=196883+1 has no 432 analogue), and the only S-unit equations among the constants are trivial (7=4+3, the 4/7 split; and the additive increment ladder already in #77). The factorisation 432=16*27 just re-expresses the arena CHO already ingests; nothing moves from CHOSEN. The sixth face of the FORM-not-CONTENT boundary, with a real conceptual extension on the (+) side. EXPLORATORY: the exponents and the 4/7 mixing stay as charged, NO Bayes credit moves; the module asserts the exact factorisations, the firewall that the pattern breaks on F4/E6/E7/E8, and a humility tripwire that {2,3,7}-smoothness stays common (never a rarity that could be mistaken for a result).",
     adelic_constant_relation.main),
    ("big_bets_closeout",
     "BIG-BETS CLOSEOUT (EXPLORATORY): the capstone over the whole big-bets branch — the analogue of gold_standard_closeout for the internal program. A REPORTER (re-derives nothing; grants no Bayes credit) that consolidates the four ranked bets / eight EXPLORATORY modules (#77-#84) into the SIX FORM-not-CONTENT faces — Lambda (causal_set_lambda, everpresent_lambda_tracking), gravity/G (entropic_gravity_cho), the generation count N=3 (causal_growth_index), flavour texture (statistical_flavour_ensemble), the exceptional arena (positive_geometry_cluster), and the constants (padic_hierarchy, adelic_constant_relation) — and records the one finding they triangulate: EVERY bet supplied the FORM the static algebra lacked (a counting measure, an automatic area law S~A, a covariant Bell-causal growth law, a sharp distributional falsifier of anarchy, an exact positive-geometry host, an adelic reframing) but NONE forced the CONTENT (the exponent 64, the 1/4 in S=A/4, the number 3, a CHO-specific texture, arena SELECTION, the specific values). Six outside directions, ONE boundary — which CONFIRMS gold_standard_closeout from new directions: the lone missing object is SINGULAR, a derived dynamical action that selects the seed/value, not a different gap per sector. Source-of-truth tripwires (asserted): all 8 probes are still STATUS_EXPLORATORY/VERDICT_OPEN and still humble (>=1 open bridge AND >=1 kill condition, so none was silently promoted); the six faces partition exactly those 8 modules; and the EARNED scoreboard floor is still ln B=-3.2<0 (the whole arc moved NO credit, the null still wins). The one (+) keeper is a DIAGNOSIS, not a derivation — the CHO constants are arithmetic objects on the octonion primes {2,3,7} (432=16*27) that a real-ANALYTIC spectral action over R could never emit, which is WHY Phase 1 hit its wall; it reframes the gap, it does not close it. Recorded STATUS_EXPLORATORY / VERDICT_OPEN; forbids only SILENT drift.",
     big_bets_closeout.main),
    ("berry_sigma_model_op2",
     "DECISIVE topological-route test for pi/432 (EXPLORATORY): the single internal experiment that could flip the scoreboard sign WITHOUT a grant. Phase 1.3 (f0_spectral_action_heatkernel) REFUTED the analytic route — for the finite octonionic triple the spectral-action ratio a4/a2 = M4/M2^2 = 0.00582895 is a pi-FREE rational, so it can never equal the transcendental pi/432 = 0.00727221 (the only pi a spectral action emits is the continuum (4 pi)^(-d/2)); the big-bets adelic keeper argued the same for a real-analytic action over R. BOTH refutations point one way: the object that carries pi is TOPOLOGICAL, not analytic. This module assembles that alternative as ONE decisive experiment — a Berry/Wess-Zumino sigma-model whose target is the triality-vacuum manifold OP^2 (the rank-one idempotent variety of J3(O), dim 16 = the E6 minimal orbit) with the E6-invariant cubic norm N3 as the potential, S[path] = (Berry/WZ kinetic on OP^2) - (N3 potential) — and tests the TWO independent halves that must BOTH pass to flip the sign for real. [FORM] PASSES (asserted as tripwires): the Berry holonomy of the minimal great-circle (geodesic) loop of ACTUAL rank-one J3(O) idempotents is pi (= 1/2 * 2pi enclosed solid angle), cross-checked against the source-of-truth great-circle phase (epsilon_action_selection.candidate_action_angle = action_derivation.berry_phase_of_latitude(pi/2)); a non-geodesic latitude loop (theta=pi/3) gives pi/2, so pi is the geodesic-selected holonomy specifically; and the loop runs over genuine rank-one trace-1 projectors (|P^2-P|~1e-16, rank 1). So the topological kinetic term DOES emit pi — the right kind of object, succeeding exactly where the analytic spectral action provably cannot. [CONTENT] FAILS, for a STRUCTURAL reason that IS the result (asserted): N3 = det = 0 on ALL of OP^2 (every point is rank-one; max|N3|~0, max|X#|~0) and the J3(O) spectrum is identically (1,0,0) there, so N3 — and indeed EVERY F4-invariant, since F4 preserves the spectrum — is CONSTANT on the vacuum manifold and cannot lift its degeneracy to select three distinct eigenvalue-seeds; the measured charged-lepton hierarchy (0.94362, 0.05611, 0.00027) on the eigenvalue simplex is a NON-symmetric triple that is NOT an N3 critical point (|grad N3|=0.043 there) while the all-EQUAL state I/3 — the global MAXIMUM N3 = 1/27 — IS (grad 0): the ANTI-hierarchy; and the best single-knob eps0 ladder misses the hierarchy by ~1.40 decades (spectral_action_432). NET (the new, sharp content): the sigma-model SEPARATES pi/432 — the FORM (pi) is reachable by the topological route (the kinetic term is SETTLED), but the CONTENT (the seeds) is NOT reachable from any F4-invariant potential and REQUIRES an F4-BREAKING seed-selection term — a NEW symmetry no-go that localises the ENTIRE remaining gap to one object with the kinetic pi now topological and fixed. The scoreboard sign does NOT flip (CONTENT failed): pi/432 is NOT promoted, no Bayes credit moves, F0 stays GEOMETRIC/open. CONFIRMS Phase 1.4 (structure forced, absolute seed open) from an independent dynamical direction, and converts it into a symmetry no-go. EXPLORATORY: F0 not promoted, no Bayes credit moves.",
     berry_sigma_model_op2.main),
    ("berry_pi_intrinsic_op2",
     "HARDENS the FORM (the pi) of pi/432 (EXPLORATORY): the pi berry_sigma_model_op2 emitted was measured on ONE associative CP^1 slice; this proves it INTRINSIC to OP^2 and a half-turn. [A] the transition sphere's two antipodal poles are ORTHOGONAL primitive idempotents E1,E2 (Tr(E1 o E2)=0 = two generations); gamma(theta)=pi(1-cos theta) exactly, and the great circle (the geodesic equidistant from the two orthogonal generations) encloses the hemisphere and gives pi, so pi is the holonomy that SEPARATES two orthogonal generations, not an input. [B] pi is F4-INTRINSIC: F4=Aut(J3(O)) is an isometry of the trace metric (verified ~1e-13), so transporting the loop by a random automorphism keeps it rank-one idempotents (PoP=P, N3=0), preserves every overlap Tr(P_i o P_{i+1}) (the metric data the phase=1/2*area depends on), yet moves it into genuinely OCTONIONIC directions (e2..e7 ~0.2); OP^2=F4/Spin(9) is two-point-homogeneous, so every geodesic 2-sphere is an F4-image and the phase is the SAME pi. [C] the half-turn is the SU(2) sign flip: the great-circle Bargmann product is real-NEGATIVE (e^{i pi}=-1; cf. epsilon_vcb_halfangle tan(pi/8)). Hardens the kinetic term against the octonionic directions WITHOUT evaluating an ill-defined octonionic Bargmann product (it proves the phase-determining trace data is F4-invariant). CONTENT (the three seeds) stays open (every F4-invariant flat on OP^2, needs an F4-BREAKING term); no Bayes credit moves, pi/432 NOT promoted, F0 stays GEOMETRIC/open.",
     berry_pi_intrinsic_op2.main),
    ("f4_breaking_seed_op2",
     "LOCALIZES the CONTENT (the three seeds) of pi/432 (EXPLORATORY): berry_sigma_model_op2 proved seed-selection needs an F4-BREAKING term (N3 and every F4-invariant flat on OP^2); this tests whether the framework's OWN canonical F4-breaking object — the rank-one triality-breaking vacuum spurion |tau><tau| (epsilon_rank_one_kernel, spurion_bridge) — supplies it. TWO-SIDED result. [POSITIVE / no-go EVADED, asserted as tripwires] the linear frame-breaking height V_A(P)=Tr(P o A) has, on OP^2, critical points EXACTLY at the three primitive idempotents E1,E2,E3 of A's eigenframe (standard Morse theory of a height function on the flag manifold F4/Spin(9)): the F4-gradient g_D=Tr((D.P) o A) vanishes (~1e-16) at all three generations for frame-diagonal A, gradient ASCENT from 6 random OP^2 points flows to the top generation (overlap 1.0000), and the control A=I (F4-invariant) is flat (V=Tr P=1, grad ~1e-15 — reproduces the no-go). So the three generations ARE the critical set of the canonical frame-breaking potential, and the DIRECTION is frame-canonical NOT circular — any distinct-spectrum A in the generation frame gives the SAME three critical points (only the values change). [HONEST OPEN, asserted] the critical VALUES are V_A(E_i)=spec(A): the seed MAGNITUDES are the spurion spectrum (the input), and the canonical vacuum spurion is RANK-ONE, lifting EXACTLY ONE level (V(E_tau)=1, the whole OP^1 orthogonal to E_tau degenerate at 0 — geometric spurion_perturbation FACT 1), so three ISOLATED tiers require CUMULATIVE orders A=E1+eps0 E2+eps0^2 E3 whose spectrum (1,eps0,eps0^2) reproduces the cascade ladder, leaving the absolute scale eps0^2=pi/432 (the measure) as the lone surviving input. NET: tightens 'needs an F4-breaking term' into 'the F4-breaking term IS the rank-one vacuum spurion; it makes the three generations the critical points (real, non-circular direction), rank-one-ness forces the cascade, the lone open scalar is eps0^2=pi/432'. CONTENT LOCALIZED not closed; no Bayes credit moves, pi/432 NOT promoted, F0 stays GEOMETRIC/open.",
     f4_breaking_seed_op2.main),
    ("f0_sigma_model_closeout",
     "F0 SIGMA-MODEL CLOSEOUT (EXPLORATORY): the capstone over the OP^2 Berry/Wess-Zumino sigma-model route to pi/432 — the dynamical/topological analogue of f0_phase1_closeout for the spectral-triple route. A REPORTER (re-derives nothing; grants NO Bayes credit) that consolidates the three sigma-model EXPLORATORY modules (berry_sigma_model_op2 #86, berry_pi_intrinsic_op2 #87, f4_breaking_seed_op2 #88) and records the route as the FOURTH independent converging-negative on the one missing dynamical action, alongside the three prior routes it CITES as source-of-truth: prefactor (f0_spectral_action_heatkernel: the finite spectral action's a4/a2=0.00582895 is a pi-FREE rational, never pi/432), ratios (spectral_action_432: the averaging-law spectrum forces structure but the best single-knob eps0 ladder misses the absolute charged-lepton hierarchy by ~1.40 decades), and topological-theta (f0_theta_reality_gate: KO-6 forces theta=0). All four localise the ENTIRE remaining F0 gap to the SAME single object — a derived dynamical action that must both PRODUCE pi/432 and SELECT the three seeds — which CONFIRMS f0_phase1_closeout from the dynamical/topological side. The one genuinely-new thing this route adds (the SHARPENING) is what KIND of action is missing: #86's no-go proves any F4-INVARIANT action is flat on the vacuum manifold OP^2 (N3 and every F4-invariant constant there), so the missing action must BREAK F4; #88 then shows the canonical F4-breaking object — the rank-one vacuum spurion — supplies the DIRECTION (the three generations are EXACTLY the Morse critical points of the frame-breaking height V_A(P)=Tr(P o A), frame-canonical and non-circular) but NOT the MAGNITUDE (the critical values are spec(A) input; the absolute scale eps0^2=pi/432 is the lone surviving input). So 'need a derived action' sharpens to 'need a derived F4-BREAKING action whose flux is pi/432 and whose spectrum is the seed': DIRECTION solved, MAGNITUDE open. Source-of-truth tripwires (asserted): the three sigma-model probes are still STATUS_EXPLORATORY/VERDICT_OPEN and still humble (>=1 open bridge AND >=1 kill condition, so none was silently promoted); the four converging-negative routes are all real audited contracts; and the EARNED scoreboard floor is still ln B=-3.2<0 (the whole route moved NO credit, the null still wins). The scoreboard sign does NOT flip (only BOTH halves passing would, and CONTENT/magnitude stays open): pi/432 stays Berry/Schur GEOMETRIC, F0 stays GEOMETRIC/open. Recorded STATUS_EXPLORATORY / VERDICT_OPEN; forbids only SILENT drift. Standing position: the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null + the one live external lever (sin^2 theta23=4/7, DUNE/Hyper-K); further internal derivations of pi/432 are the treadmill.",
    f0_sigma_model_closeout.main),
    ("f4_breaking_action_origin_gate",
     "F0 action-origin modulus gate (EXPLORATORY): tests whether the current OP^2 height dynamics and entropy/free-energy completion derive the spectrum of the F4-breaking spurion. Result: the height family A(r)=E1+rE2+r^2E3 has the same generation critical set and qualitative ascent dynamics for a continuum of r, while entropy + grade energy gives Gibbs ratios (1, exp(-beta), exp(-2 beta)) for a continuous beta. Matching eps0 requires beta=-log(eps0)=0.5 log(432/pi), but this scalar is not selected. Narrows the live route to deriving beta or r=eps0 from CHO dynamics; no Bayes credit moves.",
     f4_breaking_action_origin_gate.main),
    ("f4_breaking_beta_selection_gate",
     "F0 beta-selection gate (EXPLORATORY): tries the next scalar-fixing mechanisms after the modulus gate. Entropy constraints select beta only after a mean grade is supplied; natural means such as 1/16, 1/27, 1/8, 1/7, 1/3 miss the target, while the target mean is fitted. Dimension-only selectors give 1/432, 1/16, 1/27, 1/7, not pi/432; the exact target appears only by postulating exp(-2 beta)=Berry flux/state count=pi/432. WZ level quantisation leaves the family k*pi/432, so k=1 requires an extra primitive-sector rule. Additive Berry/Schur constants drop out of beta stationarity. Narrows the live bridge to deriving a genuine beta-dependent CHO variational term; no Bayes credit moves.",
     f4_breaking_beta_selection_gate.main),
    ("f4_breaking_primitive_level_gate",
     "F0 primitive-level gate (EXPLORATORY): promotes the WZ-level sub-bridge into the audit harness. Filling-independence of exp(iS_WZ) for S_WZ=(k/2)Omega forces k to be an integer, killing continuous WZ-normalisation freedom. With Schur carrier weight 1/432 the half-turn density is k*pi/432; primitive positive k=1 gives exp(-2 beta)=pi/432 exactly. But integrality alone leaves many positive admissible levels (1..137 with k*pi/432<1), so k=1 remains a primitive-sector selection rule, not a derived dynamical output. Narrows the live bridge to deriving primitive level-one selection from CHO dynamics; no Bayes credit moves.",
     f4_breaking_primitive_level_gate.main),
    ("f4_breaking_level_one_carrier_gate",
     "F0 level-one carrier gate (EXPLORATORY): adds the already-audited two-level transition carrier to the WZ integrality result. CP^1 geometric quantization at integer level k has Hilbert dimension k+1; the A4/Q8 carrier is the fundamental two-state system, so only k=1 matches the transition qubit. This removes the discrete primitive-level ambiguity once the two-level carrier is granted: k=1 gives density pi/432 and beta=-log(eps0). It still does not derive the beta-dependent CHO variational map exp(-2 beta)=density or the full F4-breaking action, so no Bayes credit moves.",
     f4_breaking_level_one_carrier_gate.main),
    ("f4_breaking_born_beta_map_gate",
     "F0 Born beta-map gate (EXPLORATORY): tests the local map from the selected level-one WZ density to the Gibbs seed amplitude. The carrier gate gives a probability/flux density d=pi/432; the F4-breaking cascade uses amplitude ratios. Under the Born square map r=sqrt(d), beta=-log(r), so exp(-beta)=eps0 and exp(-2 beta)=pi/432 exactly. Wrong maps visibly miss: treating d as the amplitude, omitting the Berry pi, or using k=2. This closes the density-to-amplitude half-log map once the Born-amplitude interpretation is granted, but it still does not derive the beta-dependent CHO action coupling or a stationarity equation; no Bayes credit moves.",
     f4_breaking_born_beta_map_gate.main),
    ("f4_breaking_born_geometry_gate",
     "F0 projective Born geometry gate (EXPLORATORY): hardens the Born interpretation granted by the Born beta-map gate. In rank-one OP^2/CP^1 projector geometry, Tr(P o Q)=|<psi|phi>|^2, so the selected WZ/carrier density d=pi/432 is a transition probability and the projective amplitude is necessarily sqrt(d)=eps0. The gate checks trace probabilities add to one on an orthogonal generation frame, survive F4 transport into genuinely octonionic directions, and reject wrong readings such as density-as-amplitude, state-count-only, or projective-angle-as-amplitude. This removes the local Born-geometry ambiguity but still does not derive the CHO action coupling or beta stationarity equation; no Bayes credit moves.",
     f4_breaking_born_geometry_gate.main),
    ("f4_breaking_source_stationarity_gate",
     "F0 source-stationarity gate (EXPLORATORY): tests the next conditional rung after projective Born geometry. If the selected WZ/carrier density d=pi/432 is coupled as the source probability for q(beta)=exp(-2 beta), the Bernoulli/KL stationarity equation gives q=d and beta=-log(eps0) uniquely. Wrong source/coupling choices miss. This derives beta stationarity only conditional on the source-channel coupling; the CHO action term that supplies that coupling remains open, and no Bayes credit moves.",
     f4_breaking_source_stationarity_gate.main),
    ("f4_breaking_calibrated_source_action_gate",
     "F0 calibrated source-action gate (EXPLORATORY): tests whether the source-stationarity result depends on the special KL/log-score choice. KL, Brier/quadratic, Hellinger, and logit-quadratic calibrated local source actions all have the same strict stationary point q=d for the projective channel q(beta)=exp(-2 beta), so beta=-log(eps0) is robust inside this calibrated class. Improper controls fail. This narrows the remaining assumption from a KL source term to calibrated source coupling; the CHO action origin of that calibration remains open, and no Bayes credit moves.",
     f4_breaking_calibrated_source_action_gate.main),
    ("f4_breaking_large_deviation_source_gate",
     "F0 large-deviation source gate (EXPLORATORY): tests an out-of-the-box origin for the KL source term. If the projective transition channel is sampled as repeated two-outcome trials and the selected WZ/Born density d=pi/432 is the empirical frequency, finite binomial counting gives the relative negative log-likelihood density exactly as KL(d_hat||q), whose large-deviation limit is the Bernoulli source action. Stationarity again gives q=d and beta=-log(eps0). This derives the KL rate only conditional on an independent projective-transition ensemble; the CHO origin of that ensemble/coupling remains open, and no Bayes credit moves.",
     f4_breaking_large_deviation_source_gate.main),
    ("theory_probation_closeout",
    "THEORY PROBATION CLOSEOUT: preserves the theorem-level core (J3(O) idempotent frame, Schur weights, Freudenthal seesaw, OP^2/Berry geometry), archives failed routes as null records, and states that the SM-constant physics claim can only advance via a derived F4-breaking action whose flux gives pi/432 and whose spectrum gives the seed. If that fails, demote to beautiful algebraic numerology with strong structure, not a theory of nature. Reporter only; no Bayes credit.",
    theory_probation_closeout.main),
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
