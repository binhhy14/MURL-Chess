### Table 1. Minimax and MCTS Results for the 20 Chess Positions

The table below shows the number of pieces, number of legal moves, 
selected first move, and average execution time for Minimax and MCTS. 

Minimax was tested at depth 3, while MCTS used depth 3 and 1,000 iterations. 
Each position was run five times to calculate the average execution time.

Position  Pieces  Legal Moves  Minimax Move  Minimax Time (s)  MCTS Move  MCTS Time (s)
--------  ------  -----------  ------------  -----------------  ---------  ------------
1         25      40           d5f4          1.5627             d6e7       0.2908
2         21      31           d3e2          1.5317             d3f5       0.3257
3         15      40           b4c3          1.0215             g7h7       0.3427
4         27      43           d3e3          2.9604             d3e4       0.2897
5         9       23           e1f3          0.1874             g7g8       0.2329
6         8       22           d7c8          0.4703             d7e6       0.1786
7         8       44           h3g5          0.6407             h3g5       0.2572
8         8       41           f7f8          0.4529             c8e7       0.2030
9         8       42           h6d6          0.4553             b8g8       0.2204
10        8       51           d6h2          0.5921             e8h8       0.2498
11        11      46           e5e8          1.9250             e5e8       0.2682
12        7       35           g8e7          0.4254             g8e7       0.2181
13        7       21           e1d1          0.1412             d7d8       0.1734
14        10      35           h6g7          0.5851             e5c7       0.2495
15        12      51           a3a8          1.2833             d8e7       0.2823
16        5       26           g3g4          0.0851             g3h4       0.1626
17        6       30           d7d8q         0.3010             f6g6       0.2175
18        6       3            g1g7          0.0233             a1a2       0.1280
19        6       38           c4g8          0.3947             c4g8       0.2274
20        7       24           a6a7          0.2775             a6a7       0.1882