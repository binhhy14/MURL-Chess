"""
Run the official MURL MCTS experiment on all 20 chess positions.

Configuration:
- 20 positions
- depth = 3
- professor's definition: 3 White + 3 Black = 6 plies
- 10,000 MCTS iterations
- 5 runs per position
- exact forced-mate verification after the MCTS runs
- CSV output

Run from the project root:

    py experiments/exp2/run_mcts.py
"""

from __future__ import annotations

import csv
import os
import sys
import time
from collections import Counter
from pathlib import Path

# Allow this file to import src.mcts when executed from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import chess

from src.mcts import find_forced_mate_moves, run_mcts


DEPTH = 3
TOTAL_PLIES = DEPTH * 2
ITERATIONS = 10_000
RUNS_PER_POSITION = 5

positions = {
    1: "r1b1k1nr/p2p1ppp/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1 w - - 0 1",
    2: "1r4r1/pbpkpn1p/1b3P2/8/8/B1PB1q2/P4PPP/3R2K1 w - - 0 1",
    3: "1Q6/5pk1/2p3p1/1p2N2p/1b5P/1b4n1/r5P1/2K5 b - - 0 1",
    4: "rnb1kb1r/pp3ppp/2p5/4q3/4n3/3Q4/PPPB1PPP/2KR1BNR w - - 0 1",
    5: "8/6R1/7p/5K1k/8/6p1/5bPP/4N3 w - - 0 1",
    6: "7k/3Q2pp/4r3/8/8/8/3r3P/6K1 w - - 0 1",
    7: "6rk/6pp/8/8/8/3Q3N/8/4R2K w - - 0 1",
    8: "2N3rk/5Qpp/8/8/8/5R2/2K5/8 w - - 0 1",
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
    19: "8/n5kP/3P4/8/8/8/2Q5/5K2 w - - 0 1",
    20: "7k/b1Pn4/R6P/8/8/6K1/8/8 w - - 0 1",
}

position_names = {
    1: "The Immortal Game",
    2: "The Evergreen Game",
    3: "The Game of the Century",
    4: "Reti's Mate",
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
    20: "Under-Promotion to a Knight",
}


def most_common_move(moves: list[str]) -> str:
    counts = Counter(moves)
    return counts.most_common(1)[0][0]


def main() -> None:
    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    csv_path = results_dir / "mcts_results.csv"

    rows = []

    print("=" * 78)
    print("MURL CHESS - MCTS EXPERIMENT")
    print("=" * 78)
    print(f"Positions: {len(positions)}")
    print(f"Depth: {DEPTH}")
    print(f"Total plies: {TOTAL_PLIES}")
    print(f"Iterations per run: {ITERATIONS:,}")
    print(f"Runs per position: {RUNS_PER_POSITION}")
    print("=" * 78)

    overall_start = time.perf_counter()

    for position_id, fen in positions.items():
        board = chess.Board(fen)
        piece_count = len(board.piece_map())
        legal_move_count = board.legal_moves.count()

        print("\n" + "=" * 78)
        print(f"Position {position_id}: {position_names[position_id]}")
        print(f"Pieces: {piece_count}")
        print(f"Legal moves: {legal_move_count}")
        print(f"Depth: {DEPTH}")
        print(f"Total plies: {TOTAL_PLIES}")
        print(f"Iterations: {ITERATIONS:,}")
        print("=" * 78)

        run_moves = []
        run_times = []

        for run_number in range(1, RUNS_PER_POSITION + 1):
            # Use a different deterministic seed for each run.
            seed = position_id * 10_000 + run_number

            start = time.perf_counter()

            move, root = run_mcts(
                board,
                depth=DEPTH,
                iterations=ITERATIONS,
                seed=seed,
            )

            elapsed = time.perf_counter() - start

            move_uci = move.uci() if move is not None else "NONE"

            run_moves.append(move_uci)
            run_times.append(elapsed)

            print(
                f"Run {run_number}: "
                f"{move_uci} ({elapsed:.4f} sec)"
            )

        mcts_move = most_common_move(run_moves)
        average_time = sum(run_times) / len(run_times)

        # Exact verification is separate from MCTS.
        # It tells us whether MCTS found a forced mate in the professor's
        # 6-ply depth window.
        print("\nRunning exact forced-mate verification...")

        verification_start = time.perf_counter()

        forced_moves = find_forced_mate_moves(
            board.copy(stack=False),
            TOTAL_PLIES,
        )

        verification_time = time.perf_counter() - verification_start

        forced_move_strings = [move.uci() for move in forced_moves]

        if forced_move_strings:
            mcts_correct = mcts_move in forced_move_strings
            forced_move_display = ", ".join(forced_move_strings)
            forced_mate = "YES"
        else:
            mcts_correct = None
            forced_move_display = "NONE"
            forced_mate = "NO"

        print("\nMCTS result:")
        print("  Moves selected: " + ", ".join(run_moves))
        print(f"  Most common MCTS move: {mcts_move}")

        print("\nExact verification:")
        print(f"  Forced mate found: {forced_mate}")
        print(f"  Forced-mate moves: {forced_move_display}")
        print(f"  MCTS correct: {mcts_correct}")
        print(f"  Average MCTS time: {average_time:.4f} sec")
        print(f"  Exact verification time: {verification_time:.4f} sec")

        # Print the top root moves from the final run.
        print("\nTop MCTS root moves from final run:")
        stats = sorted(
            [
                (child.move.uci(), child.mean_reward, child.visits)
                for child in root.children
            ],
            key=lambda item: item[2],
            reverse=True,
        )

        for move_uci, reward, visits in stats[:5]:
            print(
                f"  {move_uci}: "
                f"reward={reward:.4f}, visits={visits}"
            )

        rows.append(
            {
                "position": position_id,
                "name": position_names[position_id],
                "pieces": piece_count,
                "legal_moves": legal_move_count,
                "depth": DEPTH,
                "total_plies": TOTAL_PLIES,
                "iterations": ITERATIONS,
                "mcts_move": mcts_move,
                "forced_mate": forced_mate,
                "forced_mate_moves": forced_move_display,
                "mcts_correct": mcts_correct,
                "average_mcts_time_sec": round(average_time, 6),
                "exact_verification_time_sec": round(
                    verification_time, 6
                ),
                "run1_move": run_moves[0],
                "run2_move": run_moves[1],
                "run3_move": run_moves[2],
                "run4_move": run_moves[3],
                "run5_move": run_moves[4],
            }
        )

    total_time = time.perf_counter() - overall_start

    fieldnames = list(rows[0].keys())

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\n" + "=" * 78)
    print("FINAL SUMMARY")
    print("=" * 78)

    for row in rows:
        print(
            f"{row['position']:>2}. "
            f"{row['mcts_move']:<8} "
            f"correct={str(row['mcts_correct']):<5} "
            f"time={row['average_mcts_time_sec']:.4f}s"
        )

    print("=" * 78)
    print(f"Total experiment time: {total_time / 60:.2f} minutes")
    print(f"CSV saved to: {csv_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
