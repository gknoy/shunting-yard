"""
# test_shunting.py
"""

import pytest
from operator import add, mul  # , pow
from math import pi, sin

from entities import div, neg, Special, Operator as Op, Function as Fn, render_tokens
from shunting_yard import get_rpn_tokens, eval_rpn
from tokenizer import tokenize, enrich


# Formatting notes: test parametrization is sometimes hand-wrapped
# so that they take up less vertical space, rather than how ruff would do it.

# -------------
# Shunting Yard: Process tokens into RPN order
# -------------


@pytest.mark.skip  # shunting yard NYI
@pytest.mark.parametrize(
    "input, expected",
    [
        ([3, Op(add), 4], [3, 4, add]),
        (
            # "sin ( max ( 2, 3 ) ÷ 3 × π )",
            [
                sin, Special.PAREN_LEFT, max,
                Special.PAREN_LEFT, 2, 3, Special.PAREN_RIGHT,
                div, 3, mul, pi, Special.PAREN_RIGHT,
            ],
            # 2 3 max 3 ÷ π × sin
            [
                2, 3, Fn(max), 3, Op(div),
                pi, Op(mul), Fn(sin),
            ],
        ),
    ],
)  # fmt: skip
def test_get_rpn_tokens(input, expected):
    # TODO: This might be a LOT easier to read if we kept string inputs,
    #       and then used render to get string version of the tokens.
    assert expected == get_rpn_tokens(input)


@pytest.mark.skip  # shunting yard NYI
@pytest.mark.parametrize(
    "input, expected",
    [
        ("3 + 4", "3 4 +"),
        ("sin ( max ( 2, 3 ) ÷ 3 × π )", "2 3 max 3 ÷ π × sin"),
        # trololol. Let eval handle repeated calls to neg.
        ("-----5", "5 neg neg neg neg neg"),
        ("3--5", "3 5 neg -"),
    ],
)
def test_get_rendered_rpn_tokens(input, expected):
    input_tokens = enrich(tokenize(input))
    rpn_tokens = get_rpn_tokens(input_tokens)
    assert expected == render_tokens(rpn_tokens)


# -------------
# Evaluate RPN token stream so that we can have simpler test cases
# -------------


@pytest.mark.skip  # eval NYI
@pytest.mark.parametrize(
    "input, expected",
    [
        ([3, 4, Op(add)], 7),
        ([3, 4, Fn(neg), add], -1),
        (
            # "sin ( max ( 2, 3 ) ÷ 3 × π )"
            [
                2, 3, Fn(max), 3, Op(div),
                pi, Op(mul), Fn(sin),
            ],
            0,
        ),
    ],
)  # fmt: skip
def test_eval_rpn(input, expected):
    assert eval_rpn(input) == expected


# ==================
# test cases swiped from a friend
# ==================
# TODO: replace "x neg" with "-x" when we are processing tokens

# TEST_CASES = [
#     {"input": "-3 + -4", "expected": "-3 -4 +"},
#     {"input": "-3.5 + -4.25", "expected": "-3.5 -4.25 +"},
#     {"input": "6.0 - -2.5", "expected": "6.0 -2.5 -"},
#     {"input": "-1.2e3 + -3.4e-2", "expected": "-1.2e3 -3.4e-2 +"},
#     {"input": "-7 + -0.5", "expected": "-7 -0.5 +"},
#     {"input": "-2.5 * -1e-2", "expected": "-2.5 -1e-2 *"},
#     {"input": "(-3.5 + -4.5) * -2.0", "expected": "-3.5 -4.5 + -2.0 *"},
#     {"input": " -3+    -4", "expected": "-3 -4 +"},
#     {"input": "-3.5+  -4.25 ", "expected": "-3.5 -4.25 +"},
#     {"input": " 6.0 -    -2.5", "expected": "6.0 -2.5 -"},
#     {"input": "-1.2e3   + -3.4e-2", "expected": "-1.2e3 -3.4e-2 +"},
#     {"input": " -7+  -0.5 ", "expected": "-7 -0.5 +"},
#     {"input": "  -2.5   * -1e-2 ", "expected": "-2.5 -1e-2 *"},
#     {"input": "  (  -3.5+  -4.5  )* -2.0", "expected": "-3.5 -4.5 + -2.0 *"},
#     {"input": "2+3", "expected": "2 3 +"},
#     {"input": " 4  -1 ", "expected": "4 1 -"},
#     {"input": " 6*     7", "expected": "6 7 *"},
#     {"input": " 8 /2 ", "expected": "8 2 /"},
#     {"input": "2 + 3", "expected": "2 3 +"},
#     {"input": "4 - 1", "expected": "4 1 -"},
#     {"input": "6 * 7", "expected": "6 7 *"},
#     {"input": "8 / 2", "expected": "8 2 /"},
#     {"input": "2 + 3 * 4", "expected": "2 3 4 * +"},
#     {"input": "2 * 3 + 4", "expected": "2 3 * 4 +"},
#     {"input": "2 + 3 * 4 - 5", "expected": "2 3 4 * + 5 -"},
#     {"input": "(2 + 3) * 4", "expected": "2 3 + 4 *"},
#     {"input": "2 * (3 + 4)", "expected": "2 3 4 + *"},
#     {"input": "(2 + 3) * (4 - 1)", "expected": "2 3 + 4 1 - *"},
#     {"input": "5 - 3 - 2", "expected": "5 3 - 2 -"},
#     {"input": "4 / 2 / 2", "expected": "4 2 / 2 /"},
#     {"input": "x + y", "expected": "x y +"},
#     {"input": "x1 + _var2", "expected": "x1 _var2 +"},
#     {"input": "sin(x)", "expected": "x sin"},
#     {"input": "cos(x + y)", "expected": "x y + cos"},
#     {"input": "log(10)", "expected": "10 log"},
#     {"input": "sqrt(4 + 5)", "expected": "4 5 + sqrt"},
#     {"input": "2 ^ 3", "expected": "2 3 ^"},
#     {"input": "2 ^ 3 ^ 2", "expected": "2 3 2 ^ ^"},  # assumes right-associative
#     {"input": "3.14 * r ^ 2", "expected": "3.14 r 2 ^ *"},
#     {"input": "0.5 + .5", "expected": "0.5 0.5 +"},
#     {"input": "1.0e3 + 2.5E-2", "expected": "1.0e3 2.5E-2 +"},
#     {"input": "max(a, b + c)", "expected": "a b c + max"},
#     {"input": "pow(2, 10)", "expected": "2 10 pow"},
#     {"input": "2 * x + y / 3 ^ z", "expected": "2 x * y 3 z ^ / +"},
#     {"input": "((x))", "expected": "x"},
#     {"input": "(x + (y)) * z", "expected": "x y + z *"},
#     {"input": "", "expected": "ERR"},
#     {"input": "sin()", "expected": "ERR"},
#     {"input": "x + ", "expected": "ERR"},
#     {"input": "()", "expected": "ERR"},
#     {"input": "log(1, 2)", "expected": "ERR"},
#     {"input": "2 + * 3", "expected": "ERR"},
#     {"input": "sqrt(4 + 5", "expected": "ERR"},
#     {"input": "2 +", "expected": "ERR"},
#     {"input": "(2 + 3", "expected": "ERR"},
#     {"input": "2 + * 3", "expected": "ERR"},
# ]
