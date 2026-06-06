"""
Derived-vs-residual accounting for the continuum/RG-gap observables.
====================================================================

For alpha, sin^2(theta_W), and M_W the CHO framework derives a clean algebraic
TERM, and then relies on an UNDERIVED continuum/RG residual to reach the
measured value:

    alpha^-1(0)   = 128*pi/3        + Delta(vacuum polarization)
    sin^2 theta_W = 1/4             + Delta(RG running to M_Z)
    M_W           = M_P / 3^36      * (normalization not yet derived)

Reporting these at "<0.1% error" is misleading, because the <0.1% includes the
residual that has NOT been computed from CHO. The honest figure of merit is:

    * the error of the DERIVED term alone, and
    * what fraction of the gap the underived residual must supply.

A small residual fraction means the derived algebra already does most of the
work and the remaining continuum calculation is a correction. A large residual
fraction means the headline agreement is mostly carried by physics CHO has not
yet derived.
"""
import math

PI = math.pi


def report(name, derived_term, measured, residual_label, derived_is_factor=False):
    if derived_is_factor:
        # M_W case: derived value is the bare algebraic scale; residual is a
        # multiplicative O(1) normalization.
        gap = measured / derived_term
        derived_err = (derived_term - measured) / measured
        residual_size = abs(gap - 1.0)
        print(f"  {name}")
        print(f"    derived algebraic value : {derived_term:.5g}")
        print(f"    measured                : {measured:.5g}")
        print(f"    derived-term error      : {derived_err*100:+.2f}%")
        print(f"    required {residual_label:<22}: x{gap:.4f}  "
              f"(|residual| = {residual_size*100:.1f}%)")
        print()
        return
    derived_err = (derived_term - measured) / measured
    residual = measured - derived_term
    residual_frac = abs(residual) / abs(measured)
    print(f"  {name}")
    print(f"    derived algebraic term  : {derived_term:.5g}")
    print(f"    measured                : {measured:.5g}")
    print(f"    derived-term error      : {derived_err*100:+.2f}%  "
          f"(this is the HONEST error bar on the derived piece)")
    print(f"    underived residual      : {residual:+.5g}  ({residual_label})")
    print(f"    residual / measured     : {residual_frac*100:.2f}%  "
          f"<- carried by physics not yet derived from CHO")
    print()


def main():
    print("=" * 72)
    print("  CHO DERIVED-vs-RESIDUAL ACCOUNTING (continuum/RG-gap observables)")
    print("  Puts the error bar on the part CHO actually derives.")
    print("=" * 72)
    print()

    # alpha^-1: derived term 128*pi/3, residual = leptonic+hadronic VP.
    report("alpha^-1(0)  =  128*pi/3  +  VP",
           128 * PI / 3, 137.036, "vacuum polarization below Lambda_QCD")

    # sin^2 theta_W: derived term 1/4, residual = RG running to M_Z.
    report("sin^2 theta_W  =  1/4  +  RG",
           0.25, 0.23122, "RG running 1/4 -> M_Z")

    # M_W: derived bare scale M_P/3^36, residual = O(1) normalization.
    M_P = 1.221e19
    report("M_W  =  M_P / 3^36  x  norm",
           M_P / 3.0**36, 80.377, "electroweak normalization",
           derived_is_factor=True)

    print("  Summary")
    print("  " + "-" * 60)
    print("   * alpha and sin^2(theta_W): the DERIVED terms are ~2.2% and ~8%")
    print("     from data; the small printed '<0.1%' belongs to the FULL formula")
    print("     including the underived residual. Quote the derived-term error.")
    print("   * M_W: the bare algebraic scale already lands ~1.2% high with an")
    print("     O(1) normalization; the normalization itself is not yet derived.")
    print("   * Next proof obligation (per DERIVATION_LEDGER S1,S4,S5): derive")
    print("     each residual from the lattice action + RG, then these become")
    print("     genuine sub-percent predictions instead of derived-term + gap.")
    print()


if __name__ == "__main__":
    main()
