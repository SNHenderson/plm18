import argparse

def parse():
    parser = argparse.ArgumentParser(description="Parse and play card games.")
    parser.add_argument("game", help="the name of the game")
    parser.add_argument("--log", nargs="?", const="output.txt", metavar="FILENAME", help="starts the game in log mode")

    return parser.parse_args()
