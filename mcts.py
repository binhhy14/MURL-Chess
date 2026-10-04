# Import the python-chess library
import chess
import random
import math
import time

# ------------ MCTS NODE ------------

class ChessSearchNode:

    def __init__(
        self,
        board_position,
        parent_node=None,
        move_from_parent=None,
        depth=0
    ):

        # Store this chess position
        self.board_position = board_position.copy()

        # Previous node
        self.parent_node = parent_node

        # Move used to reach this node
        self.move_from_parent = move_from_parent

        # Depth of this node in the search tree
        self.depth = depth

        # Child nodes already created
        self.child_nodes = []

        # Legal moves not expanded yet
        self.moves_not_expanded = list(
            self.board_position.legal_moves
        )

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

    # Create a node one level deeper
    child_node = ChessSearchNode(
        new_board,
        parent_node=node,
        move_from_parent=move,
        depth=node.depth + 1
    )

    # Save the child node
    node.child_nodes.append(child_node)

    return child_node


# ------------ SIMULATION ------------

def simulate_game(node, max_depth=3):

    # Start from this node's position
    simulation_board = node.board_position.copy()

    # Current depth of this node
    current_depth = node.depth

    # Play only until depth 3
    while (
        not simulation_board.is_game_over()
        and current_depth < max_depth
    ):

        # Get legal moves
        legal_moves = list(simulation_board.legal_moves)

        # Pick one legal move randomly
        move = random.choice(legal_moves)

        # Play the move
        simulation_board.push(move)

        # Go one level deeper
        current_depth += 1

    # Evaluate the final position
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

    # Game did not end before max_depth
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

def run_mcts_iteration(root_node, max_depth=3):

    # Start from the root
    current_node = root_node

    # Keep selecting while there are no moves left to expand
    # and we have not reached depth 3
    while (
        len(current_node.moves_not_expanded) == 0
        and len(current_node.child_nodes) > 0
        and current_node.depth < max_depth
    ):

        # Select one child using UCB
        current_node = select_best_child(current_node)

    # Expand one new move if possible
    # Do not expand beyond depth 3
    if (
        len(current_node.moves_not_expanded) > 0
        and not current_node.board_position.is_game_over()
        and current_node.depth < max_depth
    ):
        current_node = expand_node(current_node)

    # Play a random simulation up to depth 3
    simulation_result = simulate_game(
        current_node,
        max_depth
    )

    # Send the result back to the root
    backpropagate(
        current_node,
        simulation_result
    )


# ------------ RUN MCTS ------------

def run_mcts(board, number_of_iterations, depth=3):

    # Create the root from the current position
    root_node = ChessSearchNode(board)

    # Run MCTS many times
    for iteration in range(number_of_iterations):

        run_mcts_iteration(root_node, depth)

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
    # Test the 20 chess positions from the assignment
    positions = {
        1: "r1b1k1nr/p2p1ppp/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1 w - - 0 1",

        2: "1r4r1/pbpkpn1p/1b3P2/8/8/B1PB1q2/P4PPP/3R2K1 w - - 0 1",

        3: "1Q6/5pk1/2p3p1/1p2N2p/1b5P/1b4n1/r5P1/2K5 b - - 0 1",

        4: "rnb1kb1r/pp3ppp/2p5/4q3/4n3/3Q4/PPPB1PPP/2KR1BNR w - - 0 1",

        5: "8/6R1/7p/5K1k/8/6p1/5bPP/4N3 w - - 0 1",

        6: "7k/3Q2pp/4r3/8/8/8/3r3P/6K1 w - - 0 1",

        7: "6rk/6pp/8/8/8/3Q3N/8/4R2K w - - 0 1",

        8: "2N3rk/5Qpp/8/8/8/8/5R2/2K5 w - - 0 1",

        9: "1R4rk/3N2pp/7Q/8/8/8/8/6K1 w - - 0 1",

        10: "4R3/6pk/2Q5/5N2/2p5/8/7p/1K6 w - - 0 1",

        11: "1rN3k1/5pp1/8/4Q3/1q1R4/8/5PP1/6K1 w - - 0 1",

        12: "6N1/Q4Rpk/8/8/8/6n1/8/K7 w - - 0 1",

        13: "2n4k/3R4/3p4/8/4N3/8/8/3nK3 w - - 0 1",

        14: "6rk/6pp/7P/1N2Q3/6pb/8/8/6K1 w - - 0 1",

        15: "r2B2k1/5ppp/8/5Q2/8/R7/5PPP/6K1 w - - 0 1",

        16: "7k/1P6/6p1/8/8/6K1/8/5R2 w - - 0 1",

        17: "6k1/P2P4/5R2/6b1/8/8/6K1/8 w - - 0 1",

        18: "3Nk3/2P3b1/8/8/8/8/8/K5R1 w - - 0 1",

        19: "8/n5kP/3P4/8/2Q5/5K2/8/8 w - - 0 1",

        20: "7k/b1Pn4/R6P/8/8/6K1/8/8 w - - 0 1"
    }

    # MCTS settings
    number_of_iterations = 1000
    number_of_runs = 5
    depth = 10

    # Test every position
    for position_number, fen in positions.items():

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
                number_of_iterations,
                depth
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


        print("\nPosition:", position_number)
        print("Number of pieces:", number_of_pieces)
        print("Legal moves:", number_of_legal_moves)
        print("Depth:", depth)
        print("Iterations:", number_of_iterations)
        print("Best move:", final_best_move)
        print(
            "Average execution time:",
            average_time,
            "seconds"
        )


if __name__ == "__main__":
    main()