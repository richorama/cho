# Critical Repair Plan

Created: 2026-06-07

Purpose: convert the critical review into an executable plan. The rule for this phase is simple: do not add more attractive numerical relations until the load-bearing bridges are either proved, narrowed to one explicit hypothesis, or demoted.

## Review Verdict To Fix

The framework is currently best described as a few-input algebraic phenomenology program with strong representation-theoretic structure and several hard-to-vary numerical relations. It is not yet a strict derivation of the Standard Model parameters, and it is not yet a Theory of Everything. The repair program below is designed to make that boundary move for honest reasons.

The decisive weaknesses are:

1. No unique physics map from `C x H x O` objects to fields, generations, chirality, operators, spacetime, and scales.
2. No single forced Yukawa/seesaw operator that gives masses, CKM, PMNS, and phases in one diagonalization.
3. `epsilon0^2 = pi/432` remains the Bayes-factor hinge unless promoted from geometric triangulation to theorem-level trace/measure result.
4. Continuum and RG matching for `alpha`, `sin^2(theta_W)`, `M_W`, and `Lambda` are not derived.
5. Gravity is still a kinematic internal `G2` result, not a 4D Lorentzian metric with dynamics.
6. External-facing docs still contain claims that read stronger than the ledger permits.

## Hard Operating Rules

- **No new constants rule:** no new fitted prefactor, exponent, or row enters the headline table during this repair phase.
- **One-object rule:** flavour claims must pass through one operator or be explicitly marked as scaffolded.
- **One-scale rule:** continuum claims must state the matching scale and whether it is derived or chosen.
- **Ledger-first rule:** if a result is conditional, the condition appears in `DERIVATION_LEDGER.md` before it appears in public prose.
- **Bayes scoreboard rule:** every promoted derivation must update `model_complexity.py` / `scoreboard.py`; every demotion must also update them.
- **Kill-condition rule:** every workstream has a failure outcome that changes status, not just a success outcome.

## Phase 0 - Claim Hygiene Sprint

**Goal:** make the repository impossible to overread.

**Target files:** `README.md`, `PLAN.MD`, `DERIVATION_LEDGER.md`, `OPERATOR_GAP_AUDIT.md`, `blog_post.md`; old `papers/*.tex` drafts were removed in Phase 7.

**Tasks:**

1. Replace strong public claims with ledger-matched wording.
   - `N_gen = 3`: say count and chirality are obstruction-free via the idempotent-frame route; spectrum and content map remain open.
   - Cosmological constant: say open bridge unless the free-energy factorization and `11/12` screen are derived.
   - Gravity: say kinematic internal metric brick, not dynamical gravity.
2. Refresh stale gap docs against the latest ledger.
   - `OPERATOR_GAP_AUDIT.md` should acknowledge the later progress on lepton `8`, Fano counts, `1/(4pi)` identification, and `|V_cb|` half-angle, while keeping the remaining operator gaps sharp.
3. Add a small `PUBLIC_CLAIMS.md` or equivalent table if claim drift continues.

**Acceptance:** a grep for phrases like `proves N_gen`, `resolves the cosmological constant`, `Theory of Everything`, and `zero parameter` finds either no occurrence or an immediately adjacent caveat.

**Kill/demotion condition:** if a public claim cannot be made ledger-accurate without weakening it substantially, weaken it. The credibility gained is worth more than the slogan lost.

## Phase 1 - Freeze The Axiomatic Physics Map

**Goal:** define the exact map from algebra to physics before any more phenomenology.

**Deliverable:** `foundations/07_physics_map.md` plus a machine witness `compute/physics_map_audit.py`.

**Minimum content of the map:**

1. State space: what exact module carries one generation and what exact module carries three generations.
2. Fermion-content map: how the 16 Weyl states, charge, chirality, weak doublet/singlet split, antiparticles, and generation idempotents sit in one object.
3. Gauge action: explicit `SU(3) x SU(2) x U(1)` action and commutants.
4. Anomaly audit: verify the one-generation hypercharge assignments cancel the SM gauge anomalies.
5. Dirac/Yukawa domain: define the allowed class of mass operators before choosing a mass matrix.
6. Scale map: list which scales are algebraic, which are Planck-input, and which require RG matching.

**Acceptance:** `compute/physics_map_audit.py` prints one table of states with `(generation, chirality, SU(3), SU(2), Y, Q)` and passes charge consistency, chirality consistency, and anomaly cancellation.

**Kill/demotion condition:** if the content map cannot place the SM multiplets without extra per-field choices, mark G1 as `count result / physical content map open` everywhere and stop calling it a generation derivation.

## Phase 2 - Turn `epsilon0^2 = pi/432` Into A Measure Theorem Or Demote It

**Goal:** close the Bayes-factor hinge.

**Deliverable:** `foundations/08_epsilon_measure_theorem.md` plus `compute/epsilon_measure_audit.py`.

**The theorem to prove:** given the CHO action, the rank-one transition space, and the induced invariant measure, the normalized transition trace is uniquely

```text
Tr_transition / dim_phase_space = pi / (16 * 27)
```

with `pi`, `16`, and `27` entering as one forced measure statement, not three assembled facts.

**Tasks:**

1. Define the transition phase space exactly: is it `OP2 x J3(O)`, a bundle over it, a quotient, or a subspace?
2. Define the measure exactly: Berry/Wess-Zumino term, symplectic form, Haar/coset measure, or Bohr-Sommerfeld count.
3. Prove why rank one is selected by the action, not by desired hierarchy.
4. Prove why the `A4` flavour symmetry appears from CHO triality breaking, or explicitly list `A4` as an input bit.
5. Compute nearby alternatives in the audit: rank `r > 1`, `OP2` alone, `J3(O)` alone, different stabilizers, different frame choices.

**Acceptance:** the proof has one theorem statement, named hypotheses, and no phrase equivalent to "choose the trace space". The audit must show all nearby alternatives fail by a stated symmetry/action criterion.

**Kill/demotion condition:** if the measure cannot be derived, keep `epsilon0^2 = pi/432` as `GEOMETRIC` or demote it to `CHOSEN` in `model_complexity.py`, and let `scoreboard.py` report the resulting Bayes factor.

## Phase 3 - Build The One Yukawa/Seesaw Operator

**Goal:** replace separate flavour scaffolds with one diagonalized operator.

**Deliverable:** `foundations/09_yukawa_operator_theorem.md` plus `compute/yukawa_operator_full.py`.

**Required output from one construction:**

1. Charged-sector mass matrices for up, down, and charged leptons.
2. The NNI/cascade structure, including first-generation factors `1/4`, `9/4`, and `1/(4pi)`.
3. CKM magnitudes `|V_us|`, `|V_cb|`, `|V_ub|` and the Jarlskog invariant from the same matrices.
4. Neutrino Dirac/Majorana structure, PMNS deviations from TBM, and mass-splitting ratio.
5. A clear statement of which parameters are fixed, which are signs/phases, and which remain chosen.

**Implementation plan:**

1. Start from `CHO_OPERATOR.md`, but make it executable as a single object rather than a tuple of targets.
2. Define the allowed operator basis from the physics map in Phase 1.
3. Force projectors from the action/representation category rather than selecting them by sector.
4. Diagonalize once and compare all mass/mixing observables.
5. Add a deformation/null test: show that removing one claimed algebraic ingredient breaks several outputs at once.

**Acceptance:** one script produces the mass eigenvalues, CKM, PMNS, and phases from one operator definition, with a printed parameter ledger. It must preserve the good CKM Jarlskog result while also giving corrected magnitudes.

**Kill/demotion condition:** if CKM magnitudes and Jarlskog cannot coexist in one operator, downgrade C4 and any dependent CKM claims to open bridge. If PMNS still requires target-angle insertion, keep N2-N5 as scaffolded/count-level rather than matrix-derived.

## Phase 4 - Continuum And RG Matching

**Goal:** stop hiding continuum physics in residual terms.

**Deliverables:** `foundations/10_continuum_rg.md`, `compute/rg_matching_audit.py`, and updates to `derived_vs_residual.py`.

**Tasks:**

1. State the CHO matching scale or prove how it is selected.
2. Run standard one-loop and, where needed, two-loop SM RG from that scale to low energy.
3. Include threshold conventions for heavy quarks, electroweak symmetry breaking, and neutrino seesaw scale.
4. Recompute `alpha`, `sin^2(theta_W)`, `M_W`, Higgs quartic, and relevant Yukawas using the same scheme.
5. Separate `derived boundary condition`, `standard RG running`, and `threshold input` in all output tables.

**Acceptance:** the script reproduces the current residual corrections without inverse-running from the observed target. The matching scale and thresholds are declared before comparison.

**Kill/demotion condition:** if the matching scale is chosen to hit the data, mark S4/S5 as phenomenological fits. If the derived boundary conditions miss by more than the stated theory floor after standard RG, report that as the real error.

## Phase 5 - Gravity Gate

**Goal:** decide whether gravity is part of the theory or an interesting side project.

**Deliverable:** `foundations/11_gravity_gate.md` plus, only if viable, `compute/gravity_lorentz_reduction.py`.

**Tasks:**

1. Try to reduce the internal `Im(O)` `G2 < SO(7)` metric to a 4D Lorentzian metric without inserting a spacetime subspace by hand.
2. Join the `C x H = M2(C)` Minkowski arena to the octonionic associator metric.
3. Identify a candidate field equation or variational principle that yields an Einstein-like equation and a Newton constant.
4. Check a flat limit and at least one weak-field/Newtonian scaling limit.

**Acceptance:** a 4D Lorentzian metric, transformation law under `SO(3,1)`, a flat limit, and a candidate dynamics appear in one coherent construction.

**Kill/demotion condition:** if the 4D Lorentzian reduction requires a hand-picked four-plane or no dynamics emerges, keep gravity explicitly out of scope and remove any ToE framing from public-facing docs.

**Phase 5 execution note (2026-06-07):** `compute/gravity_gate_audit.py` and
`foundations/11_gravity_gate.md` trigger the demotion condition. The internal
`G2` metric remains a useful kinematic brick, but no canonical invariant
four-plane, Lorentzian signature, or Einstein/Newton dynamics emerge. Gravity is
therefore out of scope for the present framework and kept as a separate
exploratory line.

## Phase 6 - Prediction Discipline

**Goal:** make future tests harder to retune and easier to interpret.

**Target files:** `FUTURE_TESTS.md`, `compute/prediction_registry.py`, `compute/forward_predictions.py`, `compute/predict_neutrino_sum.py`.

**Tasks:**

1. Keep positive quantitative predictions separate from null exclusions.
2. For each prediction, record the exact formula, frozen inputs, date, hash, experimental channel, and kill condition.
3. Add update protocol: new data create a dated addendum; old predictions are never overwritten.
4. Prioritize the strongest tests: neutrino ordering/sum, `theta23` octant, `0nu beta beta`, Higgs self-coupling, and the existing `m_nu3` floor tension.

**Acceptance:** prediction hashes change only when a new dated registry entry is intentionally added.

**Kill/demotion condition:** if a future target depends on an unfixed bridge that can move after data arrive, do not call it a prediction; call it a bridge sensitivity.

**Phase 6 execution note (2026-06-07):** `compute/prediction_registry.py`
is now a locked manifest gate. Positive quantitative predictions (`Sigma m_nu`,
`theta23` octant, `m_betabeta`) are separated from bridge sensitivities
(`m_nu3` floor tension and `kappa_lambda` matching-level target), and null
exclusions remain in `FUTURE_TESTS.md`. The registry records formula, frozen
inputs, channel, kill condition, date, and SHA-256 value digest for each entry;
the manifest digest is locked so silent retunes fail the audit.

## Phase 7 - Paper Rewrite Strategy

**Goal:** make the publishable unit smaller, sharper, and more defensible.

**Paper 1 should become:** a rigorous algebraic paper on the state map, generation idempotents, charge/chirality, and anomaly cancellation. Do not lead with masses.

**Paper 2 should become:** the epsilon and Yukawa operator paper, but only after Phases 2 and 3 have real theorems or honest demotions.

**Paper 3 should become:** either a modest cosmological-constant bridge note or be deferred until continuum/RG/free-energy factorization is stronger.

**Gravity should be:** a separate exploratory note unless Phase 5 passes.

**Acceptance:** each paper has one theorem-level core and a separate section titled "Open Bridges". The abstract does not claim more than the ledger status.

**Phase 7 execution note (2026-06-07):** generated paper artifacts, arXiv
submission notes, and old LaTeX paper drafts have been removed. The project is
now code/markdown first. Future papers should be rebuilt from the ledger,
foundation notes, and audit outputs when a small theorem-level unit is ready.

## Phase 8 - Theory Validation Harness

**Goal:** make the validation suite enforce scientific claim status, not just
script execution.

**Deliverable:** `compute/audit_contract.py` plus semantic tests in
`tests/test_audit_validation.py`.

**Minimum contract for each audit artifact:**

1. Ledger IDs touched by the artifact.
2. Current status: theorem, derived bridge, open bridge, future test,
   diagnostic, locked registry, exploratory, or out of scope.
3. Public-claim policy: what can and cannot be said from this artifact.
4. Remaining open bridges and kill conditions where the claim is not closed.
5. Prediction-registry linkage for future-facing claims.

**Acceptance:** every `compute/audit.py` artifact has exactly one structured
contract; the locked prediction registry matches the contract; the tests fail if
`epsilon0^2 = pi/432`, the one-operator flavour gate, or gravity scope silently
change status without a deliberate contract update.

**Kill/demotion condition:** if an artifact cannot be assigned a clear contract,
it is not mature enough to carry a public claim.

**Phase 8 execution note (2026-06-07):** `compute/audit_contract.py` now covers
all 37 registered audit artifacts. The unittest harness enforces contract
coverage, locked-prediction alignment, the open F0 epsilon hinge, the open
one-operator Yukawa gate, and the gravity out-of-scope demotion.

## Suggested Execution Order

```text
Week 1      Phase 0: claim hygiene and stale gap-doc refresh
Weeks 1-3   Phase 1: physics map + anomaly/content audit
Weeks 3-6   Phase 2: epsilon measure theorem attempt
Weeks 4-8   Phase 3: one Yukawa/seesaw operator
Weeks 7-10  Phase 4: continuum/RG matching
Weeks 9-12  Phase 5: gravity gate, only after SM map is stable
Ongoing     Phase 6: prediction registry discipline
After pass  Phase 7: paper rewrite
Ongoing     Phase 8: theory-validation contract harness
```

## Project-Level Definition Of Done

The repair phase succeeds if all of the following are true:

1. A reviewer can trace every public claim to a ledger status.
2. The SM state/content map is explicit and anomaly-clean.
3. `epsilon0^2 = pi/432` is either theorem-level or honestly charged as an input.
4. One operator, not several target matrices, produces the flavour observables.
5. Continuum/RG residuals are computed from stated boundary conditions.
6. Gravity is either a real 4D Lorentzian/dynamical construction or explicitly out of scope.
7. The Bayes scoreboard remains visible and moves only when derivation statuses change.
8. The test harness fails when audit artifacts drift away from their ledger-backed contracts.

This is the path from "beautiful and suggestive" to "hard to dismiss." The point is not to protect every current claim. The point is to make the surviving claims sturdy.