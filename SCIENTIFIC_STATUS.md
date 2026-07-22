# Scientific Status and Project Conclusion

This file is the public source of truth for the octonion campaign. Historical
gate narratives describe what was computed; they do not override this status.

**Final status (2026-07-22): PARKED.** The campaign did not derive a physical
flavour theory or produce sufficient novel science to justify continued
formula-building. Its durable outputs are the exact implementations, boundary
results, and explicit no-go gates.

## Claim classes

| Class | Current content | Permitted interpretation |
|---|---|---|
| Exact finite mathematics | Octonion/Jordan identities, representation dimensions, Fano incidence, commutants, finite no-go results | Reproducible mathematical results |
| Prior-work reconstruction | Colour and one-generation structures from division algebras; frame-function Born selection | Exact implementations of known ideas, not new physics |
| Conditional construction | Chirality after adopting a projector; three families after identifying a Jordan frame with generations | Consequences of stated extra inputs |
| Flavour conjecture | Fano/Fock count assignments and `epsilon0^2 = pi/432` | Phenomenological ansatz, not a derivation |
| Open physics | Composite dynamics, CHO-to-Jordan fermion bridge, Yukawa operator, RG matching, CP and hierarchy | Required before claiming new physics |

Unit tests certify code identities and finite enumerations. They do not turn an
adopted physical map or a central-value coincidence into a theorem.

## Executed hardening gates

### O32: canonical Yukawa operator -- **OPEN / NO-GO AT CURRENT INPUT LEVEL**

The adopted Jordan slots carry identical colour actions. Gauge equivariance
therefore permits at least the six-dimensional subspace of real-symmetric
`3 x 3` generation-only textures. If the unbroken frame permutation `S3` is
also imposed, the allowed generation operators reduce to `a I + b J`, which
has a singlet and a degenerate doublet (or a triply degenerate identity) rather
than three distinct masses. In addition, O27's `24`-versus-`32` obstruction means the
project does not yet possess a genuine three-generation weak/chiral fermion
module on which the desired Yukawa map could act.

Consequently no canonical Yukawa operator is derived. A hierarchy requires a
new symmetry-breaking spurion or action; its direction and measure must be
selected independently of measured masses.

### O33: flavour assignment audit -- **DIAGNOSTIC ONLY**

All six assignments of the Fano counts `{3,4,7}` to
`{|V_us|^2, sin^2(theta13), Delta m^2_21/Delta m^2_3l}` are enumerated. The
adopted `(7,3,4)` mapping is currently the best of those six after profiling one
common scale (`epsilon^2 = 0.007213`, `chi^2 = 6.03` for two nominal degrees of
freedom, approximate `p = 0.049`). The lightweight audit lacks the experimental
covariance matrix, and a conservative correction for inspecting six assignments
gives `p = 0.295`. These numbers are diagnostics, not a publication-grade fit.

The fixed value `pi/432` gives `chi^2 = 9.83` for the same three inputs and is
reported separately from the profiled scale. No empirical tolerance is a
test-suite promotion criterion.

O29's quoted quark ratios use `m_c(m_c)/m_t(m_t)` and
`m_s(2 GeV)/m_b(m_b)`. These are mixed-scale inputs. They cannot support
precision claims until all masses are evolved in one scheme to one declared
scale with uncertainties and threshold corrections.

## Closure decision

The flavour programme is closed at its present level. Do not add further fitted
integer relations. Reopening it would require an independently motivated result
that simultaneously supplies:

1. a genuine three-generation fermion module with the complete gauge and chiral
   action;
2. a canonical symmetry-breaking action selecting a unique Yukawa/Dirac
   operator without measured inputs; and
3. new observables frozen before comparison, with RG evolution and covariance.

The repository should be cited, if useful, as an exploratory computational
record rather than as a completed theory or a derivation of Standard Model
parameters.

## What should be done differently next time

1. **Start with a literature gap, not a suggestive algebra.** State one result
   that experts do not already know and verify novelty before building a large
   campaign.
2. **Make the bridge the first gate.** Do not calculate phenomenology until the
   physical state space, dynamics and observable map are derived.
3. **Separate theorem discovery from data confrontation.** Freeze definitions,
   parameters and predictions before opening experimental tables.
4. **Count model choices as parameters.** Channel assignments, factorisations,
   representation choices and octants contribute to look-elsewhere freedom even
   when their final formulas contain no continuous knob.
5. **Require scale-correct observables.** Specify scheme, matching scale, RG flow,
   uncertainties and covariance before describing numerical agreement.
6. **Use tests for mathematics, not epistemology.** Tests can certify an exact
   census; they cannot certify that a physical interpretation is true.
7. **Set an early kill condition.** If the construction admits an arbitrary
   commutant or needs a hand-selected spurion, stop before fitting constants.

## Better targets

The most promising continuation is methodological rather than a new Theory of
Everything:

- develop reusable exact-arithmetic tools for nonassociative and Jordan-algebra
  calculations, with independently useful classification or obstruction
  theorems;
- investigate a narrowly stated commutant, representation or composability
  classification only after confirming it is open in the literature; or
- study approximate coarse-graining, recoverability and interaction using
  operator algebras or quantum error correction, targeting a theorem with clear
  assumptions rather than a reconstruction of observed constants.

Any future phenomenological project should begin from a Lagrangian or operational
dynamics, produce a small preregistered set of genuinely out-of-sample
predictions, and accept falsification without adding corrective structure.
