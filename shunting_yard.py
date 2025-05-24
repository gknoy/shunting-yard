"""
# Shunting Yard algorithm implementation in Python
#
# cf. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
"""

from enum import Enum
from typing import Iterator
import math


# =========================
# Tokenization
# =========================

CHAR_TYPES = {
    "paren": {"(", ")", "[", "]", "{", "}"},
    "operator": set(list("+-*/")),  # for exponentiation, use "pow"
    # "decimal": {"."},  # for now, only use ints ;)
    "letter": set(list("abcdefghijklmnopqrstuvwxyz")),
    "digit": set(list("0123456789")),
    "whitespace": {" ", "\t", "\n"},
}


class TokenType(Enum):
    PAREN = 1
    OPERATOR: 2
    FUNCTION: 3
    NUMBER: 4
    IGNORED: 5


class Bracket(Enum):
    # TODO: match bracket flavors
    OPEN = 0
    CLOSE = 1


def classify_char(c: str, char_types) -> str | None:
    for key, values in char_types.items():
        if c in values:
            return key
    return None


class Token:
    token_type: str = None
    # valid_chars: list|str = None
    value = None

    def __init__(self, value):
        self.value = value

    def append(self, char):
        assert self.value is not None and type(char) is str
        self.value = f"{self.value}{char}"

    def get_value(self):
        raise NotImplementedError


class Whitespace(Token):
    token_type = TokenType.IGNORED

    def get_value(self):
        return None


class Paren(Token):
    token_type = TokenType.PAREN

    def get_value(self):
        # TODO: match bracket flavors
        if self.value in "({[":
            return Bracket.OPEN
        if self.value in "]})":
            return Bracket.CLOSE


class Number(Token):
    token_type = TokenType.NUMBER
    # valid_chars = CHAR_TYPES["digit"]

    def get_value(self):
        assert self.value is not None
        return int(self.value)


class Function(Token):
    token_type = TokenType.FUNCTION
    # valid_chars = CHAR_TYPES["letter"]

    def get_value(self):
        func = getattr(math, self.value)
        assert func is not None
        return func


# token generator (note type annotation requires python 3.13 ...)
def tokenize(line: str):  #  -> Iterator[str, int]
    """
    Read a line, return a list of tokens

    In:  "123 + log(42/7)"
    Out: ["123", "+", "log", "(", "42", "/", "7", ")"]
    """
    # TODO: Decide whether to return numbers vs strings that could be numbers
    current_char_class = None
    token = None
    for char in line:
        # TODO: Figure out what kind of token this char can be part of
        # if it's different than current,
        char_class = classify_char(char)
        # Return numbers if we have them
        if token is not None:
            try:
                # "123" -> 123
                token = int(token)
            except:
                pass
            yield token
            token = None

            #
            yield token

        token = char

    raise NotImplementedError


# =========================
# Processing tokens w/ shunting yard algorithm
# cf. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
# =========================


def get_rpn_tokens(input_tokens: list[str | int]) -> list[str | int]:
    raise NotImplementedError
