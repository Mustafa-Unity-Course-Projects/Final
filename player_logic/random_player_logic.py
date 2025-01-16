import random

from action import Action
from player_logic import PlayerLogic


class RandomPlayerLogic(PlayerLogic):

    def play(self, *args, **kwargs) -> Action:
        return random.choice(list(Action))
