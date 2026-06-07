# Robustness Actions

Created: 2026-06-07

Purpose: define the next research actions after the repair gates were implemented. The old phase plan has done its job: the project now has claim hygiene, audit gates, a locked prediction registry, no stale paper artifacts, and a semantic validation contract. This document is the live action plan for making the surviving claims harder to dismiss.

## Current Baseline

The project is now code and markdown first. The authoritative spine is:

1. `DERIVATION_LEDGER.md` for claim status.
2. `compute/audit.py` for executable artifacts.
3. `compute/audit_contract.py` for machine-readable claim contracts.
4. `tests/test_audit_validation.py` for fine-grained artifact and semantic validation.
5. `FUTURE_TESTS.md` and `compute/prediction_registry.py` for frozen future-facing claims.

The main open scientific seams are no longer hidden:

- `F0`: `epsilon0^2 = pi/432` is still the Bayes-factor hinge until the invariant normalized measure is derived or demoted.
- `yukawa_operator_full`: masses, CKM, PMNS, and phases are not yet produced by one forced operator.
- `rg_matching_audit`: continuum/RG matching scales and thresholds are explicit but not derived.
- `physics_map_audit`: one generation is anomaly-clean; the functorial three-generation content map remains open.
- `gravity_gate_audit`: gravity is out of scope for the present framework.

## Operating Rules

1. **Contracts before claims.** Any claim-status change starts in `compute/audit_contract.py`, then updates `DERIVATION_LEDGER.md`, public docs, and tests.
2. **No silent promotions.** A theorem promotion requires a new or strengthened executable witness plus a ledger update.
3. **No new headline constants.** New numerical relations are not robustness work unless they close an existing open bridge or falsify one.
4. **One object beats many fits.** Prefer constructions that make several existing outputs move together over isolated postdictions.
5. **Demotion is progress.** If a bridge cannot be closed under its own kill condition, demote it and let the scoreboard absorb the cost.

## Action Track A - Make The Harness More Semantic

**Goal:** make the validation suite check theory-state drift, not just script execution.

**Next actions:**

1. Add a compact JSON export mode to `compute/audit_contract.py` so tools can inspect contracts without parsing printed tables.
2. Add a test that every ledger ID referenced by `compute/audit_contract.py` exists in `DERIVATION_LEDGER.md`.
3. Add a test that every contract marked `open_bridge` or `exploratory` has at least one explicit open bridge and kill condition.
4. Add a small `compute/claim_status_report.py` that groups artifacts by status and prints the shortest path to promotion or demotion.

**Acceptance:** a reviewer can run one command and see which claims are closed, open, future-facing, diagnostic, or out of scope.

## Action Track B - Put `epsilon0^2 = pi/432` On Trial

**Goal:** close or demote the F0 hinge.

**Next actions:**

1. Isolate the remaining H4 measure hypothesis from `foundations/08_epsilon_measure_theorem.md` into a minimal mathematical statement.
2. Add a new witness script for the normalized invariant measure, separate from the existing nearby-alternative audit.
3. Test whether the transition measure is forced by the CHO action, the rank-one kernel, and the Spin(9)/two-level symmetry together.
4. If the measure still requires choosing the trace space by hand, demote F0 in the ledger and update `model_complexity.py` / `scoreboard.py`.

**Acceptance:** F0 is either promoted with a named theorem and machine witness, or honestly charged as an input in the Bayes accounting.

## Action Track C - Collapse Flavour Into One Operator

**Goal:** replace target-specific flavour scaffolds with one diagonalized CHO operator.

**Next actions:**

1. Extract the allowed operator basis from the physics-map and chiral-projector artifacts.
2. Make `compute/yukawa_operator_full.py` output a structured parameter ledger: fixed, sign/phase, bridge, and chosen.
3. Add a deformation/null test showing which outputs fail together when a claimed algebraic ingredient is removed.
4. Force the CKM magnitudes and Jarlskog invariant through the same charged-sector diagonalization.
5. Force the PMNS perturbation through the same seesaw structure, or demote the PMNS matrix claims to scaffold.

**Acceptance:** one operator produces charged masses, CKM, PMNS, and phase diagnostics, or the dependent claims are demoted in the contract and ledger.

## Action Track D - Derive Or Demote Continuum Matching

**Goal:** stop treating RG and threshold corrections as residual bookkeeping.

**Next actions:**

1. Split `compute/rg_matching_audit.py` into boundary-condition, running, and threshold sections with structured outputs.
2. Add explicit tests that inverse-matched scales are labelled as inverse-matched, never derived.
3. Try one concrete CHO matching-scale proposal from the action; compare it against `alpha`, `sin^2(theta_W)`, `M_W`, and Higgs/quartic targets.
4. If no scale is selected by the action, keep S4/S5 phenomenological and remove any stronger public wording.

**Acceptance:** low-energy residuals are computed from declared boundary conditions and thresholds, not inferred from observed targets.

## Action Track E - Finish The Content Map

**Goal:** make the state map functorial enough to support operator work.

**Next actions:**

1. Extend `compute/physics_map_audit.py` from one-generation anomaly bookkeeping to the three idempotent-frame copies.
2. State the exact functor from frame idempotents / `T(OP2)` tangent spinors to SM field labels.
3. Add tests that the map does not use per-field arbitrary choices.
4. Feed the resulting state basis into the allowed Yukawa-operator domain.

**Acceptance:** the project can say exactly what object carries three generations before asking it to carry masses.

## Action Track F - Keep Predictions Frozen And Readable

**Goal:** make future data comparisons hard to retune.

**Next actions:**

1. Add a generated markdown summary from `compute/prediction_registry.py` into `FUTURE_TESTS.md` or a companion report.
2. Add dated addendum support before the first real update is needed.
3. Separate discovery pressure, null exclusions, and bridge sensitivities in the public docs.

**Acceptance:** a future measurement can be compared against a frozen entry without interpreting prose or rerunning old code by hand.

## Recommended Order

```text
1. Harness semantics: JSON export, ledger-ID coverage, status report.
2. F0 epsilon measure: theorem attempt or explicit demotion.
3. One-operator flavour gate: structured parameter ledger and deformation tests.
4. Continuum/RG matching: derived scale attempt or demotion.
5. Three-generation content map: functorial basis for later operator work.
6. Prediction reporting: generated future-test summaries and addenda.
```

The immediate priority is Track A, because it makes every later physics change safer. The highest-value physics target remains Track B: the sign of the Bayes scoreboard turns on whether `pi/432` is forced.