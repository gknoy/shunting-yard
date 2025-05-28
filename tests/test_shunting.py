"""
# test_shunting.py
"""

import pytest

from operator import add, mul  # , pow
from math import pi, sin

from functions import div
from tokenizer import tokenize, enrich, Paren
from shunting_yard import get_rpn_tokens, eval_rpn


@pytest.mark.parametrize(
    "input, expected",
    [
        ("3+4", [3, 4, add]),
        (
            "sin ( max ( 2, 3 ) ÷ 3 × π )",
            [
                sin, Paren.LEFT, max, Paren.LEFT, 2, 3, Paren.RIGHT,
                div, 3, mul, pi, Paren.RIGHT,
            ],
        ),
    ],
)  # fmt: skip
def test_get_rpn_tokens(input, expected):
    assert get_rpn_tokens(enrich(tokenize(input))) == expected


# -------------
# Evaluate RPN token stream so that we can have simpler test cases
# -------------


@pytest.mark.skip  # FIXME: actually unskip this once implemented ;)
@pytest.mark.parametrize(
    "input, expected",
    [
        ([3, 4, add], 7),
        (
            # "sin ( max ( 2, 3 ) ÷ 3 × π )"
            [
                sin, Paren.LEFT, max, Paren.LEFT, 2, 3, Paren.RIGHT,
                div, 3, mul, pi, Paren.RIGHT,
            ],
            0,
        ),
    ],
)  # fmt: skip
def test_eval_rpn(input, expected):
    assert eval_rpn(input) == expected
