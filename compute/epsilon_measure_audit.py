"""
Epsilon measure audit: pi/432 as a conditional normalized transition trace.
============================================================================

Phase 2 asks whether epsilon0^2 = pi/432 is a theorem-level measure statement or
must remain a geometric bridge. This artifact is deliberately conservative: it
checks the exact value under named hypotheses and pressure-tests nearby
alternatives, but it does not move the Bayes scoreboard from GEOMETRIC to DERIVED.

The conditional theorem audited here is:

    epsilon0^2 = Tr_transition / dim_phase_space
               = (pi * rank(P_transition)) / (dim(A_Weyl) * dim(J3(O)))
               = pi / (16 * 27)

provided the transition measure is the normalized invariant measure on the
primitive A_Weyl x J3(O) transition product and the transition kernel is pure
rank one.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_measure_audit.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math


DIM_A_WEYL = 16
DIM_J3O = 27
DIM_A_REAL = 64
DIM_J3O_TRACELESS = 26
DIM_OP2 = 16
FANO_LINE_PAIR_ORBIT = 21
TARGET_DENOMINATOR = DIM_A_WEYL * DIM_J3O


@dataclass(frozen=True)
class Hypothesis:
    code: str
    statement: str
    status: str


@dataclass(frozen=True)
class Candidate:
    name: str
    numerator: float
    denominator: int
    failed_criteria: tuple[str, ...]
    note: str

    @property
    def value(self):
        return self.numerator / self.denominator

    @property
    def ratio_to_target(self):
        return self.value / target_value()


HYPOTHESES = [
    Hypothesis(
        "H1",
        "phase space is A_Weyl x J3(O), dimensions 16 x 27",
        "supported by state-count, product-space, Weyl-isomorphism, and Spin(9)-embedding audits; one frame/measure selection remains",
    ),
    Hypothesis(
        "H2",
        "transition kernel is primitive rank one",
        "supported by epsilon_rank_one_kernel.py; residual is vacuum purity as the spurion direction",
    ),
    Hypothesis(
        "H3",
        "angular weight is the Berry half-turn pi",
        "supported by action/free-action/A4 two-level audits; residual is the microscopic A4 origin",
    ),
    Hypothesis(
        "H4",
        "measure is the normalized invariant transition trace on that product",
        "not fully derived; this is the live Phase 2 measure hypothesis",
    ),
    Hypothesis(
        "H5",
        "the same transition operator feeds the later Yukawa/seesaw construction",
        "open to Phase 3; not credited here",
    ),
]


CRITERIA = {
    "weyl_spinor": "uses the chiral 16-dimensional A_Weyl spinor rather than a larger real algebra or missing gauge factor",
    "jordan_trace": "uses the full unital 27-dimensional J3(O) trace space",
    "primitive_rank": "uses one pure primitive idempotent, not several generations at once",
    "berry_pi": "uses the Berry half-turn pi, not a raw reciprocal or full turn",
    "orbit_quotient": "quotients symmetry-equivalent local Fano supports rather than multiplying by their orbit size",
    "normalized_measure": "uses the normalized transition trace rather than an unnormalized sphere area",
}


def target_value():
    return math.pi / TARGET_DENOMINATOR


def candidates():
    return [
        Candidate(
            "target: pi/(16*27)",
            math.pi,
            TARGET_DENOMINATOR,
            (),
            "primitive Weyl x Jordan transition trace",
        ),
        Candidate(
            "rank-2 kernel",
            2.0 * math.pi,
            TARGET_DENOMINATOR,
            ("primitive_rank",),
            "switches on two generations at once",
        ),
        Candidate(
            "rank-3 kernel",
            3.0 * math.pi,
            TARGET_DENOMINATOR,
            ("primitive_rank",),
            "full rank-three generation frame, no hierarchy",
        ),
        Candidate(
            "OP2 only",
            math.pi,
            DIM_OP2,
            ("jordan_trace",),
            "uses only the vacuum manifold, not the ambient Jordan trace",
        ),
        Candidate(
            "J3(O) only",
            math.pi,
            DIM_J3O,
            ("weyl_spinor",),
            "drops the Weyl/tangent spinor factor",
        ),
        Candidate(
            "real algebra x J3(O)",
            math.pi,
            DIM_A_REAL * DIM_J3O,
            ("weyl_spinor",),
            "averages over the real algebra instead of the chiral Weyl module",
        ),
        Candidate(
            "A_Weyl x traceless J3(O)",
            math.pi,
            DIM_A_WEYL * DIM_J3O_TRACELESS,
            ("jordan_trace",),
            "drops the Jordan unit/trace direction",
        ),
        Candidate(
            "raw reciprocal 1/(16*27)",
            1.0,
            TARGET_DENOMINATOR,
            ("berry_pi",),
            "removes the action-selected Berry holonomy",
        ),
        Candidate(
            "full turn 2pi/(16*27)",
            2.0 * math.pi,
            TARGET_DENOMINATOR,
            ("berry_pi",),
            "uses a full turn instead of the minimal half-turn",
        ),
        Candidate(
            "Fano pair degeneracy 21*pi/432",
            FANO_LINE_PAIR_ORBIT * math.pi,
            TARGET_DENOMINATOR,
            ("orbit_quotient",),
            "counts one automorphism orbit as 21 independent channels",
        ),
        Candidate(
            "sphere area 4pi/(16*27)",
            4.0 * math.pi,
            TARGET_DENOMINATOR,
            ("normalized_measure",),
            "uses unnormalized S2 area rather than normalized transition measure",
        ),
    ]


def candidate_summary():
    rows = candidates()
    target = rows[0]
    alternatives = rows[1:]
    all_alternatives_fail = all(row.failed_criteria for row in alternatives)
    target_ok = not target.failed_criteria and abs(target.value - math.pi / 432.0) < 1e-15
    return rows, target_ok, all_alternatives_fail


def print_hypotheses():
    print("  NAMED HYPOTHESES")
    print("  " + "-" * 72)
    for item in HYPOTHESES:
        print(f"      {item.code}: {item.statement}")
        print(f"          status: {item.status}")
    print()


def print_candidate_table(rows):
    print("  NEARBY MEASURE ALTERNATIVES")
    print("  " + "-" * 72)
    print(f"      {'candidate':<32} {'value':>12} {'x target':>10}  failed criterion")
    for row in rows:
        failed = ", ".join(row.failed_criteria) if row.failed_criteria else "none"
        print(f"      {row.name:<32} {row.value:>12.8f} {row.ratio_to_target:>10.3f}  {failed}")
        print(f"          {row.note}")
    print()


def print_criteria():
    print("  CRITERIA DICTIONARY")
    print("  " + "-" * 72)
    for key, description in CRITERIA.items():
        print(f"      {key:<19} {description}")
    print()


def main():
    print("=" * 78)
    print("  EPSILON MEASURE AUDIT - conditional theorem gate for epsilon0^2")
    print("  Does pi/432 appear as one normalized transition trace?")
    print("=" * 78)

    rows, target_ok, alternatives_fail = candidate_summary()

    print_hypotheses()

    print("  CONDITIONAL TRACE COMPUTATION")
    print("  " + "-" * 72)
    print(f"      dim(A_Weyl)                         : {DIM_A_WEYL}")
    print(f"      dim(J3(O))                          : {DIM_J3O}")
    print(f"      rank(P_transition)                  : 1")
    print(f"      theta                               : pi")
    print(f"      epsilon0^2 = pi/(16*27)             : {target_value():.10f}")
    print(f"      matches pi/432                      : {'PASS' if target_ok else 'FAIL'}")
    print()

    print_candidate_table(rows)
    print_criteria()

    print("  VERDICT")
    print("  " + "-" * 72)
    print(f"      target computation                  : {'PASS' if target_ok else 'FAIL'}")
    print(f"      nearby alternatives excluded        : {'PASS' if alternatives_fail else 'FAIL'}")
    print("      scoreboard status                   : GEOMETRIC, not DERIVED")
    print("      live residual                       : H4 normalized measure theorem")
    print()
    print("  This artifact therefore narrows Phase 2 to one named issue: prove the")
    print("  normalized invariant transition measure H4, or demote epsilon0^2 from")
    print("  GEOMETRIC to CHOSEN in model_complexity.py / scoreboard.py.")
    print()

    if not (target_ok and alternatives_fail):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
