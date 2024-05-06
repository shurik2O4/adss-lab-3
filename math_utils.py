from typing import Iterable
import numpy as np

row_names = column_names = list[tuple[str,int]]

def first_negative(arr: Iterable) -> tuple[int, float]:
    return filter(lambda x: x[1] < 0, enumerate(arr)).__next__()

def min_positive(arr: Iterable) -> tuple[int, float]:
    return min([(i, v) for i, v in enumerate(arr)], key=lambda x: x[1] if x[1] >= 0 else np.inf)

def div_column_by_constants(equation: np.ndarray, column: int, constants: np.ndarray) -> np.ndarray:
    print("Column with element:", equation[:, column])
    return np.array([c[0] for c in constants]) / equation[:, column]

def collect_solution(row_names: row_names, constants: np.ndarray, solution: np.ndarray) -> None:
    # If X is in the row, add the constant to the solution
    for i, (r, xi) in enumerate(row_names):
        if r == 'x':
            solution[xi - 1] = float(constants[i][0])