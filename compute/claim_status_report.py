"""
Claim-status report for the CHO theory-validation harness.

This is a reader-friendly view of `audit_contract.py`: it groups artifacts by
scientific status and prints the next proof or demotion pressure for each open
claim. It does not change any status; contracts and the derivation ledger remain
authoritative.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/claim_status_report.py
"""

from collections import defaultdict

import audit_contract


STATUS_ORDER = (
    audit_contract.STATUS_THEOREM,
    audit_contract.STATUS_DERIVED_BRIDGE,
    audit_contract.STATUS_OPEN_BRIDGE,
    audit_contract.STATUS_FUTURE_TEST,
    audit_contract.STATUS_LOCKED_REGISTRY,
    audit_contract.STATUS_DIAGNOSTIC,
    audit_contract.STATUS_EXPLORATORY,
    audit_contract.STATUS_OUT_OF_SCOPE,
)


def _next_step(contract):
    if contract.open_bridges:
        return contract.open_bridges[0]
    if contract.kill_conditions:
        return contract.kill_conditions[0]
    return contract.public_claim_policy


def grouped_contracts():
    grouped = defaultdict(list)
    for contract in audit_contract.CONTRACTS.values():
        grouped[contract.status].append(contract)
    for contracts in grouped.values():
        contracts.sort(key=lambda item: item.artifact)
    return grouped


def main():
    grouped = grouped_contracts()
    print("CHO CLAIM STATUS REPORT")
    print("=" * 78)
    print(f"total contracted artifacts: {len(audit_contract.CONTRACTS)}")
    print()
    for status in STATUS_ORDER:
        contracts = grouped.get(status, [])
        if not contracts:
            continue
        print(f"{status.upper()} ({len(contracts)})")
        print("-" * 78)
        for contract in contracts:
            ledger = ",".join(contract.ledger_ids)
            print(f"{contract.artifact:<34} {contract.verdict:<11} {ledger}")
            print(f"    next: {_next_step(contract)}")
        print()


if __name__ == "__main__":
    main()