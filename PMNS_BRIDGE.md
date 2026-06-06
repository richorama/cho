# PMNS Bridge Scaffold

Frozen date: 2026-06-06

Purpose: separate the part of the lepton-mixing bridge that can already be derived from residual TBM symmetries from the broken-triality perturbation that still needs a CHO operator.

## Derived Inside The Scaffold

The PDG-aligned tribimaximal basis is fixed by three orthonormal vectors:

```text
v1 = ( 2, -1,  1) / sqrt(6)
v2 = ( 1,  1, -1) / sqrt(3)
v3 = ( 0,  1,  1) / sqrt(2)
```

These define the tribimaximal mixing matrix `U_TBM`, equivalent to the usual TBM basis up to charged-lepton row rephasings. For any Majorana spectrum `diag(m1, m2, m3)`, the matrix

```text
M_TBM = U_TBM diag(m1, m2, m3) U_TBM^T
```

is invariant under the residual reflections

```text
G_i = 2 v_i v_i^T - I.
```

This gives a genuine matrix derivation of the leading TBM pattern. It does not yet derive the observed deviations.

## Broken-Triality Perturbation Target

The corrected CHO targets are

```text
sin^2(theta13) = 3 epsilon0^2
sin^2(theta12) = 1 / (3 + sqrt(7) epsilon0)
sin^2(theta23) = 4 / 7
Delta m21^2 / Delta m31^2 = 4 epsilon0^2
```

The bridge problem is now:

```text
M_corr = U_corr diag(0, 2 epsilon0, 1) U_corr^T
DeltaM = M_corr - M_TBM
```

Derive `DeltaM` from a broken-triality CHO seesaw operator rather than inserting the corrected angles by hand. A simple cyclic `Z3` action has not yet been shown to be the residual symmetry of this TBM mass matrix; see `OPERATOR_GAP_AUDIT.md`.

## Diagnostic Script

Run:

```bash
python3 compute/pmns_bridge.py
```

The script verifies the TBM residual symmetries, constructs the corrected PMNS target matrix, and prints the perturbation matrix that the future broken-triality operator must produce.
