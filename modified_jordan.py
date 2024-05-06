from utils import print_matrix
from math_utils import *
import numpy as np

def jordan_elimination(row_names: row_names, column_names: column_names, matrix: np.ndarray, r: int, s: int) -> tuple[row_names, column_names, np.ndarray]:
    if matrix[r][s] == 0: raise ValueError(f"Matrix value at ({r},{s}) is 0")

    copy = matrix.copy()
    # 3: Invert the column sign
    copy[:, s] = -copy[:, s]

    # 1: Set the element to 1
    copy[r][s] = 1

    # 2: Don't change row elements
    # 4: Calculate other elements
    # r, i - row
    # s, j - column
    for i in range(copy.shape[0]):
        for j in range(copy.shape[1]):
            # Don't touch the row and column
            if i != r and j != s:
                copy[i][j] = matrix[i][j] * matrix[r][s] - matrix[i][s] * matrix[r][j]

    # Extra: swap the row and column names
    column_names[s], row_names[r] = row_names[r], column_names[s]

    # 5: Divide the new matrix by the element
    return (row_names, column_names, copy / matrix[r][s])


if __name__ == "__main__":
    # Test the function
    # matrix = input_matrix(print_back=True)
    # matrix = np.array([[-1.,  0.,  3., -2.,  1.,  3.],
    #                    [ 1., -1.,  0.,  1.,  1.,  3.],
    #                    [-1., -3.,  1.,  1., -1., -2.],
    #                    [-1.,  1.,  0.,  0.,  1.,  0.]])
    matrix = np.array([[-1,  2, -1,  2,  1,  6],
                       [ 1,  4,  3,  2,  1,  9],
                       [ 1,  2,  0,  2, -1,  2],
                       [-2, -2, -1, -1, -1,  0]])
    
    rows = [('y', i + 1) for i in range(matrix.shape[0])]
    cols = [('x', i + 1) for i in range(matrix.shape[1])]
    rows, cols, result = jordan_elimination(row_names, column_names, matrix, int(input("Row: ")) - 1, int(input("Col: ")) - 1)
    print_matrix(result, "Result:")