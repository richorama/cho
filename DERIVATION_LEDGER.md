# CHO Derivation Ledger

Frozen date: 2026-06-06

Purpose: make the logical status of each CHO claim explicit. This ledger separates theorem-level consequences, derived bridge claims, motivated ansaetze, and numerical comparisons so the project can progress by tightening the weakest links instead of adding more formulas.

Parameter convention: describe CHO as a **few-input** framework. The audit does not fit a separate continuous low-energy parameter for each row, but it does rely on explicit algebraic inputs, bridge assumptions, and continuum/RG matching prescriptions.

## Status Key

| Status | Meaning | What would strengthen it |
|---|---|---|
| Theorem | Mathematical result follows from stated algebraic assumptions | Clean citation/proof and precise physical identification |
| Derived bridge | Formula follows after one named physics-to-algebra bridge is accepted | Derive the bridge from the CHO action or representation theory |
| Open bridge | Numerically strong and structurally motivated, but the bridge is incomplete | Construct the operator, mass matrix, or continuum limit explicitly |
| Ansatz | Motivated formula currently chosen from available algebraic factors | Replace with a derivation or demote from headline count |
| Future test | Not yet experimentally settled | Keep the target fixed and compare against future data |

## Canonical Counting

The compute table currently contains 25 quantitative rows. The paper text often says 23 because some rows are grouped as sector relations rather than listed as individual masses. For external-facing material, use:

- Headline claim: 23 grouped relations, matching Paper 2.
- Audit claim: 25 table rows in `compute/summary_table.py`, where `m_c`, `m_s`, and `m_mu` are displayed explicitly.

Do not mix these counts without explaining the grouping.

## Core Assumptions

| ID | Assumption | Current role | Open issue |
|---|---|---|---|
| A1 | Physics algebra `A = C x H x O` | Starting structure for internal degrees of freedom | Justify uniqueness as physics input, not only post-hoc fit |
| A2 | Fermions are minimal left ideals of `A` | Gives one-generation state space | Tighten map from ideal basis to SM representations |
| A3 | Triality sectors correspond to generations | Gives family structure | Make correspondence functorial/representation-theoretic |
| A4 | CHO information/lattice action sets scales | Source of base-3 suppressions and continuum parameters | Derive continuum limit and RG boundary conditions |
| A5 | Planck mass is the only dimensional input | Fixes all mass scales | Keep all low-energy inputs out of derivations except final comparison |
| A6 | Continuum/RG matching prescriptions | Connects algebraic-scale relations to measured low-energy constants | Derive matching scales and thresholds from the action |

## Quantitative Ledger

| ID | Observable or claim | Formula or value | Status | Main proof obligation |
|---|---|---|---|---|
| G1 | Number of generations | `N_gen = 3` | Theorem, conditional on A2-A3 | Show the three triality reps are physically the three fermion generations, not merely three related reps |
| G2 | No fourth generation | sedenion/J4(O) obstruction | Theorem, conditional on A2-A3 | Clarify why any fourth family must require the obstructed extension |
| S1 | Electroweak hierarchy / W mass | `M_W = M_P / 3^36` | Derived bridge | Derive each `1/3` factor from the lattice action and fix normalization without using `v` |
| S2 | Top mass | `m_t = v / sqrt(2)` | Derived bridge | Prove unique top Yukawa saturation and compute threshold correction |
| S3 | Higgs mass | `m_H = v sqrt(pi/12)` | Derived bridge | Derive Higgs quartic normalization from D4/root geometry in the field theory action |
| S4 | Fine structure constant | `alpha^-1(0) = 128 pi / 3 + VP` | Open bridge | Complete lattice-to-continuum matching and vacuum-polarization calculation |
| S5 | Weinberg angle | `sin^2(theta_W) = 1/4 + RG` | Open bridge | Fix the matching scale and thresholds from CHO, not by inverse running |
| F0 | Triality-breaking parameter | `epsilon_0^2 = pi/432` | Open bridge / conditional projector derivation | `ACTION_PROJECTOR_BRIDGE.md` derives rank-one Fano support after line-pair selection and `PRIMITIVE_PROJECTOR_BRIDGE.md` derives the primitive product from the normalized action once the transition ray exists; still prove the ray, trace space, vacuum selection, and `pi` holonomy from CHO |
| M1 | Charm mass | `m_c = epsilon_0^2 m_t` | Open bridge / partially derived projector | `sector_projector_derivation.py` gives the grade-0 singlet rank `1`; derive why the Yukawa map selects it |
| M2 | Strange mass | `m_s = 3 epsilon_0^2 m_b` | Open bridge / partially derived projector | `sector_projector_derivation.py` gives the grade-1 color-triplet rank `3`; derive the Yukawa trace |
| M3 | Muon mass | `m_mu = 8 epsilon_0^2 m_tau` | Open bridge / candidate operator | Candidate uses full Fock rank `8`; derive why charged leptons trace over the full eight-state space |
| M4 | Tau mass | `m_tau/m_t = sqrt(2) epsilon_0^2` | Open bridge | Derive the tau alignment and normalization directly from CHO Yukawa structure |
| M5 | Bottom mass | `m_b/m_tau = 7/3` | Open bridge | Derive `dim(Im O)/N_c` as an operator ratio, not only a counting rule |
| M6 | Inter-sector ratio | `m_s m_t/(m_b m_c) = 3` | Derived bridge / dependent | Track scheme dependence and covariance with `m_s`, `m_b`, `m_c`, `m_t` |
| M7 | Inter-sector ratio | `m_mu m_t/(m_tau m_c) = 8` | Derived bridge / dependent | Same covariance treatment as M6 |
| M8 | Georgi-Jarlskog ratio | `m_mu m_b/(m_tau m_s) = 8/3` | Derived bridge / dependent | Same covariance treatment as M6 |
| M9 | Up mass | `m_u = (1/4) m_c^2/m_t` | Open bridge / candidate operator | `CHO_OPERATOR.md` embeds the `1/4` weak projector shape; derive uniqueness |
| M10 | Down mass | `m_d = (9/4) m_s^2/m_b` | Open bridge / candidate operator | Candidate gives `(1/4) N_c^2`; derive the sector-square rule |
| M11 | Electron mass | `m_e = (1/4 pi) m_mu^2/m_tau` | Open bridge / candidate operator | Candidate gives `(1/4)(1/pi)`; `sector_projector_derivation.py` shows naive `S6` volume does not derive `1/pi`; compute the actual measure |
| C1 | Cabibbo angle | `|V_us| = sqrt(7) epsilon_0` | Derived bridge | Build and diagonalize the CHO mass matrices directly |
| C2 | CKM 2-3 mixing | `|V_cb| = epsilon_0/2` | Derived bridge | Derive the `1/2` from the same mass-matrix construction |
| C3 | CKM 1-3 mixing | `|V_ub| = (sqrt(2)-1)|V_us||V_cb|` | Open bridge | Derive `sqrt(2)-1 = tan(pi/8)` as a subleading triality/phase effect |
| C4 | Jarlskog invariant | `J = 3.01e-5` | Open bridge / candidate operator | `CHO_OPERATOR.md` derives the Fano phase and shows the Fritzsch placement gives the right J; derive corrected CKM magnitudes and J from one matrix |
| N1 | Heaviest neutrino mass | `m_nu3 = v^2/(2 M_P/3^9)` | Derived bridge | Derive `M_R = M_P/3^9` from the representation/lattice scale hierarchy |
| N2 | Neutrino splitting ratio | `Delta m21^2/Delta m31^2 = 4 epsilon_0^2` | Open bridge / candidate operator | Candidate factorizes the broken-triality target through `Y_nu`; derive `DeltaY` dynamically and identify the actual residual symmetry |
| N3 | PMNS reactor angle | `sin^2(theta13) = 3 epsilon_0^2` | Open bridge / candidate operator | Same `DeltaY` target as N2 |
| N4 | PMNS solar angle | `sin^2(theta12) = 1/(3 + sqrt(7) epsilon_0)` | Open bridge / candidate operator | Derive quark-lepton complementarity from the shared triality operator |
| N5 | PMNS atmospheric angle | `sin^2(theta23) = 4/7` | Open bridge / candidate operator, future sensitive | Derive the `4 of 7` direction count dynamically and track octant data |
| CP1 | Strong CP | `theta_bar = 0` | Derived bridge | Formalize Fano parity as a symmetry of the QCD path-integral measure |
| CC1 | Cosmological constant | `Lambda^(1/4) = (11/12) M_P/(sqrt(2) 3^64)` | Open bridge | Derive free-energy factorization and the `11/12` screening factor without tuning |
| D1 | No WIMP/axion/SUSY/proton decay | Null exclusion claims | Future test | Tie each claim to mass/coupling/lifetime reach and state lower evidential weight than positive quantitative targets |
| STAT1 | 25-row audit table | Median error and pull summary | Descriptive diagnostic | Build minimal independent observable set with covariance; do not present all rows as independent hits |

## Highest-Value Next Proofs

1. Prove that the candidate operator in `CHO_OPERATOR.md` is forced by the CHO action or representation theory.
2. Derive the rank-one epsilon transition, sector projectors, and shape factors inside that one operator.
3. Reconcile CKM corrected magnitudes with the Fritzsch-level Jarlskog phase placement in one charged-Yukawa diagonalization.
4. Resolve the PMNS gap in `OPERATOR_GAP_AUDIT.md`: derive `DeltaY` dynamically and clarify the residual symmetry beyond simple cyclic `Z3`.
5. Rework the statistics around an independent observable set with covariance for mass-derived ratios.
6. Produce continuum/RG matching artifacts for `alpha`, `sin^2(theta_W)`, `M_W`, and `Lambda`.

## Bridge Artifacts

- `compute/flavour_derivation.py` — first scaffold for M9-M11, C1-C4, and N2-N5. It derives charged-sector NNI bridge factors, builds CKM/PMNS unitary matrices, and exposes the remaining CKM Jarlskog phase-placement task.
- `compute/epsilon_bridge.py` — diagnostic scaffold for the `epsilon0^2 = pi/432` trace target, empirical bridge estimates, nearby trace normalizations, and proof obligations.
- `ACTION_PROJECTOR_BRIDGE.md`, `PRIMITIVE_PROJECTOR_BRIDGE.md`, `compute/action_projector_derivation.py`, and `compute/primitive_projector_derivation.py` — action/projector diagnostics showing rank-one Fano support, the Fano-pair automorphism orbit, and the normalized action rank penalty that conditionally selects the primitive `A_Weyl x J3(O)` product.
- `EPSILON_BRIDGE.md` — companion memo defining the `epsilon0^2` bridge state space, proposed trace formula, failure modes, and next proof steps.
- `compute/yukawa_bridge.py` and `YUKAWA_BRIDGE.md` — charged-flavour scaffold deriving leading NNI adjacency and the cascade relation, while isolating sector shape factors as operator targets.
- `compute/pmns_bridge.py` and `PMNS_BRIDGE.md` — PMNS scaffold deriving TBM residual symmetries and printing the broken-triality Majorana perturbation target.
- `compute/cho_bridge_operator.py` and `CHO_OPERATOR.md` — unified candidate operator embedding the epsilon trace, sector projectors, NNI shape factors, Fano phase diagnostics, and PMNS seesaw target.
- `compute/operator_gap_audit.py` and `OPERATOR_GAP_AUDIT.md` — explicit audit of unsolved operator, CKM, PMNS, and continuum/RG gaps.
- `compute/sector_projector_derivation.py` — sector-count diagnostic deriving Fock-grade ranks `1` and `3`, while leaving lepton full-rank trace and `1/pi` as open measure problems.
- `FLAVOUR_DERIVATION.md` — companion memo explaining the scaffold, its inputs, and what remains to be proven by a full CHO Yukawa operator.
- `METHODOLOGY_LIMITS.md` — caveat document for few-input parameter language, postdictions, dependent audit rows, continuum/RG gaps, dimensional-counting risks, and null-test scales.
