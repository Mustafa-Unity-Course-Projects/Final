import hashlib
from enum import StrEnum
from pydantic import BaseModel


class Suit(StrEnum):
    HEARTS = "hearts"
    SPADES = "spades"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"

    def __lt__(self, other):
        val_map = {
            self.HEARTS: 1,
            self.SPADES: 2,
            self.DIAMONDS: 3,
            self.CLUBS: 4,
        }
        return val_map[self] < val_map[other]


class Rank(StrEnum):
    ACE = "ace"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"
    SIX = "six"
    SEVEN = "seven"
    EIGHT = "eight"
    NINE = "nine"
    TEN = "ten"
    JACK = "jack"
    QUEEN = "queen"
    KING = "king"

    @property
    def val(self) -> int:
        return {
            self.ACE: 1,
            self.TWO: 2,
            self.THREE: 3,
            self.FOUR: 4,
            self.FIVE: 5,
            self.SIX: 6,
            self.SEVEN: 7,
            self.EIGHT: 8,
            self.NINE: 9,
            self.TEN: 10,
            self.JACK: 11,
            self.QUEEN: 12,
            self.KING: 13,
        }[self]

    def __lt__(self, other):
        return self.val < other.val


class Card(BaseModel):
    suit: Suit
    rank: Rank

    def __hash__(self):
        return int(hashlib.md5(self.__repr__().encode()).hexdigest(), 16) % (10 ** 8)

    def __repr__(self):
        return f"{self.suit}|{self.rank}"

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        if self.val != other.val:
            return self.val < other.val
        return self.rank < other.rank

    @property
    def value(self):
        return self.rank.val


