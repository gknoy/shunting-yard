"""
# Shunting Yard algorithm implementation in Python
#
# cf. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
"""

from typing import Callable
from tokenizer import tokenize, enrich, Paren


# =========================
# Processing tokens w/ shunting yard algorithm
# cf. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
# =========================


TokenType = int | Paren | Callable


def get_rpn_tokens(input_tokens: list[TokenType]) -> list[TokenType]:
    raise NotImplementedError


def eval_rpn(input_rpn_tokens: list[TokenType]) -> int | float:
    # evaluate the RPN stack
    # [3, 4, add] -> 7
    raise NotImplementedError
