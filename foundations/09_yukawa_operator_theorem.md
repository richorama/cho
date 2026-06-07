# Yukawa/Seesaw Operator Theorem Gate

Created: 2026-06-07

Status: **Phase 3 integration gate, not a closed theorem.** This note states what it would mean for CHO to derive the flavour sector from one operator. The companion machine witness is [compute/yukawa_operator_full.py](../compute/yukawa_operator_full.py).

## 1. Target Theorem

The desired theorem is that a single CHO operator

```text
O_CHO = (H_triality, P_sector, W_H, A_gen, Phi_Fano, Y_nu)
```

is forced by the algebra/action and, after one charged-sector diagonalization plus one seesaw construction, produces:

1. charged-sector matrices for up, down, and charged leptons;
2. the NNI/cascade structure, including the first-generation factors `1/4`, `9/4`, and `1/(4*pi)`;
3. CKM magnitudes `|V_us|`, `|V_cb|`, `|V_ub|` and the Jarlskog invariant from the same charged matrices;
4. PMNS deviations from TBM, the seesaw perturbation, and the neutrino splitting ratio;
5. a parameter ledger saying which quantities are derived, selected, or still open.

## 2. Current Executable Gate

[compute/yukawa_operator_full.py](../compute/yukawa_operator_full.py) wraps the existing composite operator from `compute/cho_bridge_operator.py` and prints four audit sections:

1. **Component ledger:** `epsilon0^2`, generation adjacency, sector ranks, weak shape, lepton sphere factor, Fano phase, and PMNS perturbation status.
2. **Charged matrices:** dimensionless NNI/Fritzsch matrices for up, down, and lepton sectors with the predicted cascade spectra.
3. **CKM gate:** strict CKM from one charged-Yukawa diagonalization, compared with the separate CKM magnitude projection.
4. **PMNS/seesaw gate:** corrected-TBM target angles and the explicit `DeltaY` / `DeltaM` perturbation norms.

The current verdict is intentionally conservative:

```text
AUDIT STATUS: PASS
THEOREM STATUS: OPEN
```

That means the executable gate is coherent and useful, but the flavour theorem is not closed.

## 3. What Is Already Useful

The current integration gate improves the old scaffold in three ways.

1. The charged-sector matrices are explicit objects, not prose targets.
2. The CKM problem is localized: the strict charged-matrix diagonalization gets a reasonable Jarlskog value but does not yet reconcile all magnitudes; the separate magnitude projection is closer numerically but is not one mass-matrix diagonalization.
3. The PMNS perturbation is explicit as `DeltaY` / `DeltaM`, so a future broken-triality operator has a concrete target.

## 4. What Remains Open

The theorem is open for exactly the reasons printed by the gate:

1. **Sector selection:** the ranks `1`, `3`, and `8` are supported as Fock traces, but the final CHO Yukawa trilinear has not been shown to select them dynamically.
2. **Weak/lepton shapes:** `1/4`, `9/4`, and `1/(4*pi)` remain operator/action targets, even though their geometric interpretations have improved.
3. **CKM one-diagonalization:** one charged-matrix diagonalization must produce `|V_us|`, `|V_cb|`, `|V_ub|`, and `J` together.
4. **PMNS dynamics:** `DeltaY` is still constructed from corrected target angles, not derived from broken triality.
5. **Epsilon measure:** Phase 2 leaves the normalized transition-measure hypothesis open, so the common spurion remains `GEOMETRIC`, not `DERIVED`.

## 5. Kill / Demotion Condition

If no one-operator construction can reconcile CKM magnitudes with the Fano-phase Jarlskog placement, then C4 and dependent CKM claims must remain open bridge claims. If PMNS continues to require target-angle insertion, N2-N5 remain scaffolded/count-level rather than matrix-derived.

The useful next technical move is not another formula. It is a structural deformation of the charged-Yukawa matrices that either closes the CKM gate or proves that the current Fano-phase placement cannot coexist with the corrected magnitudes.
