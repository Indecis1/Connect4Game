# This file discuss the winning checking algorithm

The checking algorithm is managed by the ```Board``` class

The algorithm's steps are 
1. Init filter we will use
1. if the after a player turn the board is full and the player didn't win, it is a draw
1. foreach player build a new board with 1 where are his/her token and 0 otherwise
1. foreach new board slice it in 4$`\times`$4 overlapping views
1. multiply element-wise each view by each filter
1. if one of the multiplication sums is 4 the player won the game

## Init Filter

In the game rules a player has won if he has 4 consecutive token in any direction
so to check that we would build 4$`\times`$4 matrix with 4 consecutive 1 in a direction.

These filters perform a vertical check
```math
\begin{bmatrix}
1 & 0 & 0 & 0 \\
1 & 0 & 0 & 0 \\
1 & 0 & 0 & 0 \\
1 & 0 & 0 & 0
\end{bmatrix}

\begin{bmatrix}
0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0
\end{bmatrix}

\begin{bmatrix}
0 & 0 & 1 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 1 & 0
\end{bmatrix}

\begin{bmatrix}
0 & 0 & 0 & 1 \\  
0 & 0 & 0 & 1 \\
0 & 0 & 0 & 1 \\
0 & 0 & 0 & 1 
\end{bmatrix}
```

These filters perform horizontal check
```math
\begin{bmatrix}
1 & 1 & 1 & 1 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0
\end{bmatrix}

\begin{bmatrix}
0 & 0 & 0 & 0 \\
1 & 1 & 1 & 1 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0
\end{bmatrix}

\begin{bmatrix}
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
1 & 1 & 1 & 1 \\
0 & 0 & 0 & 0
\end{bmatrix}

\begin{bmatrix}
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
1 & 1 & 1 & 1
\end{bmatrix}
```

These filters perform diagonal check

```math
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}

\begin{bmatrix}
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
1 & 0 & 0 & 0
\end{bmatrix}
```

## Build player board
foreach player compute a new board with 1 where he played and 0 where he didn't play

## Build overlapping views
With the new player board create all 4$`\times`$4 overlapping views.

If we take for example a 5$`\times`$5 boars, here are all the overlapping views of this board

![connect4_doc](https://github.com/Indecis1/Connect4Game/assets/80837432/df64c304-0a0c-4159-a22c-c258ac2b7933)

If we take connect 4 game the board which is 6$`\times`$7. we have 6-4+1 = 3 views in the first dimension and 7-4+1 = 4 
views in the second dimension. The total of overlapping views is 3$`\times`$4 = 12 overlapping views.

## Element-wise multiplication

foreach view we multiply it with all the filters, and we perform the sum of each matrix. If a sum == 4 it means that
the player has 4 consecutive token in the direction. The direction is determined by the filter used
