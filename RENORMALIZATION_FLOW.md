# The Renormalisation Flow Of The Closure Defect

*Interaction is real at every finite resolution and renormalises to zero: the
nearest-neighbour coupling is an irrelevant operator whose fixed point is exactly the
Q01/Q09 non-interacting no-go.*

Gate Q13 relaxed exact autonomy to a bounded misfit — the closure defect — and showed
a single controlled-rotation coupling has defect `4 b^2`, so interaction survives
coarse-graining approximately. Gate Q14 asks the decisive follow-up: under *repeated*
coarse-graining, does a fixed coupling grow (relevant), persist (marginal), or wash out
(irrelevant)? The answer is exact and clean.

Certified by `tests/test_gate_q14_renormalization_flow.py`; censuses in
`amplitude_bootstrap/renormalization_flow.py`.

## 1. Setup

A chain of `n` qubits carries a translation-invariant nearest-neighbour coupling
`CROT(a, b) = |0><0| (x) I + |1><1| (x) R(a, b)` between each adjacent pair, with
`R(a, b) = [[a, -b], [b, a]]` and `a^2 + b^2 = 1` (exactly unitary over `Q(i)`). The
chain is coarse-grained by tracing the end qubit, then the end qubit of the resulting
effective channel, and so on — the honest spatial recursion of Gate Q06 — recording the
exact least-squares closure defect `d_k` at each level `k`.

## 2. Exact defect vectors

```text
n = 3, b = 3/5 :  d = (144/25, 576/625)
n = 4, b = 3/5 :  d = (576/25, 2304/625, 576/625)
```

Zero coupling gives the all-zero vector: the non-interacting product is exactly
autonomous under the whole recursion (the fixed point). For `b > 0` every `d_k > 0`:
Q13's approximate interaction persists at every finite scale.

## 3. The renormalisation law

The step-to-step contraction ratios are exact and universal:

```text
d_2 / d_1 = a^2 / 4        (the boundary step, across the coupled cut)
d_{k+1} / d_k = 1/4        (every deeper step)
```

Both are `<= 1/4 < 1`, so the defect **contracts by at least a factor of four at every
coarse-graining step** and decays geometrically to zero. The coupling is an
**irrelevant operator**; the coarse world flows to the non-interacting, autonomous
fixed point.

This is the structural payoff: it *derives* the Gate Q01/Q09 exact no-go
("observer-consistent amplitude dynamics are non-interacting") as the **endpoint of a
renormalisation flow**, not as a brute enumeration. Interaction is genuine at every
finite resolution — the amplitude premise really does buy approximate interacting
dynamics — but the observer-consistency defect renormalises it away, so a sufficiently
coarse observer sees a non-interacting world. Classicality is the deep-recursion limit.

## 4. Scope and non-claims

- The defect is the misfit of the best *linear* surrogate, so it lower-bounds the
  best-*channel* misfit; the contraction statement is therefore conservative.
- The flow is exact for the declared controlled-rotation coupling on chains of length
  three and four, traced from the end. The boundary ratio `a^2/4` and deep ratio `1/4`
  are verified over the Pythagorean couplings `b in {3/5, 5/13, 7/25}`.
- Irrelevance is a statement about *this* coupling and blocking. The open target is a
  relevant or marginal coupling: a nonzero interaction whose defect does **not**
  contract under recursion would be the first candidate for genuinely emergent
  interacting physics in this crucible. None has been found here — consistent with, and
  now explaining, the campaign's non-interacting verdict.

## Reproducibility

```bash
python3 -m unittest discover -s tests -p "test_gate_q14*.py" -v
```
