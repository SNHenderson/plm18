from utils import arg_parser
from obj import collection
from dsl import game_parser
from dsl import game_builder

def main():
    # parse arguments
    # args = arg_parser.parse()

    # parse game file
    # game_rules = game_parser.parse(args.filename)

    # create game
    # game = game_builder.build_game(game_rules)
    
    game = game_builder.build_speed(None)

    #game = game_builder.build_bartok(None)

    # start game loop 
    game.run()

if __name__ == "__main__":
    main()