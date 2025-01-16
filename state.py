import hashlib

from pydantic import BaseModel

from card import Card


class State(BaseModel):
    playable_cards: list[Card]
    pile_sum: int
    losing: bool
    final_round: bool

    def __hash__(self):
        return int(
            hashlib.md5(
                f"{self.playable_cards}|{self.pile_sum}|{self.losing}|{self.final_round}".encode()
            ).hexdigest(),
            16
        )
