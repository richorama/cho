# Primitive Projector Bridge

Frozen date: 2026-06-06

Purpose: derive as much as possible of the primitive `A_Weyl x J3(O)` projector from the CHO information action, without hiding the assumptions that still remain.

## Local Action Term

Use the normalized alignment form of the CHO information action:

```text
S_link(P, K) = log( <P, K> / (||P|| ||K||) )
```

This is the projector version of the `log cos(theta)` link term used in the scattering and Yukawa diagnostics. Here `K` is the rank-one transition kernel supplied locally by the Fano intersection, and `P` is an admissible bridge projector on `A_Weyl x J3(O)`.

The normalization is essential. A raw trace `Tr(P K)` cannot distinguish a primitive projector from a larger projector that merely contains the same transition ray.

## Rank Penalty

Let `K = |tau><tau|` have rank one. If an idempotent projector `P` contains that transition ray and has bridge-trace rank `r`, then

```text
<P, K> = 1
||K|| = 1
||P|| = sqrt(Tr(P^2)) = sqrt(r)
```

so

```text
cos(theta) = 1 / sqrt(r)
S_link = -1/2 log(r).
```

The action is maximal at `r = 1`. Every extra Weyl or Jordan trace direction lowers the action by a definite amount.

For a product bridge projector

```text
P = P_Weyl x P_Jordan,
rank(P) = rank(P_Weyl) rank(P_Jordan),
```

the action separates:

```text
S_link = -1/2 log(rank(P_Weyl)) - 1/2 log(rank(P_Jordan)).
```

Thus the normalized information action selects

```text
rank(P_Weyl) = 1,
rank(P_Jordan) = 1.
```

This is the primitive product row required by the epsilon bridge.

## Jordan Meaning

For the exceptional Jordan factor, the primitive object is a normalized primitive idempotent `e` in `J3(O)`:

```text
e o e = e,
Tr_J(e) = 1.
```

It defines a rank-one linear projector on the 27-dimensional bridge trace space:

```text
P_e(X) = <e, X> e / <e, e>.
```

The derivation above selects this one-dimensional trace direction over the full 27-dimensional Jordan trace because the full trace has the lower action value `-1/2 log(27)`.

## What This Closes

This closes a narrower version of the primitive-embedding gap:

- if the CHO link action is the normalized `log cos` term;
- if the local transition kernel is already rank one;
- if admissible bridge projectors are idempotent product projectors on `A_Weyl x J3(O)`;
- if the transition ray lies inside the candidate projector;

then the action derives the primitive `1 x 1` product projector as the unique maximum among the rank ladder.

## What Remains Open

This does not derive the full epsilon bridge by itself. The remaining proof obligations are:

- derive the physical transition ray `|tau>` from the CHO action or boundary condition;
- derive the physical representative of the single Fano line-pair orbit;
- prove that the trace space is exactly `A_Weyl x J3(O)`;
- derive the `pi` holonomy;
- show that this same transition operator feeds the charged masses, CKM, PMNS, and neutrino splitting without changing its meaning.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 compute/primitive_projector_derivation.py
```

The script prints the action-rank table and the assumptions under which the primitive product is actually derived.