"""
RoboPlan - Module C
Game Playing: Dock Contention

Algorithms:
1. MiniMax
2. Alpha-Beta Pruning
3. Iterative Deepening
4. Move Ordering
5. Node-count comparison chart
"""

import argparse
import time
import random
import matplotlib.pyplot as plt


# ============================================================
# GAME
# ============================================================

class DockGame:
    """
    Small adversarial resource game.

    There are 10 charging units remaining.
    Each robot can claim 1, 2, or 3 units.

    The robot that takes the final unit wins.

    Branching factor = 3.
    """

    def __init__(self, remaining=10):
        self.remaining = remaining

    def legal_moves(self):
        return [
            move
            for move in [1, 2, 3]
            if move <= self.remaining
        ]

    def make_move(self, move):
        return DockGame(self.remaining - move)

    def terminal(self):
        return self.remaining == 0


# ============================================================
# MINI MAX
# ============================================================

def minimax(game, depth, maximizing, counter):
    """
    Plain MiniMax.
    """

    counter[0] += 1

    # Terminal state
    if game.terminal():
        if maximizing:
            return -1000
        else:
            return 1000

    # Depth limit reached
    if depth == 0:
        return evaluate(game)

    moves = game.legal_moves()

    if maximizing:

        best_value = float("-inf")

        for move in moves:

            child = game.make_move(move)

            value = minimax(
                child,
                depth - 1,
                False,
                counter
            )

            best_value = max(
                best_value,
                value
            )

        return best_value

    else:

        best_value = float("inf")

        for move in moves:

            child = game.make_move(move)

            value = minimax(
                child,
                depth - 1,
                True,
                counter
            )

            best_value = min(
                best_value,
                value
            )

        return best_value


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate(game):
    """
    Simple heuristic.

    Winning positions are preferred.
    """

    if game.remaining == 0:
        return -1000

    # Favor states where opponent has limited choices
    return -game.remaining


# ============================================================
# ALPHA-BETA
# ============================================================

def alpha_beta(
    game,
    depth,
    alpha,
    beta,
    maximizing,
    counter,
    move_ordering=False
):
    """
    Alpha-Beta pruning.
    """

    counter[0] += 1

    if game.terminal():

        if maximizing:
            return -1000
        else:
            return 1000

    if depth == 0:
        return evaluate(game)

    moves = game.legal_moves()

    # Move ordering:
    # try larger moves first because they often
    # lead to better tactical positions.
    if move_ordering:
        moves = sorted(
            moves,
            reverse=True
        )

    if maximizing:

        value = float("-inf")

        for move in moves:

            child = game.make_move(move)

            value = max(
                value,
                alpha_beta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    counter,
                    move_ordering
                )
            )

            alpha = max(
                alpha,
                value
            )

            if alpha >= beta:
                break

        return value

    else:

        value = float("inf")

        for move in moves:

            child = game.make_move(move)

            value = min(
                value,
                alpha_beta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                    counter,
                    move_ordering
                )
            )

            beta = min(
                beta,
                value
            )

            if alpha >= beta:
                break

        return value


# ============================================================
# BEST MOVE
# ============================================================

def choose_minimax_move(game, depth):

    best_move = None
    best_value = float("-inf")

    counter = [0]

    for move in game.legal_moves():

        child = game.make_move(move)

        value = minimax(
            child,
            depth - 1,
            False,
            counter
        )

        if value > best_value:

            best_value = value
            best_move = move

    return best_move, best_value, counter[0]


def choose_alpha_beta_move(
    game,
    depth,
    move_ordering=False
):

    best_move = None
    best_value = float("-inf")

    counter = [0]

    moves = game.legal_moves()

    if move_ordering:
        moves = sorted(
            moves,
            reverse=True
        )

    for move in moves:

        child = game.make_move(move)

        value = alpha_beta(
            child,
            depth - 1,
            float("-inf"),
            float("inf"),
            False,
            counter,
            move_ordering
        )

        if value > best_value:

            best_value = value
            best_move = move

    return best_move, best_value, counter[0]


# ============================================================
# ITERATIVE DEEPENING
# ============================================================

def iterative_deepening(game, maximum_depth):

    print("\n" + "=" * 70)
    print("ITERATIVE DEEPENING")
    print("=" * 70)

    final_move = None

    for depth in range(1, maximum_depth + 1):

        start_time = time.perf_counter()

        move, value, nodes = choose_alpha_beta_move(
            game,
            depth,
            move_ordering=True
        )

        elapsed = (
            time.perf_counter()
            - start_time
        )

        final_move = move

        print(
            f"Depth {depth}: "
            f"Move={move}, "
            f"Value={value}, "
            f"Nodes={nodes}, "
            f"Time={elapsed:.6f}s"
        )

    return final_move


# ============================================================
# NODE COMPARISON
# ============================================================

def compare_algorithms():

    depths = range(2, 7)

    minimax_nodes = []
    alpha_beta_nodes = []
    ids_nodes = []

    print("\n" + "=" * 70)
    print("NODE COUNT COMPARISON")
    print("=" * 70)

    print(
        f"{'Depth':<10}"
        f"{'MiniMax':<15}"
        f"{'Alpha-Beta':<15}"
        f"{'AB + IDS':<15}"
    )

    for depth in depths:

        game = DockGame(10)

        # MiniMax
        _, _, mm_nodes = choose_minimax_move(
            game,
            depth
        )

        # Alpha-Beta
        _, _, ab_nodes = choose_alpha_beta_move(
            game,
            depth,
            move_ordering=False
        )

        # Alpha-Beta + Move Ordering
        _, _, ids_nodes_count = choose_alpha_beta_move(
            game,
            depth,
            move_ordering=True
        )

        minimax_nodes.append(
            mm_nodes
        )

        alpha_beta_nodes.append(
            ab_nodes
        )

        ids_nodes.append(
            ids_nodes_count
        )

        print(
            f"{depth:<10}"
            f"{mm_nodes:<15}"
            f"{ab_nodes:<15}"
            f"{ids_nodes_count:<15}"
        )

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        list(depths),
        minimax_nodes,
        marker="o",
        label="MiniMax"
    )

    plt.plot(
        list(depths),
        alpha_beta_nodes,
        marker="o",
        label="Alpha-Beta"
    )

    plt.plot(
        list(depths),
        ids_nodes,
        marker="o",
        label="Alpha-Beta + IDS"
    )

    plt.xlabel(
        "Depth"
    )

    plt.ylabel(
        "Nodes Explored"
    )

    plt.title(
        "MiniMax vs Alpha-Beta vs Alpha-Beta + IDS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        "node_comparison.png",
        dpi=150
    )

    print(
        "\nChart saved as: node_comparison.png"
    )


# ============================================================
# PLAY GAME
# ============================================================

def play_game(depth):

    print("\n" + "=" * 70)
    print("DOCK CONTENTION GAME")
    print("=" * 70)

    game = DockGame(10)

    print(
        "\nThere are 10 charging units."
    )

    print(
        "On each turn, a robot can claim "
        "1, 2, or 3 units."
    )

    print(
        "The robot taking the final unit wins."
    )

    print(
        "\nYou are Robot B."
    )

    print(
        "The AI is Robot A."
    )

    while not game.terminal():

        # ----------------------------------------------------
        # AI MOVE
        # ----------------------------------------------------

        ai_move, value, nodes = choose_alpha_beta_move(
            game,
            depth,
            move_ordering=True
        )

        print(
            f"\nAI chooses: {ai_move}"
        )

        print(
            f"Nodes explored: {nodes}"
        )

        game = game.make_move(
            ai_move
        )

        print(
            f"Units remaining: "
            f"{game.remaining}"
        )

        if game.terminal():

            print(
                "\nAI Robot wins the charging dock!"
            )

            return

        # ----------------------------------------------------
        # HUMAN MOVE
        # ----------------------------------------------------

        while True:

            try:

                move = int(
                    input(
                        "\nYour move (1/2/3): "
                    )
                )

                if move in game.legal_moves():
                    break

                print(
                    "Invalid move."
                )

            except ValueError:

                print(
                    "Please enter 1, 2, or 3."
                )

        game = game.make_move(
            move
        )

        print(
            f"Units remaining: "
            f"{game.remaining}"
        )

        if game.terminal():

            print(
                "\nYou win the charging dock!"
            )

            return


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="RoboPlan Dock Contention Game"
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=5,
        help="Search depth"
    )

    parser.add_argument(
        "--play",
        action="store_true",
        help="Play against the AI"
    )

    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare node counts"
    )

    args = parser.parse_args()

    print("\n")
    print("=" * 70)
    print("ROBO PLAN - MODULE C")
    print("GAME PLAYING: DOCK CONTENTION")
    print("=" * 70)

    if args.compare:

        compare_algorithms()

    elif args.play:

        play_game(
            args.depth
        )

    else:

        game = DockGame(10)

        print(
            "\nRunning Alpha-Beta AI..."
        )

        move, value, nodes = choose_alpha_beta_move(
            game,
            args.depth,
            move_ordering=True
        )

        print(
            f"Best move: {move}"
        )

        print(
            f"Evaluation: {value}"
        )

        print(
            f"Nodes explored: {nodes}"
        )

        print(
            "\nRunning Iterative Deepening..."
        )

        iterative_deepening(
            game,
            args.depth
        )


if __name__ == "__main__":
    main()