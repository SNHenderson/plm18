from pyparsing import Word, OneOrMore, ZeroOrMore, Or, Literal
from pyparsing import oneOf, delimitedList
from pyparsing import alphas, alphanums, nums, printables
from models.player import Player
from models.game import Game

# Converts yes/no strings to True/False
def string_to_bool(string):
    val = { "yes": True, "no": False }.get(string);
    if val is None:
        raise ValueError
    return val

def props_for(obj):
    return obj.keys()

def KeyValue(key_type, val_type):
    if type(key_type) is str:
        key_type = Literal(key_type)
    if type(val_type) is str:
        val_type = Literal(val_type)
    key_type = key_type.setResultsName("key")
    val_type = val_type.setResultsName("value")

    return key_type + ":" + val_type

YesNo = oneOf("yes no") \
            .setName("YesNo") \
            .addParseAction(lambda toks: string_to_bool(toks[0]))

Name = Word(alphanums) \
            .setName("Name") \
            .addParseAction(lambda toks: toks[0])

Number = Word(nums) \
            .setName("Number") \
            .addParseAction(lambda toks: int(toks[0]))

KeyboardChar = Word(printables) \
            .setName("KeyboardChar")

Identifier = Word(alphanums + "_") \
            .setName("Identifier");

Operator = oneOf("+ - * / > < >= <= = . ( ) 's")
Expression = OneOrMore(Operator | Identifier) \
                .setName("Expression") \
                .addParseAction(lambda toks: " ".join(toks))

Iteration = Identifier + "<-" + Expression
Binding = Identifier + "=" + Expression
Assignment = Or(Iteration | Binding) \
                .setName("Assignment") \
                .addParseAction(lambda toks: [toks])

# Environment = Or(delimitedList(Assignment), "None") \
Environment = (delimitedList(Assignment) | "None") \
                .setName("Environment") \
                .addParseAction(lambda toks: [toks] )


# Properties of a Player
player = {}

# Properties of a Pile
pile = {
    "facedown": YesNo,
    "size": Number,
    "owner": Identifier
}

# Properties of a Rule
rule = {
    "expr": Expression,
    "where": Environment
}

# Properties of a Move
move = {
    "where": Expression,
    "from": Expression,
    "to": Expression,
    "trigger": KeyboardChar,
    "how": Expression
}

# Properties of a Event
event = {
    "trigger": Expression,
    "action": Expression
}

class GameDefinition(object):
    def __init__(self):
        self.name = ""
        self.turn_based = ""
        self.collection_count = 0
        self.win_condition = ""
        self.player_hand_size = 0
        self.player_collections = 0
        self.players = []
        self.piles = []
        self.rules = []
        self.moves = []
        self.events = []


def parse(filename):
    with open(filename) as f:
        def line():
            """ Returns the next non-empty line in file f """
            ln = f.readline()
            return line() if ln.isspace() else ln

        def parse_line(rule):
            # return rule.parseString(line())
            ln = line()
            return rule.parseString(ln)

        def parse_obj_defn(obj_type):
            """
            Collects all the properties of an object and stores it in an object
            """
            obj = {}
            props = props_for(obj_type)
            prop_rule = Or([ KeyValue(p, obj_type[p]) for p in props ])

            # Get the name of the object
            obj["name"] = parse_line(Name)[0]

            for _ in props:
                # Convert the value to the right type, store with key k
                # (k, _, v) = parse_line(prop_rule)
                val =  parse_line(prop_rule)
                (k, _, v) = val
                obj[k] = v
            return obj

        def get_obj_defns(obj_type, count, ):
            return [parse_obj_defn(obj_type) for _ in range(count)]

        def get_number(prompt):
            prompt_rule = KeyValue(prompt, Number)
            return parse_line(prompt_rule).value

        gd = GameDefinition()

        # Parse header info
        gd.name = parse_line(KeyValue("Name", Name)).value
        gd.turn_based = parse_line(KeyValue("Turn-based", YesNo)).value

        # Get number of players
        player_count = get_number("Number of players")

        # Get player hand sizes
        gd.player_hand_size = get_number("Player hand size")

        # Get player collection count
        gd.player_collections = get_number("Player collections")

        # Parse player config
        gd.players = get_obj_defns(player, player_count)

        # Get number of piles
        pile_count = get_number("Number of piles")

        # Parse pile config
        gd.piles = get_obj_defns(pile, pile_count)

        # Get number of rules
        rule_count = get_number("Number of rules")

        # Parse rule config
        gd.rules = get_obj_defns(rule, rule_count)

        # Get number of moves
        move_count = get_number("Number of moves")

        # Parse move config
        gd.moves = get_obj_defns(move, move_count)

         # Get number of events
        event_count = get_number("Number of events")

        # Parse event config
        gd.events = get_obj_defns(event, event_count)

        # Get win condition
        gd.win_condition = parse_line(KeyValue("Win condition", Expression)).value

        return gd
