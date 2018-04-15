import inspect
import itertools

from collections import OrderedDict
from dsl.environment import Operator
from dsl.environment import global_env
from models.events import Event
from models.hand import Hand
from models.moves import Move
from models.pile import Pile
from models.player import Player
from models.rules import Rule

class Expression(object):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.token)

    def eval(self, env):
        raise NotImplementedError("Cannot evaluate " + self.token)

class OperandExpression(Expression):
    def __init__(self, token):
        super().__init__(token)

    def eval(self, env):
        tok = self.token
        if self.is_numeric():
            return int(tok)
        else: 
            # Look for the name first in the local and then the global environment
            return env.get(tok, global_env.get(tok, tok))
    
    def is_numeric(self):
        return self.token.isdigit()

class RuleExpression(Expression):
    def __init__(self, token, expression, assignments):
        super().__init__(token)
        self.expression = expression
        self.assignments = assignments

    def eval(self, env):
        bindings = env.copy()
        iterations = {}

        # Parse assignments
        for a in self.assignments:
            if a == "None":
                continue
            else:
                name = a[0]
                op = a[1]
                expr = a[2:]

                resolved_expr = evaluate(parse(expr), env)
                assert not isinstance(resolved_expr, str), "Could not resolve '%s'" % expr

                if op == "=":
                    bindings[name] = resolved_expr
                elif op == "<-":
                    iterations[name] = resolved_expr
                else:
                    assert False, "Unexpected operator '%s'" % op

        expr = self.expression.copy()
        if iterations:
            # Rules with iterations must start with an iteration keyword
            keyword = expr.pop(0).token

            if keyword == "any":
                iteration_func = any
            elif keyword == "all":
                iteration_func = all
            else:
                raise ValueError("Unknown iteration keyword: '%s'" % keyword)

            # Generate possible environments. This could be more efficient using iterators
            possible_bindings = [ [ ( name, item ) for item in resolved ]
                                  for (name, resolved) in iterations.items() ]

            # Try all possible enivronments
            results = []
            for selected_bindings in itertools.product(*possible_bindings):
                bound_env = { k: v for (k, v) in selected_bindings }
                bindings.update(bound_env)
                result = evaluate(expr, bindings)
                results.append(result)
            return iteration_func(map(lambda x: x is True, results))

        else:
            return evaluate(expr, bindings)

def parse(expr):
    # Don't accidentally iterate over a string
    assert not isinstance(expr, str)

    # List of operators in format (op, level) where level is level of nesting op was found at
    op_stack = []

    # Output post-fix list
    output = []

    # Current level of nesting
    level = 0

    # Purges the operator stack of operators higher in precedence than the given value in the current level of nesting
    def shunt_ops(precedence=-1):
        for (op, op_level) in reversed(op_stack):
            if precedence <= op.precedence and op_level == level:
                output.append(op)
                op_stack.pop()
            else:
                break

    for current_token in expr:
        # Opening parentheses indicate another level of nesting
        if current_token == "(":
            level += 1

        # Closing parentheses indicate the current level of nesting is closed
        elif current_token == ")":
            shunt_ops()
            level -= 1
        else:
            # Check for globally known operators and functions
            global_val = global_env.get(current_token)

            if callable(global_val):
                # Treat global functions as operators with low precedence
                global_val = Operator(global_val.__name__, global_val, 1) 

            if isinstance(global_val, Operator):
                # Perform shunting if necessary
                if op_stack and global_val.precedence <= op_stack[-1][0].precedence:
                    shunt_ops(global_val.precedence)

                # Push operator to the stack
                op_stack.append((global_val, level))

            # Must be an operand
            else:
                output.append(OperandExpression(current_token))

    # Push any remaining operators to the output
    shunt_ops()

    return output

def evaluate(expression, local_env=None):
    assert not isinstance(expression, str), "Cannot evaluate strings: " + expression

    local_env = local_env.copy() if local_env else {}
    stack = []

    def run(f):
        args = []
        argcount = len(inspect.signature(f).parameters)

        for _ in range(argcount):
            args.append(stack.pop())

        # Run function
        result = f(*reversed(args))
        return evaluate([result])

    def evaluate_term(term):
        if callable(term):
            return run(term)
        elif isinstance(term, Operator):
            return run(term.function)
        elif isinstance(term, RuleExpression):
            return term.eval(local_env)
        elif isinstance(term, OperandExpression):
            # Resolve the term and re-evaluate the result in case it resolves to another type of Expression
            result = term.eval(local_env)
            return evaluate_term(result)
        return term

    for term in expression:
        stack.append(evaluate_term(term))

    assert len(stack) == 1, "Invalid expression: evaluation must produce exactly one result"
    return stack.pop()

def build_piles(pile_dict):
    piles = OrderedDict()
    for p in pile_dict:
        pile = Pile(p.get('name'), p.get('facedown'))
        piles[p.get('name')] = pile

    for name, pile in piles.items():
        global_env[pile.name] = pile

    return piles.items()

def build_players(player_dict, size, count):
    players = OrderedDict()
    for p in player_dict:
        player = Player(p.get('name'))
        player.add_collection(player.hand)
        players[p.get('name')] = player

    for name, player in players.items():
        global_env[player.name] = player

    return players.items()

def build_rules(rule_dict):
    rules = OrderedDict()
    for rule in rule_dict:
        name = rule.get('name')
        expression = parse(rule.get("expr"))
        assignments = rule.get("let")

        r = RuleExpression(name, expression, assignments)
        rules[name] = r
        global_env[name] = r

    return rules

def build_moves(move_data):
    def create_rule(expression, assignments):
        parsed = parse(expression)
        def action_checker(action):
            # Initial environment contains all of the action's and move's properties
            initial_env = action.move.__dict__.copy()
            initial_env.update(action.__dict__)
            return RuleExpression(expression, parsed, assignments).eval(initial_env)
        return Rule(action_checker)

    resolve = lambda x: evaluate(parse(x))
    def build_move(move):
        return Move(*[
            resolve(move.get("where")),
            resolve(move.get("from")),
            resolve(move.get("to")),
            move.get("trigger"),
            create_rule(move.get("how"), move.get("let"))
        ])
    return [build_move(m) for m in move_data]

def build_events(event_data):
    def build_event(event):
        e = {key : parse(value) for key, value in event.items()}
        return Event(lambda: evaluate(e.get('trigger')), lambda: do_event(e.get('action')))
    return [ build_event(e) for e in event_data ]

def build_win_condition(win_condition):
    w = parse(win_condition)
    return lambda: evaluate(w)

def do_event(action):
    evaluate(action)

