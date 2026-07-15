"""Export or independently verify the affine-classification certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, Tuple

from observer_bootstrap.boolean_algebra import is_affine_anf, rule_to_anf
from observer_bootstrap.reversible_dynamics import trajectory_conflict_certificate


ARTIFACT_PATH = Path(__file__).resolve().parent / "affine_conflict_certificates.json"


def direct_step(rule: int, configuration: Tuple[Tuple[int, int], ...]):
    size = len(configuration)
    current = tuple(cell[0] for cell in configuration)
    return tuple(
        (
            ((rule >> (
                4 * current[(index - 1) % size]
                + 2 * current[index]
                + current[(index + 1) % size]
            )) & 1) ^ configuration[index][1],
            current[index],
        )
        for index in range(size)
    )


def direct_observation(rule: int, configuration, coarse_site: int):
    configuration = tuple(tuple(cell) for cell in configuration)
    previous = tuple(configuration[index][0] for index in range(0, 6, 2))
    current_configuration = direct_step(rule, direct_step(rule, configuration))
    current = tuple(current_configuration[index][0] for index in range(0, 6, 2))
    next_configuration = direct_step(
        rule, direct_step(rule, current_configuration)
    )
    next_values = tuple(next_configuration[index][0] for index in range(0, 6, 2))
    coarse_input = (
        previous[coarse_site],
        current[(coarse_site - 1) % 3],
        current[coarse_site],
        current[(coarse_site + 1) % 3],
    )
    return coarse_input, next_values[coarse_site] ^ previous[coarse_site]


def certificate_payload() -> Dict[str, object]:
    certificates = []
    for rule in range(256):
        if is_affine_anf(rule_to_anf(rule)):
            continue
        certificate = trajectory_conflict_certificate(rule)
        if certificate is None:
            raise RuntimeError("missing certificate for rule {}".format(rule))
        certificates.append(
            {
                "rule": certificate.rule,
                "blocking": certificate.blocking_name,
                "first": certificate.first,
                "first_coarse_site": certificate.first_coarse_site,
                "second": certificate.second,
                "second_coarse_site": certificate.second_coarse_site,
            }
        )
    return {
        "schema": "observer-bootstrap.affine-conflicts.v1",
        "source_size": 6,
        "temporal_stride": 2,
        "coarse_rule_class": "reversible-radius-one",
        "certificates": certificates,
    }


def canonical_json(payload: Dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def verify_payload(payload: Dict[str, object]) -> None:
    if payload.get("schema") != "observer-bootstrap.affine-conflicts.v1":
        raise ValueError("unsupported certificate schema")
    if payload.get("source_size") != 6:
        raise ValueError("certificate source size must be six")
    if payload.get("temporal_stride") != 2:
        raise ValueError("certificate temporal stride must be two")
    if payload.get("coarse_rule_class") != "reversible-radius-one":
        raise ValueError("unsupported coarse rule class")
    certificates = payload.get("certificates")
    if not isinstance(certificates, list) or len(certificates) != 240:
        raise ValueError("artifact must contain 240 certificates")
    rules = []
    for certificate in certificates:
        rule = certificate["rule"]
        if certificate["blocking"] != "decimation":
            raise ValueError("certificate must use decimation")
        first = direct_observation(
            rule, certificate["first"], certificate["first_coarse_site"]
        )
        second = direct_observation(
            rule, certificate["second"], certificate["second_coarse_site"]
        )
        if first[0] != second[0] or first[1] == second[1]:
            raise ValueError("invalid conflict for rule {}".format(rule))
        rules.append(rule)
    expected = [
        rule for rule in range(256) if not is_affine_anf(rule_to_anf(rule))
    ]
    if rules != expected:
        raise ValueError("certificate rules do not match all non-affine rules")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        payload = json.loads(ARTIFACT_PATH.read_text(encoding="ascii"))
        verify_payload(payload)
    else:
        payload = certificate_payload()
        verify_payload(payload)
        ARTIFACT_PATH.write_text(canonical_json(payload), encoding="ascii")
    digest = hashlib.sha256(ARTIFACT_PATH.read_bytes()).hexdigest()
    print("{}  {}".format(digest, ARTIFACT_PATH.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())