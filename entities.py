"""
# Stuff used to represent tokens that support:
# - Operators: have an associativity and a wrapped callable
# - rendering its value (e.g. div -> "/")
"""

import math
import operator
from enum import Enum


number = int | float


def div(a: number, b: number) -> number:
    """Wrap division in a callable since there isn't one in math or operator"""
    return a / b


# TODO: create a number class to wrap numeric types, if we ever need that?


class Special(Enum):
    PAREN_LEFT = "("
    PAREN_RIGHT = ")"
    COMMA = ","


class Callable:
    """base class for Operator and Function"""

    def __init__(self, function: callable, associativity="left", n_args=2):
        self.function = function
        self.associativity = associativity
        self.n_args = n_args  # consumers should check this before passing args

    def __call__(self, *args):
        return self.function(*args)

    def __eq__(self, other):
        return self.function == other.function and self.associativity == other.associativity


class Operator(Callable):
    """
    Operator is treated as a two-argument function,
    except maybe for then `!` wouldn't work
    """

    pass


class Function(Callable):
    """Wrap a callable, e.g. math.abs or math.gcd"""

    pass


entity_mapping = {
    "(": Special.PAREN_LEFT,
    ")": Special.PAREN_RIGHT,
    ",": Special.COMMA,
    # Unlike the built-in ** operator, math.pow() converts
    # both its arguments to type float. Use ** or the built-in pow()
    # function for computing exact integer powers.
    "^": Operator(operator.pow, associativity="right"),
    "/": Operator(div),
    "÷": Operator(div),
    "*": Operator(operator.mul),
    "×": Operator(operator.mul),
    "+": Operator(operator.add),
    "-": Operator(operator.sub),
    "%": Operator(operator.mod),
    # abs isn't infix so we don't consider it an "operator"
    "abs": Function(operator.abs, n_args=1),
    "sqrt": Function(math.sqrt, n_args=1),
    # numeric literals
    "π": math.pi,
    "pi": math.pi,
    # otherwise, default to getattr(math, func_name)
}


Entity = number | Special | Operator | Function


def get_entity(token: str) -> Entity:
    entity = entity_mapping.get(token)
    if entity is None:
        # it might be in math!
        math_func = getattr(math, token, None)
        if math_func is None:
            raise NotImplementedError
        else:
            # this will not work if math_func only takes one arg
            return Function(math_func)
    return entity
