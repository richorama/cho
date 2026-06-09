# BIG BETS — where to point the next phase

*Written 2026-06-08, at the decision point the gold-standard closeout records.*

This is a research plan, not a promise. It exists because the **internal** CHO program
terminated honestly: the one object the static algebra ℂ⊗ℍ⊗𝕆 could never emit — a
**dynamical action / measure / scale** — is exactly where criteria 1, 3, and the open
half of 2 all localise. The scoreboard sits at **ln B = −3.2** (earned floor), favouring
the O(1)-numerology null until π/432 is *granted*. More invariance witnesses are the
treadmill `bayesian_evidence.py` warns about. So: a clean fork, new bets, same honesty.

Nothing here is frozen. These are bets, ranked. We follow the evidence; each bet carries
its own **kill condition** so it can die fast and cheaply on the existing scoreboard.

---

## The lesson that picks the bets

CHO proved a sharp, transferable thing: **static algebra fixes kinematics, never dynamics.**
It gave states, charges, chirality, and an *exact* generation count (N=3, machine-checked,
evading Distler–Garibaldi via F4 connectedness). It could never give a measure or a scale.
Phase 1 (the spectral action) failed *structurally*: a real-analytic spectral action cannot
emit π/432 — that number is a Berry/holonomy (orbit-volume) quantity. Three independent
converging-negatives (heat-kernel a₄/a₂ rational; spectrum-ratio miss; topological-θ gate
zero) all said the same thing.

**Selection filter for every bet below** — score each on three axes:

- **(A) Does it supply dynamics / a measure natively?** (or get it from *counting*) — this is
  the actual hole.
- **(B) Can it ingest CHO's wins** (3 generations, charges, chirality, 16, 27, 432) rather
  than restart?
- **(C) One sharp falsifiable hook**, scored on the existing Bayes scoreboard, with a kill
  condition.

Two things survive from the old project no matter which bet we take: the **honest-null
scoreboard discipline** (measure your own evidence; never spin a null as positive) and the
**explore-first / record-converging-negatives** habit. The difference between us and
assembly theory (a measure dressed as a law, over-claimed past peer review — see its 2024
critiques) is that we *measure our own null and report it*. Keep that.

---

## What's actually on the table (the scoreboard maths)

The single biggest unclaimed chunk of description length is the **three hierarchy
exponents**, all written as powers of 3 in the existing repo:

| scale | repo formula | exponent | repo's (post-hoc, CHOSEN) label |
|-------|--------------|----------|---------------------------------|
| M_W (electroweak) | `M_W = M_P / 3^36` | 36 | "‖Roots₊(E6)‖ = 72/2" |
| M_R (seesaw)      | `M_R = M_P / 3^9`  | 9  | "seesaw exponent" |
| Λ^¼ (cosmological) | `Λ^¼ = (11/12) M_P /(√2·3^64)` | 64 | "dim_ℝ(ℂ⊗ℍ⊗𝕆) = 2·4·8" |

`model_complexity.py` charges these as `CHOSEN` (≈ 5.2 + 3.3 + 6.0 bits, plus 7.3 for the
11/12) ≈ **21.8 bits ≈ 15 nats**. They are the largest single lever on the board: forcing
them moves ln B from −3.2 toward ≈ +12. The repo left them `CHOSEN` because its labels are
**heterogeneous** (a root-count, an algebra-dimension, …) — honest, and the right call.

The clue the repo did not chase: read the exponents **3-adically**.

- All three are **perfect squares**: 36 = 6², 9 = 3², 64 = 8².
- Their **increments are consecutive arena dimensions**:
  36 − 9 = **27 = dim J₃(𝕆)**, and 64 − 36 = **28 = dim so(8)** (the triality algebra).
- So `{9, 36, 64}` are the cumulative sums `9 → 9+27 → 9+27+28` of `{9, 27, 28}` — a
  *homogeneous* set of arena dimensions, unlike the repo's mixed labels.

That is a structural fingerprint, and base-3 is independently distinguished by the theory
(three generations, J₃, triality, Tr P₁ = 3). Hence **Bet 1**.

---

## The bets, ranked

### Bet 1 — *The constants are arithmetic, not analytic.* (3-adic / adelic re-reading) — **START HERE**

**Why first:** biggest needle-move (15 nats), sharpest kill condition, reuses every forced
integer (16, 27, 28, 432, base-3), and it *explains the central failure* — a real-analytic
spectral action lives over ℝ and literally cannot emit a holonomy like π or a 3-adically
natural hierarchy. The constants smell of number theory: 432 = 16·27, 4/7, and the
power-of-3 hierarchies are the kind of object invisible over ℝ and forced over the adeles.

- **(A) measure?** A different completion of ℚ supplies a *different* natural measure; the
  hierarchy "problem" (why M_W ≪ M_P) becomes an artifact of `|·|_∞`. 3-adically these are
  unit-scale, not fine-tuned.
- **(B) reuse?** Directly: same Spin(9)/J₃(𝕆)/triality arena that forced 16, 27, 432;
  the increments are 27 and 28 from that arena.
- **(C) hook + kill:** the exponents `{9, 36, 64}` decompose as cumulative arena dimensions
  `{9, 27, 28}`. **Kill condition:** if (i) base-3 gives no cleaner integer exponents than
  arbitrary bases beyond what the theory independently forces, AND (ii) the
  `{9, 27, 28}` decomposition is not significant against a Monte-Carlo null of random
  exponent triples (look-elsewhere–corrected), then the exponents are genuinely free and we
  log a converging-negative — no nats claimed.

**Named lineage (not crankery):** Volovich's hypothesis (fundamental physics is
number-theoretic), Freund–Witten adelic string amplitudes, the adelic product formula
∏_p|x|_p·|x|_∞ = 1. The novel move is reading *these specific CHO integers* p-adically.

**First module:** `compute/padic_hierarchy.py` (built in this fork) — the 3-adic valuation
of the three hierarchies; the perfect-square + cumulative-dimension audit; a base-specialness
test; a look-elsewhere Monte-Carlo null; honest OPEN/EXPLORATORY verdict.

**RESULT (run, wired, recorded — EXPLORATORY, no credit moved):** the exact arithmetic holds
and is now asserted as tripwires — `{9, 36, 64}` are perfect squares `{3², 6², 8²}` whose
consecutive increments are `+27 = dim J₃(O)` and `+28 = dim so(8)`, a homogeneous ladder where
the repo's labels were heterogeneous. The *conceptual* gain is solid: 3-adically every ratio is
unit-ordinary (adelic product `|x|_∞·|x|_3 = 1`), so the electroweak smallness lives entirely in
`|·|_∞` — the hierarchy "problem" is an archimedean artifact, which is exactly *why* a
real-analytic spectral action over ℝ could never emit these scales. The *numerical* hit is
SUGGESTIVE-ONLY: only the EW ratio is base-3-clean (the CC ratio needs the `√2·12/11` prefactor,
base-3 distance ≈ 0.42 — reported, not hidden), and a seeded look-elsewhere null gives corrected
`p ≈ 0.018`, **above** the 0.001 promotion bar. Verdict: exponents stay `CHOSEN`, F0/S1/N1/CC1
untouched. Recorded in `DERIVATION_LEDGER.md`; contract is `STATUS_EXPLORATORY / VERDICT_OPEN`.
A probe that lit up conceptually and stayed null numerically — the honest-null discipline holds.

**Follow-ons if it lights up:** read 4/7 (θ₂₃) and the π/432 numerator as adelic periods or
(mock) modular-form coefficients; test whether the *whole* constant set satisfies one
arithmetic relation (a single modular form whose q-expansion is the charge/exponent ladder —
the Monstrous-Moonshine precedent: 196883, 432, …).

### Bet 2 — *Make the dynamics primary by counting.* (causal sets × CHO)

The highest-ceiling bet: it could revive the *physics* claim, not just explain the failure.
Causal set theory (Sorkin) gets dynamics from **sequential growth** — pure counting — and
already did what CHO could not: it **predicted the order of magnitude of Λ** ("everpresent
lambda", fluctuating like √N) before the data, *and* it hands you gravity, which CHO gated
out (so CHO was never a ToE).

- **(A) measure?** Natively — the growth dynamics *is* a measure on histories.
- **(B) reuse?** Put a CHO/Jordan internal state on each causet element; ask whether growth
  forces N=3 **and** supplies the action.
- **(C) hook + kill:** does the growth rule *see* the internal index? If the internal CHO
  structure cannot couple to the order-theoretic d'Alembertian, it dies fast.

Pairs naturally with **entropic gravity** (Jacobson/Verlinde/Padmanabhan): Einstein's
equations as an equation of state from horizon entropy — "the action is emergent from
counting microstates." CHO gravity gated out because we tried to derive it as a field;
entropic gravity says don't — count CHO microstates on causal horizons.

> **RESULT (first probe — `compute/causal_set_lambda.py`, EXPLORATORY).** Built the
> Bet 1 × Bet 2 synthesis: bridge CHO's cosmological-constant exponent to Sorkin's
> causal-set law `Λ ~ ±1/√V` (a Poisson fluctuation of the spacetime-atom count `V`, and
> the one *pre-data* causal-set success — it predicted `Λ ~ 10⁻¹²²` *before* the 1998
> supernovae). The arithmetic is exact and clean: Sorkin needs a cosmic 4-volume
> `V = Λ⁻² ~ 3⁵¹² ~ 10²⁴⁴`, which **is** the observed 4-volume in every standard
> convention (Hubble, age, particle horizon); and via `Λ^¼ ~ V^(−1/8)` this recovers the
> CHO exponent `64 ~ (1/8)·log₃(V_obs)` to within ~0.5. So the **single largest `CHOSEN`
> chunk in `model_complexity.py`** (the CC exponent, ~13 bits) gains a candidate
> *statistical-dynamical* origin — a volume-fluctuation scale — supplying the counting
> dynamics the static algebra never had (gold-standard criterion A). **Honest negatives,
> baked in as asserts:** the `1/8 = ¼·½` power is *not* `dim(𝕆)=8` (coincidence, quoted
> not leaned on); base 3 is **unforced** by the volume match (base 8 actually fits the
> cosmic volume *better*, distance 0.02 vs 0.40 — its only warrant is external, from
> Bet 1); and the construction uses the **observed** `V` as input, so it *trades* "why 64?"
> for the cosmic-coincidence "why is the universe this old/large now?" — it relocates the
> mystery, it does not abolish it. **The real payoff is a falsifier, not the number:** CHO
> says `Λ` is a fixed algebraic constant (`w = −1`) while Sorkin's everpresent `Λ` is
> *dynamical* (`w(t) ≠ −1`) — incompatible except at the present epoch, so DESI/Euclid
> `w₀`–`wₐ` discriminate; KILL if dark energy is confirmed an exact constant. Verdict:
> `STATUS_EXPLORATORY / VERDICT_OPEN`, the exponent stays `CHOSEN`, CC1/S1 untouched, **no
> Bayes credit moves**. Recorded in `DERIVATION_LEDGER.md`. A candidate *mechanism* + a
> falsifier — the highest-ceiling bet lit up conceptually; the honest-null discipline holds.

**Follow-ons if it lights up:** put a CHO/Jordan internal state on each causet element and
ask whether the order-theoretic growth dynamics *sees* the internal index (forcing N=3 and
supplying the action — the (B)/(C) tests above); and chase the entropic-gravity angle
(Jacobson horizon-entropy → does counting CHO microstates on a causal horizon reproduce the
Einstein equation of state?).

> **RESULT (second probe — `compute/entropic_gravity_cho.py`, EXPLORATORY).** Ran the
> entropic-gravity follow-on: the *other* thing CHO gated out is gravity itself (why it was
> never a ToE), so ask whether *counting* supplies it. Jacobson 1995 makes Einstein's
> equations an equation of state: `dQ = T dS` on every local Rindler horizon, with the
> Bekenstein–Hawking entropy `S = A/(4G) = A/4`, *yields* `G_μν + Λg_μν = 8πG T_μν`. The
> single non-thermodynamic input is the coefficient `1/4` (= Newton's `G`) — the same kind
> of pure number the static algebra cannot emit. **What counting does:** tiling a horizon
> with cells of CHO internal dimension `d` gives `S = (A/a_cell)·ln d ∝ A` — the area law is
> automatic, exactly the area-extensive entropy Jacobson needs (the dynamics-from-counting
> prerequisite, criterion A). **What it provably does *not* do (the decisive, honest
> negative):** matching `S = A/4` only forces `a_cell = 4 ln d` (and `d = 2` reproduces the
> textbook "it-from-bit" `4 ln 2 = 2.77` Planck-areas/bit); the identity
> `N_cells·log₂(d) ≡ N_bits` holds *exactly* for every `d`, so the CHO internal dimension is
> **pure bit-bookkeeping** — it packs `log₂ d` bits per cell and changes *nothing* about the
> `1/4`. Counting touches only the **form** (area law), never the **content** (the value of
> `G`) — the project's lesson applied to gravity, and a cleaner negative than the Λ probe.
> (Species check: one CHO state per Planck area overcounts, `ln d ≫ 1/4`; the naive match
> needs `d = e^{1/4} = 1.28`, no quantum solution.) **The sharp payoff is a cross-module
> tension, not a number:** the *same* Planck-density causal set that reproduces Λ in
> `causal_set_lambda.py` has, by the Dou–Sorkin result, horizon "molecules" counting the
> area; if each carried a full CHO state of dimension `d` the horizon entropy would be
> `(4 ln d)×` Bekenstein–Hawking — a factor `~13` too big for `d = 27 = dim J₃(𝕆)` — **unless
> the CHO internal state is horizon-unresolved** (a gauge/projected direction, not a free
> horizon d.o.f.). That is a definite, falsifiable constraint linking the two Bet-2 modules.
> Verdict: `STATUS_EXPLORATORY / VERDICT_OPEN`, Newton's `G` is *not* derived (relocated to
> `a_cell = 4 ln d`), no prediction promoted, **no Bayes credit moves**; recorded in
> `DERIVATION_LEDGER.md`. The two probes together delimit what "dynamics from counting" can
> do for CHO: it supplies the *form* of both gated-out sectors (Λ's magnitude as a
> fluctuation, gravity's area law) while the precise *coefficients* (the Λ prefactor, the
> `1/4 = G`) stay CHO-untouched — an honest map of the boundary, not a revival of the claim.

> **RESULT (Bet 2a deepening — `compute/everpresent_lambda_tracking.py`, EXPLORATORY).**
> Invested in the Λ bridge's single biggest debit (it consumes the *observed* 4-volume, so
> it trades "why 64?" for the cosmic-coincidence "why *now*?") by taking Sorkin's
> **everpresent** Λ seriously as a *dynamical* dark energy `Λ(t) ~ ±1/√V(t) ~ H(t)²` and
> turning the constant-vs-dynamical hook into a **computed** redshift divergence. The *same*
> exponent now has two experimentally distinct readings: CHO-**static** (`Λ` fixed, `w = −1`,
> so `Ω_Λ(z) = Ω_{Λ,0}/E(z)²` *dilutes* to zero at high `z`) vs Sorkin-**everpresent**
> (`Λ ~ H²` *tracks* the critical density, `Ω_Λ(z) ~ O(1)` at every epoch). **Two dividends:**
> (1) the everpresent reading **partly repays the why-now debit** — "`O(1)` now" becomes
> "`O(1)` always", a property of the counting law the static reading could not offer; and
> (2) the falsifier is now **quantitative** — the readings diverge as `Ω_ever/Ω_static = E(z)²`
> (≈3 at `z=1`, ≈`6×10⁸` at recombination), exactly the trend DESI/Euclid `w₀`–`wₐ`
> tomography measures, with the 2024–25 hints of *evolving* dark energy (`w₀ > −1`, `wₐ < 0`)
> pointing **away** from the CHO-static `w = −1`. **The honest core, asserted as a tripwire:**
> the entire testable time-structure is **causal-set content** — the divergence *shape* is
> invariant under the CHO exponent (it sets only today's normalization), so CHO is a
> **spectator** in the dynamics. The deepening therefore sharpens the bet in *both*
> directions: it strengthens the *causal-set* side (why-now repaid, a live falsifier) while
> making it unmistakable that a confirmed evolving-DE signal would back **Sorkin over
> CHO-static** — CHO's own `w = −1` is the casualty. (Caveat kept in view: a strictly smooth
> `Λ ~ H²` is degenerate with a rescaled Newton constant; the genuine dark-energy content
> lives in the *sign fluctuations* — Ahmed et al. 2004; Zwane et al. 2018 — not simulated
> here, so no `w₀`–`wₐ` fit is claimed.) Verdict: `STATUS_EXPLORATORY / VERDICT_OPEN`, no
> prediction promoted, **no Bayes credit moves**; recorded in `DERIVATION_LEDGER.md`. Net:
> the most promising bet got more promising *as causal-set physics* and more clearly
> *CHO-agnostic* — the next move that would actually credit CHO is the internal-state growth
> rule (does the dynamics see the index?), the open Bet-2 question this does not close.

> **RESULT (Bet 2 crux — `compute/causal_growth_index.py`, EXPLORATORY).** Ran the
> make-or-break test the two prior probes deferred: *does the causal-set growth dynamics
> SEE an internal CHO index, and thereby force `N = 3` while supplying the action?* Put an
> internal index `sᵢ ∈ {1..N}` on each element of a Rideout–Sorkin classical-sequential-growth
> causet (the transitive-percolation case, i.i.d. pre-closure pairs + transitive closure, so
> both CSG axioms are explicit) and let it couple to the birth probabilities. **What growth
> gives (criterion A, real):** index-blind growth is covariant on every poset — *counting
> supplies a genuine measure on histories*, exactly the object the static algebra never had.
> **What it does NOT give (the decisive negative):** discrete general covariance is
> *equivalent to a symmetric coupling* — a related pair always has its lower element born
> first (its factor is birth-order independent automatically), while an incomparable pair
> `{a,b}` enters as `1 − p(sₐ,s_b)` in one birth order and `1 − p(s_b,sₐ)` in another, so
> covariance ⟺ `p` symmetric (the `V` poset splits `0.042` vs `0.126` under an asymmetric
> coupling, collapses under a symmetric one). That constrains the *coupling*, never the
> *cardinality*: covariance leaves an `N(N+1)/2`-parameter family that is never empty, so a
> covariant non-spectator coupling exists for `N ∈ {2,3,4,5,6}` — **`N = 3` is not singled
> out.** Bell causality is automatic (the measure factorises over pairs) for every `N`, and
> the index-blind causet marginal is exactly `N`-independent (the spectator limit, `TV = 0`).
> **CHO's best shot, also closed:** even a non-trivial *inheritance* (child index = product
> of the parents') is covariant + commutative + associative for every `N` (`ℤ/N`); the
> exceptional rank-3 Albert algebra `J₃(𝕆)` is picked out only by the *non-associative*
> octonionic composition — a kinematic (Hurwitz/Jordan classification) input, **not** anything
> the order-theoretic growth provides. **Verdict:** the growth dynamics is provably *blind to
> the internal index's cardinality* — it can carry a CHO index as a covariant passenger but
> cannot SELECT `N = 3`. Counting gives the FORM (a covariant, Bell-causal measure on
> histories) but never the CONTENT (`N = 3`) — the *same* boundary the Λ and gravity probes
> drew, now shown from the dynamics side. `STATUS_EXPLORATORY / VERDICT_OPEN`, `N = 3` stays a
> kinematic input (`G1` untouched), **no Bayes credit moves**; recorded in
> `DERIVATION_LEDGER.md`. **This resolves the Bet-2 crux as a NEGATIVE:** causal-set growth
> revives the *measure* CHO lacked, but cannot revive the *physics* claim (it does not derive
> the generation count or the action from the internal structure). The honest map of Bet 2 is
> now complete on all three faces — Λ magnitude, gravity area-law, and the growth measure are
> CHO-agnostic *form*; the CHO *content* (the exponent, the `1/4`, the `3`) stays kinematic.

### Bet 3 — *Stop predicting single Yukawas; predict their distribution.* (RMT / free probability)

We are *losing* the one-number coincidence game at −3.2 nats. Random-matrix theory makes the
**distribution** fundamental and universal (microscopic detail washes out; SYK even grows
emergent near-AdS₂ gravity from pure disorder). The CKM/PMNS data genuinely look like
"anarchy with structure."

- **(A) measure?** Yes — a symmetry-constrained ensemble is a measure on textures.
- **(B) reuse?** The CHO symmetry content *constrains* the ensemble (which entries are
  forced zero, which are O(1)).
- **(C) hook + kill:** turns one fragile coincidence into *many* correlated, falsifiable
  statistical observables (mass-ratio and mixing-angle distributions). Kill: if a
  symmetry-blind ensemble fits as well as the CHO-constrained one, CHO adds nothing.

> **RESULT (Bet 3 — `compute/statistical_flavour_ensemble.py`, EXPLORATORY).** Ran the
> kill-condition comparison directly: four Monte-Carlo ensembles of 3×3 complex Yukawas
> (CKM = U_u†U_d), **A** anarchy (symmetry-blind Ginibre), **B** Froggatt–Nielsen hierarchy
> `eps0^(q_i+q_j)` only, **C** the NNI texture zeros, **D** the single zero triality actually
> derives. **The real win:** distributions *do* turn the losing one-number game into a sharp
> many-observable one — they **decisively falsify symmetry-blind anarchy for quarks** (anarchy
> gives large mixing, median sin² ≈ 0.3–0.5, and reproduces the tiny quark CKM moduli with
> probability ≈ 0) while leaving the **same** anarchy viable for the anarchic lepton sector (a
> PMNS-sized θ₁₃ a few % of the time). The observed quark/lepton dichotomy falls straight out.
> **The honest null:** what beats anarchy is the mass **hierarchy**, not the CHO texture. The
> Gatto–Sartori–Tonin correlation corr(|V_us|, √(m_d/m_s)) — the observed coincidence
> 0.2243 ≈ 0.2236 — is ≈ 0 for anarchy but ≈ +0.48 for the Froggatt–Nielsen hierarchy *alone*
> (both scale as eps0^(q1−q2)); CHO's derived triality zero lifts it only ≈ +0.07 more, and the
> hierarchy's contribution **strictly exceeds** the texture zero's (asserted). The discriminator
> is the eps-ladder — the *same* charged input the scoreboard already debits (F0) — and NNI is
> emitted by every Froggatt–Nielsen model. So distributions give the FORM (a falsification that
> kills anarchy) but not the CONTENT (a CHO-specific texture that beats same-hierarchy
> symmetry-blindness): the same boundary the Λ, gravity, and growth-index probes drew, now on
> the flavour-statistics face. **C1..C4 untouched; no Bayes credit moves.** The methodological
> upgrade (predict distributions, kill the symmetry-blind null) is real and worth keeping; it
> just does not, by itself, credit CHO over a generic hierarchical flavour model.

### Bet 4 — *Geometry that **is** the amplitude.* (positive geometry / amplituhedron / surfaceology)

The cleanest existing proof that you don't always need the action we were missing: the
amplitude is the canonical form of a positive geometry, and locality + unitarity *emerge
from positivity* — no Lagrangian. Its incompleteness (only special SUSY/planar theories) is
the open frontier.

- **(A) measure?** The canonical form *is* the dynamics.
- **(B) reuse?** Speculative but pointed: hunt for a positive geometry whose combinatorics is
  an **exceptional / octonionic cluster algebra** (exceptional-type cluster algebras already
  surface in amplitudes). If generations are a cell decomposition, the constants are forced
  by geometry, not chosen. Twistor theory (Penrose) is the bridge; CHO chirality is already
  the right starting structure.
- **(C) hook + kill:** find the octonionic positive geometry or don't — highest build cost,
  fuzziest near-term kill.

> **RESULT (Bet 4 first probe — `compute/positive_geometry_cluster.py`, EXPLORATORY).** Probed
> the positive geometry through its computable skeleton — the finite-type cluster algebra
> (Fomin–Zelevinsky `<->` Dynkin), since the full octonionic amplituhedron is not constructible
> in numpy (and may not exist). All exact integer arithmetic from the Dynkin degree tables.
> **The real win (criterion B — hosting is exact):** the exact exceptional types CHO privileges
> carry its arena integers as cluster/root invariants — `D4` (triality `= ` 3 generations) has
> exactly **16** cluster variables (`= dim C(x)H`) and dimension **28** (`= dim so(8)`); `E6`
> (`J3(O)`) has exactly **36** positive roots (the repo's own `M_W` exponent label
> “‖Roots₊(E6)‖”) and a minuscule **27** (`= dim J3(O) = ` 27 lines on a cubic surface
> `= |W(E6)|/|W(D5)|`); the hierarchy increments `{27,28} = {36-9, 64-36} = {E6 minuscule,
> D4 adjoint}`; and `E6` is the **unique** exceptional with a `Z/3` centre, so base-3 is
> structurally distinguished for exactly CHO's algebra (`Gr(3,6)~D4`, `Gr(3,7)/Gr(4,7)~E6` — the
> amplitude bridge is real). **The honest null (criterion A — forcing fails):** those integers
> are root-system data CHO already ingests (reuse, not a new forcing); the genuinely
> cluster-specific invariant — the cluster count `= ` the *cell* number of the positive geometry
> — is NEVER a CHO integer and NEVER **3** (cells `{5,8,14,20,42,50,105,132,182,429,833,4160,
> 25080}`), so the geometry does not force the generation count; the matches are non-unique
> (`27 = ` `A6` cluster vars too) and multi-hosted (`D4, E6, F4, G2` all carry a CHO integer —
> the arena is NOT selected, a humility tripwire); `432 = 16*27` vs `A6`'s 429 cells and `64` vs
> `E7`'s 63 roots are near-miss traps; the `Z/3` centre is `E6` rep theory (a CHO input), not
> canonical-form dynamics, and is not the triality/generation `Z/3`; and the actual octonionic
> positive geometry (cells `= ` generations) is **not** constructed — non-associativity obstructs
> the standard totally-positive cluster coordinates (the open frontier, exactly why this bet is
> highest-cost / fuzziest-kill). **Verdict:** positive geometry HOSTS the CHO exceptional arena
> exactly (and even sharpens “why base-3”) but the canonical-form/cluster machinery forces
> nothing new — the **fifth face** of the same FORM-not-CONTENT boundary. EXPLORATORY, no credit
> moved (`F0`, `G1` stay as charged).

---

## Dusty pure-maths to dust off (tools, aligned with what already worked)

- **Finite geometry & combinatorial designs** — the Fano plane *is* octonion multiplication;
  split octonions ↔ GQ(2,2); the Hesse configuration has 9 points (3 generations × 3
  colours?). The dustiest pick that is *most aligned* with what worked, and exactly where
  "why **exactly** 3?" sometimes gets a forced answer.
- **Operads / cobordism hypothesis** (Baez–Dolan, Lurie) — "dynamics as a monoidal functor
  from cobordisms": an algebra-of-gluing that could supply the action-analogue.
- **Topos / synthetic QM** (Isham–Döring) — maybe the missing measure lives in a topos
  (contextual truth values), not a measure space.
- **Tropical geometry & cluster algebras** — the combinatorial shadow where exceptional
  types and amplitudes meet; connective tissue for Bet 4.
- **Clifford / geometric algebra**; **surreal / nonstandard analysis** (a different
  continuum — relevant to what `continuum_limit.py` wrestled with). Lower priority.

## Cautionary tales (steal the intuition, keep the discipline)

- **Assembly theory** (Cronin–Walker): seductive idea (history/selection as physical), but
  2024 critiques (PLOS Complex Systems; npj Syst. Biol.) show its index reduces to
  LZ/algorithmic complexity and *does not explain selection*. A measure dressed as a law,
  over-claimed past peer review — the exact failure mode our scoreboard exists to prevent.
- **Wolfram hypergraph rewriting / the Ruliad**: real combinatorial machinery (multiway +
  causal invariance), wildly over-claimed physics. A toolbox, not a theory.

---

## Priority

| Bet | Supplies dynamics/measure? | Eats CHO wins? | Sharp hook? | Build cost | Order |
|-----|---------------------------|----------------|-------------|------------|-------|
| 1 · arithmetic / 3-adic | partial (different measure) | **yes** (16,27,28,432,base-3) | **very** (15 nats, 432=16·27) | low | **1st** |
| 2 · causal sets × CHO | **yes** (+ Λ, + gravity) | yes (internal space) | medium | high | 2nd |
| 3 · RMT / statistical flavour | yes (distributions) | yes (texture) | yes (many observables) | medium | 3rd |
| 4 · positive geometry | yes (canonical form) | speculative | low (near-term) | very high | 4th |

**Start with Bet 1.** Cheapest, sharpest kill, reuses the forced integers verbatim, and it
attacks *why* the spectral action failed. If it lights up, Bet 2 is the principled way to get
the dynamics (and gravity) the old approach never could; Bet 3 is the honest fallback that
turns a losing one-number game into a winnable many-observable one.

> **The one-line thesis of Bet 1:** *the CHO constants are written in the wrong number
> system.* π/432 = π/(16·27), 4/7, and the power-of-3 hierarchies are arithmetic/adelic
> objects. The spectral action couldn't emit them because it lives over ℝ while they live
> over the adeles (distinguished prime p = 3, from triality). Test that first — it lights up
> or dies fast, on the existing scoreboard.

Carry the discipline into every bet: keep the scoreboard, record converging-negatives, the
agent never commits.
