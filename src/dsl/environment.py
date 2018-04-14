import operator as op
import inspect
from models.moves import Positions

class Operator(object):
    def __init__(self, name, function, precedence):
        self.name = name
        self.function = function
        self.precedence = precedence

    def __str__(self):
        return "<Operator %s >" % self.name

    def __repr__(self):
        return str(self)

def wrap(f, unary=False):
    """
    Wraps a builtin function with a lambda.
    Does not change behavior, but it allows for method signature inspection.
    """
    if not inspect.isbuiltin(f):
        return f
    elif unary:
        return lambda x: f(x)
    else:
        return lambda x, y: f(x, y)


#Source: http://norvig.com/lispy.html. Modified as needed.
class Env(dict):
    "An environment: a dict of {'var':[val, precedence]} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)

def standard_env():
    "An environment with some standard procedures."
    env = dict()

    # Operator Precedence Hierarchy
    # Each set is a precedence class, and sets are ordered from low to high precedence
    # Each enter is in the form (name, function, arity)
    oph = [
        { ('or', op.or_), ('not', op.not_) },
        { ('and', op.and_) },
        { ('>', op.gt), ('<', op.lt), ('>=', op.ge), ('<=', op.le), ('is', op.eq) },
        { ('+', op.add), ('-', op.sub) },
        { ('.', lambda x, y: getattr(x, y) ) }
    ]
    unary_ops = {'not'}

    # Add operator data
    env.update({ operator: Operator(operator, wrap(function, operator in unary_ops), precedence)
                   for (operators, precedence) in zip(oph, range(len(oph)))
                   for (operator, function) in operators })

    # Add position data
    env.update({
        "all": Positions.ANY,
        "top": Positions.LAST,
        "bottom": Positions.FIRST
    })

    for list_name in ["players", "piles", "rules", "moves", "events"]:
        env[list_name] = []

    return env

global_env = standard_env()
