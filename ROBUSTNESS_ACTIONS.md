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

**Execution note (2026-06-07):** `compute/audit_contract.py --json` now exports
machine-readable contracts; `compute/claim_status_report.py` groups artifacts by
status; tests verify ledger-ID coverage and kill-condition discipline for open
and exploratory contracts.

## Action Track B - Put `epsilon0^2 = pi/432` On Trial

**Goal:** close or demote the F0 hinge.

**Next actions:**

1. Isolate the remaining H4 measure hypothesis from `foundations/08_epsilon_measure_theorem.md` into a minimal mathematical statement.
2. Add a new witness script for the normalized invariant measure, separate from the existing nearby-alternative audit.
3. Test whether the transition measure is forced by the CHO action, the rank-one kernel, and the Spin(9)/two-level symmetry together.
4. If the measure still requires choosing the trace space by hand, demote F0 in the ledger and update `model_complexity.py` / `scoreboard.py`.

**Acceptance:** F0 is either promoted with a named theorem and machine witness, or honestly charged as an input in the Bayes accounting.

**Execution note (2026-06-07):** `compute/epsilon_measure_witness.py` is now a
first-class audit artifact. It isolates H4, the invariant normalized-measure
rule, as the remaining F0 seam and keeps theorem status open.

## Action Track C - Collapse Flavour Into One Operator

**Goal:** replace target-specific flavour scaffolds with one diagonalized CHO operator.

**Next actions:**

1. Extract the allowed operator basis from the physics-map and chiral-projector artifacts.
2. Make `compute/yukawa_operator_full.py` output a structured parameter ledger: fixed, sign/phase, bridge, and chosen.
3. Add a deformation/null test showing which outputs fail together when a claimed algebraic ingredient is removed.
4. Force the CKM magnitudes and Jarlskog invariant through the same charged-sector diagonalization.
5. Force the PMNS perturbation through the same seesaw structure, or demote the PMNS matrix claims to scaffold.

**Acceptance:** one operator produces charged masses, CKM, PMNS, and phase diagnostics, or the dependent claims are demoted in the contract and ledger.

**Execution note (2026-06-07):** `compute/yukawa_operator_full.py` now prints a
categorized parameter ledger and deformation/null tests showing which outputs
fail together when epsilon, Fano phase, sector projectors, or PMNS perturbations
are removed.

## Action Track D - Derive Or Demote Continuum Matching

**Goal:** stop treating RG and threshold corrections as residual bookkeeping.

**Next actions:**

1. Split `compute/rg_matching_audit.py` into boundary-condition, running, and threshold sections with structured outputs.
2. Add explicit tests that inverse-matched scales are labelled as inverse-matched, never derived.
3. Try one concrete CHO matching-scale proposal from the action; compare it against `alpha`, `sin^2(theta_W)`, `M_W`, and Higgs/quartic targets.
4. If no scale is selected by the action, keep S4/S5 phenomenological and remove any stronger public wording.

**Acceptance:** low-energy residuals are computed from declared boundary conditions and thresholds, not inferred from observed targets.

**Execution note (2026-06-07):** `compute/rg_matching_audit.py` exposes a
structured matching report and the tests enforce that inverse-matched scales are
not labelled as derived.

## Action Track E - Finish The Content Map

**Goal:** make the state map functorial enough to support operator work.

**Next actions:**

1. Extend `compute/physics_map_audit.py` from one-generation anomaly bookkeeping to the three idempotent-frame copies.
2. State the exact functor from frame idempotents / `T(OP2)` tangent spinors to SM field labels.
3. Add tests that the map does not use per-field arbitrary choices.
4. Feed the resulting state basis into the allowed Yukawa-operator domain.

**Acceptance:** the project can say exactly what object carries three generations before asking it to carry masses.

**Execution note (2026-06-07):** `compute/physics_map_audit.py` now prints the
three idempotent-frame copies of the one-generation table and tests that the
current extension uses no per-field arbitrary choices while keeping the functorial
content map open.

## Action Track F - Keep Predictions Frozen And Readable

**Goal:** make future data comparisons hard to retune.

**Next actions:**

1. Add a generated markdown summary from `compute/prediction_registry.py` into `FUTURE_TESTS.md` or a companion report.
2. Add dated addendum support before the first real update is needed.
3. Separate discovery pressure, null exclusions, and bridge sensitivities in the public docs.

**Acceptance:** a future measurement can be compared against a frozen entry without interpreting prose or rerunning old code by hand.

**Execution note (2026-06-07):** `compute/prediction_registry.py --markdown`
generates a markdown summary from the locked registry rows, and `FUTURE_TESTS.md`
points to that generated export path.

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

## Gold-Standard Roadmap (added 2026-06-08)

Honest strategic review of what separates the current framework from gold-standard
(testable, defensible, publishable) physics. This supersedes nothing above; it
re-prioritises Tracks B–E under one diagnosis.

### The one-number state (live `compute/scoreboard.py`)

- `ln B = -3.2` crediting only closed theorems — the O(1)-numerology null still
  wins.
- `ln B = +5.6` if `eps0^2 = pi/432` is granted as geometric. The sign flip rests
  on the single F0 claim, and is fragile (at prior width F=2 it is only `+1.6`).
- The CHOSEN tier is **44.1 bits** of unpaid Occam cost; of that the three hand-
  picked integer exponents `3^36` (M_W), `3^9` (M_R), `3^64 + 11/12` (Lambda) are
  **21.8 bits** — nearly half, the CC exponent alone 13.3 bits.

### The diagnosis — the soft spot is the *kind* of math, not its rigor

The classical representation theory (J3(O), F4/Spin(9), E6, triality, KO-dim 6) is
solid and largely inherited from the literature (Furey, Todorov–Dubois-Violette,
Baez–Huerta). Three specific things are soft:

1. **Invariance arguments are substituted for dynamics.** Every F0 module has the
   shape "assume the symmetry is G, then Schur/the orbit method/majorisation forces
   the measure / ray / product." What forces G to be the *physical* symmetry is the
   action — and `foundations/02_action.md` is a *candidate*, not a derivation. Gold-
   standard is Lagrangian → equations of motion → vacuum → spectrum, with the numbers
   as OUTPUTS. There are now ~25 `epsilon_*`/`f0_*` witnesses and the scoreboard still
   reads "GEOMETRIC, seam open": **more invariance witnesses will not move `ln B`.**
2. **The exponents `3^36 / 3^9 / 3^64` are unforced numerology** (21.8 bits) — the
   most vulnerable and most expensive part.
3. **No single operator.** Masses, CKM, PMNS are separate bridges;
   `spectral_action.py` shows one generation forces NO mass ratio, so the hierarchy
   must live in a cross-generation operator that has not been built.

### Gold-standard scorecard (where the gap is, by criterion)

Grading CHO against what "gold-standard physics" (Standard Model / GR class) demands:

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Dynamical principle (action -> EoM -> vacuum -> spectrum) | ABSENT | `02_action.md` is a candidate; ~24 of 68 artifacts are F0 invariance/normalisation witnesses, scoreboard still "GEOMETRIC, seam open" |
| 2 | Parameters derived not fitted | PARTIAL | 7 DERIVED (31.2 bits) vs 9 CHOSEN (44.1 bits); the 3 exponents alone are 21.8 bits |
| 3 | One unifying object | ABSENT | masses / CKM / PMNS are separate bridges; no single diagonalised operator |
| 4 | Confirmed pre-registered prediction | PENDING | `sin^2 th23 = 4/7` frozen but unmeasured; all else postdiction |
| 5 | Mathematical rigour (theorems) | PARTIAL | exactly 1 THEOREM-status artifact (`ladder_charges`, inherited); 23 OPEN_BRIDGE; genuine new theorems exist (idempotent `N_gen=3`, Schur `1/16` & `1/27`, Freudenthal seesaw) but the headline numbers ride bridges |
| 6 | Continuum / UV control | FALSIFIED (single scale) | `rg_scale_derivation.py`: two EW boundaries over-determine the matching scale by ~1.8e4 (12 GeV vs 2e5 GeV); gravity gated out |
| 7 | Independent reproduction / acceptance | ABSENT | self-published; MDL `R~1.19` marginal; `ln B` favours the numerology null |

The whole gap reduces to one number: `ln B = -3.2` (closed-theorem floor, null wins)
-> `+5.6` (if `pi/432` is GRANTED geometric) -> `+36.2` (program complete). Today the
`+5.6` is granted, not earned.

### The closing roadmap — one make-or-break build, then conditional follow-on

Criteria 1, 2, 3 and half of 6 are NOT four independent jobs: they are all
properties of a finite spectral triple `(A, H, D)` and its spectral action
`Tr f(D/Lambda)`. So the roadmap is ONE gated build, not five parallel tracks.

**PHASE 1 - THE GATE: finite spectral triple + spectral action (make-or-break).**
- 1.1 Assemble `(A, H, D)` explicitly. `A = C(x)H(x)O`; `H` = the physical fermion
  module (3 generations as the J3(O) frame idempotents, 16 Weyl each, antiparticles
  via the real structure `J`); `D = D_free (+) gamma5 (x) Y`, with `Y` the
  cross-generation finite Dirac from the Jordan/Freudenthal structure (reuse
  `spectral_action_432.py` `L_X`, `ko_dimension_chirality.py` `gamma`/`J`).
  ACCEPTANCE: the NCG axioms verify numerically (`D` self-adjoint; KO-dim 6 signs
  `(+,+,-)`, already in hand; order-zero and order-one conditions; non-degenerate
  intersection form). KILL: an axiom fails irreparably -> the 432 space is not a
  consistent geometry -> withdraw the geometric `pi/432` reading, `ln B` holds at
  `-3.2`, ship the standalone math + honest null.
- 1.2 Heat-kernel expansion `a0 Lambda^4 + a2 Lambda^2 + a4 + ...`; the coefficients
  are closed traces of `Y` (`Tr(Y^dag Y)`, `Tr((Y^dag Y)^2)`).
- 1.3 DECISIVE EXPERIMENT: is `pi/432` one of those coefficients? The measure space
  is `16x27=432`; test whether the normalised `a4/a2` (or the finite-spectrum moment)
  equals `pi/432` from the geometry. ACCEPTANCE: yes -> F0 CLOSES dynamically, the
  `+5.6` becomes EARNED, `eps0` moves DERIVED on the scoreboard, criterion 1 met.
  KILL: a different number -> F0 is not a spectral-action output, withdraw the credit,
  `ln B` headline stays `-3.2`.
- 1.4 Does the finite spectrum of `Y` reproduce the hierarchy as eigenvalue ratios?
  (Seeds Phase 2.)

**PHASE 2 - conditional on Phase 1: one object -> spectrum.**
- Tier 3: diagonalise the SAME `Y` for charged masses + CKM, its seesaw partner for
  PMNS. ACCEPTANCE: one diagonalisation gives masses + CKM + PMNS within stated error
  -> criterion 3 met, ~5 DERIVED_BRIDGEs collapse into one.
- Tier 2: the exponents `3^36 / 3^9 / 3^64` as RG running of the spectral-action
  couplings from a DERIVED unification scale `Lambda` (Connes-Chamseddine unifies all
  couplings at `Lambda`; the powers of 3 should be `ln(Lambda/M_Z)` e-foldings, not
  chosen integers). ACCEPTANCE: they come out -> 21.8 bits move CHOSEN -> DERIVED,
  `ln B` climbs toward `+36`. KILL: they do not -> relabel them explicit inputs and
  shrink the headline.

**PHASE 3 - continuum/UV consistency (Tier 4).** Resolve the over-determination
(12 GeV vs 2e5 GeV): the two EW boundaries must become ONE unification-scale
condition of the spectral action (the analogue of Connes' `sin^2 th_W = 3/8` at
`Lambda`), running down to both. ACCEPTANCE: one `Lambda` reproduces both. BONUS: the
`a2` coefficient IS Einstein-Hilbert, so doing Phase 1 properly produces a gravity
sector for free (the Lorentzian-signature 4D reduction stays open).

**PHASE 4 - external clock (parallel; no theory work closes it).** Tier 5: the
`sin^2 th23 = 4/7` upper-octant bet is frozen; DUNE / Hyper-K resolves it. Upper
octant confirmed = first gold-standard datum; lower octant = kill.

**THE FORK.** Phase 1 is binary. Succeed -> CHO graduates from organised postdictions
to a candidate spectral-action theory and the Bayes sign flips on EARNED credit.
Fail -> the gold-standard route is closed; ship the standalone math
(`PAPER_JORDAN_THEOREMS.md`, done) + the honest null, and stop the invariance-witness
treadmill (24 F0 modules is already well past diminishing returns).

### Execution note (2026-06-08)

`compute/f0_vacuum_majorization.py` added: it does not add another invariance
witness but strengthens the F0 *vacuum* selection to a functional-independent
majorisation statement (rank-one ray = majorisation-maximal state, selected by the
whole Schur-concave/convex class including the Connes spectral-action purity term),
and bridges the F0 program to the spectral-action framework that Tier 1 requires.
It is a robustness increment, NOT a closure: F0 stays GEOMETRIC, no Bayes credit
moves. The next substantive step is Tier 1 proper — constructing `D` on the 432
space and computing its spectral action — which is large and should be built on the
verified `spectral_action.py` / `ko_dimension_chirality.py` constructions rather
than as another normalized-trace witness.

### Execution note (2026-06-09) — Phase 1.1 attempted

`compute/f0_spectral_triple_gate.py` added: the first explicit ASSEMBLY of the
finite triple `(A, H, D; J, gamma)` on the 432 space called for by Phase 1.1, with
an honest Connes-axiom ledger that reports the failures as loudly as the passes. It
reuses `ko_dimension_chirality.py` (the `gamma`/`J` real structure), the octonion
left-multiplications of `spectral_action.py`, and the Jordan `L_X` of
`spectral_action_432.py`. RESULT — half passes, two NAMED obstructions:
- **PASS:** the `C^8` octonion spin brick is a consistent KO-dimension-6 chirality
  module (`gamma8^2 = I` Hermitian; `J8 = conj` gives `(eps, eps'') = (+1, -1)`), and
  the product `H = C^8 (x) C^54` (`dim_C = 432`) carries a self-adjoint
  `D = gamma8 (x) D_F` with `gamma^2 = J^2 = I` and `gamma D = -D gamma`. The
  metric / real-structure half of the triple is sound.
- **OBSTRUCTION 1 (order-zero = the octonion associator):** `[[D, a], b] = 0`
  literally evaluates the associator of `A = C(x)H(x)O`. It FAILS on the full module
  (residual `~16`; restricting only the algebra to `H` still fails, `~12`) and is
  recovered to machine precision (`~1e-15`) ONLY on a genuine associative BIMODULE or
  the complex line. Order-one fails likewise (`~26`). Non-associativity is the
  structural obstruction; the fix is to rebuild `A` as its associative / special-Jordan
  envelope.
- **OBSTRUCTION 2 (Yukawa doubling → KO-dim 4):** the Jordan Yukawa `L_X` is
  chirality-EVEN, so realising it as a Dirac requires particle/antiparticle doubling,
  which sends the product KO-dimension `6 (x) 6 -> 4 (mod 8)`, not the 6 a single chiral
  generation needs. The fix is to carry the Yukawa in the real structure `J`, not as an
  even operator.

Neither obstruction is the irreparable KILL (which would withdraw the geometric
`pi/432` reading and hold `ln B` at `-3.2`); both are known and repairable, and
together they LOCALISE the Phase-1.2 prerequisite to: **build the spectral action on
the associative / special-Jordan envelope of `A`, with the Yukawa embedded in the real
structure `J`.** The naive `(A, H, D)` is NOT yet a consistent triple, so the
heat-kernel `a4/a2` test of Phase 1.3 (the decisive `pi/432` experiment) is NOT yet
reachable. F0 stays GEOMETRIC/open, no Bayes credit moves, the scoreboard ladder
(`-21.3 / -3.2 / +5.6 / +36.2`) and the frozen registry manifest are untouched. Wired
into `audit.py` and `audit_contract.py` (69/69 contracted, status PASS) as an
`OPEN_BRIDGE` under F0.

### Execution note (2026-06-09) — Phase 1.2 prerequisite sharpened

`compute/f0_real_structure_gate.py` added: it closes a hidden inconsistency in the
Phase-1.1 gate (which checked the KO-dim-6 signs with `J = ` complex conjugation but
checked order-zero against actual right-multiplication — two DIFFERENT real
structures, whereas a triple has only ONE `J` for which EVERY axiom must hold). Testing
both axioms against each candidate `J` on the octonion brick `C^8` turns
Obstruction 1 into a precise DICHOTOMY plus its standard resolution — all computed, none
hand-set:
- **`J = ` complex conjugation (the KO-6 choice, `B = I`):** the opposite algebra
  `J L_a J^-1 = conj(L_a) = L_a` EQUALS `A`, so order-zero `[A, A^o] = [A, A] = 0`
  FORCES `A` COMMUTATIVE. The quaternion left-algebra `L(H)` fails order-zero (`~14`);
  only the abelian complex line `L(C)` holds (`~1e-16`). With the KO-6 real structure
  the largest order-zero-compatible algebra on one brick is ABELIAN — no `SU(2)`, no
  `SU(3)`.
- **`J = ` octonion conjugation (`kappa . conj`, `B = diag(1,-1,...,-1)`):** here
  `J L_a J^-1 = -R_a` (genuine right multiplication; the identity `KAPPA L_i KAPPA = -R_i`
  is exact to `0`), so order-zero becomes the associator — it holds on the quaternion
  BIMODULE (`~1e-15`) and ALLOWS a noncommutative `A`. BUT this `J` destroys the
  grading: `J gamma J^-1 = -0.5 gamma` is not `+/- gamma` (residual `2.0`), so the
  KO-dimension is UNDEFINED — chirality is lost.
- **DICHOTOMY:** on a single irreducible octonion brick NO real structure `J` gives
  BOTH KO-dimension 6 AND a noncommutative order-zero algebra. The two requirements pull
  `J` in incompatible directions (conjugation vs octonion-conjugation). This is the
  SHARP form of the Phase-1.1 order-zero obstruction.
- **RESOLUTION (standard Connes route, computed):** stop forcing the octonions to BE the
  order-zero algebra. A nonabelian `A = H` acting on `A (x) A^o` satisfies order-zero
  EXACTLY (`0`) by left-right commutation (left and right multiplication on a matrix
  algebra commute regardless of how noncommutative `A` is) while staying genuinely
  nonabelian (`||[i, j]|| = 2`). The octonions then GRADE the module (they supply
  `gamma8` and the charges), they do NOT supply the order-zero `*`-algebra — exactly how
  Connes' Standard Model evades the associator. This points to the concrete rebuild
  `A = C (+) H (+) M_3(C)` on `A (x) A^o`.

This neither closes nor advances F0's Bayes credit: it converts the Phase-1.1
order-zero FAIL into a precise statement and names the rebuild it demands. Two open
bridges remain before a spectral action can be written — (i) carry out that associative
rebuild as a genuine product triple that RESTORES KO-dim 6, and (ii) embed the
chirality-even Jordan Yukawa in the real-structure (Majorana) sector so the finite
KO-dimension does not drop from 6 to 4 (Obstruction 2, still open). Until both are done
`eps0^2 = pi/432` stays GEOMETRIC and open; nothing here promotes it. The scoreboard
ladder (`-21.3 / -3.2 / +5.6 / +36.2`) and the frozen registry manifest are untouched.
Wired into `audit.py` and `audit_contract.py` (70/70 contracted, status PASS; pytest
89 passed) as an `OPEN_BRIDGE` under F0.

### Execution note (2026-06-09) — Phase 1.2 PROPER: associative rebuild carried out

`compute/f0_associative_triple_gate.py` added: it CARRIES OUT the associative rebuild
that the prerequisite only named, for the one-generation LEPTON sector, and closes both
of the open bridges it had left. The question going in was genuinely open — a fresh
CHO-specific obstruction (e.g. KO-6 together with order-one forcing `D = 0`) would have
been an equally valid and equally reportable outcome. It did not occur. The finite
geometry is `H = C^8` (basis `[nuR, eR, nuL, eL | ` antiparticles`]`), `A = C (+) H`
acting on the left, `J = (`particle`<->`antiparticle swap`) . conj`, `gamma = ` chirality
flipped on antiparticles. All numbers come out of explicit `8x8` / `6x6` / `9x9`
matrices, none are hand-set:
- **(A) Order-zero RESTORED for a noncommutative algebra.** `[a_L, b_R] = 0` holds
  EXACTLY on `A (x) A^o` for the genuinely nonabelian summands `H` (`~9e-16`,
  `||[x,y]|| = 14.7`) and `M_3(C)` (`~2e-15`, `||[x,y]|| = 15.3`), and for the actual SM
  lepton rep (`~9e-16`). The colour `M_3(C)` factor commutes with the lepton sector by
  construction (left-right multiplication on a matrix algebra commute) — generalising the
  prerequisite's `H`-toy resolution to all three summands.
- **(B) KO-dimension 6 RESTORED.** `J^2 = +I` (`eps = +1`) and `J gamma J^-1 = -gamma`
  (`eps'' = -1`) give KO-dim 6 — chirality WITHOUT Connes-doubling. This is exactly the
  grading the prerequisite's `J = kappa.conj` had destroyed; the associative route
  recovers it because `gamma` now lives on the module, not on the octonions.
- **(C) A NONZERO physical Dirac satisfies order-one.** The explicit Dirac with Dirac
  Yukawas (`nuR<->nuL`, `eR<->eL`) AND a Majorana mass (`nuR<->nuRbar`) is Hermitian,
  `gamma`-ODD, `J`-REAL (`J D J^-1 = D`) and satisfies order-one `[[D, a], b^o] = 0`
  (`~9e-16`). So the seesaw lives in the real-structure (Majorana) sector and the finite
  KO-dimension stays 6, not 4 — closing the second bridge (the Yukawa real-structure
  embedding) the prerequisite left open.

The associative SKELETON EXISTS: a consistent KO-dim-6 finite real spectral triple of
Standard-Model type, with a nonzero Yukawa+Majorana Dirac, for a SINGLE real structure
`J`. The Phase-1.1 "the triple does not exist" verdict is REPAIRED at the level of the
associative skeleton. HONEST CAVEAT: this is the KNOWN Connes-Chamseddine-Marcolli
skeleton recovered constructively — the complement to the no-go, NOT new physics — and it
moves NO Bayes credit. Two CHO-specific bridges remain before `eps0^2 = pi/432` could be
promoted: step C (replace the generic Yukawa by the SPECIFIC octonionic Jordan mass
operator `L_X` and realise the full `432 = 16 (A_Weyl) x 27 (J3(O))` module — only the
8-dim colour-singlet lepton slice is built here; the quark colour sector and three
generations are not yet built), and Phase 1.3 (show `eps0^2 = pi/432` emerges as the
spectral-action ratio `a4/a2` — `epsilon_heat_kernel` already warns the spectral `pi`
enters only via the Gaussian `(4 pi)^(-d/2)`, so a bare `pi` numerator is unlikely from
this route). Until both are done F0 stays GEOMETRIC/open; nothing here promotes it. The
scoreboard ladder (`-21.3 / -3.2 / +5.6 / +36.2`) and the frozen registry manifest are
untouched. Wired into `audit.py` and `audit_contract.py` (71/71 contracted, status PASS;
pytest 90 passed) as an `OPEN_BRIDGE` under F0.

### Execution note (2026-06-09) — Phase 1.2 step C: octonionic Yukawa `L_X`

`compute/f0_octonionic_yukawa_gate.py` added: it takes the step-B KO-6 skeleton (which
used a GENERIC Yukawa) and asks the sharp CHO question — does the SPECIFIC octonionic
Jordan mass operator `L_X` slot into that triple, and if so do the spectral-triple axioms
FORCE its averaging-law texture or merely admit it? The honest answer was reported
whichever way the numerics fell; they fell two-sided. The faithful finite geometry is
`H = C^8 (x) C^27` — the step-B lepton charge factor tensored with the `J3(O)` flavour
`27` — with the Yukawa `K_Yuk (x) L_X`: the charge `L<->R` coupling `K_Yuk` is `gamma1`-ODD
and `L_X` is the UNGRADED octonionic generation matrix (`gamma = gamma1 (x) I27`,
`J = J1 (x) conj`). All numbers come from explicit `8x8` / `27x27` / `216x216` matrices:
- **(A) `L_X` IS the octonionic averaging-law operator.** Its spectrum is exactly the
  Jordan averaging law — three singlets `{1, 0.6, 0.3}` (mult 1) and three octets
  `{0.8, 0.65, 0.45}` (mult 8), 27 eigenvalues total — and it is self-adjoint to `0`.
- **(B) The second Phase-1.1 obstruction is DISSOLVED — `L_X` needs NO doubling.** Because
  chirality lives in the charge factor (`gamma = gamma1 (x) I27`), the ungraded `L_X`
  enters as a pure generation multiplier and the product Dirac
  `D = K_Yuk (x) L_X + K_Maj (x) M_maj` is self-adjoint, `gamma`-ODD, `J`-REAL, with KO
  signs `eps = +1`, `eps'' = -1` -> KO-dim 6, and order-zero (`~9e-16`) AND order-one
  (`~9e-16`) BOTH holding for the genuine octonionic `D`. The Phase-1.1 "`L_X`
  chirality-even -> Connes-doubling -> `6 (x) 6 -> 4` KO collapse" is gone.
- **(C) DECISIVE — the axioms do NOT force the Yukawa.** Order-one factors through the
  charge sector: each charge coupling tensored with a RANDOM Hermitian flavour operator
  still satisfies order-one (`K_Yuk (x) random ~7e-15`, `K_Maj (x) random = 0`). So the
  gauge algebra sees the flavour factor as pure multiplicity and ANY self-adjoint flavour
  operator passes — the octonionic `L_X` is ADMISSIBLE but NOT FORCED.

TWO-SIDED VERDICT. POSITIVE: the octonionic `L_X` lives in a consistent KO-6 triple,
ungraded and undoubled, carrying its averaging-law masses into `D`'s spectrum — the second
Phase-1.1 obstruction is closed. SOBERING: the triple axioms (order-zero/one, KO-6) are
NECESSARY but not SUFFICIENT — they do not pin the Yukawa, so the CHO mass texture is NOT
secured by the triple's existence; it must instead be SELECTED by the spectral ACTION
`Tr f(D/Lambda)` (Phase 1.3). `epsilon_heat_kernel` already warns the spectral `pi` enters
only via the Gaussian `(4 pi)^(-d/2)`, so Phase 1.3 is more likely to REFUTE than confirm
`eps0^2 = pi/432` as `a4/a2`. F0 stays GEOMETRIC/open; the scoreboard ladder
(`-21.3 / -3.2 / +5.6 / +36.2`) and frozen registry manifest are untouched. Wired into
`audit.py` and `audit_contract.py` (72/72 contracted, status PASS; pytest 91 passed) as an
`OPEN_BRIDGE` under F0.