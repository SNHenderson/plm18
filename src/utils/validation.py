class Validatable(object):
    def __init__(self):
        self.restrictions = []
        self.should_validate = False

    def restrict(self, r):
        self.restrictions.add(r)

    def enable_validation():
        self.should_validate = True


def validate(undo=None):
    # The parameterized decorator
    def validate_with_undo(fn):

        # The decorated function
        def validating_fn(self, *args, **kwargs):
            fn(self, *args, **kwargs)
            if self.should_validate:
                valid = all([r(self) for r in self.restrictions])
                if not valid:
                    if undo is None:
                        raise ValidationException 
                    undo(self, *args, **kwargs)
                return valid
            return True

        return validating_fn

    return validate_with_undo

class ValidationException(Exception):
    pass
