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

**Update (2026-06-06): this is now done.** `compute/covariance_gof.py` builds the full covariance with a shared-`eps0` common-mode error (each row enters with sensitivity equal to the power of `eps0` in its CHO formula). Result: the 22 independent rows collapse to an effective `N_eff ~ 10` observables, and the correlated reduced `chi^2 ~ 1.8` against `N_eff` (`p ~ 0.06`) -- statistically consistent but borderline, and notably less impressive than the diagonal figure. Quote `N_eff ~ 10` and the correlated `chi^2`, not the raw row count, for any external goodness-of-fit claim.

## Continuum/RG Status

The continuum action and RG matching are not yet strong enough to carry the whole theory. In particular:

- `alpha^-1 = 128 pi / 3 + VP` needs a controlled lattice-to-continuum derivation.
- `sin^2(theta_W) = 1/4 + RG` needs a fixed matching scale and threshold treatment derived from CHO rather than inferred from the observed value.
- `M_W = M_P / 3^36` needs a normalization derivation that does not use the electroweak scale as hidden input.
- The cosmological-constant formula needs a more rigorous derivation of free-energy factorization and the `11/12` screening factor.

## Dimensional Counting Warning

Factors such as `16`, `27`, `64`, `3`, `7`, `8`, and `11/12` are suggestive only when they arise from an explicit operator, trace, path integral, or representation-theoretic map. Until then, they should be labeled as bridge rules or ansaetze rather than forced consequences.

Priority bridge upgrades:

1. Prove the candidate operator in `CHO_OPERATOR.md` from the CHO action or representation theory.
2. Complete the action-projector proof: Fano incidence motivates rank-one octonionic support, but `epsilon0^2=pi/432` still requires CHO to derive the line-pair selection, Weyl rank-one channel, bridge trace space, and `pi` holonomy.
3. Complete the sector-projector/operator proof: `1`, `3`, and `8` now have number-operator/Fock-trace support, and the lepton `1/(4 pi)` is identified as a transition-sphere measure; the open problem is deriving their selection inside one CHO Yukawa trilinear.
4. Reconcile CKM Jarlskog phase placement and corrected magnitudes in one full charged-Yukawa diagonalization.
5. Resolve the PMNS gap in `OPERATOR_GAP_AUDIT.md`: derive `DeltaY` dynamically and replace simple cyclic-`Z3` language with the actual residual symmetry if needed.
6. Derive continuum/RG matching from the lattice action for `alpha`, `sin^2(theta_W)`, `M_W`, and `Lambda`.

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

## Robustness Audit Artifacts

The following scripts produce the honest figures of merit that should travel with any headline claim. Run them all via `python3 compute/audit.py` (or individually, e.g. `python3 compute/audit.py look_elsewhere`). Quote these numbers, not the raw percentage agreements, when describing how strong the framework is.

| Artifact | Question it answers | Current honest result |
|---|---|---|
| `compute/look_elsewhere.py` | Is each constant the simplest number in CHO's own vocabulary that fits the data, or would many comparably-simple numbers fit? | **12/12 constants are the simplest fitter** (rank 1, no strictly simpler alternative). The per-row density column flags weak rows: `1/2` is cheap (density 0.33), `pi/432` is hard (0.001). This is the strongest, most choice-independent evidence the values are hard to vary. |
| `compute/model_complexity.py` | How many parameters does CHO really have, and does it compress the data? | **17 discrete structural choices + 1 continuous input (M_P), not zero.** Compression ratio `R = L_data/L_model = 1.19` (1.04 including M_P) — a marginal compressor today. Target `R = 1.81` if the per-row prefactors get derived rather than chosen. |
| `compute/independent_observables.py` | What is the real goodness-of-fit once dependent rows are removed and a theory error is stated? | On 22 independent rows with a stated 1.5% theory floor: **reduced chi^2 = 0.92, p = 0.57** (statistically consistent). The `m_e` first-generation row is a visible `-3.75 sigma` outlier. The naive "all rows independent, experimental error only" chi^2 is astronomically large — proof these are approximate relations, not precision predictions. |
| `compute/derived_vs_residual.py` | Where is the error bar on the part CHO actually derives, separate from the underived continuum/RG residual? | The **derived terms** are off by **alpha: -2.2%, sin^2(theta_W): +8.1%, M_W: +1.2%.** The "<0.1%" sometimes quoted belongs to the full formula including the residual CHO has not yet derived. Quote the derived-term error until S1/S4/S5 in the ledger are closed. |
| `compute/first_generation_audit.py` | Why is `m_e` a `-3.75 sigma` outlier, and how bad is it really? | The first-generation masses are SQUARED ratios of *predicted* 2nd/3rd-gen masses, so they compound upstream ~1% errors. The `m_e` headline `-5.6%` decomposes into **~ -2.2% intrinsic** (the unproven `1/(4pi)` factor against measured inputs) **plus ~ -3.4% propagation**. Because the electron mass is known to 8 digits, `m_e` can never be a precision claim until `1/pi` is derived exactly; the honest move is to derive it or demote the row (ledger M11). Removing this single outlier leaves reduced chi^2 ~ 0.29 over the rest. |
| `compute/predict_neutrino_sum.py` | What can near-future data falsify? | **Frozen prediction (2026-06-06): Sigma m_nu = 60 meV (band 57-62), normal ordering.** Surfaces a real internal tension: CHO's `m_nu3 = 48.9 meV` sits ~2.5% below the oscillation floor `sqrt(Delta m31^2) = 50.1 meV`. Falsification conditions are listed in the script. |

Bottom line for external-facing material: CHO's constants are genuinely hard to vary, but it is a few-input (~17 discrete parameters) framework with marginal compression and 2-8% errors on the underived continuum terms. The decisive upgrade — and the entire upside in `R` and goodness-of-fit — is gated on deriving the prefactors, exactly as tracked in `DERIVATION_LEDGER.md`.

