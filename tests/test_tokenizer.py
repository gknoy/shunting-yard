"""
# tests of the tokenizer and enrichment tooling
"""

import pytest

from tokenizer import tokenize, enrich
# from tokenizer import classify_char


# @pytest.mark.parametrize(
#     "char,expected",
#     [
#         (")", "paren"),
#         ("+", "operator"),
#         ("0", "digit"),
#         ("a", "letter"),
#     ],
# )
# def test_classify_char(char, expected):
#     # TODO: refactor into more exhaustive tests of each category
#     assert classify_char(char) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("3+4", ["3", "+", "4"]),
        ("302 + sin(400)", ["302", "+", "sin", "(", "400", ")"]),
    ],
)
def test_tokenize(input, expected):
    assert list(tokenize(input)) == expected
