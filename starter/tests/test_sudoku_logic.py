import random
import sudoku_logic


def test_create_empty_board_shape_and_empty_values():
    board = sudoku_logic.create_empty_board()
    assert isinstance(board, list)
    assert len(board) == sudoku_logic.SIZE
    for row in board:
        assert len(row) == sudoku_logic.SIZE
        assert all(cell == sudoku_logic.EMPTY for cell in row)


def test_fill_board_generates_valid_completed_board():
    random.seed(0)
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(board) is True
    assert all(cell != sudoku_logic.EMPTY for row in board for cell in row)
    expected = set(range(1, sudoku_logic.SIZE + 1))
    for row in board:
        assert set(row) == expected
    for c in range(sudoku_logic.SIZE):
        col = [board[r][c] for r in range(sudoku_logic.SIZE)]
        assert set(col) == expected
    for br in range(0, sudoku_logic.SIZE, 3):
        for bc in range(0, sudoku_logic.SIZE, 3):
            vals = []
            for r in range(3):
                for c in range(3):
                    vals.append(board[br + r][bc + c])
            assert set(vals) == expected


def test_generate_puzzle_returns_puzzle_and_solution_of_expected_sizes():
    random.seed(1)
    clues = 35
    puzzle, solution = sudoku_logic.generate_puzzle(clues=clues)
    assert all(cell != sudoku_logic.EMPTY for row in solution for cell in row)
    nonzeros = sum(1 for row in puzzle for cell in row if cell != sudoku_logic.EMPTY)
    assert nonzeros == clues


def test_is_safe_detects_conflicts_and_allows_safe_values():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 0, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 5) is False
    assert sudoku_logic.is_safe(board, 0, 1, 3) is True


def test_deep_copy_returns_independent_copy():
    board = sudoku_logic.create_empty_board()
    copied = sudoku_logic.deep_copy(board)
    copied[0][0] = 9
    assert board[0][0] != 9
