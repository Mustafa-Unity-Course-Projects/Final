import pickle

from board import Board, CARD_PER_ROUND
from card import Card
from player import Player
from player_logic.random_player_logic import RandomPlayerLogic
from player_logic.reinforcement_player_logic import ReinforcementPlayerLogic
from train import MAX_ROUND, draw_cards, create_state, print_players

MAX_SET = 500

def play_hands() -> tuple[Player, bool]:  # Player that played the last card, Whether game is over.
    last_player = Board.players[-1]
    for player in Board.players:
        state = create_state(player)
        played_card: Card | None = player.play(state=state, playable_cards=state.playable_cards)
        print(f"{player.name } played card: {played_card}")
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

    print(f"Round won by {player_that_won.name}")

    round_score = sum(card.value for card in Board.pile)
    for player in Board.players:
        if player == player_that_won:
            player.score += round_score
    Board.round += 1
    Board.players = list(reversed(Board.players))


def execute_set():
    Board.round = 0
    for round_index in range(MAX_ROUND):
        execute_round()

    winner: Player = max(Board.players, key=lambda x: x.score)
    Board.player_to_win_count[winner] += 1
    print(f"{winner.name} won the set.")
    for player in Board.players: player.score = 0


def main():
    reinforcement_player = Player(name="player-reinforcement", logic=ReinforcementPlayerLogic(learning_rate=0, exploration_rate=0))
    with open("trained_vals.pkl", "rb") as f:
        reinforcement_player.logic.state_action_q_map = pickle.load(f)
    print("Model loaded successfully.")
    players: list[Player] = [
        reinforcement_player,
        Player(name="player-random", logic=RandomPlayerLogic()),
    ]
    Board.players = players
    for player in players:
        Board.player_to_win_count[player] = 0

    for _ in range(MAX_SET):
        execute_set()

    print_players(players)
    print({player.name: val for player, val in Board.player_to_win_count.items()})

if __name__ == '__main__':
    main()