"""
# tests of the tokenizer and enrichment tooling
"""

import pytest
from math import pi, sqrt
from operator import add, mul, pow, abs

from entities import div, Special, Operator as Op, Function as Fn, neg, subtract
from tokenizer import tokenize, enrich


@pytest.mark.parametrize(
    "input, expected",
    [
        ("3+-4", ["3", "+", "-", "4"]),
        ("3e2 + sin(-400)", ["3e2", "+", "sin", "(", "-", "400", ")"]),
        # verify we can differentiate minus (subtraction) from unary minus (negation)
        # ("---5", ["-", "-", "-", "5"]),
        ("---5", ["-", "-", "-", "5"]),
        ("3--5", ["3", "-", "-", "5"]),
    ],
)
def test_tokenize(input, expected):
    """
    tokenize(str) should give an iterable of strings.
    Multiple minus signs are NOT collapsed or
    otherwise changed to negative numbers.
    """
    assert expected == list(tokenize(input))


@pytest.mark.parametrize(
    "input,expected",
    [
        (["abs"], [Fn(abs, arity=1)]),
        (["+"], [Op(add)]),
        (["*"], [Op(mul)]),
        (["/"], [Op(div)]),
        (["^"], [Op(pow, associativity="right")]),
        (["3", "+", "4"], [3, Op(add), 4]),
        (["(", ",", ")"], [Special.PAREN_LEFT, Special.COMMA, Special.PAREN_RIGHT]),
        (
            ["302", "+", "sqrt", "(", "400", ")"],
            [
                302,
                Op(add),
                Fn(sqrt, arity=1),
                Special.PAREN_LEFT,
                400,
                Special.PAREN_RIGHT,
            ],
        ),
        # numeric stuff
        (["123456", "pi", "π", "2.12"], [123456, pi, pi, 2.12]),
    ],
)
def test_enrich(input, expected):
    enriched = list(enrich(input))
    assert expected == enriched


@pytest.mark.parametrize(
    "input,expected",
    [
        # a - b yields sutraction
        (["3", "-", "4"], [3, subtract, 4]),
        # leading - means negation
        (["-", "5"], [neg, 5]),
        # odd neg counts get left as is because we are
        # heathens who don't care about efficiency ;D
        (["-", "-", "-", "5"], [neg, neg, neg, 5]),
        # evens do not cancel out because we'll do the math during eval
        (["-", "-", "5"], [neg, neg, 5]),
    ],
)
def test_enrich_negation(input, expected):
    enriched = list(enrich(input))
    assert expected == enriched
