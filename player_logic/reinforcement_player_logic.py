import random
from collections import defaultdict

from action import Action
from player_logic import PlayerLogic
from state import State


class ReinforcementPlayerLogic(PlayerLogic):
    state_action_q_map: defaultdict[State, list[tuple[Action, float]]]
    states_and_actions_this_round: list[tuple[State, Action]]
    learning_rate: float  # [0, 1]
    exploration_rate: float  # [0, 1]

    def init_state_action_q_map(self):
        def create_action_q_tuples() -> list[tuple[Action, float]]:
            return [(action, 0.0) for action in Action]
        self.state_action_q_map = defaultdict(create_action_q_tuples)

    def __init__(self, learning_rate: float = 0.7, exploration_rate: float = 0.5):
        self.init_state_action_q_map()
        self.states_and_actions_this_round = []
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate

    def play(self, state: State) -> Action:
        action_and_qs: list[tuple[Action, float]] = self.state_action_q_map.get(state) or []

        if not action_and_qs:
            action = random.choice([Action.CHAIN, Action.FOLD, Action.MAX])
            state_action = state, action
        else:
            state_action: tuple[State, Action]
            if random.uniform(0, 1) < self.exploration_rate:
                action, _ = random.choice(action_and_qs)
                state_action = state, action
            else:
                _, max_q = max(action_and_qs, key=lambda x: x[1])
                possible_actions = [action for action, q in action_and_qs if q == max_q]
                state_action = state, random.choice(possible_actions)

        self.states_and_actions_this_round.append(state_action)
        return state_action[1]


    def reward(self, reward: float):
        for state, action in self.states_and_actions_this_round:
            actions_and_qs: list[tuple[Action, float]] = self.state_action_q_map[state]
            q = next(q for act, q in actions_and_qs if act == action)
            new_q = (1 - self.learning_rate) * q + self.learning_rate * reward
            actions_and_qs.remove((action, q))
            actions_and_qs.append((action, new_q))

        self.states_and_actions_this_round = []
