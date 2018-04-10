import operator as op

#Source: http://norvig.com/lispy.html. Modified as needed.
class Env(dict):
    "An environment: a dict of {'var':[val, precedence]} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)

def standard_env() -> Env:
    "An environment with some standard procedures."
    env = Env()
    env.update({
        '*': [op.mul, 5], '/': [op.truediv, 5],
        '+': [op.add, 4], '-': [op.sub, 4],
        '>': [op.gt, 3], '<': [op.lt, 3], '>=': [op.ge, 3], '<=': [op.le, 3], '=': [op.eq, 3],
        'and': [op.and_, 2], 
        'or': [op.or_, 1], 'not': [op.not_, 1]
    })
    return env

global_env = standard_env()