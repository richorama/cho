# CHO in Context: Comparison with the Division-Algebra Literature

Created: 2026-06-06 (legacy repair-pass Tier 3, item T3.1)

Purpose: locate every CHO headline claim relative to prior work, and state
explicitly which claims the established programs would **grant**, which they
**stop before**, and which they would **dispute**. The repository's result
documents previously cited no related work; this note closes that gap and
pre-empts the obvious referee objection ("this is unaware of / avoiding the
field").

Honest framing up front: within the division-algebra Standard Model lineage,
**CHO is the most numerically aggressive and the least mathematically rigorous
member.** Its peers prove representation theory and stop exactly where CHO's
"open bridges" begin. That is simultaneously CHO's distinctive contribution and
its central vulnerability.

---

## 1. The peer programs

| Program | Core object | What they establish | Where they stop |
|---|---|---|---|
| **Furey** (2012–2024) | `ℝ⊗ℂ⊗ℍ⊗𝕆`, ideals of `ℂ⊗𝕆` | One generation of SM gauge reps as minimal left ideals; unified `SU(3)×U(1)` and `SU(2)×U(1)` from chains; deliberately rigorous | Does **not** predict masses, mixing angles, or couplings — stops before dynamics |
| **Dixon** (1994–) | `𝕋 = ℝ⊗ℂ⊗ℍ⊗𝕆` | Long-running derivation of SM rep content; some mass/structure attempts | Conservative; no precision mass/mixing program |
| **Todorov & Dubois-Violette** (2018–) | exceptional Jordan algebra `J₃(𝕆)` | SM gauge group from automorphisms/derivations of `J₃(𝕆)`; some mass relations | Stops before a full flavour spectrum; no continuum action |
| **Baez & Huerta** (2010) | `𝕆`, triality, `SO(8)` | Rigorous octonion/triality theorems; the algebraic 3-fold structure | Pure mathematics; make no phenomenological mass claims |
| **Boyle & Krasnov** (2020–) | octonions, `ℝ⊗ℂ⊗ℍ⊗𝕆`, `Cl(8)` | Gauge-group and rep-level results; CPT-symmetric cosmology (Boyle) | Conservative on numbers; no mass/mixing fits |
| **Lisi** (2007) — *cautionary* | `E8` | Pattern-matched SM+gravity into `E8` | Broken by Distler–Garibaldi no-go (chiral fermions + 3 generations not embeddable as claimed) |

---

## 2. Claim-by-claim grant/dispute matrix

Status legend: **GRANT** = prior work proves or would accept it; **STOP** = prior
work stops before making this claim (neither supports nor disputes); **DISPUTE** =
prior work or a known result would actively contest it.

| CHO claim | Furey | Dixon | Todorov/D-V | Baez/Huerta | Boyle/Krasnov | Notes |
|---|---|---|---|---|---|---|
| SM gauge group `⊂ Aut(ℂ⊗ℍ⊗𝕆)` (`01_algebra.md` §2) | **GRANT** | **GRANT** | **GRANT** (via `J₃(𝕆)`) | n/a | **GRANT** | Best-supported CHO claim; directly in the literature |
| One generation = minimal ideals (A2) | **GRANT** | **GRANT** | partial | n/a | **GRANT** | Furey's home turf; CHO should cite her ideal construction directly |
| Triality → exactly 3 generations (G1/G2) | **STOP** | **STOP** | **STOP** | **GRANT** (triality math) | **STOP** | Baez/Huerta supply the triality theorems; the *physical* 3-generation identification is CHO's own step and is **not** established by anyone — see `three_generations_nogo_audit.py` |
| `ε₀² = π/432` and the flavour bridges (F0, M1–M5) | **STOP** | **STOP** | **STOP** | **STOP** | **STOP** | No peer makes mass-number claims; CHO is alone here. `foundations/02_action.md` is the first action-level support |
| CKM / PMNS from triality (C1–C4, N1–N5) | **STOP** | **STOP** | **STOP** | **STOP** | **STOP** | Entirely CHO; unsupported and unchallenged by prior work |
| `m_H`, `m_t`, `M_W`, `α⁻¹`, `sin²θ_W` numbers | **STOP** | **STOP** | **STOP** | **STOP** | **STOP** | Numerically aggressive; this is where referees from this field will push hardest |
| Cosmological constant `Λ^(1/4)` (CC1) | **STOP** | **STOP** | **STOP** | **STOP** | partial (Boyle: CPT vacuum) | Boyle's CPT-symmetric universe is a *different* CC mechanism; worth contrasting |
| Dynamical gravity from `𝒜` | **STOP** | **STOP** | **STOP** | **STOP** | **STOP** | No one in this lineage has it; neither does CHO (see `PLAN.MD`, T4) |

---

## 3. What this tells us

1. **CHO's gauge-sector claims are well-supported** and overlap heavily with
   Furey, Dixon, Todorov, and Boyle. These should be *cited*, not presented as
   novel. The `J₃(𝕆)` trace space in `SPURION_BRIDGE.md` is the same object
   Todorov & Dubois-Violette use — that overlap is an asset and should be made
   explicit.

2. **CHO's three-generations claim leans on Baez–Huerta triality math but adds a
   physical identification no one else makes.** This is the single most important
   thing to defend rigorously, because it is the headline "theorem" and it is
   exactly the kind of step that the Distler–Garibaldi no-go demolished for Lisi's
   `E8`. See §4 and `three_generations_nogo_audit.py`.

3. **Everything numerical (masses, mixing, Λ) is CHO-only.** No peer supports it,
   but no peer disputes it either — because they all stop before making numerical
   claims. This is CHO's genuine novelty *and* its exposure: it cannot borrow
   anyone else's rigor for these rows. Their credibility rests entirely on the
   internal audit (`DERIVATION_LEDGER.md`, `look_elsewhere.py`, `covariance_gof.py`)
  and on closing the bridges ([foundations/02_action.md](foundations/02_action.md)
  and [ROBUSTNESS_ACTIONS.md](ROBUSTNESS_ACTIONS.md)).

---

## 4. The Lisi / Distler–Garibaldi lesson

Lisi's `E8` theory also used an exceptional algebra and pattern-matched the SM.
Distler & Garibaldi (2009) proved a representation-theory **no-go**: one cannot
embed three chiral generations the way the model claimed (the construction forces
mirror/vector-like partners). The lesson for CHO is sharp:

> Algebraic generation-counting collapses the moment a representation-theory
> obstruction is found. CHO's `N_gen = 3` must survive the *chirality* and
> *embedding* tests, not merely the triality-counting test.

This is why the audit trail pairs this comparison with an active stress-test of
G1/G2 (`compute/three_generations_nogo_audit.py`): the goal is to *try to break*
the three-generations theorem the way `E8` was broken. If it survives, it becomes
CHO's strongest rigorous result; if it does not, G1/G2 drop from *theorem* to
*conjecture* in the ledger — which is the honest outcome.

---

## 5. References to preserve in future writeups

These should be preserved in any future paper rewrite or markdown exposition of
the division-algebra background:

- C. Furey, *Standard model physics from an algebra?* (PhD thesis, 2015) and
  *`SU(3)×SU(2)×U(1)(×U(1))` as a symmetry of division algebraic ladder operators* (2018).
- G. M. Dixon, *Division Algebras: Octonions, Quaternions, Complex Numbers and the
  Algebraic Design of Physics* (1994).
- I. Todorov & M. Dubois-Violette, *Deducing the symmetry of the standard model
  from the automorphism and structure groups of the exceptional Jordan algebra* (2018).
- J. Baez & J. Huerta, *Division algebras and supersymmetry* (2010); J. Baez,
  *The Octonions* (2002).
- L. Boyle, *The Standard Model, the Exceptional Jordan Algebra, and Triality* (2020);
  N. Furey & M. Hughes; K. Krasnov, *octonions and the Standard Model* (2021–).
- A. G. Lisi, *An Exceptionally Simple Theory of Everything* (2007); J. Distler &
  S. Garibaldi, *There is no "Theory of Everything" inside E8* (2009) — cited as the
  no-go benchmark CHO's G1/G2 must survive.

(Exact citation keys/years to be verified against the published versions before
the papers are compiled.)
