from control.controller import Controller
from dsl import game_builder
from dsl import game_parser
from models import collection
from utils import arg_parser
from views.log import LogView
from views.pretty import PrettyView

def run():
    # parse arguments
    #args = arg_parser.parse()

    # parse game file
    game_rules = game_parser.parse(args.game)
    game_parser.parse("games/bartok2.txt")

    # create game
    # game = game_builder.build_game(game_rules)
    
    # if args.game == "bartok":
    #     game = game_builder.build_bartok(None)
    # elif args.game == "speed":
    #     game = game_builder.build_speed(None)

    # view = LogView(args.log) if args.log else PrettyView()
    # # Uncomment this line to play Speed
    # #game = game_builder.build_speed(None)

    # # Uncomment this line to play Bartok
    # #game = game_builder.build_bartok(None)

    # # start game loop 
    # #game.run()

    # # start game loop
    # game_controller = Controller(game, view)
    # game_controller.run()

run()