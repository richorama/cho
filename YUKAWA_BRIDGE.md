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

This converts `1`, `3`, and `8` from bare dimensional counts into trace targets. Later repair work sharpened this point: after choosing the complex-octonion idempotent `omega=(1+i e7)/2`, the Fock grades have dimensions `1,3,3,1`, and `compute/epsilon_channel_coefficients.py` derives the mass-sector ranks as number-operator traces: `up = Tr P_0 = 1`, `down = Tr P_1 = 3`, and `lepton = Tr I_Fock = 2^3 = 8`. What remains open is not the integer `8` itself, but why the final CHO Yukawa trilinear dynamically selects these traces in one operator.

## Open Operator Targets

The sector shape factors are still bridge targets:

```text
up:     k_u = 1/4
down:   k_d = 9/4
lepton: k_l = 1/(4*pi)
```

The final CHO Yukawa operator must derive these factors as traces, overlaps, or Schur-complement invariants. Until then M9-M11 stay `Open bridge / scaffolded`.

**Lepton update (Item 2, `compute/lepton_yukawa_action.py`).** The lepton factor `k_l = 1/(4*pi)` is no longer chosen: it is FORCED as the `SU(2)` invariant-average (Schur) normalization `= 1/(total solid angle)` on the SAME two-level Bloch sphere `S^2` whose hemisphere solid angle `2*pi` gives the Berry `theta = pi` of `foundations/02_action.md`. That module assembles the WHOLE charged-lepton Yukawa as ONE Hermitian operator `Y = m_tau * diag(1, 8*epsilon0^2, k_l*(8*epsilon0^2)^2)`, reusing the derived Fock trace `8` (M3) and the rank-one "lift exactly one level" cascade. Spectrum: `tau` exact, `mu/tau` at `-2.2%`, `e/tau` at `-6.3%` (the known M11 first-generation outlier, reported honestly; only `mu` is asserted). Still open even for leptons: WHY the lepton channel takes the continuous-sphere average while the quark sectors take discrete weak-isospin projections (`k_u = 1/4`, `k_d = 9/4`, no `pi`), deriving the trilinear from the CHO equations of motion, and the `~6%` `m_e` residual. The up/down factors remain fully open.

**Sphere-vs-discrete update (`compute/sector_sphere_dichotomy.py`).** That open lepton-vs-quark question is sharpened to ONE discriminant: `pi` appears in a sector's first-generation shape IFF the transition is averaged over a CONTINUOUS manifold, and is ABSENT (rational) IFF over a DISCRETE Fock grade. A finite group (`Q8`) averages the rank-one projector to EXACTLY `I/2` (rational, no `pi`); the continuous `S^2` average is `1/(4*pi)` (and `Vol(S^2)=4*pi` is transcendental, so the lepton value can never be a finite/discrete rational). The sector's Fock support picks the regime: a quark projects onto a SINGLE number-operator grade (`up = Tr P_0 = 1`, `down = Tr P_1 = 3 = N_c`), giving the RATIONAL `k_u = (Tr P_0/2)^2 = 1/4` and `k_d = (Tr P_1/2)^2 = 9/4 = (1/4) N_c^2` -- exactly M10's "sector-square rule", from the SAME derived Fock ranks; the colour-singlet lepton uses the full continuous colourless module, hence the sphere measure `1/(4*pi)`. **Still open (not faked):** WHY the colour singlet uses the continuous average while the coloured sectors project onto a single grade (the dynamical SELECTION) is the residual input; the `(rank/2)^2` law is a two-sector fit; F0 is NOT promoted; M9-M11 stay open bridges.

For the sector-count diagnostic, run `python3 compute/sector_projector_derivation.py`.

## Diagnostic Script

Run:

```bash
python3 compute/yukawa_bridge.py
```

The script prints the adjacency derivation, sector cascade table, comparison with observed first-generation ratios, and the proof obligations for the missing Yukawa operator.
