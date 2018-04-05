from pyparsing import Word, alphas, alphanums, oneOf, printables, delimitedList, Group
from models.player import Player
from models.game import Game
from utils.objs import dict_obj

# Converts yes/no strings to True/False
def yn_as_boolean(str):
    return True if str == 'yes' else False

# Legal values for yes/no
yn_rules = "yes | no"

# Legal digits
digits = "0 1 2 3 4 5 6 7 8 9"

# Special chars 
specials = "+ - * / > < >= <= = . ( )"

# Identifies a Player in config file
player_id = "p" + oneOf(digits) + ":"

# Properties of a Player
player = {
    "name": str,
    "hand_size": int,
    "collection_count": int
}

# Legal values for Player properties
player_prop_rules = " | ".join(list(player.keys()))

# Identifies a Pile in config file
pile_id = "pile" + oneOf(digits) + ":"

# Properties of a Pile
pile = {
    "name": str,
    "facedown": yn_as_boolean,
    "size": int,
    "owner": str
}

# Legal values for Pile properties
pile_prop_rules = " | ".join(list(pile.keys()))

# Identifies a Rule in config file
rule_id = "rule" + oneOf(digits) + ":"

# Properties of a Rule
rule = {
    "name": str,
    "expr": str
}

# Legal values for Rule properties 
rule_prop_rules = " | ".join(list(rule.keys()))

# Identifies a Move in config file
move_id = "move" + oneOf(digits) + ":"

# Properties of a Move
move = {
    "where": str,
    "from": str,
    "to": str,
    "when": str,
    "how": str
}

# Legal values for Move properties 
move_prop_rules = " | ".join(list(move.keys()))

# Identifies a Event in config file
event_id = "event" + oneOf(digits) + ":"

# Properties of a Event
event = {
    "trigger": str,
    "action": str,
    "params": str
}

# Legal values for Event properties 
event_prop_rules = " | ".join(list(event.keys()))

class GameDefinition(object):
    def __init__(self):
        self.name = ""
        self.turn_based = ""
        self.collection_count = 0
        self.win_condition = ""
        self.players = []
        self.piles = []
        self.rules = []
        self.moves = []
        self.events = []
        

def parse(filename):
    # TODO: read contents and construct a game
    file = open(filename, 'r')

    gd = GameDefinition()

    def r(f):
        return f.readline()

    def get_obj_defns(obj_list, obj_id, obj_prop_val_rule, obj_type):
        """
        Collects all the properties of an object and stores it in 
        an object, storing all such objects in obj_list
        """
        line = ""

        # Process each obj defn
        for i in range(len(obj_list)):
            line = r(file) if line == "" else line

            # Create object in right location in obj_list
            idx = int(obj_id.parseString(line)[-2])
            obj_list[idx] = {}
            line = r(file)

            # Store each k,v pair (with proper type) for the curr obj
            while line.startswith("    "):
                prop = obj_prop_val_rule.parseString(line)

                # Convert the value to the right type, store with key k
                k = prop[0]
                v = prop[-1]
                obj_list[idx][k] = obj_type[k](v)
                line = r(file)

    # Parse header info
    name_rule = "Name: " + Word(alphas)
    turn_rule = "Turn-based: " + oneOf(yn_rules)
    gd.name = name_rule.parseString(r(file)) [-1]
    gd.turn_based = yn_as_boolean(turn_rule.parseString(r(file)) [-1])

    # Skip blank line after header
    r(file)

    # Get number of players
    player_count_val_rule = "Number of players: " + Word(digits)
    player_count = int(player_count_val_rule.parseString(r(file)) [-1])
    # print("Player count: %d\n" % player_count)

    # Parse player config
    gd.players = [None] * player_count
    player_prop_val_rule = oneOf(player_prop_rules) + ": " + Word(digits + alphas)
    get_obj_defns(gd.players, player_id, player_prop_val_rule, player)
    # print(gd.players)
    # print("\n")

    # Get number of piles
    pile_count_val_rule = "Number of piles: " + Word(digits)
    pile_count = int(pile_count_val_rule.parseString(r(file)) [-1])
    # print("Pile count: %d\n" % pile_count)

    # Parse pile config
    gd.piles = [None] * pile_count
    pile_prop_val_rule = oneOf(pile_prop_rules) + ": " + Word(alphas + digits)
    get_obj_defns(gd.piles, pile_id, pile_prop_val_rule, pile)
    # print(gd.piles)
    # print("\n")

    # Get number of rules
    rule_count_val_rule = "Number of rules: " + Word(digits)
    rule_count = int(rule_count_val_rule.parseString(r(file)) [-1])
    # print("Rule count: %d\n" % rule_count)

    # Parse rule config
    gd.rules = [None] * rule_count
    rule_prop_val_rule = oneOf(rule_prop_rules) + ": " + Word(alphas + digits + specials).setParseAction(lambda t: t[0].replace('(','').replace(')', ''))
    get_obj_defns(gd.rules, rule_id, rule_prop_val_rule, rule)
    # print(gd.rules)
    # print("\n")

    # Get number of moves
    move_count_val_rule = "Number of moves: " + Word(digits)
    move_count = int(move_count_val_rule.parseString(r(file)) [-1])
    # print("Move count: %d\n" % move_count)

    # Parse move config
    gd.moves = [None] * move_count
    move_prop_val_rule = oneOf(move_prop_rules) + ": " + Word(alphas + digits + specials).setParseAction(lambda t: t[0].replace('(','').replace(')', ''))
    get_obj_defns(gd.moves, move_id, move_prop_val_rule, move)
    # print(gd.moves)

     # Get number of events
    event_count_val_rule = "Number of events: " + Word(digits)
    event_count = int(event_count_val_rule.parseString(r(file)) [-1])

    # Parse event config
    gd.events = [None] * event_count
    event_prop_val_rule = oneOf(event_prop_rules) + ": " + Word(alphas + digits + specials).setParseAction(lambda t: t[0].replace('(','').replace(')', ''))
    get_obj_defns(gd.events, event_id, event_prop_val_rule, event)

    # Get win condition
    win_cond_rule = "Win condition: " + Word(alphas + digits + specials).setParseAction(lambda t: t[0].replace('(','').replace(')', ''))
    gd.win_condition = win_cond_rule.parseString(r(file)) [-1]

    return gd