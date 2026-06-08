# Future Test Register

Frozen dates: 2026-06-06, 2026-06-07

This file records future-facing tests whose decisive data are still ahead. The point is to keep the targets fixed before future data arrive. Null exclusions are weaker than positive quantitative predictions, so the relevant experimental scale/window is listed where possible.

Phase 6 status: the quantitative registry is locked by `compute/prediction_registry.py`. Re-running that artifact recomputes every value payload and fails if any stored hash changes without a new dated entry.

Generated summary: run `PYTHONDONTWRITEBYTECODE=1 python3 compute/prediction_registry.py --markdown` to produce a markdown table directly from the locked registry rows.

Update protocol: new data or a theoretical revision creates a dated addendum. Old frozen entries are never overwritten. If a target depends on an unfixed bridge that can move after data arrive, it is labelled a bridge sensitivity rather than a positive prediction.

## Null Exclusions / Hard Falsifiers

These are falsifiable exclusions. Continued null results are consistency checks, not positive confirmations.

| ID | Fixed prediction | Test channel | Falsifying outcome | Notes |
|---|---|---|---|---|
| F1 | No fourth fermion generation at any mass | Collider searches, precision electroweak fits | Discovery of a fourth SM-like generation | Strongest consequence of the generation theorem |
| F2 | Normal neutrino ordering | JUNO, DUNE, Hyper-K | Inverted ordering established | CHO seesaw hierarchy assumes normal ordering |
| F3 | No WIMP dark matter in the usual weak-scale window | LZ, XENONnT, DARWIN, collider missing-energy searches | Confirmed weak-scale particle dark matter with SM weak interactions | Benchmark window: roughly `10 GeV-10 TeV`; null results are consistency checks, not confirmation |
| F4 | No QCD axion in covered mass-coupling windows | ADMX, MADMAX, helioscopes, haloscopes | Axion discovery | Strong CP is claimed to vanish by Fano parity; no single experiment covers all axion parameter space |
| F5 | No proton decay through next-generation lifetime bounds | Hyper-Kamiokande, DUNE | Any confirmed proton decay channel | Benchmark: `p -> e+ pi0` sensitivity approaching `~10^35 yr` would strongly test the claim |
| F6 | No low-energy supersymmetry within direct collider reach | HL-LHC and future colliders | Superpartners discovered | Benchmark: HL-LHC-scale colored superpartner searches; heavier inaccessible SUSY is not fully excluded by null results |
| F7 | No free fractional electric charges beyond SM quark confinement | Millicharge and fractional-charge searches | Free fractional charge discovered | Charge quantization is a gauge/representation claim, not a positive discovery forecast |
| F8 | `theta_bar = 0` exactly | nEDM and storage-ring EDM searches | Nonzero strong CP phase inferred | Null EDM bounds are consistency checks; a nonzero strong CP phase would hit the Fano-parity claim |

## Positive Quantitative Predictions

These entries have frozen value hashes in `compute/prediction_registry.py`.

| ID | Frozen target | Exact formula / source | Frozen inputs | Experimental channel | Kill condition | SHA-256 |
|---|---|---|---|---|---|---|
| Q1 | `Sigma m_nu = 57.5-62.5 meV`, normal ordering | `m3 = v^2/(2(M_P/3^9))`; `m2 = sqrt(max(m3^2-Delta m31^2,0)+Delta m21^2)`; `Sigma=m1+m2+m3`, `m1 in [0,5] meV`; `compute/predict_neutrino_sum.py` | `M_P=1.221e19 GeV`, `v=246.22 GeV`, `Delta m21^2=7.42e-5 eV^2`, `Delta m31^2=2.510e-3 eV^2` | DESI, Euclid, CMB-S4, LiteBIRD; JUNO/DUNE/Hyper-K for ordering | Inverted ordering, robust sum far outside the band after systematics, or a terrestrial `m_nu3` incompatible with the CHO seesaw scale | `acfc9596b509cd0ec9e1a813f44f49bffa573247fbf373cd356d2e74cf32d86d` |
| Q2 | `sin^2(theta23) = 4/7 = 0.571428...` and upper octant | Fano lines avoiding vacuum / all Fano lines; `compute/epsilon_mixing_coefficients.py` | vacuum `omega=(1+i e7)/2`, avoiding lines `4`, total lines `7` | DUNE, Hyper-K, NuFit/global PMNS fits | Stable lower octant or upper-octant value incompatible with `4/7` after global fits settle | `8d50b686829815414cc5847726b32c74fc140cf0dec6d3614782227afa448725` |
| Q3 | `m_betabeta = 1.5-3.7 meV` | `|sin^2(theta12) cos^2(theta13)m2 + exp(i alpha) sin^2(theta13)m3|`, `alpha` free; `compute/forward_predictions.py` | `epsilon0^2=pi/432`, `sin^2(theta12)=1/(3+sqrt(7)epsilon0)`, `sin^2(theta13)=3epsilon0^2`, normal ordering, `m1 ~= 0` | LEGEND-1000, nEXO | Confirmed `0nu beta beta` signal implying `m_betabeta > ~10 meV` | `40ca0216983340e59a3b9f713897179d614118cb21958d33109d02b5ddb464cd` |

**Item 7 — the single sharpest bet (analysis pointer; value unchanged).** Of the positive predictions above, `Q2` (`sin^2 theta23 = 4/7`, upper octant) is staked as the framework's single sharpest falsifiable claim, because it is the ONLY mixing prediction that is both an exact rational AND independent of the open `eps0` (`pi/432`) seam. The dedicated forward-test analysis `compute/theta23_octant_prediction.py` verifies the `eps0`-independence (`d sin^2 theta23 / d eps0 = 0` exactly, versus the moving control `sin^2 theta13 = 3 eps0^2`), shows the octant is the Fano discriminator (the lower-octant mirror is exactly `cos^2 = 3/7`, and `4` avoiding lines `> 3` through-vacuum lines IS "upper octant"), notes it already passed the Item-6 per-row precision test (pull `-0.02`), and cross-checks the frozen `Q2` payload read-only. This is an analysis pointer only: the `Q2` target, inputs, kill condition, and SHA-256 above are unchanged and remain authoritative. The octant being currently unresolved (T2K/NOvA tension) is what makes this a genuine pre-registered bet, decided this decade by DUNE / Hyper-Kamiokande.

## Bridge Sensitivities / Pressure Tests

These are still valuable, but they depend on an unfixed bridge that could move. They are not counted as positive predictions.

| ID | Frozen target | Why sensitivity, not prediction | Experimental channel | Kill / pressure condition | SHA-256 |
|---|---|---|---|---|---|
| B1 | `m_nu3 = 48.86 meV` versus oscillation floor `50.10 meV` | The few-percent lift may come from threshold/RG normalization not yet derived | JUNO, DUNE, Hyper-K, global oscillation fits | Gap grows beyond any few-percent correction without adding a new knob | `c1a30b6a7fffebcb50dd4bb5db759c68ff40e89d9567d3d46d050d62bc3c8a7e` |
| B2 | `kappa_lambda = 1.014` at the CHO matching level | Threshold/RG matching and the Higgs-sector bridge are not fully closed | HL-LHC, FCC-ee/hh, future Higgs factories | Large confirmed `|kappa_lambda-1|` after matching uncertainties settle | `1154d8bc36c30e0ca811d3463a87a13007f232fa23508475a4b04f13f08fc26e` |

Registry manifest digest after the Phase 6 migration:

```text
21cba7701a8292bc96a44d96b7e13b66f6e21fcbd56595257a517ae47875836f
```

## Interpretation Rules

- Do not retune formulas after new measurements. If a target moves, add a dated registry entry and preserve the old hash.
- Separate direct falsification from pressure on a bridge assumption. For example, a shifted Higgs self-coupling first tests threshold matching, while a fourth generation directly attacks the algebraic generation claim.
- Treat null results as consistency checks, not confirmations by themselves; quote the mass/coupling/lifetime window being tested.
- Keep postdictions, positive future predictions, bridge sensitivities, and null exclusions in separate tables in papers and public writeups.
