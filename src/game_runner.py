from control.controller import Controller
from dsl import game_builder
from dsl import game_parser
from models import collection
from utils import arg_parser
from views.view import View
from views.log import LogView
from views.pretty import PrettyView

def run():
    # parse arguments
    args = arg_parser.parse()

    # parse game file
    game_rules = game_parser.parse(args.game)

    # create game
    game = game_builder.build_game(game_rules)
    
    view = LogView(args.log) if args.log else PrettyView()

    # start game loop
    game_controller = Controller(game, view)
    game_controller.run()

if __name__ == "__main__":
    run()