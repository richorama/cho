"""
Primitive A_Weyl x J3(O) projector derivation from normalized log-cos action.

This is a conditional derivation, not a complete epsilon proof. It shows that
once a rank-one transition kernel exists, the normalized CHO information action
selects the primitive product projector over all larger projectors containing
the same transition ray.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


DIM_WEYL = 16
DIM_JORDAN = 27


@dataclass(frozen=True)
class BridgeProjector:
    name: str
    weyl_rank: int
    jordan_rank: int
    note: str

    @property
    def rank(self) -> int:
        return self.weyl_rank * self.jordan_rank

    @property
    def cosine(self) -> float:
        return 1.0 / math.sqrt(self.rank)

    @property
    def action(self) -> float:
        return math.log(self.cosine)

    @property
    def epsilon_sq(self) -> float:
        return math.pi * self.rank / (DIM_WEYL * DIM_JORDAN)


def bridge_projectors() -> list[BridgeProjector]:
    return [
        BridgeProjector(
            "primitive Weyl x primitive Jordan",
            1,
            1,
            "unique log-cos maximum",
        ),
        BridgeProjector(
            "full Weyl x primitive Jordan",
            DIM_WEYL,
            1,
            "dilutes the transition over all Weyl channels",
        ),
        BridgeProjector(
            "primitive Weyl x full Jordan",
            1,
            DIM_JORDAN,
            "dilutes the transition over the Jordan trace",
        ),
        BridgeProjector(
            "full Weyl x full Jordan",
            DIM_WEYL,
            DIM_JORDAN,
            "maximal dilution",
        ),
    ]


def raw_trace_for_containing_projector() -> float:
    """Tr(PK) for any idempotent P containing the rank-one kernel K."""
    return 1.0


def print_variational_derivation() -> None:
    print("PRIMITIVE PROJECTOR DERIVATION")
    print("=" * 78)
    print("Local normalized action term:")
    print("  S_link(P,K) = log(<P,K> / (||P|| ||K||))")
    print("Assume K=|tau><tau| is a rank-one transition kernel and P is an")
    print("idempotent bridge projector containing that ray.")
    print()
    print("Then <P,K>=1, ||K||=1, ||P||=sqrt(rank(P)), so")
    print("  S_link = -1/2 log(rank(P)).")
    print("The action is maximal exactly at rank(P)=1.")
    print()


def print_rank_table() -> None:
    print("Rank ladder under the normalized log-cos action")
    print("-" * 78)
    target = math.pi / (DIM_WEYL * DIM_JORDAN)
    header = f"{'embedding':40s} {'rank':>5s} {'cos':>10s} {'S_link':>11s} {'target x':>9s}  note"
    print(header)
    for projector in bridge_projectors():
        multiplier = projector.epsilon_sq / target
        print(
            f"{projector.name:40s} {projector.rank:5d} "
            f"{projector.cosine:10.6f} {projector.action:11.6f} "
            f"{multiplier:9.1f}  {projector.note}"
        )
    print()


def print_why_normalization_matters() -> None:
    print("Why the normalization is doing real work")
    print("-" * 78)
    print(f"Raw trace Tr(PK) = {raw_trace_for_containing_projector():.1f} for every projector P containing K.")
    print("So an unnormalized trace cannot choose between primitive, full-Weyl,")
    print("full-Jordan, or full bridge projectors.")
    print("The normalized log-cos action penalizes each extra trace dimension by")
    print("  Delta S = -1/2 log(r_extra).")
    print()


def print_product_factorization() -> None:
    print("Product factorization")
    print("-" * 78)
    print("For P = P_Weyl x P_Jordan,")
    print("  rank(P) = rank(P_Weyl) rank(P_Jordan)")
    print("  S_link  = -1/2 log(rank(P_Weyl)) -1/2 log(rank(P_Jordan)).")
    print("Therefore the unique maximum in the product-idempotent class is")
    print("  rank(P_Weyl)=1 and rank(P_Jordan)=1.")
    print()


def print_closure_status() -> None:
    print("Failure-closed status")
    print("-" * 78)
    rows = [
        ("rank-one local Fano kernel", "from incidence, after representative choice"),
        ("primitive Weyl factor", "derived by normalized rank penalty, conditional on product class"),
        ("primitive Jordan factor", "derived by normalized rank penalty, conditional on product class"),
        ("transition ray/vacuum representative", "not derived here"),
        ("trace space A_Weyl x J3(O)", "not derived here"),
        ("pi holonomy", "not derived here"),
        ("epsilon0^2 = pi/432", "conditional on the remaining open inputs"),
    ]
    for label, status in rows:
        print(f"  {label:34s} {status}")


def main() -> None:
    print_variational_derivation()
    print_rank_table()
    print_why_normalization_matters()
    print_product_factorization()
    print_closure_status()


if __name__ == "__main__":
    main()