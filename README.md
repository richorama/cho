# CHO: ℂ⊗ℍ⊗𝕆

A few-input algebraic framework for the Standard Model, built from the tensor product of the three largest normed division algebras.

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
- [EPSILON_BRIDGE.md](EPSILON_BRIDGE.md) — focused bridge target for deriving `epsilon0^2 = pi / 432` as an operator trace or transition amplitude
- [YUKAWA_BRIDGE.md](YUKAWA_BRIDGE.md) — charged-flavour bridge scaffold deriving the NNI adjacency and cascade mass relation
- [PMNS_BRIDGE.md](PMNS_BRIDGE.md) — neutrino-mixing bridge scaffold deriving TBM residual symmetries and the broken-`Z3` perturbation target
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
YUKAWA_BRIDGE.md         Charged-flavour Yukawa bridge scaffold
PMNS_BRIDGE.md           Neutrino-mixing bridge scaffold
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
