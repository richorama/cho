# The Electroweak su(2) Theorem: the Weak Doublet, the Chiral so(4) Split, and the Hypercharge Spectrum

Created: 2026-06-06

Status: **mixed, and the mixture is the point.** Parts I–III below are *closed
theorems* (finite linear algebra over the octonion multiplication table). Part IV —
the reproduction of the Standard-Model hypercharge spectrum — is **conditional** on
one input, the chiral doublet/singlet assignment, and is stated as a *proposition
relative to that input*, not as a theorem. This note is deliberate about which is
which; overclaiming Part IV as "derived" would be exactly the rigour failure the
program is trying to leave behind.

Companion code (machine witness for every numbered statement):
[`compute/weak_isospin_hypercharge.py`](../compute/weak_isospin_hypercharge.py).

This is the second proof document in the rigour push, after
[`04_generation_symmetry_theorem.md`](04_generation_symmetry_theorem.md).

---

## 0. Setup and notation

Let $\mathbb{O}$ be the octonions with the fixed multiplication table `OCT_MULT`
used throughout the repository, and let
$$
\mathbb{H} \;=\; \mathrm{span}_{\mathbb R}\{\,e_0, e_1, e_2, e_3\,\}\;\subset\;\mathbb{O}
$$
be the associative quaternion subalgebra spanned by the identity $e_0$ and the
first Fano line $(e_1,e_2,e_3)$, with $e_1 e_2 = e_3$ and cyclic. For $i\in\{1,2,3\}$
let $L_{e_i}:\mathbb{H}\to\mathbb{H}$, $x\mapsto e_i x$, be left multiplication, a
real $4\times4$ matrix in the ordered basis $(e_0,e_1,e_2,e_3)$. Define the
**weak-isospin generators**
$$
T_a \;:=\; \tfrac{i}{2}\,L_{e_a}, \qquad a\in\{1,2,3\}.
$$
Each $T_a$ is a Hermitian $4\times4$ complex matrix (since $L_{e_a}$ is real and
antisymmetric, $iL_{e_a}$ is Hermitian). Concretely,
$$
L_{e_1} =
\begin{pmatrix} 0&-1&0&0\\ 1&0&0&0\\ 0&0&0&-1\\ 0&0&1&0 \end{pmatrix},
$$
and $L_{e_2}, L_{e_3}$ are obtained by cyclic relabelling of the imaginary axes.

---

## Part I — The quaternions carry a weak-isospin doublet

**Theorem 1 (su(2) from $\mathbb{H}$).**
*The operators $T_1,T_2,T_3$ satisfy the $\mathfrak{su}(2)$ commutation relations*
$$
[\,T_a, T_b\,] \;=\; i\,\varepsilon_{abc}\,T_c ,
$$
*with quadratic Casimir*
$$
T^2 \;:=\; T_1^2 + T_2^2 + T_3^2 \;=\; \tfrac{3}{4}\,\mathbb{1}_4 \;=\; j(j+1)\,\mathbb 1_4,\quad j=\tfrac12,
$$
*and $T_3$ has spectrum $\{+\tfrac12,+\tfrac12,-\tfrac12,-\tfrac12\}$. Hence the
quaternions, viewed as a complex $\mathbb{H}\otimes_{\mathbb R}\mathbb C \cong
\mathbb C^4$ module, decompose as two copies of the spin-$\tfrac12$ representation
of $\mathfrak{su}(2)$ — a weak doublet.*

*Proof.* In the associative algebra $\mathbb{H}$, left multiplication is an algebra
homomorphism: $L_{e_a}L_{e_b} = L_{e_a e_b}$. For $a\neq b$ the Fano relation gives
$e_a e_b = \varepsilon_{abc} e_c$ and $e_a e_a = -e_0$, so
$$
L_{e_a}L_{e_b} - L_{e_b}L_{e_a}
= L_{e_a e_b} - L_{e_b e_a}
= L_{\varepsilon_{abc}e_c} - L_{-\varepsilon_{abc}e_c}
= 2\varepsilon_{abc}L_{e_c}.
$$
Therefore
$$
[T_a,T_b] = \big(\tfrac{i}{2}\big)^2 [L_{e_a},L_{e_b}]
= -\tfrac14\cdot 2\varepsilon_{abc}L_{e_c}
= -\tfrac12\varepsilon_{abc}L_{e_c}
= i\,\varepsilon_{abc}\big(\tfrac{i}{2}L_{e_c}\big)
= i\,\varepsilon_{abc}T_c .
$$
For the Casimir, $L_{e_a}^2 = L_{e_a e_a} = L_{-e_0} = -\mathbb 1_4$, so
$T_a^2 = (\tfrac{i}{2})^2 L_{e_a}^2 = -\tfrac14(-\mathbb 1_4) = \tfrac14\mathbb 1_4$,
and $T^2 = 3\cdot\tfrac14\mathbb 1_4 = \tfrac34\mathbb 1_4$. A Hermitian operator with
$T^2 = \tfrac34$ on a space carrying an $\mathfrak{su}(2)$ action is pure spin
$j=\tfrac12$ (from $j(j+1)=\tfrac34$); since $\dim_{\mathbb C} = 4 = 2\times 2$, the
module is two copies of the doublet, and $T_3 = \tfrac{i}{2}L_{e_3}$ has each
eigenvalue $\pm\tfrac12$ twice. $\qquad\blacksquare$

> **Machine witness (Theorem 1).** `check_su2_algebra(isospin_generators())`
> returns `(0.0, 0.0)` (algebra error, Casimir error both exactly zero);
> `isospin_eigenvalues(T[2]) = [-0.5, -0.5, 0.5, 0.5]`.

No isospin quantum number was put in by hand: $\pm\tfrac12$ is forced by
$L_{e_a}^2 = -\mathbb 1$, i.e. by the quaternion relation $e_a^2 = -1$.

---

## Part II — Weak isospin is chiral: the so(4) left/right split

**Theorem 2 ($\mathfrak{so}(4)=\mathfrak{su}(2)_L\oplus\mathfrak{su}(2)_R$).**
*Let $R_{e_a}:x\mapsto x e_a$ be right multiplication. Then*
$$
[\,L_{e_a},\,R_{e_b}\,] = 0 \quad\text{for all } a,b\in\{1,2,3\},
$$
*the sets $\{L_{e_a}\}$ and $\{R_{e_a}\}$ each generate a copy of
$\mathfrak{su}(2)$, and together they span a $6$-dimensional Lie algebra
isomorphic to $\mathfrak{so}(4)\cong\mathfrak{su}(2)_L\oplus\mathfrak{su}(2)_R$.
The weak-isospin algebra of Part I is exactly one chiral factor,
$\mathfrak{su}(2)_L$.*

*Proof.* Associativity of $\mathbb{H}$ gives, for all $x$,
$L_{e_a}R_{e_b}\,x = e_a(x e_b) = (e_a x)e_b = R_{e_b}L_{e_a}\,x$, so
$[L_{e_a},R_{e_b}]=0$. By the same homomorphism argument as Theorem 1 (right
multiplication is an *anti*-homomorphism, which flips a sign that cancels in the
bracket), $\{\tfrac{i}{2}R_{e_a}\}$ also satisfy the $\mathfrak{su}(2)$ relations.
The six matrices $\{L_{e_1},L_{e_2},L_{e_3},R_{e_1},R_{e_2},R_{e_3}\}$ are linearly
independent real antisymmetric $4\times4$ matrices; since $\dim\mathfrak{so}(4)=6$
and these six lie in $\mathfrak{so}(4)$ (antisymmetric) and are independent, they
*span* it. Two mutually commuting $\mathfrak{su}(2)$'s whose direct sum is
$6$-dimensional give precisely the classical decomposition
$\mathfrak{so}(4)=\mathfrak{su}(2)_L\oplus\mathfrak{su}(2)_R$, the infinitesimal
form of the double cover $SU(2)\times SU(2)\to SO(4)$. $\qquad\blacksquare$

> **Machine witness (Theorem 2).** `left_right_split()` returns `(0.0, 6)`:
> all left–right commutators vanish exactly, and the joint span has rank $6$.

This is the *algebraic origin of chirality* in the weak sector: $\mathbb{H}$ does
not carry one $SU(2)$ but two, and the Standard Model gauges only the **left**
factor. Choosing $\mathfrak{su}(2)_L$ over $\mathfrak{su}(2)_R$ is the same chiral
choice that reappears as the open seam in Part IV.

---

## Part III — Direct product with colour; simultaneous diagonalisation

**Theorem 3 (commuting factors).**
*On the one-generation module $\mathbb C\otimes\mathbb H\otimes\mathbb O \cong
\mathbb C^4\otimes\mathbb C^8$, the weak generators $T_a\otimes\mathbb 1_8$ commute
with both*
- *the colour/charge operator $\mathbb 1_4\otimes Q$ of Lever C
  ([`ladder_charges.py`](../compute/ladder_charges.py)), and*
- *the KO-dimension-6 chirality $\mathbb 1_4\otimes\gamma$ of Lever B
  ([`ko_dimension_chirality.py`](../compute/ko_dimension_chirality.py)).*

*Moreover the weak raising operator $T_+\otimes\mathbb 1_8$ commutes with
$\mathbb 1_4\otimes\gamma$. Consequently the gauge action is a direct product
$SU(2)_{\text{weak}}\times SU(3)_{\text{colour}}$, a weak rotation preserves
handedness (both members of a doublet share one chirality), and $Q$ and $T_3$ are
simultaneously diagonalisable — every one-particle state has well-defined
$(Q,T_3)$.*

*Proof.* The operators act on different tensor legs: $T_a$ on the $\mathbb H$ leg,
$Q$ and $\gamma$ on the $\mathbb O$ leg. For any operators $A$ on $\mathbb C^4$ and
$B$ on $\mathbb C^8$,
$$
(A\otimes\mathbb 1_8)(\mathbb 1_4\otimes B)
= A\otimes B
= (\mathbb 1_4\otimes B)(A\otimes\mathbb 1_8),
$$
so $[T_a\otimes\mathbb 1_8,\ \mathbb 1_4\otimes Q]=0$ and likewise for $\gamma$ and
for $T_+$. Commuting Hermitian operators ($T_3$ and $Q$) are simultaneously
diagonalisable. The colour $SU(3)$ acts within the $\mathbb O$ leg (Lever C) and
the weak $SU(2)$ within the $\mathbb H$ leg, so they generate a direct product.
$\qquad\blacksquare$

> **Machine witness (Theorem 3).** `tensor_consistency(Q, gamma)` returns
> `(0.0, 0.0, 0.0)`: weak generators commute with $Q$, with $\gamma$, and the
> raising operator commutes with $\gamma$, all exactly.

---

## Part IV — Hypercharge: a proposition *conditional on the chiral assignment*

Parts I–III are unconditional theorems. The reproduction of the hypercharge
spectrum needs one further datum, which is **not** proved here.

> **Input (C) — the chiral assignment.** Each of the $16$ Weyl fields of one
> generation is assigned to an isospin representation: the eight left-handed
> fields form $SU(2)_L$ doublets ($T_3=\pm\tfrac12$, the spectrum of Part I) and
> the eight right-handed fields are $SU(2)_L$ singlets ($T_3=0$, the trivial rep).
> This left=doublet / right=singlet pattern is the open seam: $\mathbb H$ alone
> (Part II) would make *every* field a doublet, and the projection that singlets
> the right-handed sector is Lever B's KO-dimension-6 real structure, not yet
> derived (see §5).

**Proposition 4 (Gell-Mann–Nishijima spectrum, given (C)).**
*Define hypercharge by $Y := 2(Q - T_3)$, with $Q$ the Lever C electric charge and
$T_3$ the Part I weak isospin. Then under the assignment (C), the one-generation
fields carry exactly the Standard-Model hypercharges*
$$
Y \in \Big\{\, \tfrac13,\ \tfrac43,\ -\tfrac23,\ -1,\ -2,\ 0 \,\Big\},
$$
*field by field as tabulated below, totalling $16$ Weyl fermions.*

| field | $Q$ | $T_3$ | $Y=2(Q-T_3)$ | mult |
|---|---|---|---|---|
| $u_L\ (3,2)$ | $+2/3$ | $+1/2$ | $+1/3$ | 3 |
| $d_L\ (3,2)$ | $-1/3$ | $-1/2$ | $+1/3$ | 3 |
| $\nu_L\ (1,2)$ | $0$ | $+1/2$ | $-1$ | 1 |
| $e_L\ (1,2)$ | $-1$ | $-1/2$ | $-1$ | 1 |
| $u_R\ (3,1)$ | $+2/3$ | $0$ | $+4/3$ | 3 |
| $d_R\ (3,1)$ | $-1/3$ | $0$ | $-2/3$ | 3 |
| $e_R\ (1,1)$ | $-1$ | $0$ | $-2$ | 1 |
| $\nu_R\ (1,1)$ | $0$ | $0$ | $0$ | 1 |

*Proof.* Given (C), $Q$ and $T_3$ are fixed per field (columns 2–3); $Y$ is the
arithmetic of column 4, and each value matches the known Standard-Model
hypercharge. The total is $2\cdot(3+3+1+1)=16$. $\qquad\blacksquare$

> **Machine witness (Proposition 4).** `gell_mann_nishijima()` returns `all_ok =
> True` (every $Y$ matches), `count_weyl = 16`.

**What is and is not derived in Part IV.** The *operators* $Q$ (Lever C) and
$T_3$ (Part I) are algebra outputs, and the cross-check
`charges_trace_to_algebra` confirms that every $|Q|$ used lies in the Lever C
octonionic spectrum $\{0,\tfrac13,\tfrac23,1\}$ and every nonzero $|T_3|$ used lies
in the Part I doublet spectrum $\{\tfrac12\}$ — so no charge or isospin *value* is
free. What is **not** derived is the *assignment* (C) — specifically, which fields
are doublets versus singlets. Proposition 4 is therefore a theorem *relative to*
(C), and the honest content of "hypercharge is derived" is exactly:

> Hypercharge is not an independent input; it is fixed by electric charge,
> weak isospin, and the chiral assignment, via one formula $Y=2(Q-T_3)$.

The remaining freedom has been compressed from "a hypercharge per field" (six
numbers) to "one chiral projection" (the seam of §5).

---

## 5. The single residual, stated honestly

The one undischarged input is (C), the chiral doublet/singlet assignment. Its
status:

- **Reduced, not eliminated.** Before this note the Standard-Model hypercharges
  were six unexplained rational numbers. Parts I–III prove the $SU(2)$ structure
  and the simultaneous diagonalisability outright; Proposition 4 then shows the six
  numbers collapse to the *single* discrete choice (C). The free content is now one
  chiral projector, not six charges.
- **Located.** (C) is precisely the statement that the right-handed fields lie in
  the trivial $SU(2)_L$ rep. By Theorem 2, $\mathbb H$ offers two $SU(2)$'s; the
  projector that keeps only the left action on the right-handed sector is Lever B's
  KO-dimension-6 real structure $\gamma$. Closing the **Lever B ↔ Lever D linkage**
  — exhibiting the chiral idempotent on $\mathbb C\otimes\mathbb H\otimes\mathbb O$
  that realises (C) — is the outstanding obligation, and is the natural next proof
  target.

**Falsifier.** If no $\gamma$-compatible idempotent on
$\mathbb C\otimes\mathbb H\otimes\mathbb O$ reproduces the left=doublet /
right=singlet pattern (C), then the hypercharge spectrum is *not* forced by the
algebra and Proposition 4 remains a postdiction rather than a reduction.

---

## 6. Provenance and scope

- Theorems 1–3 are elementary but **fully proved** here and exactly machine-checked
  (all witness errors $0.0$). They reproduce, in this repository's own octonionic
  language, structure long known in the division-algebra Standard-Model literature
  (Furey, Dubois-Violette, Todorov); they are stated with proof for
  self-containedness, not claimed as novel.
- The **novel and honest** content is the bookkeeping of Part IV: making explicit
  that, given the algebra-derived $Q$ and $T_3$, the entire hypercharge spectrum is
  one formula away, and that the *only* residual freedom is the single chiral
  projection (C) — not six independent charges.
- This note proves nothing about the Yukawa/mass **spectrum**, which remains open
  elsewhere in the ledger.
