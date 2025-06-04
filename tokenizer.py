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
from token import ENCODING, NEWLINE, ENDMARKER, MINUS, NUMBER
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

        I want intercept MINUS tokens and yield negative numbers if the minus is followed by a number.

    FIXME: This is completely fucked at trying to recognize negative numbers. :)

     -----5
     is the same as
     (-(-(-(-(-5)))))

    I'd like to replace e.g. "---5" -> ["-5"]
    but instead i can just pass `neg` on to the calculation and leave it be.
    "sin(-5) -> [sin, (, -5, )]
    """
    _last = None  # the last non-minus token we've seen.

    for index, token in enumerate(tokens):
        try:
            number = int(token)  # todo: handle floats or ints
            _last = number
            yield number
            continue
        except:
            pass

        try:
            number = float(token)
            _last = number
            yield number
            continue
        except:
            pass

        # get a function, named constant, operator, or Paren
        entity = get_entity(token)

        if entity == Special.MINUS:
            if (
                index == 0  # first token
                or _last is None  # nth minus in a row since start
                or _last == Special.PAREN_LEFT
                or (type(_last) is Operator and _last != neg)
            ):
                entity = neg

            elif (
                # - we follow a number or a closed paren
                type(_last) is int or type(_last) is float or _last == Special.PAREN_RIGHT
            ):
                entity = subtract
            else:
                raise Exception(f"invalid: {entity}, prev non-minus: {_last}")
            yield entity
            continue

        # otherwise, we have a pi or an operator:
        _last = entity
        yield entity
