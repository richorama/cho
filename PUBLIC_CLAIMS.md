# Public Claims Table

Created: 2026-06-07

Purpose: one public-facing source of truth for what the framework may claim today. If a claim is stronger than this table, weaken the claim or upgrade the ledger first.

## Claim Status

| Claim area | Public wording to use | Current status | Do not say yet |
|---|---|---|---|
| Overall scope | A few-input algebraic framework for Standard Model parameter relations from division algebras | Defensible. Gravity is exploratory and the framework is not a completed theory | Completed Theory of Everything; zero-parameter theory |
| Gauge representations | The `C x H x O` / division-algebra gauge and one-generation representation layer is strongly supported by prior work and reproduced here | Derived / prior-work-backed. Cite Furey, Dixon, Todorov-Dubois-Violette, Boyle/Krasnov | Entire gauge sector is a novel CHO invention |
| Electric charge, weak isospin, hypercharge | The one-generation gauge quantum-number map is anomaly-clean and algebraically supported | Strong algebraic result; `physics_map_audit.py` verifies `Q`, `T3`, `Y`, and anomaly cancellation. Three-generation content map remains open | Full fermion-content map or mass spectrum is closed |
| Three generations | The idempotent-frame route gives an obstruction-free count/chirality route to three generations | Count and chirality bridge advanced. Fermion-content map, Dirac operator, and Yukawa spectrum remain open | `N_gen = 3` is fully proved as physical SM generations |
| `epsilon0^2 = pi/432` | A geometrically triangulated bridge whose value is the Bayes-factor hinge | `pi`, `16`, and `27` have strong geometric support; the Phase 2 measure audit isolates the remaining normalized-trace hypothesis | Fully derived prefactor with no residual hypothesis |
| Masses and mixings | Hard-to-vary few-input relations with explicit open operator bridges | Descriptive agreement is interesting; the Phase 3 one-operator gate is executable but theorem status remains open | All SM masses and mixings are derived from first principles |
| CKM/PMNS | Several CKM/PMNS coefficients are derived as counts/half-angles; full matrices remain operator targets | C1/C2/N2/N3/N5 advanced; `yukawa_operator_full.py` shows CKM one-diagonalization and PMNS `DeltaY` remain open | One CHO mass matrix already gives CKM and PMNS completely |
| `alpha`, `sin^2(theta_W)`, `M_W` | Algebraic boundary terms plus underived continuum/RG residuals | Derived pieces are not sub-percent by themselves; RG matching remains open | Sub-percent predictions independent of residual continuum physics |
| Cosmological constant | A striking open bridge for the observed scale | Free-energy factorisation, `3^64`, and `11/12` screening remain proof obligations | Resolved the cosmological constant problem |
| Gravity | A kinematic internal `G2`-covariant metric brick from the octonion associator | Interesting research line. No 4D Lorentzian metric, field equation, or Newton constant yet | Dynamical gravity or GR has been derived |
| Null exclusions | Future-facing falsifiers and weaker consistency targets | Useful only with explicit windows and lower evidential weight than positive predictions | Null experimental results confirm CHO |
| Statistics | Quote covariance and Bayes scoreboard, not raw row count | `N_eff ~ 10`, correlated `chi^2` borderline; `ln B` depends on crediting `pi/432` | 25 independent precision predictions |

## Required Citation Pattern

When writing public prose:

1. Pair every headline with its status in [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md).
2. Pair every statistical claim with [METHODOLOGY_LIMITS.md](METHODOLOGY_LIMITS.md) or `compute/scoreboard.py`.
3. Pair every future claim with [FUTURE_TESTS.md](FUTURE_TESTS.md) and the prediction registry.
4. Pair every gravity claim with [foundations/03_gravity.md](foundations/03_gravity.md).
