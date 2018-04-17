# Plan

## Base classes:

- Card:
    - rank: int
    - suit: str
- Deck
    - cards: list<Card>
- Pile
    - type: str ("Discard", "Draw", or "Transfer")
    - owner: str
    - Start size: int
    - Draw rule: lambda
    - cards: list<Card> (used as a stack)
- Hand
    - owner: str
    - size: int (constant size hand)
    - cards: list<Card>
- Player
    - name: str (to match with Pile owner)
    - lastPlayedCard: Card
    - score: int
    - hand: Hand

