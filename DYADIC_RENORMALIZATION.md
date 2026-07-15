# Dyadic Renormalization Of Reversible Affine Dynamics

## Scope

This campaign extends the affine sufficiency theorem from one factor-two step
to an exact hierarchy of dyadic scales. It does not enlarge the microscopic
rule class or revive the physical interpretation campaign.

Let

```text
x[t+1] = A x[t] XOR x[t-1] XOR a0,
A = al*S^-1 + ac*I + ar*S,
```

and let `b = 2^k`, with `k >= 1`. Partition the lattice into blocks of `b`
sites. A nonconstant affine block observer has the form

```text
B(x)[j] = d XOR XOR_q w[q] * x[b*j + q],
```

where the binary weight vector `w` is nonzero. Sample microscopic trajectories
at times `t`, `t+b`, and `t+2b`.

## Theorem

Every affine elementary rule induces an exact reversible radius-one trajectory
law under every nonconstant affine block observer at every dyadic scale `b`.
The effective linear coefficients are unchanged:

```text
(al, ac, ar) -> (al, ac, ar).
```

Writing `s = al XOR ac XOR ar` and `p = XOR_q w[q]`, the effective constant is

```text
a0' = s * (a0*p XOR d).
```

This includes left decimation (`d=0`, `p=1`) and block parity (`d=0`, with `p`
equal to the parity of `b`). Since every allowed `b` is even, block parity
removes the constant field.

## Symbolic Proof

For the homogeneous recurrence, sampled trajectories are governed by operator
polynomials

```text
P[0](A) = 0,
P[1](A) = A,
P[m+1](A) = A*P[m](A) XOR P[m-1](A).
```

Repeated squaring in characteristic two gives

```text
P[b](A) = A^b
        = al*S^-b + ac*I + ar*S^b
```

for every dyadic `b`. The three shifts become the left, center, and right
coarse sites after blocking. Eliminating the intermediate slices also leaves
the constant field `A^(b-1)(a0)`. On a uniform field, `A` acts by multiplication
by `s`; since `b-1` is positive, this contributes `s*a0`. Applying the affine
observer and rewriting the result in terms of the observed current state gives
the stated constant `s*(a0*p XOR d)`.

The Laurent-polynomial recurrence is implemented by
`sampled_affine_operator_terms`. Direct microscopic evolution independently
checks all 16 affine rules at scales `2`, `4`, and `8`. Every nonconstant affine
observer at block sizes `2` and `4` is checked on an affine basis of the full
two-time microscopic state space.

## Fixed Points And Two-Cycles

For a fixed observer, repeated dyadic coarse-graining changes only `a0` by

```text
T(a0) = s*(p*a0 XOR d).
```

If `s*p*d = 0`, the effective rule is a fixed point after at most one step. If
`s = p = d = 1`, then `T(a0) = a0 XOR 1`, so the two rules differing only in
their constant term form a two-cycle. No longer affine RG orbit occurs.

The original zero-offset decimation and parity observers therefore stabilize
after one step. Complemented odd-weight observers supply the only short cycles.

## Non-Dyadic Control

The dyadic restriction is structural. For additive rule `150`, whose operator
is `S^-1 + I + S`, temporal stride three gives

```text
P[3](A) = S^-3 + S^-2 + S^-1 + S + S^2 + S^3.
```

The shifts by one and two microscopic sites are not aligned with blocks of
three, so the dyadic radius-one argument does not apply. This is an explicit
control against treating matched spatial and temporal rescaling alone as
sufficient. It is not a classification of all non-dyadic rules or observers.

The control is strengthened to an exact necessity theorem in
[INTEGER_SCALE_CLASSIFICATION.md](INTEGER_SCALE_CLASSIFICATION.md): rule `60`
provides a hidden non-block-aligned shift at every non-power-of-two scale.

## Relation To Gate 06

Gate 06 supplies necessity: every non-affine elementary rule already has a
size-six decimation obstruction at the first dyadic scale. Gate 07 supplies the
all-scale affine hierarchy. Together they show that the universal factor-two
classification is not an isolated census artifact: its surviving family is
closed under every subsequent dyadic rescaling.

No claim is made about nonlinear block observers beyond the size-six pair-map
audit, or about larger-radius effective laws, records, observers, or physics.
