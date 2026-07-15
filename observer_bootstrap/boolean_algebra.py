"""Boolean algebraic normal forms for elementary local rules."""

from __future__ import annotations

from typing import Tuple


AnfCoefficients = Tuple[int, int, int, int, int, int, int, int]


def rule_to_anf(rule: int) -> AnfCoefficients:
    """Return coefficients indexed by monomial masks over (right, center, left)."""
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA rule")
    coefficients = [(rule >> mask) & 1 for mask in range(8)]
    for variable in (1, 2, 4):
        for mask in range(8):
            if mask & variable:
                coefficients[mask] ^= coefficients[mask ^ variable]
    return tuple(coefficients)


def anf_to_rule(coefficients: AnfCoefficients) -> int:
    if len(coefficients) != 8 or any(value not in (0, 1) for value in coefficients):
        raise ValueError("ANF requires eight binary coefficients")
    rule = 0
    for inputs in range(8):
        output = 0
        monomial = inputs
        while True:
            output ^= coefficients[monomial]
            if monomial == 0:
                break
            monomial = (monomial - 1) & inputs
        rule |= output << inputs
    return rule


def is_affine_anf(coefficients: AnfCoefficients) -> bool:
    return all(
        coefficient == 0
        for mask, coefficient in enumerate(coefficients)
        if bin(mask).count("1") >= 2
    )


def affine_effective_rules(rule: int) -> Tuple[int, int]:
    """Return decimation and parity trajectory laws for an affine rule."""
    coefficients = rule_to_anf(rule)
    if not is_affine_anf(coefficients):
        raise ValueError("effective affine formula requires an affine rule")

    constant = coefficients[0]
    right = coefficients[1]
    center = coefficients[2]
    left = coefficients[4]
    decimation_constant = constant & (left ^ center ^ right)
    decimation = (decimation_constant, right, center, 0, left, 0, 0, 0)
    parity = (0, right, center, 0, left, 0, 0, 0)
    return anf_to_rule(decimation), anf_to_rule(parity)