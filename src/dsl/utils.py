from collections import OrderedDict
from models.events import Event
from models.hand import Hand
from models.moves import Move
from models.moves import Positions
from models.pile import Pile
from models.player import Player
from models.rules import Rule
from utils.environment import global_env
import inspect

namespace = {
    "first": "bottom_card",
    "all": Positions.ANY,
    "top": Positions.LAST,
    "bottom": Positions.FIRST
}

def replace_keywords(words):
    return [int(word) if isinstance(word, str) and word.isdigit() else namespace.get(word, word) for word in words]


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

        # Globally-known operators
        global_val = global_env.get(current_token)
        if global_val:
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

    # Replace keywords with known values
    o = replace_keywords(output)
    return replace_keywords(output)

def check_env(loc, item):
    assert 0
    if callable(item):
        loc.append(item())
    else:
        try:

            op = global_env.find(item)[item][0]
            args = [loc.pop()]
            if loc:
                args.append(loc.pop())
            loc.append(op(*reversed(args)))
        except AttributeError as e:
            assert False, e
            loc.append(item)
        except TypeError as e:
            assert False, e
            loc.append(item)

def check_list(item_list):
    assert 0
    loc = []

    for item in item_list:
        check_env(loc, item[0])

    return loc[0]

def check_rule(rule, move, card):
    # TODO: Rules not working, as expected
    return evaluate(rule)

    if isinstance(card, Hand):
        return any([check_rule(rule, move, c) for c in card])

    for l in rule:
        if len(l) > 1:
            if l[0] == "rules":
                if stack:
                    first = stack.pop()
                    if stack:
                        second = stack.pop()
                        loc.append(check_rule(l[1], l2, l1))
                    else:
                        loc.append(check_rule(l[1], move, l1))
                else:
                    loc.append(check_rule(l[1], move, card))
            if l[0] == "card":
                val = [card]
                for j in l[1:]:
                    if callable(val):
                        val = val()
                    val = [getattr(val.pop(), j)]
                check_env(loc, val[0])
            elif l[0] == "move":
                val = [move]
                for j in l[1:]:
                    pop = val[-1]
                    if callable(pop):
                        val = [pop()]
                    val = [getattr(val.pop(), j)]
                check_env(loc, val[0])
        else: check_env(loc, l[0])
    return loc[0]


def evaluate(expression):
    stack = []

    def run(f):
        args = []
        argcount = len(inspect.signature(f).parameters)
        # required_args = argcount - 1 if inspect.ismethod(f) else argcount
        
        for _ in range(argcount):
            args.append(stack.pop())

        # Run function and push result
        result = f(*reversed(args))
        if callable(result):
            return run(result)
        else:
            return result

    for term in expression:
        if callable(term):
            stack.append(run(term))
        else:
            stack.append(term)

    assert len(stack) == 1, "Invalid expression: must result in exactly one result"
    return stack.pop()

def build_piles(pile_dict):
    piles = OrderedDict()
    for p in pile_dict:
        pile = Pile(p.get('name'), p.get('facedown'))
        piles[p.get('name')] = pile

    for name, pile in piles.items():
        namespace[pile.name] = pile

    return piles.items()

def build_players(player_dict, size, count):
    players = OrderedDict()
    for p in player_dict:
        player = Player(p.get('name'))
        # player.hand.restrict(lambda self: len(self.hand) <= size)
        player.add_collection(player.hand)
        players[p.get('name')] = player

    for name, player in players.items():
        namespace[player.name] = player

    return players.items()

def build_rules(rule_dict):
    rules = OrderedDict()
    for rule in rule_dict:
        rules[rule.get('name')] = build_list(rule.get('expr'))
        namespace[rule.get('name')] = rules[rule.get('name')]

    return rules

def build_moves(move_data):
    def build_move(move):
        m = {key: (build_list(value)) for key, value in move.items()}
        return Move(*[
            evaluate(m.get("where")),
            evaluate(m.get("from")),
            evaluate(m.get("to")),
            evaluate(m.get("when")),
            Rule(m.get("how"), check_rule)
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

