# Action Projector Bridge Diagnostic

Frozen date: 2026-06-06

Purpose: sharpen the rank-one epsilon objection. The bridge

```text
epsilon0^2 = Tr(pi P_transition) / dim(A_Weyl x J3(O)) = pi / 432
```

is only derived if the CHO action forces a rank-one projector on the full `16 x 27` bridge space. Fano incidence by itself does less than that.

## What Fano Incidence Gives

In the Fano plane, any two distinct lines intersect in exactly one imaginary octonion direction. This supports:

```text
selected Fano-line pair -> rank-one octonionic direction
```

The word `selected` is essential. There are `21` unordered Fano-line pairs, and pure incidence gives the same one-dimensional overlap for all of them. The diagnostic now checks the Fano automorphism group: the `21` pairs form a single automorphism orbit. That means the degeneracy is not 21 unrelated numerical choices; it can be interpreted as a symmetry-equivalent vacuum/gauge choice after symmetry breaking.

What is still missing is the action, boundary condition, Higgs-line alignment, or generation-adjacency rule that selects a representative orbit element in the physical vacuum.

## What The Full Epsilon Projector Requires

The bridge trace space is:

```text
A_Weyl x J3(O),  dim = 16 * 27 = 432.
```

The rank ladder is:

```text
primitive Weyl x primitive Jordan    rank = 1 * 1      target
full Weyl x primitive Jordan         rank = 16 * 1     16 times too large
primitive Weyl x full Jordan         rank = 1 * 27     27 times too large
full Weyl x full Jordan              rank = 16 * 27    432 times too large
```

Only the primitive product row gives `pi / 432`. Therefore the action must derive both a rank-one Jordan/Fano direction and a rank-one Weyl/internal channel.

## What The Normalized Information Action Adds

The CHO diagnostics use a normalized `log cos(theta)` link action. For a rank-one transition kernel `K=|tau><tau|` and an idempotent bridge projector `P` containing that ray,

```text
S_link(P,K) = log( <P,K> / (||P|| ||K||) )
			 = -1/2 log(rank(P)).
```

For a product projector `P = P_Weyl x P_Jordan`, this becomes

```text
S_link = -1/2 log(rank(P_Weyl)) - 1/2 log(rank(P_Jordan)).
```

So, once the local rank-one transition kernel and product-idempotent bridge class are admitted, the information action selects the primitive `1 x 1` product projector. The full-Weyl, full-Jordan, and full-bridge alternatives are lower-action dilution channels, not equally good choices.

This is still conditional: it does not select the physical transition ray, prove the trace space, or derive the `pi` holonomy.

## Status

This improves the audit, not the theorem count.

- Rank-one Fano direction: derived only after choosing a Fano-line pair.
- Unique transition pair: not derived; incidence has a `21`-fold degeneracy, but the degeneracy is one Fano-automorphism orbit.
- Full `A_Weyl x J3(O)` rank-one projector: conditionally derived as the normalized information-action maximum once a rank-one transition kernel and product-idempotent bridge class are supplied.
- `pi` holonomy: still a coset/action target.
- Coupling reuse across masses, CKM, and PMNS: still a shared-operator target.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 compute/action_projector_derivation.py
PYTHONDONTWRITEBYTECODE=1 python3 compute/primitive_projector_derivation.py
```

The scripts print the incidence degeneracy, the Fano-automorphism orbit check, the bridge-rank embedding table, the normalized action rank penalty, and the closure tests a real CHO action derivation must pass.
