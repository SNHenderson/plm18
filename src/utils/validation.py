class Validatable(object):
    def __init__(self):
        self.restrictions = set()

        # A dictionary that maps actions to rules that must be satisfied to take the action
        self.rules = {}
        self.should_validate = False

    def restrict(self, r):
        self.restrictions.add(r)

    def add_rule(self, fName, rule):
        """ Maps the function with name fName to a rule lambda
        """
        self.rules[fName] = rule

    def enable_validation(self):
        self.should_validate = True
        for prop in self.__dict__.values():
            if isinstance(prop, Validatable):
                prop.enable_validation()


def validate(undo=None):
    # The parameterized decorator
    def validate_with_undo(fn):

        # The decorated function
        def validating_fn(self, *args, **kwargs):
            val = fn(self, *args, **kwargs)
            if self.should_validate:
                valid = all([r(self) for r in self.restrictions])
                if not valid:
                    if undo: undo(self, *args, **kwargs)
                    raise ValidationException
            return val

        return validating_fn

    return validate_with_undo

def check_rule():
    """ For the given function, applies the rule associated
    with that function in self.rules{}, and only executes
    the function if the rule is satisfied. Throws exception
    otherwise
    """
    def check(fn):
        def do_move(self, *args):
            allowed = self.rules[fn.__name__](*args)
            if allowed:
                val = fn(self, *args)
            else:
                raise ValidationException
            return val
        return do_move
    return check


class ValidationException(Exception):
    pass
