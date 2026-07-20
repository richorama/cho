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

## Non-claims

This campaign selects (or fails to select) the probability calculus in an exotic
amplitude ring. It does not derive the Standard Model. Suggestive links between
`h_3(O)`, `F4`/`E6`/`E8`, and particle content exist in the literature but remain
numerology-adjacent until dynamics are derived, which this framework structurally
cannot yet do.
