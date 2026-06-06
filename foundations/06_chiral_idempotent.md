# The Chiral Idempotent: Closing the Lever B ↔ Lever D Seam

Created: 2026-06-06

Status: **the structural core is a closed theorem; one honest residual remains
(the fermion-content map), and it is named.** This note discharges input (C) of
[`05_electroweak_su2_theorem.md`](05_electroweak_su2_theorem.md) — the
left=doublet / right=singlet assignment that Proposition 4 was conditional on —
down to a single chiral projector, by *constructing* that projector and proving
its properties. It is the third proof document of the rigour push, after
[`04`](04_generation_symmetry_theorem.md) and [`05`](05_electroweak_su2_theorem.md).

Companion code (machine witness for every numbered statement):
[`compute/chiral_projector.py`](../compute/chiral_projector.py). All witness
errors below are exactly $0.0$.

---

## 0. The problem, precisely

Lever D, Theorem 3 proved that the weak generators $T_a\otimes\mathbb 1_8$
*commute* with the chirality $\mathbb 1_4\otimes\gamma$ on
$\mathbb C\otimes\mathbb H\otimes\mathbb O = \mathbb C^4\otimes\mathbb C^8$. This
is exactly why the naive chiral projector fails to produce the Standard Model's
chiral matter: if $T_a\otimes\mathbb 1_8$ commutes with $\mathbb 1_4\otimes\gamma$,
then on *both* the $\gamma=+1$ and $\gamma=-1$ subspaces the isospin acts as a
*full doublet*. A spectator $\gamma$ cannot turn the right-handed sector into
singlets.

Input (C) — that left-handed fields are doublets and right-handed fields are
$SU(2)_L$ singlets — therefore looked like eight independent per-field choices.
This note shows it is **one** choice: a single idempotent.

---

## 1. The gauged generators are chirally projected

The physical content of "the weak force acts only on left-handed fields" is that
the **gauged** generators are not $T_a\otimes\mathbb 1_8$ but the chirally
projected operators
$$
\boxed{\;G_a \;:=\; T_a \otimes P_L, \qquad P_L := \tfrac12(\mathbb 1_8 + \gamma)\;}
$$
where $\gamma$ is a KO-dimension-6 chirality on the $\mathbb O$ leg (built below)
and $P_L$ is the corresponding idempotent.

**Theorem 1 (su(2) closure survives projection).**
*The $G_a$ satisfy $[G_a,G_b] = i\varepsilon_{abc}G_c$.*

*Proof.* $P_L$ is an idempotent: $P_L^2 = \tfrac14(\mathbb 1+\gamma)^2 =
\tfrac14(\mathbb 1 + 2\gamma + \gamma^2) = \tfrac14(2\mathbb 1 + 2\gamma) = P_L$,
using $\gamma^2 = \mathbb 1$ (Proposition 3). Hence
$$
[G_a, G_b] = [T_a\otimes P_L,\ T_b\otimes P_L]
= [T_a,T_b]\otimes P_L^2
= (i\varepsilon_{abc}T_c)\otimes P_L
= i\varepsilon_{abc}\,G_c,
$$
where the middle equality uses $(A\otimes P)(B\otimes P) = AB\otimes P^2$ and
Theorem 1 of [`05`](05_electroweak_su2_theorem.md) for $[T_a,T_b]$. $\qquad\blacksquare$

> **Machine witness (Theorem 1).** `idempotent_error(P_L) = 0.0`;
> `check_projected_su2(G) = 0.0`.

It is precisely the idempotency $P_L^2=P_L$ — not commutativity — that lets the
projector ride through the bracket. This is the structural reason the
construction works.

---

## 2. One idempotent gives doublet on the left, singlet on the right

**Theorem 2 (the dichotomy).**
*The gauged quadratic Casimir $C := \sum_{a}G_a^2$ equals $\tfrac34\,\mathbb 1_4
\otimes P_L$. Consequently*
$$
C = \tfrac34 \text{ on } \mathbb C^4\otimes(\gamma{=}{+}1)\ \text{(a $j=\tfrac12$ DOUBLET)},
\qquad
C = 0 \text{ on } \mathbb C^4\otimes(\gamma{=}{-}1)\ \text{(the TRIVIAL rep, a SINGLET)}.
$$
*Hence the single idempotent $P_L$ realises the entire left=doublet /
right=singlet dichotomy (C).*

*Proof.* Using $T_a^2$ summed $=\tfrac34\mathbb 1_4$ (Theorem 1 of
[`05`](05_electroweak_su2_theorem.md)) and $P_L^2=P_L$,
$$
C = \sum_a (T_a\otimes P_L)^2 = \Big(\sum_a T_a^2\Big)\otimes P_L^2
= \tfrac34\mathbb 1_4 \otimes P_L .
$$
$P_L$ is the spectral projector onto $\gamma=+1$, so $P_L=\mathbb 1$ there and
$P_L=0$ on $\gamma=-1$; the two displayed values follow. A two-level space with
Casimir $\tfrac34=\tfrac12(\tfrac12+1)$ is the spin-$\tfrac12$ doublet; Casimir
$0$ is the trivial one-dimensional rep. $\qquad\blacksquare$

> **Machine witness (Theorem 2).** `casimir_spectrum_by_chirality` returns
> nonzero Casimir on the $\gamma{=}{+}1$ sector $=[0.75]$ and max$|C|$ on the
> $\gamma{=}{-}1$ sector $=0.0$.

This is the crux result: **the residual freedom in (C) is one chiral projector,
not a table of eight assignments.**

---

## 3. The chirality must be aligned with charge — and then it is KO-6

Theorem 2 used a chirality $\gamma$ with $\gamma^2=\mathbb 1$. For the projector
to split **charge eigenstates** consistently, $\gamma$ must commute with the
Lever C charge $Q$. This is a genuine constraint, and meeting it sharpens
Lever B.

Lever C's charge operator fixes one octonionic colour direction $e_f$ and is
built bilinearly from left-multiplications by the remaining six imaginary units
$\{e_i : i\neq f\}$. Define the **charge-aligned chirality**
$$
\gamma_Q \;:=\; i\!\!\prod_{i\neq f} L_{e_i}
\qquad\text{(volume element over the six charge-carrying directions).}
$$

**Proposition 3 (KO-6 and alignment).**
*$\gamma_Q^2 = \mathbb 1_8$; the real structure $J$ (complex conjugation) gives
$(\varepsilon,\varepsilon'') = (+1,-1)$, i.e. KO-dimension $6$; and*
$$
[\,Q,\ \gamma_Q\,] = 0 .
$$

*Proof.* The six matrices $L_{e_i}$ ($i\neq f$) satisfy the Clifford relations
$\{L_{e_i},L_{e_j}\} = -2\delta_{ij}$ (Lever B), so they pairwise anticommute and
square to $-\mathbb 1$. For a product of $n=6$ such factors,
$$
\Big(\textstyle\prod_{k=1}^{6} L_{e_{i_k}}\Big)^2
= (-1)^{\binom{6}{2}}\prod_k L_{e_{i_k}}^2
= (-1)^{15}(-1)^6 = -1,
$$
so $\gamma_Q^2 = i^2\cdot(-1) = (-1)(-1) = +1$. For the KO signs, $J$ is complex
conjugation, $J^2=+\mathbb 1$ so $\varepsilon=+1$; and since the $L_{e_i}$ are
real matrices while the prefactor is $i$, $J\gamma_Q J^{-1} = \overline{\gamma_Q}
= -i\prod L_{e_i} = -\gamma_Q$, giving $\varepsilon''=-1$. The pair
$(+1,-1)$ is KO-dimension $6$ (Connes–Barrett table, as in Lever B).

For alignment: $Q = \tfrac13\sum_k \alpha_k^\dagger\alpha_k$ is a sum of products
of *two* of the six $L_{e_i}$, i.e. $Q$ lies in the **even** subalgebra
generated by $\{L_{e_i}:i\neq f\}$. In a Clifford algebra of even rank $6$, the
volume element $\prod_{i\neq f}L_{e_i}$ commutes with every even element (it
anticommutes with each of the six generators an even number — namely $5+1=6$ —
of times when commuted past a grade-$2$ element). Hence $[Q,\gamma_Q]=0$.
$\qquad\blacksquare$

> **Machine witness (Proposition 3).** `aligned_chirality(fixed)` gives
> `gamma_Q^2 = I` error $0.0$, `ko6_signs = (+1, -1)`, and
> `|[Q, gamma_Q]| = 0.0`. By contrast Lever B's representative
> $\gamma=iL_1\cdots L_6$ (which keeps the colour axis) gives
> $|[Q,\gamma]| = \tfrac13 \neq 0$ — the misalignment that made (C) look open.

**Refinement of Lever B.** Lever B established KO-dimension $6$ with a
*representative* chirality; Proposition 3 shows the chirality that is physically
consistent with the Lever C charge is the volume element over the six
charge-carrying directions (dropping the colour axis). It is still KO-6, and now
$[Q,\gamma_Q]=0$. This is a consistency refinement, not a new input.

---

## 4. The charge–chirality split

Because $[Q,\gamma_Q]=0$, $Q$ and $\gamma_Q$ are simultaneously diagonalisable
and every electric-charge eigenstate has a definite chirality.

**Corollary 4 (the split).**
*The eight charge eigenstates of one $\mathbb C\otimes\mathbb O$ ideal split into
two chirality quartets:*

| chirality | charges (with colour multiplicity) | states |
|---|---|---|
| $\gamma_Q = +1$ (doublet sector) | $Q=\tfrac13\ (\times 3),\ \ Q=1\ (\times 1)$ | 4 |
| $\gamma_Q = -1$ (singlet sector) | $Q=0\ (\times 1),\ \ Q=\tfrac23\ (\times 3)$ | 4 |

*Proof.* Immediate from simultaneous diagonalisation; the table is the computed
$(Q,\gamma_Q)$ spectrum. $\qquad\blacksquare$

> **Machine witness (Corollary 4).** `charge_chirality_table(Q, gamma_Q)`
> returns exactly this assignment.

---

## 5. Main theorem and honest residual

**Theorem (Chiral Idempotent).**
*On $\mathbb C\otimes\mathbb H\otimes\mathbb O$ there is a single
KO-dimension-6 idempotent $P_L=\tfrac12(\mathbb 1+\gamma_Q)$, built from the
charge-aligned chirality $\gamma_Q$, such that the gauged weak generators
$G_a=T_a\otimes P_L$ (i) close $\mathfrak{su}(2)$, (ii) act as a $j=\tfrac12$
doublet on the $\gamma_Q=+1$ sector and as a singlet on the $\gamma_Q=-1$ sector,
and (iii) commute with electric charge, so the doublet/singlet split is
charge-definite. Consequently input (C) of Lever D — previously eight
independent per-field assignments — is reduced to this one projector.*

*Proof.* Theorems 1, 2 and Proposition 3 / Corollary 4. $\qquad\blacksquare$

### What is now *not* conditional, and what still is

- **Discharged.** Proposition 4 of [`05`](05_electroweak_su2_theorem.md) no
  longer rests on a free per-field table: the doublet/singlet dichotomy is one
  idempotent, charge-compatible. The hypercharge formula $Y=2(Q-T_3)$ then runs
  on operators ($Q$, $T_3$) and one projector ($P_L$), all algebra-internal.
- **Residual 1 (orientation).** Which sign, $P_L=\tfrac12(\mathbb 1+\gamma_Q)$ or
  $\tfrac12(\mathbb 1-\gamma_Q)$, is "left" is a convention — the *definition* of
  left-handedness — not a free parameter per field.
- **Residual 2 (the content map, honestly open).** Corollary 4 splits the eight
  charge states $4+4$ by chirality, but identifying the $\gamma_Q=+1$ quartet
  *field by field* with the physical Standard-Model left-handed multiplets is the
  **fermion-content map** onto $T(\mathbb{OP}^2)$, which is listed as open in the
  ledger (row G1). This note does **not** close that map; it proves the
  *dichotomy and its charge-compatibility*, which is what (C) required as an
  input, and leaves the physical labelling to the content map.

**Falsifier.** If no charge-commuting KO-6 chirality existed on
$\mathbb C\otimes\mathbb O$ (i.e. if every chirality gave $[Q,\gamma]\neq0$), the
projected construction would be inconsistent and (C) would remain an irreducible
per-field input. Proposition 3 exhibits one, so this falsifier is *not*
triggered.

---

## 6. Provenance and scope

- The chiral-projection mechanism (weak isospin acting through a chiral
  idempotent) is the algebraic counterpart of the Standard Model's left-handed
  gauge coupling and is standard in the division-algebra / NCG literature
  (Furey, Dubois-Violette, Connes); the construction here is in this
  repository's own octonionic operators and is stated with proof for
  self-containedness.
- The **novel and honest** content is twofold: (i) making explicit that
  idempotency $P_L^2=P_L$ — not commutativity — is what closes the algebra under
  projection (Theorem 1), and (ii) the *alignment refinement* (Proposition 3):
  the charge-consistent KO-6 chirality is the volume element over the six
  charge-carrying directions, for which $[Q,\gamma_Q]=0$ exactly, whereas the
  colour-axis representative gives $\tfrac13$.
- This note closes the **dichotomy** half of (C). It says nothing about the
  Yukawa/mass **spectrum**, and it explicitly leaves the field-by-field
  **content map** open (§5, Residual 2).
