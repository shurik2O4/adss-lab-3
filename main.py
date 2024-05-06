#!/usr/bin/env python3
from math_utils import *
from simplex import *
from utils import *
from lab3 import *

# Get input
Z, limit = input_limit_equation("Z=")

# If the limit is max, invert
if limit == "max":
    Z = -Z
else:
    # When assembling a matrix, coefficients are inverted
    # Since max Z = -min Z', we can just set change limit to max
    limit = "max"

equations, constants = input_equation_system("Boundaries:")
# Store for later
original_shape = (equations.shape[0], equations.shape[1])

j = float(input("j="))
v = 0.

print_matrix(assemble_matrix(equations, constants, Z, v), "Simplex matrix:")

rows = create_names('0', range(equations.shape[0]))
columns = create_names('x', range(equations.shape[1]))

# Solve the matrix (reference solution)
rows, columns, equation, constants, Z, v = remove_0s_rows(rows, columns, equations, constants, Z, v)

print_matrix(assemble_matrix(equation, constants, Z, v), "Simplex matrix after removing 0's:")

#                                                                                              Just another 🩼
reference_solution, optimal_solution = simplex(rows, columns, equation, constants, Z, v, shape_override=original_shape)

print(f"Reference solution: X: ({'; '.join([str(round(i, 3)) for i in reference_solution])})")
print(f"Optimal solution: X: ({'; '.join([str(round(i, 3)) for i in optimal_solution])})")