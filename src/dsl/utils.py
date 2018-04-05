from models.game import Game
from models.pile import Pile
from models.player import Player
from models.rank import Rank
from models.suit import Suit
from models.hand import Hand
from models.moves import Move
from models.events import Event
from models.rules import Rule
from models.moves import Positions
from models.collection import Collection
from dsl.utils import *
from utils.objs import dict_obj
from utils.environment import global_env
from collections import OrderedDict
from random import shuffle

namespace = {
    "first": "bottom_card",
    "toprank": "top_rank",
    "topsuit": "top_suit",
    "all": Positions.ANY,
    "top": Positions.LAST
}

def replace_keywords(words):
    ints = [int(word) if word.isdigit() else word for word in words]
    return [namespace.get(word) if word in namespace else word for word in ints]

def build_list(expr):
    # Tokenize
    toks = [ e.split(".") for e in expr.split(" ")]
    return [ replace_keywords(t) for t in toks ]

def find_attributes(items, ignore = None):
    if not ignore:
        ignore = []
    for value in items:
        if len(value) > 1:
            if value[0] not in ignore:
                for l in value[1:]: 
                    value[0] = getattr(value[0], l)
                del value[1:]

def check_env(loc, item, env=global_env):
    if callable(item):
        loc.append(item())
    else:
        try:
            op = env.find(item)[item]
            args = [loc.pop()]
            if len(loc) > 0:
                args.append(loc.pop())
            loc.append(op(*list(reversed(args))))
        except AttributeError as e:
            loc.append(item)
        except TypeError as e:
            loc.append(item)

def check_list(item_list):
    loc = []

    for item in item_list:
        check_env(loc, item[0])

    return loc[0]

def check_rule(rule_list, move, card):
    loc = []
    if type(card) == Hand:
        return any([check_rule(rule_list, move, c) for c in card])
    for l in rule_list:
        if len(l) > 1:
            if l[0] == "rules":
                if len(loc) > 0:
                    l1 = loc.pop()
                    loc.append(check_rule(l[1], move, l1))
                else:
                    loc.append(check_rule(l[1], move, card))
            if l[0] == "card":
                val = [getattr(card, l[1])]
                for j in l[2:]: 
                    val = getattr(val, j)
                loc.append(val[0])
            elif l[0] == "move":
                val = [getattr(move, l[1])]
                for j in l[2:]: 
                    val = getattr(val, j)
                loc.append(val[0])
        else: check_env(loc, l[0])
    return loc[0]

def build_piles(pile_dict):
    piles = OrderedDict()
    for p in pile_dict:
        pile = Pile(p.get('name'), p.get('facedown'))
        piles[p.get('name')] = pile

    for name, pile in piles.items():
        namespace[pile.name] = pile

    return piles.items()

def build_players(player_dict):
    players = OrderedDict()
    for p in player_dict:
        player = Player(p.get('name'))
        player.restrict(lambda self: len(self.collections) == p.get('collection_count'))
        player.hand.restrict(lambda self: len(self.hand) <= p.get('hand_size'))
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

    for key, value in rules.items():
        find_attributes(value, ["card", "move", "rules"]) 

    return rules

def build_moves(move_dict):
    def build_move(move):
        m = {key : build_list(value) for key, value in move.items()}
        for key, value in m.items():
            find_attributes(value)
        rule = Rule(m.get('how')[0][0], check_rule)
        return [m.get('where')[0][0], m.get('from')[0][0], m.get('to')[0][0], m.get('when')[0][0], rule.check]  
    return [ build_move(m) for m in move_dict ] 

def build_events(event_dict):
    def build_event(events):
        e = {key : build_list(value) for key, value in events.items()}
        for key, value in e.items():
            find_attributes(value)
        return [lambda : check_list(e.get('trigger')), lambda : doEvent(e.get('action'))]
    return [build_event(e) for e in event_dict]

def build_wins(win_dict):
    def build_win(win_condition):
        w = build_list(win_condition)
        find_attributes(w)
        return w
    return lambda self: check_list(build_win(win_dict))

def doEvent(action):
    loc = []
    for l in action:
        if callable(l[0]) and len(loc) > 0:
            l[0](*loc)
            loc = []
        else:
            loc.append(l[0])