from utils import arg_parser
from obj import collection
from obj import views
from obj.controller import Controller
from dsl import game_parser
from dsl import game_builder

def main():
    # parse arguments
    # args = arg_parser.parse()

    # parse game file
    # game_rules = game_parser.parse(args.filename)

    # create game
    # game = game_builder.build_game(game_rules)
    
    # Uncomment this line to play Speed
    #game = game_builder.build_speed(None)

    # Uncomment this line to play Bartok
    game = game_builder.build_bartok(None)
    #view = views.log_view("logs/mvctest.txt")
    view = views.pretty_view()

    # start game loop
    game_controller = Controller(game, view)
    game_controller.run()

if __name__ == "__main__":
    main()
