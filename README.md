# plm18 GROUP H

Hall,Connor

Kayani,Joshua

Henderson,Samuel

Link: https://github.com/SNHenderson/plm18/tree/master

## Installation

This project uses several Python libraries that need to be installed

### Dependencies:
- pyparsing

After cloning this repo, these can be installed via `pip install -r requirements.txt` using the requirements.txt file in the root.

## Running

### Speed

Start a game with: `bin/cards games/speed.txt`. To generate a transcript of gameplay, use: `bin/cards --log <filename> games/speed.txt`. The transcript is written to `logs/<filename>`.

**Controls**
- `q` for player 1 to discard to first discard pile
- `w` for player 1 to discard to second discard pile
- `e` for player 1 to draw a card
- `i` for player 2 to discard to first discard pile
- `p` for player 2 to discard to second discard pile
- `o` for player 2 to draw a card
- `b` for replacing the top-most cards on the discard piles with those from the replace piles

### Bartok

Start a game with: `bin/cards games/bartok.txt`. To generate a transcript of gameplay, use: `bin/cards --log <filename> games/bartok.txt`. The transcript is written to `logs/<filename>`.

**Controls**
- `q` for player 1 to discard a card
- `e` for player 1 to draw a card
- `i` for player 2 to discard a card
- `p` for player 2 to draw a card
- `z` for player 3 to discard a card
- `c` for player 3 to draw a card
- `b` for player 4 to discard a card
- `m` for player 4 to draw a card

## Samples
Sample transcripts for both games can be found in the `docs/samples` folder. The game config files can be in found `games`.



