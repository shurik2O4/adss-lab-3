from modified_jordan import jordan_elimination
from utils import print_matrix
from typing import Iterable
import numpy as np
from math_utils import *

matrix = equation = constants = Z = solution = np.ndarray
v = float

def assemble_matrix(equation: equation, constants: constants, Z: Z, v: v) -> np.ndarray:
    # [ EQUATION ] [c]
    # [ EQUATION ] [c]
    # [ EQUATION ] [c]
    # [ EQUATION ] [c]
    # [    Z     ] [v]

    # Put constants on the right
    copy = np.hstack((equation, constants))

    bottom = np.append(Z, v)

    # Add the bottom row
    return np.vstack((copy, bottom))

def disassemble_matrix(matrix: matrix) -> tuple[equation, constants, Z, v]:
    # Separate bottom row
    Z = matrix[-1, :-1]
    v = matrix[-1, -1]

    # Remove bottom row
    sliced = matrix[:-1]

    # Separate constants into one column array
    constants = np.array([np.array([i]) for i in sliced[:, -1]])

    # Remove constants
    equation = sliced[:, :-1]

    return equation, constants, Z, v

def simplex(row_names: row_names, column_names: column_names, equation: equation, constants: constants, Z: Z, v: v, shape_override: tuple[int, int] = None) -> tuple[solution, solution]:
    # Since recieved equation was previously cut, I can't rely on it's shape
    shape = equation.shape if shape_override is None else shape_override
    
    ref_solution = np.array([0.] * shape[1])
    optimal_solution = np.array([0.] * shape[1])

    # Look for a negative value in the constants column
    while np.any(constants < 0):
        constants_row_i, _ = first_negative(constants)

        try:
            # Find a negative value in the row
            col, _ = first_negative(equation[constants_row_i])
        except IndexError as e:
            raise ValueError(f"Boundaries are contradictory: {e}")

        # Divide each element in the column by the element in the constants
        div_result = div_column_by_constants(equation, col, constants)
        
        # Find the minimum positive value
        row, _ = min_positive(div_result)

        row_names, column_names, matrix = jordan_elimination(row_names, column_names, assemble_matrix(equation, constants, Z, v), row, col)
        equation, constants, Z, v = disassemble_matrix(matrix)

    collect_solution(row_names, constants, ref_solution)

    # step = 0
    while np.any(Z < 0):
        col, _ = first_negative(Z)

        div_result = div_column_by_constants(equation, col, constants)
        row, _ = min_positive(div_result)

        row_names, column_names, matrix = jordan_elimination(row_names, column_names, assemble_matrix(equation, constants, Z, v), row, col)
        equation, constants, Z, v = disassemble_matrix(matrix)

        # step += 1
        # print_matrix(matrix, f"Step {step}:")

    collect_solution(row_names, constants, optimal_solution)

    return ref_solution, optimal_solution