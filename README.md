# CHO: ℂ⊗ℍ⊗𝕆

A few-input algebraic framework for the Standard Model, built from the tensor product of the three largest normed division algebras.

> **Scope (updated 2026-06-07).** This project is framed as *an algebraic
> framework for Standard Model parameters from division algebras* — **not** a
> completed Theory of Everything. Phase 5 explicitly keeps gravity out of scope:
> [foundations/11_gravity_gate.md](foundations/11_gravity_gate.md) and
> [compute/gravity_gate_audit.py](compute/gravity_gate_audit.py) show that the
> internal `G2` metric brick does not yet supply a canonical 4D Lorentzian metric
> or dynamics. The defensible claim is a constrained, hard-to-vary
> parametrization of SM masses, mixings, and couplings plus a conditional
> three-generations result.

## What is this?

From the algebra **𝒜 = ℂ⊗ℍ⊗𝕆** (64 real dimensions), the Planck scale, and a small set of explicit bridge assumptions, this framework produces **23 grouped quantitative relations** — particle masses, mixing angles, coupling constants — without fitting a separate continuous parameter for each observable. The computational audit table lists 25 rows because several grouped mass relations are displayed explicitly. Median descriptive error: 1.0%.

This project was developed as a human–AI collaboration (with Claude, Anthropic) exploring whether division algebra structure alone can determine the constants of nature.

## Paper Drafts

The live project is now code and markdown first. Generated PDFs, LaTeX build
outputs, arXiv submission notes, and the old LaTeX paper drafts have been
removed. [papers/](papers/) is now only a placeholder for a future rewrite. Any
future paper should be rebuilt from the ledger, foundation notes, and executable
audits rather than patched forward from stale drafts.

## Blog post

- [blog_post.md](blog_post.md) — accessible overview of the framework and its results

## Audit trail

- [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md) — canonical status ledger for theorem-level claims, bridge assumptions, open derivations, and ansaetze
- [PUBLIC_CLAIMS.md](PUBLIC_CLAIMS.md) — public-facing claim table: what can be said today, what remains conditional, and what must not be claimed yet
- [METHODOLOGY_LIMITS.md](METHODOLOGY_LIMITS.md) — caveats on postdictions, statistical dependence, continuum/RG gaps, dimensional counting, and null tests
- [compute/audit.py](compute/audit.py) — single entry point for the full robustness and derivation-frontier suite (hardness-to-vary, honest MDL parameter count, independent-observable goodness-of-fit, covariance goodness-of-fit, derived-vs-residual error bars, Phase 4 continuum/RG matching, Phase 5 gravity gating, the first-generation outlier decomposition, frozen falsifiable forward predictions, the Lever A–C derivation experiments, the model-comparison Bayes factor, the inverse-spectral knob counts, a tamper-evident prediction registry, and a derivation scoreboard that reads the Bayes factor as one number); run all with `python3 compute/audit.py`, or one with `python3 compute/audit.py <name>`
- [compute/audit_contract.py](compute/audit_contract.py) — machine-readable theory-validation contract: every audit artifact is tied to ledger IDs, current scientific status, public-claim policy, open bridges, kill conditions, and prediction-lock discipline
- [CRITICAL_REPAIR_PLAN.md](CRITICAL_REPAIR_PLAN.md) — next repair plan from the theoretical-physics review: claim hygiene, the algebra-to-physics map, the `epsilon0^2 = pi/432` measure theorem, one Yukawa/seesaw operator, continuum/RG matching, the gravity gate, and prediction discipline
- [foundations/02_action.md](foundations/02_action.md) and [compute/action_derivation.py](compute/action_derivation.py) — first written-down CHO action; derives the `pi` holonomy in `epsilon0^2 = pi/432` as the Berry phase of the action's unique closed geodesic (variational, not "shortest loop"); residuals R1–R3 left explicit
- [compute/forward_predictions.py](compute/forward_predictions.py) — frozen future targets with explicit kill conditions: `m_betabeta` as a positive quantitative prediction, plus `m_nu3` floor tension and `kappa_lambda` as bridge sensitivities
- [compute/covariance_gof.py](compute/covariance_gof.py) — covariance goodness-of-fit (closes STAT1): the 22 independent rows collapse to `N_eff ~ 10` effective observables under the shared-`eps0` common mode
- [COMPARISON.md](COMPARISON.md) — claim-by-claim grant/dispute matrix against the division-algebra literature (Furey, Dixon, Todorov/Dubois-Violette, Baez–Huerta, Boyle/Krasnov) and the Lisi/E8 no-go benchmark
- [compute/three_generations_nogo_audit.py](compute/three_generations_nogo_audit.py) — Distler–Garibaldi-style stress test: the original "3 triality reps = 3 chiral generations" bridge faces vector-vs-spinor and chirality obstructions; the later idempotent-frame route avoids the count/chirality obstruction, while the fermion-content map remains open
- [foundations/07_physics_map.md](foundations/07_physics_map.md) and [compute/physics_map_audit.py](compute/physics_map_audit.py) — Phase 1 repair witness: freezes the one-generation quantum-number map, verifies algebraic `Q`/`T3`/`Y` consistency, and checks SM anomaly cancellation while leaving the three-generation content map and Yukawa spectrum open
- [foundations/03_gravity.md](foundations/03_gravity.md) — scoped, optional gravity research line with a minimal computable milestone and a permanent-down-scope kill condition
- [foundations/11_gravity_gate.md](foundations/11_gravity_gate.md) and [compute/gravity_gate_audit.py](compute/gravity_gate_audit.py) — Phase 5 gravity gate: verifies the internal kinematic metric brick but keeps gravity out of scope because no canonical 4D Lorentzian reduction or dynamics emerge

### Derivation frontier — bringing heavier mathematics to bear
- [compute/jordan_eigenvalue_generations.py](compute/jordan_eigenvalue_generations.py) — **Lever A**: a spectral route to *three* generations that bypasses the triality mirror obstruction. The Freudenthal characteristic polynomial of `J₃(𝕆)` is a cubic with three real roots and three primitive idempotents resolving the identity, so "three" is the *rank* of the algebra (verified on 4000 random Hermitian samples). Structural checks PASS; an honest negative on physical content (a flavour-diagonal element returns only its seeded spectrum)
- [compute/ko_dimension_chirality.py](compute/ko_dimension_chirality.py) — **Lever B**: the decisive cheap chirality test. Builds `Cl(0,7)` from octonion left-multiplications and computes the real-structure signs `(ε, ε″) = (+1, −1)` → **KO-dimension 6**, the same value Connes' noncommutative-geometry Standard Model needs for chirality *without* fermion doubling — the structural cure for the mirror pair that downgrades the generation claim
- [compute/ladder_charges.py](compute/ladder_charges.py) — **Lever C**: the hypercharge filter. The `ℂ⊗𝕆` number operator reproduces the one-generation electric charges `{0, 1/3, 2/3, 1}` with colour multiplicities `(1, 3, 3, 1)` as an *output* of the algebra (Furey / Dubois-Violette), verified numerically
- [compute/bayesian_evidence.py](compute/bayesian_evidence.py) — model-comparison Bayes factor of CHO vs an O(1)-numerology null. The honest scoreboard: it charges CHO the full Occam price for every prefactor it *chooses* and credits nothing for those it *derives*. Crediting only the numerically-closed prefactors (today's conservative floor) gives `ln B ≈ −3`; crediting the geometric `π/432` as well gives `ln B ≈ +6` — the verdict now hinges on a single named seam, not a knob
- [compute/scoreboard.py](compute/scoreboard.py) — **the one-number bottom line.** Reuses the (credit-independent) evidence gain and sweeps the credit policy from "skeptic credits nothing" to "program complete", reading off `ln B` at each step. The `ε₀` derivation program moved the Bayes factor from `ln B = −21` (when only `8/3` was a closed result) → `−3` (today's closed theorems: the Fock-grade ranks, Fano-line counts, and `SU(2)` half-angle) → `+6` once the geometric `π/432` is credited. The sign-flip is pinned to exactly one claim — whether `π/432` is geometrically forced — so the headline is a sharp, falsifiable seam rather than a free parameter
- [compute/spectral_action.py](compute/spectral_action.py) — **inverse-spectral go/no-go**: instead of guessing one operator per channel, declare a single algebra-internal Dirac operator on `ℂ⊗𝕆 = ℂ⁸` (the one-generation module) and *count knobs vs forced constants*. The generic Connes count is 32 free parameters; the algebra-internal restriction buys only `0.68` bits (down to 20), and the spectrum carries **no forced non-trivial mass ratio**. A clean negative that is informative: a single generation cannot produce a hierarchy, which turns the `432 = 16 × 27` space from a fitted choice into a forced requirement
- [compute/cross_generation_count.py](compute/cross_generation_count.py) — the same knobs-vs-constants count on the cross-generation Yukawa: a `3 × 3` inter-generation matrix under the NNI texture and `Z₃` triality collapses from 9 → 6 → **3** free parameters, but 3 knobs is just an overall scale plus 2 ratios — **break-even, not a net derivation**. One spurion `ε₀` supplies the steep hierarchy without cutting the count, tying directly to the Bayes factor: only a *derived* `ε₀² = π/432` flips `ln B` positive

#### Deriving `ε₀² = π/432` — turning an assembly into geometry
The target `π/432` was an *assembly* of three independently-chosen pieces (`π`, `16`, `27`). Four triangulating experiments convert them into geometric objects, attacking residual R3 of [foundations/02_action.md](foundations/02_action.md):
- [compute/epsilon_heat_kernel.py](compute/epsilon_heat_kernel.py) — **which `π`?** A spectral-action `π` can only enter as `(4π)^{−d/2}`, never as a bare numerator. The bare `π` is the Berry half-solid-angle `½·2π`. **Heat-kernel origin ruled out, geometric/holonomy origin ruled in** — which forces the `432` to be a pure *state count*
- [compute/epsilon_cubic_discriminant.py](compute/epsilon_cubic_discriminant.py) — **which `27`?** A clean negative: the universal cubic-discriminant `27` (`Δ = −4p³ − 27q²`) is *not* the `27` in `π/432`, because a rank-one triality breaking has a double root (`Δ = 0`). The `27` is `dim J₃(𝕆)`, a state count
- [compute/epsilon_state_count.py](compute/epsilon_state_count.py) — **the `16`, derived.** `16 = dim OP² = F₄/Spin(9)` is reproduced numerically as the dimension of the rank-one idempotent manifold of `J₃(𝕆)` (the manifold of triality vacua), via Jacobian nullity at all three primitive idempotents — no longer `dim_ℂ(A_Weyl)` chosen by hand
- [compute/epsilon_product_space.py](compute/epsilon_product_space.py) — **is `432` a genuine product?** Stratifies `27 = 1 + 16 + 10` and shows the geometric `16` is the off-diagonal octonion pair *inside* the flavour `27`, reducing R3 to one named, falsifiable claim: the gauge Weyl generation equals the vacuum tangent, `A_Weyl ≅ T(OP²)`, as Spin(9) spinors
- [compute/epsilon_weyl_isomorphism.py](compute/epsilon_weyl_isomorphism.py) — **the isomorphism, discharged.** Builds `f₄ = Der(J₃𝕆)` (dim 52) and its idempotent-stabiliser `spin(9)` (dim 36, semisimple) from the octonion table, and proves both the flavour `T(OP²)` (the `F₄/Spin(9)` isotropy rep) and the gauge `A_Weyl` (an octonionic `Cl(9)` spinor) are **irreducible 16-dim Spin(9) modules of real type** — hence the *same* spinor `Δ₉`, since Spin(9)'s 16 is unique. R3's named isomorphism is closed; only a gauge-vs-stabiliser Spin(9) subgroup embedding remains
- [compute/epsilon_spin9_embedding.py](compute/epsilon_spin9_embedding.py) — **the seam, closed to a frame.** Finds the flavour `so(9)`'s unique positive-definite invariant metric, then *recovers* its octonionic `Cl(9)` Clifford system as the Casimir vector-eigenspace (multiplicities `1, 9, 126`; `{Γ,Γ}=2δ`; bivectors span exactly the flavour `so(9)`). So gauge and flavour Spin(9) are the **same** octonionic construction, `O(16)`-conjugate by uniqueness of the `Cl⁰(9)≅ℝ(16)` irrep — the seam shrinks to one frame choice on the octonion pair
- [compute/epsilon_rank_one_kernel.py](compute/epsilon_rank_one_kernel.py) — **R1, reframed.** The rank-one kernel `|τ⟩⟨τ|` is a *primitive idempotent* of `J₃(𝕆)` (spectrum `(1,0,0)`, a zero-entropy pure vacuum) — the **same** rank-3 spectral fact that forces `N_gen = 3`. A rank-`r` kernel would switch on `r` generations at once (`ε₀² → r·π/432`, no hierarchy), so rank one is dual to three generations, not an independent ansatz; the residual is vacuum purity
- [compute/epsilon_free_action.py](compute/epsilon_free_action.py) — **R2, reframed.** The rank-one kernel + complement is a two-level system with `U(2)→SO(3)` Bloch-sphere symmetry. Assuming only that symmetry, the invariant potential is *constant* (transitivity), the invariant metric is *round, unique up to scale* (`SO(2)` isotropy), and `θ=π` is *independent* of that scale — so the free action + topological term is the **unique** symmetric weight; a competing potential is forbidden. The residual shrinks to the microscopic origin of the two-level symmetry
- [compute/epsilon_channel_coefficients.py](compute/epsilon_channel_coefficients.py) — **the lepton 8, derived (M3).** Builds the octonionic Witt ladder's number operator `N=Σαₖ†αₖ` on `ℂ⊗𝕆`; its Fock-grade projectors trace to `(1,3,3,1)`. The three mass-sector coefficients are then all `N`-spectral traces: `up=Tr P₀=1`, `down=Tr P₁=3`, `lepton=Tr I_Fock=2³=8` — the lepton `8` is the full Fock dimension, not a hand-chosen rank (CKM/PMNS/ν coefficients and the `1/π` shape factor stay open)
- [compute/epsilon_mixing_coefficients.py](compute/epsilon_mixing_coefficients.py) — **the mixing counts, advanced (M11).** The vacuum `ω=(1+ie₇)/2` fixes `e₇`; the octonion Fano plane's `7` lines split into `3` through the vacuum (colour/stabiliser) and `4` avoiding it. Those counts ARE the mixing multiplicities: `|V_us|=√7·ε₀` (amplitude, `√` of `7`), `sin²θ₁₃=3·ε₀²`, `Δm²₂₁/Δm²₃₁=4·ε₀²`, `sin²θ₂₃=4/7` — all `~1.4%`. The lepton `1/(4π)` is identified as the uniform measure on the transition sphere `S²` (`∫dΩ=4π`). Open: the dynamical reduction of the lepton trace to that measure
- [compute/epsilon_vcb_halfangle.py](compute/epsilon_vcb_halfangle.py) — **the `|V_cb|` ½, derived (C2).** The `½` in `|V_cb|=½·ε₀` is the spin-½ HALF-ANGLE of the `SU(2)` double cover of the transition Bloch sphere: a single-qubit (inter-generation) transition amplitude is `sin(ε₀/2)≈½ε₀` (coefficient `½`), while the `Im(𝕆)` VECTOR channel of `|V_us|` carries the full angle `sin(ε₀)` (coefficient `1`, summed to `√7`). So `√7` vs `½` is exactly vector-vs-spinor, its finite avatar `tan(π/8)=√2−1`. The `½` is no longer a weak-isospin input (open: the CKM channel assignment)
- [compute/epsilon_a4_two_level.py](compute/epsilon_a4_two_level.py) — **the two-level symmetry origin (R2), derived.** The `U(2)→SO(3)` symmetry that the free-action argument assumed is the `SU(2)` closure of the `A₄` flavour group: `A₄`'s normal Klein subgroup `V₄` (the three π-rotations) lifts under `SU(2)→SO(3)` to the qubit Pauli group `Q₈={±I,±iσ}`, whose irreducible 2-dim rep spans `M₂(ℂ)` (Burnside) → continuous closure `U(2)/su(2)`. And `A₄/V₄=ℤ₃` is the three-generation grading — so the same `A₄` forces both the free action *and* `N_gen=3`. Residual: the origin of `A₄` itself
- [compute/gravity_curvature.py](compute/gravity_curvature.py) — **gravity, first kinematic brick (M-GRAV).** Non-associativity gives an internal metric perturbation: the Gram pullback of the transport defect `M_{a,b}(x)=[x,a,b]`, `g_{μν}=⟨[e_μ,a,b],[e_ν,a,b]⟩`, is symmetric, PSD, rank-4, transverse, and `G₂`-covariant. [compute/gravity_gate_audit.py](compute/gravity_gate_audit.py) then applies the Phase 5 decision gate: no canonical invariant four-plane is selected, the metric is not Lorentzian, and no dynamics/Newton constant emerges. Gravity remains an exploratory side project, not part of the present derived framework
- [compute/prediction_registry.py](compute/prediction_registry.py) — Phase 6 locked prediction registry: SHA-256 digests for `Sigma m_nu`, `theta23`, `m_betabeta`, and bridge sensitivities, with a locked manifest digest so silent retunes fail the audit
- [EPSILON_BRIDGE.md](EPSILON_BRIDGE.md) — focused bridge target for deriving `epsilon0^2 = pi / 432` as an operator trace or transition amplitude
- [foundations/08_epsilon_measure_theorem.md](foundations/08_epsilon_measure_theorem.md) and [compute/epsilon_measure_audit.py](compute/epsilon_measure_audit.py) — Phase 2 theorem gate: states the named hypotheses for `pi/432` as one normalized transition measure, checks nearby alternatives, and keeps the scoreboard status conditional
- [ACTION_PROJECTOR_BRIDGE.md](ACTION_PROJECTOR_BRIDGE.md) — action-level audit of what a true rank-one epsilon projector on `A_Weyl x J3(O)` must derive
- [compute/action_projector_derivation.py](compute/action_projector_derivation.py) — diagnostic showing rank-one Fano support and the remaining primitive `A_Weyl x J3(O)` embedding gap
- [PRIMITIVE_PROJECTOR_BRIDGE.md](PRIMITIVE_PROJECTOR_BRIDGE.md) and [compute/primitive_projector_derivation.py](compute/primitive_projector_derivation.py) — conditional derivation showing the normalized `log cos` action selects the primitive Weyl x primitive Jordan product once a rank-one transition kernel exists
- [SPURION_BRIDGE.md](SPURION_BRIDGE.md) and [compute/spurion_bridge.py](compute/spurion_bridge.py) — unified single-spurion operator with failure-closed checks for the transition ray, exact trace space, vacuum-orbit reduction, `pi` Berry-phase holonomy, and one-operator reuse across masses, CKM, PMNS, and neutrinos
- [YUKAWA_BRIDGE.md](YUKAWA_BRIDGE.md) — charged-flavour bridge scaffold deriving the NNI adjacency and cascade mass relation
- [PMNS_BRIDGE.md](PMNS_BRIDGE.md) — neutrino-mixing bridge scaffold deriving TBM residual symmetries and the broken-triality perturbation target
- [CHO_OPERATOR.md](CHO_OPERATOR.md) — unified candidate Yukawa/seesaw bridge operator collecting epsilon, sector projectors, CKM, and PMNS targets
- [foundations/09_yukawa_operator_theorem.md](foundations/09_yukawa_operator_theorem.md) and [compute/yukawa_operator_full.py](compute/yukawa_operator_full.py) — Phase 3 one-operator gate: one composite object, charged-sector matrices, CKM/PMNS closure tests, and explicit open/demotion status
- [foundations/10_continuum_rg.md](foundations/10_continuum_rg.md) and [compute/rg_matching_audit.py](compute/rg_matching_audit.py) — Phase 4 continuum/RG gate: separates algebraic boundary terms, standard one-loop running, threshold/VP inputs, and inverse-matched scales; theorem status remains open
- [OPERATOR_GAP_AUDIT.md](OPERATOR_GAP_AUDIT.md) — hard audit of what the candidate operator still does not derive
- [compute/sector_projector_derivation.py](compute/sector_projector_derivation.py) — diagnostic deriving sector ranks `1` and `3` from Fock-grade orbit counts and isolating the lepton `8`/`1_pi` assumptions
- [FUTURE_TESTS.md](FUTURE_TESTS.md) — dated future-test register separating positive quantitative predictions, bridge sensitivities, and null exclusions
- [FLAVOUR_DERIVATION.md](FLAVOUR_DERIVATION.md) — bridge memo for the explicit flavour derivation scaffold

## Representative Relations

These are descriptive low-energy comparisons. Some entries include underived continuum/RG residuals or open bridge factors; use [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md) and [METHODOLOGY_LIMITS.md](METHODOLOGY_LIMITS.md) for the claim status before quoting them as derivations.

| Observable | Predicted | Measured | Error |
|---|---|---|---|
| Higgs mass | 126.0 GeV | 125.09 GeV | 0.7% |
| Top mass | 174.1 GeV | 172.76 GeV | 0.8% |
| Weinberg angle | 0.231 | 0.23122 | <0.1% |
| Cabibbo angle | 0.2256 | 0.2243 | 0.6% |
| Jarlskog invariant | 3.01×10⁻⁵ | 3.08×10⁻⁵ | 2.3% |
| Cosmological constant | 2.31 meV | 2.24–2.33 meV | ~3% |

## Structure

```
papers/                  Reset paper placeholder; no generated PDFs or live LaTeX drafts
compute/                 Numerical verification scripts (Python 3 + NumPy)
compute/audit_contract.py Semantic contract for every audit artifact
DERIVATION_LEDGER.md     Logical status of each claim and proof obligation
METHODOLOGY_LIMITS.md    Methodology caveats and statistical interpretation
EPSILON_BRIDGE.md        Triality-breaking epsilon bridge target
foundations/08_epsilon_measure_theorem.md Conditional epsilon measure theorem gate
ACTION_PROJECTOR_BRIDGE.md Action-level rank-one projector audit
YUKAWA_BRIDGE.md         Charged-flavour Yukawa bridge scaffold
PMNS_BRIDGE.md           Neutrino-mixing bridge scaffold
CHO_OPERATOR.md          Unified candidate CHO Yukawa/seesaw operator
foundations/09_yukawa_operator_theorem.md Phase 3 one-operator theorem gate
foundations/10_continuum_rg.md Phase 4 continuum/RG matching gate
foundations/11_gravity_gate.md Phase 5 gravity gate / out-of-scope decision
OPERATOR_GAP_AUDIT.md    Remaining proof blockers for the candidate operator
FUTURE_TESTS.md          Frozen future-test register
FLAVOUR_DERIVATION.md    Flavour-sector derivation scaffold and proof gaps
blog_post.md             Public-facing writeup
```

## Validation

Install the Python dependency and run the validation harness:

```bash
python3 -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The tests run one named unittest per registered artifact in [compute/audit.py](compute/audit.py), then enforce the semantic contract in [compute/audit_contract.py](compute/audit_contract.py): contract coverage, prediction-lock alignment, the open `epsilon0` hinge, the one-operator gate, and the gravity out-of-scope decision. The same harness runs in GitHub Actions via [.github/workflows/validation.yml](.github/workflows/validation.yml).

## Paper Policy

Do not treat generated PDFs as source artifacts. Develop the ideas in markdown
and executable audits first; rebuild papers only when a small theorem-level unit
is ready and its open bridges are explicitly separated.

## Future-facing tests and null exclusions

- Normal neutrino mass ordering (JUNO, ~2027–28)
- No confirmed WIMP-like recoil in next-generation direct-detection windows (LZ/XENONnT/DARWIN)
- No proton decay through Hyper-Kamiokande-scale lifetime bounds
- No QCD axion in covered haloscope/helioscope mass-coupling windows
- No supersymmetric particles within HL-LHC-scale direct reach
- Σmν ≈ 60 meV (Euclid/DESI)

Positive discoveries in these channels would put direct pressure on the framework. Null results are consistency checks, not confirmations by themselves.

## License

MIT
