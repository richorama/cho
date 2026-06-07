# Continuum/RG Matching Gate

Created: 2026-06-07

Purpose: make the continuum and renormalization-group assumptions visible before quoting electroweak and cosmological numbers as predictions.

## Desired Theorem

A closed Phase 4 result would prove the following statement from the CHO action.

Given the algebraic boundary terms

```text
alpha^-1_boundary = 128 pi / 3
sin^2(theta_W)_boundary = 1/4
M_W_boundary = M_P / 3^36
Lambda^(1/4)_boundary = (11/12) M_P / (sqrt(2) 3^64)
```

the CHO continuum limit selects the matching scales, threshold scheme, and vacuum-polarization/free-energy corrections before any comparison with low-energy data.

That theorem is not established yet.

## Current Gate

The executable gate is `compute/rg_matching_audit.py`. It separates:

1. the algebraic boundary term,
2. the standard one-loop SM running convention,
3. threshold or vacuum-polarization inputs borrowed from the SM/experiment,
4. matching scales inferred from the observed target.

The audit exits successfully when those pieces are explicit. It does not promote any S1/S4/S5/CC1 ledger status.

## Main Findings

### Fine structure constant

The CHO boundary term is

```text
alpha^-1_boundary = 128 pi / 3 = 134.041287
```

The Thomson value is

```text
alpha^-1(0) = 137.035999
```

so the required residual is

```text
Delta alpha^-1 = +2.994713.
```

A leptonic-only leading-log interpretation would place the inverse-matched scale near `5.054 GeV`. The older QCD-scale story can be represented as a `0.700 GeV` matching example plus a hadronic vacuum-polarization remainder of about `1.061`. Both are external until the action derives the matching scale and the hadronic term.

### Weinberg angle

The audit uses the standard one-loop convention

```text
d alpha_i^-1 / d ln(mu) = -b_i/(2 pi),
b_i = (41/10, -19/6, -7),
```

with GUT-normalized `alpha_1`. Running the measured `M_Z` couplings upward, the scale at which

```text
sin^2(theta_W) = 1/4
```

is

```text
mu_* = 3.679e3 GeV.
```

That is an inverse-matched scale, not currently a CHO-derived scale. The seesaw scale `M_P/3^9` gives `sin^2(theta_W) = 0.401745` under the same one-loop running, and the Planck scale gives `0.471320`, so neither closes S5.

### W mass

The algebraic scale is already close:

```text
M_P / 3^36 = 81.349 GeV,
M_W(obs) / boundary = 0.9881.
```

The remaining issue is not numerical size; it is the electroweak normalization. A proof must derive the normalization without using the measured electroweak scale as hidden input.

### Cosmological constant

The cosmological-constant bridge is not an RG running problem in this gate. The formula gives

```text
Lambda^(1/4) = 2.305 meV.
```

The free-energy factorization, the exponent `64`, and the `11/12` screen remain separate CC1 obligations.

## Verdict

```text
AUDIT STATUS: PASS
THEOREM STATUS: OPEN
```

The current repair value is negative but important: the attractive electroweak residuals are no longer allowed to hide their scale choices. Until the CHO action derives the matching scale, thresholds, and normalization, public prose should say algebraic boundary terms plus open continuum/RG residuals.

## Kill/Demotion Rule

If future work shows that the matching scale is chosen only to hit `alpha` or `sin^2(theta_W)`, then S4/S5 must stay `Open bridge` or be demoted to phenomenological fits. If standard running from a derived CHO scale misses the data beyond the stated theory floor, that mismatch is the result to quote.
