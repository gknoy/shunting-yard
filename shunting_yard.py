"""
# Shunting Yard algorithm implementation in Python
#
# cf. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
"""

from typing import Callable
from entities import number, Paren, Special, Operator, Function
from tokenizer import tokenize, enrich, Paren, Operator, Special


# =========================
# Processing tokens w/ shunting yard algorithm
# cf. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
# =========================


TokenType = int | Paren | Callable


def is_number(token):
    return type(token) in [float, int]


def get_rpn_tokens(input_tokens: list[TokenType]) -> list[TokenType]:
    """
    while there are tokens to be read:
        read a token
        if the token is:
        - an operator o1:
            while (
                there is an operator o2 at the top of the operator stack which is not a left parenthesis,
                and (o2 has greater precedence than o1 or (o1 and o2 have the same precedence and o1 is left-associative))
            ):
                pop o2 from the operator stack into the output queue
            push o1 onto the operator stack
        - a ",":
            while the operator at the top of the operator stack is not a left parenthesis:
                pop the operator from the operator stack into the output queue
        - a left parenthesis (i.e. "("):
            push it onto the operator stack
        - a right parenthesis (i.e. ")"):
            while the operator at the top of the operator stack is not a left parenthesis:
                {assert the operator stack is not empty}
                /* If the stack runs out without finding a left parenthesis, then there are mismatched parentheses. */
                pop the operator from the operator stack into the output queue
            {assert there is a left parenthesis at the top of the operator stack}
            pop the left parenthesis from the operator stack and discard it
            if there is a function token at the top of the operator stack, then:
                pop the function from the operator stack into the output queue
    /* After the while loop, pop the remaining items from the operator stack into the output queue. */
    while there are tokens on the operator stack:
        /* If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses. */
        {assert the operator on top of the stack is not a (left) parenthesis}
        pop the operator from the operator stack onto the output queue
    """
    stack = []
    operator_stack = []

    for token in input_tokens:
        if is_number(token):
            stack.append(token)
        if type(token) is not Operator and callable(token):
            operator_stack.append(token)
        if type(token) is Operator or type(token) is Special:
            # TODO: Consider Special type operators (paren, comma)
            # TODO: Fancy shit with precedence and parens
            pass

    raise NotImplementedError


def eval_rpn(input_rpn_tokens: list[TokenType]) -> int | float:
    # evaluate the RPN stack
    # [3, 4, add] -> 7
    raise NotImplementedError
