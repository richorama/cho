# CHO Roadmap — Tackling the Four Tiers

Created: 2026-06-06

> **Execution status (2026-06-06): all four tiers actioned in a first pass.** Outcome
> summary at the bottom under "Execution Log." Headlines: T1 produced a written-down
> action that makes the `π` holonomy variational (F0 upgraded, not yet theorem); T2
> added three frozen falsifiers and a covariance GoF that honestly collapses 22 rows to
> `N_eff ~ 10`; T3 added the literature comparison and a no-go audit that **downgrades
> G1/G2 to conjecture-level** on the chirality axis; T4 recorded the down-scoped
> branding and a gravity research line. Several outcomes are deliberately negative —
> as designed.

Purpose: a concrete, file-grounded execution plan for the four prioritized upgrades.
Each item lists **deliverable**, **target files**, **method**, **acceptance criterion**
(what counts as done), and **kill condition** (the honest signal it failed). The whole
point is that several of these can come back negative — and a clean negative is a real
result, not a failure of the project.

Ordering principle: Tier 1 is gating. Tiers 2 and 3 can proceed in parallel and do not
depend on Tier 1 succeeding. Tier 4 is a branding/scope decision plus an optional long
research line.

---

## Tier 1 — Derive one prefactor from a written-down action

**Thesis under test:** `epsilon0^2 = pi/432` is a theorem of a CHO action, not a
coincidence. This is the single experiment that moves the framework from "numerology"
to "derivation." A clean failure here is the most valuable negative result available.

### T1.0 — Write down a candidate action (the actual gating step)
- **Deliverable:** `foundations/02_action.md` — an explicit, written-down functional.
  Not "the CHO information action" by name; an actual `S[Phi]` with fields, domain,
  symmetry group, and measure stated. Minimum viable target: a finite-dimensional
  matrix/spin action on `A_Weyl x J3(O)` (dim 432) whose stationary points and
  fluctuation traces are computable.
- **Method:** Start from the most concrete object you already have — the rank-one
  spurion `T_break = theta |tau><tau|` on the 432-dim space (`SPURION_BRIDGE.md`).
  Define `S` so that (a) its vacuum is the idempotent `omega = (1+i e7)/2`, (b) its
  quadratic fluctuation operator has the Fano/`PSL(2,7)` symmetry already established,
  (c) `theta` appears as a computable holonomy/Berry phase rather than an input.
- **Acceptance:** an action exists on paper such that *every* symbol in
  `epsilon0^2 = Tr(T_break)/432` is defined by `S`, with no free choices left except
  ones forced by symmetry.
- **Kill condition:** you cannot write any `S` whose extremum reproduces the spurion
  without smuggling in `pi`, `432`, or the rank-one structure by hand. If so, say so
  explicitly in `OPERATOR_GAP_AUDIT.md` and downgrade F0 from "open bridge / conditional
  projector derivation" to "ansatz" in `DERIVATION_LEDGER.md`.

### T1.1 — Derive the `432 = 16 x 27` trace space from S
- **Deliverable:** upgrade `compute/spurion_bridge.py` Block 2 from "checks nearby
  alternatives" to "S forces this space."
- **Method:** show the fluctuation operator of `S` is block-diagonal and the only block
  carrying a full complex Weyl generation AND Jordan closure AND the trace direction is
  `A_Weyl x J3(O)`. Today this is asserted by a 3-condition filter; the job is to make
  the 3 conditions *consequences* of `S`'s symmetry, not inputs.
- **Acceptance:** Block 2 prints `PASS` where the alternative spaces are excluded by an
  `S`-derived selection rule, not by a hand list.
- **Kill condition:** the trace space requires a choice not fixed by `S` → record as a
  residual input in the ledger.

> **Progress (eps0 routes 4–4c, seam, R1).** The `16 × 27` factorisation is no longer a hand
> multiplication. `compute/epsilon_state_count.py` derives `16 = dim OP² = F₄/Spin(9)`
> as the rank-one idempotent manifold of `J₃(𝕆)`; `compute/epsilon_product_space.py`
> stratifies `27 = 1 + 16 + 10` and shows the `16` is the off-diagonal octonion pair
> inside the flavour `27`; `compute/epsilon_weyl_isomorphism.py` builds
> `f₄ = Der(J₃𝕆)` (dim 52) and its idempotent-stabiliser `spin(9)` (dim 36, semisimple)
> from scratch and proves the gauge `A_Weyl` and the flavour `T(OP²)` are the **same**
> Spin(9) spinor `Δ₉`; and `compute/epsilon_spin9_embedding.py` closes the last seam by
> recovering the flavour octonionic `Cl(9)` (Casimir multiplicities `1, 9, 126`,
> `{Γ,Γ}=2δ`, bivectors = flavour `so(9)`) and showing gauge and flavour Spin(9) are
> `O(16)`-conjugate — the same subgroup up to one frame choice on the octonion pair.
> The trace-space residual R3 is thereby reduced to that single frame choice — exactly
> the `S`-derived selection rule this task asks for.

### T1.2 — Derive `theta = pi` as a forced (not minimal-by-assumption) holonomy
- **Deliverable:** upgrade Block 4 of `spurion_bridge.py`.
- **Method:** the great-circle/`Omega = 2 pi` loop currently gives `pi`, but the loop is
  chosen as "the minimal geometric loop." Show the *dynamics* of `S` (geodesic of the
  fluctuation metric / least-action triality path) select that loop. This is the
  hardest sub-step and the most likely to fail honestly.
- **Acceptance:** the minimal-action triality path computed from `S` coincides with the
  great circle, numerically, with sub-great-circle loops having higher action.
- **Kill condition:** the great circle is only minimal *geometrically*, not
  *dynamically* → `pi` remains an assumption; document it.

> **Progress (R2, the free-action weight).** `compute/epsilon_free_action.py` removes
> the last "we just chose the free action" input. The rank-one kernel plus its
> complement is a two-level system whose natural `U(2) → SO(3)` Bloch-sphere symmetry,
> assumed alone, forces: invariant potentials are **constant** (transitivity, verified
> to quadratic order — invariant subspace dim `1`), the invariant metric is **round,
> unique up to scale** (`SO(2)` isotropy irreducibility — invariant symmetric 2-tensors
> dim `1`), and `θ = π` is **independent** of that one scale (topological Berry term +
> scale-free geodesics). So the free kinetic action plus the topological term is the
> *unique* symmetric weight; a competing potential is forbidden. R2 shrinks to the
> microscopic origin of the two-level symmetry from `A4` — a symmetry question, not a
> chosen functional.

### T1.3 — Derive the channel coefficients `(1, 3, 8, sqrt7, 1/2, 3, 4)` as traces
- **Deliverable:** upgrade Block 5 + `sector_projector_derivation.py`.
- **Method:** you already derive `1` and `3` as Fock-grade ranks. Push for `8` (lepton
  full-Fock trace) and the `1/pi` measure — these are the two flagged blockers. Each
  coefficient must be `Tr(T_break . P_channel)` with `P_channel` an `S`-derived projector.
- **Acceptance:** at least the lepton `8` is derived as a trace, closing M3 in the ledger.
- **Kill condition:** `8` and `1/pi` still require hand-chosen projectors → keep M3/M11
  as open and do not claim the lepton sector.

> **Progress (M3, the lepton 8).** `compute/epsilon_channel_coefficients.py` closes the
> mass-sector half of T1.3. Using this repo's octonionic Witt ladder (the same basis
> `ladder_charges.py` finds inside `ℂ ⊗ 𝕆`), the number operator `N = Σ αₖ†αₖ` has
> spectral projectors with traces `(1, 3, 3, 1)` on the Fock module `Λ•(ℂ³)`. The three
> mass-sector ranks are then all `N`-spectral traces: `up = Tr P₀ = 1`,
> `down = Tr P₁ = 3`, and `lepton = Tr I_Fock = 2³ = 8` — the lepton `8` is the full Fock
> dimension, not a hand-chosen Yukawa rank. **M3 closed for the mass sector.** What is
> NOT addressed: the CKM/PMNS/ν coefficients `√7, ½, 4` and the lepton shape factor `1/π`
> (M11), which remain open as documented.
>
> **Progress (M11, the mixing counts + lepton `1/(4π)`).** `compute/epsilon_mixing_coefficients.py`
> advances the mixing half. The vacuum `ω=(1+ie₇)/2` fixes `e₇`; the octonion Fano plane
> has `7` lines, of which `3` pass through `e₇` (the SU(3) colour/stabiliser triplet) and
> `4` avoid it. Those integers — read straight off the incidence table, not fitted — ARE
> the mixing multiplicities: `|V_us| = √7·ε₀` (an amplitude, so `√` of the count `7`),
> `sin²θ₁₃ = 3·ε₀²` (3 lines through the vacuum), `Δm²₂₁/Δm²₃₁ = 4·ε₀²` (4 lines avoiding
> it), and `sin²θ₂₃ = 4/7` — all within `~1.4%`. The amplitude-vs-probability `√`-rule is
> Monte-Carlo verified. The lepton `1/(4π)` shape factor is identified as the uniform
> measure on the transition Bloch sphere `S²` (`∫dΩ=4π`), the `π`-carrying partner of the
> full-Fock lepton trace `8`. Open: the `|V_cb|` weak-isospin `½` and the dynamical
> reduction of the lepton trace to that sphere measure.

**Tier 1 exit report:** one short memo `foundations/02_action.md` plus updated
`PASS/FAIL` flags in `spurion_bridge.py`, and a one-line verdict in
`DERIVATION_LEDGER.md` F0 row: *theorem*, *partially derived*, or *demoted to ansatz*.
Any of the three is a publishable honest outcome.

---

## Tier 2 — Strengthen the science without new physics

### T2.1 — Add 3 dated, falsifiable forward predictions
- **Deliverable:** new module `compute/forward_predictions.py` + a `FUTURE_TESTS.md`
  section, each prediction frozen-dated with an explicit kill condition.
- **Targets (lean into tensions, do not hide them):**
  1. **m_nu3 vs oscillation floor.** You already surface that CHO `m_nu3 = 48.9 meV`
     sits ~2.5% *below* the oscillation floor `sqrt(Delta m31^2) = 50.1 meV`. State it
     as a live falsifier: if global fits tighten the floor above the CHO band with the
     CHO normalization held fixed, the neutrino sector is falsified. This is your
     strongest honest forward test because it is an *internal* tension, not a postdiction.
  2. **Neutrinoless double-beta `m_betabeta`.** Derive the CHO band from the frozen
     PMNS angles + normal ordering + the Majorana phases implied by the seesaw, and give
     the kill window against next-gen `0nubetabeta` reach (LEGEND-1000 / nEXO scale).
  3. **Higgs self-coupling `lambda_hhh`.** You already have `lambda = pi/24` from D4.
     Propagate it to a trilinear-coupling prediction `kappa_lambda` and state the
     HL-LHC / FCC kill window.
- **Method:** reuse frozen inputs only; no refitting. Mirror the structure of
  `predict_neutrino_sum.py` (frozen value, band, basis, falsifier list).
- **Acceptance:** three predictions, each with (value, band, date, kill condition),
  reproducible from `python3 compute/forward_predictions.py`.
- **Kill condition (meta):** if a "prediction" cannot be made without choosing a new
  input, it is not a prediction — drop it rather than dress it up.

### T2.2 — Proper independent-observable statistics with covariance (closes STAT1)
- **Deliverable:** upgrade `compute/independent_observables.py` to build a genuine
  covariance matrix for the mass-derived ratios, not just an exclusion list.
- **Method:** (a) identify the minimal generating set of inputs (`M_P`, `epsilon0`,
  3rd-gen anchors, `pi` factors); (b) express each observable as a function of that set;
  (c) propagate the shared-input covariance analytically (Jacobian) so correlated rows
  are not double-counted; (d) report `N_independent`, `reduced chi^2`, and `p` with the
  full covariance, replacing the diagonal-with-floor approximation.
- **Acceptance:** a single defensible sentence — "N independent observables, covariance
  included, reduced chi^2 = X, p = Y" — that survives a referee. Numpy-only (no scipy);
  reuse the incomplete-gamma chi^2 SF already in the module.
- **Kill condition:** with full covariance the fit degrades materially (e.g. reduced
  chi^2 >> 1) → report it; that is the honest GoF and supersedes the headline count.

### T2.3 — Resolve the 23-vs-25 counting inconsistency everywhere
- **Deliverable:** one canonical statement applied consistently across `README.md`,
  `blog_post.md`, the three `papers/*.tex`, and `DERIVATION_LEDGER.md`.
- **Method:** the ledger already has the rule (23 grouped = headline; 25 rows = audit
  with `m_c`, `m_s`, `m_mu` displayed). Grep for `23` and `25` and ensure every external
  mention names which convention it uses on first appearance.
- **Acceptance:** `grep -n "23\|25" README.md blog_post.md papers/*.tex` shows no bare
  count without the grouping qualifier nearby.
- **Kill condition:** none; this is pure hygiene.

---

## Tier 3 — Engage the peer literature directly

### T3.1 — `COMPARISON.md` against Furey, Dixon, Todorov/Dubois-Violette, Boyle/Krasnov
- **Deliverable:** a new `COMPARISON.md` with a claim-by-claim grant/dispute matrix.
- **Method:** for each program, one row per CHO claim class (gauge reps from `Aut`,
  triality -> 3 generations, mass numbers, mixing angles, Lambda) marked:
  *they prove it*, *they would grant it*, *they stop before it*, or *they would dispute
  it*. Be specific: Furey/Dixon establish one-generation reps and stop before masses;
  Baez-Huerta supply the triality theorems you cite as G1/G2; Todorov/Dubois-Violette
  use `J3(O)` (which you also use in the trace space, so overlap is direct); Boyle/Krasnov
  are more conservative on numbers.
- **Acceptance:** every CHO headline claim is explicitly located relative to prior work,
  with at least one citation per program. The repo currently cites no related work in
  its result docs — this closes that gap and pre-empts the obvious referee objection.
- **Kill condition:** if a claimed CHO novelty turns out to already exist in the
  literature, mark it and re-attribute. Better found by you than by a reviewer.

### T3.2 — Stress-test G1/G2 against a Distler–Garibaldi-style no-go
- **Deliverable:** `compute/three_generations_nogo_audit.py` + a section in the
  three-generations paper's notes.
- **Method:** actively try to *break* the triality -> 3 generations theorem the way E8
  unification was broken. Concretely: (a) check chirality — does the triality map produce
  genuinely chiral fermions, or does it force a vector-like partner (the E8 failure mode)?
  (b) check that the three triality reps are physically *distinct generations* and not
  three copies forced into the same rep; (c) enumerate the embedding of one SM generation
  and confirm no anti-generation is dragged in. This is the A2/A3 -> G1 proof obligation
  in the ledger.
- **Acceptance:** either a clean statement "triality -> 3 chiral generations survives the
  chirality/embedding obstruction" (this becomes the headline rigorous result), or an
  explicit identified obstruction.
- **Kill condition:** if a Distler–Garibaldi-type obstruction exists, G1/G2 drop from
  *theorem* to *conjecture* in the ledger — the single most important honesty check in
  the whole project.

---

## Tier 4 — The long game: gravity and branding

### T4.1 — Scope decision (do this first, it is free)
- **Deliverable:** a one-paragraph branding decision recorded at the top of `README.md`
  and `PLAN.MD`.
- **Two honest options:**
  - **(a) Down-scope** the public framing to "an algebraic framework for Standard Model
    parameters from division algebras," which is what the audit docs already support and
    is fully defensible today.
  - **(b) Keep "Theory of Everything"** only if Tier 4.2 becomes a funded research line
    with a real gravity deliverable.
- **Recommendation:** adopt (a) now; treat (b) as conditional on T4.2 producing a metric.
- **Acceptance:** README's first sentence no longer over-claims relative to the ledger.

### T4.2 — Gravity research line (optional, long)
- **Deliverable:** `foundations/03_gravity.md` scoping how `A = C x H x O` could produce
  a metric/curvature sector — currently absent despite `compute/graviton.py`.
- **Method:** the existing PLAN.MD already names the candidate mechanism (associator
  `[a,b,c] = (ab)c - a(bc)` as a torsion/curvature analog; Jacobson-style thermodynamic
  emergence of Einstein equations from the causal-lattice information measure). Turn that
  from prose into a minimal computable model: define the discrete connection, compute one
  curvature invariant, and check the flat-space limit.
- **Acceptance:** one explicit curvature quantity computed from the algebra, with a stated
  continuum limit — enough to justify the word "gravity" beyond a placeholder script.
- **Kill condition:** if no metric emerges without an independent geometric input, accept
  branding option (a) permanently and label gravity as out of scope.

---

## Suggested Sequencing

```text
Week-block 1   T1.0 (write the action)            <- gating, everything keys off this
Week-block 1   T2.3 (counting hygiene)            <- parallel, cheap, do immediately
Week-block 2   T1.1 + T1.2 (trace space, holonomy)
Week-block 2   T3.1 (COMPARISON.md)               <- parallel, no dependency on T1
Week-block 3   T1.3 (channel coefficients)
Week-block 3   T2.1 (forward predictions)         <- parallel
Week-block 4   T2.2 (covariance statistics)
Week-block 4   T3.2 (three-generations no-go)     <- highest rigor payoff
ongoing        T4.1 now (free), T4.2 only if resourced
```

## Definition of Done (project-level)

The framework graduates from "few-input postdictive parametrization" to "candidate
derivation" when **all three** of these hold:

1. **T1:** at least one prefactor (`epsilon0^2 = pi/432`) is a theorem of a written-down
   action — or is honestly demoted to ansatz.
2. **T2.2 + T3.2:** the goodness-of-fit is stated with full covariance, and G1/G2 have
   survived an explicit no-go stress test (or been downgraded).
3. **T4.1:** the public branding matches the ledger.

Every item above is designed so that a *negative* outcome is recorded cleanly. The
project's existing strength is its honesty; this roadmap is built to preserve it.

---

## Execution Log (2026-06-06)

| Item | Outcome | Deliverables |
|---|---|---|
| **T1.0** | **Done.** First written-down CHO action: free-particle + Wess-Zumino functional on the rank-one transition sphere. | [foundations/02_action.md](foundations/02_action.md) |
| **T1.2** | **Partial success (positive).** The `π` holonomy is now the Berry phase of the action's unique **closed geodesic** (great circle) — variational, not "shortest loop." Verified numerically (geodesic curvature zero only at the equator). | [compute/action_derivation.py](compute/action_derivation.py) |
| **T1.1 / T1.3** | **Substantial progress (R1, R2, R3, M3, M11).** The `432 = 16×27` trace space is no longer a hand multiplication: `16 = dim OP²` and `27 = dim J₃(𝕆)` are geometric, the two `16`s (gauge `A_Weyl`, flavour `T(OP²)`) are proven the **same** octonionic Spin(9) spinor `Δ₉` and the gauge-vs-flavour seam is closed to one frame choice; R1's rank-one kernel is reframed as a primitive idempotent (pure, single-generation vacuum) dual to `N_gen=3`; R2's free action is forced by the two-level `U(2)→SO(3)` symmetry (invariant potential constant, metric round up to a `θ`-irrelevant scale); the **mass-sector channel ranks (1, 3, 8) are derived as number-operator Fock-grade traces** (`up=Tr P₀=1`, `down=Tr P₁=3`, `lepton=Tr I_Fock=2³=8`), closing M3; and the **mixing multiplicities (7, 3, 4, 4/7) are derived as Fano-line counts** with the lepton `1/(4π)` identified as the transition-sphere measure (advancing M11). Remaining inputs: the microscopic origin of the two-level symmetry (R2), the `|V_cb|` weak-isospin `½`, and the dynamical reduction of the lepton trace to the sphere measure. | ledger F0/M3/M11, [compute/epsilon_state_count.py](compute/epsilon_state_count.py), [compute/epsilon_product_space.py](compute/epsilon_product_space.py), [compute/epsilon_weyl_isomorphism.py](compute/epsilon_weyl_isomorphism.py), [compute/epsilon_spin9_embedding.py](compute/epsilon_spin9_embedding.py), [compute/epsilon_rank_one_kernel.py](compute/epsilon_rank_one_kernel.py), [compute/epsilon_free_action.py](compute/epsilon_free_action.py), [compute/epsilon_channel_coefficients.py](compute/epsilon_channel_coefficients.py), [compute/epsilon_mixing_coefficients.py](compute/epsilon_mixing_coefficients.py) |
| **T2.1** | **Done.** Three frozen, dated falsifiers with kill conditions: `m_ν₃` vs oscillation floor (2.5% internal tension), `m_ββ = 1.5–3.7 meV`, `κ_λ ≈ 1.01`. | [compute/forward_predictions.py](compute/forward_predictions.py), FUTURE_TESTS Q6/Q7 |
| **T2.2** | **Done (honest negative-ish).** Full covariance with a shared-`eps0` common mode: 22 rows collapse to **`N_eff ~ 10`**; correlated reduced `χ² ~ 1.8` against `N_eff` (`p ~ 0.06`) — consistent but borderline, and **less impressive** than the diagonal figure. Closes STAT1. | [compute/covariance_gof.py](compute/covariance_gof.py) |
| **T2.3** | **Done.** Counting language made consistent (`grouped` qualifier added; one "zero adjustable parameters" claim corrected to few-input language). | papers/electroweak_parameters.tex |
| **T3.1** | **Done.** Claim-by-claim grant/dispute matrix vs Furey, Dixon, Todorov/Dubois-Violette, Baez–Huerta, Boyle/Krasnov, with the Lisi/E8 cautionary case and references to add. | [COMPARISON.md](COMPARISON.md) |
| **T3.2** | **Done (decisive negative).** No-go audit: triality rep-counting is **sound**, but the "3 reps = 3 chiral generations" bridge faces a vector-vs-spinor obstruction and a chirality (mirror-pair) obstruction — the E8 failure mode. **G1/G2 downgraded to "theorem (rep counting), conjecture-level on bridge A3."** | [compute/three_generations_nogo_audit.py](compute/three_generations_nogo_audit.py), ledger G1/G2 |
| **T4.1** | **Done.** Down-scoped branding recorded: "algebraic framework for SM parameters," ToE framing marked aspirational. | README.md, PLAN.MD scope notes |
| **T4.2** | **Done (scoped).** Gravity research line written with a minimal computable milestone (M-GRAV) and a permanent-down-scope kill condition; flags the 8v vector-vs-generation tension with T3.2. | [foundations/03_gravity.md](foundations/03_gravity.md) |

**Net effect on the Definition of Done:** (1) T1 partially met — `π` is action-selected,
full F0 theorem still pending R1–R3; (2) T2.2 met and T3.2 met (G1/G2 stress-tested and
honestly downgraded); (3) T4.1 met. The most important scientific result of this pass is
a **negative** one: the headline three-generations "theorem" is conditional on an
unproven, obstruction-facing bridge — exactly the kind of finding the roadmap was built
to surface.
