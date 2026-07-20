# The Interaction-Relevance Sweep

*No coupling escapes the flow: a broad family of exactly-unitary entangling generators
is genuinely interacting yet universally irrelevant. Interaction spreads under depth but
never becomes relevant, because pure decimation dilutes the defect by the Hilbert
dimension of the traced factor.*

Gate Q14 showed one coupling (the controlled rotation) is irrelevant: its closure defect
renormalises to zero. Gate Q15 asks whether *any* coupling escapes that flow. A marginal
or relevant coupling — a defect that stays constant or grows under recursion — would be
the first candidate for genuinely emergent interacting physics in this crucible.

Certified by `tests/test_gate_q15_interaction_relevance.py`; censuses in
`amplitude_bootstrap/interaction_relevance.py`.

## 1. The sweep

A declared family of seven exactly-unitary, genuinely entangling two-qubit generators
over `Q(i)` — `CNOT`, `CZ`, `SWAP`, `iSWAP`, `CS` (controlled-`S`), `CROT` (controlled
Pythagorean rotation), and `DCNOT = CNOT.SWAP` — is each laid down as a
translation-invariant nearest-neighbour coupling on a chain, optionally repeated to
depth `t`, and coarse-grained by tracing the end qubit repeatedly. Each defect flow is
classified by its largest step ratio: `< 1` irrelevant, `= 1` marginal, `> 1` relevant.

## 2. Every generator is interacting yet irrelevant

At depth one on a three-qubit chain:

```text
cnot  : (16,    0)        irrelevant   reach 1
cz    : (16,    4)        irrelevant   reach 2
swap  : (24,    0)        irrelevant   reach 1
iswap : (24,    0)        irrelevant   reach 1
cs    : (8,     2)        irrelevant   reach 2
crot  : (144/25, 576/625) irrelevant   reach 2
dcnot : (24,    0)        irrelevant   reach 1
```

Every generator has a strictly positive level-one defect (it is genuinely interacting)
and a flow that contracts to zero. **No member is marginal or relevant.** The
non-interacting product control is an exact fixed point (all-zero flow).

## 3. Depth spreads interaction but does not make it relevant

`iSWAP` is a clean light-cone witness. On a four-qubit chain the number of
coarse-graining steps its defect survives grows one-for-one with the circuit depth:

```text
depth 1 -> reach 1        (96, 0, 0)
depth 2 -> reach 2        (96, 6, 0)
depth 3 -> reach 3        (96, 24, 6)
```

The coupling transports correlations further under time, so the interaction becomes
visible after more traces. Yet each spatial decimation still contracts the defect, so
`iSWAP` stays irrelevant at every depth.

## 4. Why nothing escapes: dimensional dilution

The deep-recursion contraction is set by the Hilbert dimension of the traced factor — a
step ratio of `1/4 = 1/2^2` per qubit. Pure decimation therefore always dilutes an
interaction; it can never sustain one. A relevant coupling would require a
coarse-graining that **compensates** this dimensional dilution (a genuine block-spin
rescaling, not a bare partial trace). Q15 makes that missing ingredient precise: within
the project's decimation discipline, observer-consistency forces every interaction to
renormalise away, exactly matching — and now explaining — the campaign's non-interacting
verdict.

## 5. Scope and non-claims

- The defect is the best *linear* surrogate's misfit, so it lower-bounds the
  best-*channel* misfit; the "irrelevant" verdicts are conservative.
- The sweep is exact over the declared seven-generator family, chains of length three and
  four, and depths one to three. It is decisive for that crucible; it is not a proof that
  no coupling whatsoever, under any coarse-graining, can be relevant.
- The open target is unchanged and now sharper: a coarse-graining that compensates the
  dimensional dilution (block-spin with rescaling) is the natural next premise to test
  for a relevant coupling and genuinely emergent interacting dynamics.

## Reproducibility

```bash
python3 -m unittest discover -s tests -p "test_gate_q15*.py" -v
```
