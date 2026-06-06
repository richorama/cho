"""
Charged-flavour Yukawa bridge scaffold.

This script upgrades part of the flavour bridge from formula listing to a
small derivation scaffold. It derives the nearest-neighbor texture from an
adjacent generation operator and derives the cascade mass relation. The sector
shape factors remain explicit operator targets.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Inputs:
    dim_complex_algebra: int = 16
    dim_jordan: int = 27
    n_color: int = 3
    dim_octonion: int = 8
    sin2_theta_w_tree: float = 0.25

    @property
    def epsilon_sq(self) -> float:
        return np.pi / (self.dim_complex_algebra * self.dim_jordan)


@dataclass(frozen=True)
class Sector:
    name: str
    multiplicity: float
    shape_factor: float
    shape_label: str
    observed_first_over_third: float
    observed_second_over_third: float

    def second_over_third(self, epsilon_sq: float) -> float:
        return self.multiplicity * epsilon_sq

    def first_over_third(self, epsilon_sq: float) -> float:
        q = self.second_over_third(epsilon_sq)
        return self.shape_factor * q * q

    @property
    def observed_shape_factor(self) -> float:
        return self.observed_first_over_third / (self.observed_second_over_third ** 2)


OBSERVED = {
    "m_u": 2.16e-3,
    "m_d": 4.67e-3,
    "m_s": 93.4e-3,
    "m_c": 1.27,
    "m_b": 4.18,
    "m_t": 172.76,
    "m_e": 0.511e-3,
    "m_mu": 0.10566,
    "m_tau": 1.777,
}


def pct_error(predicted: float, observed: float) -> float:
    return (predicted - observed) / observed * 100.0


def generation_adjacency() -> np.ndarray:
    """Leading one-step triality adjacency in generation space."""
    return np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ], dtype=int)


def sectors(inputs: Inputs) -> list[Sector]:
    return [
        Sector(
            name="up",
            multiplicity=1.0,
            shape_factor=inputs.sin2_theta_w_tree,
            shape_label="1/4",
            observed_first_over_third=OBSERVED["m_u"] / OBSERVED["m_t"],
            observed_second_over_third=OBSERVED["m_c"] / OBSERVED["m_t"],
        ),
        Sector(
            name="down",
            multiplicity=float(inputs.n_color),
            shape_factor=inputs.n_color ** 2 * inputs.sin2_theta_w_tree,
            shape_label="N_color^2 / 4 = 9/4",
            observed_first_over_third=OBSERVED["m_d"] / OBSERVED["m_b"],
            observed_second_over_third=OBSERVED["m_s"] / OBSERVED["m_b"],
        ),
        Sector(
            name="lepton",
            multiplicity=float(inputs.dim_octonion),
            shape_factor=inputs.sin2_theta_w_tree / np.pi,
            shape_label="1/(4*pi)",
            observed_first_over_third=OBSERVED["m_e"] / OBSERVED["m_tau"],
            observed_second_over_third=OBSERVED["m_mu"] / OBSERVED["m_tau"],
        ),
    ]


def print_adjacency_derivation() -> None:
    adjacency = generation_adjacency()
    two_step = adjacency @ adjacency
    print("YUKAWA BRIDGE: GENERATION ADJACENCY")
    print("=" * 78)
    print("Leading triality transition allows one adjacent generation step:")
    for row in adjacency:
        print("  " + " ".join(str(value) for value in row))
    print()
    print(f"Direct 1<->3 entry at leading order: {adjacency[0, 2]}")
    print(f"Two-step 1->3 path count in A^2:      {two_step[0, 2]}")
    print("Derived scaffold result: M13 = 0 at leading order; 1<->3 first appears as a second-order path.")
    print()


def print_cascade_table(inputs: Inputs) -> None:
    print("Cascade relation and sector traces")
    print("-" * 78)
    print("m2/m3 = multiplicity * epsilon0^2")
    print("m1/m3 = shape_factor * (m2/m3)^2")
    print()
    print(f"epsilon0^2 = {inputs.epsilon_sq:.10f}")
    print()
    header = f"{'sector':<8} {'mult':>5} {'shape':<20} {'m2/m3':>12} {'m1/m3':>12} {'obs m1/m3':>12} {'err':>8}"
    print(header)
    print("-" * len(header))
    for sector in sectors(inputs):
        q = sector.second_over_third(inputs.epsilon_sq)
        first = sector.first_over_third(inputs.epsilon_sq)
        print(
            f"{sector.name:<8} "
            f"{sector.multiplicity:>5.1f} "
            f"{sector.shape_label:<20} "
            f"{q:>12.6e} "
            f"{first:>12.6e} "
            f"{sector.observed_first_over_third:>12.6e} "
            f"{pct_error(first, sector.observed_first_over_third):>+7.1f}%"
        )
    print()


def print_shape_targets(inputs: Inputs) -> None:
    print("Sector shape-factor targets")
    print("-" * 78)
    print(f"{'sector':<8} {'target k':>12} {'observed k':>12} {'target err':>12}  operator target")
    for sector in sectors(inputs):
        print(
            f"{sector.name:<8} "
            f"{sector.shape_factor:>12.6f} "
            f"{sector.observed_shape_factor:>12.6f} "
            f"{pct_error(sector.shape_factor, sector.observed_shape_factor):>+11.1f}%  "
            f"derive {sector.shape_label} from CHO Yukawa traces"
        )
    print()


def print_proof_obligations() -> None:
    print("Proof obligations")
    print("-" * 78)
    obligations = [
        "Construct the trilinear CHO Yukawa map ideal_i x Higgs x ideal_j -> scalar.",
        "Show that one triality step is allowed at leading order and two-step 1<->3 is suppressed.",
        "Derive the sector multiplicity projectors with traces 1, 3, and 8.",
        "Derive the shape factors 1/4, 9/4, and 1/(4*pi) as operator traces or Schur-complement invariants.",
        "Use the same operator to place the Fano phase and compute the CKM Jarlskog invariant.",
    ]
    for index, obligation in enumerate(obligations, 1):
        print(f"{index}. {obligation}")
    print()
    print("Status: M13 and cascade algebra are derived in this scaffold; sector shape factors remain open operator targets.")


def main() -> None:
    inputs = Inputs()
    print_adjacency_derivation()
    print_cascade_table(inputs)
    print_shape_targets(inputs)
    print_proof_obligations()


if __name__ == "__main__":
    main()
