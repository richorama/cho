# CHO: ℂ⊗ℍ⊗𝕆

A few-input algebraic framework for the Standard Model, built from the tensor product of the three largest normed division algebras.

> **Scope (decided 2026-06-06).** This project is framed as *an algebraic framework
> for Standard Model parameters from division algebras* — **not** a completed Theory
> of Everything. It has no dynamical gravity yet (see [foundations/03_gravity.md](foundations/03_gravity.md)
> for the scoped, optional research line). The defensible claim is a constrained,
> hard-to-vary parametrization of SM masses, mixings, and couplings plus a
> conditional three-generations result. The "Theory of Everything" framing in
> [PLAN.MD](PLAN.MD) is aspirational and gated on the gravity work; until a metric
> sector is derived, prefer the down-scoped wording above.

## What is this?

From the algebra **𝒜 = ℂ⊗ℍ⊗𝕆** (64 real dimensions), the Planck scale, and a small set of explicit bridge assumptions, this framework produces **23 grouped quantitative relations** — particle masses, mixing angles, coupling constants — without fitting a separate continuous parameter for each observable. The computational audit table lists 25 rows because several grouped mass relations are displayed explicitly. Median descriptive error: 1.0%.

This project was developed as a human–AI collaboration (with Claude, Anthropic) exploring whether division algebra structure alone can determine the constants of nature.

## Papers

- [Paper 1: Three Generations from Octonion Triality](papers/three_generations.pdf) — proves N_gen = 3 from three independent algebraic theorems
- [Paper 2: Electroweak Parameters from ℂ⊗ℍ⊗𝕆](papers/electroweak_parameters.pdf) — 23 grouped low-energy relations from few inputs
- [Paper 3: The Cosmological Constant from ℂ⊗ℍ⊗𝕆](papers/cosmological_constant.pdf) — resolves the 122-order-of-magnitude hierarchy

## Blog post

- [blog_post.md](blog_post.md) — accessible overview of the framework and its results

## Audit trail

- [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md) — canonical status ledger for theorem-level claims, bridge assumptions, open derivations, and ansaetze
- [METHODOLOGY_LIMITS.md](METHODOLOGY_LIMITS.md) — caveats on postdictions, statistical dependence, continuum/RG gaps, dimensional counting, and null tests
- [compute/audit.py](compute/audit.py) — single entry point for the five robustness artifacts (hardness-to-vary, honest MDL parameter count, independent-observable goodness-of-fit, derived-vs-residual error bars, and a frozen falsifiable neutrino-sum prediction); run `python3 compute/audit.py`
- [ROADMAP.md](ROADMAP.md) — execution plan and log for the four prioritized upgrades (action derivation, forward predictions, covariance statistics, literature comparison, three-generations no-go, branding/gravity scope)
- [foundations/02_action.md](foundations/02_action.md) and [compute/action_derivation.py](compute/action_derivation.py) — first written-down CHO action; derives the `pi` holonomy in `epsilon0^2 = pi/432` as the Berry phase of the action's unique closed geodesic (variational, not "shortest loop"); residuals R1–R3 left explicit
- [compute/forward_predictions.py](compute/forward_predictions.py) — three frozen, dated falsifiers: `m_nu3` vs the oscillation floor, neutrinoless double-beta `m_betabeta`, and the Higgs self-coupling `kappa_lambda`
- [compute/covariance_gof.py](compute/covariance_gof.py) — covariance goodness-of-fit (closes STAT1): the 22 independent rows collapse to `N_eff ~ 10` effective observables under the shared-`eps0` common mode
- [COMPARISON.md](COMPARISON.md) — claim-by-claim grant/dispute matrix against the division-algebra literature (Furey, Dixon, Todorov/Dubois-Violette, Baez–Huerta, Boyle/Krasnov) and the Lisi/E8 no-go benchmark
- [compute/three_generations_nogo_audit.py](compute/three_generations_nogo_audit.py) — Distler–Garibaldi-style stress test: triality rep-counting is sound, but the "3 reps = 3 chiral generations" bridge faces vector-vs-spinor and chirality obstructions, downgrading G1/G2 to conjecture-level on bridge A3
- [foundations/03_gravity.md](foundations/03_gravity.md) — scoped, optional gravity research line with a minimal computable milestone and a permanent-down-scope kill condition

### Derivation frontier — bringing heavier mathematics to bear
- [compute/jordan_eigenvalue_generations.py](compute/jordan_eigenvalue_generations.py) — **Lever A**: a spectral route to *three* generations that bypasses the triality mirror obstruction. The Freudenthal characteristic polynomial of `J₃(𝕆)` is a cubic with three real roots and three primitive idempotents resolving the identity, so "three" is the *rank* of the algebra (verified on 4000 random Hermitian samples). Structural checks PASS; an honest negative on physical content (a flavour-diagonal element returns only its seeded spectrum)
- [compute/ko_dimension_chirality.py](compute/ko_dimension_chirality.py) — **Lever B**: the decisive cheap chirality test. Builds `Cl(0,7)` from octonion left-multiplications and computes the real-structure signs `(ε, ε″) = (+1, −1)` → **KO-dimension 6**, the same value Connes' noncommutative-geometry Standard Model needs for chirality *without* fermion doubling — the structural cure for the mirror pair that downgrades the generation claim
- [compute/ladder_charges.py](compute/ladder_charges.py) — **Lever C**: the hypercharge filter. The `ℂ⊗𝕆` number operator reproduces the one-generation electric charges `{0, 1/3, 2/3, 1}` with colour multiplicities `(1, 3, 3, 1)` as an *output* of the algebra (Furey / Dubois-Violette), verified numerically
- [compute/bayesian_evidence.py](compute/bayesian_evidence.py) — model-comparison Bayes factor of CHO vs an O(1)-numerology null. **Honest negative at full parameter cost**: charged the full Occam price for all ~83 prefactor bits, the Bayes factor favours the null (`ln B ≈ −21`) until ~31 of those bits are *derived* — making the derivation program the explicit, quantified lever
- [compute/prediction_registry.py](compute/prediction_registry.py) — tamper-evident pre-registration: SHA-256 digests of the frozen falsifiers (`Σmν`, P1–P3) plus a manifest digest, so any later silent retune of a "prediction" is detectable
- [EPSILON_BRIDGE.md](EPSILON_BRIDGE.md) — focused bridge target for deriving `epsilon0^2 = pi / 432` as an operator trace or transition amplitude
- [ACTION_PROJECTOR_BRIDGE.md](ACTION_PROJECTOR_BRIDGE.md) — action-level audit of what a true rank-one epsilon projector on `A_Weyl x J3(O)` must derive
- [compute/action_projector_derivation.py](compute/action_projector_derivation.py) — diagnostic showing rank-one Fano support and the remaining primitive `A_Weyl x J3(O)` embedding gap
- [PRIMITIVE_PROJECTOR_BRIDGE.md](PRIMITIVE_PROJECTOR_BRIDGE.md) and [compute/primitive_projector_derivation.py](compute/primitive_projector_derivation.py) — conditional derivation showing the normalized `log cos` action selects the primitive Weyl x primitive Jordan product once a rank-one transition kernel exists
- [SPURION_BRIDGE.md](SPURION_BRIDGE.md) and [compute/spurion_bridge.py](compute/spurion_bridge.py) — unified single-spurion operator with failure-closed checks for the transition ray, exact trace space, vacuum-orbit reduction, `pi` Berry-phase holonomy, and one-operator reuse across masses, CKM, PMNS, and neutrinos
- [YUKAWA_BRIDGE.md](YUKAWA_BRIDGE.md) — charged-flavour bridge scaffold deriving the NNI adjacency and cascade mass relation
- [PMNS_BRIDGE.md](PMNS_BRIDGE.md) — neutrino-mixing bridge scaffold deriving TBM residual symmetries and the broken-triality perturbation target
- [CHO_OPERATOR.md](CHO_OPERATOR.md) — unified candidate Yukawa/seesaw bridge operator collecting epsilon, sector projectors, CKM, and PMNS targets
- [OPERATOR_GAP_AUDIT.md](OPERATOR_GAP_AUDIT.md) — hard audit of what the candidate operator still does not derive
- [compute/sector_projector_derivation.py](compute/sector_projector_derivation.py) — diagnostic deriving sector ranks `1` and `3` from Fock-grade orbit counts and isolating the lepton `8`/`1_pi` assumptions
- [FUTURE_TESTS.md](FUTURE_TESTS.md) — dated register of future-facing falsifiable predictions frozen on 2026-06-06
- [FLAVOUR_DERIVATION.md](FLAVOUR_DERIVATION.md) — bridge memo for the explicit flavour derivation scaffold

## Key relations

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
papers/                  LaTeX sources and compiled PDFs
compute/                 Numerical verification scripts (Python 3 + NumPy)
DERIVATION_LEDGER.md     Logical status of each claim and proof obligation
METHODOLOGY_LIMITS.md    Methodology caveats and statistical interpretation
EPSILON_BRIDGE.md        Triality-breaking epsilon bridge target
ACTION_PROJECTOR_BRIDGE.md Action-level rank-one projector audit
YUKAWA_BRIDGE.md         Charged-flavour Yukawa bridge scaffold
PMNS_BRIDGE.md           Neutrino-mixing bridge scaffold
CHO_OPERATOR.md          Unified candidate CHO Yukawa/seesaw operator
OPERATOR_GAP_AUDIT.md    Remaining proof blockers for the candidate operator
FUTURE_TESTS.md          Frozen future-test register
FLAVOUR_DERIVATION.md    Flavour-sector derivation scaffold and proof gaps
blog_post.md             Public-facing writeup
```

## Building the papers

```bash
cd papers/
pdflatex three_generations.tex && pdflatex three_generations.tex
pdflatex electroweak_parameters.tex && pdflatex electroweak_parameters.tex
pdflatex cosmological_constant.tex && pdflatex cosmological_constant.tex
```

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
