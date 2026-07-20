# The Octonion Campaign

*Observer-consistency on the last normed division algebra.*

The classical campaign used bits; the amplitude campaign changed exactly one
premise to complex amplitudes over the Gaussian rationals `Q(i)`. This campaign
changes exactly one premise again and takes the final rung of the Cayley-Dickson
ladder `R -> C -> H -> O`: amplitudes become **octonions** over the rationals.

## Why octonions, and why this is the last stop

Each doubling of the ladder loses one property — ordering (`R->C`), commutativity
(`C->H`), then **associativity** (`H->O`). **Hurwitz's theorem (1898)** says
`R, C, H, O` are the *only* normed division algebras: the norm form
`|x|^2 = x conj(x)` is multiplicative exactly up to the octonions and fails at the
next doubling (the sedenions, which have zero divisors). So the Born norm — the
project's `r = 2` invariant — is precisely the composition-algebra norm, and there
are exactly four amplitude worlds that can carry it.

Two structural facts frame the campaign:

- **Gleason's floor meets the octonion ceiling at 3.** The Born-selection theorem
  needs Hilbert dimension `d >= 3`; octonionic quantum mechanics *only* exists up
  to `d = 3`, the exceptional Jordan algebra `h_3(O)`. The window is a single
  dimension wide.
- **Composite systems are expected to fail harder**, sharpening the amplitude
  campaign's honest boundary that observer-consistency buys the probability
  calculus but not interacting dynamics.

## Method (unchanged)

Exact rational arithmetic, exhaustive finite census, predeclared gates with
matched controls, and every scientific claim pinned to a named `unittest`. The
Cayley-Dickson ladder *is* the code: a level-`k` number is a flat tuple of `2**k`
rationals (`jordan_bootstrap/octonion.py`).

## Gate O00 — representation invariance (implemented, passing)

The octonionic successor to amplitude Gate Q00. Representation changes are exact
rational **unit octonions**; the invariant they must preserve is the Born norm
`|x|^2`.

- **240** exactly-representable unit octonions are declared and frozen: the 16
  signed axes `+-e_k` (the octonionic "monomial" subgroup — signed relabeling)
  and 224 genuine two-axis superpositions built from the exact Pythagorean pair
  `(3/5, 4/5)` (the octonionic echo of the amplitude campaign's `(3,4,5)`
  rotations). The size `240` is a coincidence of the construction, **not** the E8
  root system (whose unit octonions are irrational).
- **Norm invariance is exact:** over 4800 checks, unit-octonion multiplication
  moves no Born norm (`0` mismatches), and the unit set is closed under
  multiplication (57600 checks, `0` non-units) — the exact echo of Hurwitz
  multiplicativity.
- **Controls bite:** every non-unit scaling is rejected (60/60), the algebra is
  genuinely non-associative (168 basis triples fail associativity), the
  quaternion sub-level still associates, every nonzero octonion has an exact
  two-sided inverse, and the ladder's kill condition is exhibited — one doubling
  past the octonions the norm identity breaks, `(e_1+e_10)(e_4+e_15)` giving norm
  `8 != 4`.

Contract: `tests/test_gate_o00_representation_invariance.py`. Package:
`jordan_bootstrap/`.

## Next gates (planned)

- **O01** — exact frame-function / Born selection on octonionic amplitudes:
  *implemented, passing* (see below).
- **O0x** — the composite-system wall: show tensoring fails and state the sharpened
  no-go for interacting octonionic dynamics.

## Gate O01 — frame-function / Born selection (implemented, passing)

The octonionic successor to amplitude Gates Q11/Q12. A state is a vector in
`O**d`; an orthonormal frame is an exact rational orthogonal matrix acting on the
coordinates; the `r`-frame total is `sum_i |(O s)_i|^r`, an exact rational for even
`r`. The question: which `r` gives a total independent of the frame?

- **Only `r = 2` survives.** Over the declared census (10 states across `d = 3, 4`)
  the Born total is exactly frame-invariant (`0 / 20` mismatches — Parseval for the
  octonion norm), while `r = 4` and `r = 6` are contextual (`6 / 10` states
  disagree between the two frames).
- **It reproduces the complex Born theorem exactly.** The `(1,1,1)` witness state
  gives frame totals `3` (both frames) at `r = 2`, but `3` vs **`3027/625`** at
  `r = 4` and `3` vs **`5331/625`** at `r = 6` — the identical rationals of
  `BORN_RULE_THEOREM.md`, now with octonionic amplitudes. The same discrepancy
  appears for the imaginary-unit state `(e_1, e_1, e_1)`, so the selection is not a
  real-amplitude artefact.
- **Superposition is essential (octonionic monomial control).** Right-multiplying
  every coordinate by a fixed *unit octonion* leaves the whole multiset of weights
  unchanged for every `r` (`0 / 120` mismatches, Hurwitz / Gate O00), so the
  octonionic relabeling group can never expose `r != 2`. Only a genuinely
  superposing rational rotation does.

Contract: `tests/test_gate_o01_frame_consistency.py`.

## Next gates (planned, continued)

- **O02** — Born selection on the exceptional Jordan algebra `h_3(O)`:
  *implemented, passing* (see below).
- **O0x** — the composite-system wall and the interacting-dynamics no-go.

## Gate O02 — Born selection on h_3(O) (implemented, passing)

Gate O01 selected the norm rule for octonion coordinate vectors; this gate moves
to the honest home of octonionic quantum states: the exceptional Jordan algebra
`h_3(O)` of 3x3 Hermitian octonionic matrices under `A o B = (AB + BA)/2`. Its
rank-one primitive idempotents (`P o P = P`, `tr P = 1`) are the pure states --
the octonionic projective plane `OP^2` -- and a Jordan frame resolves the
identity into three orthogonal idempotents. The Born rule is the trace form
`tr(P o Q)`.

Two genuinely Jordan-algebraic results, both exact:

- **Gleason on `h_3(O)`.** For every declared state and every Jordan frame the
  trace-form total `sum_i tr(P o Q_i)` equals `tr(P)` (`0 / 8` mismatches) -- the
  frame resolves the identity, so the Born total is frame-independent. The two
  declared frames are verified exact resolutions of the identity (`2 / 2`).
- **Non-associativity obstructs statehood.** Three declared rational unit vectors
  whose octonion entries span a non-associative triple give outer products that
  are Hermitian and unit-trace yet are **not** idempotent (`3 / 3` fail), so they
  are not points of `OP^2`. Not every octonionic ray is a state -- the first
  honest wall the octonions raise, and it appears already at the level of what
  counts as a pure state. The four quaternionic (associative) unit vectors, by
  contrast, all give genuine primitive idempotents (`4 / 4`).

The `(1,1,1)` superposition remains contextual at `r = 4` inside the idempotent
picture, tying O02 back to O01 and the complex Born theorem.

Contract: `tests/test_gate_o02_jordan_born_selection.py`.

## Next gates (planned, continued)

- **O03** — the composite-system wall: *implemented, passing* (see below).

## Gate O03 — the composite-system wall (implemented, passing)

Gates O00-O02 built a consistent *single* octonionic system. This gate asks
whether two can be composed, and finds the honest wall. Composing observables (a
tensor product of state spaces) needs an *associative* envelope: ordinary QM's
`h_n(C)` is *special*, sitting inside `M_n(C)`, and that associative product is
what makes `M_m(C) tensor M_n(C) = M_{mn}(C)`. Octonionic matrix multiplication is
non-associative, so no envelope exists.

- **The mechanism, exact.** Octonionic 3x3 matrix multiplication has a nonzero
  associator: the `(e_1, e_2, e_4)` route gives the exact witness `2 e_7` at entry
  `(0,0)`. Every declared octonionic triple fails to associate (`3 / 3`), while
  every complex realization (`0 / 2`) and every quaternionic realization (`0 / 3`)
  associates exactly -- because `C` and `H` are associative and give composable
  `h_n`.
- **Why the wall is exactly at `h_3(O)`.** By Artin's theorem any *two* octonions
  generate an associative subalgebra (verified over a frozen set of pairs and every
  length-3 word), so an `h_2(O)` realization would still compose; the obstruction
  needs three independent imaginary directions -- the same size at which the
  octonionic projective plane exists at all.

Non-claim: this is the finite *mechanism*, consistent with Albert's theorem that
`h_3(O)` is exceptional (not special) and Zelmanov's classification, not a
re-derivation. Operationally it sharpens the amplitude campaign's boundary:
octonionic quantum mechanics is a consistent single-system probability calculus
with *no* composite (hence no interacting) extension.

Contract: `tests/test_gate_o03_composite_wall.py`.

## Gate O04 — automorphism invariance (implemented, passing)

O00 asked only that *relabelling* the octonionic axes (signed permutations of the
basis) leaves the Born probabilities alone. This gate strengthens that to the real
symmetry: the finite group of genuine *algebra automorphisms* of the octonions,
and lifts it to `h_3(O)`.

- **The group, exact.** The monomial automorphisms — those sending each basis
  imaginary `e_i` to a signed basis element `+/- e_j` — form a group of order
  exactly **1344 = 168 x 8**. The 168 is `|GL(3,2)| = |PSL(2,7)|`, the collineation
  group of the Fano plane (the multiplication table of `O`); the 8 = 2^3 are the
  independent sign changes on the three generators. This is the finite skeleton of
  the continuous automorphism group `G_2`, computed by census, not asserted.
- **Every element is verified.** Each of the 1344 candidates is checked to satisfy
  `phi(x y) = phi(x) phi(y)` on the basis and to preserve the octonion norm
  (`1344 / 1344`, zero mismatches).
- **Born invariance, exact.** Lifting an automorphism entrywise to `h_3(O)` gives a
  Jordan automorphism: over the full census (`4032` checks each, zero failures) it
  preserves the trace, sends primitive idempotents (pure states) to primitive
  idempotents, is a homomorphism for the Jordan product, and — the headline —
  leaves every trace-form Born probability `tr(P . Q)` exactly invariant.

Where O00 showed the probabilities don't care how you *name* the axes, O04 shows
they don't care about any *symmetry of the algebra itself*: the whole `G_2`-flavoured
1344-element group is a symmetry of the octonionic Born calculus. This is the exact,
finite analogue of unitary invariance in the complex campaign.

Non-claim: this exhibits the finite monomial subgroup and its invariance, not the
full continuous `G_2` or a classification of Jordan automorphisms of `h_3(O)`
(which is `F_4`).

Contract: `tests/test_gate_o04_automorphism_invariance.py`.

## Gate O05 — Kochen-Specker contextuality: the rational verdict (implemented, passing)

The amplitude campaign found state-independent contextuality (Gate Q08) through the
Peres-Mermin magic square -- a *two-qubit* construction in `M_4(C)`. That road is
closed here: O03 proved octonions admit no composite system, so the magic square
cannot even be assembled over `O`. The only remaining road is the original
single-system Kochen-Specker theorem in dimension three -- exactly where `h_3(O)`
lives. A *context* is a Jordan frame; a deterministic non-contextual value-state is a
`{0, 1}` labelling of the rays giving exactly one `1` per context.

Under this repo's exact-rational discipline a ray must be a *rational* unit vector: a
primitive integer vector `(a, b, c)` whose norm is a perfect square (only then is the
normalized vector rational and `outer(v)` an exact primitive idempotent of `h_3(O)`).
Over these rays the Kochen-Specker obstruction disappears, constructively:

- **Lemma 1.** A primitive integer vector with perfect-square norm has exactly one odd
  coordinate. (Mod 4 a square is `0` or `1`; the norm is congruent to the number of
  odd coordinates, ruling out three; primitivity rules out zero.) Verified over the
  whole census (`219 / 219` rays at bound 13).
- **Lemma 2.** Two orthogonal such rays carry their odd coordinate in *different*
  positions -- else their dot product would be odd, hence nonzero. Verified on every
  orthogonal pair (`303 / 303`).
- **Corollary (Godsil-Zaks, 1988).** Label a ray `1` iff its unique odd coordinate is
  in position `0`. By Lemma 2 the three rays of any context occupy distinct positions,
  so exactly one is labelled `1`: an explicit, exact, deterministic non-contextual
  value-state on *all* rational rays at once (`0` context violations over `69`
  contexts). Every ray is verified to lift to a genuine primitive idempotent and every
  context to a genuine Jordan frame over the octonion Jordan product.

So both roads to contextuality close over the exact-rational octonions: the composite
road by O03, the single-system road by an explicit rational colouring. Genuine
Kochen-Specker contextuality in `d = 3` is an *irrational* phenomenon, invisible at the
resolution this campaign computes in. Meanwhile the octonionic Born rule stays a
*different*, probabilistic non-contextual assignment: for the genuinely octonionic
state used here, each context's three Born probabilities sum to exactly `1` (`0`
violations over `69` contexts).

Non-claim: this is the exact-rational verdict, not a claim that octonionic quantum
mechanics is non-contextual over its irrational closure, and not a re-proof of
Kochen-Specker or of Godsil-Zaks in full generality -- it exhibits the explicit
colouring and certifies it on the octonionic algebra.

Contract: `tests/test_gate_o05_contextuality.py`.

## Non-claims

This campaign selects (or fails to select) the probability calculus in an exotic
amplitude ring. It does not derive the Standard Model. Suggestive links between
`h_3(O)`, `F4`/`E6`/`E8`, and particle content exist in the literature but remain
numerology-adjacent until dynamics are derived, which this framework structurally
cannot yet do.
