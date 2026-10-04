# Minimax

## What is Minimax?

Minimax is a search algorithm used for two-player games such as chess.

The algorithm assumes:
- White tries to maximize the evaluation score.
- Black tries to minimize the evaluation score.

## How It Works

1. Generate legal moves.
2. Make a move.
3. Recursively search the resulting position.
4. Evaluate the position when the search reaches the chosen depth.
5. Choose the best score for the current player.

## Depth

In my implementation, depth counts individual moves (plies).

- Depth 1 = one move
- Depth 2 = two moves
- Depth 3 = three moves

## Board Evaluation

My current evaluation function uses material:

- Pawn = 1
- Knight = 3
- Bishop = 3
- Rook = 5
- Queen = 9

Positive score = advantage for White.

Negative score = advantage for Black.

Checkmate is given a much larger score.

## Implementation

The main implementation is in:

`src/minimax.py`

## Experiment

Minimax was tested on the 20 chess positions provided for the MURL project.

The experiment measured:
- Best move
- Execution time
- Number of legal moves
- Number of pieces

## Questions / Things to Improve

- Does depth 3 find the intended checkmate?
- How does execution time change with more pieces?
- How would alpha-beta pruning improve the algorithm?