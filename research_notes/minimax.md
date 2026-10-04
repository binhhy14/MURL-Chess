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

The current experiment uses:

- Depth = 3
- 5 runs per position

The experiment recorded:

- Best move
- Execution time
- Number of legal moves
- Number of pieces

## Observations

### Does Depth 3 Find the Intended Checkmate?

The current Minimax implementation does not reliably find the intended
mate-in-three solutions.

This is because the current implementation uses a material-based
evaluation function and searches only to depth 3.

The depth also counts individual moves (plies), so depth 3 does not
represent three moves by one side.

### Execution Time and Number of Pieces

The execution time generally increased when positions had more pieces
and more legal moves.

However, the number of pieces alone did not determine the execution
time. The number of legal moves also affected how many positions the
algorithm had to search.

For example, Position 4 had 27 pieces and 43 legal moves and took
approximately 2.97 seconds on average, while Position 18 had 6 pieces
and only 3 legal moves and took approximately 0.02 seconds.

### Alpha-Beta Pruning

Alpha-beta pruning was not implemented in the current version.

It could improve Minimax by avoiding branches that cannot affect the
final decision.

A future experiment could compare Minimax with and without alpha-beta
pruning and measure the difference in execution time.