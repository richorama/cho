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

**Update (2026-06-07): Phase 4 gate added.** `compute/rg_matching_audit.py`
separates algebraic boundary terms, standard one-loop running, VP/threshold
inputs, and target-implied scales. It finds `sin^2(theta_W)=1/4` at
`mu_* = 3.679e3 GeV` by inverse running, not from a CHO-derived scale. For
`alpha^-1`, `128 pi/3` needs `Delta alpha^-1 = +2.995`; the legacy `0.700 GeV`
QCD-scale example still needs a hadronic VP remainder of about `1.061`. This is
useful bookkeeping, not a status upgrade.

## Gravity Status

Gravity is explicitly out of scope for the present framework. The kinematic
metric brick in `compute/gravity_curvature.py` is real and useful: it gives a
positive-semidefinite, `G2`-covariant internal rank-4 metric from the octonion
associator. But the Phase 5 gate `compute/gravity_gate_audit.py` shows the
missing pieces are still load-bearing: no canonical invariant 4D spacetime plane
is selected, the internal metric is not Lorentzian, and no field equation or
Newton constant emerges. Public prose should not say CHO derives gravity or GR.

## Three Generations: Count vs Spectrum

The `N_gen = 3` result (`compute/three_generations_frame.py`, ledger G1) is a
COUNT-and-CHIRALITY result: generations are the three primitive idempotents of a
`J3(O)` frame, three `F4`-equivalent IDENTICAL points of `OP^2`. Precisely
because they are identical, the construction does not yet explain anything that
DISTINGUISHES the generations -- the mass hierarchy and the mixing angles. All
of that lives in the Yukawa SPECTRUM, which is OPEN (a flavour-diagonal element
still returns only its seeded diagonal; Lever A `jordan_eigenvalue_generations.py`
C4 is an honest negative). Public prose should say CHO derives that there are
three chiral families, not yet why their masses differ.

The decisive follow-up is `compute/spectral_action_432.py` (the cross-generation
counterpart of `spectral_action.py`'s one-generation negative). It tests the
algebra-internal Yukawa on the generation factor `J3(O)` as Jordan left-
multiplication `L_X`. The result is a STRICT improvement on the one-generation
result, but still a PARTIAL: (i) the spectrum of `L_X` is verified from the
structure tensor to obey a parameter-free AVERAGING LAW -- every inter-generation
mixing level is the arithmetic mean of two generation levels, `{a,b,c}` and
`{(a+b)/2,(b+c)/2,(c+a)/2}` (each x8), so `constants_out = 3` forced relations;
(ii) breaking the inner frame `S3` with the SINGLE existing spurion
`eps0^2 = pi/432` reduces the generation knobs from 3 to 1; but (iii) no
single-knob ladder in `eps0` reproduces the measured charged-lepton hierarchy
(the best, geometric `1, eps0, eps0^2`, misses the lightest state by ~1.4
decades). Net: the open Yukawa-spectrum problem is now localised to ONE scalar
seed function (the three diagonal eigenvalues' profile); the mixing law itself is
derived. Closing it requires a dynamical/variational selection principle the
algebra alone does not supply -- the single genuinely open research item.

`compute/epsilon_generation_ladder.py` sharpens that lone seed further. Writing
each charged-generation mass as a power of the FORCED base `eps0 = sqrt(pi/432)`,
the scheme-clean LEPTON ladder is best described by TRIANGULAR exponents `(0,1,3)`
(log-mass quadratic in generation index; worst miss 0.33 decades), and that hit
is the only one of 28 integer triples fitting within 0.4 decades. The open seed is
therefore not an arbitrary profile but, at least for leptons, a one-knob CURVATURE
in log-mass -- a sharper, smaller target. The caveats stay loud: no single law is
universal across up/down/lepton, and the quark exponents carry MS-bar/scale
caveats, so this is a derived-looking PATTERN, not a theorem.

`compute/generation_cascade.py` reduces that seed structurally rather than fitting
it. Using only the framework's own commitment -- the three generations are the
three roots of the `J3(O)` Freudenthal cubic, whose coefficients are the three F4
invariants `(trace, quadratic, cubic norm)` -- it proves the heaviest generation
equals the trace and that the light-pair PRODUCT is EXACTLY the cubic norm over
the heaviest mass (`m2*m3 = |N3|/m1`, Vieta residual `5e-15`): the lightest
fermion is a genuine cubic-norm SEESAW. In the seesaw regime the three exponents
are `(0, ord T2, ord N3 - ord T2)`, so the open seed collapses from THREE
continuous masses per sector to TWO integer suppression orders `(q,Q)`. The
scheme-clean leptons read the clean `(1,4)` = triangular `(0,1,3)`. The honest
limit is unchanged in kind: `(q,Q)` are NOT universal across quark sectors (up
`~(2,7)`, down `~(2,4)`) and not yet derived from dynamics -- but the open
question is now discrete and two-dimensional, a much smaller target than an
arbitrary mass profile.

## Dimensional Counting Warning

Factors such as `16`, `27`, `64`, `3`, `7`, `8`, and `11/12` are suggestive only when they arise from an explicit operator, trace, path integral, or representation-theoretic map. Until then, they should be labeled as bridge rules or ansaetze rather than forced consequences.

The large base-3 EXPONENTS in the scale relations (`3^36`, `3^9`, `3^64`) deserve
extra caution: a single integer exponent on a fixed base tiles a logarithmic
target in steps of `ln 3 ~ 1.1`, and an `O(1)` prefactor fills most of the gap
between steps. `compute/scale_look_elsewhere.py` quantifies this -- the simple
prefactor library already covers `~93%` of one exponent window -- so a hit is
nearly unavoidable and is weak evidence on its own. Treat the scale relations as
structurally motivated counting rules whose only sharp content is the integer
exponent, not as hard-to-vary derivations.

Priority bridge upgrades:

1. Prove the candidate operator in `CHO_OPERATOR.md` from the CHO action or representation theory.
2. Complete the action-projector proof: Fano incidence motivates rank-one octonionic support, but `epsilon0^2=pi/432` still requires CHO to derive the line-pair selection, Weyl rank-one channel, bridge trace space, and `pi` holonomy.
3. Complete the sector-projector/operator proof: `1`, `3`, and `8` now have number-operator/Fock-trace support, and the lepton `1/(4 pi)` is identified as a transition-sphere measure; the open problem is deriving their selection inside one CHO Yukawa trilinear.
4. Reconcile CKM Jarlskog phase placement and corrected magnitudes in one full charged-Yukawa diagonalization.
5. Resolve the PMNS gap in `OPERATOR_GAP_AUDIT.md`: derive `DeltaY` dynamically and replace simple cyclic-`Z3` language with the actual residual symmetry if needed.
6. Close the continuum/RG matching gate: derive the matching scale, VP/threshold scheme, electroweak normalization, and free-energy screen from the lattice action.

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
| `compute/look_elsewhere.py` | Is each constant the simplest number in CHO's own vocabulary that fits the data, or would many comparably-simple numbers fit? | **12/12 constants are the simplest fitter** (rank 1, no strictly simpler alternative). The per-row density column flags weak rows: `1/2` is cheap (density 0.33), `pi/432` is hard (0.001). This is the strongest, most choice-independent evidence the values are hard to vary. **Scope caveat: this covers only the dimensionless COEFFICIENTS.** The large power-of-three SCALE relations are audited separately. |
| `compute/scale_look_elsewhere.py` | Are the power-of-three hierarchy relations (`M_W`, `M_R`, `Lambda`) as hard to vary as the coefficients? | **No.** On a log axis a simple `prefactor x integer-exponent` already covers `~88-100%` of one exponent window (mean `~93%`), so these hits are CHEAP; the real content is the integer exponent plus an `O(1)` prefactor. The cosmological-constant row is weakest (100% coverage, 30 fitters, CHO rank 30). A base sweep shows base 3 is not uniquely forced. Do NOT cite the `12/12 simplest` figure for these rows. |
| `compute/mass_ratio_rg_audit.py` | At what renormalization scale do the mass-ratio relations hold? | **5/6 are 1-loop RG-invariant** (same-sector ratios cancel) and need no scale. **`m_b/m_tau = 7/3` (M5) is scale-dependent** -- it holds at `mu ~ m_b` (0.8%) and drifts to `-70%` at the GUT scale, so it must be quoted at a stated scale. Corrects a false RG-invariance claim previously in `rg_running.py`. |
| `compute/spectral_action_432.py` | Does the cross-generation 432 = 16x27 structure FORCE the Yukawa spectrum? | **Partly.** The algebra-internal Yukawa `L_X` on `J3(O)` obeys a verified parameter-free **averaging law** (mixing level = mean of two generation levels; `constants_out = 3`), and the single spurion `eps0^2 = pi/432` cuts the generation knobs from 3 to 1. **But no one-knob `eps0` ladder reproduces the measured lepton hierarchy** (best misses the lightest state by ~1.4 decades). The open problem is localised to ONE scalar seed function; closing it needs a dynamical selection principle. |
| `compute/epsilon_generation_ladder.py` | In the FORCED base `eps0 = sqrt(pi/432)`, what integer power is each generation mass? | **Scheme-clean leptons prefer a quadratic-in-index (triangular `(0,1,3)`) law** (worst miss 0.33 dec) over the geometric `(0,1,2)` ladder (1.40 dec), and that triangular hit is the ONLY one of 28 integer triples fitting within 0.4 dec (4% look-elsewhere). `m_c/m_t = eps0^2` to ~0.2%. **But no single law is universal** across up/down/lepton (quark sectors carry MS-bar/scale caveats), so it is a derived-looking pattern, not a theorem. Sharpens the open seed to "a log-mass curvature the dynamics must output". |
| `compute/spurion_perturbation.py` | What algebraic structure could even PRODUCE a power-law generation ladder? | **Two theorems from the J3(O) tensor.** FACT 1: the rank-one spurion lifts exactly ONE level at first order, so a 3-tier hierarchy must be cumulative (orders `eps^1, eps^2, ...`). FACT 2: the canonical Jordan quadratic `U_X` gives MULTIPLICATIVE mixing `{ab,bc,ca}` (residual exactly 0), so log-mass is additive in exponents -- the prerequisite for any power law. The minimal nilpotent chain `c_n=(0,1,2)` then yields triangular `(0,1,3)`, matching leptons (0.33 dec). **Open (not faked):** a dynamical proof that the chain is `c_n=n` and universal. |
| `compute/generation_cascade.py` | If generations are roots of the `J3(O)` cubic, what fixes the hierarchy? | **A derived seesaw + a 3->2 reduction.** The light-pair product equals the Freudenthal cubic norm over the heaviest mass EXACTLY (`m2*m3 = \|N3\|/m1`, residual `5e-15`), so the lightest fermion is a cubic-norm SEESAW; the heaviest equals the trace. The whole sector hierarchy reduces to TWO integer invariant-suppression orders `(q,Q)=(ord T2, ord N3)`, and the scheme-clean leptons read the clean `(1,4)` = triangular `(0,1,3)`. **Open (not faked):** `(q,Q)` are NOT universal across quark sectors (up `~(2,7)`, down `~(2,4)`) and not yet derived from dynamics. |
| `compute/model_complexity.py` | How many parameters does CHO really have, and does it compress the data? | **17 discrete structural choices + 1 continuous input (M_P), not zero.** Compression ratio `R = L_data/L_model = 1.19` (1.04 including M_P) — a marginal compressor today. Target `R = 1.81` if the per-row prefactors get derived rather than chosen. |
| `compute/independent_observables.py` | What is the real goodness-of-fit once dependent rows are removed and a theory error is stated? | On 22 independent rows with a stated 1.5% theory floor: **reduced chi^2 = 0.92, p = 0.57** (statistically consistent). The `m_e` first-generation row is a visible `-3.75 sigma` outlier. The naive "all rows independent, experimental error only" chi^2 is astronomically large — proof these are approximate relations, not precision predictions. |
| `compute/derived_vs_residual.py` | Where is the error bar on the part CHO actually derives, separate from the underived continuum/RG residual? | The **derived terms** are off by **alpha: -2.2%, sin^2(theta_W): +8.1%, M_W: +1.2%.** The "<0.1%" sometimes quoted belongs to the full formula including the residual CHO has not yet derived. Quote the derived-term error until S1/S4/S5 in the ledger are closed. |
| `compute/rg_matching_audit.py` | Are the continuum/RG scales and thresholds derived before comparison, or inferred from the target? | **Phase 4 audit passes, theorem remains open.** Standard one-loop running gives `sin^2(theta_W)=1/4` at an inverse-matched `3.679e3 GeV`, not at the seesaw or Planck scale. `alpha^-1` still needs explicit VP/threshold input, and `M_W` still needs the electroweak normalization. |
| `compute/gravity_gate_audit.py` | Does the internal `G2` metric become 4D Lorentzian gravity with dynamics? | **Phase 5 audit passes, gravity remains out of scope.** The `C x H` Lorentzian arena and internal PSD metric are coherent, but no canonical invariant four-plane is selected, no Lorentzian signature emerges from the associator metric, and no Einstein/Newton dynamics are derived. |
| `compute/first_generation_audit.py` | Why is `m_e` a `-3.75 sigma` outlier, and how bad is it really? | The first-generation masses are SQUARED ratios of *predicted* 2nd/3rd-gen masses, so they compound upstream ~1% errors. The `m_e` headline `-5.6%` decomposes into **~ -2.2% intrinsic** (the unproven `1/(4pi)` factor against measured inputs) **plus ~ -3.4% propagation**. Because the electron mass is known to 8 digits, `m_e` can never be a precision claim until `1/pi` is derived exactly; the honest move is to derive it or demote the row (ledger M11). Removing this single outlier leaves reduced chi^2 ~ 0.29 over the rest. |
| `compute/predict_neutrino_sum.py` | What can near-future data falsify? | **Frozen prediction (2026-06-06): Sigma m_nu = 60 meV (band 57-62), normal ordering.** Surfaces a real internal tension, now quantified honestly by `floor_violation()`: CHO's `m_nu3 = 48.9 meV` sits `~4.6 sigma` BELOW the oscillation floor `sqrt(Delta m31^2) = 50.1 meV`. This is not a soft tension -- `m3` cannot take that value while standard oscillation data hold -- so the N1 seesaw bridge is under active falsification pressure. The integer exponent `9` is fine; the miss is an `O(1)` seesaw normalization (`M_R` must shrink `~2.5%`). Falsification conditions are listed in the script. |
| `compute/prediction_registry.py` | Can future-facing targets be silently retuned after data arrive? | **Phase 6 audit passes when hashes are locked.** The registry separates positive quantitative predictions from bridge sensitivities, records formula/input/channel/kill metadata, and fails if any stored value digest or the manifest digest changes without a new dated entry. |

Bottom line for external-facing material: CHO's dimensionless COEFFICIENTS are
genuinely hard to vary, but the power-of-three SCALE relations are not (`~93%`
log-axis coverage), and it is a few-input (~17 discrete parameters) framework
with marginal compression and 2-8% errors on the underived continuum terms. The
one genuine forward prediction, `m_nu3`, currently sits `~4.6 sigma` below the
neutrino-mass floor, so N1 is under active pressure. The decisive upgrade -- and
the entire upside in `R` and goodness-of-fit -- is gated on deriving the
prefactors, exactly as tracked in `DERIVATION_LEDGER.md`.

