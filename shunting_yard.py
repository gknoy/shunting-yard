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
        or if the stack is empty,
        or if the top of the stack is "(" (a floor)
        push it on the stack.
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
            # push function onto the stack until we get done w/ the parens
            # fn ( a, b , ... )
            stack.append(token)
        elif is_left_paren(token):
            stack.append(token)
        elif is_right_paren(token):
            # discard ')' token, pop + discard stack symbols until we see '('
            while stack and not is_left_paren(stack[-1]):
                yield stack.pop()
            if stack and is_left_paren(stack[-1]):
                # discard left paren (IDK about enforcing balance)
                stack.pop()
                #
            # if there's a function left at the top of the stack, pop + discard that
            # e.g sin(a)
            # (this one comes from wiki description I believe)
            if stack and is_function(stack[-1]):
                yield stack.pop()
        elif is_operator(token):
            # and has either
            #   higher precedence than the operator on the top of the stack,
            #   or has the same precedence as the operator on the top of the stack and is right associative,
            #   or if the stack is empty,
            #   or if the top of the stack is "(" (a floor)
            # push it on the stack.

            if (
                not stack
                or is_left_paren(stack[-1])
                or precedence(token) > precedence(stack[-1])
                or (precdence(token) == precedence(stack[-1]) and token.associativity == "left")
            ):
                stack.append(token)
            else:
                top_op = stack[-1]
                # TODO The rest of this

            # and has either
            #   lower precedence than the operator on the top of the stack,
            #   or has the same precedence as the operator on the top of the stack and is left associative
            # -- continue to pop the stack until this is not true.
            # -- Then, push the incoming operator.

        elif type(token) is Operator or type(token) is Special:
            # TODO: Consider Special type operators (paren, comma)
            # TODO: Fancy shit with precedence and parens
            pass

    # finally, once there are no more tokens, pop the rest of the stack:
    while stack:
        yield stack.pop()


def eval_rpn(input_rpn_tokens: list[Entity]) -> int | float:
    # evaluate the RPN stack
    # [3, 4, add] -> 7
    raise NotImplementedError
