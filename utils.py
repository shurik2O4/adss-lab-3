import sys
from typing import Callable, TextIO
import numpy as np
from sys import argv
import re

NO_PROMPTS = "-q" in argv

def input_matrix(prompt: str = "Matrix:", print_back = True) -> np.ndarray:
    """Wrapper function."""
    matrix = _input_matrix(prompt)
    if print_back:
        print_matrix(matrix, "Input matrix:")
    return matrix

def _input_matrix(prompt) -> np.ndarray:
    if not NO_PROMPTS:
        print(prompt)
    data = []
    while True:
        try:
            line_msg = f"L{len(data) + 1} >> " if not NO_PROMPTS else ""
            i = input(line_msg)
            if len(i) == 0:
                break
            # if i == "s":
            #     data = [[1.0, 3.0, 3.0, 5.0], [4.0, 5.0, 6.0, 6.0], [9.0, 8.0, 7.0, 7.0], [1.0, 2.0, 3.0, 4.0]]
            #     break
            # if i == "d":
            #     data = [[1.0, 2.0, 3.0, 4.0, 5.0], [6.0, 7.0, 8.0, 9.0, 6.0], [3.0, 7.0, 8.0, 7.0, 2.0]]
            #     break
            # if i == "e":
            #     data = [[1.0, 5.0, 3.0, -4.0, 20.0], 
            #             [3.0, 1.0, -2.0, 0.0, 9.0],
            #             [5.0, -7.0, 0.0, 10.0, -9.0],
            #             [0.0, 3.0, -5.0, 0.0, 1.0]]
            #     break
            data.append(list(map(float, i.split(" "))))
        except KeyboardInterrupt:
            print()
            exit(0)
        # End of file
        except EOFError:
            break
    return np.array(data)
    
def print_matrix(matrix: np.ndarray, msg: str = "Matrix:", round: int = 2) -> None:
    copy = np.round(matrix, round)
    print(msg)
    print(copy)

def print_exc_and_exit(e: Exception) -> None:
    print(e)
    exit(1)


def choice_input(choices: list[str], prompt: str = "Choice ($): ") -> str:
    s = prompt.replace("$", ', '.join([str(c) for c in choices]))
    while True:
        if not NO_PROMPTS:
            print(s,end='')
            try:
                i = input()
                if i in choices:
                    return i
                else:
                    print("Invalid choice")
            except KeyboardInterrupt:
                print()
                exit(0)
            except EOFError:
                break
            except ValueError as e:
                print(e)

def input_float_list(prompt: str = "Enter a list of numbers: ") -> list[float]:
    while True:
        try:
            i = input(prompt)
            return list(map(float, i.strip().split(" ")))
        except KeyboardInterrupt:
            print()
            exit(0)
        except EOFError:
            break
        except ValueError as e:
            print(e)

__LIMIT_EQUASION_REGEX = re.compile(r"^([-,\+]?\d{0,}x\d+)+->(min|max)$")
__EQUATION_REGEX = re.compile(r"^([-,\+]?\d{0,}x\d+)+=(\d+)$")
__EQUATION_MEMBER_REGEX = re.compile(r"([-,\+]?\d{0,})x(\d+)")

def __valid_limit_equation(s: str) -> bool:
    return __LIMIT_EQUASION_REGEX.match(s) is not None

def __valid_inequality(s: str) -> bool:
    return __EQUATION_REGEX.match(s) is not None

def __parse_numeric(s: str) -> float:
    """Python won't parse a string like '+', '-' as a number so here's a crutch. 🩼"""
    if len(s) == 0 or s == '+': return 1
    if s == '-': return -1
    return float(s)
    
def __parse_equation(eq: str) -> list[float]:
    # Gather matching parts
    parts = [(__parse_numeric(m.group(1)), int(m.group(2))) for m in __EQUATION_MEMBER_REGEX.finditer(eq)]
    # Prepare a list of coefficients (i.e. the only thing we care about)
    equation = [0] * max(member[1] for member in parts)
    # Put the coefficients in the right places
    for member in parts:
        equation[member[1] - 1] = member[0]
    
    return equation

def input_limit_equation(prompt: str = "Limit equation: ") -> tuple[np.ndarray, str]:
    # Get and validate input
    while True:
        try:
            s = input(prompt).replace(" ", "")
            if not __valid_limit_equation(s):
                print(f"Invalid limit equation: '{s}'")
                continue
            parts = s.split("->")
            # Parse the equation
            equation = np.array(__parse_equation(parts[0]))

            # Return the parsed equation and the optimization type
            return equation, parts[1]
        except KeyboardInterrupt:
            print()
            exit(0)
        except EOFError:
            break
        except ValueError as e:
            print(e)

def input_equation_system(prompt: str = "Equation system: ") -> tuple[np.ndarray, np.ndarray]:
    # Get and validate input
    rows = []
    print(prompt)
    while True:
        try:
            # Read a line
            s = input(f"EQ{len(rows)} >> ").replace(" ", "")
            # Exit if empty
            if s == "":
                break
            # Check if valid
            if not __EQUATION_REGEX.match(s):
                print(f"Invalid equation: '{s}'")
                continue
            # Store it
            rows.append(s)
        except KeyboardInterrupt:
            print()
            exit(0)
        except EOFError:
            break
        except ValueError as e:
            print(e)

    # Parse into a list of values
    equations = []
    constants = []
    for row in rows:
        # Split the equation
        parts = row.split("=")
        # Parse members
        members = __parse_equation(parts[0])
        # Extract the constant
        const = float(parts[1])
        # and the inequation operator
        operator = parts[0][-1]

        # If the operator is '>' we need to negate the equation
        # and change the sign of the constant
        if operator == '>':
            members = [-m for m in members]
            const = -const
            operator = '<'

        # Add the equation to the list
        equations.append(members)
        # And the constant (copy the value, not a reference)
        constants.append([float(const)])

    # Pad the equations with 0s to make them the same length
    max_len = max(len(eq) for eq in equations)
    for eq in equations:
        eq += [0] * (max_len - len(eq))
    
    return np.array(equations), np.array(constants)


def create_names(n: str, range: range) -> list[tuple[str, int]]:
    return [(n, i + 1) for i in range]