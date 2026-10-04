import csv

minimax_file = "experiments/results/minimax_results.csv"
mcts_file = "experiments/results/mcts_results.csv"
output_file = "experiments/results/comparison.csv"


with open(minimax_file, newline="", encoding="utf-8") as file:
    minimax_data = list(csv.DictReader(file))

with open(mcts_file, newline="", encoding="utf-8") as file:
    mcts_data = list(csv.DictReader(file))


with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Position",
        "Name",
        "Pieces",
        "Legal Moves",
        "Minimax Move",
        "Minimax Time (s)",
        "MCTS Move",
        "MCTS Time (s)"
    ])

    for minimax_row, mcts_row in zip(minimax_data, mcts_data):

        writer.writerow([
            minimax_row["Position"],
            minimax_row["Name"],
            minimax_row["Pieces"],
            minimax_row["Legal Moves"],
            minimax_row["Best Move"],
            minimax_row["Average Time (s)"],
            mcts_row["Best Move"],
            mcts_row["Average Time (s)"]
        ])


print("Comparison results saved to:", output_file)