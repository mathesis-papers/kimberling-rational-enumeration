import argparse
from fractions import Fraction
from functools import lru_cache
from math import gcd
import json
from pathlib import Path


def next_generation(prefix):
    seen = set(prefix)
    fresh = []
    for outer in prefix:
        for inner in prefix:
            value = outer / (1 + inner)
            if value not in seen:
                seen.add(value)
                fresh.append(value)
    return prefix + fresh


def literal_update(prefix):
    pairs = [outer / (1 + inner) for outer in prefix for inner in prefix]
    return list(dict.fromkeys(prefix + pairs))


@lru_cache(maxsize=8192)
def descent(numerator, denominator):
    assert 1 <= numerator <= denominator
    if numerator == denominator:
        return ()
    if 2 * numerator <= denominator:
        parent = (numerator, denominator - numerator)
        operation = 'L'
    else:
        parent = (denominator - numerator, numerator)
        operation = 'R'
    assert 1 <= parent[0] <= parent[1] < denominator
    return descent(*parent) + (operation,)


def evaluate(word):
    value = Fraction(1)
    for operation in word:
        value = value / (1 + value) if operation == 'L' else 1 / (1 + value)
    return value


@lru_cache(maxsize=8192)
def positive_word(numerator, denominator, constant):
    value = Fraction(numerator, denominator)
    numerator, denominator = value.numerator, value.denominator
    if denominator == 1:
        return ('T',) * (numerator - 1)
    if numerator < denominator:
        parent = Fraction(constant * denominator, numerator)
        assert parent.denominator < denominator
        return positive_word(parent.numerator, parent.denominator, constant) + ('C',)
    quotient, remainder = divmod(numerator, denominator)
    return positive_word(remainder, denominator, constant) + ('T',) * quotient


def evaluate_positive(word, constant):
    value = Fraction(1)
    for operation in word:
        value = value + 1 if operation == 'T' else constant / value
    return value


def continued_fraction_digit_sum(value):
    numerator, denominator = value.numerator, value.denominator
    digits = []
    while denominator:
        quotient, remainder = divmod(numerator, denominator)
        digits.append(quotient)
        numerator, denominator = denominator, remainder
    assert digits[0] == 0 and digits[-1] >= 2
    return sum(digits[1:])


def check():
    prefix = [Fraction(1)]
    prefixes = [prefix]
    for generation in range(2, 7):
        advanced = next_generation(prefix)
        assert advanced[:len(prefix)] == prefix
        assert len(advanced) == len(set(advanced))
        assert all(0 < value <= 1 for value in advanced)
        assert len(advanced) > len(prefix)
        if generation <= 5:
            assert advanced == literal_update(prefix)
        prefixes.append(advanced)
        prefix = advanced
    sizes = [len(values) for values in prefixes]
    assert sizes == [1, 2, 5, 20, 245, 38179]
    minima = []
    first_generation = {}
    for generation, values in enumerate(prefixes, start=1):
        minimum = min(values)
        assert minimum == Fraction(1, 2 ** (generation - 1))
        minima.append(str(minimum))
        for value in values:
            first_generation.setdefault(value, generation)
            assert value >= minimum
    for exponent in range(6):
        assert first_generation[Fraction(1, 2 ** exponent)] == exponent + 1
    digit_sum_bounds = 0
    for value, generation in first_generation.items():
        if value < 1:
            assert generation <= continued_fraction_digit_sum(value)
            digit_sum_bounds += 1
    membership_pairs = 0
    for denominator, values in enumerate(prefixes, start=1):
        for numerator in range(1, denominator + 1):
            assert Fraction(numerator, denominator) in values
            membership_pairs += 1
    unary_identity_pairs = 0
    unary_closure_witnesses = 0
    reciprocal_closure_witnesses = 0
    for denominator in range(1, 41):
        for numerator in range(1, 41):
            value = Fraction(numerator, denominator)
            assert 1 / (1 / (1 + value)) == value + 1
            for constant in range(1, 5):
                assert constant / (constant / value) == value
                unary_identity_pairs += 1
                word = positive_word(numerator, denominator, constant)
                assert evaluate_positive(word, constant) == value
                unary_closure_witnesses += 1
                if constant == 1:
                    reconstructed = Fraction(1)
                    for operation in word:
                        if operation == 'T':
                            reconstructed = 1 / (1 + reconstructed)
                            reconstructed = 1 / reconstructed
                        else:
                            reconstructed = 1 / reconstructed
                    assert reconstructed == value
                    reciprocal_closure_witnesses += 1
    expected_numerators = [1, 1, 2, 1, 1, 3, 4, 3, 3, 2, 3, 4, 8, 1, 1, 3, 1, 3, 2, 4]
    expected_denominators = [1, 2, 3, 4, 3, 5, 5, 4, 10, 5, 8, 9, 15, 8, 6, 20, 5, 16, 9, 15]
    assert [value.numerator for value in prefixes[3]] == expected_numerators
    assert [value.denominator for value in prefixes[3]] == expected_denominators
    tested = 0
    reduced = 0
    for denominator in range(1, 401):
        for numerator in range(1, denominator + 1):
            word = descent(numerator, denominator)
            assert len(word) <= denominator - 1
            assert evaluate(word) == Fraction(numerator, denominator)
            tested += 1
            reduced += gcd(numerator, denominator) == 1
    positions = {value: index for index, value in enumerate(prefix, start=1)}
    rows = [[1]]
    for denominator in range(2, 8):
        rows.append([positions[Fraction(numerator, denominator)]
                     for numerator in range(1, denominator)])
    expected_rows = [[1], [2], [5, 3], [4, 2, 8], [17, 10, 6, 7],
                     [15, 5, 2, 3, 32], [63, 38, 44, 23, 25, 30]]
    assert rows == expected_rows
    occurrences = {}
    for denominator in range(2, 41):
        for numerator in range(1, denominator):
            value = Fraction(numerator, denominator)
            if value in positions:
                position = positions[value]
                occurrences.setdefault(position, []).append((denominator, numerator))
    tested_positions = []
    for position, value in enumerate(prefix, start=1):
        if position >= 2 and value.denominator <= 40:
            expected = [(multiple * value.denominator, multiple * value.numerator)
                        for multiple in range(1, 40 // value.denominator + 1)]
            assert occurrences[position] == expected
            tested_positions.append(position)
    assert 1 not in occurrences
    assert occurrences[2] == [(denominator, denominator // 2) for denominator in range(2, 41, 2)]
    return {
        'arithmetic': 'exact fractions.Fraction; arbitrary-precision integers; no rounding',
        'cumulative_sizes_U1_through_U6': sizes,
        'cumulative_minima_U1_through_U6': minima,
        'dyadic_first_generations_exponents_0_through_5': list(range(1, 7)),
        'continued_fraction_generation_bounds_checked_U6': digit_sum_bounds,
        'denominator_bound_membership_pairs_through_q6': membership_pairs,
        'unary_identity_checks_p_q_1_through_40_c_1_through_4': unary_identity_pairs,
        'unary_closure_witnesses_p_q_1_through_40_c_1_through_4': unary_closure_witnesses,
        'reciprocal_shift_closure_witnesses_p_q_1_through_40': reciprocal_closure_witnesses,
        'literal_order_comparison': 'all entries of U2 through U5',
        'coordinate_comparison': 'all 20 numerators and denominators of U4 in A371279/A371280',
        'descent_denominator_range': [1, 400],
        'descent_displayed_pairs_checked': tested,
        'descent_reduced_pairs_checked': reduced,
        'descent_checks': 'strict denominator decrease, exact reconstruction, word length at most q-1',
        'position_rows_H1_through_H7': rows,
        'multiplicity_row_range': [2, 40],
        'multiplicity_positions_checked': len(tested_positions),
        'multiplicity_domain': 'every position in U6 with reduced denominator at most 40',
        'position_2_occurrence_rows': [entry[0] for entry in occurrences[2]],
        'P_2_over_5': positions[Fraction(2, 5)],
        'result': 'all assertions passed',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    result = json.dumps(check(), indent=2, sort_keys=True) + '\n'
    if arguments.output:
        arguments.output.write_text(result)
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
