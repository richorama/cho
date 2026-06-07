# The Physics Map: One-Generation Quantum Numbers and Anomalies

Created: 2026-06-07

Status: **partial closure of the algebra-to-physics map.** This note freezes the current map for one Standard Model generation and records exactly what is machine-checked. It closes the quantum-number/anomaly bookkeeping layer. It does **not** close the functorial map from the generation idempotents into `T(OP2)`, the Dirac/Yukawa operator, or the mass spectrum.

Companion witness: [compute/physics_map_audit.py](../compute/physics_map_audit.py).

## 1. Domain And Convention

The internal algebraic input is still

```text
A = C x H x O.
```

The one-generation charge module is the complex octonion ideal `C x O`, as in the Furey/Dubois-Violette construction reproduced numerically by `compute/ladder_charges.py`. The weak-isospin module is the quaternionic factor `H`, as in `compute/weak_isospin_hypercharge.py`. The chiral doublet/singlet split is implemented by the charge-aligned KO-6 idempotent of `compute/chiral_projector.py`.

The table below lists physical left- and right-handed Weyl fields. For anomaly sums, right-handed fields enter with the opposite sign, equivalently as left-handed conjugates. Hypercharge uses the convention

```text
Q = T3 + Y/2,    so    Y = 2(Q - T3).
```

## 2. Frozen One-Generation Table

| field | gen | chirality | SU(3) | SU(2) | multiplicity | Q | T3 | Y |
|---|---:|---|---|---|---:|---:|---:|---:|
| `u_L` | 1 | L | 3 | 2 | 3 | `+2/3` | `+1/2` | `+1/3` |
| `d_L` | 1 | L | 3 | 2 | 3 | `-1/3` | `-1/2` | `+1/3` |
| `nu_L` | 1 | L | 1 | 2 | 1 | `0` | `+1/2` | `-1` |
| `e_L` | 1 | L | 1 | 2 | 1 | `-1` | `-1/2` | `-1` |
| `u_R` | 1 | R | 3 | 1 | 3 | `+2/3` | `0` | `+4/3` |
| `d_R` | 1 | R | 3 | 1 | 3 | `-1/3` | `0` | `-2/3` |
| `e_R` | 1 | R | 1 | 1 | 1 | `-1` | `0` | `-2` |
| `nu_R` | 1 | R | 1 | 1 | 1 | `0` | `0` | `0` |

Total: `16` Weyl states including a sterile `nu_R`.

## 3. What Is Algebraic Here

The machine witness checks four layers.

1. `compute/ladder_charges.py` supplies the electric-charge magnitudes `{0, 1/3, 2/3, 1}` with multiplicities `(1, 3, 3, 1)` from the `C x O` number operator.
2. `compute/weak_isospin_hypercharge.py` supplies weak `SU(2)` from the quaternionic `H` factor, with `T3 = +/-1/2`, and verifies `Y = 2(Q - T3)`.
3. `compute/chiral_projector.py` supplies one charge-aligned KO-6 idempotent so weak generators act as doublets on one chirality and singlets on the other while `[Q, gamma_Q] = 0`.
4. `compute/physics_map_audit.py` ties these into the frozen table and checks anomaly cancellation.

This is the intended public wording: **the one-generation gauge quantum-number map is anomaly-clean and algebraically supported.** Do not upgrade that sentence to a mass-spectrum claim.

## 4. Anomaly Cancellation

With the physical left/right convention described above, the witness computes:

```text
SU(3)^2 U(1) = 0
SU(2)^2 U(1) = 0
U(1)^3       = 0
grav^2 U(1) = 0
```

It also checks the global Witten anomaly condition: there are four left-handed `SU(2)` doublets per generation (three coloured quark doublets plus one lepton doublet), an even number.

This matters because anomaly cancellation is a hard consistency filter. A table that reproduces charges but fails these sums is not a viable Standard Model generation.

## 5. Remaining Residuals

This note does not close every part of Phase 1.

Open items:

1. **Generation content map:** show functorially how three copies of this one-generation map sit on the three `J3(O)` frame idempotents / `T(OP2)` tangent spinors.
2. **Antiparticle bookkeeping:** state the conjugate ideal and charge-conjugation map at the same level of explicitness.
3. **Dirac/Yukawa domain:** define the allowed mass operators before using them to fit or derive masses.
4. **Scale map:** classify which mass scales are algebraic, Planck-input, or continuum/RG matched.

The next most valuable deliverable is the Dirac/Yukawa domain, because it feeds directly into the one-operator and content-map tracks in [ROBUSTNESS_ACTIONS.md](../ROBUSTNESS_ACTIONS.md).

## 6. Falsifier

If the charge-aligned table cannot be embedded into the three-generation idempotent-frame module without per-field choices, then the current `N_gen = 3` result remains a count/chirality result only, not a full Standard Model generation derivation.