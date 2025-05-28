"""
# tokenizer.py
#
# split a stream of stuff into a stream of strings, and then enrich those into meaningful values
"""

import math
import operator
from enum import Enum

# I feel like it's clearer to use 'operator.add' later on
# from math import sin, cos, tan, sqrt
# from operator import abs, add, sub, mul, pow
from typing import Iterator

from functions import div


# =========================
# Tokenization
#
# Break an input string into a sequence of string tokens
# Separation happens when we have whitespace, or when the characters for a token
# differ from neighbors (e.g. "3+4" -> ["3", "+", "4"])
# =========================

CHAR_TYPES = {
    "paren": {"(", ")"},  # "[", "]", "{", "}"},
    "operator": set(list("+-*/^÷×")),
    "special": {"π"},
    "numeric": set(list("0123456789.")),  # TODO: support "3e4" notation
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
    **{char: "number" for char in CHAR_TYPES["numeric"]},
    **{char: "special" for char in CHAR_TYPES["special"]},
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
        # TODO: Maybe use multiple valid token types for a char,
        #       so that seeing 'e' can be used in numbers or
        if char_type != token_type:
            if token is not None and token_type != "whitespace":
                yield token
            token = f"{c}"
            token_type = char_type
        elif token_type in ["operator", "special"]:
            # return the previous operator we saw,
            # since we can't have multi-char operators.
            # (use "^" instead of "**")
            # (pi is included here)
            yield token
        else:
            # same token so concat them
            token = f"{token}{c}"
    # final token ;)
    yield token


# =========================
# Enrichment
## =========================


class Paren(Enum):
    LEFT = "("
    RIGHT = ")"

    @classmethod
    def match(cls, s):
        for item in [cls.LEFT, cls.RIGHT]:
            if item.value == s:
                return item
        return None


entity_mapping = {
    # Unlike the built-in ** operator, math.pow() converts
    # both its arguments to type float. Use ** or the built-in pow()
    # function for computing exact integer powers.
    "^": operator.pow,
    "/": div,
    "÷": div,
    "*": operator.mul,
    "×": operator.mul,
    "+": operator.add,
    "-": operator.sub,
    # TODO: idk how to differentiate negative numbers
    #   Ideally we do this during enrichment, so "3--4" -> [3, sub, -4]
    "abs": operator.abs,
    "%": operator.mod,
    "π": math.pi,
    "pi": math.pi,
    # otherwise, default to getattr(math, func_name)
}


def enrich(items: Iterator[str]) -> Iterator:
    """
    Given a sequence of string tokens, replace them with Useful Shit
        numbers
        math functions
        operators (TODO: fix right associative exponents ;))
    """
    for item in items:
        try:
            number = int(item)  # todo: handle floats or ints
            yield number
            continue
        except:
            pass

        try:
            number = float(item)
            yield number
            continue
        except:
            pass

        if item == "pi":
            yield math.pi
            continue

        maybe_paren = Paren.match(item)
        if maybe_paren:
            yield maybe_paren
            continue

        func = entity_mapping.get(item, None)
        if func is None:
            # try to look it up in math
            func = getattr(math, item, None)
        if func is None:
            raise NotImplementedError
        yield func
