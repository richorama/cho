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

`compute/cascade_universality.py` then closes the second-generation half of that
open question -- honestly, not by fitting. Written as a Freudenthal seesaw, the
UNIVERSAL skeleton is `(0,2,4)` (`m2/m1 = eps0^2`, `m3/m1 = eps0^4`), and every
sector deviation is a `log_{eps0}()` image of two prefactors. Dividing the
measured middle exponent by the INDEPENDENTLY DERIVED Georgi-Jarlskog integers
`c2 = {up:1, down:3, lepton:8}` (the `8/3 = dim(O)/N_color` relation -- not fitted;
they reproduce the measured `m2/m1` to ~2%) gives a UNIVERSAL `2.00 +/- 0.01`
across all three sectors, and the measured `(q,Q)` are reconstructed to `<1%` from
`(2,4)` plus prefactors. So the second-generation suppression is universally
`eps0^2`; the cascade's apparent `q` scatter was just the derived GJ factors. The
loud caveat: the LIGHTEST generation does NOT become universal -- its reduced
exponent is `4 + log_{eps0}(c3)`, and the first-generation prefactor `c3` is
sector-dependent (lepton `~1/(4 pi)` identified, up `~1/4` and down `~2.2` are the
existing open first-generation anomalies). The cascade's `(q,Q)` residue is thus
reduced to the already-open first-generation O(1) prefactors, not eliminated.

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
| `compute/cascade_universality.py` | Is the cascade `(q,Q)` sector-dependence new free data? | **No -- the second-generation half is the already-derived flavour data.** The universal seesaw skeleton is `(0,2,4)`; dividing the measured middle exponent by the INDEPENDENTLY DERIVED Georgi-Jarlskog factors `{up:1, down:3, lepton:8}` (the `8/3 = dim(O)/N_color` relation, ~2% match) gives a UNIVERSAL `2.00 +/- 0.01` across all sectors, and the measured `(q,Q)` are reconstructed to `<1%` from `(2,4)` + prefactors. So the second-generation suppression is universally `eps0^2`. **Open (not faked):** the lightest exponent reduces to `4 + log_{eps0}(c3)` with the first-generation prefactor `c3` sector-dependent (lepton `~1/(4 pi)` identified; up `~1/4`, down `~2.2` remain the existing open first-generation anomalies). |
| `compute/epsilon_measure_schur.py` | Is the `1/16` and `1/27` in `eps0^2 = pi/432` a chosen normalization (the open seam H4)? | **No -- both are forced by irreducibility (Schur).** The invariant average of a rank-one projector on an irreducible `d`-dim module is the flat `(1/d) I` (Schur). `Spin(9)` acts irreducibly on `Delta_9` (commutant `1`) `-> 1/16`; `F4 = Der(J3O)` is REDUCIBLE on the `27` (commutant `2`, `27 = 1+26`, identity over-weighted `1/3`), so `F4` alone is insufficient; the full cubic-norm group `E6 = f4 (+)` traceless-`L_X` (dim `78`, closes under bracket) is irreducible (commutant `1`) `-> 1/27` to machine precision. This promotes the `1/dim` normalization half of H4 from assumption to theorem. **Open (not faked):** why the phase space is the PRODUCT `Delta_9 (x) J3(O)` (the representation identification); F0 is NOT promoted to `DERIVED`. |
| `compute/epsilon_phase_space_product.py` | If `1/16` and `1/27` are closed, what is still open in the product `Delta_9 (x) J3(O)`? | **The seam is now explicit and narrow.** Under Assumption P (independent commuting gauge/flavour actions with minimal multiplicity), the canonical carrier is `Delta_9 (x) J3(O)` and the factorized invariant average is exact: `(I_16/16) (x) (I_27/27) = I_432/432`, giving `pi/432` mechanically. So normalization + factorization are closed under P. **Open (not faked):** derive Assumption P itself from CHO action/one-operator dynamics; until then F0 stays open. |
| `compute/epsilon_assumption_p_gate.py` | Is there direct operator-level evidence (not just representation counting) for Assumption P in the current scaffold? | **Yes -- strong evidence, still not full derivation.** The current epsilon bridge operator on `16x27` has operator-Schmidt rank `1` (exact separable form), reconstructs as a primitive product to machine precision, and gives normalized trace `pi/432`. A stress test adding an independent second product term raises Schmidt rank to `2`, so the gate is genuinely sensitive to cross-sector mixing. **Open (not faked):** this is still scaffold evidence; deriving the same separable primitive kernel from CHO action dynamics remains the live step. |
| `compute/epsilon_product_irreducible.py` | The gate above tests a separable operator -- isn't that circular, since separability is what Assumption P assumes? | **Yes, that was circular -- and this removes the circular part.** `Delta_9 (x) J3(O)` is irreducible under the factor-wise product group `Spin(9) x E6` (verified by partial-trace Reynolds averaging, `<P>_{G1 x G2} = (1/16) I_16 (x) <Tr_1 P>_{E6}`, no `432x432` element ever formed), so by Schur EVERY rank-one spurion Schur-averages to `I_432/432`. A maximally entangled spurion (operator-Schmidt rank `16`) gives the SAME flat average as a separable one (rank `1`) to `5e-18`: flatness does NOT depend on separability or minimal multiplicity, so those two clauses of Assumption P are now unnecessary. An `F4` control (leaves `27` reducible, residual `1e-2`) confirms factor-wise `E6` is required. **Net:** Assumption P collapses from three clauses to one -- "factor-wise `Spin(9) x E6` invariance". **Open (not faked):** that one clause (equivalently the `432`-dim product arena) is still not derived from the CHO action; F0 stays open. |
| `compute/epsilon_symplectic_volume.py` | Is the PRODUCT `Delta_9 (x) J3(O)` an extra assumption, or can the factorization be a theorem? | **It is a theorem of the orbit method -- given the symmetry is a product group.** `16` and `27` are recomputed from scratch (Weyl dimension formula) as the Bohr-Sommerfeld / Borel-Weil state counts of single coadjoint orbits (the `Spin(9)` spinor orbit, the `E6` minimal orbit; method checks `so(9)` vector `9`, adjoint `36`, `E6` adjoint `78`). Quantization is MULTIPLICATIVE over a direct-product group (verified on `A1xA1->4`, `A2xA1->6`, `A2xA2->9`), so the Liouville volume of the product orbit is `16x27=432`: "the arena is a product" follows from "the symmetry is a product group", not a separate assumption. The bare `pi` is the symplectic half-flux of the minimal transition orbit `CP^1=S^2` (reusing the great-circle Berry phase), giving `pi/432`. **Open (not faked):** `OP^2=F4/Spin(9)` is itself non-symplectic, so the carriers are orbits in `so(9)^*`, `e6^*`, not `OP^2`; WHICH two orbits the CHO action quantizes is still not derived; F0 is NOT promoted. |
| `compute/epsilon_orbit_selection.py` | The symplectic-volume route left "WHICH two orbits does the action quantize?" -- can that be answered, or is it free? | **The two are the MINIMAL (coherent-state) orbits, and 'minimal' is forced for BOTH factors.** (16) `Spin(9)` acts TRANSITIVELY on the spinor sphere `S^15` -- the orbit-tangent `span{A_a v}` has dimension `15` at every unit spinor with stabiliser `36-15=21=dim Spin(7)` -- so the spinor orbit is UNIQUE (no "which orbit" freedom). (27) the `E6` minimal orbit is the rank-one variety of `J3(O)` (Freudenthal sharp `X#=0`, verified zero on rank-one and nonzero on rank-2/3), which is EXACTLY the action's own rank-one selection (`epsilon_rank_one_kernel`, `epsilon_action_stationary`); the rank-one orbit is the minimal nonzero `e6`-orbit (tangent `17 < 26`). The two interlock: the `f4`-orbit `OP^2=F4/Spin(9)` of a rank-one idempotent has tangent dimension `16 = Delta_9`. **Open (not faked):** this GRANTS coherent-state (minimal-orbit) quantization and the external `Delta_9` identification; deriving coherent-state localization from full CHO dynamics is still open; it reduces "which two orbits (assumed)" to "the two minimal orbits (forced)"; F0 is NOT promoted. |
| `compute/epsilon_factor_forcedness.py` | `432` factors ten ways -- why `16 x 27`, and why a product of two groups at all? | **`16 x 27` is the unique derived-carrier split, and `432` is no single-group minimal rep.** Among all ten factorizations, `16 x 27` is the ONLY pair whose both factors are independently-derived carriers (`16 = Delta_9 = dim OP^2`, `27 = dim J3(O)`), strictly out-scoring every rival (`8 = dim O`, `4 = dim H`, `36 = dim so(9)`, each paired with a structureless partner). A single-group no-go scan recomputes the fundamental-rep dimensions of `su(n)`, `so(n)`, `G2, F4, E6, E7, E8` from their root systems and finds `432` among NONE of them, while it IS the `Spin(9) x E6` (spinor)x(minimal) bifundamental, so a product is forced. **Open (not faked):** this ranks pre-derived structure (it does not by itself derive the two carrier dimensions) and is a minimal/fundamental-rep statement, not an absolute no-go; F0 is NOT promoted. |
| `compute/epsilon_action_stationary.py` | Within an action class, is the primitive separable epsilon kernel actually variationally forced? | **Yes -- in the normalized link-action class.** For `O>=0, Tr(O)=pi`, the objective `S_link=log(<O,K>/(||O||_F||K||_F))` obeys `S_link<=0` by Cauchy, with equality iff `O` is proportional to `K`; fixed trace then forces unique maximizer `O=piK`. The current scaffold operator saturates exactly; random PSD/separable scans lie strictly below. **Open (not faked):** this does not yet derive the physical ray `K` or the admissible class itself from full CHO action equations. |
| `compute/epsilon_action_selection.py` | `epsilon_action_stationary` feeds in the rank-one ray `K` by hand -- is rank one assumed, or is it extremal? | **It is extremal: the rank-one ray is the global minimiser of the `E6`-invariant cubic potential `N3`.** The Freudenthal sharp IS the gradient of the cubic norm, `X# = grad N3` (finite-difference `dN3|_X(Y)` vs the trace-form `<X#,Y>` matches to `~1e-8`; `N3 = det =` eigenvalue product), so the critical locus of `N3` is exactly `X#=0` (rank `<=1`). Trace-constrained criticality `X#=lam I` has ONLY `{rank-one}` (`lam=0`) and `{central cI}` (`lam=c^2`); on the physical slice `{O>=0, Tr O=1}` AM-GM gives `N3 in [0, 1/27]` with the rank-one idempotents the global MINIMISERS (`N3=0`, the minimum flat exactly along the `f4`-orbit `OP^2` of tangent dim `16`, rising into the full-rank bulk `diag(1-2t,t,t)`) and `I/3` the unique maximiser (`1/27`). `F4` preserves `N3` (`~1e-15`); `E6` preserves the rank-one variety (`~1e-13`). Interlock: the SAME `N3` whose group `E6` Schur-forces the flat `1/27` measure (`epsilon_measure_schur`) selects the ray via its minimisers (`max N3 = 1/27 = 1/dim` because `dim J3(O)=27=3^3`, quoted not leaned on). **Open (not faked):** deriving that the CHO action's potential IS this `N3` (not just identifying it), the kinetic coefficient on the Berry `pi`, and the full equations of motion are still open; this is a variational CHARACTERISATION of the ray, not an action-level derivation of the kernel; F0 is NOT promoted and no Bayes credit moves. |
| `compute/lepton_yukawa_action.py` | Can ONE action produce ONE charged-lepton Yukawa operator end-to-end, or is the lepton `1/(4 pi)` just a chosen angle density? | **It is forced, and the operator assembles end-to-end.** The two-level Bloch sphere `S^2` of `foundations/02_action.md` supplies BOTH lepton numbers: its hemisphere solid angle (`2 pi`) is the Berry `theta = pi` (Bargmann great-circle holonomy, computed to `9e-16`), and its total solid angle (`4 pi`) is the SU(2) invariant-average (Schur) normalization, so `k_l = 1/(4 pi)` is `1/(total solid angle)` of the SAME sphere -- not a fitted density. Reusing the derived Fock trace `8` (M3) and the rank-one "lift exactly one level" rule, the single Hermitian `Y = m_tau * diag(1, 8 eps0^2, k_l(8 eps0^2)^2)` lands `tau` exactly and `mu/tau` at `-2.2%`. **Open (not faked):** `e/tau` is `-6.3%` (the known M11 outlier, reported -- only `mu` is asserted); WHY leptons take the continuous-sphere average while quarks take discrete weak-isospin projections (`1/4`, `9/4`, no `pi`) is not derived; the trilinear is not yet obtained from the CHO equations of motion; F0 is NOT promoted. |
| `compute/sector_sphere_dichotomy.py` | WHY does the lepton shape carry `pi` (`1/(4 pi)`) while the quark shapes (`1/4`, `9/4`) are rational? | **One discriminant: `pi` <=> CONTINUOUS average, rational <=> DISCRETE average.** A finite group (`Q8`) averages the rank-one projector to EXACTLY `I/2` (rational, no `pi`); the continuous `S^2` average is `1/(4 pi)` (`Vol(S^2)=4 pi` is transcendental). The sector's Fock support sets the regime: a quark projects onto a SINGLE number-operator grade (`up=Tr P_0=1`, `down=Tr P_1=3=N_c`, discrete -> rational), giving `k_u=(Tr P_0/2)^2=1/4` and `k_d=(Tr P_1/2)^2=9/4=(1/4)N_c^2` -- exactly ledger M10's sector-square rule, from the SAME derived Fock ranks; the colour-singlet lepton uses the full continuous colourless module -> the sphere measure `1/(4 pi)`. The naive discrete extrapolation `(8/2)^2=16` is REPLACED by the continuum. **Open (not faked):** WHY the colour singlet uses the continuous average while the coloured sectors project onto a single grade (the dynamical SELECTION) is still the input; the `(rank/2)^2` law is a two-sector fit; the `~6%` `m_e` residual is untouched; F0 is NOT promoted. |
| `compute/model_complexity.py` | How many parameters does CHO really have, and does it compress the data? | **17 discrete structural choices + 1 continuous input (M_P), not zero.** Compression ratio `R = L_data/L_model = 1.19` (1.04 including M_P) — a marginal compressor today. Target `R = 1.81` if the per-row prefactors get derived rather than chosen. |
| `compute/independent_observables.py` | What is the real goodness-of-fit once dependent rows are removed and a theory error is stated? | On 22 independent rows with a stated 1.5% theory floor: **reduced chi^2 = 0.92, p = 0.57** (statistically consistent). The `m_e` first-generation row is a visible `-3.75 sigma` outlier. The naive "all rows independent, experimental error only" chi^2 is astronomically large — proof these are approximate relations, not precision predictions. |
| `compute/per_row_theory_error.py` | Is the single global 1.5% theory floor the right error model, or should each row carry an error set by its own derivation status? | The global floor is methodologically wrong: it over-credits underived rows and hides where the theory is actually sharp. Item 6 keys each row's theory error to its **weakest-bridge status** (frozen `DERIVED`/`GEOMETRIC`/`CHOSEN` taxonomy + open-residual flags), tier magnitudes fixed from independent sister rows (not tuned) and cross-checked by the eps0-ladder's own `1.23%` RMS. Honest two-sided result: the one fully eps0-independent exact theorem `sin^2 theta_23 = 4/7` earns a precision test and **passes** (exp pull `-0.02`); but a sub-percent (`0.5%`) claim for the DERIVED-prefactor ladder rows `m_s`, `m_mu` is **falsified at 2.4–2.8 sigma** — they are `~1.5–2%` relations, so the geometric tier stays at `~1.5%` until the ladder normalization is derived; the continuum rows `alpha^-1`, `sin^2 theta_W` are derivation-limited and **excluded, not inflated**. A sensitivity scan (halving every tier error → `p ~ 0.09`) confirms the widths are real, not padding. GoF refinement only: no row promoted, scoreboard/Bayes factor untouched. |
| `compute/derived_vs_residual.py` | Where is the error bar on the part CHO actually derives, separate from the underived continuum/RG residual? | The **derived terms** are off by **alpha: -2.2%, sin^2(theta_W): +8.1%, M_W: +1.2%.** The "<0.1%" sometimes quoted belongs to the full formula including the residual CHO has not yet derived. Quote the derived-term error until S1/S4/S5 in the ledger are closed. |
| `compute/rg_matching_audit.py` | Are the continuum/RG scales and thresholds derived before comparison, or inferred from the target? | **Phase 4 audit passes, theorem remains open.** Standard one-loop running gives `sin^2(theta_W)=1/4` at an inverse-matched `3.679e3 GeV`, not at the seesaw or Planck scale. `alpha^-1` still needs explicit VP/threshold input, and `M_W` still needs the electroweak normalization. |
| `compute/rg_scale_derivation.py` | Can the electroweak matching scale be DERIVED, or is it inverse-fit (Item 3)? | **No single matching scale exists -- the scale is inverse-fit (KILL branch).** CHO's two electroweak boundaries (`alpha_em^-1 = 128 pi/3` and `sin^2 = 1/4`) fix BOTH gauge couplings (`alpha_1^-1 = 96 pi/5 = 60.319`, `alpha_2^-1 = 32 pi/3 = 33.510`) at one would-be scale, but one-loop running reaches them at `mu ~ 12 GeV` vs `mu ~ 2.2e5 GeV` -- a `1.8e4` discrepancy, so the single-continuum-scale reading is FALSIFIED. The lone inverse-matched `sin^2 = 1/4` scale is `M_P/3^32.5` (a non-integer power of three), and no independently-derived CHO scale (`v`, `M_W`, seesaw, `M_P`) lands at `1/4` (closest miss `0.0138`). **Open (not faked):** S4/S5 stay Open bridge with a sharper, falsification-grade reason; deriving one physical matching scale + threshold scheme from CHO is the obligation. No row promoted; scoreboard untouched. |
| `compute/gravity_gate_audit.py` | Does the internal `G2` metric become 4D Lorentzian gravity with dynamics? | **Phase 5 audit passes, gravity remains out of scope.** The `C x H` Lorentzian arena and internal PSD metric are coherent, but no canonical invariant four-plane is selected, no Lorentzian signature emerges from the associator metric, and no Einstein/Newton dynamics are derived. |
| `compute/first_generation_audit.py` | Why is `m_e` a `-3.75 sigma` outlier, and how bad is it really? | The first-generation masses are SQUARED ratios of *predicted* 2nd/3rd-gen masses, so they compound upstream ~1% errors. The `m_e` headline `-5.6%` decomposes into **~ -2.2% intrinsic** (the unproven `1/(4pi)` factor against measured inputs) **plus ~ -3.4% propagation**. Because the electron mass is known to 8 digits, `m_e` can never be a precision claim until `1/pi` is derived exactly; the honest move is to derive it or demote the row (ledger M11). Removing this single outlier leaves reduced chi^2 ~ 0.29 over the rest. |
| `compute/predict_neutrino_sum.py` | What can near-future data falsify? | **Frozen prediction (2026-06-06): Sigma m_nu = 60 meV (band 57-62), normal ordering.** Surfaces a real internal tension, quantified by `floor_violation()`: CHO's `m_nu3 = 48.9 meV` sits `1.2 meV` BELOW the oscillation floor `sqrt(Delta m31^2) = 50.1 meV`, which against the floor's experimental error alone reads as `~4.6 sigma`. That experimental-only figure is reassessed in `neutrino_floor_resolution.py` (next row, Item 4): with the tree-level theory error folded in it is a `~1.2 sigma` undershoot. Falsification conditions are listed in the script. |
| `compute/neutrino_floor_resolution.py` | Is the `m_nu3` floor deficit really a `4.6 sigma` falsification (Item 4)? | **No -- it is a `~1.2 sigma` undershoot once the tree-level seesaw carries its own theory error.** The `4.6 sigma` divides the `1.2 meV` deficit by the floor's EXPERIMENTAL error alone, assigning ZERO error to a tree-level seesaw whose two inputs are derived only up to an `O(1)` normalization. Calibrated from their SISTER rows -- `M_R = M_P/3^9` (sister `M_W = M_P/3^36`, `+1.2%`) and `y_nu3 = 1` (sister `y_t = 1`, `+0.8%`, entering squared) -- the theory error is `~2.0%` (`+/- 1.0 meV`), giving `1.2 sigma`. **Demoted (not faked):** N1 drops from a precision claim to order-1 consistency; the central value is stated plainly as still just below the physical floor; the obligation is to DERIVE the `O(1)` normalization (genuine kill = a pinned derived normalization still below the floor). The frozen `Sigma m_nu` band still covers the on-floor minimal sum. No row promoted; scoreboard untouched. |
| `compute/prediction_registry.py` | Can future-facing targets be silently retuned after data arrive? | **Phase 6 audit passes when hashes are locked.** The registry separates positive quantitative predictions from bridge sensitivities, records formula/input/channel/kill metadata, and fails if any stored value digest or the manifest digest changes without a new dated entry. |
| `compute/theta23_octant_prediction.py` | If the framework must stake ONE sharp falsifiable bet on an unmeasured quantity, which one, and why that one (Item 7)? | **`sin^2(theta23) = 4/7 = 0.5714` (`theta23 = 49.1 deg`, UPPER octant) — the single sharpest CHO claim.** It is selected over every other prediction because it is the ONLY mixing number that is an exact rational AND `eps0`-INDEPENDENT: the module verifies `d sin^2 theta_23 / d eps0 = 0` exactly under an `eps0 +/- 20%` scan, while the control `sin^2 theta_13 = 3 eps0^2` moves — so it stands clear of the open `pi/432` seam that hinges the Bayes factor. It also already **passed** the Item-6 per-row precision test (exp pull `-0.02`). The octant is the **Fano discriminator**: the lower-octant mirror is exactly `cos^2 = 3/7`, and the same partition that fixes the value (`4` Fano lines avoiding the vacuum `e7` vs `3` through it) fixes the octant (`4 > 3` IS "upper"). **Genuine forward bet (not faked):** the octant is currently UNRESOLVED (T2K/NOvA tension), so this is pre-registered, not a postdiction; KILL = a stable lower-octant resolution (`sin^2 < 1/2`) or an upper value pinned far from `4/7`; decisive reach DUNE / Hyper-Kamiokande. The Fano-count→angle map stays a derived bridge (N5), not a theorem; the module cross-checks the frozen registry (Q2) read-only and promotes NO row — scoreboard/Bayes factor untouched. |
| `compute/jordan_standalone_theorems.py` | What part of the underlying mathematics stands on its own, with no physical interpretation attached (Item 5)? | **Three classical-in-assembly theorems, decoupled and machine-verified.** (A) The Jordan-frame `S3` is INNER in the connected `F4` (preserves all three F4 invariants, drift `~1e-14`), so it permutes three congruent `OP^2 = F4/Spin(9)` points carrying the SAME real spinor `Delta_9` -- categorically unlike the OUTER `Spin(8)` triality on the inequivalent `8v,8s,8c`, so no mirror/Distler-Garibaldi obstruction applies. (B) Schur forces the flat `1/16` and `1/27` (the latter needs `E6`, not `F4`), product `1/432`. (C) Vieta on the Freudenthal cubic is the exact seesaw `m2*m3 = |N3|/m1` (`5e-15`). Every ingredient is classical and cited; the contribution is the clean decoupled assembly. **Decoupled (not faked):** registered `diagnostic`; it does NOT close G1/F0/A3 and must not be cited as physical evidence. See `PAPER_JORDAN_THEOREMS.md`. |

Bottom line for external-facing material: CHO's dimensionless COEFFICIENTS are
genuinely hard to vary, but the power-of-three SCALE relations are not (`~93%`
log-axis coverage), and it is a few-input (~17 discrete parameters) framework
with marginal compression and 2-8% errors on the underived continuum terms. The
one genuine forward prediction, `m_nu3`, sits `1.2 meV` below the neutrino-mass
floor -- a `~1.2 sigma` undershoot once the tree-level seesaw carries its own
theory error (`neutrino_floor_resolution.py`), so N1 is demoted to order-1
consistency rather than a precision claim, with its central value still just
below the physical floor. The decisive upgrade -- and the entire upside in `R`
and goodness-of-fit -- is gated on deriving the prefactors, exactly as tracked
in `DERIVATION_LEDGER.md`.

