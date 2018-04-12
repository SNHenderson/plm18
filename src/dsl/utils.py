from collections import OrderedDict
from models.events import Event
from models.hand import Hand
from models.moves import Move
from models.pile import Pile
from models.player import Player
from models.rules import Rule
from dsl.environment import global_env
from dsl.environment import Operator
import inspect

def replace_keywords(words, local_env):
    output = []
    for word in words:
        try:
            output.append(int(word))
        except (TypeError, ValueError):
            # Attempt to find the keyword in first the local and then the global environment
            val = local_env.get(word, global_env.get(word, word))
            if isinstance(val, list):
                # Looks like this was another expression, so expand it here
                output += replace_keywords(val, local_env)
            else:
                output.append(val)

    return output

def build_list(expr):
    # Replace syntactic sugar with the appropriate operator
    expr = expr.replace("'s ", ".")
    expr = expr.replace(".", " . ")

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
        print(expression, action)
        return evaluate(expression, {"move": action.move, "card": action.card})

    return Rule(action_checker)


def evaluate(expression, local_env=None):
    expression = replace_keywords(expression, local_env or {})

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

    def do_any(expr):
        m = local_env.get("move")
        results = [evaluate(expr, { "card": c, "move": m }) for c in m.end]
        return any(results)

    for term in expression:
        if callable(term):
            stack.append(run(term))
        elif isinstance(term, str) and term.startswith("any_"):
            subexpression = [term.replace("any_", "")]
            stack.append(do_any(subexpression))
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
        # player.hand.restrict(lambda self: len(self.hand) <= size)
        player.add_collection(player.hand)
        players[p.get('name')] = player

    for name, player in players.items():
        global_env[player.name] = player

    return players.items()

def create_env(assignments):
    local_env = {}
    iterations = {}
    for a in assignments:
        if a == "None":
            continue
        else:
            (var, op, expression) = a
            if op == "=":
                local_env[var] = evaluate(expression)
            elif op == "<-":
                iterations[var] = expression

    # TODO: Running
    # iterables = iterations.values()
        
    possible_environments = [ create_env(*comb) for combo in product(iterables) ]
    
    # TODO: run call rule with each environment, then run any or all

    return local_env

def build_rules(rule_dict):
    rules = OrderedDict()
    for rule in rule_dict:
        name = rule.get('name')
        parsed_rule = build_list(rule.get('expr'))
        parsed_assignments = build_assignments(rule.get('where'))
        rules[name] = parsed_rule
        global_env[name] = parsed_rule

    assert 0
    return rules

def build_moves(move_data):
    def build_move(move):
        m = {key: (build_list(value)) for key, value in move.items()}
            
        return Move(*[
            evaluate(m.get("from")),
            evaluate(m.get("to")),
            evaluate(m.get("when")),
            create_rule(m.get("how"))
        ])
    return [build_move(m) for m in move_data]

def build_events(event_data):
    def build_event(events):
        e = {key : build_list(value) for key, value in events.items()}
        return Event(lambda: evaluate(e.get('trigger')), lambda: do_event(e.get('action')))
    return [ build_event(e) for e in event_data ]

def build_win_condition(win_dict):
    w = build_list(win_dict)
    return lambda: evaluate(w)

def do_event(action):
    assert 0, "TODO"

    loc = []
    for l in action:
        if callable(l[0]) and loc:
            l[0](*loc)
            loc = []
        else:
            loc.append(l[0])

