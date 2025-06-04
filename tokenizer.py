"""
# tokenizer.py
#
# split a stream of stuff into a stream of strings, and then enrich those into meaningful values
#
# Uses python's builtin tokenize.tokenize to get tokens, which auto-handles finding numbers and names and parens
#
#    In [51]: tokens = list(tokenize(BytesIO("-3e2 - -4.3 * sin(π)".encode("utf-8")).readline))
#    In [52]: tokens
#    Out[52]:
#    [TokenInfo(type=65 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line=''),
#    TokenInfo(type=55 (OP), string='-', start=(1, 0), end=(1, 1), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=2 (NUMBER), string='3e2', start=(1, 1), end=(1, 4), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=55 (OP), string='-', start=(1, 5), end=(1, 6), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=55 (OP), string='-', start=(1, 7), end=(1, 8), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=2 (NUMBER), string='4.3', start=(1, 8), end=(1, 11), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=55 (OP), string='*', start=(1, 12), end=(1, 13), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=1 (NAME), string='sin', start=(1, 14), end=(1, 17), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=55 (OP), string='(', start=(1, 17), end=(1, 18), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=1 (NAME), string='π', start=(1, 18), end=(1, 19), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=55 (OP), string=')', start=(1, 19), end=(1, 20), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=4 (NEWLINE), string='', start=(1, 20), end=(1, 21), line='-3e2 - -4.3 * sin(π)'),
#    TokenInfo(type=0 (ENDMARKER), string='', start=(2, 0), end=(2, 0), line='')]
"""

from io import BytesIO
from token import ENCODING, NEWLINE, ENDMARKER
from tokenize import tokenize as builtin_tokenize
from typing import Iterator

from entities import get_entity, Special, Operator, neg, subtract


# =========================
# Tokenization
#
# Break an input string into a sequence of string tokens
# Separation happens when we have whitespace, or when the characters for a token
# differ from neighbors (e.g. "3+4" -> ["3", "+", "4"])
# =========================


def tokenize(input: str) -> Iterator[str]:
    """
    Use the builtin tokenize.tokenize to get a stream of tokens
    Tokens have a type, exact_type, and a string field.
    """
    # the builtin tokenize.tokenize reads from the readline method of
    # an input stream instance.  Super weird to use in this way :)
    token_stream = builtin_tokenize(BytesIO(input.encode("utf-8")).readline)
    for token in token_stream:
        if token.type in {ENCODING, NEWLINE, ENDMARKER}:
            continue
        # I don't love that this throws away the
        # tokenizer's knowledge that this token is a number or MINUS,
        # but I'm deliberately yielding only strings from this.
        yield token.string


# =========================
# Enrichment
## =========================


def enrich(tokens: Iterator[str]) -> Iterator:
    """
    Given a sequence of string tokens, replace them with Useful Shit
    - numbers
    - math operators -> functions
    - math functions -> functions
    - minuses -> neg or subtract functions (which have different arity)

    Misc notes:
        -----5
        is the same as
        (-(-(-(-(-5)))))

    I'd like to replace e.g. "---5" -> ["-5"]
    but instead I can just pass `neg` on to the calculation and leave it be.
    """
    last_non_minus = None  # the last non-minus entity we've seen.

    for index, token in enumerate(tokens):
        try:
            number = int(token)  # todo: handle floats or ints
            last_non_minus = number
            yield number
            continue
        except ValueError:
            pass

        try:
            number = float(token)
            last_non_minus = number
            yield number
            continue
        except ValueError:
            pass

        if token == "-":
            if (
                index == 0  # first token
                or last_non_minus is None  # nth minus in a row since start
                or last_non_minus == Special.PAREN_LEFT
                or (type(last_non_minus) is Operator and last_non_minus != neg)
            ):
                entity = neg

            elif (
                # - we follow a number or a closed paren
                type(last_non_minus) is int
                or type(last_non_minus) is float
                or last_non_minus == Special.PAREN_RIGHT
            ):
                entity = subtract
            else:
                raise Exception(f"Unexpected Minus, prev non-minus: {last_non_minus}")
            yield entity
            continue

        # Otherwise, we have a function, named constant, operator, or Paren
        entity = get_entity(token)

        last_non_minus = entity
        yield entity
