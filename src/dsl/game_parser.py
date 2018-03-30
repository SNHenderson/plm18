from pyparsing import Word, alphas, oneOf
from models.player import Player
from models.game import Game

# Converts yes/no strings to True/False
def yn_as_boolean(str):
    return True if str == 'yes' else False

# Legal values for yes/no
yn_rules = "yes | no"

# Legal digits
digits = "0 1 2 3 4 5 6 7 8 9"

# Identifies a Player in config file
player_id = "p" + oneOf(digits) + ":"

# Properties of a Player
player = {
    "name": str,
    "hand.size": int
}

# Legal values for Player properties
player_prop_rules = " | ".join(list(player.keys()))

# Identifies a Ple in config file
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

class GameDefinition(object):
    pass


def parse(filename):
    # TODO: read contents and construct a game
    file = open(filename, 'r')

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
    name = name_rule.parseString(r(file)) [-1]
    turn_based = yn_as_boolean(turn_rule.parseString(r(file)) [-1])

    # Skip blank line after header
    r(file)

    # Get number of players
    player_count_val_rule = "Number of players: " + Word(digits)
    player_count = int(player_count_val_rule.parseString(r(file)) [-1])
    print("Player count: %d\n" % player_count)

    # Parse player config
    player_defs = [None] * player_count
    player_prop_val_rule = oneOf(player_prop_rules) + ": " + Word(digits + alphas)
    get_obj_defns(player_defs, player_id, player_prop_val_rule, player)
    print(player_defs)

    # Get number of piles
    pile_count_val_rule = "Number of piles: " + Word(digits)
    pile_count = int(pile_count_val_rule.parseString(r(file)) [-1])
    print("Pile count: %d\n" % pile_count)

    # Parse pile config
    pile_defs = [None] * pile_count
    pile_prop_val_rule = oneOf(pile_prop_rules) + ": " + Word(alphas + digits)
    get_obj_defns(pile_defs, pile_id, pile_prop_val_rule, pile)
    print(pile_defs)