"""
# tokenizer.py
#
# split a stream of stuff into a stream of strings, and then enrich those into meaningful values
"""

from enum import Enum
from typing import Iterator
import math


# =========================
# Tokenization
#
# Break an input string into a sequence of string tokens
# Separation happens when we have whitespace, or when the characters for a token
# differ from neighbors (e.g. "3+4" -> ["3", "+", "4"])
# =========================

CHAR_TYPES = {
    "paren": {"(", ")"},  # "[", "]", "{", "}"},
    "operator": set(list("+-*/^")),
    # "decimal": {"."},  # for now, only use ints ;)
    "digit": set(list("0123456789")),
    # Letters can be used to name functions, e.g. "sin"
    # If we can't find a function w/ that name,
    # that will be an error during enrichment
    "letter": set(list("abcdefghijklmnopqrstuvwxyz")),
    "whitespace": {" ", "\t", "\n"},
}


# TODO: define a TokenType enum if needed
TOKEN_TYPES = {
    # character -> str
    **{char: "paren" for char in CHAR_TYPES["paren"]},
    **{char: "operator" for char in CHAR_TYPES["operator"]},
    **{char: "number" for char in CHAR_TYPES["digit"]},
    # **{char: "number" for char in CHAR_TYPES["decimal"]},  # NYI
    **{char: "function" for char in CHAR_TYPES["letter"]},
    **{char: "whitespace" for char in CHAR_TYPES["whitespace"]},
}

# def classify_char(c: str, char_types) -> str | None:
#     for key, values in char_types.items():
#         if c in values:
#             return key
#     return None


def tokenize(input: str) -> Iterator[str]:
    token = None
    token_type = None
    for c in input:
        if c not in TOKEN_TYPES:
            raise f"Unrecognized token character: {c}"
        char_type = TOKEN_TYPES[c]
        if char_type != token_type:
            if token is not None and token_type != "whitespace":
                yield token
            token = f"{c}"
            token_type = char_type
        else:
            # same token so concat them
            token = f"{token}{c}"
    # final token ;)
    yield token


# =========================
# Enrichment
## =========================


def enrich(items: Iterator[str]) -> Iterator:
    """
    Given a sequence of string tokens, replace them with Useful Shit
        numbers
        math functions
        operators (TODO: fix right associative exponents ;))
    """
    for item in items:
        try:
            i = int(item)
            yield i
        except:
            raise NotImplementedError
            pass

        # TODO: replace operators ("+") with operation functions
        # TODO: replace math functions ("sin", "abs") with math functions
