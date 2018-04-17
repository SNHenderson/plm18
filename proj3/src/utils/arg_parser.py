import argparse

def parse():
    parser = argparse.ArgumentParser(description="Parse and play card games.")
    parser.add_argument("game", help="the name of the game")
    parser.add_argument("--log", nargs="?", const="output.txt", metavar="FILENAME", help="logs the output of the game")
    parser.add_argument('--debug', dest='debug', action='store_true', help="starts the game in debug mode")
    parser.set_defaults(debug=False)

    return parser.parse_args()
