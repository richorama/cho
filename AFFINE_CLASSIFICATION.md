# Affine Classification Campaign

## Scope

This campaign consolidates the finite reversible trajectory census into a
classification theorem. It does not extend the model or search for new physics.

Let `f : {0,1}^3 -> {0,1}` be an elementary local rule on a periodic binary
ring. Its reversible second-order lift is

```text
x[t+1,i] = f(x[t,i-1], x[t,i], x[t,i+1]) XOR x[t-1,i].
```

Pair decimation keeps the left cell of each adjacent pair. Pair parity XORs the
two cells. The trajectory test applies either spatial blocking to states sampled
at times `0`, `2`, and `4`, and asks whether the blocked trajectory obeys another
radius-one reversible second-order law.

## Classification Theorem

For an elementary rule `f`, the following statements are equivalent:

1. for every even ring size `N >= 6`, pair decimation and pair parity each induce
    a reversible radius-one trajectory law, which may differ from `f` and from
    each other;
2. `f` is affine over `GF(2)`.

Equivalently, write the unique algebraic normal form

```text
f(l,c,r) = a0 XOR al*l XOR ac*c XOR ar*r
           XOR alc*l*c XOR alr*l*r XOR acr*c*r XOR alcr*l*c*r.
```

The universal-in-size survivors are exactly the 16 rules with
`alc = alr = acr = alcr = 0`.

## Sufficiency Identity

For an affine rule, write `f(x) = A x XOR a0`, where
`A = al*S^-1 + ac*I + ar*S`. The second-order recurrence implies

```text
x[t+4] XOR x[t] = A^2 x[t+2] XOR A(a0).
```

Over `GF(2)`, cross terms in `A^2` cancel. Its radius-two shifts become
radius-one shifts after pair blocking. Decimation retains the constant
`a0*(al XOR ac XOR ar)`, while pair parity removes every constant field.
The function `affine_effective_rules` implements these two coefficient maps.

This identity is independent of ring size. It proves sufficiency for every even
ring whose coarse ring has at least three distinct sites. The lower bound
`N >= 6` avoids the size-two coarse ring, where left and right neighbors alias.

## Necessity Certificates

Every one of the 240 non-affine rules has a machine-checkable size-six pair of
microscopic trajectories. Each pair presents the same decimated coarse previous
value and current radius-one neighborhood but demands different next values.
Therefore no reversible radius-one decimated trajectory law exists at size six.
The certificate does not exclude larger-radius, stateful, or nonlocal coarse
laws. It does prove that such a rule cannot satisfy the stated radius-one closure
condition for every even size at least six.

The certificate generator, production replay validator, and a definition-level
test verifier are exercised by
`test_every_non_affine_rule_has_a_bounded_conflict_certificate`. The latter
reimplements the truth-table update and decimation directly instead of calling
the generator's observation helper. All 240 certificates already fail
decimation; parity is unnecessary for necessity.

## Size-Six Blocking Audit

All 16 Boolean pair maps were frozen and enumerated at source size six:

- the two constant maps are operationally degenerate;
- the six nonconstant affine maps each select all 16 affine rules;
- the eight nonlinear maps retain only constant microscopic rules `0` and `255`;
- no nonconstant pair map admits a non-affine rule.

The theorem is a closure classification, not a common-fixed-point theorem: the
effective laws may differ by blocking and from the microscopic law. It is not
specifically caused by parity. Agreement between the two theorem blockings also
adds no selection pressure here: decimation by itself already gives the complete
universal-in-size affine classification.

## Reversible Record Propositions

The full second-order state has an exact local inverse, so bounded recovery is
generic across all 256 rules rather than selected by scale consistency. The
ancillary channel copies the current state for one step. At the next step its
value is XOR-masked by an arbitrary previous bit, so that subsystem alone is not
a durable record.

## Campaign Status

The proof and blocking-audit obligations are complete. The accompanying
technical note states the theorem, audit, record limitation, and nonclaims in
publication order.

No physical interpretation follows from this theorem.