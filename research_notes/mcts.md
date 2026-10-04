# Monte Carlo Tree Search

## What is MCTS?

Monte Carlo Tree Search (MCTS) is a search method that uses repeated
simulations to explore possible moves.

## Four Main Steps

1. Selection
2. Expansion
3. Simulation
4. Backpropagation

## Selection

The algorithm chooses a promising child node using UCB.

## Expansion

A new child node is created from an unexplored legal move.

## Simulation

The algorithm plays random moves until the simulation reaches the
maximum depth or the game ends.

## Backpropagation

The simulation result is passed back through the nodes that were visited.

Each node updates:

- visit count
- reward

## UCB

UCB balances:

- Exploitation: choose moves that performed well.
- Exploration: try moves that have been explored less.

## Implementation

The main implementation is in:

`src/mcts.py`

## Experiment

MCTS was tested on the same 20 positions used for Minimax.

Current experiment:

- Depth = 3
- 1,000 iterations
- 5 runs per position

Execution time and selected moves were recorded.

## Observations

### MCTS vs. Minimax

MCTS was generally faster than Minimax in the current experiment.

The average execution time across the 20 positions was approximately:

- Minimax: 0.92 seconds per position
- MCTS: 0.24 seconds per position

However, faster execution does not necessarily mean that MCTS
performed better.

The two methods selected the same move in 5 out of the 20 positions.

### Number of Simulations

The current experiment uses 1,000 iterations for each position.

Increasing the number of iterations would give MCTS more opportunities
to explore different moves, but it would also increase execution time.

### Increasing the Number of Iterations

The current experiment only uses 1,000 iterations, so it is not enough
to determine how increasing the number of iterations affects move
selection.

A future experiment could compare different numbers of iterations,
such as 100, 500, 1,000, and 5,000.