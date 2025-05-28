"""
# tests of the tokenizer and enrichment tooling
"""

import pytest
import math
import operator

from functions import div
from tokenizer import tokenize, enrich, Paren


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
        (
            ["302", "+", "sqrt", "(", "400", ")"],
            [302, operator.add, math.sqrt, Paren.LEFT, 400, Paren.RIGHT],
        ),
    ],
)
def test_enrich(input, expected):
    assert list(enrich(input)) == expected
