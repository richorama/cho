# CHO: ℂ⊗ℍ⊗𝕆

A parameter-free algebraic framework for the Standard Model, built from the tensor product of the three largest normed division algebras.

## What is this?

From the single algebra **𝒜 = ℂ⊗ℍ⊗𝕆** (64 real dimensions) and one measured input (the Planck mass), this framework derives **23 quantitative predictions** — particle masses, mixing angles, coupling constants — with zero free parameters. Median error: 1.0%.

This project was developed as a human–AI collaboration (with Claude, Anthropic) exploring whether division algebra structure alone can determine the constants of nature.

## Papers

- [Paper 1: Three Generations from Octonion Triality](papers/three_generations.pdf) — proves N_gen = 3 from three independent algebraic theorems
- [Paper 2: Electroweak Parameters from ℂ⊗ℍ⊗𝕆](papers/electroweak_parameters.pdf) — 23 predictions with zero free parameters
- [Paper 3: The Cosmological Constant from ℂ⊗ℍ⊗𝕆](papers/cosmological_constant.pdf) — resolves the 122-order-of-magnitude hierarchy

## Blog post

- [blog_post.md](blog_post.md) — accessible overview of the framework and its results

## Key predictions

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
blog_post.md             Public-facing writeup
```

## Building the papers

```bash
cd papers/
pdflatex three_generations.tex && pdflatex three_generations.tex
pdflatex electroweak_parameters.tex && pdflatex electroweak_parameters.tex
pdflatex cosmological_constant.tex && pdflatex cosmological_constant.tex
```

## Falsifiable predictions

- Normal neutrino mass ordering (JUNO, ~2027–28)
- No WIMP dark matter (LZ/XENONnT)
- No proton decay (Hyper-Kamiokande)
- No axion (various experiments)
- No supersymmetric particles (HL-LHC)
- Σmν ≈ 60 meV (Euclid/DESI)

Any one of these failing would falsify the framework.

## License

MIT
