import sys
import os
import csv
import time
import chess

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from minimax import find_best_move


# Names of the 20 chess positions
position_names = {
    1: "The Immortal Game",
    2: "The Evergreen Game",
    3: "The Game of the Century",
    4: "Réti's Mate",
    5: "Loyd's Charles XII Problem",
    6: "Back-Rank Mate: Queen Sacrifices",
    7: "Back-Rank Mate: Quiet Knight Move",
    8: "Queen Sacrifice and Knight Support",
    9: "Rook Sacrifice: Queen on the Long Diagonal",
    10: "Rook Sacrifice: Queen and Knight Mate",
    11: "Anastasia's Mate",
    12: "Arabian Mate",
    13: "Arabian Mate: Rook Lift",
    14: "Smothered Mate",
    15: "Double-Check Mate",
    16: "Promotion Mate",
    17: "Double Promotion",
    18: "Under-Promotion to a Rook",
    19: "Under-Promotion to a Bishop",
    20: "Under-Promotion to a Knight"
}


# The 20 chess positions provided for the MURL project
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

    10: "4R3/6pk/3Q4/5N2/2p5/8/7p/1K6 w - - 0 1",

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


# Professor's depth 3 means:
# 3 White moves + 3 Black moves = 6 plies
depth = 3

# Number of times to run each position
runs = 5


# Save results here
output_file = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "results",
    "minimax_results.csv"
)


# Make sure the results folder exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)


# Store all experiment results
results = []


# Run every chess position
for position_number, board_position in positions.items():

    board = chess.Board(board_position)

    # Count legal moves in the original position
    number_of_legal_moves = len(list(board.legal_moves))

    # Count pieces in the original position
    number_of_pieces = len(board.piece_map())

    # Store total execution time
    total_time = 0

    # Store the result from the last run
    best_move = None
    best_score = None

    # Run the same position multiple times
    for run in range(runs):

        # Create a fresh board for every run
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

        # Add this run's execution time
        total_time += end_time - start_time

    # Calculate average execution time
    average_time = total_time / runs

    # Store the result
    results.append([
        position_number,
        position_names[position_number],
        number_of_pieces,
        number_of_legal_moves,
        best_move,
        best_score,
        average_time
    ])

    # Print result to terminal
    print("\nPosition:", position_number)
    print("Name:", position_names[position_number])
    print("Number of pieces:", number_of_pieces)
    print("Legal moves:", number_of_legal_moves)
    print("Depth:", depth)
    print("Total plies:", depth * 2)
    print("Best move:", best_move)
    print("Best score:", best_score)
    print("Average execution time:", average_time, "seconds")


# Save all results to CSV
with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow([
        "Position",
        "Name",
        "Pieces",
        "Legal Moves",
        "Best Move",
        "Best Score",
        "Average Time (s)"
    ])

    writer.writerows(results)


print("\nMinimax results saved to:", output_file)