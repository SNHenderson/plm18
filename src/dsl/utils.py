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


def replace_keywords(words, local_env):
    output = []
    for word in words:
        try:
            output.append(int(word))
        except (TypeError, ValueError):
            # Attempt to find the keyword in first the local and then the global environment
            val = local_env.get(word, global_env.get(word, word))
#           if val in global_env.get("rules"):
#               output += replace_keywords(val, local_env)
#           else:
            output.append(val)

    return output

def parse(expr):
    # Replace syntactic sugar with the appropriate operator
    expr = expr.replace("'s", ".")

    # List of operators in format (op, level) where level is level of nesting op was found at
    op_stack = []

    # Output post-fix list
    output = []

    # Current level of nesting
    level = 0

    # Purges the operator stack of operators in the current level of nesting higher in precendence than the given value
    def shunt_ops(precedence=-1):
        for (op, op_level) in reversed(op_stack):
            if precedence <= op.precedence and op_level == level:
                output.append(op.function)
                op_stack.pop()
            else:
                break

    for current_token in expr.split():

        # Check for known operators
        global_val = global_env.get(current_token)
        if global_val and isinstance(global_val, Operator):
            # Perform shunting if necessary
            if op_stack and global_val.precedence <= op_stack[-1][0].precedence:
                shunt_ops(global_val.precedence)
            # Add operator to the stack
            op_stack.append((global_val, level))

        # Opening parentheses indicate another level of nesting
        elif current_token == "(":
            level += 1

        # Closing parentheses indicate the current level of nesting is closed
        elif current_token == ")":
            shunt_ops()
            level -= 1

        # Operands
        else:
            output.append(current_token)

    # Push any remaining operators to the output
    shunt_ops()

    return output

def create_rule(expression):
    def action_checker(action):
        # Initial environment contains all of the action's and move's properties
        initial_env = action.move.__dict__.copy()
        initial_env.update(action.__dict__)
        return evaluate(expression, initial_env)

    return Rule(action_checker)


def evaluate(expression, local_env=None):
    local_env = local_env.copy() if local_env else {}
    expression = replace_keywords(expression, local_env)

    stack = []

    def run(f):
        args = []
        argcount = len(inspect.signature(f).parameters)

        for _ in range(argcount):
            args.append(stack.pop())

        # Run function
        result = f(*reversed(args))
        if callable(result):
            # If the result is a function, run that one too
            return run(result)
        else:
            return result

    for term in expression:
        if callable(term):
            stack.append(run(term))
        elif isinstance(term, RuleExpression):
            result = term.eval(local_env)
            stack.append(result)
        else:
            stack.append(term)

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


class RuleExpression(object):
    # TODO: Put this code somewhere it actually makes sense

    def __init__(self, expression, assignments):
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
                (var, op, expr) = a
                resolved_expr = evaluate(parse(expr), env)
                assert not isinstance(resolved_expr, str), "Could not resolve '%s'" % expr

                if op == "=":
                    bindings[var] = resolved_expr
                elif op == "<-":
                    iterations[var] = resolved_expr
                else:
                    assert False, "Unexpected operator '%s'" % op

        expr = self.expression.copy()
        if iterations:
            keyword = expr.pop(0)
            if keyword == "any":
                iteration_func = any
            elif keyword == "all":
                iteration_func = all
            else:
                assert False, "Unknown iteration keyword: '%s'" % keyword

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
            temp = evaluate(expr, bindings)
            return temp

            return evaluate(expr, bindings)
        

def build_rules(rule_dict):
    rules = OrderedDict()
    for rule in rule_dict:
        name = rule.get('name')
        expression = parse(rule.get("expr"))
        assignments = rule.get("where")

        r = RuleExpression(expression, assignments)
        rules[name] = r
        global_env[name] = r

    return rules

def build_moves(move_data):
    def build_move(move):
        m = {key: (parse(value)) for key, value in move.items()}
        return Move(*[
            evaluate(m.get("where")),
            evaluate(m.get("from")),
            evaluate(m.get("to")),
            evaluate(m.get("trigger")),
            create_rule(m.get("how"))
        ])
    return [build_move(m) for m in move_data]

def build_events(event_data):
    def build_event(events):
        e = {key : parse(value) for key, value in events.items()}
        return Event(lambda: evaluate(e.get('trigger')), lambda: do_event(e.get('action')))
    return [ build_event(e) for e in event_data ]

def build_win_condition(win_condition):
    w = parse(win_condition)
    return lambda: evaluate(w)

def do_event(action):
    evaluate(action)

