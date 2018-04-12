import operator as op

class Operator(object):
    def __init__(self, name, function, precedence):
        self.name = name
        self.function = function
        self.precedence = precedence

    def __str__(self):
        return "<Operator %s >" % self.name

    def __repr__(self):
        return str(self)

def wrap(f):
    """
    Wraps a binary function with a lambda.
    Does not change in behavior, but it allows for method signature inspection.
    """
    w = lambda x, y: f(x, y)
    # w.__repr__ = f.__repr__
    return w


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

    def test(x,y):
        return x.__dict__[y]

    # Operator Precedence Hierarchy. Organized from low to high precedence
    oph = [
        [ ('or', op.or_), ('not', op.not_) ],
        [ ('and', op.and_) ],
        [ ('>', op.gt), ('<', op.lt), ('>=', op.ge), ('<=', op.le), ('=', op.eq) ],
        [ ('+', op.add), ('-', op.sub) ],
        [ ('.', lambda x, y: getattr(x, y) ) ]
    ]

    op_data = { operator: Operator(operator, wrap(function), precedence)
                  for (operators, precedence) in zip(oph, range(len(oph)))
                  for (operator, function) in operators }

    return op_data

global_env = standard_env()
