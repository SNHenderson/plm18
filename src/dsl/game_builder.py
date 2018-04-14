from models.game import Game
from models.moves import Move
from models.events import Event
from dsl.environment import global_env
from dsl import utils


def build_game(game_data):
    game = Game(game_data.name, game_data.turn_based)

    # Create and register players
    players = utils.build_players(game_data.players, game_data.player_hand_size, game_data.player_collections)
    [ game.add_player(player) for name, player in players ]

    # Create and register piles
    piles = utils.build_piles(game_data.piles)

    # Shuffle the cards
    cards = game.deck.shuffled()

    # Set the collections
    collections = [player.hand for name, player in players]
    collections += [pile for name, pile in piles]

    # Set the card count
    counts = [game_data.player_hand_size for player in game_data.players]
    counts += [pile.get('size') for pile in game_data.piles]

    # Register collections with the game
    [ game.add_collection(c) for c in collections ]

    # Build rules to be used for moves. This adds them to the namespace
    utils.build_rules(game_data.rules)

    # Build and add moves
    [ game.add_move(m) for m in utils.build_moves(game_data.moves) ]

    # Build and add events
    [ game.add_event(e) for e in utils.build_events(game_data.events) ]

    # Build and add the win condition
    game.add_win_condition(utils.build_win_condition(game_data.win_condition))

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))

    # Allow access to game properties from rules
    global_env.update(game.__dict__)

    return game

