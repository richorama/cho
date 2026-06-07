# Epsilon Measure Theorem Gate

Created: 2026-06-07

Status: **conditional theorem gate, not a scoreboard promotion.** This note is now the live F0 target in [ROBUSTNESS_ACTIONS.md](../ROBUSTNESS_ACTIONS.md). It states the strongest current form of the `epsilon0^2 = pi/432` bridge as one normalized transition-trace theorem with named hypotheses. The companion audit is [compute/epsilon_measure_audit.py](../compute/epsilon_measure_audit.py).

## 1. Target Statement

The desired theorem is not three separate facts `pi`, `16`, and `27`. It is one measure statement:

```text
epsilon0^2 = Tr_transition / dim_phase_space
           = (pi * rank(P_transition)) / (dim(A_Weyl) * dim(J3(O)))
           = pi / (16 * 27).
```

The key distinction is whether the normalized transition trace is forced by the CHO action and representation category, or merely chosen after observing the successful hierarchy.

## 2. Named Hypotheses

| code | hypothesis | present status |
|---|---|---|
| H1 | The transition phase space is `A_Weyl x J3(O)`, dimensions `16 x 27` | Strong geometric support: `16 = T(OP2) = Delta9`, `27 = dim J3(O)`, and the gauge/flavour `Spin(9)` seam is reduced to a frame choice |
| H2 | `P_transition` is primitive rank one | Supported by [compute/epsilon_rank_one_kernel.py](../compute/epsilon_rank_one_kernel.py): primitive = rank one = pure single-generation idempotent |
| H3 | The angular weight is the Berry half-turn `pi` | Supported by the action/free-action/two-level audits; residual is the microscopic origin of the `A4` flavour symmetry |
| H4 | The measure is the normalized invariant transition trace on the product | **Open live theorem hypothesis** |
| H5 | The same transition operator feeds the eventual Yukawa/seesaw construction | Open to Phase 3 |

Under H1-H4 the trace computation is immediate:

```text
dim(A_Weyl x J3(O)) = 16 * 27 = 432
rank(P_transition)  = 1
theta               = pi
Tr_transition       = pi

epsilon0^2          = pi / 432.
```

H5 is not needed to compute the number, but it is needed before the mass and mixing uses of `epsilon0` become one-operator derivations.

## 3. Nearby Alternatives

[compute/epsilon_measure_audit.py](../compute/epsilon_measure_audit.py) checks the target against nearby alternatives:

| alternative | why it fails |
|---|---|
| rank-2 or rank-3 kernel | violates primitive rank-one purity; switches on multiple generations at once |
| `OP2` alone | drops the ambient Jordan trace |
| `J3(O)` alone | drops the Weyl/tangent spinor factor |
| real algebra `64 x 27` | averages over the real algebra instead of the chiral Weyl module |
| `16 x 26` traceless Jordan | drops the unit/trace direction of `J3(O)` |
| raw reciprocal `1/432` | removes the Berry holonomy |
| full turn `2pi/432` | uses the wrong minimal path |
| Fano pair degeneracy `21*pi/432` | counts one automorphism orbit as 21 independent channels |
| sphere area `4pi/432` | uses unnormalized area instead of normalized transition measure |

This is a useful narrowing: the alternatives fail by named structural criteria rather than by being numerically unattractive.

## 4. What Remains To Prove

The live theorem is H4:

```text
The CHO action induces the normalized invariant transition trace on
A_Weyl x J3(O), with no extra density, stabilizer volume, orbit multiplicity,
or continuous parameter.
```

A complete proof should define:

1. the exact transition bundle or quotient whose fibres are being traced;
2. the invariant measure or symplectic volume form;
3. the normalization convention and why it is forced;
4. the role of the stabilizer/orbit quotient;
5. why no additional density appears from the Yukawa/seesaw operator domain.

Until that proof exists, `epsilon0^2 = pi/432` should stay in the `GEOMETRIC` bucket of [compute/model_complexity.py](../compute/model_complexity.py), not the `DERIVED` bucket.

## 5. Kill Condition

If H4 cannot be derived, demote `epsilon0^2 = pi/432` from `GEOMETRIC` to `CHOSEN` in [compute/model_complexity.py](../compute/model_complexity.py) and let [compute/scoreboard.py](../compute/scoreboard.py) report the Bayes-factor cost. If H4 is proven and H5 later succeeds, promote only then, with the proof and operator audit cited in [DERIVATION_LEDGER.md](../DERIVATION_LEDGER.md).
