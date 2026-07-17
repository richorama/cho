# The Born Rule From Observer-Consistency

*A self-contained selection theorem: among the `r`-norm probability rules, only the
2-norm is consistent across measurement resolutions, in Hilbert dimension three and above.*

This note isolates one result of the observer-consistency project and states it with a
complete proof. It is self-contained: it assumes only elementary linear algebra and does
not presuppose Gleason's theorem, which it instead reconstructs constructively in the exact
finite setting. The claims are certified over the Gaussian rationals `Q(i)` by the tests
`tests/test_gate_q11_born_selection.py`, `tests/test_gate_q12_frame_consistency.py`, and
`tests/test_gate_born_rule_theorem.py`.

---

## 1. Setup

Let `H` be a complex Hilbert space of finite dimension `d`, and fix a nonzero state vector
`s`. A **sharp measurement** is a rank-one projective measurement, given by an orthonormal
basis `B = {e_1, ..., e_d}`; its outcomes are the directions `e_k`.

For a real exponent `r > 0`, the **`r`-norm rule** assigns the measurement `B` on state `s`
the outcome distribution

```text
q_r(e_k | B, s) = |<e_k|s>|^r / Z_r(B, s),      Z_r(B, s) = sum_{j=1}^{d} |<e_j|s>|^r.   (1)
```

By construction each `q_r(. | B, s)` is a probability distribution. The exponent `r = 2` is
the Born rule, for which `Z_2(B, s) = <s|s>` and `q_2(e | B, s) = |<e|s>|^2 / <s|s>`.

Write `g_r^s(e) = |<e|s>|^r` for the (unnormalised) **frame weight** of a unit effect `e`,
so `Z_r(B, s) = sum_{e in B} g_r^s(e)` is the **frame total** of the basis.

## 2. The observer-consistency demand

An outcome direction `e` can belong to many different sharp measurements. An internal
observer who registers outcome `e` cannot tell which surrounding measurement produced it,
so consistency requires that the probability assigned to `e` not depend on that choice.

> **Non-contextuality.** For every state `s` and every pair of bases `B`, `B'` with
> `e in B` and `e in B'`, the rule assigns `q_r(e | B, s) = q_r(e | B', s)`.

Because the numerator `g_r^s(e)` in (1) is shared, non-contextuality at `e` is equivalent
to equality of the frame totals `Z_r(B, s) = Z_r(B', s)`. Since two bases sharing `e`
differ only in how the orthogonal complement `e^perp` (a `(d-1)`-dimensional space) is
resolved into an orthonormal frame, the demand is exactly:

> **(C)** The frame total over `e^perp` is independent of the orthonormal frame chosen for
> `e^perp`, for every state `s`.

Equivalently, in Gleason's language, `g_r^s` must be a **regular frame function**: its sum
over every orthonormal basis is a single basis-independent constant `W(s)`.

## 3. The theorem

> **Theorem.** Let `d >= 3`. The `r`-norm rule (1) is non-contextual for every state if and
> only if `r = 2`. In that case `q_2(e | B, s) = <e|rho|e>` with `rho = |s><s| / <s|s>`,
> the Born rule. For `d = 2` the non-contextuality demand is degenerate and selects no
> exponent.

The proof is in three parts: sufficiency (r = 2 works, every `d`), necessity (r != 2 fails,
`d >= 3`), and the `d = 2` degeneracy. A fourth remark isolates *why superposition is
essential*.

### 3.1 Sufficiency: `r = 2` is non-contextual (Parseval)

Let `B = {e_k}` be any orthonormal basis. Expanding `s` in that basis,

```text
sum_k |<e_k|s>|^2 = <s|s>,                                                            (2)
```

which is Parseval's identity. The right-hand side does not mention `B`, so `Z_2(B, s)` is
the basis-independent constant `<s|s>`; condition **(C)** holds and

```text
q_2(e | B, s) = |<e|s>|^2 / <s|s> = <e|rho|e>
```

depends only on `e` and `rho`. Non-contextuality holds in every dimension. **∎**

*Exact certificate.* `frame_function.born_is_exactly_parseval(d)` verifies (2) as an exact
identity over `Q(i)` for every declared basis and every census state in `d = 3, 4`
(`test_gate_q12_frame_consistency.py::test_born_frame_sum_is_exactly_parseval`).

### 3.2 Necessity: `r != 2` is contextual for `d >= 3`

It suffices to exhibit one state and one complement `e^perp` whose frame total changes
under a rotation of `e^perp`. Work in the three-dimensional subspace `span{e_0, e_1, e_2}`
with `e = e_0`, and take the state `s = e_0 + e_1 + e_2` (equal superposition).

- **Split A** uses the frame `{e_1, e_2}` for the complement. The two complement weights
  are `|<e_1|s>|^r = 1` and `|<e_2|s>|^r = 1`, so the complement total is `2`.
- **Split B** rotates the complement by the exact rational (Pythagorean) rotation
  `u = (3 e_1 + 4 e_2)/5`, `v = (-4 e_1 + 3 e_2)/5`. Then `<u|s> = (3+4)/5 = 7/5` and
  `<v|s> = (-4+3)/5 = -1/5`, so the complement total is `(7/5)^r + (1/5)^r`.

For `r = 2` both totals equal `2` — consistent, as they must. For any `r != 2` the function
`phi(r) = (7/5)^r + (1/5)^r` is strictly convex in the two weights and does **not** equal
`2`; concretely for `r = 4` it is `(2401 + 1)/625 = 2402/625 != 2`, and for `r = 6` it is
`(117649 + 1)/15625 != 2`. Hence `Z_r(A, s) != Z_r(B, s)`, the shared effect `e_0` receives
two different probabilities, and non-contextuality fails. Embedding this configuration in
any `d >= 3` (leaving the remaining basis vectors fixed) preserves the discrepancy. **∎**

*Exact certificate.* `frame_function.theorem_witnesses()` computes the two splits on
`s = (1,1,1)` and returns, exactly, the whole-basis totals: `r = 2` gives `3 = <s|s>` for
both splits, while `r = 4` gives `3` versus `3027/625` and `r = 6` gives `3` versus
`5331/625` (the extra `1` beyond the complement is the shared effect's own weight
`|<e_0|s>|^r = 1`). See `test_gate_born_rule_theorem.py`.

*Dimension-general certificate.* The embedding "leaving the remaining basis vectors
fixed" is itself made exact by `frame_function.dimensional_necessity_witnesses((3,4,5))`,
which runs the identical `{1,2}`-plane rotation on `s = (1,...,1)` in each dimension. Split
`A` always totals `d`; split `B` totals `(d-2) + c_r/625` with `c_4 = 2402` and
`c_6 = 4706`, so the two disagree for `r in {4,6}` while agreeing at `d` for `r = 2`, in
every dimension `d = 3, 4, 5`. The `d = 3` case reproduces the single-configuration numbers
above (`3027/625`, `5331/625`). This confirms that necessity is not an artefact of `d = 3`.

### 3.3 The `d = 2` degeneracy

For `d = 2` the complement of a fixed effect `e` is one-dimensional, so any basis containing
`e` is `{e, e'}` with `e'` unique up to a phase. Since `|<e'|s>|` is phase-independent, the
frame total `Z_r({e, e'}, s)` is the same for every such basis and every `r`; the
non-contextuality demand is vacuous and selects nothing. This is precisely why the
Gleason-type selection begins at `d = 3`. (For completeness: `d = 2` also admits irregular
frame functions with no density-operator representation, the classical reason Gleason's
theorem excludes the qubit.) **∎**

*Exact certificate.* `born_selection.qubit_cannot_distinguish()`
(`test_gate_q11_born_selection.py::test_selection_requires_dimension_at_least_three`).

### 3.4 Why superposition is essential

The classical representation-change group is the group of outcome **relabelings**
(permutations); the amplitude premise extends it to the **monomial** unitaries
(permutations composed with unit phases). Neither can expose `r != 2`: a monomial map sends
a basis to a permuted, rephased basis, which has the *same multiset of weights*
`{g_r^s(e_j)}`, hence the same frame total for every `r`. Only a genuinely superposing
change of basis — one that mixes distinct rays, as the Pythagorean rotation above does —
alters the total. The selection of the Born rule is therefore powered *precisely* by the
one ingredient the amplitude premise adds over classical relabeling: superposition.

*Exact certificate.* `theorem_witnesses().monomial_invariant_for_all_exponents` is `True`
(`test_gate_born_rule_theorem.py::test_monomial_relabelling_exposes_nothing`), while the census
`frame_function.frame_consistency_census(d)` shows the permutation control clean for every
exponent yet the superposing frames inconsistent for `r != 2`
(`test_gate_q12_frame_consistency.py`).

## 4. Equivalent forms of the conclusion

The theorem admits three interchangeable readings, all established above.

1. **Non-contextuality.** Only `r = 2` assigns a measurement outcome a probability
   independent of the surrounding sharp measurement (Section 3, Q11).
2. **Frame-function / resolution consistency.** Only `r = 2` gives a measurement a total
   probability independent of the orthonormal frame — the project's coarse-graining
   principle applied to a complete measurement (Section 3.1–3.2, Q12).
3. **Gleason representation.** The unique non-contextual rule is `q_2(e) = <e|rho|e>`, the
   Born rule for the density operator `rho = |s><s|/<s|s>`; the constant `W(s) = <s|s>` is
   the Gleason frame constant.

## 5. Scope and non-claims

- The proof of **sufficiency** (Section 3.1) and of the **superposition** and **dimension**
  necessity mechanisms is fully general (all real `r > 0`, all `d`). The exact `Q(i)`
  certificates realise **necessity** for the even exponents `r in {4, 6}` and for the
  enumerated rational bases in `d = 3, 4, 5`; they are constructive finite witnesses, not a
  substitute for the analytic argument, which covers every `r != 2`.
- This selects the probability **calculus**, i.e. the map from effects and states to
  numbers. It says nothing about dynamics, tensor structure, or a preferred observable, and
  in particular does not depend on any result about interacting dynamics elsewhere in the
  project.
- No measured constant, symmetry, or dimension is used as an input or an objective. The
  only premise beyond finite Hilbert space is the observer-consistency demand of Section 2.

## 6. Reproducibility

```bash
python3 -m unittest discover -s tests -p "test_gate_q11*.py" -v
python3 -m unittest discover -s tests -p "test_gate_q12*.py" -v
python3 -m unittest discover -s tests -p "test_gate_born_rule_theorem.py" -v
```

The production module `amplitude_bootstrap/frame_function.py` computes the frame totals and
witnesses as exact rationals; the tests own every asserted value. A typeset, arXiv-ready
LaTeX version of this note is in [paper/born_rule_theorem.tex](paper/born_rule_theorem.tex).
The broader project context is in [PAPER.md](PAPER.md), [AMPLITUDE_PLAN.md](AMPLITUDE_PLAN.md), and
[AMPLITUDE_CONSTITUTION.md](AMPLITUDE_CONSTITUTION.md).
