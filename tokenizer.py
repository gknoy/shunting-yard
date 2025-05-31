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
from token import *
from tokenize import tokenize as builtin_tokenize
from typing import Iterator

from entities import get_entity


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

    I want intercept MINUS tokens and yield negative numbers if the minus is followed by a number.
    """
    # the builtin tokenize.tokenize reads from the readline method of
    # an input stream instance.  Super weird to use in this way :)
    token_stream = builtin_tokenize(BytesIO(input.encode("utf-8")).readline)

    # The minus tokens we haven't yet yielded.
    # When we see a minus, we don't yield it until we know whether we
    # have a negative number.
    # e.g.
    #   - - - 4  # bad
    #   - - 4    # [-, -4]
    #   - 4      # [ -4 ]
    #   - pi     # [ -pi ]  (any number or the literals "pi" or "π")
    #   - (      # [-, LPAR]
    minuses = []
    pies = {"pi", "π"}

    for token in token_stream:
        print(f">>> {token}")
        if token.type in {ENCODING, NEWLINE, ENDMARKER}:
            print("skipping token")
            continue
        if token.exact_type == MINUS:
            print(" Stashing minus token")
            minuses.append(token)
            continue  # we don't know whether to yield things
        if token.type == NUMBER or token.string in pies:
            if len(minuses):
                for minus in minuses[:-1]:
                    print(f" --> yielding '-'")
                    yield "-"
                print(f" --> yielding {token}")
                yield f"-{token.string}"
            else:
                print(f" --> yielding {token}")
                yield token.string
        else:
            for minus in minuses[:-1]:
                print(f" --> yielding '-'")
                yield "-"
            print(f" --> yielding {token}")
            yield token.string


# =========================
# Enrichment
## =========================

# FIXME: Move special + operators to functions.py -> rename operators.py


def enrich(tokens: Iterator[str]) -> Iterator:
    """
    Given a sequence of string tokens, replace them with Useful Shit
    """
    # Note: this expects incoming tokens to already have negativeness applied
    for token in tokens:
        try:
            number = int(token)  # todo: handle floats or ints
            yield number
            continue
        except:
            pass

        try:
            number = float(token)
            yield number
            continue
        except:
            pass

        # get a function, named constant, operator, or Paren
        yield get_entity(token)
