### Table 1. Minimax and MCTS Results for the 20 Chess Positions

The table below shows the number of pieces, number of legal moves,

selected first move, and average execution time for Minimax and MCTS.

Minimax was tested at depth 3, while MCTS used depth 3 and 1,000 iterations.

Each position was run five times to calculate the average execution time.

Position  Pieces  Legal Moves  Minimax Move  Minimax Time (s)  MCTS Move  MCTS Time (s)

--------  ------  -----------  ------------  -----------------  ---------  ------------

1         25      40           f5g7          29.5918             d6e7       0.2908
2         21      31           d3f5          44.8206             d3f5       0.3257
3         15      40           g3e2          18.5011             g7h7       0.3427
4         27      43           d3d8          11.3690             d3e4       0.2897
5         9       23           g7g3          28.2388             g7g8       0.2329
6         8       22           d7c8           1.5659             d7e6       0.1786
7         8       44           h3g5           8.0227             h3g5       0.2572
8         8       41           f7g8           6.5189             c8e7       0.2030
9         8       42           b8g8           6.4177             b8g8       0.2204
10        8       51           e8h8           9.5467             e8h8       0.2498
11        11      46           d4d8          37.2952             e5e8       0.2682
12        7       35           f7g7           5.3130             g8e7       0.2181
13        7       21           e4f6           1.1880             d7d8       0.1734
14        10      35           b5d6          22.4631             e5c7       0.2495
15        12      51           a3a8          24.9783             d8e7       0.2823
16        5       26           f1f7           1.5139             g3h4       0.1626
17        6       30           d7d8q          5.0609             f6g6       0.2175
18        6       3            g1g7           2.6577             a1a2       0.1280
19        6       38           c4g8           3.4352             c4g8       0.2274
20        7       24           c7c8q         13.7978             a6a7       0.1882