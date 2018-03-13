class Validatable(object):
    def __init__(self):
        self.restrictions = set()

        self.should_validate = False

    def restrict(self, r):
        self.restrictions.add(r)

    def enable_validation(self):
        self.should_validate = True
        for prop in self.__dict__.values():
            if isinstance(prop, Validatable) and not prop.should_validate:
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

class ValidationException(Exception):
    pass
