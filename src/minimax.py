import chess


# ------------ EVALUATION FUNCTION ------------

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -10000
        else:
            return 10000

    if board.is_game_over():
        return 0

    white_pawns = len(board.pieces(chess.PAWN, chess.WHITE))
    black_pawns = len(board.pieces(chess.PAWN, chess.BLACK))
    white_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
    black_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))
    white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
    black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))
    white_rooks = len(board.pieces(chess.ROOK, chess.WHITE))
    black_rooks = len(board.pieces(chess.ROOK, chess.BLACK))
    white_queens = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queens = len(board.pieces(chess.QUEEN, chess.BLACK))

    white_score = (
        white_pawns * 1
        + white_knights * 3
        + white_bishops * 3
        + white_rooks * 5
        + white_queens * 9
    )

    black_score = (
        black_pawns * 1
        + black_knights * 3
        + black_bishops * 3
        + black_rooks * 5
        + black_queens * 9
    )

    return white_score - black_score


# ------------ MINIMAX WITH ALPHA-BETA PRUNING ------------

def minimax(board, plies, alpha=float("-inf"), beta=float("inf")):

    # Stop searching when we reach the desired depth
    # or the game has ended.
    if plies == 0 or board.is_game_over():
        return evaluate_board(board)

    if board.turn == chess.WHITE:

        # White tries to maximize the score.
        best_score = float("-inf")

        for move in list(board.legal_moves):

            board.push(move)

            score = minimax(board, plies - 1, alpha, beta)

            board.pop()

            best_score = max(best_score, score)

            # Alpha is White's best guaranteed score so far.
            alpha = max(alpha, best_score)

            # No need to search the remaining moves.
            if alpha >= beta:
                break

        return best_score

    else:

        # Black tries to minimize the score.
        best_score = float("inf")

        for move in list(board.legal_moves):

            board.push(move)

            score = minimax(board, plies - 1, alpha, beta)

            board.pop()

            best_score = min(best_score, score)

            # Beta is Black's best guaranteed score so far.
            beta = min(beta, best_score)

            # No need to search the remaining moves.
            if alpha >= beta:
                break

        return best_score


# ------------ FIND THE BEST MOVE ------------

def find_best_move(board, depth):

    # Professor's definition:
    # Depth 3 = 3 White moves + 3 Black moves
    #         = 6 individual moves (plies)
    total_plies = depth * 2

    best_move = None

    if board.turn == chess.WHITE:
        best_score = float("-inf")
    else:
        best_score = float("inf")

    moves = list(board.legal_moves)

    # Initial alpha-beta values.
    alpha = float("-inf")
    beta = float("inf")

    for move in moves:

        board.push(move)

        # The first move has already been made,
        # so search the remaining plies.
        score = minimax(
            board,
            total_plies - 1,
            alpha,
            beta
        )

        board.pop()

        if board.turn == chess.WHITE:

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        else:

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)

    return best_move, best_score