import random
import sudoku_logic


def test_generated_puzzle_has_unique_solution():
    random.seed(2)
    clues = 30
    puzzle, solution = sudoku_logic.generate_puzzle(clues=clues)
    # Ensure solution is full
    assert all(cell != sudoku_logic.EMPTY for row in solution for cell in row)
    # Ensure puzzle has requested number of clues
    nonzeros = sum(1 for row in puzzle for cell in row if cell != sudoku_logic.EMPTY)
    assert nonzeros == clues
    # Ensure uniqueness
    cnt = sudoku_logic.count_solutions([row[:] for row in puzzle], max_solutions=2)
    assert cnt == 1
