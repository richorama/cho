"""
BIG-BETS Bet 2 (EXPLORATORY) -- entropic gravity / horizon counting x CHO.
==========================================================================

Companion to causal_set_lambda.py.  That module asked whether *counting* gives
the cosmological constant (the first thing the static algebra C(x)H(x)O gated
out) a dynamical origin.  This module asks the same question of the OTHER thing
CHO gated out -- GRAVITY itself -- which is why CHO was never a Theory of
Everything.  The tool is the same: dynamics from counting.

The setting (Jacobson 1995).  Einstein's equations are an EQUATION OF STATE: if
every local Rindler horizon obeys the Clausius relation dQ = T dS with the Unruh
temperature T and the Bekenstein-Hawking entropy

        S  =  A / (4 G)  =  A / 4        (Planck units, G = ell_P^2 = 1),

then  R_uv - (1/2) R g_uv + Lambda g_uv = 8 pi G T_uv  FOLLOWS.  The single
input that is not thermodynamics is the coefficient 1/4 -- a pure number that
fixes Newton's G.  Just like Lambda's exponent and the pi/432 holonomy, the
static algebra cannot EMIT this number; it is the gated-out gravitational sector.

The counting ansatz (this module).  Tile a horizon with cells, each carrying a
CHO internal Hilbert space of dimension d (d in {2,3,4,7,8,16,26,27,...}: qubit,
generation index, H, O, spinor 16, J3(O), ...).  Local counting gives

        S  =  (A / a_cell) * ln d   ~   A          (AREA LAW, automatically).

So counting supplies the area-extensive entropy Jacobson needs -- the structural
prerequisite for the Einstein equation of state.  That is the dynamics-from-
counting move (gold-standard criterion A) applied to gravity.

What counting does and does NOT fix (the honest core).  Matching S = A/4 forces

        a_cell  =  4 ln d        (Planck areas per CHO cell).

d=2 reproduces the textbook "it-from-bit" value 4 ln 2 = 2.77 Planck-areas/bit.
But the coefficient 1/4 (= Newton's G) is NOT derived -- it is RELOCATED into the
cell area a_cell, which CHO does not independently fix.  Worse, the CHO internal
dimension is pure BIT-BOOKKEEPING for the coefficient:

        N_cells * log2(d)  ==  N_bits         (exactly, for every d),

i.e. a d-state cell just packs log2(d) bits and changes nothing about 1/4.  This
is a cleaner, more DECISIVE negative than the Lambda probe: there counting
recovered the exponent 64 (suggestively); here counting provably touches only the
FORM (area law) and not the CONTENT (the value of G).  Static algebra -> kinematics
(entropy is area-extensive), never dynamics (the value of G).

The sharp cross-module tension (the real payoff).  causal_set_lambda.py reproduces
Lambda with ONE causal-set atom per Planck 4-volume (Planck sprinkling density).
The Dou-Sorkin result says horizon "molecules" of such a causal set count the AREA:
N_mol ~ rho^(1/2) A = A / ell_P^2 (one molecule per Planck area).  If each molecule
carried a full CHO internal state of dimension d, the horizon entropy would be

        S  =  N_mol * ln d  =  (A / ell_P^2) * ln d  =  (4 ln d) * (A/4),

i.e. (4 ln d)-times TOO BIG: a factor ~13 over Bekenstein-Hawking for d = 27 = J3(O).
So the SAME Planck-density causal set that nails Lambda would VIOLATE the
Bekenstein-Hawking bound unless the CHO internal state is HORIZON-UNRESOLVED (a
gauge/projected direction, not a free horizon degree of freedom).  That is a
definite, falsifiable constraint linking the two Bet-2 modules.

VERDICT: EXPLORATORY.  The area law (hence the Einstein equation of state via
Jacobson) emerges from counting -- the dynamics the static algebra lacked -- but
Newton's G (the 1/4) is NOT derived; it is relocated to a_cell = 4 ln d, and CHO's
internal dimension is pure bookkeeping for it.  No prediction is promoted, NO Bayes
credit moves (this is the gated-out gravity sector, disjoint from the frozen
flavour/CC rows).  The module asserts the exact bookkeeping AND a humility tripwire
(the required cell area spreads too widely across the CHO menu to pick a unique
horizon cell, so "CHO fixes G" cannot be silently claimed).
"""
import numpy as np

from causal_set_lambda import ELL_P   # same Planck/atom scale as the Lambda module

# --- Bekenstein-Hawking / Jacobson input:  S = A/(4G) = A/4 in Planck units ---
BH_COEFF = 0.25            # S = BH_COEFF * A ; the 1/4 that fixes Newton's G

# --- CHO internal-state dimensions a horizon cell could carry (the menu) ---
CHO_DIMS = {
    2: "qubit (it-from-bit)", 3: "generation index", 4: "quaternion H",
    7: "imaginary O", 8: "octonion O", 14: "g2", 16: "spinor 16",
    26: "traceless J3(O)", 27: "J3(O)", 28: "so(8)", 52: "f4", 78: "e6",
}

IT_FROM_BIT_AREA = 4.0 * np.log(2.0)   # 2.7726 Planck-areas/bit (textbook reference)
MENU_SPREAD_MIN = 5.0     # humility: a_cell spread over the menu must exceed this


def required_cell_area(d):
    """Cell area (Planck areas) that makes S=(A/a_cell)ln d match S = BH_COEFF*A."""
    return np.log(d) / BH_COEFF        # = 4 ln d


def cho_cell_table():
    """For each CHO dimension: (d, name, required a_cell, bits/cell = log2 d)."""
    rows = []
    for d, name in CHO_DIMS.items():
        rows.append((d, name, required_cell_area(d), np.log2(d)))
    return rows


def area_law_ratio(d, a_cell=1.0):
    """S(2A)/S(A) for the local-counting ansatz -- exactly 2 (entropy ~ area)."""
    def S(A):
        return (A / a_cell) * np.log(d)
    return S(2.0) / S(1.0)


def planck_tiled_overcount(d):
    """One CHO state per Planck area gives S/A = ln d; overcount vs BH = ln d / (1/4)."""
    s_over_a = np.log(d)
    return s_over_a, s_over_a / BH_COEFF


def naive_match_dimension():
    """d that would give S = A/4 at one cell per Planck area: ln d = 1/4 => d = e^(1/4)."""
    return np.exp(BH_COEFF)


def bit_bookkeeping(d, A=1.0):
    """Show N_cells*log2(d) == N_bits: the CHO dimension is pure bit-bookkeeping."""
    n_cells = A / required_cell_area(d)
    n_bits = A / IT_FROM_BIT_AREA
    return n_cells * np.log2(d), n_bits


def dou_sorkin_density(d):
    """Required causal-set sqrt-density per Planck area so N_mol*ln d = BH_COEFF*A."""
    return BH_COEFF / np.log(d)


def main():
    print("=" * 70)
    print("BIG-BETS Bet 2: entropic gravity  S=A/4  vs CHO horizon counting  (EXPLORATORY)")
    print("=" * 70)

    # ---- [A] the gap: Jacobson needs the pure number 1/4 ----
    print("\n[A] Jacobson 1995: dQ = T dS with S = A/(4G) = A/4  =>  Einstein equations.")
    print("    The coefficient 1/4 (= 1/4G) is a PURE NUMBER that fixes Newton's G --")
    print("    the gated-out GRAVITY sector the static algebra cannot emit (cf. Lambda, pi/432).")

    # ---- [B] counting -> area law (the dynamics-from-counting move) ----
    print("\n[B] Counting ansatz: horizon tiled by cells carrying CHO internal dim d.")
    print("    S = (A/a_cell) ln d  ~  A  (AREA LAW, automatic from local counting).")
    r = area_law_ratio(27, a_cell=1.0)
    print("    area-law check: S(2A)/S(A) = %.3f  => S is area-extensive (criterion A:" % r)
    print("    counting supplies the entropy Jacobson's equation of state needs).")

    # ---- [C] the coefficient: a_cell = 4 ln d over the CHO menu ----
    print("\n[C] Match S = A/4  =>  a_cell = 4 ln d  (Planck areas per CHO cell):")
    print("      %-3s %-22s %-10s %s" % ("d", "interpretation", "a_cell", "bits/cell"))
    for d, name, a_cell, bits in cho_cell_table():
        print("      %-3d %-22s %8.3f   %5.3f" % (d, name, a_cell, bits))
    print("    d=2 reproduces the textbook it-from-bit value 4 ln 2 = %.4f Planck-areas/bit."
          % IT_FROM_BIT_AREA)

    # ---- [D] decisive negative: bookkeeping + species/overcount ----
    print("\n[D] What counting does NOT fix (the honest core):")
    for d in (2, 8, 16, 27):
        prod, n_bits = bit_bookkeeping(d)
        print("      d=%2d: N_cells*log2(d) = %.6f  ==  N_bits = %.6f" % (d, prod, n_bits))
    print("    => the CHO dimension is PURE BIT-BOOKKEEPING; it changes nothing about 1/4.")
    print("    Species/overcount: one CHO state per Planck area (a_cell=1) gives S/A = ln d:")
    for d in (2, 16, 27):
        s_over_a, factor = planck_tiled_overcount(d)
        print("      d=%2d: S/A = %.3f  >>  1/4 = %.3f   (overcount x %.1f)"
              % (d, s_over_a, BH_COEFF, factor))
    d_req = naive_match_dimension()
    print("    To hit S=A/4 at one cell/Planck-area needs ln d = 1/4 => d = e^(1/4) = %.4f"
          % d_req)
    print("    -- not an integer and below 2: NO quantum system (let alone a CHO rep) works.")

    # ---- [E] the sharp cross-module tension (ties to causal_set_lambda.py) ----
    print("\n[E] Cross-module tension with causal_set_lambda.py (the real payoff):")
    print("    That module reproduces Lambda with ONE atom per Planck 4-volume (Planck rho).")
    print("    Dou-Sorkin: such a causal set's horizon molecules count AREA, N_mol ~ A/ell_P^2.")
    print("    If each molecule carried a full CHO state of dim d, then")
    for d in (16, 27):
        factor = np.log(d) / BH_COEFF
        print("      d=%2d: S = N_mol ln d = (4 ln d)(A/4) = %.1f x Bekenstein-Hawking" % (d, factor))
    print("    => the SAME Planck-density causal set that nails Lambda would OVERCOUNT black-")
    print("       hole entropy by ~13x (d=27) UNLESS the CHO internal state is HORIZON-")
    print("       UNRESOLVED (a gauge/projected direction, not a free horizon d.o.f.).")
    print("    Required sub-Planck molecule sqrt-density for consistency: rho^(1/2) =")
    for d in (16, 27):
        print("      d=%2d: %.4f per Planck area" % (d, dou_sorkin_density(d)))
    a27_m2 = required_cell_area(27) * ELL_P ** 2
    print("    (physical horizon cell for d=27: a_cell = %.2f ell_P^2 = %.3e m^2)"
          % (required_cell_area(27), a27_m2))

    # ---- [F] verdict + falsifier ----
    print("\n[F] Verdict & falsifier")
    print("    WIN: the area law (=> Einstein equation of state via Jacobson) emerges from")
    print("         counting -- the dynamics the static algebra lacked (criterion A).")
    print("    NEGATIVE: Newton's G (the 1/4) is NOT derived -- relocated to a_cell = 4 ln d;")
    print("         the CHO dimension is pure bookkeeping for it.")
    print("    FALSIFIER: if the CHO internal state is a genuine horizon d.o.f. at Planck")
    print("         density, S is (4 ln d)x too large -- the Lambda-fixing causal set is")
    print("         refuted; it SURVIVES only if the internal state is horizon-unresolved")
    print("         (a definite prediction). KILL if the 1/4 provably needs continuum CFT")
    print("         (Cardy/central-charge) input no CHO microstate counting can supply.")
    print("    EXPLORATORY: no prediction promoted; NO Bayes credit moves.")

    # ---- stable tripwires (exact bookkeeping + humility) ----
    # Area law is exactly linear in A:
    assert abs(area_law_ratio(27, a_cell=1.0) - 2.0) < 1e-12, "entropy not area-extensive"
    # d=2 reproduces the textbook it-from-bit cell area:
    assert abs(required_cell_area(2) - IT_FROM_BIT_AREA) < 1e-9, "it-from-bit value lost"
    assert abs(IT_FROM_BIT_AREA - 2.7725887) < 1e-5, "4 ln 2 drifted"
    # Bit-bookkeeping identity: the CHO dimension carries NO info about the 1/4:
    for d in CHO_DIMS:
        prod, n_bits = bit_bookkeeping(d)
        assert abs(prod - n_bits) < 1e-12, "bit-bookkeeping identity broke for d=%d" % d
    # Species/overcount: Planck-tiling ALWAYS overcounts (ln d > 1/4 for every CHO d>=2):
    for d in CHO_DIMS:
        assert np.log(d) > BH_COEFF, "no overcount for d=%d?" % d
    # The naive one-cell-per-Planck-area match has NO integer/quantum solution:
    d_req = naive_match_dimension()
    assert 1.0 < d_req < 2.0, "e^(1/4) left the (1,2) no-solution window"
    # HUMILITY: required cell area spreads widely over the menu => CHO does not pick G:
    areas = [required_cell_area(d) for d in CHO_DIMS]
    assert (max(areas) - min(areas)) > MENU_SPREAD_MIN, "menu collapsed -- re-examine"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
