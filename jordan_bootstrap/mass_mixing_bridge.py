"""Gate O29 -- the mass<->mixing bridge: one Fock module ties masses to angles.

O28 showed the octonion Fano plane forces a web of parameter-free relations among
the *mixing* observables. This gate closes the loop to the *mass* sector, exactly
over ``Q``, porting the master-branch cross bridge (``compute/epsilon_channel_coefficients.py``
and ``epsilon_free_mass_mixing_bridge.py`` behind Zenodo 21107402).

The charged-fermion mass ratios are driven by the *same* single knob ``eps0^2 =
pi/432`` through integer **Fock-grade counts** of the O11 number operator ``N``. Its
grade multiplicities (eigenvalues ``0,1,2,3``) are exactly ``(1, 3, 3, 1)`` with
total ``8 = 2^3 = dim Lambda^*(C^3)``, and the mass-sector coefficients are traces of
its spectral projectors:

    up      m_c/m_t     = 1 * eps0^2     (Tr P_0, grade-0 vacuum / colour singlet)
    down    m_s/m_b     = 3 * eps0^2     (Tr P_1, grade-1 / colour triplet)
    lepton  m_mu/m_tau  = 8 * eps0^2     (Tr I, the full Fock module 2^3)

Together with the O28 mixing counts (``|V_us|^2 = 7``, ``sin^2 theta13 = 3``,
``dm21^2/dm31^2 = 4``, all ``* eps0^2``), *every* observable is ``(integer) * eps0^2``.
So dividing **any mass ratio by any mixing observable cancels the knob**, leaving a
pure rational relating a quark or lepton *mass* to a *mixing* angle -- a cross-sector
bridge with no free parameter. Exact over ``Q``:

1. **The headline identity ``m_s/m_b = sin^2(theta13)``.** Both carry the integer
   ``3`` -- but from *independent* origins: the mass ``3`` is the Fock grade-1 trace
   ``Tr P_1`` (colour-triplet dimension), the mixing ``3`` is the count of Fano lines
   *through* the vacuum. That two separately-assigned integers coincide is a genuine
   structural statement, not a tuning: a *down-quark mass ratio equals the leptonic
   reactor mixing probability*.
2. **Lepton-sector ties.** ``m_mu/m_tau = 2 * (dm21^2/dm31^2)`` (``8 = 2*4``) and
   ``m_mu/m_tau = (8/3) sin^2(theta13)`` (``8`` vs ``3``).
3. **Consistency with the O28 web.** ``m_s/m_b / |V_us|^2 = 3/7`` is exactly the O28
   ratio ``R1`` -- because ``m_s/m_b = sin^2(theta13)``.
4. **Mass-mass ratios.** The grade counts alone give ``(m_s/m_b)/(m_c/m_t) = 3``,
   ``(m_mu/m_tau)/(m_s/m_b) = 8/3``, ``(m_mu/m_tau)/(m_c/m_t) = 8``.

**Data confrontation.** The stored quark inputs are quoted at different
renormalisation scales.  Their apparent precision is therefore not a physical
test until they are evolved to one declared scheme and scale.  Central-value
comparisons remain diagnostics, not promotion criteria.

Non-claim: what is forced exactly is (i) the mass counts ``{1, 3, 8}`` as ``N``-grade
traces on the O11 Fock module, and (ii) the ``eps0``-free cross ratios once the
master's *adopted* assignment of counts to observables (which grade labels which mass
ratio, which Fano count labels which angle) is granted. The absolute scale ``eps0^2 =
pi/432`` and those assignments are adopted, not derived; the ``m_c/m_t`` relations are
scale-dependent; no absolute masses, hierarchy origin, or CP phase follows. The value
is that a *single finite Fock module* -- the same ``C (x) O`` ladder that gave colour
and charge -- forces several currently-correct relations *across* the mass and mixing
sectors. Cross-refs master ``compute/epsilon_channel_coefficients.py``,
``epsilon_free_mass_mixing_bridge.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from .fermion_charges import charge_multiplicities
from .mixing_web import cabibbo_count, mass_splitting_count, reactor_count

_MULT = charge_multiplicities()  # (1, 3, 3, 1)


def up_count() -> int:
    """The up-sector mass coefficient ``m_c/m_t / eps0^2 = 1`` (``Tr P_0``)."""
    return _MULT[0]


def down_count() -> int:
    """The down-sector mass coefficient ``m_s/m_b / eps0^2 = 3`` (``Tr P_1``)."""
    return _MULT[1]


def lepton_count() -> int:
    """The lepton mass coefficient ``m_mu/m_tau / eps0^2 = 8`` (``Tr I``, full Fock)."""
    return sum(_MULT)


def mass_counts() -> Tuple[int, int, int]:
    """The three mass-sector Fock-grade coefficients ``(up, down, lepton) = (1, 3, 8)``."""
    return (up_count(), down_count(), lepton_count())


# --- exact eps0-free cross ratios (mass ratio / mixing observable) ---
def ratio_ms_mb_over_theta13() -> Fraction:
    """``(m_s/m_b) / sin^2(theta13) = down/reactor = 3/3 = 1`` -- the headline."""
    return Fraction(down_count(), reactor_count())


def ratio_mmu_mtau_over_splitting() -> Fraction:
    """``(m_mu/m_tau) / (dm21^2/dm31^2) = lepton/splitting = 8/4 = 2``."""
    return Fraction(lepton_count(), mass_splitting_count())


def ratio_mmu_mtau_over_theta13() -> Fraction:
    """``(m_mu/m_tau) / sin^2(theta13) = lepton/reactor = 8/3``."""
    return Fraction(lepton_count(), reactor_count())


def ratio_ms_mb_over_cabibbo() -> Fraction:
    """``(m_s/m_b) / |V_us|^2 = down/cabibbo = 3/7`` -- equals O28's ``R1``."""
    return Fraction(down_count(), cabibbo_count())


def headline_identity_holds() -> bool:
    """Exact check ``m_s/m_b = sin^2(theta13)``: the down and reactor counts coincide."""
    return down_count() == reactor_count()


def matches_o28_reactor_ratio() -> bool:
    """Exact check that ``(m_s/m_b)/|V_us|^2`` equals the O28 web ratio ``R1 = 3/7``."""
    from .mixing_web import ratio_theta13_over_cabibbo

    return ratio_ms_mb_over_cabibbo() == ratio_theta13_over_cabibbo()


# --- exact mass-mass ratios (grade counts only) ---
def ratio_down_over_up() -> Fraction:
    """``(m_s/m_b)/(m_c/m_t) = 3``."""
    return Fraction(down_count(), up_count())


def ratio_lepton_over_down() -> Fraction:
    """``(m_mu/m_tau)/(m_s/m_b) = 8/3``."""
    return Fraction(lepton_count(), down_count())


def ratio_lepton_over_up() -> Fraction:
    """``(m_mu/m_tau)/(m_c/m_t) = 8``."""
    return Fraction(lepton_count(), up_count())


# --------------------------------------------------------------------------
# Data confrontation -- documented measured central values.
# --------------------------------------------------------------------------
# Charged-fermion inputs (PDG 2024, GeV): m_c(m_c), m_t(m_t), m_s(2 GeV),
# and m_b(m_b). The quark ratios below therefore mix scales and are flagged.
# Mixing uses NuFIT 6.0 normal-ordering central values.
_MC, _MT = 1.27, 163.0
_MS, _MB = 0.0934, 4.183
_MMU, _MTAU = 0.1056584, 1.77686
_S13 = 0.0222
_RDM = 7.43e-5 / 2.500e-3

_R_UP = _MC / _MT
_R_DOWN = _MS / _MB
_R_LEP = _MMU / _MTAU


def _dev(predicted: float, measured: float) -> float:
    return (measured - predicted) / predicted


def data_confrontation() -> List[Tuple[str, Fraction, float, float, bool]]:
    """Rows ``(name, predicted rational, measured, deviation, scale_sensitive)``."""
    rows: List[Tuple[str, Fraction, float, float, bool]] = []
    p = ratio_ms_mb_over_theta13()
    rows.append(("m_s/m_b = sin2_theta13", p, _R_DOWN / _S13,
                 _dev(float(p), _R_DOWN / _S13), True))
    p = ratio_mmu_mtau_over_splitting()
    rows.append(("m_mu/m_tau = 2*(dm21/dm31)", p, _R_LEP / _RDM,
                 _dev(float(p), _R_LEP / _RDM), False))
    p = ratio_mmu_mtau_over_theta13()
    rows.append(("m_mu/m_tau = (8/3)*sin2_theta13", p, _R_LEP / _S13,
                 _dev(float(p), _R_LEP / _S13), False))
    p = ratio_lepton_over_down()
    rows.append(("(m_mu/m_tau)/(m_s/m_b) = 8/3", p, _R_LEP / _R_DOWN,
                 _dev(float(p), _R_LEP / _R_DOWN), True))
    # scale-sensitive rows involving the up-sector ratio m_c/m_t
    p = ratio_down_over_up()
    rows.append(("(m_s/m_b)/(m_c/m_t) = 3", p, _R_DOWN / _R_UP,
                 _dev(float(p), _R_DOWN / _R_UP), True))
    p = ratio_lepton_over_up()
    rows.append(("(m_mu/m_tau)/(m_c/m_t) = 8", p, _R_LEP / _R_UP,
                 _dev(float(p), _R_LEP / _R_UP), True))
    return rows


def max_clean_deviation() -> float:
    """Worst fractional disagreement among the scale-*insensitive* identities."""
    return max(abs(r[3]) for r in data_confrontation() if not r[4])


def clean_bridge_agrees(tolerance: float = 0.03) -> bool:
    """Legacy descriptive threshold over comparable rows; not a promotion gate."""
    return max_clean_deviation() <= tolerance


def empirical_results_are_promotion_gate() -> bool:
    """Mass/mixing agreement requires common-scale RG evolution and covariance."""
    return False


@dataclass(frozen=True)
class MassMixingBridgeCensus:
    """Exact ledger of the mass<->mixing bridge over ``Q``, plus data agreement."""

    grade_multiplicities: Tuple[int, ...]
    mass_counts: Tuple[int, int, int]
    headline_identity: bool
    ms_mb_over_theta13: Fraction
    mmu_mtau_over_splitting: Fraction
    mmu_mtau_over_theta13: Fraction
    ms_mb_over_cabibbo: Fraction
    matches_o28_r1: bool
    down_over_up: Fraction
    lepton_over_down: Fraction
    lepton_over_up: Fraction
    max_clean_deviation: float
    clean_bridge_agrees: bool
    empirical_promotion_allowed: bool


def mass_mixing_bridge_census() -> MassMixingBridgeCensus:
    """Assemble the exact O29 ledger and its current data confrontation."""
    return MassMixingBridgeCensus(
        grade_multiplicities=_MULT,
        mass_counts=mass_counts(),
        headline_identity=headline_identity_holds(),
        ms_mb_over_theta13=ratio_ms_mb_over_theta13(),
        mmu_mtau_over_splitting=ratio_mmu_mtau_over_splitting(),
        mmu_mtau_over_theta13=ratio_mmu_mtau_over_theta13(),
        ms_mb_over_cabibbo=ratio_ms_mb_over_cabibbo(),
        matches_o28_r1=matches_o28_reactor_ratio(),
        down_over_up=ratio_down_over_up(),
        lepton_over_down=ratio_lepton_over_down(),
        lepton_over_up=ratio_lepton_over_up(),
        max_clean_deviation=max_clean_deviation(),
        clean_bridge_agrees=clean_bridge_agrees(),
        empirical_promotion_allowed=empirical_results_are_promotion_gate(),
    )
