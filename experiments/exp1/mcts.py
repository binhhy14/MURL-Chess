# Import the python-chess library
import chess
import random
import math
import time

# ------------ MCTS NODE ------------

class ChessSearchNode:

    def __init__(self, board_position, parent_node=None, move_from_parent=None):

        # Store this chess position
        self.board_position = board_position.copy()

        # Previous node
        self.parent_node = parent_node

        # Move used to reach this node
        self.move_from_parent = move_from_parent

        # Child nodes already created
        self.child_nodes = []

        # Legal moves not expanded yet
        self.moves_not_expanded = list(self.board_position.legal_moves)

        # Number of visits
        self.visit_count = 0

        # Total simulation result
        self.reward_sum = 0.0

# ------------ EXPANSION ------------

def expand_node(node):

    # No move left to expand
    if len(node.moves_not_expanded) == 0:
        return None

    # Take the first move not expanded yet
    move = node.moves_not_expanded.pop(0)

    # Copy the current board
    new_board = node.board_position.copy()

    # Play the move
    new_board.push(move)

    # Create a node for the new position
    child_node = ChessSearchNode(
        new_board,
        parent_node=node,
        move_from_parent=move
    )

    # Save the child node
    node.child_nodes.append(child_node)

    return child_node


# ------------ SIMULATION ------------

def simulate_game(node, max_plies=40):

    # Start from this node's position
    simulation_board = node.board_position.copy()

    # Count moves in the simulation
    plies_played = 0

    # Play until game over or the move limit
    while not simulation_board.is_game_over() and plies_played < max_plies:

        # Get legal moves for the current side
        legal_moves = list(simulation_board.legal_moves)

        # Pick one legal move randomly
        move = random.choice(legal_moves)

        # Play the move
        simulation_board.push(move)

        # Count the move
        plies_played += 1

    # Evaluate the final simulation position
    return get_simulation_result(simulation_board)


# ------------ SIMULATION RESULT ------------

def get_simulation_result(board):

    # Use the real result if the game ended
    if board.is_game_over():

        result = board.result()

        # White wins
        if result == "1-0":
            return 1

        # Black wins
        if result == "0-1":
            return -1

        # Draw
        return 0

    # Game did not end before max_plies
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }

    white_score = 0
    black_score = 0

    # Count material for both sides
    for piece_type, value in piece_values.items():

        white_score += len(
            board.pieces(piece_type, chess.WHITE)
        ) * value

        black_score += len(
            board.pieces(piece_type, chess.BLACK)
        ) * value

    # White has more material
    if white_score > black_score:
        return 1

    # Black has more material
    if black_score > white_score:
        return -1

    # Equal material
    return 0


# ------------ BACKPROPAGATION ------------

def backpropagate(node, simulation_result):

    # Start from the simulated node
    current_node = node

    # Move backward until the root is passed
    while current_node is not None:

        # This node was visited once more
        current_node.visit_count += 1

        # Add the simulation result
        current_node.reward_sum += simulation_result

        # Move to the parent node
        current_node = current_node.parent_node


# ------------ UCB SCORE ------------

def calculate_ucb(parent_node, child_node):

    # Try an unvisited child first
    if child_node.visit_count == 0:
        return float("inf")

    # Average simulation result
    average_reward = (
        child_node.reward_sum / child_node.visit_count
    )

    # Black prefers lower White reward
    if parent_node.board_position.turn == chess.BLACK:
        average_reward = -average_reward

    # Give extra value to less visited nodes
    exploration_bonus = math.sqrt(
        math.log(parent_node.visit_count)
        / child_node.visit_count
    )

    return average_reward + exploration_bonus


# ------------ SELECTION ------------

def select_best_child(node):

    # Best child found so far
    best_child = None

    # Start lower than every possible UCB score
    best_ucb = float("-inf")

    # Check every child of this node
    for child in node.child_nodes:

        # Calculate this child's UCB score
        ucb_score = calculate_ucb(node, child)

        # Keep the child with the highest UCB
        if ucb_score > best_ucb:
            best_ucb = ucb_score
            best_child = child

    return best_child


# ------------ ONE MCTS ITERATION ------------

def run_mcts_iteration(root_node):

    # Start from the root
    current_node = root_node

    # Go down while this node has no new move to expand
    while (
        len(current_node.moves_not_expanded) == 0
        and len(current_node.child_nodes) > 0
    ):

        # Select one child using UCB
        current_node = select_best_child(current_node)

    # Expand one new move if possible
    if (
        len(current_node.moves_not_expanded) > 0
        and not current_node.board_position.is_game_over()
    ):
        current_node = expand_node(current_node)

    # Play a random simulation
    simulation_result = simulate_game(current_node)

    # Send the result back to the root
    backpropagate(current_node, simulation_result)


# ------------ RUN MCTS ------------

def run_mcts(board, number_of_iterations):

    # Create the root from the current position
    root_node = ChessSearchNode(board)

    # Run MCTS many times
    for iteration in range(number_of_iterations):

        run_mcts_iteration(root_node)

    # Find the most visited root child
    best_child = None
    most_visits = -1

    for child in root_node.child_nodes:

        if child.visit_count > most_visits:
            most_visits = child.visit_count
            best_child = child

    # Return the move that created the best child
    return best_child.move_from_parent, root_node



def main():

    # Test positions
    positions = {
        4:  "r5k1/8/8/8/8/8/8/6KR w - - 0 1",
        6:  "r5k1/3p4/8/8/8/3P4/8/6KR w - - 0 1",
        8:  "rn4k1/3p4/8/8/8/3P4/8/1N4KR w - - 0 1",
        10: "rn4k1/8/2pp4/8/8/2PP4/8/1N4KR w - - 0 1",
        12: "rn3bk1/8/2pp4/8/8/2PP4/8/1N3BKR w - - 0 1"
    }

    # MCTS settings
    number_of_iterations = 1000
    number_of_runs = 5

    # Test every position
    for piece_count, fen in positions.items():

        # Create board for position information
        board_info = chess.Board(fen)

        print("\nBoard:")
        print(board_info)

        # Count pieces
        number_of_pieces = len(board_info.piece_map())

        # Count legal moves
        number_of_legal_moves = len(
            list(board_info.legal_moves)
        )

        times = []
        best_moves = []

        # Run each position 5 times
        for run in range(number_of_runs):

            # Create a fresh board
            board = chess.Board(fen)

            # Start timing
            start_time = time.perf_counter()

            # Run MCTS
            best_move, root_node = run_mcts(
                board,
                number_of_iterations
            )

            # Stop timing
            end_time = time.perf_counter()

            execution_time = end_time - start_time

            # Save results
            times.append(execution_time)
            best_moves.append(str(best_move))

        # Calculate average time
        average_time = sum(times) / len(times)

        # Find the most common best move
        final_best_move = max(
            set(best_moves),
            key=best_moves.count
        )

        print("\nTest:", piece_count, "pieces")
        print("Number of pieces:", number_of_pieces)
        print("Legal moves:", number_of_legal_moves)
        print("Iterations:", number_of_iterations)
        print("Best move:", final_best_move)
        print(
            "Average execution time:",
            average_time,
            "seconds"
        )


if __name__ == "__main__":
    main()