# Methodology and Limitations

Frozen date: 2026-06-06

This project should be presented as a **few-input algebraic framework**, not as a completed zero-parameter theory. The strongest current result is the interlocking pattern of low-energy relations. The weakest current layer is the derivation of the continuum action, RG matching, and several algebra-to-physics bridge rules.

## Parameter Language

Use this wording:

> The current CHO audit uses a few explicit inputs and bridge assumptions. It does not fit continuous low-energy parameters separately for each observable.

Avoid this wording except when quoting older titles:

> zero free parameters

Current explicit inputs/assumptions include:

- the choice of algebra `A = C x H x O`
- the physical identification of fermions with minimal left ideals
- the triality-to-generation bridge
- the CHO lattice/information action
- the Planck scale as the dimensional input
- continuum/RG matching prescriptions for `alpha`, `sin^2(theta_W)`, and threshold corrections
- flavour bridge rules such as `epsilon0^2 = pi/432` and first-generation NNI factors, until derived from an operator

## Postdictions vs Predictions

Most numerical agreements in the current table are **postdictions**: the experimental constants were known before these formulas were written. They are still useful if the formulas are constrained, interlocking, and hard to vary, but they should not be described as confirmed predictions.

Use separate categories:

| Category | Meaning | Examples |
|---|---|---|
| Retrodictive relation | Formula compared to already-known data | `m_H`, `m_t`, CKM magnitudes, PMNS angles |
| Bridge test | A relation that tests an algebra-to-physics rule | first-generation NNI factors, `epsilon0^2` |
| Future-facing prediction | Target not yet decisively measured | neutrino ordering, `sum m_nu`, Higgs self-coupling |
| Null exclusion claim | Absence of a class of new physics | no WIMP, no axion, no SUSY, no proton decay |

## Statistical Independence

The 25 audit rows are not 25 independent measurements. Several rows share the same inputs or are algebraic consequences of the same relation:

- `m_c`, `m_s`, `m_mu`, and the inter-sector ratios all reuse `epsilon0^2` and overlapping masses.
- CKM magnitudes share `epsilon0` and the same triality bridge.
- PMNS angles and neutrino splitting share `epsilon0` plus the corrected-TBM bridge.
- Some rows use masses that also appear in ratio rows.

Therefore the summary statistics are descriptive diagnostics, not a formal global likelihood. A stronger next statistical artifact should define a minimal independent observable set and include covariance for mass-derived ratios.

## Continuum/RG Status

The continuum action and RG matching are not yet strong enough to carry the whole theory. In particular:

- `alpha^-1 = 128 pi / 3 + VP` needs a controlled lattice-to-continuum derivation.
- `sin^2(theta_W) = 1/4 + RG` needs a fixed matching scale and threshold treatment derived from CHO rather than inferred from the observed value.
- `M_W = M_P / 3^36` needs a normalization derivation that does not use the electroweak scale as hidden input.
- The cosmological-constant formula needs a more rigorous derivation of free-energy factorization and the `11/12` screening factor.

## Dimensional Counting Warning

Factors such as `16`, `27`, `64`, `3`, `7`, `8`, and `11/12` are suggestive only when they arise from an explicit operator, trace, path integral, or representation-theoretic map. Until then, they should be labeled as bridge rules or ansaetze rather than forced consequences.

Priority bridge upgrades:

1. Derive `epsilon0^2 = pi/432` as an operator trace or transition amplitude.
2. Derive first-generation NNI factors `1/4`, `9/4`, and `1/(4 pi)` from a CHO Yukawa operator.
3. Derive CKM Jarlskog phase placement from the full NNI matrices.
4. Derive corrected PMNS angles from a broken-`Z3` seesaw matrix.
5. Derive continuum/RG matching from the lattice action.

## Null Claims

Null claims are weaker than positive quantitative predictions unless tied to concrete exclusion scales or signatures. Present them as fixed exclusion targets rather than as already-confirmed successes.

Examples:

| Claim | Quantitative benchmark |
|---|---|
| No WIMP dark matter | No confirmed weak-scale nuclear recoil signal above next-generation direct-detection reach for roughly `10 GeV-10 TeV` WIMP masses |
| No QCD axion | No QCD axion signal in the covered haloscope/helioscope mass-coupling windows; no single experiment covers all axion parameter space |
| No low-energy SUSY | No superpartners within direct collider reach, e.g. HL-LHC-scale colored superpartner searches |
| No proton decay | No confirmed proton decay; Hyper-K style bounds should push `p -> e+ pi0` lifetimes toward `~10^35 yr` sensitivity |

These tests constrain broad model classes unevenly. A null result is a consistency check, not a confirmation by itself.
