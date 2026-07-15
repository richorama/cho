"""Boolean algebraic normal forms for elementary local rules."""

from __future__ import annotations

from typing import Iterable, Tuple


AnfCoefficients = Tuple[int, int, int, int, int, int, int, int]
LaurentTerms = Tuple[int, ...]


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


def _xor_laurent_terms(*terms: Iterable[int]) -> LaurentTerms:
    coefficients = set()
    for polynomial in terms:
        for exponent in polynomial:
            if exponent in coefficients:
                coefficients.remove(exponent)
            else:
                coefficients.add(exponent)
    return tuple(sorted(coefficients))


def _multiply_laurent_terms(
    left: LaurentTerms, right: LaurentTerms
) -> LaurentTerms:
    return _xor_laurent_terms(
        tuple(
            left_exponent + right_exponent
            for left_exponent in left
            for right_exponent in right
        )
    )


def affine_operator_terms(rule: int) -> LaurentTerms:
    """Return the nonzero shift exponents in an affine rule's linear operator."""
    coefficients = rule_to_anf(rule)
    if not is_affine_anf(coefficients):
        raise ValueError("affine operator requires an affine rule")

    return tuple(
        exponent
        for exponent, coefficient in (
            (-1, coefficients[4]),
            (0, coefficients[2]),
            (1, coefficients[1]),
        )
        if coefficient
    )


def sampled_affine_operator_terms(rule: int, temporal_stride: int) -> LaurentTerms:
    """Return P_m(A), where sampled trajectories obey P_0=0, P_1=A."""
    if temporal_stride < 1:
        raise ValueError("temporal_stride must be positive")
    operator = affine_operator_terms(rule)
    previous = ()
    current = operator
    for _ in range(1, temporal_stride):
        previous, current = current, _xor_laurent_terms(
            _multiply_laurent_terms(operator, current), previous
        )
    return current


def are_terms_block_aligned(terms: LaurentTerms, block_size: int) -> bool:
    """Return whether every Laurent shift descends to an integer coarse shift."""
    if block_size < 1:
        raise ValueError("block_size must be positive")
    return all(exponent % block_size == 0 for exponent in terms)


def affine_rules_align_at_matched_scale(scale: int) -> bool:
    """Return whether every affine ECA operator is block-aligned at this scale."""
    if scale < 2:
        raise ValueError("scale must be at least two")
    return all(
        are_terms_block_aligned(sampled_affine_operator_terms(rule, scale), scale)
        for rule in range(256)
        if is_affine_anf(rule_to_anf(rule))
    )


def dyadic_affine_effective_rules(
    rule: int, block_size: int
) -> Tuple[int, int]:
    """Return decimation and parity laws at a matched dyadic spacetime scale."""
    decimation = dyadic_affine_block_rule(
        rule, block_size, (1,) + (0,) * (block_size - 1)
    )
    parity = dyadic_affine_block_rule(rule, block_size, (1,) * block_size)
    return decimation, parity


def dyadic_affine_block_rule(
    rule: int, block_size: int, weights: Tuple[int, ...], offset: int = 0
) -> int:
    """Return the law induced by a nonconstant affine dyadic block functional."""
    if block_size < 2 or block_size & (block_size - 1):
        raise ValueError("block_size must be a power of two at least two")
    if len(weights) != block_size or any(weight not in (0, 1) for weight in weights):
        raise ValueError("weights must contain one binary value per block site")
    if not any(weights):
        raise ValueError("block functional must be nonconstant")
    if offset not in (0, 1):
        raise ValueError("offset must be binary")
    coefficients = rule_to_anf(rule)
    if not is_affine_anf(coefficients):
        raise ValueError("effective affine formula requires an affine rule")

    constant = coefficients[0]
    right = coefficients[1]
    center = coefficients[2]
    left = coefficients[4]
    coefficient_sum = left ^ center ^ right
    weight_parity = sum(weights) % 2
    effective_constant = coefficient_sum & (
        (constant & weight_parity) ^ offset
    )
    effective = (effective_constant, right, center, 0, left, 0, 0, 0)
    return anf_to_rule(effective)


def affine_effective_rules(rule: int) -> Tuple[int, int]:
    """Return the factor-two decimation and parity trajectory laws."""
    return dyadic_affine_effective_rules(rule, 2)