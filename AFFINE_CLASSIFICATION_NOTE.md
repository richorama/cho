# Exact Coarse-Graining of Reversible Binary Dynamics

## Affine Classification And A Record Limitation

### Abstract

We classify elementary binary local rules whose reversible second-order lifts
admit exact radius-one trajectory laws after factor-two spatial and temporal
coarse-graining. Requiring radius-one closure for every even periodic ring of
size at least six selects exactly the 16 affine Boolean rules. Sufficiency follows from a
`GF(2)` operator identity; necessity is certified by a size-six local conflict
for each of the 240 non-affine rules. An audit of all Boolean pair maps shows
that decimation alone already enforces the classification, while nonlinear pair
maps retain only constant rules. Reversibility provides generic local recovery
from the full state but does not provide a durable ancillary record. The result
is an exact algebraic classification, not a derivation of physical law.

## 1. Model

Let `x[t,i]` be a bit on a periodic ring and let `f` be one of the 256 Boolean
functions of the left, center, and right bits. The reversible lift is

```text
x[t+1,i] = f(x[t,i-1], x[t,i], x[t,i+1]) XOR x[t-1,i].
```

Microscopic trajectories are sampled at times `0`, `2`, and `4`. Pair
decimation keeps one site from each adjacent pair; pair parity XORs the pair.
Closure means that the blocked samples obey a reversible radius-one recurrence
with one effective elementary rule. The effective rule may depend on the
blocking and need not equal the microscopic rule.

## 2. Theorem

**Theorem.** For a microscopic elementary rule `f`, the following are equivalent:

1. at every even periodic ring size `N >= 6`, both pair decimation and pair
	parity induce reversible radius-one trajectory laws;
2. the algebraic normal form of `f` is affine.

Thus

```text
f(l,c,r) = a0 XOR al*l XOR ac*c XOR ar*r,
```

with four free binary coefficients. There are exactly `2^4 = 16` such rules.

### Sufficiency

Write the affine update as `f(x) = A x XOR a0`, with
`A = al*S^-1 + ac*I + ar*S`. Eliminating the odd time slices gives

```text
x[t+4] XOR x[t] = A^2 x[t+2] XOR A(a0).
```

In characteristic two, all cross terms in `A^2` cancel. Only shifts by `-2`,
`0`, and `2` remain, becoming nearest-neighbor shifts after pair blocking.
Decimation retains the constant `a0*(al XOR ac XOR ar)`; parity cancels the
constant field. This supplies the two effective affine rules at every size.
The bound `N >= 6` ensures the coarse ring has at least three distinct sites;
at `N = 4`, coarse left and right neighbors coincide.

### Necessity

For each non-affine truth table, exhaustive exact search at size six produces
two trajectories with the same decimated coarse previous value and current
radius-one neighborhood but incompatible next outputs. A definition-level test
verifier independently replays every certificate. Since universal radius-one
closure includes size six, each certificate disproves that universal property
for its rule. The certificates do not exclude larger-radius, stateful, or
nonlocal coarse laws. All 240 non-affine rules have a decimation certificate.

## 3. Size-Six Blocking Dependence

At source size six, with disjoint adjacent pairs and temporal stride two, the 16
Boolean pair maps split into:

| Pair-map class | Maps | Microscopic survivors |
|---|---:|---:|
| Constant | 2 | operationally degenerate |
| Nonconstant affine | 6 | all 16 affine rules |
| Nonlinear | 8 | rules `0` and `255` only |

No nonconstant pair map admits a non-affine microscopic rule. Pair parity is not
uniquely responsible for the affine family. More importantly, requiring two
blockings does not strengthen the result in this model: decimation alone already
rejects all 240 non-affine rules, while affine sufficiency under decimation is
proved for every admissible size.

## 4. Causal Transport And Records

Earlier frozen holdouts found persistent background-independent causal imprints
in eight of 20 irreversible scale-consistent rules and none of 236 controls.
That is a genuine enrichment for transport.

It is not a memory theorem. Passive local decoding failed for the interacting
fixed points, and a predeclared repetition-code protocol was not enriched.
Under the reversible lift, the full two-channel state determines the past by a
local inverse for every rule. The ancillary channel itself stores the current
bit for one step and is then masked by arbitrary prior information. Recoverable
dynamics therefore does not imply an autonomous durable record subsystem.

## 5. Interpretation

The closure classification is exact and reusable, but its conceptual reach is narrow.
It shows that a natural local coarse-graining condition is algebraically severe
and selects affine dynamics. It does not show that observer consistency forces
physics, because one simple blocking already supplies the full restriction and
the selected family does not support the required records.

The surviving affine family is subsequently proved to close under every
nonconstant affine block functional throughout the full dyadic scale hierarchy
in [DYADIC_RENORMALIZATION.md](DYADIC_RENORMALIZATION.md). The converse scale
classification in
[INTEGER_SCALE_CLASSIFICATION.md](INTEGER_SCALE_CLASSIFICATION.md) proves that
powers of two are exactly the matched scales that work universally for the
affine family. These extensions do not alter the physical interpretation or the
record limitation established here.

The justified endpoint is a Level 2 algebraic universality class plus a record
limitation. No claim is made about spacetime, quantum theory, particles,
observers, or experiment.

## 6. Executable Evidence

Run:

```bash
python3 run_all.py
python3 export_affine_certificates.py --verify
```

The scientific contracts cover ANF uniqueness, the 16 affine rules, symbolic
effective flows, 240 replayable obstruction certificates, the complete pair-map
audit, exact reversibility, causal transport controls, and record failures.
The checked-in JSON artifact contains all 240 microscopic witness pairs and can
be replayed without invoking certificate search. Its canonical SHA-256 digest is
`c485b2f8e075921ddc97b3e83b0d258aa89c270a5113183d17e3d9810edf1cab`.