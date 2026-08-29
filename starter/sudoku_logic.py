import copy
import random

SIZE = 9
EMPTY = 0

# Difficulty presets map difficulty name to number of prefilled cells (clues)
# These are configurable and determine how many cells remain filled in the puzzle.
DIFFICULTY_PREFILLS = {
    'easy': 40,
    'medium': 35,
    'hard': 30,
}
def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def _find_empty_cells(board):
    return [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == EMPTY]


def _candidates(board, row, col):
    return [n for n in range(1, SIZE + 1) if is_safe(board, row, col, n)]


def count_solutions(board, max_solutions=2):
    """Count solutions for a given board, stopping early at max_solutions."""
    # Use recursive backtracking with MRV heuristic
    # Find empty cell with minimum remaining values
    # Return number of solutions found (capped at max_solutions)

    # Find any empty cell
    min_cell = None
    min_cands = None
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == EMPTY:
                cands = _candidates(board, r, c)
                if not cands:
                    return 0
                if min_cands is None or len(cands) < len(min_cands):
                    min_cands = cands
                    min_cell = (r, c)
    # No empty cells: one valid solution
    if min_cell is None:
        return 1

    r, c = min_cell
    count = 0
    for val in min_cands:
        board[r][c] = val
        count += count_solutions(board, max_solutions)
        board[r][c] = EMPTY
        if count >= max_solutions:
            return count
    return count


def remove_cells_unique(board, clues, max_restarts=5):
    """
    Remove cells while ensuring the puzzle has exactly one solution.
    If unable to reach desired number of clues after a number of restarts,
    this will restart with a new filled board.
    """
    # We operate in-place on board. The caller should copy if needed.
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    attempts = 0
    restarts = 0
    # Try to remove until desired number of non-empty cells == clues
    while True:
        random.shuffle(cells)
        for (r, c) in cells:
            if board[r][c] == EMPTY:
                continue
            # Tentatively remove
            backup = board[r][c]
            board[r][c] = EMPTY
            cnt = count_solutions(copy.deepcopy(board), max_solutions=2)
            if cnt != 1:
                # revert
                board[r][c] = backup
            else:
                # successful removal
                pass
            nonzeros = sum(1 for row in board for cell in row if cell != EMPTY)
            if nonzeros == clues:
                return
        # If we completed a pass without reaching desired clues, restart
        restarts += 1
        if restarts > max_restarts:
            raise RuntimeError("Unable to generate unique-solution puzzle after restarts")
        # Refill board and try again
        # Note: caller likely has a fresh filled board; here we signal failure
        return False

def generate_puzzle(clues=35, difficulty=None, max_restarts=10):
    """
    Generate a puzzle with exactly `clues` filled cells and a unique solution.
    This will attempt up to `max_restarts` times to produce such a puzzle.
    """
    # Allow callers to pass a difficulty instead of an explicit clues count.
    if difficulty is not None:
        if difficulty not in DIFFICULTY_PREFILLS:
            raise ValueError(f"unknown difficulty: {difficulty}")
        clues = DIFFICULTY_PREFILLS[difficulty]

    if clues < 17 or clues > SIZE * SIZE:
        raise ValueError("clues must be between 17 and 81")

    for attempt in range(max_restarts):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)

        # Work on a copy for removals
        puzzle_board = deep_copy(board)

        # Attempt to remove cells while keeping uniqueness
        try:
            res = remove_cells_unique(puzzle_board, clues, max_restarts=3)
            if res is False:
                # remove_cells_unique signals that this filled board couldn't be reduced
                continue
        except RuntimeError:
            continue

        # Final sanity check: ensure puzzle has exactly one solution
        cnt = count_solutions(deep_copy(puzzle_board), max_solutions=2)
        if cnt == 1:
            return puzzle_board, solution
    raise RuntimeError("Failed to generate a unique-solution puzzle")
