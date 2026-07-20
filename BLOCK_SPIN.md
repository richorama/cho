# Block-Spin Coarse-Graining

*Replacing the partial trace by an isometric block-spin does not rescue interaction. A
single blocking can even beat the trace — `CZ` becomes exactly autonomous where
decimation leaves a defect — yet under the flow every coupling still contracts to the
non-interacting fixed point. The fixed point survives a second, inequivalent,
dimension-reducing coarse-graining.*

Gate Q15 blamed interaction-irrelevance on the *dimensional dilution* of a bare
decimation: tracing out a qubit shrinks the closure defect by the Hilbert dimension of
the discarded factor, so no coupling can be relevant. The obvious objection is that the
partial trace is a crude blocking — it throws structure away. A **block-spin** merges two
qubits into one effective qubit through an isometry `w` (`w†w = I`), a genuine scale
transformation chosen to *keep* structure. Does some isometry sustain an interaction?

Certified by `tests/test_gate_q16_block_spin.py`; censuses in
`amplitude_bootstrap/block_spin.py`.

## 1. The block-spin

For a microscopic operator `O` the block-spin map is `B_w(O) = w† O w`, with `w` a `4×2`
isometry embedding one coarse qubit into two fine qubits. On a chain a layer
`W = w ⊗ w ⊗ …` merges every pair. The exact least-squares closure defect (Gate Q13) is
measured at each level. A declared family of six exact isometries over `Q(i)` is swept —
`keep` (force environment to `|0⟩`), `ghz` (aligned embedding), `sym` (Pythagorean
superposition), `bell` (real rotation of the `{|00⟩,|11⟩}` plane), `phase` (a complex
`Q(i)` superposition), and `gen` (a generic retained subspace) — against the couplings
`CZ`, `CNOT`, and `CROT`.

## 2. Block-spin is inequivalent to decimation

Under decimation `CZ` has closure defect `4` (Gate Q13). Under block-spin it is *exactly
autonomous* — defect `0` — for every computational-basis isometry:

```text
CZ single-block defect:  keep 0   ghz 0   sym 0   bell 0   phase 0   gen 1108224/390625
```

A single blocking gives an autonomy the trace cannot: block-spin is a structurally
distinct coarse-graining, not a repackaged partial trace. The generic isometry `gen`
reintroduces a positive defect, so this autonomy is a property of the *aligned* subfamily,
not of every blocking — but its mere existence certifies the inequivalence.

## 3. Interaction is still universally irrelevant

The two-level block-spin flow on a four-qubit chain contracts at every step for every
`(coupling, isometry)` pair. Across the whole 18-pair sweep the worst contraction ratio
is

```text
worst ratio = 5215972980711164182368 / 46456577684866181640625  ≈  0.112  <  1   (crot, gen)
```

Every pair is classified `irrelevant` (or `fixed_point` where the defect is already
zero). **No isometry makes any coupling marginal or relevant.**

## 4. The fixed point is robust

The non-interacting fixed point of Gates Q01/Q09/Q14/Q15 survives a second, inequivalent,
dimension-reducing coarse-graining. Interaction-irrelevance is therefore not an artefact
of the partial trace: it is a property of dimensional reduction itself. Any coarse-graining
that maps two qubits to one dilutes the defect, and the dilution wins.

## 5. Scope and the remaining escape route

This gate does not claim that *no* coarse-graining sustains interaction. It shows that
neither bare decimation (Q15) nor isometric block-spin (Q16) — the two natural
*dimension-reducing* blockings — does so. The one premise this crucible has not yet
changed is a **MERA-style entangling disentangler applied before blocking**: a unitary
that redistributes correlations across the cut so the surviving qubit inherits, rather
than loses, the interaction. That is a genuinely larger premise, and the natural next
gate.
