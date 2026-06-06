# Yukawa Bridge Scaffold

Frozen date: 2026-06-06

Purpose: upgrade the charged-flavour bridge from formula list to operator targets. This note separates what is actually derived by the current scaffold from what still requires a CHO Yukawa operator proof.

## Derived Inside The Scaffold

### 1. Nearest-Neighbor Texture

Let the ordered generation basis be `(1, 2, 3)`. The leading triality transition is adjacent:

```text
1 <-> 2 <-> 3
```

The corresponding adjacency mask is

```text
0 1 0
1 0 1
0 1 0
```

so the direct `1 <-> 3` entry is absent at leading order:

```text
M13 = M31 = 0.
```

This is the cleanest current derivation: it follows from the one-step triality selection rule. The physical proof still needs the trilinear CHO Yukawa map that enforces the one-step rule.

### 2. Cascade Mass Relation

If the second-generation suppression is

```text
q_f = m2 / m3,
```

and the sector NNI shape factor is

```text
k_f = m1*m3 / m2^2,
```

then the first-generation mass follows algebraically:

```text
m1 / m3 = k_f * q_f^2.
```

This is no longer a loose prose relation: it is the cascade rule that the final Yukawa operator must reproduce.

### 3. Sector Multiplicity Traces

The scaffold treats the second-generation suppressions as rank traces over sector projectors:

```text
up:     q_u = 1 * epsilon0^2
down:   q_d = N_color * epsilon0^2 = 3 * epsilon0^2
lepton: q_l = dim(O) * epsilon0^2 = 8 * epsilon0^2
```

This converts `1`, `3`, and `8` from bare dimensional counts into trace targets. The remaining proof is to derive the sector projectors from the CHO trilinear Yukawa map.

## Open Operator Targets

The sector shape factors are still bridge targets:

```text
up:     k_u = 1/4
down:   k_d = 9/4
lepton: k_l = 1/(4*pi)
```

The final CHO Yukawa operator must derive these factors as traces, overlaps, or Schur-complement invariants. Until then M9-M11 stay `Open bridge / scaffolded`.

## Diagnostic Script

Run:

```bash
python3 compute/yukawa_bridge.py
```

The script prints the adjacency derivation, sector cascade table, comparison with observed first-generation ratios, and the proof obligations for the missing Yukawa operator.
