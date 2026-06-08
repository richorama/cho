# Three Theorems on the Exceptional Jordan Algebra 𝔍₃(𝕆)

**Standalone mathematics, decoupled from any physical interpretation**

Richard Astbury
Developed as a human–AI collaboration (with Claude, Anthropic)
Frozen: 2026-06-08

---

## Abstract

We isolate and machine-verify three small results about the rank-3 exceptional
(Albert) Jordan algebra $\mathfrak{J}_3(\mathbb{O})$ of $3\times 3$ Hermitian
octonionic matrices. None of the three uses, asserts, or depends on a physical
interpretation: there are no generations, masses, Yukawa couplings, no spurion,
and the number $\pi/432$ does not appear. The objects are $\mathfrak{J}_3(\mathbb{O})$,
its automorphism group $F_4=\mathrm{Aut}(\mathfrak{J}_3(\mathbb{O}))$, the point
stabiliser $\mathrm{Spin}(9)$, the reduced structure group $E_6$ preserving the
Freudenthal cubic norm, and elementary representation theory and polynomial
algebra. A reader who rejects every physical claim made elsewhere in this project
can still check every line here, by hand and by machine.

- **Theorem A (inner frame symmetry).** The symmetric group $S_3$ permuting the
  three primitive idempotents of a Jordan frame acts by *inner* automorphisms —
  it lies in the connected group $F_4$, which has no outer automorphism — so it
  cannot carry an $F_4$-module to an inequivalent one. The three idempotents are
  $F_4$-congruent points of the Cayley plane $\mathbb{O}P^2=F_4/\mathrm{Spin}(9)$,
  each with isotropy of dimension $36=\dim\mathfrak{spin}(9)$ and tangent space
  the $16$-dimensional *real* $\mathrm{Spin}(9)$ spinor $\Delta_9$ (self-conjugate).
  This is categorically different from the *outer* triality of
  $D_4=\mathrm{Spin}(8)$, which permutes three **inequivalent** $8$-dimensional
  modules $8_v,8_s,8_c$.
- **Theorem B (Schur rigidity).** The unique invariant mean of a rank-one
  projector on an irreducible real $G$-module of dimension $d$ is $\tfrac1d\,I$.
  $\Delta_9$ ($\dim 16$) is $\mathrm{Spin}(9)$-irreducible, giving the flat weight
  $1/16$; $\mathfrak{J}_3(\mathbb{O})$ ($\dim 27$) is **reducible** under $F_4$
  ($27=1\oplus 26$) but **irreducible** under the cubic-norm group $E_6$, giving
  the flat weight $1/27$. The flat $1/27$ is forced by $E_6$, not by its
  subgroup $F_4$.
- **Theorem C (Freudenthal-cubic seesaw).** For the characteristic cubic
  $t^3-T_1t^2+T_2t-N_3$ of an element (coefficients the three $F_4$ invariants),
  Vieta gives eigenvalue product $m_1m_2m_3=N_3$, hence $m_2m_3=|N_3|/m_1$: the
  light pair's product is the cubic norm divided by the heaviest eigenvalue.

Every constituent fact is **classical** and is cited rather than claimed. The
contribution is the *assembly* into three clean, decoupled, checkable statements,
plus three observations: (A) that the frame $S_3$ being inner is exactly what
exempts the idempotent picture from an *outer-triality* obstruction; (B) the
crisp $F_4$-reducible / $E_6$-irreducible dichotomy that pins the flat $1/27$ to
the cubic-norm group; and (C) reading Vieta on the cubic norm as a seesaw. Each
is backed by an executable witness ([compute/jordan_standalone_theorems.py](compute/jordan_standalone_theorems.py))
that returns `PASS` inside the project's audit harness.

---

## 1. Scope and stance

This note is a deliberate *decoupling*. The wider project develops a physical
interpretation of $\mathfrak{J}_3(\mathbb{O})$ — generations, a flavour measure,
a mass spectrum — and is explicit that those bridges remain open and gated
(see [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md) and
[PAPER_OPTION_A.md](PAPER_OPTION_A.md)). The purpose here is the opposite: to
extract the parts of the underlying mathematics that stand entirely on their own,
state them as theorems of pure algebra and representation theory, and verify them
with no physical input whatsoever.

We are explicit about novelty. The constituent facts below are all classical: the
Albert algebra and its frames (Jordan–von Neumann–Wigner; Springer; McCrimmon);
$F_4=\mathrm{Aut}(\mathfrak{J}_3(\mathbb{O}))$ connected with no outer
automorphism, and $\mathbb{O}P^2=F_4/\mathrm{Spin}(9)$ (Freudenthal; Yokota); the
$16$-dimensional real $\mathrm{Spin}(9)$ spinor; $E_6$ as the reduced structure
group preserving the cubic norm with irreducible $27$; Schur's lemma; and Vieta's
formulae. We do **not** claim any of these as new theorems. What we claim is the
clean *assembly* — three statements decoupled from physics, each with a machine
witness — and three specific observations that, to our knowledge, are not usually
stated together in this crisp form. The value is clarity and checkability, not
depth.

Throughout, "verified" means: a hand proof or a citation, plus an executable
check that returns `PASS` in [compute/audit.py](compute/audit.py). The witness for
this note is [compute/jordan_standalone_theorems.py](compute/jordan_standalone_theorems.py);
it reuses the project's verified linear-algebra constructions (it does not
re-implement them) and adds the decoupled theorem-layer statements. "Decoupled"
refers to the *theorems and their proofs*, not to the code: the reused helpers are
pure linear algebra with no physical content.

---

## 2. The exceptional Jordan algebra and its symmetry groups

Let $\mathbb{O}$ be the octonions and let
$$
\mathfrak{J}_3(\mathbb{O})=\Bigl\{\,X=\begin{pmatrix}\alpha & a & \bar b\\ \bar a & \beta & c\\ b & \bar c & \gamma\end{pmatrix} : \alpha,\beta,\gamma\in\mathbb{R},\ a,b,c\in\mathbb{O}\,\Bigr\},
\qquad \dim_\mathbb{R}\mathfrak{J}_3(\mathbb{O})=27,
$$
with the commutative Jordan product $X\circ Y=\tfrac12(XY+YX)$ (Albert 1934;
Jordan–von Neumann–Wigner 1934). Every $X$ satisfies its **characteristic cubic**
$$
X^3-T_1\,X^2+T_2\,X-N_3\,I=0,\qquad
T_1=\operatorname{tr}X,\quad
T_2=\tfrac12\bigl((\operatorname{tr}X)^2-\operatorname{tr}(X\circ X)\bigr),\quad
N_3=\det X,
$$
where $\det X$ is the Freudenthal determinant (cubic norm) and the three
coefficients are the elementary symmetric functions of the (real) eigenvalues
(Springer 1962). The three groups we use are:

- $F_4=\mathrm{Aut}(\mathfrak{J}_3(\mathbb{O}))$, the compact connected simple
  group of dimension $52$ and trivial outer automorphism group; it preserves
  $\circ$, hence $T_1,T_2,N_3$ (Chevalley–Schafer 1950; Freudenthal; Yokota).
- $\mathrm{Spin}(9)\subset F_4$, the stabiliser of a primitive idempotent
  ($\dim 36$); the quotient $F_4/\mathrm{Spin}(9)=\mathbb{O}P^2$ is the Cayley
  projective plane (Freudenthal 1951).
- $E_6$, the reduced structure group ($\dim 78$), the connected group preserving
  the cubic norm $N_3$ up to scale; it acts irreducibly on the $27$ (Springer;
  Jacobson 1971). $F_4\subset E_6$ is the subgroup additionally fixing $I$.

A **Jordan frame** is a complete system $\{e_1,e_2,e_3\}$ of orthogonal primitive
idempotents: $e_i\circ e_j=\delta_{ij}e_i$, $\sum_i e_i=I$, each $e_i$ primitive.
The diagonal frame is $e_i=\mathrm{diag}(\delta_{i1},\delta_{i2},\delta_{i3})$.

---

## 3. Theorem A — inner frame symmetry

> **Theorem A.** Let $\{e_1,e_2,e_3\}$ be a Jordan frame of
> $\mathfrak{J}_3(\mathbb{O})$. The $S_3$ that permutes the $e_i$ is realised by
> automorphisms lying in the connected group $F_4=\mathrm{Aut}(\mathfrak{J}_3(\mathbb{O}))$.
> Consequently this $S_3$ acts trivially on the set of isomorphism classes of
> $F_4$-modules, and the three idempotents lie in a single $F_4$-orbit
> $\mathbb{O}P^2=F_4/\mathrm{Spin}(9)$, each with isotropy of dimension
> $36=\dim\mathfrak{spin}(9)$ and tangent space the $16$-dimensional real
> $\mathrm{Spin}(9)$ spinor $\Delta_9$ (commutant dimension $1$, hence
> self-conjugate).

**Proof sketch.** The permutation of a frame is induced by conjugation
$X\mapsto P_\sigma X P_\sigma^{-1}$ by the corresponding $3\times 3$ permutation
matrix, which is a Jordan automorphism (it preserves $\circ$ and the diagonal
frame is mapped to its $\sigma$-image). Every Jordan automorphism preserves
$T_1,T_2,N_3$, so each frame permutation fixes all three $F_4$ invariants; the
witness confirms this to machine precision across random elements. Because $F_4$
is connected, for $g\in F_4$ and any module $\rho$ one has
$\rho\circ\mathrm{conj}_g\cong\rho$, so the $S_3$ cannot send a module to an
inequivalent one. $F_4$ acts transitively on primitive idempotents with
stabiliser $\mathrm{Spin}(9)$ (Freudenthal 1951), so $e_1,e_2,e_3$ are
$F_4$-congruent points of $\mathbb{O}P^2$; the tangent space at each is the real
$16$-dimensional spinor $\Delta_9$, which is of real type (commutant $=\mathbb{R}$,
dimension $1$), hence self-conjugate. $\qquad\blacksquare$

**Witness.** [compute/jordan_standalone_theorems.py](compute/jordan_standalone_theorems.py)
`inner_frame_symmetry` (drift of $T_1,T_2,N_3$ under all $6$ frame permutations
$\sim 10^{-14}$), `op2_points` (isotropy $[36,36,36]$, tangent $[16,16,16]$,
$\dim F_4=52$), `delta9_real_spinor` ($\dim\Delta_9=16$, $\mathrm{Spin}(9)$
commutant $=1$). The detailed inner-frame mechanics are in
[compute/three_generations_frame.py](compute/three_generations_frame.py).

**Why this is the interesting observation (and the contrast with triality).** A
recurrent obstruction in algebraic model-building is the Distler–Garibaldi result
that a single $E_8$ cannot contain three "copies" of a fermion module with the
correct chirality, because the order-3 symmetry available there is the **outer**
triality of $D_4=\mathrm{Spin}(8)$, which permutes three *inequivalent*
$8$-dimensional modules $8_v,8_s,8_c$ (and so cannot produce three *like*-chirality
copies). The frame $S_3$ of $\mathfrak{J}_3(\mathbb{O})$ is a different animal: it
is **inner** in the connected group $F_4$, it permutes three **mutually
congruent** points carrying the **same** self-conjugate real spinor $\Delta_9$,
and it therefore cannot pose a "vector-vs-spinor / opposite-chirality mirror"
obstruction at all. Stated purely mathematically: *the order-3 symmetry of a
Jordan frame is inner and congruence-preserving, whereas the order-3 symmetry of
$\mathrm{Spin}(8)$ is outer and class-permuting.* That distinction is the content
of Theorem A.

---

## 4. Theorem B — Schur rigidity of the invariant mean

> **Theorem B.** Let a compact group $G$ act orthogonally and irreducibly on a
> real vector space $V$ of dimension $d$. For any rank-one orthogonal projector
> $P$, the Haar average $\int_G gPg^{-1}\,dg$ equals $\tfrac1d\,I$. Applying this:
> $\Delta_9$ ($d=16$) is $\mathrm{Spin}(9)$-irreducible, so its invariant mean is
> $\tfrac1{16}I$; $\mathfrak{J}_3(\mathbb{O})$ ($d=27$) is **reducible** under
> $F_4$ (the decomposition $27=1\oplus 26$ leaves the trace direction with weight
> $\tfrac13$, so the mean is **not** flat), but is **irreducible** under $E_6$, so
> its $E_6$-invariant mean is $\tfrac1{27}I$. Hence on the product module the
> invariant mean is $\tfrac1{16}\cdot\tfrac1{27}=\tfrac1{432}$ per direction.

**Proof.** The average $M=\int_G gPg^{-1}dg$ is $G$-invariant, so by Schur's lemma
on the real irreducible $V$ it is a scalar $\lambda I$; taking traces,
$\lambda d=\operatorname{tr}P=1$, whence $\lambda=1/d$. For $\Delta_9$ this gives
$1/16$. For $\mathfrak{J}_3(\mathbb{O})$ under $F_4$ the module is **not**
irreducible — $I$ spans a fixed line, $27=1\oplus 26$ — so Schur does not force a
scalar, and indeed the trace direction retains weight $1/3$ (one of three
diagonal idempotents); the mean is not flat. Passing to the larger group $E_6$,
which acts irreducibly on the $27$, Schur applies and the mean is $1/27$. The
product is $1/432$. $\qquad\blacksquare$

**Witness.** [compute/jordan_standalone_theorems.py](compute/jordan_standalone_theorems.py)
`schur_weights`: $\mathrm{Spin}(9)$ commutant $=1$ and mean diagonal $=0.0625=1/16$
(off-diagonal $\sim 10^{-16}$); $F_4$ commutant $=2$ (reducible $1\oplus 26$),
trace-direction weight $\approx 0.333$; $E_6$ commutant $=1$, mean diagonal
$=0.037037=1/27$ (off-diagonal $\sim 10^{-16}$), with the $E_6$ algebra closing at
$\dim 78$. The Reynolds/Schur construction is detailed in
[compute/epsilon_measure_schur.py](compute/epsilon_measure_schur.py) and
[foundations/08_epsilon_measure_theorem.md](foundations/08_epsilon_measure_theorem.md).

**The observation.** The crisp point is the **dichotomy**: the flat weight $1/27$
is *not* a normalisation choice and is *not* available from $F_4$ — it is forced
precisely by enlarging to the cubic-norm group $E_6$ under which the $27$ is
irreducible. The pair $(1/16,1/27)$, and their product $1/432$, are theorems of
Schur's lemma applied to two specific irreducibles, with the $1/27$ pinned to
$E_6$ rather than $F_4$.

---

## 5. Theorem C — a seesaw identity for the Freudenthal cubic

> **Theorem C.** Let $X\in\mathfrak{J}_3(\mathbb{O})$ have characteristic cubic
> $t^3-T_1t^2+T_2t-N_3$ with eigenvalues ordered by magnitude
> $|m_1|\ge|m_2|\ge|m_3|$. Then Vieta's relation gives
> $$
> m_1m_2m_3=N_3,\qquad\text{hence}\qquad m_2m_3=\frac{N_3}{m_1},\quad |m_2m_3|=\frac{|N_3|}{|m_1|}.
> $$
> The product of the two smaller eigenvalues equals the cubic norm divided by the
> largest. **Corollary.** If the subleading invariants are suppressed at integer
> orders $\operatorname{ord}(T_2)=q$ and $\operatorname{ord}(N_3)=Q$ in a small
> parameter, then in the regime $2q\le Q$ the eigenvalue magnitudes sit at orders
> $(0,\,q,\,Q-q)$ to leading order.

**Proof.** The eigenvalues are the roots of the monic characteristic cubic, so
Vieta gives $m_1m_2m_3=N_3$ directly; dividing by $m_1\neq 0$ yields
$m_2m_3=N_3/m_1$. For the corollary, with $T_1=O(1)$ the largest root is
$m_1=O(1)$; the second elementary symmetric $m_1m_2+m_2m_3+m_3m_1=T_2$ is
dominated by $m_1m_2$ when $|m_3|\ll|m_2|$, giving $m_2=O(\text{ord }q)$; then
$m_3=N_3/(m_1m_2)=O(\text{ord }Q-q)$, valid (i.e. $|m_3|\le|m_2|$) exactly when
$2q\le Q$. $\qquad\blacksquare$

**Witness.** [compute/jordan_standalone_theorems.py](compute/jordan_standalone_theorems.py)
`freudenthal_seesaw` verifies the exact identity $|m_2m_3-|N_3|/m_1|/(|N_3|/m_1)\sim
10^{-15}$ over random strongly-hierarchical elements; `order_cascade` checks the
order corollary $(0,q,Q-q)$ in a **generic** small parameter $0.1$ (an arbitrary
mathematical parameter, with $O(1)$ prefactor scatter). The cubic-root machinery
is in [compute/generation_cascade.py](compute/generation_cascade.py). The exact
Vieta identity is the asserted theorem; the order corollary is a leading-order
diagnostic.

**The observation.** Read structurally, $m_2m_3=|N_3|/m_1$ is a **seesaw**: fixing
the cubic norm $N_3$, making one eigenvalue large depresses the product of the
other two. This is nothing more than Vieta on the Freudenthal cubic, but stating
it that way makes the cubic-norm invariant $N_3$ the controlling quantity of a
small-eigenvalue suppression — a clean algebraic identity worth recording on its
own.

---

## 6. Provenance and novelty (stated plainly)

| Ingredient | Status | Source |
|---|---|---|
| Albert algebra $\mathfrak{J}_3(\mathbb{O})$, frames, characteristic cubic | classical | Albert 1934; Jordan–von Neumann–Wigner 1934; Springer 1962; McCrimmon 2004 |
| $F_4=\mathrm{Aut}(\mathfrak{J}_3(\mathbb{O}))$ connected, no outer automorphism | classical | Chevalley–Schafer 1950; Freudenthal 1964 |
| $\mathbb{O}P^2=F_4/\mathrm{Spin}(9)$; $16$-dim real spinor tangent | classical | Freudenthal 1951; Yokota 2009 |
| $E_6$ = reduced structure group; $27$ irreducible | classical | Springer 1962; Jacobson 1971 |
| Schur's lemma; Reynolds/Haar averaging | classical | standard |
| Vieta's formulae for the monic cubic | classical | standard |
| **Decoupled assembly of A, B, C with machine witnesses** | this note | — |
| **Obs. A:** inner frame $S_3$ exempts the picture from an outer-triality obstruction | this note | — |
| **Obs. B:** $F_4$-reducible / $E_6$-irreducible dichotomy pins flat $1/27$ to $E_6$ | this note | — |
| **Obs. C:** Vieta on the cubic norm read as a seesaw | this note | — |

We make no claim that A, B, or C is a deep new theorem. Each follows from
classical structure by a short argument. The contribution is to *separate* this
mathematics cleanly from any physical reading, to state it precisely, and to back
each statement with a reproducible check.

---

## 7. Decoupling from the physical program

This is the load-bearing disclaimer. **Nothing in this note establishes, or is
evidence for, any physical claim.** In particular:

- Theorems A, B, C are statements about $\mathfrak{J}_3(\mathbb{O})$, about
  $F_4/\mathrm{Spin}(9)/E_6$ representation theory, and about Vieta. They are true
  irrespective of whether the wider project's physical interpretation is correct.
- The physical interpretation — identifying frame idempotents with fermion
  generations (ledger bridge `G1`), reading the invariant mean as a flavour
  measure with $\varepsilon_0=\sqrt{\pi/432}$ (bridge `F0`), and the cubic
  seesaw as a mass hierarchy (bridge `A3`) — is developed and gated **separately**
  in [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md). Those bridges remain **open**.
  This note does **not** close them, and must not be cited as if it did.
- Conversely, the validity of A, B, C does not depend on those bridges. That
  independence is the entire point of publishing this layer on its own.

The audit harness enforces this separation: the witness module is registered with
a `diagnostic` contract whose kill conditions forbid presenting these theorems as
evidence that the physical interpretation is derived, forbid claiming novelty for
the classical inputs, and forbid moving any model-comparison ("Bayes") credit on
the basis of this consolidation (see [compute/audit_contract.py](compute/audit_contract.py)).

---

## 8. Reproducibility

```bash
# the decoupled witness for this note (states A, B, C as pure mathematics)
PYTHONDONTWRITEBYTECODE=1 python3 compute/jordan_standalone_theorems.py

# the same results inside the full self-audit (every artifact + its contract)
PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 compute/audit_contract.py
```

Supporting modules: [compute/three_generations_frame.py](compute/three_generations_frame.py)
(Theorem A mechanics), [compute/epsilon_measure_schur.py](compute/epsilon_measure_schur.py)
with [foundations/08_epsilon_measure_theorem.md](foundations/08_epsilon_measure_theorem.md)
(Theorem B), and [compute/generation_cascade.py](compute/generation_cascade.py)
(Theorem C).

---

## References

- A. A. Albert, *On a certain algebra of quantum mechanics*, Ann. of Math. **35** (1934) 65–73.
- P. Jordan, J. von Neumann, E. Wigner, *On an algebraic generalization of the quantum mechanical formalism*, Ann. of Math. **35** (1934) 29–64.
- C. Chevalley, R. D. Schafer, *The exceptional simple Lie algebras $F_4$ and $E_6$*, Proc. Natl. Acad. Sci. USA **36** (1950) 137–141.
- H. Freudenthal, *Oktaven, Ausnahmegruppen und Oktavengeometrie* (1951); *Lie groups in the foundations of geometry*, Adv. Math. **1** (1964) 145–190.
- T. A. Springer, *Characterization of a class of cubic forms*, Indag. Math. **24** (1962) 259–265.
- N. Jacobson, *Exceptional Lie Algebras*, Marcel Dekker (1971).
- K. McCrimmon, *A Taste of Jordan Algebras*, Springer (2004).
- I. Yokota, *Exceptional Lie groups*, arXiv:0902.0431 (2009).
- J. Distler, S. Garibaldi, *There is no "Theory of Everything" inside $E_8$*, Comm. Math. Phys. **298** (2010) 419–436. *(cited only for the outer-triality contrast in §3.)*
