import random
from functools import lru_cache

from card import Card, Rank, Suit
from player import Player

CARD_PER_ROUND = 3

class GameBoard:
    players: list[Player]
    pile: list[Card]
    deck: list[Card]
    round: int
    player_to_win_count: dict[Player, int] = {}

    @staticmethod
    @lru_cache()
    def create_deck() -> list[Card]:
        return [
            Card(suit=suit, rank=rank)
            for suit in Suit
            for rank in Rank
        ]

    def init_deck(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)

    @property
    def top_of_pile(self) -> Card | None:
        return self.pile[-1] if self.pile else None

    def refresh(self):
        self.round += 1
        self.init_deck()
        self.pile = []
        for player in self.players:
            player.hand = []

    def __init__(self):
        self.players = []
        self.pile = []
        self.init_deck()
        self.round = 0



Board = GameBoard()
