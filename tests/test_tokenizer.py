"""
# tests of the tokenizer and enrichment tooling
"""

import pytest
import math

from operator import add, sub, mul, pow, abs

from entities import div, Special, Operator, Function
from tokenizer import tokenize, enrich


@pytest.mark.parametrize(
    "input, expected",
    [
        ("3+-4", ["3", "+", "-4"]),
        ("302 + sin(-400)", ["302", "+", "sin", "(", "-400", ")"]),
    ],
)
def test_tokenize(input, expected):
    assert list(tokenize(input)) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        (["abs"], [Function(abs)]),
        (["+"], [Operator(add)]),
        (["-"], [Operator(sub)]),
        (["*"], [Operator(mul)]),
        (["/"], [Operator(div)]),
        (["^"], [Operator(pow, associativity="right")]),
        (["3", "+", "4"], [3, Operator(add), 4]),
        (["(", ",", ")"], [Special.PAREN_LEFT, Special.COMMA, Special.PAREN_RIGHT]),
        (
            ["302", "+", "sqrt", "(", "400", ")"],
            [
                302,
                Operator(add),
                Function(math.sqrt),
                Special.PAREN_LEFT,
                400,
                Special.PAREN_RIGHT,
            ],
        ),
        # numeric stuff
        (["123456", "pi", "π", "2.12"], [123456, math.pi, math.pi, 2.12]),
    ],
)
def test_enrich(input, expected):
    enriched = list(enrich(input))
    assert enriched == expected
