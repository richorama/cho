# Exact Integer-Scale Classification

## Scope

This theorem classifies the matched spatial and temporal scales at which the
entire affine elementary-rule family admits autonomous radius-one laws under
every nonconstant affine block observer. It completes the scale question left
open by the dyadic sufficiency theorem.

The classification is stated on the infinite lattice, or equivalently on all
sufficiently large periodic rings whose block sites and witness sites do not
alias. It concerns exact laws, not approximate closure.

## Theorem

Let `m >= 2` be an integer. Partition space into blocks of `m` sites and sample
time every `m` microscopic steps. The following are equivalent:

1. every affine elementary rule induces an exact reversible radius-one law
   under every nonconstant affine block functional;
2. every affine sampled operator is aligned with the block lattice;
3. `m` is a power of two.

Thus dyadic scales are not merely sufficient. They are exactly the universal
matched scales for the affine family.

## Sampled Trace Polynomials

For the homogeneous reversible recurrence, define

```text
P[0](A) = 0,
P[1](A) = A,
P[m+1](A) = A*P[m](A) XOR P[m-1](A).
```

The sampled trajectory identity has linear term `P[m](A)`. In characteristic
two these polynomials obey

```text
P[2*n](A) = P[n](A)^2.
```

One proof uses the transfer matrix of the second-order recurrence. Its `n`th
power has trace `P[n](A)`, and over `GF(2)` the trace of a squared two-by-two
matrix is the square of its trace. Iteration gives

```text
P[2^v*q](A) = P[q](A)^(2^v).
```

## Sufficiency

If `m = 2^v`, then

```text
P[m](A) = A^m.
```

Frobenius removes all mixed shift terms, leaving only shifts `-m`, `0`, and
`m`. They become the nearest-neighbor coarse shifts. Gate 07 proves closure for
every nonconstant affine block functional, including the effective constant
and the fixed-point or two-cycle classification.

## Necessity

Use affine rule `60`, whose linear operator is

```text
A = I + S^-1.
```

Write `m = 2^v*q`, where `q` is odd. The polynomial `P[q](A)` is monic of degree
`q`, and all its other powers of `A` have degree at most `q-2`. After substituting
`A = I + S^-1`, its coefficients at shifts `-q` and `-(q-1)` are both one: the
second coefficient comes only from the monic term and equals `q mod 2`.
Frobenius then shows that `P[m](A)` contains the shifts

```text
-m,
-(m - 2^v).
```

If `q > 1`, the second shift lies strictly between `-m` and `0`, so it is not a
multiple of the block size. Decimation does not observe that microscopic site.
Nevertheless changing that site changes the decimated sampled output.

This is a trajectory-law obstruction, not only a support heuristic. After the
sampled previous state is XORed away, an autonomous coarse law would require
`B*P[m](A)*x` to factor through the blocked current state `B*x`. Reversibility
allows the sampled current configuration `x` to be arbitrary. The hidden shift
therefore gives two current configurations with identical decimation and
different required coarse outputs. No autonomous decimated law of any radius
exists for rule `60` at that scale.

Consequently universal affine closure fails whenever `q > 1`. The remaining
case `q = 1` is exactly the power-of-two case.

## Executable Evidence

`test_gate_08_integer_scale_classification.py` checks:

- `P[2*n](A) = P[n](A)^2` for all 16 affine rules through `n = 32`;
- the explicit rule-60 hidden shift through scale `256`;
- all-rule alignment exactly at powers of two through scale `128`;
- API boundary conditions.

These finite checks independently exercise the implementation. The unbounded
classification follows from the symbolic odd-part argument above, not from the
finite scan.

## Nonclaims

The theorem does not classify individual affine rules at non-dyadic scales.
Some, including rule `90`, can align at additional scales. It classifies the
scales that work universally for the full affine family. It also makes no claim
about nonlinear block observers, approximate laws, records, observers, or
physics.
