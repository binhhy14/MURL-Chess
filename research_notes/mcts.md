# Monte Carlo Tree Search

## What is MCTS?

Monte Carlo Tree Search (MCTS) is a search method that uses repeated simulations to explore possible moves.

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

The algorithm plays random moves until the simulation reaches the maximum depth or the game ends.

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

## Questions / Things to Improve

- How does the number of simulations affect the result?
- How does MCTS compare with Minimax?
- Does increasing the number of iterations improve move selection?