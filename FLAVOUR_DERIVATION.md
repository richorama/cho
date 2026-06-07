# Flavour Derivation Scaffold

Frozen date: 2026-06-06

This note describes `compute/flavour_derivation.py`, the first bridge artifact after the derivation ledger. Its purpose is to turn the flavour sector from a list of successful formulas into a small derivation engine with explicit inputs, matrices, and remaining proof obligations.

For the shared triality-breaking quantity itself, see `EPSILON_BRIDGE.md` and `compute/epsilon_bridge.py`. Those artifacts isolate the separate proof target for deriving `epsilon0^2 = pi / 432` as an operator trace or transition amplitude.

For the charged-sector operator target, see `YUKAWA_BRIDGE.md` and `compute/yukawa_bridge.py`. For the neutrino-mixing operator target, see `PMNS_BRIDGE.md` and `compute/pmns_bridge.py`. The unified candidate operator that collects both is `CHO_OPERATOR.md` with `compute/cho_bridge_operator.py`.

For the remaining blockers in that candidate, see `OPERATOR_GAP_AUDIT.md` and `compute/operator_gap_audit.py`.

For the partial sector-rank derivation from the complex-octonion Fock grades, see `compute/sector_projector_derivation.py`.

## Goal

The scaffold starts from CHO algebraic data only:

- `epsilon0^2 = pi / (16 * 27)` from the epsilon bridge trace target
- `N_color = 3`
- `dim(O) = 8`
- `dim(Im O) = 7`
- `sin^2(theta_W)_tree = 1/4`
- `delta_Fano = arccos(1/3)`
- triality nearest-neighbor rule: `M13 = 0`

Experimental values are isolated in a final comparison dictionary and are not used to derive the predictions.

## What It Builds

1. **Charged-sector NNI bridge rules**

   For each sector, the script derives dimensionless ratios normalized by the third-generation mass:

   | Sector | `m2/m3` | `|A/C|^2` | `m1/m3` |
   |---|---:|---:|---:|
   | up | `epsilon0^2` | `1/4` | `(1/4) epsilon0^4` |
   | down | `3 epsilon0^2` | `9/4` | `(9/4)(3 epsilon0^2)^2` |
   | lepton | `8 epsilon0^2` | `1/(4 pi)` | `(1/(4 pi))(8 epsilon0^2)^2` |

   It also constructs minimal adjacent-transition matrices with `M13 = 0` and `|A/C|^2` equal to the sector bridge rule. These matrices are diagnostic: they encode the bridge rule, but they are not yet claimed to be the final CHO Yukawa operator.

2. **CKM unitary scaffold**

   The script constructs a PDG-parameterized CKM matrix from:

   - `|V_us| = sqrt(7) epsilon0`
   - `|V_cb| = epsilon0 / 2`
   - `|V_ub| = (sqrt(2) - 1) |V_us| |V_cb|`
   - `delta = arccos(1/3)`

   This reproduces the CKM magnitudes. The Jarlskog value from this simple PDG phase placement is intentionally reported separately because Paper 2's `J = 3.01e-5` requires the full NNI phase placement. That is now an explicit proof obligation instead of an implicit step.

3. **PMNS unitary scaffold**

   The script constructs a corrected-TBM PMNS matrix from:

   - `sin^2(theta13) = 3 epsilon0^2`
   - `sin^2(theta12) = 1 / (3 + sqrt(7) epsilon0)`
   - `sin^2(theta23) = 4/7`
   - `delta_PMNS = pi + arccos(1/3)` as a scaffold convention

## How To Run

```bash
python3 compute/flavour_derivation.py
```

The script prints algebraic inputs, charged-sector NNI bridge tables, diagnostic nearest-neighbor matrices, CKM magnitudes and unitary matrix, and PMNS angles and unitary matrix.

## Current Bridge Status

This scaffold improves the project in two ways:

- It makes the first-generation NNI factors local and auditable instead of scattered through prose and summary scripts.
- It separates the CKM magnitude success from the still-open CKM phase-placement proof for the Jarlskog invariant.

Ledger implications:

- M9-M11 are `Open bridge / scaffolded`: the cascade relation is explicit, while the sector shape factors still need the CHO Yukawa operator. **Update:** `compute/epsilon_mixing_coefficients.py` now derives the mixing multiplicities `(7, 3, 4, 4/7)` as Fano-line counts (all lines / lines through the vacuum `e7` / lines avoiding it) and identifies the lepton `1/(4 pi)` shape factor as the uniform measure on the transition Bloch sphere `S^2` (`Int dOmega = 4 pi`) — advancing M11; the dynamical reduction of the lepton trace to that measure remains open. **Further:** `compute/epsilon_vcb_halfangle.py` then derives the `|V_cb|` coefficient `1/2` as the `SU(2)` spinor half-angle `sin(eps0/2)` (vector-vs-spinor against the `sqrt(7)` `Im(O)` channel of `|V_us|`; finite avatar `tan(pi/8) = sqrt(2)-1`, which is also the `C3` `|V_ub|` factor), closing C2 down to the channel assignment.
- C1-C3 are implemented as a CKM unitary scaffold.
- C4 remains open at the operator level because the simple PDG phase placement does not yet reproduce the Paper 2 Jarlskog target.
- N2-N5 are implemented as a PMNS unitary scaffold, but still need a broken-triality seesaw matrix derivation and a clarified residual symmetry.

## Next Proof Target

The next proof should promote the candidate operator in `CHO_OPERATOR.md` into a real CHO Yukawa operator:

```text
Y_f : ideal_i x Higgs x ideal_j -> scalar
```

That operator should derive all of the following in one construction:

- `M13 = 0`
- sector factors `1`, `N_c^2`, and `1/pi`
- CKM phase placement yielding `J = 3.01e-5`
- corrected PMNS angles from a broken-triality seesaw matrix
