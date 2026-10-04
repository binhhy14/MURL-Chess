"""
MCTS for the MURL chess project.

The search is Monte Carlo Tree Search, not full-width Minimax.

Main improvements for tactical chess positions:
1. UCT selection with opponent-aware exploitation.
2. Tactical rollout policy:
   checkmate -> promotion -> check -> capture -> safe move -> random move.
3. Rollouts avoid obvious one-move checkmates when possible.
4. Terminal checkmate gets the strongest possible reward.
5. Non-terminal leaf positions use a small material/check heuristic.
6. Move ordering expands tactical moves early.
7. Exact forced-mate search is kept separate and is used ONLY to evaluate
   whether the MCTS result was correct.

References:
- Browne et al. (2012), "A Survey of Monte Carlo Tree Search Methods"
- Kocsis and Szepesvári (2006), "Bandit Based Monte-Carlo Planning"
- python-chess documentation: https://python-chess.readthedocs.io/
- No external MCTS implementation was copied.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional

import chess


WHITE_WIN = 1.0
DRAW = 0.0
BLACK_WIN = -1.0

PIECE_VALUES = {
    chess.PAWN: 1.0,
    chess.KNIGHT: 3.0,
    chess.BISHOP: 3.0,
    chess.ROOK: 5.0,
    chess.QUEEN: 9.0,
    chess.KING: 0.0,
}


def material_score(board: chess.Board) -> float:
    """Positive means White has more material."""
    score = 0.0

    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    return score


def immediate_checkmate(board: chess.Board) -> Optional[chess.Move]:
    """Return a move that checkmates immediately, if one exists."""
    for move in board.legal_moves:
        board.push(move)
        is_mate = board.is_checkmate()
        board.pop()

        if is_mate:
            return move

    return None


def move_priority(board: chess.Board, move: chess.Move) -> float:
    """
    Tactical ordering score.

    This does NOT decide the final move. It only makes MCTS examine
    promising tactical moves earlier.
    """
    score = 0.0

    # Promotions are very important in the supplied test positions.
    if move.promotion is not None:
        score += 1000.0

    # Captures deserve early attention.
    if board.is_capture(move):
        score += 100.0

        captured_piece = board.piece_at(move.to_square)
        if captured_piece is not None:
            score += PIECE_VALUES[captured_piece.piece_type] * 10.0

    # Checks are usually critical in mate problems.
    if board.gives_check(move):
        score += 300.0

    # Prefer moves that immediately win material.
    piece = board.piece_at(move.from_square)
    if piece is not None:
        score += PIECE_VALUES[piece.piece_type] * 0.01

    return score


def ordered_moves(board: chess.Board) -> list[chess.Move]:
    """Return legal moves with tactical moves first."""
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: move_priority(board, m), reverse=True)
    return moves


def has_immediate_mate(board: chess.Board) -> bool:
    return immediate_checkmate(board) is not None


def choose_rollout_move(
    board: chess.Board,
    rng: random.Random,
) -> chess.Move:
    """
    Tactical rollout policy.

    Instead of choosing every move uniformly at random:
      1. take mate in one if available;
      2. prefer promotions;
      3. prefer checks;
      4. prefer captures;
      5. avoid moves that allow an immediate opponent mate when possible;
      6. otherwise choose randomly from a small weighted candidate set.
    """
    legal_moves = list(board.legal_moves)

    # 1. Never miss a mate in one.
    mate_move = immediate_checkmate(board)
    if mate_move is not None:
        return mate_move

    # Classify moves.
    tactical = []
    safe_moves = []

    for move in legal_moves:
        board.push(move)

        # If this move allows the opponent to mate immediately,
        # mark it as dangerous.
        opponent_can_mate = has_immediate_mate(board)

        board.pop()

        if not opponent_can_mate:
            safe_moves.append(move)

        if (
            move.promotion is not None
            or board.gives_check(move)
            or board.is_capture(move)
        ):
            if not opponent_can_mate:
                tactical.append(move)

    # 2-4. Prefer safe tactical moves.
    if tactical:
        return max(
            tactical,
            key=lambda m: move_priority(board, m) + rng.random() * 5.0,
        )

    # 5. If safe moves exist, sample from them.
    if safe_moves:
        return rng.choice(safe_moves)

    # 6. Every move is tactically dangerous, so sample legally.
    return rng.choice(legal_moves)


def heuristic_value(
    board: chess.Board,
    root_color: chess.Color,
) -> float:
    """
    Small leaf evaluation in [-1, 1].

    MCTS still receives +1/-1 for actual checkmate.
    This heuristic only gives useful information when a simulation
    reaches the depth limit without checkmate.
    """
    if board.is_checkmate():
        winner = not board.turn
        return WHITE_WIN if winner == chess.WHITE else BLACK_WIN

    if board.is_stalemate() or board.is_insufficient_material():
        return DRAW

    score = material_score(board)

    # Normalize material so the value stays in a compact range.
    value = max(-0.9, min(0.9, score / 20.0))

    # Give a small bonus to the side giving check.
    if board.is_check():
        checking_side = not board.turn
        value += 0.08 if checking_side == chess.WHITE else -0.08

    value = max(-1.0, min(1.0, value))

    if root_color == chess.WHITE:
        return value

    return -value


def simulation_result(
    board: chess.Board,
    root_color: chess.Color,
    max_plies: int,
    rng: random.Random,
) -> float:
    """
    Play one rollout from the expanded node.

    The root player's perspective is used for the returned reward.
    """
    for _ in range(max_plies):
        if board.is_game_over():
            break

        move = choose_rollout_move(board, rng)
        board.push(move)

    if board.is_checkmate():
        winner = not board.turn
        return WHITE_WIN if winner == root_color else BLACK_WIN

    if board.is_stalemate() or board.is_insufficient_material():
        return DRAW

    return heuristic_value(board, root_color)


@dataclass
class ChessSearchNode:
    board: chess.Board
    parent: Optional["ChessSearchNode"] = None
    move: Optional[chess.Move] = None
    root_color: chess.Color = chess.WHITE
    untried_moves: list[chess.Move] = field(default_factory=list)
    children: list["ChessSearchNode"] = field(default_factory=list)
    visits: int = 0
    total_reward: float = 0.0

    def __post_init__(self) -> None:
        if not self.untried_moves:
            self.untried_moves = ordered_moves(self.board)

    @property
    def mean_reward(self) -> float:
        if self.visits == 0:
            return 0.0
        return self.total_reward / self.visits


def uct_value(
    parent: ChessSearchNode,
    child: ChessSearchNode,
    exploration: float = math.sqrt(2.0),
) -> float:
    """Opponent-aware UCT value."""
    if child.visits == 0:
        return float("inf")

    exploitation = child.mean_reward

    # At White/root-player nodes, maximize root reward.
    # At the opponent's nodes, minimize root reward.
    if parent.board.turn != parent.root_color:
        exploitation = -exploitation

    exploration_term = exploration * math.sqrt(
        math.log(max(1, parent.visits)) / child.visits
    )

    return exploitation + exploration_term


def select_child(node: ChessSearchNode) -> ChessSearchNode:
    """Select the child with the highest opponent-aware UCT score."""
    return max(node.children, key=lambda child: uct_value(node, child))


def expand_node(node: ChessSearchNode) -> ChessSearchNode:
    """Expand one previously unexpanded legal move."""
    move = node.untried_moves.pop(0)

    next_board = node.board.copy(stack=False)
    next_board.push(move)

    child = ChessSearchNode(
        board=next_board,
        parent=node,
        move=move,
        root_color=node.root_color,
    )

    node.children.append(child)
    return child


def backpropagate(node: ChessSearchNode, reward: float) -> None:
    """Backpropagate one simulation result to the root."""
    current = node

    while current is not None:
        current.visits += 1
        current.total_reward += reward
        current = current.parent


def run_mcts_iteration(
    root: ChessSearchNode,
    rollout_plies: int,
    rng: random.Random,
) -> None:
    """One complete MCTS iteration: selection, expansion, simulation, backup."""
    node = root

    # Selection.
    while (
        not node.board.is_game_over()
        and not node.untried_moves
        and node.children
    ):
        node = select_child(node)

    # Expansion.
    if not node.board.is_game_over() and node.untried_moves:
        node = expand_node(node)

    # Simulation.
    simulation_board = node.board.copy(stack=False)
    reward = simulation_result(
        simulation_board,
        root.root_color,
        rollout_plies,
        rng,
    )

    # Backpropagation.
    backpropagate(node, reward)


def choose_mcts_move(root: ChessSearchNode) -> Optional[chess.Move]:
    """
    Standard final MCTS choice: most visited root child.

    Using visits rather than mean reward is standard because it is
    more stable when the tree has been sampled many times.
    """
    if not root.children:
        return None

    best_child = max(
        root.children,
        key=lambda child: (child.visits, child.mean_reward),
    )
    return best_child.move


def root_statistics(root: ChessSearchNode) -> list[tuple[str, float, int]]:
    """Return root move statistics sorted by visits."""
    rows = []

    for child in root.children:
        rows.append(
            (
                child.move.uci(),
                child.mean_reward,
                child.visits,
            )
        )

    rows.sort(key=lambda row: row[2], reverse=True)
    return rows


def run_mcts(
    board: chess.Board,
    depth: int = 3,
    iterations: int = 10_000,
    seed: Optional[int] = None,
) -> tuple[Optional[chess.Move], ChessSearchNode]:
    """
    Run MCTS.

    IMPORTANT:
    Professor defines depth 3 as:
        3 White moves + 3 Black moves = 6 plies.

    Therefore:
        total_plies = depth * 2
    """
    root_color = board.turn
    total_plies = depth * 2

    rng = random.Random(seed)

    root = ChessSearchNode(
        board=board.copy(stack=False),
        root_color=root_color,
    )

    # If the starting position already has a mate in one, return it.
    # This is a tactical safeguard, not a full Minimax search.
    mate_move = immediate_checkmate(root.board)
    if mate_move is not None:
        return mate_move, root

    # The root move itself consumes one ply.
    rollout_plies = max(0, total_plies - 1)

    for _ in range(iterations):
        run_mcts_iteration(root, rollout_plies, rng)

    return choose_mcts_move(root), root


# ---------------------------------------------------------------------------
# Exact verification.
# This section is NOT used by run_mcts().
# It is used by the experiment script to measure MCTS correctness.
# ---------------------------------------------------------------------------

def can_force_mate(
    board: chess.Board,
    plies_remaining: int,
    target_color: chess.Color,
    memo: Optional[dict] = None,
) -> bool:
    """
    Exact bounded forced-mate search.

    target_color's turn:
        at least one move must force mate.

    opponent's turn:
        every legal response must still allow target_color to force mate.
    """
    if memo is None:
        memo = {}

    key = (
        board.fen(),
        plies_remaining,
        target_color,
    )

    if key in memo:
        return memo[key]

    if board.is_checkmate():
        result = board.turn != target_color
        memo[key] = result
        return result

    if (
        plies_remaining == 0
        or board.is_stalemate()
        or board.is_insufficient_material()
    ):
        memo[key] = False
        return False

    legal_moves = ordered_moves(board)

    if board.turn == target_color:
        # Existential: target needs one winning continuation.
        for move in legal_moves:
            board.push(move)
            result = can_force_mate(
                board,
                plies_remaining - 1,
                target_color,
                memo,
            )
            board.pop()

            if result:
                memo[key] = True
                return True

        memo[key] = False
        return False

    # Universal: opponent can choose ANY legal response.
    for move in legal_moves:
        board.push(move)
        result = can_force_mate(
            board,
            plies_remaining - 1,
            target_color,
            memo,
        )
        board.pop()

        if not result:
            memo[key] = False
            return False

    memo[key] = True
    return True


def find_forced_mate_moves(
    board: chess.Board,
    total_plies: int,
) -> list[chess.Move]:
    """
    Return every root move that forces mate within total_plies.

    This is used only to judge whether the MCTS-selected move is correct.
    """
    target_color = board.turn
    forced_moves = []
    memo = {}

    for move in ordered_moves(board):
        board.push(move)

        if can_force_mate(
            board,
            total_plies - 1,
            target_color,
            memo,
        ):
            forced_moves.append(move)

        board.pop()

    return forced_moves
