# MURL Chess

## Machine Learning, Chess and Mathematics

This repository contains my work for the MURL research project on
machine learning, chess, and mathematics.

The project explores chess search algorithms and later moves toward
reinforcement learning and neural networks.

## Project Goals

The main goals of the project are:

- Implement Minimax for chess.
- Implement Monte Carlo Tree Search (MCTS).
- Test both methods on chess positions.
- Measure and compare their performance.
- Learn the basic ideas behind neural networks and reinforcement learning.
- Explore how machine learning methods can be applied to chess.

## Project Structure

```text
MURL_PROJECT_CHESS/
│
├── src/
│   ├── minimax.py
│   └── mcts.py
│
├── experiments/
│   ├── run_minimax.py
│   ├── run_mcts.py
│   └── compare_results.py
│
├── results/
│   ├── minimax_results.csv
│   ├── mcts_results.csv
│   └── comparison.csv
│
├── research_notes/
│   ├── minimax.md
│   ├── mcts.md
│   ├── neural_networks.md
│   └── reinforcement_learning.md
│
├── reports/
│   └── ...
│
├── sources/
│   └── references.md
│
├── README.md
└── requirements.txt