# NEXT PHASE — the resume plan

*Written 2026-06-11, from the parked state ([STATUS.md](STATUS.md)). This is a
research plan, not a promise.*

The project is parked honestly. The Bayes scoreboard
([compute/scoreboard.py](compute/scoreboard.py)) sits at **`ln B = −3.2`** (today's
earned floor — the model is *mildly disfavoured* on closed results), and the whole
verdict hinges on one unbuilt object: an `F4`-breaking dynamical action whose flux
gives `pi/432`. This plan picks three tracks to resume, each chosen for a different
*kind* of payoff:

| Track | What it buys | Can it move the scoreboard? |
|---|---|---|
| **1 — Causal-set / discrete spacetime** | **grows the theory's scope** (gravity + cosmology in one room; live DESI data) | indirectly, and only via the `64` exponent — currently *relocates* the mystery, does not force it |
| **2 — `pi/432` rigidity/uniqueness** | **the scoreboard jump** — the only lever that flips the sign | YES: `−3.2 → +5.6` if `pi/432` is granted; a clean *negative* is still a real result |
| **3 — `sin²θ₂₃ = 4/7` external verdict** | **a verdict you don't control** — the one genuine *forward* bet | no direct Bayes, but the highest-credibility outcome possible (confirmed, not fitted) |

**Discipline carried over from the parked project (do not break):**

- The `pi/432` search stays **quarantined** in `experiments/pi432_action_search/`
  — nothing there is imported by [compute/audit.py](compute/audit.py), nothing
  there moves Bayes credit until it produces a real candidate action with explicit
  assumptions and kill conditions.
- The `θ₂₃` prediction stays **frozen** in
  [compute/prediction_registry.py](compute/prediction_registry.py) (`Q2`,
  hash-locked). New analysis cross-checks the payload read-only; it never retunes it.
- Every new probe carries **a kill condition** and an honest `EXPLORATORY /
  OPEN` verdict. Converging-negatives are recorded, never spun as positive.
- Never raise a public claim above [STATUS.md](STATUS.md). If prose drifts stronger,
  weaken the prose.

---

## The scoreboard, in one place (verified live)

| credit policy | `ln B` | verdict |
|---|---|---|
| historical (only `8/3` closed) | −21.3 | null |
| **today's closed-theorem floor** | **−3.2** | **null (mildly disfavoured)** |
| + geometric `pi/432` credited | +5.6 | CHO favoured |
| target (program complete) | +36.2 | CHO |

The sign flips **only** on the `pi/432` grant. That is why Track 2 is the lever and
Tracks 1 and 3 are scope/credibility plays, not scoreboard plays. Be honest about
which is which.

> **Progress (2026-06-11).** Track 2 step 1 and all of Track 3 are DONE — see the
> `✓ DONE` markers in the steps below. **All of it is diagnostic: the scoreboard is
> unchanged at `ln B = −3.2`.** Track 2 produced the *conditional* uniqueness result
> (not the jackpot), and Track 3 hardened the `theta23` value to an operator
> invariant while the physical `N5` map stays open. Track 1 is not started.

---

## Track 1 — Causal-set / discrete spacetime (grow the theory)

### In plain terms

Right now the framework treats spacetime as a fixed backdrop and gravity is
**out of scope**. But your dark-energy machinery already borrows *causal-set
theory*, where spacetime is a discrete web of events and dark energy comes from
**counting** those events. That same discrete web is, in principle, a theory of
gravity. So gravity and (dynamical) dark energy live in the *same room* — this is
the richest unexplored territory, and it is where the live DESI data is.

### Where it stands

- [compute/causal_set_lambda.py](compute/causal_set_lambda.py) — bridges CHO's
  `Λ¼ ~ M_P/3⁶⁴` to Sorkin's pre-data law `Λ ~ 1/√V` (V = number of spacetime
  atoms), and shows `64 ≈ log₃(V_observed)/8`. **Honest debit:** it uses the
  *observed* 4-volume as input, so it trades "why 64?" for "why is the universe this
  old/large now?" (the cosmic-coincidence problem). It *relocates* the mystery.
- [compute/everpresent_lambda_tracking.py](compute/everpresent_lambda_tracking.py)
  — takes the *everpresent* reading seriously: `Λ(t) ~ H(t)²`, so dark energy
  *tracks* the critical density and the two readings (static `w = −1` vs.
  fluctuating) diverge in the past by `E(z)²` (~70× at z=5). **Honest debit:** CHO
  is a *spectator* — it sets only today's normalization; the time-dynamics is pure
  causal-set content, and a smooth `Λ ~ H²` is degenerate with a rescaled Newton
  constant. The real dark-energy content is in the **sign fluctuations**, which the
  module does *not* simulate.

### Concrete steps

1. **Simulate the fluctuations, not the heuristic.** Build
   `compute/everpresent_lambda_stochastic.py` implementing the actual stochastic
   everpresent-Λ model (Ahmed–Dodelson–Greene–Sorkin 2004; Zwane–Afshordi–Sorkin
   2018) — the Λ *sign* fluctuations, not the Hubble-4-volume order-of-magnitude
   sketch.
   - **Acceptance:** reproduce the published fluctuation magnitude; compute a
     `w₀–wₐ` track and overlay the DESI DR2 contour.
   - **Kill:** if the model cannot sit inside the DESI `w₀–wₐ` contour at all, the
     everpresent reading is dead — and CHO's static `w = −1` is the lone survivor,
     which then must face the 2024–25 evolving-dark-energy hints head-on. Either
     way, record it.

2. **Promote CHO from spectator to participant.** Build
   `compute/cho_labelled_causal_set.py`: put a `C⊗H⊗O` label on each causal-set
   element and ask whether the element-counting law *forces* base-3 and/or the
   exponent `64` from the algebra's own structure, instead of inserting them.
   - **Acceptance:** a counting law in which the `3` (base) or `64` emerges from the
     algebraic labelling — this is the bridge from "CHO sets today's value" to "CHO
     sets the dynamics," and the only way Track 1 earns Bayes credit on the `64`
     exponent (~6 bits).
   - **Kill (already a tripwire):** the divergence shape is currently
     *label-independent* — if the CHO label adds nothing to Sorkin's count, CHO
     stays a spectator. Log the converging-negative; no credit moves.

3. **Reach for a gravity brick from the same web.** Combine
   [compute/gravity_curvature.py](compute/gravity_curvature.py) (the `G2`-covariant
   associator metric) with the CHO-labelled causal set to attempt an emergent
   continuum metric.
   - **Acceptance:** a metric that emerges from the discrete CHO causal set and
     reduces toward `SO(3,1)` — the first step past the parked Phase-5 gravity gate.
   - **Kill:** if the associator metric stays positive-semidefinite (Euclidean) with
     no Lorentzian reduction (the existing Phase-5 finding), gravity stays out of
     scope; record and stop.

### Honest scoreboard impact

**Low** direct Bayes (CHO is a spectator in the dynamics), **high** topical
relevance (live DESI data), and it **grows the theory's scope** to gravity +
cosmology. This is "grow the theory," not "win the scoreboard." The one place it
*could* touch the scoreboard is step 2 (forcing the `64` exponent) — keep that
ambition honest: right now it relocates the mystery, it does not abolish it.

---

## Track 2 — The `pi/432` rigidity / uniqueness theorem (the scoreboard jump)

### In plain terms

`pi/432` is the number the whole verdict hinges on. The good news: it is **not**
three lucky coincidences. Two of its three pieces already have real reasons —
the `π` is a geometric "Berry phase" half-twist, and the `432 = 16 × 27` is forced
by a rigidity theorem (Schur's lemma, Theorem B). The missing piece is the
*dynamical rule* (an "action") whose natural resting state produces this twist on
these two spaces. The user's sharpening is the key move: don't just **find an**
action that gives `pi/432` — prove the action is **essentially the only one**.
That is a *rigidity / uniqueness* theorem, and it is what actually convinces a
skeptic.

### Where it stands

- The durable decomposition is `pi/432 = (Berry/WZ π) × 1/(16·27)`. What is missing
  is the `F4`-breaking action that *selects* the flux, the carrier, and the seed
  spectrum.
- The quarantined sandbox
  [experiments/pi432_action_search/](experiments/pi432_action_search/) has the
  state of play: [ruled_out_routes.md](experiments/pi432_action_search/ruled_out_routes.md)
  (heat-kernel `a4/a2`, finite KO-θ, `F4`-invariant `OP²` potentials, single-scale
  RG — all killed as *direct* routes), the top-3 live probes (moment-map orbit
  quantization, anomaly/WZ inflow, Jordan-nonassociative spectral action), and a
  first actual action functional,
  [candidate_wz_jordan_entropy_action.py](experiments/pi432_action_search/candidate_wz_jordan_entropy_action.py),
  whose Euler–Lagrange equations output the seed ratios `(1, √Φ, Φ)` with
  `Φ = pi/432`. Supporting gates already quantize the WZ coefficient to an integer
  *level* (primitive nonzero level → half-flux `π`), but **level-one primitiveness
  and the `Δ₉ × J₃(𝕆)` carrier still have to be derived from the CHO action**, not
  inserted.

### Concrete steps

1. **Reframe the question from existence to rigidity.** Build
   `experiments/pi432_action_search/uniqueness_gate.py`. Instead of "find an action
   that gives `pi/432`," characterize the *space* of admissible WZ/period actions on
   the `Δ₉ × J₃(𝕆)` carrier and ask: is `pi/432` + the seed spectrum **forced**, or
   is it one of many?
   - **Acceptance (the jackpot):** prove that level-one + the carrier are forced by
     the CHO arena, so the action is essentially unique → `pi/432` becomes
     **derived** → scoreboard `−3.2 → +5.6`.
   - **Acceptance (the honest negative, still valuable):** prove that inequivalent
     actions give `pi/432` (non-uniqueness), so the theory has **exactly one
     irreducible free knob** → scoreboard stays `−3.2`, but the claim is now honest
     instead of hopeful. Record it and demote `F0` to a declared single knob.
   - **✓ DONE (2026-06-11).** [uniqueness_gate.py](experiments/pi432_action_search/uniqueness_gate.py)
     built and wired into the quarantined sandbox sweep (moves no Bayes credit).
     The outcome is the *conditional* positive, not the jackpot: among the divisors
     of `432`, only `16` and `27` are irreducible-module dimensions of the CHO
     structure-group chain, so the Schur-flat carrier `(16, 27)` is **unique** —
     but conditional on three named residual knobs (the two-factor ansatz,
     `E6`-over-`F4` for the `27`, and primitive WZ level). Naive numerology is
     killed (`432` has nine factor pairs, several CHO-meaningful). So
     `pi/432`-forced-from-CHO-dynamics stays **OPEN** and the scoreboard stays `−3.2`.

2. **Attack the carrier-selection via the moment-map route.** The top probe
   [moment_map_orbit_quantization.py](experiments/pi432_action_search/moment_map_orbit_quantization.py)
   is precisely about whether the carrier data is *selected* by symplectic
   reduction rather than chosen. This is the natural engine for step 1's positive
   branch.
   - **Acceptance:** a moment-map / symplectic reduction that lands on the
     `Δ₉ × J₃(𝕆)` carrier and level-one flux **without inserting them**.

3. **Rule out the alternative origins (the trap).** The companion result
   [compute/higgs_quartic_geometry.py](compute/higgs_quartic_geometry.py) shows the
   lesson the whole program keeps hitting: every integer in the theory (24, 64, 432)
   has *three or four* equally-good origins. A uniqueness theorem must therefore
   explicitly **rule out the rival origins** of `16`, `27`, and the level, or it has
   not proved uniqueness.
   - **Acceptance:** an enumeration of the candidate origins with a forcing argument
     (or an honest statement that they cannot be separated → the negative branch of
     step 1).

### Honest scoreboard impact

**This is the only track that can flip the sign.** Highest reward, highest risk.
The decisive, *new* conceptual move is the uniqueness framing: a clean *negative*
("`pi/432` cannot be uniquely forced") is itself a publishable, honest result — it
tells you the theory has one irreducible knob, which is very different from
pretending it has none. Keep the quarantine: nothing here moves the scoreboard
until a real candidate action exists with assumptions and a kill condition.

---

## Track 3 — `sin²θ₂₃ = 4/7`, the external verdict (the forward bet)

### In plain terms

Almost every number the framework quotes is a *postdiction* — it explains a value
already measured. **One** number is a genuine *forward* bet on something not yet
decided: the neutrino "atmospheric" mixing angle, predicted to be `sin²θ₂₃ = 4/7`
(the *upper octant*). DUNE and Hyper-Kamiokande will decide it this decade. This is
the first thing that could be **confirmed rather than fitted** — the most credible
outcome a theory can have, because you don't control the experiment.

### Where it stands

This track is the *most developed* on the theory side already:

- The value is **frozen** as `Q2` in
  [compute/prediction_registry.py](compute/prediction_registry.py) (hash-locked).
- The value is **proved canonical**:
  [compute/theta23_fano_invariance.py](compute/theta23_fano_invariance.py) shows
  `4/7` is a finite-geometry invariant — vacuum-independent (every point of the
  Fano plane lies on exactly 3 lines) and convention-independent (under
  `Aut(Fano) = PSL(2,7)`, order 168). No referee can say "you picked the labels."
- The reach is **quantified**:
  [compute/theta23_experimental_reach.py](compute/theta23_experimental_reach.py)
  — at DUNE/Hyper-K precision `σ ~ 0.01`, `4/7` separates from maximal at `7.1σ`
  and from the `3/7` mirror at `14.3σ`; a `5σ` octant verdict needs only
  `σ ≤ 0.0143`. Current data is in genuine tension (the normal-ordering global
  minimum sits on the `3/7` side), so this is a real bet under live pressure.
- The "sharpest claim" status is **machine-checked**, not editorial
  ([compute/prediction_defensibility.py](compute/prediction_defensibility.py)).

The **one open obligation** is the `N5` bridge: the physical map
"atmospheric mixing probability = (Fano lines avoiding the vacuum)/(all lines)".
The *value* `4/7` is forced; the *bridge* to physics is not yet an operator theorem.

### Concrete steps

1. **Sharpen the `N5` bridge from a count to an operator.** Extend
   [compute/epsilon_mixing_coefficients.py](compute/epsilon_mixing_coefficients.py)
   toward a PMNS mixing *operator* whose atmospheric entry is *forced* to `4/7`,
   rather than read off the Fano incidence table.
   - **Acceptance:** a mixing operator on the neutrino sector whose `θ₂₃` entry is
     `4/7` by construction, with the other entries consistent with the measured
     `θ₁₂`, `θ₁₃`.
   - **Kill:** if the operator can produce other octant ratios just as naturally,
     `N5` stays an open bridge — say so; the forward bet still stands on the frozen
     value.
   - **✓ DONE (2026-06-11).** [theta23_mixing_operator.py](compute/theta23_mixing_operator.py)
     recasts `4/7` as the normalized trace of an explicit rank-`4` Fano-line
     projector and proves it is a single-orbit **symmetry-class invariant** under
     all `168` automorphisms (`Pi_g P(v) Pi_g^T = P(g(v))`, point-transitive). The
     *value-half* is now an operator invariant; the **physical map** (oscillation
     probability = projector trace) is *not* derived, so `N5` stays the one open
     bridge, exactly as the kill clause anticipated. Diagnostic; no row promoted.

2. **Freeze and track — the discipline of a verdict you don't control.** Build a
   thin `compute/theta23_data_tracker.py` that ingests each new
   NuFIT / DUNE / Hyper-K release and recomputes the live tension and `σ`
   **without touching the frozen `Q2` payload**. The whole point is that the
   prediction was registered *before* the data; the tracker only watches.
   - **Acceptance:** a dated, append-only log of the octant tension over time,
     cross-checking `Q2` read-only.
   - **✓ DONE (2026-06-11).** [theta23_data_tracker.py](compute/theta23_data_tracker.py):
     dated, append-only snapshot log scored read-only against the frozen `Q2`;
     current representative data is honestly **UNRESOLVED**.

3. **Pre-register the decision rule (formalize what already exists).** Lock the
   verdict protocol from `theta23_experimental_reach.py` as the registered rule:
   `σ ≤ 0.0143` ⇒ `5σ` octant verdict; a stable lower-octant resolution ⇒ **KILL**;
   an upper-octant value far from `4/7` ⇒ value killed, octant survives.
   - **Acceptance:** the rule lives in the registry as a dated, hash-locked decision
     protocol, so no post-hoc reinterpretation is possible.
   - **✓ DONE (2026-06-11).** Implemented as a **SHA-256 hash-locked `DECISION_RULE`**
     inside [theta23_data_tracker.py](compute/theta23_data_tracker.py) (folded into
     step 2's module rather than a separate registry entry): `sigma <= 1/70` ⇒ `5s`
     octant verdict; a stable lower octant ⇒ KILL; a far-upper value ⇒ value killed,
     octant survives. Editing the rule after the fact trips the lock.

### Honest scoreboard impact

**Zero direct Bayes** — it is a forward bet, not yet decided, and it is deliberately
`ε₀`-independent so it stands clear of the `pi/432` seam. But it is the single
highest-*credibility* outcome available: an experiment you don't control either
confirms or kills it. The value-half is already as hardened as it can be without
data; the only remaining theory work is the `N5` bridge (step 1).

---

## How the three tracks interact (and the recommended order)

There is a real link between Tracks 1 and 2. Both are attacks on the **same hole**:
the parked project proved that *static algebra fixes kinematics but never dynamics*
— it can give states, charges, chirality, and the generation count, but it cannot
emit a **measure or a scale**. Track 2 hunts that missing dynamical object in the
*continuous* language (a WZ/Berry-flux action); Track 1 hunts it in the *discrete*
language (a causal-set counting law). A `C⊗H⊗O`-labelled counting dynamics that
produces a measure (Track 1, step 2) is a *candidate* for exactly the dynamical
principle Track 2 needs. **Caveat (honest):** causal-set counting has so far
supplied *form, not CHO content* — so treat the link as "two attacks on one hole,"
not "Track 1 will solve Track 2."

**Recommended order:**

1. **Track 3, step 1 + freeze/track first.** Cheapest, and it is the live forward
   bet — the `N5`-bridge work is bounded and the rest is "register and wait for
   DUNE." Lowest effort, highest credibility.
2. **Track 2 (the uniqueness gate).** The scoreboard lever and the genuinely new
   conceptual move. Highest reward; a clean negative is still a real result.
3. **Track 1 (stochastic everpresent-Λ + CHO-labelled counting).** Grows the scope
   into gravity + cosmology and feeds Track 2's "where does CHO get a measure?"
   question. Most open-ended; pursue with DESI data in hand.

**A combined kill condition for the whole phase:** if (a) the uniqueness gate shows
`pi/432` cannot be uniquely forced, **and** (b) the CHO-labelled causal set adds
nothing to Sorkin's counting, **and** (c) the octant resolves to the lower (`3/7`)
side — then the honest conclusion is that `C⊗H⊗O` is a constrained *parametrization*
with one irreducible knob and no dynamical core, and the right move is to publish the
durable Jordan-algebra theorems (A–D) on their own merit and stop the
theory-of-everything claim. That outcome would be disappointing but **not** a
failure of method — it is the honest-null discipline doing its job.

---

*Status of this plan: a ranked set of bets with kill conditions, in the same spirit
as [BIG_BETS_PLAN.md](BIG_BETS_PLAN.md). It promotes nothing, freezes nothing new,
and moves no Bayes credit. Resuming any track means building the first module listed
under it and recording an honest `EXPLORATORY / OPEN` verdict.*
