from pydantic import BaseModel, Field

from action import Action
from card import Card
from player_logic import PlayerLogic
from state import State


class Player:
    name: str
    hand: list[Card]
    score: int = 0
    logic: PlayerLogic

    def play(self, playable_cards: list[Card],  state: State) -> Card | None:
        if not playable_cards:
            return None

        action = self.logic.play(state)

        if action == Action.FOLD:
            return None
        elif action == Action.CHAIN:
            return min(playable_cards, key=lambda x: x.value)
        else:
            return max(playable_cards, key=lambda x: x.value)

    def pass_reward(self, reward: float):
        self.logic.reward(reward)

    def __hash__(self):
        return hash(self.name)

    def __init__(self, name: str, logic: PlayerLogic):
        self.name = name
        self.logic = logic

