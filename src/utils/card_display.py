#source: https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards

CARD = """\
┌─────────┐
│{}       │
│         │
│         │
│    {}   │
│         │
│         │
│       {}│
└─────────┘
""".format('{rank: <2}', '{suit: <2}', '{rank: >2}')

HIDDEN_CARD = """\
┌─────────┐
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
└─────────┘
"""

def join_lines(strings):
    """
    Stack strings horizontally.
    This doesn't keep lines aligned unless the preceding lines have the same length.
    :param strings: Strings to stack
    :return: String consisting of the horizontally stacked input
    """
    liness = [string.splitlines() for string in strings]
    return '\n'.join(''.join(lines) for lines in zip(*liness))

def ascii_version_of_card(*cards):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :return: A string, the nice ascii version of cards
    """

    # we will use this to print the appropriate icons for each card
    name_to_symbol = {
        'SPADES':   '♠',
        'DIAMONDS': '♦',
        'HEARTS':   '♥',
        'CLUBS':    '♣',
    }

    name_to_rank = {
        'ACE':   'A',
        'TWO':   '2',
        'THREE': '3',
        'FOUR':  '4',
        'FIVE':  '5',
        'SIX':   '6',
        'SEVEN': '7',
        'EIGHT': '8',
        'NINE':  '9',
        'TEN':   '10',
        'JACK':  'J',
        'QUEEN': 'Q',
        'KING':  'K',
    }

    def card_to_string(card):
        rank = name_to_rank[card.rank]
        suit = name_to_symbol[card.suit]

        # add the individual card on a line by line basis
        return CARD.format(rank=rank, suit=suit)


    return join_lines(map(card_to_string, cards))


def ascii_version_of_hidden_card(*cards):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """

    return join_lines((HIDDEN_CARD, '\n' * 9))
