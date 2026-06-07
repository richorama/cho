"""
Physics-map audit: one-generation quantum numbers and anomaly cancellation.
===========================================================================

This is the Phase 1 repair artifact from CRITICAL_REPAIR_PLAN.md. It freezes the
current algebra-to-physics map enough to make it auditable:

* Q comes from the C x O number operator (ladder_charges.py).
* weak SU(2) and T3 come from the H factor (weak_isospin_hypercharge.py).
* Y is fixed by Gell-Mann--Nishijima, Y = 2(Q - T3).
* the chiral doublet/singlet dichotomy is represented by the KO-6 idempotent
  (chiral_projector.py / foundations/06_chiral_idempotent.md).

The artifact deliberately does not claim the full fermion-content map is closed.
It checks the algebraic quantum-number ledger and the SM anomaly cancellations;
the remaining open seam is the functorial map from the idempotent-frame tangent
spinors T(OP2) to the field labels below, plus the Yukawa operator.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/physics_map_audit.py
"""

from dataclasses import dataclass
from fractions import Fraction

from ladder_charges import charge_operator, search_witt_basis
from weak_isospin_hypercharge import (
    charges_trace_to_algebra,
    count_weyl as count_gmn_weyl,
    gell_mann_nishijima,
    isospin_eigenvalues,
    isospin_generators,
)
from chiral_projector import aligned_chirality, charge_chirality_table


@dataclass(frozen=True)
class PhysicalField:
    """Physical RH/LH field entry as used by GMN before anomaly conjugation."""

    name: str
    su3: str
    su2: str
    chirality: str
    q: Fraction
    t3: Fraction
    y: Fraction
    multiplicity: int


@dataclass(frozen=True)
class LeftWeylField:
    """All-left-handed anomaly basis; RH fields are represented by conjugates."""

    name: str
    su3: str
    su2: str
    y: Fraction
    color_mult: int
    weak_mult: int


PHYSICAL_FIELDS = [
    PhysicalField("u_L", "3", "2", "L", Fraction(2, 3), Fraction(1, 2), Fraction(1, 3), 3),
    PhysicalField("d_L", "3", "2", "L", Fraction(-1, 3), Fraction(-1, 2), Fraction(1, 3), 3),
    PhysicalField("nu_L", "1", "2", "L", Fraction(0), Fraction(1, 2), Fraction(-1), 1),
    PhysicalField("e_L", "1", "2", "L", Fraction(-1), Fraction(-1, 2), Fraction(-1), 1),
    PhysicalField("u_R", "3", "1", "R", Fraction(2, 3), Fraction(0), Fraction(4, 3), 3),
    PhysicalField("d_R", "3", "1", "R", Fraction(-1, 3), Fraction(0), Fraction(-2, 3), 3),
    PhysicalField("e_R", "1", "1", "R", Fraction(-1), Fraction(0), Fraction(-2), 1),
    PhysicalField("nu_R", "1", "1", "R", Fraction(0), Fraction(0), Fraction(0), 1),
]


ANOMALY_FIELDS = [
    LeftWeylField("Q_L", "3", "2", Fraction(1, 3), 3, 2),
    LeftWeylField("L_L", "1", "2", Fraction(-1), 1, 2),
    LeftWeylField("u_R^c", "3bar", "1", Fraction(-4, 3), 3, 1),
    LeftWeylField("d_R^c", "3bar", "1", Fraction(2, 3), 3, 1),
    LeftWeylField("e_R^c", "1", "1", Fraction(2), 1, 1),
    LeftWeylField("nu_R^c", "1", "1", Fraction(0), 1, 1),
]


def format_fraction(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def limited_fraction(value):
    return Fraction(float(value)).limit_denominator(12)


def is_color_charged(su3):
    return su3 in {"3", "3bar"}


def is_weak_doublet(su2):
    return su2 == "2"


def anomaly_coefficients():
    """Return exact anomaly coefficients in the all-left Weyl basis.

    Hypercharge convention is Q = T3 + Y/2, so these Y values are twice the
    sometimes-used y_SM. Overall normalization does not affect cancellation.
    """
    half = Fraction(1, 2)
    coeffs = {}

    coeffs["SU(3)^2-U(1)"] = sum(
        field.weak_mult * half * field.y
        for field in ANOMALY_FIELDS
        if is_color_charged(field.su3)
    )
    coeffs["SU(2)^2-U(1)"] = sum(
        field.color_mult * half * field.y
        for field in ANOMALY_FIELDS
        if is_weak_doublet(field.su2)
    )
    coeffs["U(1)^3"] = sum(
        field.color_mult * field.weak_mult * field.y ** 3
        for field in ANOMALY_FIELDS
    )
    coeffs["grav^2-U(1)"] = sum(
        field.color_mult * field.weak_mult * field.y
        for field in ANOMALY_FIELDS
    )
    coeffs["Witten SU(2) doublets mod 2"] = sum(
        field.color_mult for field in ANOMALY_FIELDS if is_weak_doublet(field.su2)
    ) % 2
    return coeffs


def lever_spectra():
    fixed, _pairs, _signs, alphas = search_witt_basis()
    if alphas is None:
        raise RuntimeError("Lever C Witt basis was not found; cannot audit physics map.")
    q_oct = charge_operator(alphas)
    t3_eigs = isospin_eigenvalues(isospin_generators()[2])
    q_ok, t_ok, q_spec, t_spec = charges_trace_to_algebra(q_oct, t3_eigs)
    gamma = aligned_chirality(fixed)
    comm, chirality_pairs = charge_chirality_table(q_oct, gamma)
    return {
        "fixed": fixed,
        "q_ok": q_ok,
        "t_ok": t_ok,
        "q_spec": q_spec,
        "t_spec": t_spec,
        "chirality_comm": comm,
        "chirality_pairs": chirality_pairs,
    }


def check_gmn_table():
    rows, gmn_ok = gell_mann_nishijima()
    row_map = {}
    for name, q, t3, y, y_sm, mult, ok in rows:
        row_map[name.split()[0]] = (
            limited_fraction(q),
            limited_fraction(t3),
            limited_fraction(y),
            limited_fraction(y_sm),
            mult,
            ok,
        )

    physical_ok = True
    for field in PHYSICAL_FIELDS:
        q, t3, y, y_sm, mult, ok = row_map[field.name]
        physical_ok = physical_ok and (
            q == field.q
            and t3 == field.t3
            and y == field.y
            and y_sm == field.y
            and mult == field.multiplicity
            and ok
        )
    return rows, gmn_ok and physical_ok and count_gmn_weyl(rows) == 16


def main():
    print("=" * 78)
    print("  PHYSICS MAP AUDIT - one-generation quantum numbers and anomalies")
    print("  Phase 1 repair: freeze the public map, then name the remaining seam.")
    print("=" * 78)

    spectra = lever_spectra()
    _rows, gmn_ok = check_gmn_table()
    anomalies = anomaly_coefficients()
    anomalies_ok = all(value == 0 for value in anomalies.values())
    chirality_ok = spectra["chirality_pairs"] is not None and spectra["chirality_comm"] < 1e-9

    print("\n  ALGEBRAIC INPUTS (machine witnesses)")
    print("  " + "-" * 72)
    print(f"      Lever C fixed colour direction       : e{spectra['fixed']}")
    print(f"      Q spectrum magnitudes from C x O     : {spectra['q_spec']}")
    print(f"      nonzero |T3| spectrum from H         : {spectra['t_spec']}")
    print(f"      Q values used all in spectrum        : {spectra['q_ok']}")
    print(f"      T3 values used all in spectrum       : {spectra['t_ok']}")
    print(f"      |[Q, gamma_Q]|                       : {spectra['chirality_comm']:.2e}")

    print("\n  PUBLIC ONE-GENERATION MAP (before RH conjugation)")
    print("  " + "-" * 72)
    print("      field   SU3  SU2  chi       Q      T3       Y   mult")
    for field in PHYSICAL_FIELDS:
        print(
            f"      {field.name:<6} {field.su3:<4} {field.su2:<4} {field.chirality:<3}"
            f" {format_fraction(field.q):>7} {format_fraction(field.t3):>7}"
            f" {format_fraction(field.y):>7} {field.multiplicity:>5}"
        )
    print(f"\n      GMN table + 16 Weyl count             : {'PASS' if gmn_ok else 'FAIL'}")

    print("\n  ANOMALY AUDIT (all fields written left-handed)")
    print("  " + "-" * 72)
    for name, value in anomalies.items():
        print(f"      {name:<28} {format_fraction(value):>8}   {'PASS' if value == 0 else 'FAIL'}")

    print("\n  SCOPE")
    print("  " + "-" * 72)
    print("   * This closes a bookkeeping gap: the public one-generation quantum")
    print("     numbers are now one explicit table, cross-checked against Lever C")
    print("     charges, Lever D weak isospin, GMN hypercharge, KO-6 chirality")
    print("     compatibility, and exact SM anomaly cancellation.")
    print("   * It does not close the full content map from the three OP2 idempotent")
    print("     tangent spinors to physical field labels, nor the Yukawa operator.")
    print("     Those remain the Phase 1/Phase 3 seams in CRITICAL_REPAIR_PLAN.md.")

    ok = spectra["q_ok"] and spectra["t_ok"] and chirality_ok and gmn_ok and anomalies_ok
    print("\n  VERDICT")
    print("  " + "-" * 72)
    if ok:
        print("      PASS: one-generation quantum-number map is internally consistent")
        print("            and anomaly-clean; content-map/Yukawa seams remain explicit.")
    else:
        print("      FAIL: physics-map consistency check failed; do not quote Q2/G1")
        print("            as a coherent one-generation map until this is resolved.")
        raise SystemExit(1)
    print()


if __name__ == "__main__":
    main()
