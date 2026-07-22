# The Octonion Campaign

*Observer-consistency on the last normed division algebra.*

> **Current status: parked.** This file is a historical gate narrative. The claim
> classification, empirical caveats, and operator go/no-go verdict in
> [SCIENTIFIC_STATUS.md](SCIENTIFIC_STATUS.md) supersede stronger interpretations
> below. In particular, O26-O31 are conditional flavour conjectures, not derived
> physics.

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

## Gate O06 — Born as the unique frame-consistent rule (implemented, passing)

Gates O01-O02 *assumed* the trace-form Born rule. This gate turns the exponent into a
holdout and asks whether observer-consistency forces it -- reproducing the amplitude
campaign's selection (Q11/Q12) one algebra higher, on the exceptional Jordan algebra.

Take the family of `p`-power rules assigning a ray `P` the weight `t(P)^p`, where
`t(P) = tr(P o Psi)` is the exact rational Born weight of a genuinely octonionic state
`Psi = outer(2/3, (2/3) e_1, (1/3) e_2)`. Observer-consistency is *frame-consistency*:
the total weight over the three rays of a Jordan frame must not depend on which frame
the observer chose. Over the rationals (bound 15: 107 contexts, 15 shared rays):

- **`p = 1` (Born).** `sum_i tr(P_i o Psi) = tr(Psi o I) = tr(Psi) = 1` for *every*
  frame -- the resolution of the identity is an octonionic Parseval identity. The frame
  total is the single value `1` and a shared ray's normalised probability is
  frame-independent (`0` contextual discrepancies).
- **`p = 2` and `p = 3`.** The frame total takes 16 distinct values, so a ray shared
  between two frames is assigned two different normalised probabilities -- `14` shared
  rays are contextual for each exponent, exact over the rationals. Concretely the ray
  `(0,1,0)` has Born weight `4/9`; in the computational frame its `p = 2` total is
  `11/27` (probability `16/33`) but in `{(4,0,3),(3,0,-4),(0,1,0)}` it is `6011/16875`
  (probability `10000/18033`).
- **Superposition does the selecting.** Permuting the three rays of a frame (a classical
  relabelling) leaves the total unchanged for every exponent, so only a genuinely
  superposing change of frame exposes `p > 1`.

Hence `p = 1` -- the trace-form Born rule -- is the *unique* frame-consistent exponent
(`frame_consistent_exponents == (1,)`), and the selection survives intact on the
non-associative `h_3(O)`.

Non-claim: this selects the Born *exponent* within the `p`-power family via
frame-consistency (a Gleason-style test), not a from-scratch re-proof of Gleason's
theorem or a classification of all frame functions on `h_3(O)`.

Contract: `tests/test_gate_o06_born_selection.py`.

## Gate O07 — the dimension threshold (implemented, passing)

O06 selected `p = 1` as the unique frame-consistent exponent on `h_3(O)`. Is that real,
or an artefact? This gate drops to the two-dimensional spin factor `h_2(O)` (`J(9)`) and
shows the selection *switches off* -- exactly at Gleason's dimension threshold, and
exactly where the octonions run out of room (Hurwitz caps the composition algebras and
O03 caps the Jordan matrix size, both at three).

Over a census of 82 rational unit rays (bound of witnesses on assorted octonion axes):

- **Every ray is a state (Artin).** O02's wall -- a unit vector whose entries share no
  associative subalgebra failing to be idempotent -- cannot arise with only two entries:
  any two octonions generate an associative subalgebra, so `outer(v)` is a primitive
  idempotent for *every* rational unit two-vector, verified `82 / 82` (including
  cross-Fano-line placements like `e_1, e_4`).
- **The complement is forced.** The orthogonal complement of a ray in `d = 2` is a
  single ray, so the only frame containing `P` is `{P, I - P}`
  (`max_frames_sharing_a_ray = 1`), and no ray is shared between distinct frames
  (`rays_shared_across_distinct_frames = 0`).
- **The selection is vacuous.** With no shared rays there is nothing for contextuality
  to distinguish, so *every* exponent is frame-consistent
  (`frame_consistent_exponents == (1, 2, 3)`), against `(1,)` on `h_3(O)`. Parseval
  (`tr(P o Psi) + tr((I - P) o Psi) = 1`) still holds for `p = 1`, but it no longer
  *selects* `p = 1`.

So contextual selection of the Born rule is a genuinely `d >= 3` phenomenon on the
octonions -- the same threshold Gleason's theorem carries.

Non-claim: this exhibits the threshold on an explicit rational census of the spin
factor, not a general proof that no `d = 2` frame function distinguishes exponents.

Contract: `tests/test_gate_o07_dimension_threshold.py`.

## Gate O08 — triality: the S_3 symmetry of the three octonionic slots (implemented, passing)

O04 certified the *entrywise* symmetries of `h_3(O)` -- the octonion automorphisms
(`G_2`'s finite skeleton) applied to each entry, fixing the matrix positions. This gate
certifies the complementary symmetry O04 cannot reach: the one that *moves the
positions*, and identifies it as triality. Writing a Hermitian octonionic matrix with
real diagonal `a, b, c` and three off-diagonal octonion slots `x, y, z`, conjugation by
a `3x3` permutation matrix (`phi(A)_{ij} = A_{sigma(i),sigma(j)}`) is a Jordan
automorphism for every `sigma` -- a reindexing of the matrix-product sum that is valid
despite non-associativity.

Over the rationals the census confirms:

- **The six permutations form an `S_3` of Jordan automorphisms**, each preserving the
  trace, primitive idempotents, Jordan frames, and every Born trace-form probability
  (`270 / 270` checks, zero mismatches).
- **The three-cycle has order three and rotates the three off-diagonal slots**
  `x -> z -> y -> x` (verified by slot occupancy). Those three slots carry the three
  inequivalent eight-dimensional `Spin(8)` representations `8_v, 8_s, 8_c`, and the
  cyclic permutation rotating them is the finite shadow of *triality* -- the order-three
  outer automorphism of `Spin(8)` that only the octonions possess (`R, C, H` have none).
- **It is genuinely new.** A permutation moves content between matrix positions, so it is
  *not* an entrywise O04 automorphism (checked against the whole 1344-element group);
  composing a permutation with an O04 monomial still preserves every Born probability
  (`216 / 216`), so the two symmetries generate a strictly larger finite subgroup of
  `F_4 = Aut(h_3(O))` under which the octonionic Born rule is invariant.

Non-claim: this exhibits the finite `S_3` (geometric) triality that permutes the three
slots, not the full continuous triality of `Spin(8)` nor all of `F_4`.

Contract: `tests/test_gate_o08_triality.py`.

## Gate O09 — the octonionic spectral theorem (implemented, passing)

Every prior gate manipulates states; this one certifies the structure that makes
"measure an observable" rigorous. An observable is any Hermitian octonionic `3x3` matrix
`A`, and the spectral theorem resolves it as `A = lambda_1 P_1 + lambda_2 P_2 +
lambda_3 P_3` with *real* eigenvalues and a Jordan frame `{P_i}` of pointer states,
recoverable from `A` alone. Exact over the rationals:

- **A cubic minimal polynomial (Cayley-Hamilton).** Although `h_3(O)` is non-associative
  and 27-dimensional, every Hermitian `A` satisfies the *cubic*
  `A^3 - T A^2 + S A - N I = 0`, with `T = tr A`, `S`, and the cubic norm `N` read off
  from the traces of the Jordan powers of `A` (Newton's identities). This is the
  degree-three structure of the *cubic* Jordan algebra, and `N` is the `E_6`-invariant
  determinant. Verified to vanish exactly for arbitrary rational Hermitian octonionic
  matrices -- including two with irrational eigenvalues, where only the coefficients stay
  rational (`2 / 2` generic cases).
- **Sylvester recovery.** For rational distinct eigenvalues the projectors come back from
  `A` by `P_i = prod_{j != i}(A - lambda_j I)/(lambda_i - lambda_j)` (a polynomial in the
  single element `A`, unambiguous by power-associativity). Over three cases -- two real
  frames and one genuinely octonionic (`e_1`-valued) frame -- the recovered `P_i` equal
  the original frame, satisfy `A o P_i = lambda_i P_i` and `sum P_i = I`, reproduce `A`,
  and the determinant equals the eigenvalue product.
- **Born expectation over the spectrum.** For a genuinely octonionic state `Psi`,
  `tr(A o Psi) = sum_i lambda_i tr(P_i o Psi)` exactly (`0` mismatches) -- expectation
  value as eigenvalue times outcome probability.

So an octonionic observable has a genuine real spectrum and a measurement frame -- the
last structural prerequisite behind the Born gates O01-O06.

Non-claim: this certifies the spectral resolution on an explicit rational census (cubic
Cayley-Hamilton on arbitrary Hermitian `A`, Sylvester recovery for rational spectra), not
a general constructive diagonalisation of every octonionic observable over its irrational
spectral closure.

Contract: `tests/test_gate_o09_spectral_theorem.py`.

## Gate O10 — colour SU(3) from the octonionic complex structure (implemented, passing)

Gates O00–O09 all stay *inside* a fixed octonion algebra. This gate asks what
continuous symmetries the octonions themselves have, and finds the first bridge
back to particle physics — done as an exact rational computation, not a numerical
Lie-theory approximation.

A **derivation** is a linear map `D` obeying the Leibniz rule
`D(x y) = D(x) y + x D(y)`; derivations form a Lie algebra under the commutator
bracket. We do not assume Cartan's theorem — we *solve the Leibniz system exactly
over the rationals* (512 linear equations in the 64 entries of `D`) and count the
null space:

- **`Aut(O) = G2`.** The derivation algebra is exactly **14-dimensional**, and its
  Killing form `K(X,Y)=tr(ad_X ad_Y)` is exactly negative definite — the compact
  real form of the exceptional Lie algebra `g2`.
- **Fix one imaginary unit `u` and colour SU(3) appears.** Imposing the single
  extra linear condition `D(u)=0` collapses the algebra to exactly
  **8 dimensions**. Three exact certificates pin it to `su(3)`: it is bracket
  closed (a subalgebra); its Killing form is non-degenerate and negative definite
  (compact semisimple, so no abelian `u(1)` factors); and dimension 8 is not a sum
  of smaller compact-simple dimensions (only `su(2)=3` exists below it, and
  `3+3=6`, `3+3+3=9`), forcing *simple* — hence the unique 8-dimensional compact
  simple algebra `A2 = su(3)`, the colour gauge algebra of the strong force.
- **The quark `3` and the singlet `1`, for free from the Leibniz rule.** Because
  `D(u)=0`, every fixing derivation commutes with left multiplication `L_u`
  (`D(u x)=D(u)x+u D(x)=u D(x)`), and octonionic alternativity gives `L_u^2=-I`.
  So `L_u` is an exact **complex structure** on the six imaginaries orthogonal to
  `u`: they become `C^3`, `su(3)` acts complex-linearly (the quark triplet `3` and
  antiquark `3bar`), and the fixed direction `u` is a colourless singlet `1`. This
  is Günaydin–Gürsey (1973) colour `SU(3)`, verified here exactly. The choice of
  axis `u` is immaterial (checked on two axes).

So the exceptional algebra that carried every prior gate *contains the strong
force's colour symmetry* as the stabiliser of a complex direction.

Non-claim: this exhibits `su(3)` (with a genuine `3 ⊕ 3bar ⊕ 1` complex
structure) as the exact octonionic complex-structure stabiliser; it is **not** a
derivation of the full Standard Model gauge group `SU(3)×SU(2)×U(1)`, nor of
three generations, nor any dynamics — it is kinematics/representation theory,
made exact.

Contract: `tests/test_gate_o10_color_su3.py`.

## Gate O11 — one fermion generation's charges from ℂ⊗𝕆 (implemented, passing)

Gate O10 found colour `su(3)` as the derivations of `𝕆` fixing an imaginary
unit. This gate takes the complementary half of the Günaydin–Gürsey / Furey
picture: it builds an explicit **fermionic Fock space** inside the complex
octonions `ℂ⊗𝕆` and reads off the electric charges of a *single* Standard-Model
generation — exactly over the Gaussian rationals `ℚ(i)`. The construction is
forced, not fitted:

- **A Clifford algebra.** The seven left-multiplications `L_{e_k}` by the
  imaginary octonion units are mutually anticommuting square roots of `−1`:
  `{L_i, L_j} = −2 δ_ij I` (checked exactly over `ℚ`). They generate `Cl(0,7)` on
  the eight real dimensions of `𝕆`.
- **A fermionic ladder.** Complexifying with the `ℂ` in `ℂ⊗𝕆` and pairing six of
  those operators gives three ladder operators `α_k = (L_{2k−1} + i L_{2k})/2`
  satisfying the canonical anticommutation relations exactly:
  `{α_j, α_k†} = δ_jk I`, `{α_j, α_k} = 0`, `α_k² = 0`. So `ℂ⊗𝕆` (eight complex
  dimensions) *is* the Fock space of three fermionic modes, `2³ = 8` states.
- **Charge is the number operator.** `N = Σ_k α_k† α_k` has exact integer spectrum
  with multiplicities **`(1, 3, 3, 1)`** across eigenvalues `0, 1, 2, 3` — the
  graded pieces `1 ⊕ 3̄ ⊕ 3 ⊕ 1`. Dividing by three gives electric charges
  **`0, 1/3, 2/3, 1`**: a neutrino, an anti-down quark (colour `3̄`), an up quark
  (colour `3`) and a positron — one full isospin-up generation, with the ladder
  lowering charge by one unit (`[N, α_k] = −α_k`).
- **Unbroken `SU(3) × U(1)`.** The nine bilinears `α_j† α_k` preserve `N`; their
  eight traceless combinations close under the bracket into colour `su(3)`, and
  `N` itself generates the commuting `u(1)` of electric charge. Colour acts inside
  each charge sector — trivially on the two singlets, as `3`/`3̄` on the two
  three-dimensional sectors.

Honest boundary (checked, not assumed): this `su(3)` is Furey's ladder-bilinear
embedding and is a *different* embedding from Gate O10's derivation `su(3)` — the
O10 derivations do **not** commute with `N` (only 1 of 8 do), so the two colour
algebras are not identified here.

Non-claim: this exhibits colour `SU(3) × U(1)_em` acting on **one** generation
with the correct charges. It is not the electroweak `SU(2)`, not the origin of
three generations, and not any dynamics — it is exact representation theory of
`ℂ⊗𝕆`, no more.

Contract: `tests/test_gate_o11_fermion_charges.py`.

## Gate O12 — three generations via triality: an honest negative result (implemented, passing)

The Standard Model has *three* fermion generations, and it is often speculated
(Furey 2018 and others) that `Spin(8)` triality — the same triality made finite
in Gate O08 — supplies them as three cyclically-related copies of the `ℂ⊗𝕆`
ideal of Gate O11. This gate tests that hope *exactly* and reports what the
arithmetic says, not what one would like.

Three pairings of the six paired imaginary axes are cyclically permuted by an
explicit order-three axis map `σ = (e₂ e₄ e₆)` (`σ³ = id`) — a concrete `Z₃`
echo of triality. The exact census shows both halves of the honest picture:

- **Each grading is a full generation.** All three pairings give the identical
  charge spectrum with multiplicities **`(1, 3, 3, 1)`** — one generation each.
- **But they are not independent generations.** Each Fock tower already spans the
  *entire* eight-complex-dimensional `ℂ⊗𝕆`. The three towers therefore coincide as
  a single module: their combined span is **`8`, not `24`**, and the three vacua
  span only **`2`** dimensions, not `3`. Triality permutes three *charge-gradings
  of one module*; it does not manufacture three linearly independent generations.

So within `ℂ⊗𝕆` alone, triality does **not** solve the generation problem — a
precise, machine-checked *no* that matches the open status of the literature. This
is the campaign's first deliberately negative gate, and it is exactly the kind of
claim the project's discipline exists to make honestly.

Non-claim: this is a boundary result. It does not rule out generations from
triality in the larger algebra `ℂ⊗ℍ⊗𝕆` or other constructions; it certifies only
that the naive "three triality-related ideals of `ℂ⊗𝕆`" are one module in
disguise.

Contract: `tests/test_gate_o12_generations.py`.

## Gate O13 — weak isospin SU(2) from the quaternions (implemented, passing)

Colour `su(3)` (O10/O11) lives in the octonions; the Standard Model's other
non-abelian factor, weak isospin `SU(2)_L`, does not — in the Furey/Dixon
programme it comes from the *quaternions* `ℍ`, one rung down the same
Cayley–Dickson ladder the octonion module already implements. Exactly over `ℚ(i)`:

- **`su(2)` is the imaginary quaternion left-multiplications.** Because `ℍ` is
  associative, `L_a L_b = L_{ab}`, so the three imaginary units obey
  `[L_i, L_j] = 2 L_k` cyclically with `L_a² = −I` — the weak isospin algebra
  (dimension 3, bracket closed, compact). The unit quaternions are the group
  `SU(2) = Sp(1)`.
- **A weak doublet.** Complexifying and pairing two generators gives a fermionic
  ladder `β = (L_i + i L_j)/2` with `{β, β†} = I` and `β² = 0`. Its number
  operator has eigenvalues `0, 1`; shifting by `−1/2` gives `T₃ = ∓1/2` — a
  left-handed weak doublet (down-type, up-type). `ℂ⊗ℍ` carries two such doublets.

Non-claim: this exhibits `su(2)` weak isospin and its doublet from `ℍ` alone. It
is a *separate* algebra from the octonionic colour `su(3)`; this gate does **not**
assemble the full gauge group `SU(3) × SU(2) × U(1)` on `ℂ⊗ℍ⊗𝕆` (Furey 2018), nor
address chirality, the Higgs mechanism, or the dynamics that break `SU(2)_L`.

Contract: `tests/test_gate_o13_weak_isospin.py`.

## Gate O14 — anomaly cancellation forces the hypercharges; sin²θ_W = 3/8 (implemented, passing)

The campaign's first result aimed at a *number* rather than a group. Gates
O10–O13 recovered the Standard Model's gauge algebra and one generation's
colour/isospin representations from the division algebras — but representations
are structure, and the hypercharges `Y` (the ugly rationals `1/6, −2/3, 1/3,
−1/2, 1`) look arbitrary. This gate proves, exactly over `ℚ`, that they are
*forced*: quantum consistency leaves no freedom.

A chiral gauge theory is consistent only if its gauge and mixed
gauge–gravitational **anomalies cancel**. For one generation of left-handed Weyl
fermions in the representations fixed by O10–O13 (`Q=(3,2,Y_Q)`, `u^c=(3̄,1,Y_u)`,
`d^c=(3̄,1,Y_d)`, `L=(1,2,Y_L)`, `e^c=(1,1,Y_e)`, with `Q = T₃ + Y`) all six
conditions are computed here *from the representation content itself* — `[SU(3)]³`,
`[SU(3)]²U(1)`, `[SU(2)]²U(1)`, `[U(1)]³`, `[grav]²U(1)`, and Witten's global
`SU(2)` parity — and every one **vanishes exactly** for the SM assignment.

The forcing is the payoff. Solving the three linear conditions leaves a
two-parameter family; fixing the `U(1)` scale by the single electric charge Gate
O11 already derived (the up-type quark carries `Q = 2/3`, so `Y_Q = 1/6`) reduces
the cubic `[U(1)]³` condition to the quadratic

    −3Y² − Y + 2/3 = −(1/3)(3Y − 1)(3Y + 2),

whose only roots are `Y = 1/3` and `Y = −2/3` — exactly the down- and up-type
hypercharges, the two roots being the physically irrelevant `u ↔ d` relabelling.
The entire hypercharge spectrum is pinned to the Standard Model: **charge
quantisation is a theorem, not an input.** Finally the weak mixing angle in the
grand-unified normalisation,

    sin²θ_W = (Σ T₃²) / (Σ Q²) = 2 / (16/3) = **3/8**,

an exact rational summed over the generation — the value SU(5)/SO(10) unification
predicts at the unification scale.

Non-claim: this derives the *ratios* of the hypercharges from anomaly freedom and
one charge normalisation; it does not derive the electroweak scale, the running of
`sin²θ_W` down to the measured low-energy `≈ 0.231`, or why nature is anomaly-free.
The `3/8` is the tree-level GUT value, not the laboratory one.

Contract: `tests/test_gate_o14_hypercharge.py`.

## Gate O15 — the octonionic dynamics wall, measured exactly (implemented, passing)

Every gate up to here is *kinematics*: which states, frames, charges and gauge
algebras the division algebras permit. This gate finally confronts what the
octonions are famous for breaking — **dynamics** — and measures the break exactly
over `ℚ`.

Ordinary quantum evolution is a one-parameter unitary group `U(t) = exp(−iHt)`.
It works for two reasons: a single generator associates with itself
(`U(t)U(s)=U(t+s)`), and *independent* evolutions compose through
Baker–Campbell–Hausdorff, whose consistency is exactly the **Jacobi identity** —
the generators form a *Lie algebra*. Over `𝕆` the second pillar collapses.

What survives, so the flow still runs:

- **Alternativity / power-associativity.** The associator `[x,y,z]=(xy)z−x(yz)` is
  totally alternating, so a *single* generator integrates to a well-defined,
  norm-preserving one-parameter flow — a lone octonionic clock is fine.
- **Moufang identities** hold exactly on every basis triple: `𝕆` is a Moufang
  loop, not lawless.
- **Isometry.** Since `𝕆` is a normed algebra, `|ux|=|u||x|` without
  associativity, so a discrete flow `xₙ₊₁ = u xₙ` by a unit `u` preserves the norm
  exactly — evolution is still "unitary-like".

The wall:

- **Jacobi fails** on `168` of the `343` imaginary basis triples, so the imaginary
  octonions under `[,]` are **not a Lie algebra**: there is no octonionic unitary
  group and no ordinary way to compose two independent evolutions.
- **The obstruction is exactly the non-associativity:** `J(x,y,z) = 6·[x,y,z]`
  identically. The failure to compose evolutions *is* six times the associator.
- **Path-ordering defect.** Composing two flow steps two ways, `(uv)x` versus
  `u(vx)`, yields two *different* unit-norm states whose difference is exactly the
  associator `[u,v,x]` — the observable dynamical signature of the wall.

What replaces the Lie law:

- **Malcev structure.** The generators close not into a Lie algebra but into a
  **Malcev algebra**: the Malcev identity `J(x,y,[x,z]) = [J(x,y,z),x]` holds
  exactly on all `343` imaginary basis triples. The very triples where Jacobi
  fails still satisfy Malcev. Octonionic infinitesimal dynamics is governed by the
  strictly weaker, non-Lie Malcev law.

Non-claim: this does **not** construct an octonionic quantum dynamics or a new
equation of motion. It is a machine-checked *no-go plus what survives* — it proves
the exact obstruction to the usual dynamics (Jacobi fails ⇒ no unitary group) and
names the precise structure any octonionic dynamics must respect (Malcev, not
Lie). It does not integrate a flow of two independent generators, derive a
Hamiltonian, or resolve how physics evades the wall.

Contract: `tests/test_gate_o15_dynamics_wall.py`.

## Gate O16 — octonionic evolution as exact rotations: where the wall lives (implemented, passing)

Gate O15 proved a negative in *abstract algebra*: the imaginary octonions under
the commutator are Malcev, not Lie, so there is no octonionic unitary group. This
gate makes the wall *operational* by representing each evolution step as a
concrete exact linear map `x ↦ u x` on the eight-dimensional state space, and asks
the sharp question — *where exactly* does the non-associativity obstruct dynamics?

- **Every unit-octonion step is an exact rotation.** For the left-multiplication
  matrix `L_u`, `L_uᵀ L_u = |u|² I`; a unit generator gives `L_u ∈ O(8)` and an
  imaginary unit a skew `L_a ∈ so(8)`. Evolution steps are rigid isometries.
- **A single generator integrates to a genuine one-parameter group.** Since the
  subalgebra of one element associates, `L_uⁿ = L_{uⁿ}` exactly — a lone octonionic
  clock is a real one-parameter subgroup of `SO(8)`.
- **The generators close into a real Lie algebra, `so(8)`.** The seven imaginary
  `L_a` are independent and their repeated commutators span exactly `28` dimensions
  `= dim so(8)`. As *operators*, the octonionic flows form an honest Lie algebra.
- **The wall lives in the map, not the operators.** `u ↦ L_u` is **not** a
  homomorphism: `L_u L_v ≠ L_{uv}`, and the defect applied to a state is exactly the
  associator of Gate O15 (`(L_u L_v − L_{uv})x = −[u,v,x]`, verified column by
  column). The octonion Moufang loop has no faithful left-multiplication
  representation; the entire non-associativity is this one defect.
- **The surviving substitute is Moufang, at operator level:** `L_u L_v L_u =
  L_{u(vu)}` holds exactly on every basis pair.

The picture is exact and honest: octonionic dynamics *can* be realised as rotations
in `SO(8)` — there is no obstruction to isometric evolution and the infinitesimal
generators form the Lie algebra `so(8)`. The price is that the finite octonion loop
does not act faithfully or associatively. The "algebra of generators" is Lie
(`so(8)`); the "loop of finite steps" is Malcev/Moufang; and the associator is
precisely the gap between them.

Non-claim: this realises single-generator flow as an exact `SO(8)` one-parameter
group and *locates* the non-associativity as the failure of `u ↦ L_u` to be a
homomorphism. It does not build a two-generator dynamics or a Hamiltonian, and the
`so(8)` here is the operator closure of left multiplications on one octonion copy —
not a claimed physical (gauge or space-time) symmetry.

Contract: `tests/test_gate_o16_isometric_flow.py`.

## Gate O17 — the associative calibration: non-associativity is the G₂ 3-form (implemented, passing)

The dynamics gates O15/O16 treated the associator as an *obstruction*. This gate
takes the swing the earlier honest assessments kept deferring and asks whether the
associator is instead a recognisable *geometric* object. It is — and one of the
most physically loaded objects in mathematics: the **associative calibration
3-form** of `G₂` holonomy. Everything is exact over `ℚ` on `Im(𝕆) = ℝ⁷`.

- **The associative 3-form.** `φ(x,y,z) = ⟨x, yz⟩` is *totally antisymmetric* on
  imaginary arguments with values in `{−1,0,+1}` — the `42` nonzero entries are the
  `7` Fano lines in their `6` orderings. This is Joyce's `φ`, whose calibrated
  3-planes are the *associative* submanifolds of a `G₂` manifold.
- **The associator IS the coassociative 4-form.** The associator of imaginary units
  reconstructs exactly from a totally antisymmetric 4-tensor: `[eᵢ,eⱼ,eₖ] = 2·Σₗ
  ψᵢⱼₖₗ eₗ`, with `ψᵢⱼₖₗ = ½⟨eₗ,[eᵢ,eⱼ,eₖ]⟩` having `168` nonzero entries (`7`
  coassociative 4-planes × `24` orderings). `ψ = *φ` is the coassociative
  calibration: the campaign's central obstruction literally *is* the coassociative
  form.
- **`G₂` invariance.** Every derivation of `𝕆` (the 14-dimensional `g₂ = Lie(Aut 𝕆)`
  of Gate O10) annihilates `φ`: `φ(Dx,y,z)+φ(x,Dy,z)+φ(x,y,Dz)=0`. The infinitesimal
  stabiliser of `φ` is exactly `g₂` — the algebraic definition of `G₂`.
- **The Akivis structure equation.** For any algebra the Jacobiator and associator
  obey the universal loop structure equation (commutator = torsion, associator =
  curvature) `J(x,y,z) = Σ_σ sign(σ)·[σ(x,y,z)]`. Because `𝕆` is alternative the
  associator is itself alternating, so the six signed terms coincide and the
  right-hand side collapses to `6·[x,y,z]` — recovering the O15 identity
  `J = 6·associator` as the structure equation of the calibration.

The swing: the octonionic non-associativity that walls off an ordinary dynamics is,
viewed correctly, the `G₂` calibration geometry underlying compactification of
eleven-dimensional M-theory on a seven-dimensional `G₂`-holonomy manifold — the
route by which exceptional geometry yields four-dimensional chiral physics. This
gate exhibits that identification exactly and finitely: `φ`, `ψ = *φ`, their `G₂`
invariance, and the structure equation, all machine-checked over `ℚ`.

Non-claim: this exhibits the *pointwise algebraic tensors* of `G₂` geometry — the
calibration forms, their exact `G₂` invariance, and the loop structure equation —
and identifies the associator with the coassociative form. It does **not**
construct a `G₂`-holonomy metric, solve the Ricci-flat / supergravity equations,
perform a compactification, or derive any four-dimensional spectrum. It is the
algebra that *seeds* exceptional-holonomy geometry, not that geometry's dynamics.

Contract: `tests/test_gate_o17_calibration.py`.

## Gate O18 — G₂ → SU(3): colour is the holonomy of the Calabi–Yau slice (implemented, passing)

The campaign's two halves have stood apart: the *gauge* half (O10–O14) pulled
colour `su(3)` from the octonions as the stabiliser of one imaginary unit, and the
*geometry* half (O17) showed the associator is the `G₂` associative calibration
`φ`. This gate joins them exactly. Fixing a preferred unit `u = e₇` splits
`Im(𝕆) = ℝ⁷ = ⟨u⟩ ⊕ u^⊥` with `u^⊥ = span(e₁..e₆)`, and reduces the `G₂` structure
to an `SU(3)` structure whose structure group is precisely the O10 colour algebra —
the pointwise algebraic shadow of "a `G₂`-holonomy 7-manifold contains a
Calabi–Yau (`SU(3)`-holonomy) slice". All exact over `ℚ`.

- **Complex structure.** `J = L_u` restricted to `u^⊥` satisfies `J² = −I` and
  preserves `u^⊥`: it makes `u^⊥` into `ℂ³`.
- **Kähler form.** `ω(x,y) = φ(u,x,y)` is antisymmetric, nondegenerate (rank `6`),
  `J`-invariant, and tames `J` (`ω(x,Jx) = |x|² > 0`).
- **Holomorphic volume form.** `Re Ω = φ|_{u^⊥}` is of type `(3,0)+(0,3)`:
  `φ(Jx,Jy,z) = −φ(x,y,z)` on `u^⊥`. Together `(ω, Ω)` are an `SU(3)` structure.
- **The `SU(3)` is colour.** The O10 stabiliser `su(3) = {D ∈ g₂ : Du = 0}`
  (dimension `8`) preserves `ω`, commutes with `J`, and preserves `Re Ω`. The colour
  algebra of Gates O10–O14 is exactly the `su(3)` holonomy of the Calabi–Yau slice
  defined by `φ`: the two halves of the campaign are one object seen two ways.

Non-claim: this is the exact *pointwise linear-algebraic* reduction of the `G₂`
structure `φ` to an `SU(3)` structure `(ω, Ω)` on the tangent space, and the
identification of that `SU(3)` with the O10 colour algebra. It does not build a
Calabi–Yau metric, integrate `J` to a complex manifold, solve the Ricci-flat
equations, or claim the colour gauge field is a gravitational holonomy. It is the
algebra of the reduction, not a compactification.

Contract: `tests/test_gate_o18_su3_structure.py`.

## Gate O19 — the U(1) that completes colour to U(3): the phase of the CY slice (implemented, passing)

Gate O18 reduced the `G₂` calibration to an `SU(3)` structure on the Calabi–Yau
slice `u^⊥ = ℂ³`. But the unitary group of `ℂ³` is `U(3)`, not `SU(3)`: there is one
extra generator, the overall *phase*. This gate exhibits it exactly, working in
`so(6) = so(u^⊥)`, and shows it is precisely the complex structure `J` of O18.

- **The phase generator is `J`.** `J = L_u` on `u^⊥` is skew (`J ∈ so(6)`) with
  `J² = −I`; its one-parameter group `exp(θJ)` rotates `ℂ³` by an overall phase.
- **`u(3)` is the centraliser of `J`.** The skew maps commuting with `J` (the
  `J`-complex-linear ones) form a `9`-dimensional algebra — exactly `u(3)`.
- **Colour and phase are mutual centralisers.** Colour `su(3)` (dim `8`) lies in
  `u(3)`, and the centraliser of colour `su(3)` within `so(6)` is exactly the
  one-dimensional span of `J`. Hence `u(3) = su(3) ⊕ u(1)_J`: colour `SU(3)` and the
  phase `U(1)` are each other's commutant and fill out the full `U(3)`.
- **The phase `U(1)` is outside `Aut(𝕆)`.** `J` is *not* a derivation (O17: it does
  not preserve `φ`), so `u(1)_J` is a genuine symmetry beyond `g₂ = Lie(Aut 𝕆)` — the
  abelian factor the choice of preferred direction *adds*. It is the centre of `U(3)`,
  the overall Calabi–Yau phase (a baryon-number-like `U(1)` giving all three colours
  the same charge), commuting with colour.

So the geometric reduction of one octonion copy yields not merely colour `SU(3)` but
`SU(3) × U(1) = U(3)` on the Calabi–Yau slice, the `U(1)` forced as the unique
commutant of colour and realised by the complex structure.

Non-claim: this exhibits the exact abelian `u(1)_J` completing colour `su(3)` to
`u(3)` on the tangent slice, as the commutant of colour and the centre of the
slice's unitary algebra. It does **not** identify this `U(1)` with electroweak
hypercharge or electric charge (those need `ℂ⊗ℍ⊗𝕆` and the weak `su(2)` of O13,
absent here), does not gauge it, and adds no dynamics.

Contract: `tests/test_gate_o19_phase_u1.py`.

## Gate O20 — the assembly: the Standard Model gauge algebra su(3)⊕su(2)⊕u(1) on ℂ⊗ℍ⊗𝕆 (implemented, passing)

The campaign has produced the three Standard-Model gauge factors on separate
algebras: colour `su(3)` from `ℂ⊗𝕆` (O10/O11), weak isospin `su(2)` from the
quaternions `ℍ` (O13), and abelian `u(1)` phases (O11/O19). Gate O20 performs the
**Furey assembly**: it realises all three at once as commuting operator algebras
on the single one-generation module `ℂ⊗ℍ⊗𝕆` (`= ℍ⊗𝕆 = 32` complex dimensions over
`ℚ(i)`), using Kronecker products on the two Cayley–Dickson tensor slots:

- **Colour** `su(3)` acts on the `𝕆` factor — the eight O11 number-preserving
  bilinears become `I_ℍ⊗C_a` (`a = 1..8`).
- **Weak** `su(2)` acts on the `ℍ` factor — the three O13 imaginary quaternion
  left-multiplications become `W_i⊗I_𝕆` (`i = 1..3`).
- **`u(1)`** is the O11 number operator on the `𝕆` factor, `I_ℍ⊗N`.

Exact facts over `ℚ(i)`: colour closes into `su(3)` (rank 8, bracket-closed); weak
closes into `su(2)` (`[W_i,W_j]=2W_k` cyclically, rank 3); **colour and weak
commute** (they act on different Cayley–Dickson slots, so every
`[I_ℍ⊗C_a, W_i⊗I_𝕆]=0`); the `u(1)=I_ℍ⊗N` is central and independent; and the
total algebra has dimension `8+3+1 = 12` — exactly `dim(su(3)⊕su(2)⊕u(1))`, the
Standard-Model gauge algebra, realised on one octonion–quaternion generation.

Non-claim: this is the standard Furey **embedding** of the SM gauge algebra into
the left-action algebra of `ℂ⊗ℍ⊗𝕆`. The colour–weak commutation is **structural**
— the two factors act on different Cayley–Dickson slots — so the gate exhibits a
consistent realisation of the `su(3)⊕su(2)⊕u(1)` content, **not** a derivation that
nature is forced to this product, nor the chirality/representation assignment, the
Higgs sector, symmetry breaking, or any dynamics. The `u(1)` here is the O11
colour-phase/number `u(1)`, not the fully mixed electroweak hypercharge.

Contract: `tests/test_gate_o20_standard_model.py`.

## Gate O21 — colour is forced: the number-preserving symmetry of one generation is su(3) acting as 1⊕3⊕3̄⊕1 (implemented, passing)

Gate O11 *built* colour `su(3)` inside the `ℂ⊗𝕆` Fock space. Gate O21 proves the
**forcing** behind Furey's construction: `su(3)` is not merely available, it is the
*unique* number-preserving internal symmetry of one generation, and its
representation content is forced to be exactly one generation's colour content.
All exact over `ℚ(i)` on the 8-dim Fock space (`Cl(6)=M₈(ℂ)`):

1. **The symmetry of the charge grading is 20-dimensional.** The commutant of the
   number operator `N` inside `M₈(ℂ)` — every operator preserving all four charge
   sectors — has dimension `20 = 1²+3²+3²+1²` (Schur, for eigenspace dims
   `1,3,3,1`). That is the *entire* internal symmetry of the grading.
2. **The ladder bilinears carve out exactly `u(3)`.** The nine `αⱼ†αₖ` span a
   9-dim algebra inside that commutant; its eight traceless generators close into
   `su(3)` (colour), with `N` the commuting `u(1)`.
3. **Colour is a singlet on both leptons.** Restricted to the charge-0 vacuum and
   charge-3 top state, every `su(3)` generator is the zero operator.
4. **The two triplet sectors are 3 and 3̄.** On the charge-1 sector `su(3)` acts as
   the faithful **fundamental 3** (span dim 8); on the charge-2 sector as the
   **antifundamental 3̄** — certified by the cubic invariant
   `d_abc = tr(Mₐ{M_b,M_c})`, which for charge 2 is exactly *minus* that of charge
   1 (the signature of the conjugate rep), while the charge-1 `d`-symbol is not
   identically zero (a genuine complex `3`, not a real rep).

So given the O11 Fock construction, the number-preserving symmetry is forced to
be `su(3)⊕u(1)` acting as `1⊕3⊕3̄⊕1` — one lepton, a quark colour triplet, an
antiquark antitriplet, one antilepton: exactly one generation's colour content.

Non-claim: the forcing is *conditional on the O11 Fock construction* — it derives
that the number-preserving symmetry of that generation is uniquely `su(3)` with
colour representation content, not why nature realises this Fock space. Exact
representation theory of `ℂ⊗𝕆`: no weak `su(2)`, no three generations, no
chirality dynamics, no Higgs.

Contract: `tests/test_gate_o21_colour_forcing.py`.

## Gate O22 — one generation's Standard-Model multiplets on ℂ⊗ℍ⊗𝕆 (implemented, passing)

O20 assembled the gauge *algebra* `su(3)⊕su(2)⊕u(1)`; O21 forced colour's rep
content on the `𝕆` factor. Gate O22 completes the picture on the full 32-dim module
`ℍ⊗𝕆` (over `ℚ(i)`): under the commuting colour `su(3)` (on `𝕆`) and weak `su(2)`
(on `ℍ`), it decomposes into exactly the quark/lepton weak-doublet pattern of one
generation — each tensor factor's rep content proven exactly. All exact over `ℚ(i)`:

1. **Weak content is pure doublets.** The weak Casimir `Σ Wᵢ² = −3·I` *uniformly*
   on the whole space (the spin-½ value), and the weak generators have trivial
   common kernel — **no weak singlets**. Every state is a weak doublet; the `ℍ`
   factor is `2⊕2`.
2. **Colour content is `1⊕3⊕3̄⊕1`** (O21). On the full module the colour
   generators' common kernel — the colour-singlet subspace — has dimension `8` (the
   two `𝕆`-factor singlets × the 4-dim weak factor): the **leptons**.
3. **The multiplet pattern is one generation.** The 32 states split into `8`
   colour-singlet weak-doublet states (**leptons**, `(1,2)`) and `24` colour-triplet
   weak-doublet states (**quarks**, `(3,2)⊕(3̄,2)`) — the Standard Model's central
   qualitative fact (quarks are colour-triplet weak doublets, leptons are
   colour-singlet weak doublets), realised as an exact tensor decomposition.

Non-claim: this exhibits the quark/lepton weak-doublet **multiplet pattern** of one
generation. As in every `ℂ⊗ℍ⊗𝕆` construction it appears *doubled* (particles and
antiparticles both present — the `3` and `3̄`, both `𝕆` singlets, both weak
doublets); it is **not** the chiral (left-only) content, **not** the hypercharge
assignment that splits the doublets, **not** three generations, and carries no
dynamics. The colour–weak product is structural (independent Cayley–Dickson
factors, O20), so this is a forced multiplet *pattern* given the `ℂ⊗ℍ⊗𝕆`
construction, not a derivation of that construction.

Contract: `tests/test_gate_o22_generation_multiplets.py`.

## Gate O23 — handedness and the vector-like wall: chirality on ℂ⊗ℍ⊗𝕆 (implemented, passing)

O22 found the multiplet *pattern* of one generation but noted it comes *doubled*,
with no chiral (left-only) asymmetry. Gate O23 confronts chirality head-on and is
scrupulous about where the algebra succeeds and where it stops. The quaternion
factor carries *two* commuting `su(2)`s — `ℂ⊗ℍ = M₂(ℂ)` has `so(4)=su(2)_L⊕su(2)_R`:

- **`su(2)_L`** is weak isospin (O13/O20): imaginary quaternion **left**-mults `Wᵢ`
  (`[Wᵢ,Wⱼ]=2Wₖ`).
- **`su(2)_R`** is imaginary quaternion **right**-mults `Rᵢ` (`[Rᵢ,Rⱼ]=−2Rₖ`); since
  `ℍ` is associative, `[Wᵢ,Rⱼ]=0`.

The right action supplies a **canonical handedness projector** `P=½(I+iR₁)`
(`P²=P`) built from the `ℂ` of `ℂ⊗ℍ` and one right unit. It commutes with the
*entire* SM gauge algebra, and `P`, `I−P` split the 32 states into two
gauge-invariant 16-dim halves — the two minimal left ideals of `ℂ⊗ℍ`, a
"left-handed" and "right-handed" copy of the generation. Exact over `ℚ(i)`:

1. **Two commuting `su(2)`s.** `[Rᵢ,Rⱼ]=−2Rₖ` and `[Wᵢ,Rⱼ]=0` (`so(4)`).
2. **Canonical handedness projector.** `P²=P`; `P`,`I−P` give gauge-invariant
   16-dim halves (`[P,colour]=[P,weak]=0`).
3. **The vector-like wall (honest negative).** Genuine SM chirality would need the
   two halves to carry *inequivalent* weak reps (one doublets, one singlets).
   Instead the weak Casimir is `−3·I` *uniformly*, so **both** halves are pure weak
   doublets: the construction is exactly **vector-like**. `ℂ⊗ℍ⊗𝕆` alone gives one
   generation's multiplet content but **not** its chiral asymmetry.

Non-claim: this exhibits the canonical handedness splitting and proves the
construction is vector-like — it does **not** derive the SM's chiral (`SU(2)_L`-only)
structure, which needs an extra ingredient beyond the module (a projector that both
selects one ideal *and* collapses the other's doublets to singlets — put in by hand
in the Furey/Dixon programme, not forced here). No hypercharge split, no dynamics.

Contract: `tests/test_gate_o23_chirality.py`.

## Gate O24 — three generations as a Jordan frame of J₃(𝕆) (implemented, passing)

O12 showed the *triality* route to three generations fails (the three `ℂ⊗𝕆`
towers coincide). Gate O24 implements the alternative that survives — following
Dubois-Violette–Todorov, Boyle, and the author's own delimitation (Zenodo
21107402): **identify the three generations with the three primitive idempotents of
a Jordan frame** of the exceptional Jordan algebra `J = J₃(𝕆)` (Gate O02's `h₃(𝕆)`).

A frame is a resolution of the identity into three orthogonal rank-one idempotents
`{E₁,E₂,E₃}` — the *rank* of `J₃(𝕆)` is three, and that is the family count.
Relative to a frame, `J` has the Peirce decomposition `J = (J₁₁⊕J₂₂⊕J₃₃) ⊕
(J₁₂⊕J₁₃⊕J₂₃)`: three 1-dim diagonal *generation slots* (`Jᵢᵢ = ℝEᵢ`) plus three
8-dim octonionic off-diagonals — `3 + 3·8 = 27 = dim J₃(𝕆)`. Exact over ℚ:

1. **Family count three.** The frame is exactly three primitive idempotents
   resolving the identity (`Σ Eᵢ = I`, `Eᵢ∘Eⱼ = 0`): rank `J₃(𝕆) = 3`.
2. **Genuinely three (not one).** The three idempotents are *linearly independent*
   in the 27-dim `J` (span dimension `3`) — unlike the O12 triality towers, which
   coincided. This is the exact contrast between the two routes.
3. **Peirce decomposition.** The three diagonal generation slots total dimension
   `3`, the octonionic off-diagonals total `24`, together `27`; each `L_{Eᵢ}` has
   the Peirce spectrum `{1: 1, ½: 16, 0: 10}`.

Non-claim: the count three is the *rank* of `J₃(𝕆)`, **adopted** following Boyle /
Dubois-Violette–Todorov, **not derived** from `ℂ⊗ℍ⊗𝕆` — the `ℂ⊗ℍ⊗𝕆 ↔ J₃(𝕆)`
bridge is an open problem, not a theorem. The value of the idempotent
identification is structural: because generations are a resolution of the identity
rather than triality-permuted representations (O12), this route is *not* subject to
the Distler–Garibaldi obstruction at the level of count and chirality. It fixes
neither the mass hierarchy nor the mixing angles (the algebra fixes a mixing law
but selects no hierarchy — Zenodo 21107402). This gate is the exact-over-ℚ
count-and-Peirce core of a fuller numpy treatment on the `master` branch
(`compute/three_generations_frame.py` — inner F4 frame-Weyl S₃, OP²=F4/Spin(9),
isotropy 36=spin(9), 16-dim real-spinor tangent; `jordan_eigenvalue_generations.py`
— the Freudenthal-cubic "why three"; `three_generations_nogo_audit.py` — the
triality no-go control), which cover the F4/Spin(9) and chirality legs omitted here.

Contract: `tests/test_gate_o24_three_generations.py`.

## Gate O25 — discharging the vector-like wall: chirality from one KO-6 idempotent

Gate O23 hit an honest wall: its handedness projector `P = ½(I + iR₁)`, built from a
quaternion *right* multiplication, split the 32-dim generation into two 16-dim
halves — but the weak Casimir was `-3 I` *uniformly*, so **both** halves were weak
doublets. The construction was exactly **vector-like**, and O23 flagged an "extra
by-hand ingredient" as the missing piece. This gate supplies that ingredient
explicitly and exactly over ℚ(i), and shows it is a *single* object.

The O23 diagnosis: its projector sat on the **wrong leg** (the `ℍ` spectator that
commutes with everything) and acted on the *module* rather than being built into the
*generators*. The fix, following the master-branch program (`foundations/06` and
`compute/chiral_projector.py` behind Zenodo 21107402), is the aligned
**KO-dimension-6 chirality** on the `𝕆` leg,

    γ_Q = i · L_{e₁} L_{e₂} … L_{e₆},

the ordered product of the *six* charge-carrying octonion left-multiplications,
**dropping the colour-fixing axis** `e₇`. Exactly over ℚ(i):

1. **A genuine chirality.** `γ_Q² = I`, `tr γ_Q = 0`, with 4-dim `+` and 4-dim `-`
   eigenspaces on the 8-dim `𝕆` leg.
2. **Aligned with charge.** `[N, γ_Q] = 0` — because `e₇` is dropped, the chirality
   commutes with the charge operator (the naive full product would not). This is
   what makes the projector gauge-compatible.
3. **One idempotent.** `P_L = ½(I + γ_Q)` satisfies `P_L² = P_L` (rank 4 on `𝕆`).
4. **Projected generators still close.** With the physically **gauged** weak
   generators `G_a = W_a ⊗ P_L`, one has `[G₁,G₂] = 2G₃` cyclically — because
   `P_L² = P_L` (idempotency, not commutativity) rides through the bracket:
   `[W_a⊗P_L, W_b⊗P_L] = [W_a,W_b]⊗P_L`.
5. **The gauged Casimir is chiral.** `Σₐ G_a² = (-3 I_ℍ) ⊗ P_L` exactly. On the
   `γ_Q = +1` sector (16-dim) the Casimir is `-3` — a weak **doublet**; on the
   `γ_Q = -1` sector (16-dim) it is `0` — a weak **singlet**. Left-handed doublets,
   right-handed singlets: the Standard-Model chiral pattern, from **one** idempotent.
6. **Contrast with the wall.** The *ungauged* weak Casimir `Σₐ W_a² = -3 I` is `-3`
   on *both* `γ_Q` sectors: applied to the module (O23's spectator) it can only give
   doublet + doublet. Gauging — folding `P_L` into the generators — is exactly what
   breaks the `L`/`R` symmetry.

(The campaign normalises weak isospin by `[W_i,W_j] = 2W_k` with Casimir `-3 I`; the
master branch uses `[T_a,T_b] = iε_{abc}T_c` with Casimir `¾ I`. Same `su(2)`,
different normalisation; the doublet-vs-singlet *split* is normalisation-independent.)

Non-claim: this is an *adopted* ingredient, not a forced one. The choice of the
aligned KO-6 chirality `γ_Q` (equivalently, which sector is called "left-handed") is
a convention inherited from the Furey/Dixon and master-branch program (Lever B), not
something `ℂ⊗ℍ⊗𝕆` selects on its own. What this gate *does* establish exactly is
that **a single KO-dimension-6 idempotent**, once adopted, converts the O23
vector-like content into the genuinely chiral doublet-left / singlet-right
Standard-Model pattern — replacing the informal "extra by-hand ingredient" with one
explicit, exactly-checkable object. The Yukawa spectrum, the Higgs, and three
generations remain outside this gate. See also (master, behind Zenodo 21107402)
`foundations/06_chiral_idempotent.md` and `compute/chiral_projector.py`.

Contract: `tests/test_gate_o25_chiral_projection.py`.

## Gate O26 — the atmospheric mixing angle as a Fano-plane invariant

The campaign's first genuinely *falsifiable* number. The octonion multiplication
triples `eᵢeⱼ = ±eₖ` are exactly the seven lines of the **Fano plane**
`PG(2,2) = S(2,3,7)` (O17's associative 3-form `φ` is nonzero precisely on them).
Pick a "vacuum" imaginary unit `e_v`; each point lies on `n+1 = 3` lines and *avoids*
`7−3 = 4`. The campaign's sharpest bet is the atmospheric octant

    sin²θ₂₃ = (lines avoiding the vacuum) / (all lines) = 4/7,

the *only* vacuum-scale-independent exact mixing rational the framework emits
(`θ₂₃ = arcsin√(4/7) ≈ 49.1°`, upper octant). The value is hardened from "read one
row of the multiplication table" to a **basis-free spectral invariant**. On the
7-dim line-space the vacuum-avoidance operator `P_avoid(v) = diag[1 if v∉L]` is a
rank-4 orthogonal projector (`P² = P = Pᵀ`, spectrum `{1⁴,0³}`). Exact over ℚ:

1. **Seven Fano lines.** The octonion triples give exactly `PG(2,2)` — a theorem
   about the multiplication, not a drawing convention.
2. **Vacuum-independence.** The split is `(3 through, 4 avoiding)` for *every* one of
   the 7 vacuum choices, so `sin²θ₂₃ = 4/7` regardless of which unit is singled out.
3. **A normalized trace.** `Tr P_avoid / 7 = 4/7 = ½ + 1/14` — maximal mixing plus
   the single-line Fano asymmetry — a basis-free spectral mean, not a chosen entry.
4. **Convention-independence.** `Aut(Fano) = PSL(2,7)`, order `168`, acts
   *transitively* on the 7 points; the induced line-permutations satisfy
   `Πg P_avoid(v) Πgᵀ = P_avoid(g(v))` for all 168 collineations, so `4/7` is a
   single-orbit **class invariant** — no octonion relabelling changes it.
5. **Octant complementarity.** The mirror `P_through` is rank 3 → `3/7`, with
   `4/7 + 3/7 = 1`.

Non-claim: what is forced, exactly and basis-free, is the *value* `4/7` **given** two
adopted inputs: (i) the physical map "atmospheric mixing probability = avoiding/total
lines" (the open "N5 bridge", not derived from any dynamics here), and (ii) the octant
choice of the *avoiding* (broken) sector over the *through* (colour-`su(3)` stabiliser)
sector. A stable lower-octant resolution near `3/7` would falsify the octant choice.
The gate derives neither the map nor the octant; it proves that once adopted, the
number is canonical and convention-free. Current global fits `sin²θ₂₃ ≈ 0.55–0.57`
sit beside `4/7 ≈ 0.571` — the framework's one live contact with data. Cross-refs
master `compute/theta23_fano_invariance.py`, `compute/theta23_mixing_operator.py`.

Contract: `tests/test_gate_o26_atmospheric_mixing.py`.

## Gate O27 — the bridge attempt: colour diagonal on three generation-slots

The campaign's highest-risk swing: trying to *force* a link between one generation's
algebra (`ℂ⊗ℍ⊗𝕆`, O20–O25) and the rank-3 `J₃(𝕆)` from which the family count 3 was
adopted (O24). It delivers a genuine exact result on *one half* and is honest that
the other stays open.

**Positive half (exact over ℚ).** In `J₃(𝕆)` the three off-diagonal octonionic slots
`(1,2),(1,3),(2,3)` are the O24 generation-slots. The colour `su(3)` of O10 — the
`g₂` derivations of `𝕆` stabilising `e₇` (dim 8) — lifts *entrywise* to `J₃(𝕆)`:

1. **Colour is a Jordan derivation.** Every one of the 8 generators obeys Leibniz
   `D(A∘B) = D(A)∘B + A∘D(B)` *exactly* on all 27×27 basis pairs and kills the real
   diagonal — so colour `su(3) ⊂ Der(J₃𝕆) = f₄`.
2. **A faithful Lie embedding.** `[lift(D_a),lift(D_b)] = lift([D_a,D_b])` on all
   27 dimensions.
3. **Identical on all three slots — no triality permutation.** The per-slot 8×8
   action is the *same* matrix on `(1,2)`, `(1,3)`, `(2,3)`: three identical colour
   multiplets, each carrying (O21) one generation's `1⊕3⊕3̄⊕1`.

This is the exact sense in which the idempotent-frame reading (O24) evades the
Distler–Garibaldi obstruction at count+representation level: colour is a
*slot-diagonal* `su(3)`, not a triality rotation mixing slots (contrast O12).

**Open half (the honest wall).**

4. **A hard dimension obstruction.** The three slots span `3×8 = 24` real octonionic
   dimensions, but each single-generation gauge module is `ℍ⊗𝕆 = 32` over ℚ(i),
   carrying the weak `ℍ` doublet of O13/O22/O25. A bare octonion slot has *no room*
   for that `ℍ` factor: the Jordan off-diagonal carries colour and the family-count,
   **not** weak isospin or the O25 chirality. The embedding `ℂ⊗ℍ⊗𝕆 → J₃(𝕆)` is *not
   exhibited*.

Non-claim: the bridge is **not closed**. What is forced exactly is that colour
`su(3)` embeds in `Der(J₃𝕆) = f₄` as a slot-diagonal derivation, so the adopted
rank-3 structure carries three identical, triality-un-permuted colour generations.
The rank-3 itself stays *adopted* (Boyle / Dubois-Violette–Todorov), not derived; the
weak/chiral/hypercharge structure lives *outside* the Jordan off-diagonal (the 24-vs-32
wall); no mass hierarchy or mixing follows. A real partial result **and** a sharp
exact no-go on the full `ℂ⊗ℍ⊗𝕆 ↔ J₃(𝕆)` bridge, which stays open. Cross-refs master
`compute/three_generations_frame.py`, `foundations/04_generation_symmetry_theorem.md`.

Contract: `tests/test_gate_o27_generation_bridge.py`.

## Gate O28 — the parameter-free mixing web from the Fano split {3, 4, 7}

O26 emitted one falsifiable rational, `sin²θ₂₃ = 4/7`. This gate follows the thread:
the *same* Fano vacuum split (3 through, 4 avoiding, 7 total) drives an entire **web**
of parameter-free relations among already-measured quark and lepton observables,
exact over ℚ. The master flavour bridge assigns the three counts to four observables
through one scale `ε₀² = π/432`:

    |V_us|²         = 7·ε₀²   (Cabibbo → all lines)
    sin²θ₁₃         = 3·ε₀²   (reactor → lines through vacuum)
    Δm²₂₁/Δm²₃₁     = 4·ε₀²   (splitting → lines avoiding vacuum)
    sin²θ₂₃         = 4/7     (atmospheric octant, O26)

Every one of the first three is `(integer)·ε₀²`, so **the knob cancels in every
ratio** — pure Fano-count rationals with *no free parameter*, testable today:

1. **The reactor angle is tied to the Cabibbo angle:** `sin²θ₁₃/|V_us|² = 3/7`
   (through/total) — a lepton probability bound to a quark one, parameter-free.
2. **Two more:** `(Δm²₂₁/Δm²₃₁)/|V_us|² = 4/7` and `(Δm²₂₁/Δm²₃₁)/sin²θ₁₃ = 4/3`.
3. **A Fano completeness sum rule:** `7 = 3+4` → `sin²θ₁₃ + Δm²₂₁/Δm²₃₁ = |V_us|²`.
4. **Only two are independent:** `R3 = R2/R1`, `R1+R2 = 1`; the O26 octant `4/7` is
   exactly `R2`, the avoiding-line partner of the reactor `3/7`.

**Data confrontation (the falsifiable payoff).** With PDG-2024 / NuFIT-5.2 central
values these parameter-free predictions agree with measurement at the few-percent
level: R1 +2.2%, R2 +2.6%, R3 +0.5%, sum rule +2.4%, `sin²θ₂₃` −2.3% (worst ~2.6%).
A precise future resolution breaking any ratio — especially `R1 = 3/7` or the sum
rule — falsifies the assignment.

Non-claim: what is forced, exactly and knob-free, is the *web of ratios* `{3/7, 4/7,
4/3}` and the sum rule, **given** the master's *adopted* assignment of the Fano
counts `{3,4,7}` to specific observables (which count labels which channel is a
modelling choice) and the amplitude-vs-probability power counting. The absolute
scale `ε₀² = π/432` is itself an adopted knob; this gate works only with the
ε₀-free ratios where it cancels. No mass hierarchy, CP phase, or dynamics follows.
The value: a *single* finite incidence structure — the octonion Fano plane — forces
several independent, currently-correct relations among measured flavour observables.
Cross-refs master `compute/epsilon_free_mixing_web.py`, `epsilon_mixing_coefficients.py`.

Contract: `tests/test_gate_o28_mixing_web.py`.

## Gate O29 — the mass↔mixing bridge: one Fock module ties masses to angles

O28 tied the *mixing* observables together; this gate closes the loop to the *mass*
sector, exact over ℚ. The charged-fermion mass ratios are driven by the same knob
`ε₀² = π/432` through integer **Fock-grade counts** of the O11 number operator `N`,
whose grade multiplicities (eigenvalues 0,1,2,3) are exactly `(1,3,3,1)`, total
`8 = 2³ = dim Λ*(ℂ³)`:

    up      m_c/m_t     = 1·ε₀²   (Tr P₀, grade-0 vacuum / colour singlet)
    down    m_s/m_b     = 3·ε₀²   (Tr P₁, grade-1 / colour triplet)
    lepton  m_μ/m_τ     = 8·ε₀²   (Tr I, the full Fock module 2³)

With O28's mixing counts (`|V_us|²=7`, `sin²θ₁₃=3`, `Δm²₂₁/Δm²₃₁=4`, all `·ε₀²`),
*every* observable is `(integer)·ε₀²`, so any mass ratio ÷ any mixing observable
cancels the knob. Exact over ℚ:

1. **Headline `m_s/m_b = sin²θ₁₃`.** Both carry `3` — but from *independent* origins:
   the mass `3` is the Fock grade-1 trace `Tr P₁` (colour-triplet dimension), the
   mixing `3` is the count of Fano lines *through* the vacuum. Two separately-assigned
   integers coinciding is a structural statement, not a tuning: a *down-quark mass
   ratio equals the leptonic reactor mixing probability*.
2. **Lepton ties.** `m_μ/m_τ = 2·(Δm²₂₁/Δm²₃₁)` (`8 = 2·4`) and
   `m_μ/m_τ = (8/3)·sin²θ₁₃`.
3. **Consistency with O28.** `m_s/m_b / |V_us|² = 3/7 = R1` (since `m_s/m_b = sin²θ₁₃`).
4. **Mass-mass ratios.** Grade counts give `(m_s/m_b)/(m_c/m_t)=3`,
   `(m_μ/m_τ)/(m_s/m_b)=8/3`, `(m_μ/m_τ)/(m_c/m_t)=8`.

**Data confrontation.** The charm-free identities agree strikingly with measured
MS-bar masses and NuFIT mixing: `m_s/m_b = sin²θ₁₃` +1.4%, `m_μ/m_τ = 2·Δm-ratio`
+0.8%, `m_μ/m_τ = (8/3)sin²θ₁₃` +1.2%, `(m_μ/m_τ)/(m_s/m_b) = 8/3` −0.1%. The
`m_c/m_t` identities are **scale-sensitive** (the tiny up-sector ratio runs strongly)
and sit near ~5% — reported but flagged, not asserted tightly.

Non-claim: forced exactly are (i) the mass counts `{1,3,8}` as `N`-grade traces on
the O11 Fock module, and (ii) the ε₀-free cross ratios, *given* the master's
*adopted* assignment of counts to observables. The scale `ε₀² = π/432` and those
assignments are adopted, not derived; the `m_c/m_t` relations are scale-dependent; no
absolute masses, hierarchy origin, or CP phase follows. The value: a *single finite
Fock module* — the same `ℂ⊗𝕆` ladder that gave colour and charge — forces several
currently-correct relations *across* the mass and mixing sectors. Cross-refs master
`compute/epsilon_channel_coefficients.py`, `epsilon_free_mass_mixing_bridge.py`.

Contract: `tests/test_gate_o29_mass_mixing_bridge.py`.

## Gate O30 — CKM amplitudes: vector √7 vs spinor ½ (the double-cover half-angle)

O28 fixed the mixing *probabilities* as Fano-line counts (`|V_us|² = 7·ε₀²`). This
gate takes the next step of the master flavour bridge and explains the two leading
CKM *amplitudes* — one a **vector**, one a **spinor** — removing the last `1/2` that
the probability bridge had put in by hand as a "weak-isospin input". Exact over ℚ:

1. **Vector channel `|V_us|`.** The Cabibbo transition lives on the 7-dim `Im(𝕆)`
   (O28's seven Fano directions). A vector rotation's off-diagonal amplitude is
   `sin θ`, leading coefficient exactly **1**; summed coherently over the 7 directions
   this is `√7·ε₀`, so `|V_us|² = 7·ε₀²` — the very count of O28
   (`vector_channel_count() == cabibbo_count() == 7`).
2. **Spinor channel `|V_cb|`.** An inter-generation transition is a single qubit; in
   the `SU(2)` fundamental `exp(−iθ n·σ/2)` the off-diagonal amplitude is `sin(θ/2)`,
   leading coefficient exactly **1/2**, so `|V_cb| = (1/2)·ε₀`.
3. **The `1/2` is derived, not input.** The module builds both representations as
   exact rational generators and reads off the two leading transition coefficients as
   `1` (vector) and `1/2` (spinor); their ratio `1/2` is the `SU(2)→SO(3)` double-cover
   half-angle. The contrast `√7` (vector, full angle, 7 dirs) vs `1/2` (spinor, half
   angle, one qubit) is exactly *vector vs spinor*.
4. **Finite-angle avatar `tan(π/8) = √2 − 1`.** The transition/survival ratio
   `tan(θ/2)` (same leading `1/2`) at the octonionic 45° reflection is `tan(π/8)`,
   verified **exactly in ℚ(√2)** — no floating point — as the positive root of
   `t² + 2t − 1 = 0` via the double-angle relation `2t/(1−t²) = 1`.

**Data confrontation.** With PDG-2024 magnitudes: `|V_us| = √7·ε₀` +0.6%,
`|V_cb| = (1/2)·ε₀` +1.0% (both < 1.1%).

Non-claim: derived exactly over ℚ are the vector coefficient `1`, the spinor
coefficient `1/2` as the double-cover half-angle, their ratio `1/2`, and
`tan(π/8) = √2 − 1`. What stays *adopted* (as in the master) is the **channel
assignment** — why `|V_cb|` is the spinor inter-generation transition while `|V_us|`
is the `Im(𝕆)` vector — which follows the two-level/`Im(𝕆)` split but is not derived
from the CHO Yukawa operator; and the scale `ε₀² = π/432`. The *value* `1/2` is no
longer an input; the channel that carries it is. No mass hierarchy or CP phase
follows. Cross-refs master `compute/epsilon_vcb_halfangle.py`.

Contract: `tests/test_gate_o30_ckm_amplitudes.py`.

## Gate O31 — the knob denominator 432 = 16 × 27 = (Weyl count) × dim J₃(𝕆)

O28–O30 all *adopted* the flavour scale `ε₀² = π/432` and worked in its ratios so the
knob cancelled. This gate takes one honest step *into* the knob: the integer `432` is
not free — it is the product of two dimensions the campaign has already computed
exactly from the algebra:

    432 = 16 × 27 = (one chirality's Weyl-fermion count) × dim J₃(𝕆),   ε₀² = π/(16·27).

- **16** — Gate O25 gauged the weak su(2) with the aligned chirality γ_Q and split the
  32-dim ℍ⊗𝕆 generation into a 16-dim left-handed weak **doublet** and 16-dim
  right-handed **singlet**; that 16 is one generation's Weyl count of a single
  chirality (the **16** of SO(10)). Here `chiral_weyl_count() = left_handed_dimension()`.
- **27** — Gate O24 built J₃(𝕆) as a 27-dim real space (3 diagonal generation slots +
  24 octonionic off-diagonal): `jordan_dimension() = generation_slot_dimension() +
  offdiagonal_dimension() = 27`.

Their product is exactly the `432` used downstream, and `π/(16·27)` reproduces the
`π/432` of O28/O29/O30 to machine precision. A second exact factorisation `432 = 24 ×
18` records the master's Higgs route `ε₀² = λ_Higgs/18 = (π/24)/18` (`λ_Higgs = π/24`,
`18 = 2×9`); both factor the same `432`, but only the `16×27` reading is anchored to
computed campaign dimensions.

Non-claim: exact here is only the integer identity `432 = 16×27` with `16` and `27`
the campaign's already-tested chiral Weyl count and dim J₃(𝕆). Still **adopted**, not
derived: the numerator `π` (a geometric half-rotation / Berry phase on the
`G₂/SU(3) ≅ S⁶` coset), and the very claim that the flavour scale *is* `π` over this
product (that `ε₀²` has this form at all and equals `m_c/m_t`). `432` has other
factorisations; `16×27` is *selected* because both factors are algebra-native
dimensions, not forced by `432`. No new observable and no dynamics follow — this gate
only makes the adopted denominator structural. Cross-refs master
`compute/mass_relations.py`.

Contract: `tests/test_gate_o31_knob_scale.py`.

## Gate O32 — canonical Yukawa operator: exact current-level no-go

The desired next step was a single, data-independent Yukawa operator on three
physical generations. The current structures do not select one.

1. O27's `24`-versus-`32` obstruction remains: the Jordan slots do not carry the
   complete weak/chiral one-generation module, so a genuine three-generation
   fermion space has not been constructed.
2. Colour acts identically on the three adopted slots, as proved in O27. By the
   resulting Kronecker-product structure, the **six-dimensional subspace** of
   real-symmetric `3 x 3` generation-only textures is gauge-equivariant. This is
   a lower bound on the full commutant, already enough to leave the hierarchy free.
3. Imposing the unbroken frame permutation `S3` reduces that space to the
   two-dimensional span of `I` and the all-ones matrix `J`. Every `a I + b J`
   has one singlet eigenvalue and a degenerate doublet, so it cannot produce
   three distinct generation masses.

Verdict: without frame symmetry there is arbitrary texture freedom; with it
there is an unavoidable degeneracy. A new symmetry-breaking action or spurion
is required, and must be selected without measured flavour inputs.

Contract: `tests/test_gate_o32_yukawa_operator.py`.

## Gate O33 — flavour assignment and scale audit

All six permutations assigning Fano counts `{3,4,7}` to
`{|V_us|^2, sin^2(theta13), Delta m^2_21/Delta m^2_3l}` are now enumerated with
approximate current uncertainties. The adopted `(7,3,4)` assignment ranks first,
but its profiled fit is borderline before accounting for assignment trials and
is not significant after a conservative six-trial correction. The fixed
`pi/432` scale fits less well than the profiled scale.

The audit also records that O29 compares `m_c(m_c)` with `m_t(m_t)` and
`m_s(2 GeV)` with `m_b(m_b)`. Those mixed-scale ratios cannot support precision
claims before common-scheme RG evolution. Empirical tolerance checks have been
demoted to diagnostics and can no longer promote a scientific claim in tests.

Contract: `tests/test_gate_o33_flavour_assignment_audit.py`.

## Non-claims


This campaign selects (or fails to select) the probability calculus in an exotic
amplitude ring. It does not derive the Standard Model. Suggestive links between
`h_3(O)`, `F4`/`E6`/`E8`, and particle content exist in the literature but remain
numerology-adjacent until dynamics are derived, which this framework structurally
cannot yet do.
