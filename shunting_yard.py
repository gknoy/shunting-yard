"""
# Shunting Yard algorithm implementation in Python
#
# cf. https://mathcenter.oxford.emory.edu/site/cs171/shuntingYardAlgorithm/
# cf. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
"""

from typing import Iterable
from entities import Special, Operator, Function, Entity
# from tokenizer import tokenize, enrich


# =========================
# Process existing tokens w/ shunting yard algorithm
# =========================


def is_left_paren(token):
    return token is Special.PAREN_LEFT


def is_right_paren(token):
    return token is Special.PAREN_RIGHT


def is_number(token):
    return type(token) in [float, int]


def is_function(token):
    return type(token) is Function


def is_operator(token):
    return type(token) is Operator


def get_rpn_tokens(input_tokens: Iterable[Entity]) -> Iterable[Entity]:
    """
    cf. https://mathcenter.oxford.emory.edu/site/cs171/shuntingYardAlgorithm/

    If the incoming symbols is an operand, print it..
    If the incoming symbol is a left parenthesis, push it on the stack.
    If the incoming symbol is a right parenthesis:
        discard the right parenthesis,
        pop and print the stack symbols until you see a left parenthesis.
        Pop the left parenthesis and discard it.
    If the incoming symbol is an operator and the stack is empty or contains a left parenthesis on top,
        push the incoming operator onto the stack.
    If the incoming symbol is an operator
        and has either higher precedence than the operator on the top of the stack,
        or has the same precedence as the operator on the top of the stack and is right associative,
        or if the stack is empty, or if the top of the stack is "(" (a floor) -- push it on the stack.
    If the incoming symbol is an operator and has either lower precedence than the operator on the top of the stack,
        or has the same precedence as the operator on the top of the stack and is left associative --
        continue to pop the stack until this is not true. Then, push the incoming operator.
    At the end of the expression, pop and print all operators on the stack. (No parentheses should remain.)
    """
    stack = []  # contains operators, functions, and parens

    for token in input_tokens:
        if is_number(token):
            yield token
            stack.append(token)
        elif is_function(token):
            stack.append(token)
        elif is_left_paren(token):
            stack.append(token)
        elif is_right_paren(token):
            # discard ')' token, pop + discard stack symbols until we see '('
            while stack and not is_left_paren(stack[-1]):
                yield stack.pop()
            if stack and is_left_paren(stack[-1]):
                stack.pop()  # discard left paren
            # if there's a function left at the top ofthe stack, pop + discard that
            # e.g sin(a)
            if stack and is_function(stack[-1]):
                pass  # FIXME
        elif is_operator(token):
            if not stack or is_left_paren(stack[-1]):
                stack.append(token)
            else:
                top_op = stack[-1]
                # TODO The rest of this

        elif type(token) is Operator or type(token) is Special:
            # TODO: Consider Special type operators (paren, comma)
            # TODO: Fancy shit with precedence and parens
            pass

    raise NotImplementedError


def eval_rpn(input_rpn_tokens: list[Entity]) -> int | float:
    # evaluate the RPN stack
    # [3, 4, add] -> 7
    raise NotImplementedError
