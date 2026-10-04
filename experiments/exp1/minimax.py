# Import the python-chess library
import chess
import time


# ------------ EVALUATION FUNCTION -----------


# This function evaluates a chess position
# Positive score = Good for White
# Negative score = Good for Black
# Score 0 = both sides have equal material
def evaluate_board(board):

    # If the current player is checkmated, that player loses.
    if board.is_checkmate():

        # If turn = White and White is checkmated, White has lost.
        if board.turn == chess.WHITE:
            return -10000

        # Black is checkmated --> white has won
        else:
            return 10000

    # Other finished games are treated as draws
    if board.is_game_over():
        return 0

    
    # Count the number of white and black pawns
    white_pawns = len(board.pieces(chess.PAWN, chess.WHITE))
    black_pawns = len(board.pieces(chess.PAWN, chess.BLACK))

    # Count the number of white and black knights
    white_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
    black_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))

    # Count the number of white and black bishops
    white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
    black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))

    # Count the number of white and black rooks
    white_rooks = len(board.pieces(chess.ROOK, chess.WHITE))
    black_rooks = len(board.pieces(chess.ROOK, chess.BLACK))

    # Count the number of white and black queens
    white_queens = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queens = len(board.pieces(chess.QUEEN, chess.BLACK))


    # Calculate White's total material score
    # Pawn = 1
    # Knight = 3
    # Bishop = 3
    # Rook = 5
    # Queen = 9
    white_score = (
        white_pawns * 1
        + white_knights * 3
        + white_bishops * 3
        + white_rooks * 5
        + white_queens * 9
    )


    # Calculate Black's total material score
    black_score = (
        black_pawns * 1
        + black_knights * 3
        + black_bishops * 3
        + black_rooks * 5
        + black_queens * 9
    )

    # Return the difference between White's score and Black's score
    return white_score - black_score  # positive is good for White / negative is good for Black

# ----------- MINIMAX FUNCTION -------------


# board = current chess position
# depth = how many more moves we want to look ahead
def minimax(board, depth):
   
   #print(
   #   "depth =", depth,
   #    "| turn =",
   #    "White" if board.turn == chess.WHITE else "Black"
   #)

    # BASE CASE:
    # Stop searching when depth becomes 0
    # or when the chess game is already finished
    if depth == 0 or board.is_game_over():

        # Give the current position a score
        return evaluate_board(board)


    # ------------ WHITE'S TURN = MAX -----------
    
    if board.turn == chess.WHITE:

        # White wants the HIGHEST score
        best_score = float("-inf")

        # Try every legal move for White
        for white_move in list(board.legal_moves):

            # Make the move
            board.push(white_move)

            # Call minimax again on the NEW board
            # depth - 1 means we move one level deeper
            score = minimax(board, depth - 1)

            # Undo the move
            board.pop()

            # White keeps the highest score
            if score > best_score:
                best_score = score

        return best_score


    #----------- BLACK'S TURN = MIN --------------
    
    else:

        # Black wants the LOWEST score
        best_score = float("inf")

        # Try every legal move for Black
        for move in list(board.legal_moves):

            # Make Black's move
            board.push(move)

            # Search one level deeper
            score = minimax(board, depth - 1)

            # Undo Black's move
            board.pop()

            # Black keeps the lowest score
            if score < best_score:
                best_score = score

        return best_score


# ---------------- FIND THE BEST MOVE ---------------

# This function tries every possible first move
# and uses Minimax to determine which one is best
def find_best_move(board, depth):

    # First, no best move found
    best_move = None

    # Turn = White
    # White wants the highest score
    if board.turn == chess.WHITE:
        best_score = float("-inf")

    # Turn = Black
    # Black wants the lowest score
    else:
        best_score = float("inf")


    #Get every legal move for the current player
    moves = list(board.legal_moves)

    #Try every possible first move
    for move in moves:

        #Make the move temporarily
        board.push(move)

        #Minimax looks into the future from this new position.
        #Use depth - 1 because we already made the first move above
        score = minimax(board, depth - 1)

        # Undo the move
        board.pop()

        #print each move and its Minimax score
       #print("Move:" , move, "Score", score)


        # turn = WHITE, keep highest score
        if board.turn == chess.WHITE:

            if score > best_score:
                best_score = score
                best_move  = move

        # turn = BLACK, keep lowest score
        else:

            if score < best_score:
                best_score = score
                best_move = move

    return best_move, best_score


def main():

    # Test positions
    positions = {
        4:  "r5k1/8/8/8/8/8/8/6KR w - - 0 1",
        6:  "r5k1/3p4/8/8/8/3P4/8/6KR w - - 0 1",
        8:  "rn4k1/3p4/8/8/8/3P4/8/1N4KR w - - 0 1",
        10: "rn4k1/8/2pp4/8/8/2PP4/8/1N4KR w - - 0 1",
        12: "rn3bk1/8/2pp4/8/8/2PP4/8/1N3BKR w - - 0 1"
    }

    # Look ahead 3 moves
    depth = 3

    # Number of times to run each position
    runs = 5

    for piece_count, board_position in positions.items():

        # Create a board
        board = chess.Board(board_position)
        print("\nBoard:")
        print(board)

        # Count legal moves in this position
        number_of_legal_moves = len(list(board.legal_moves))

        # Count pieces
        number_of_pieces = len(board.piece_map())

        # Store the total time
        total_time = 0

        # Run the same position 5 times
        for run in range(runs):

            # Create a fresh board
            board = chess.Board(board_position)

            # Start timing
            start_time = time.perf_counter()

            # Run Minimax
            best_move, best_score = find_best_move(
                board,
                depth
            )

            # Stop timing
            end_time = time.perf_counter()

            # Add this run's time
            total_time += end_time - start_time

        # Calculate average time
        average_time = total_time / runs

        print("\nTest:", piece_count, "pieces")
        print("Number of pieces:", number_of_pieces)
        print("Legal moves:", number_of_legal_moves)
        print("Depth:", depth)
        print("Best move:", best_move)
        print("Best score:", best_score)
        print(
            "Average execution time:",
            average_time,
            "seconds"
        )


if __name__ == "__main__":
    main()