# Approximate Closure And The Coupling Flow

*Relaxing exact autonomy to bounded misfit: interaction is observer-consistent
approximately, at a quantified cost that flows to zero with the coupling.*

This note records Gate Q13, the first extension past the campaign's central wall.
Gates Q01 and Q09 proved an **exact** no-go: under the partial trace, a two-qubit
unitary admits an exact autonomous coarse law only for the 36 non-interacting
product unitaries; every entangler fails outright, so "observer-consistent
amplitude dynamics are non-interacting". But that verdict is a property of demanding
*exact* closure. Real renormalised dynamics is never exactly autonomous — only
autonomous up to a controlled error. Q13 measures that error exactly.

The gate is certified by `tests/test_gate_q13_approximate_closure.py`; the exact
censuses live in `amplitude_bootstrap/approximate_closure.py`.

## 1. The closure defect

For a microscopic unitary `U` and the partial trace `B`, form the two
coarse-by-fine superoperators over `Q(i)`:

```text
T = B                 (trace)             : fine operator -> coarse operator
M = B . U(.)U^dagger  (evolve then trace) : fine operator -> coarse operator
```

An exact autonomous channel is a map `E` with `E T = M`. When none exists, take the
exact least-squares surrogate `E* = M T^dagger (T T^dagger)^{-1}` (the Gram matrix
`T T^dagger` is `4x4` and full rank, so `E*` is unique) and define the

```text
closure defect(U) = || M - E* T ||_F^2 = sum_ij |(M - E* T)_ij|^2   in  Q_{>=0}.
```

Everything is an exact rational. Because channels are a subset of linear maps, the
defect is a **lower bound** on the misfit of any autonomous *channel*: if
`defect(U) > eps` then no autonomous coarse law reproduces `U` to Frobenius error
`eps`. The defect is measured in a fixed declared operator-basis convention; its
zero set, ordering, invariances, and scaling law are convention-independent.

## 2. The exact no-go is the `eps -> 0` limit

`defect(U) == 0` holds **exactly for the 36 product unitaries** and `defect(U) > 0`
for all 108 entanglers, agreeing with `reduced_channel` everywhere. So Q13 contains
Q01 as its zero-tolerance limit. Raising the declared tolerance `eps` admits
interaction monotonically:

| `eps` | survivors | interacting |
|------:|----------:|------------:|
| 0     | 36        | 0           |
| 4     | 108       | 72          |
| 6     | 144       | 108         |

Closure is a matter of **budget, not impossibility**. This is the sense in which the
exact no-go was an artefact of exactness.

## 3. The defect is a local-unitary invariant

The defect depends only on the entangler, not on the local dressing: all 36 local
dressings of `CZ`, of `CNOT`, and of `SWAP` share one value.

```text
local: 0      cz: 4      cnot: 4      swap: 6
```

`SWAP`, which fully exchanges system and environment, is the least autonomous. The
defect therefore reads off the genuinely non-local content of the interaction — the
right kind of quantity for a renormalisation-relevant coupling.

## 4. The coupling flow: `defect = 4 b^2`

On the exactly-unitary controlled-rotation family
`CROT(a, b) = |0><0| (x) I + |1><1| (x) R(a, b)` with `R = [[a, -b], [b, a]]`,
`a^2 + b^2 = 1`, the closure defect is exactly

```text
defect(CROT(a, b)) = 4 b^2,
```

verified over the Pythagorean couplings `b in {0, 9/41, 7/25, 5/13, 3/5, 4/5}`. The
defect vanishes at zero coupling, is strictly increasing in `b`, and flows to zero
**quadratically** as `b -> 0`. Weakly interacting microscopic dynamics is
approximately autonomous, with the residual controlled at leading order by the
square of the coupling — the perturbative scaling an effective-theory picture
predicts.

## 5. Scope and non-claims

- The defect is the misfit of the best *linear* surrogate; the tighter best-*channel*
  misfit is at least as large, so all "no autonomous law within `eps`" statements are
  conservative.
- Q13 shows interaction survives *approximate* closure and identifies an exact
  quadratic coupling law; it does **not** yet exhibit a scaling *limit* in system size,
  a fixed point of iterated coarse-graining, or emergent records. Those remain the
  open targets: iterate the blocking on longer chains and ask whether the defect of a
  fixed coupling flows toward zero (irrelevant), a constant (marginal), or growth
  (relevant) under recursion.
- As with every gate, the production module computes only exact censuses; the test
  owns all expected values.

## Reproducibility

```bash
python3 -m unittest discover -s tests -p "test_gate_q13*.py" -v
```
