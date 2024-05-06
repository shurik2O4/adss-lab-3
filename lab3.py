from modified_jordan import jordan_elimination
from math_utils import *
from simplex import *
import numpy as np

def remove_0s_rows(row_names: row_names, column_names: column_names, equation: equation, constants: constants, Z: Z, v: v) -> tuple[row_names, column_names, equation, constants, Z, v]:
    # Repeat until there are no 0's in the row names
    while any([r[0] == '0' for r in row_names]):
        col = None
        # Look for a positive value in one of the rows with a 0
        rows_with_0 = [i for i, n in enumerate(row_names) if n[0] == '0']
        for r in rows_with_0:
            if any(equation[r] > 0):
                col = np.where(equation[r] > 0)[0][0]
                break
        
        if col is None:
            raise ValueError("No positive values in the row")
        
        # Divide each element in the column by the element in the constants
        div_result = div_column_by_constants(equation, col, constants)

        # Find the minimum positive value
        row, _ = min_positive(div_result)

        row_names, column_names, matrix = jordan_elimination(row_names, column_names, assemble_matrix(equation, constants, Z, v), row, col)
        
        # Remove the current column from matrix
        matrix = np.delete(matrix, col, axis=1)
        column_names.pop(col)

        print_matrix(matrix, f"Matrix after removing a column (row: {row + 1}, col: {col + 1} [{equation[row][col]}]):")

        equation, constants, Z, v = disassemble_matrix(matrix)
    
    return row_names, column_names, equation, constants, Z, v