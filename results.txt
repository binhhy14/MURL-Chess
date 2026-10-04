MURL Chess Project
Minimax and Monte Carlo Tree Search

Test setup:
I tested positions with 4, 6, 8, 10, and 12 pieces.

Minimax:
- Depth = 3
- 5 runs per position

MCTS:
- 1000 iterations
- Maximum simulation length = 40 plies
- 5 runs per position

Boards:
4 pieces:
r5k1/8/8/8/8/8/8/6KR w - - 0 1

6 pieces:
r5k1/3p4/8/8/8/3P4/8/6KR w - - 0 1

8 pieces:
rn4k1/3p4/8/8/8/3P4/8/1N4KR w - - 0 1

10 pieces:
rn4k1/8/2pp4/8/8/2PP4/8/1N4KR w - - 0 1

12 pieces:
rn3bk1/8/2pp4/8/8/2PP4/8/1N3BKR w - - 0 1


Results:

Pieces   Legal Moves   Minimax Time   MCTS Time
4        11            0.1015 s       2.6254 s
6        12            0.1301 s       2.8991 s
8        15            0.1635 s       3.0152 s
10       15            0.1561 s       2.9517 s
12       17            0.2192 s       3.1340 s

Observation:
The execution time generally increased when the positions had more legal moves.
This suggests that positions with fewer possible moves and smaller search trees
are more practical for these implementations.

The number of pieces is useful for testing, but it does not fully determine the
difficulty of a position because the number of legal moves and branches also matters.

Note:
The Minimax and MCTS times are not a direct speed comparison because they use
different search settings.