"""
# Stuff used to represent tokens that support:
# - Operators: have an associativity and a wrapped callable
# - rendering its value (e.g. div -> "/")
"""

import math
import operator
from enum import Enum
from typing import Iterable


number = int | float


def div(a: number, b: number) -> number:
    """Wrap division in a callable since there isn't one in math or operator"""
    return a / b


# unary negation
def neg(a: number) -> number:
    return -1 * number


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
        return (
            self.function == other.function
            and self.associativity == other.associativity
            and self.n_args == other.n_args
        )

    def __repr__(self):
        return f"fn={self.function} assoc={self.associativity} n_args={self.n_args}"


class Operator(Callable):
    """
    Operator is a callable that assumes either two arguments (a f b) or operand (f a)
    However, some operators (factorial) come AFTER the operand, and some (neg) come before.

    unary: "left" if operator left of operand
           "right" if operator right of operand

    e.g.
        3 - 5  # unary False
          - 5  # unary left
        3 !    # unary right
    """

    def __init__(
        self, function: callable, associativity="left", n_args=2, unary: bool | str = False
    ):
        super().__init__(function, associativity, n_args)
        assert unary in (False, "left", "right")
        self.unary = unary

    def __eq__(self, other):
        return (
            type(self) is type(other)
            and self.function == other.function
            and self.associativity == other.associativity
            and self.n_args == other.n_args
            and self.unary == other.unary
        )


class Function(Callable):
    """
    Wrap a callable, e.g. math.abs or math.gcd
    Syntactically, we expect "{function}({arg}, {arg2})",
    But honestly I don't see how this is different from an Operator other
    than that Operators are written infix (or prefix), whereas have parens after them and optional comma separated args

    min(a b)
    min(a,b)  # optional comma
    """

    def __eq__(self, other):
        return (
            type(self) is type(other)
            and self.function == other.function
            and self.associativity == other.associativity
            and self.n_args == other.n_args
        )


entity_mapping = {
    "(": Special.PAREN_LEFT,
    ")": Special.PAREN_RIGHT,
    ",": Special.COMMA,  # used in some function calls, e.g. max(a, b)
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
    "neg": Operator(neg, n_args=1, unary="left"),
    "~": Operator(neg, n_args=1, unary="left"),
    # Disallow 5!, use factorial(5) instead
    # mainly because I don't wat to handle "-5!"
    # "!": Operator(math.factorial, n_args=1, unary="right"),
    # abs isn't infix so we don't consider it an "operator"
    "abs": Function(operator.abs, n_args=1),
    "sqrt": Function(math.sqrt, n_args=1),
    "factorial": Function(math.factorial, n_args=1),
    # numeric literals
    "π": math.pi,
    "pi": math.pi,
    # otherwise, we default to getattr(math, func_name)
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


def render(entity: Entity) -> str:
    # renders the first-encountered entity (in case we have two names)
    for name, e in entity_mapping.items():
        if type(e) is type(entity) and e == entity:
            return name
    # fallback for something we didn't specify:
    if type(entity) is Function or type(entity) is Operator:
        return entity.function.__name__
    if type(entity) in [int, float]:
        return entity


def render_tokens(entities: Iterable[Entity]) -> str:
    return " ".join(render(e) for e in entities)


def get_precedence(op: Operator | Function) -> int:
    raise NotImplementedError
