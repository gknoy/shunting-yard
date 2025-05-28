"""
# tests of the tokenizer and enrichment tooling
"""

import pytest
import math
import operator

from functions import div
from tokenizer import tokenize, enrich, Special


@pytest.mark.parametrize(
    "input, expected",
    [
        ("3+4", ["3", "+", "4"]),
        ("302 + sin(400)", ["302", "+", "sin", "(", "400", ")"]),
    ],
)
def test_tokenize(input, expected):
    assert list(tokenize(input)) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        (["abs"], [operator.abs]),
        (["+"], [operator.add]),
        (["-"], [operator.sub]),
        (["*"], [operator.mul]),
        (["/"], [div]),
        (["^"], [operator.pow]),
        (["3", "+", "4"], [3, operator.add, 4]),
        (["(", ",", ")"], [Special.PAREN_LEFT, Special.COMMA, Special.PAREN_RIGHT]),
        (
            ["302", "+", "sqrt", "(", "400", ")"],
            [302, operator.add, math.sqrt, Special.PAREN_LEFT, 400, Special.PAREN_RIGHT],
        ),
        # numeric stuff
        (["123456", "pi", "π", "2.12"], [123456, math.pi, math.pi, 2.12]),
    ],
)
def test_enrich(input, expected):
    assert list(enrich(input)) == expected
