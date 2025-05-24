"""
# test_shunting.py
"""
import pytest

from shunting_yard import classify_char, tokenize, get_rpn_tokens


@pytest.mark.parametrize(
    "char,expected", [
        (")", "paren")
        ("+", "operator"),
        ("0", "digit"),
        ("a", "letter"),
    ]
)
def test_classify_char(char, expected):
    # TODO: refactor into more exhaustive tests of each category
    assert classify_char(char) == expected



