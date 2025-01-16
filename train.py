import json

from board import Board, CARD_PER_ROUND
from card import Card
from player import Player
from player_logic.random_player_logic import RandomPlayerLogic
from player_logic.reinforcement_player_logic import ReinforcementPlayerLogic
from state import State

MAX_ROUND = 5
MAX_SET = 1000000


def print_players(players: list[Player]):
    for player in players:
        print(player.__dict__)


def get_playable_cards(hand: list[Card]) -> list[Card]:
    if Board.top_of_pile:
        return [card for card in hand if card.value > Board.top_of_pile.value]
    return hand


def create_state(player: Player) -> State:
    state: State = State(
        playable_cards=get_playable_cards(player.hand),
        pile_sum=sum(i.value for i in Board.pile),
        losing=player.score != max(p.score for p in Board.players),
        final_round=Board.round == MAX_ROUND,
    )
    return state

def draw_cards():
    for player in Board.players:
        player.hand = Board.deck[:5]
        Board.deck = Board.deck[5:]


def play_hands() -> tuple[Player, bool]:  # Player that played the last card, Whether game is over.
    last_player = Board.players[-1]
    for player in Board.players:
        state = create_state(player)
        played_card: Card | None = player.play(state=state, playable_cards=state.playable_cards)
        if played_card is None:
            return last_player, True
        else:
            last_player = player
            Board.pile.append(played_card)

    return last_player, False

def execute_round():
    Board.refresh()
    draw_cards()
    player_that_won: Player = None
    for _ in range(CARD_PER_ROUND):
        player_that_won, end_round = play_hands()
        if end_round:
            break

    if player_that_won is None:
        raise Exception("Fatal error: Player that won is None")

    round_score = sum(card.value for card in Board.pile)
    for player in Board.players:
        if player == player_that_won:
            player.score += round_score
            player.pass_reward(round_score)
        else:
            player.pass_reward(-round_score)

    Board.round += 1
    Board.players = list(reversed(Board.players))


def execute_set():
    Board.round = 0
    for round_index in range(MAX_ROUND):
        execute_round()

    winner: Player = max(Board.players, key=lambda x: x.score)
    Board.player_to_win_count[winner] += 1
    for player in Board.players: player.score = 0


def main():
    players: list[Player] = [
        Player(name="player-1", logic=ReinforcementPlayerLogic()),
        Player(name="player-2", logic=RandomPlayerLogic()),
    ]
    reinforcement_player = next(p for p in players if isinstance(p.logic, ReinforcementPlayerLogic))
    Board.players = players
    for player in players:
        Board.player_to_win_count[player] = 0

    for _ in range(MAX_SET):
        execute_set()

    print_players(players)
    winrate = Board.player_to_win_count[reinforcement_player] / sum(Board.player_to_win_count.values())
    print(winrate)

    for player in players:
        player.score = 0
        Board.player_to_win_count[player] = 0

    reinforcement_player.logic.learning_rate = 0
    reinforcement_player.logic.exploration_rate = 0
    for _ in range(MAX_SET):
        execute_set()

    print_players(players)
    winrate = Board.player_to_win_count[reinforcement_player] / sum(Board.player_to_win_count.values())
    print(winrate)

    import pickle
    with open("trained_vals.pkl", "wb") as f:
        pickle.dump(dict(reinforcement_player.logic.state_action_q_map), f)


if __name__ == "__main__":
    main()
