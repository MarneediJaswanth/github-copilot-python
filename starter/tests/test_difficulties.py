import random
import sudoku_logic


def _count_prefilled(board):
    return sum(1 for row in board for cell in row if cell != sudoku_logic.EMPTY)


def test_difficulties_generate_and_are_unique():
    random.seed(3)
    difficulties = ['easy', 'medium', 'hard']
    results = {}
    for diff in difficulties:
        puzzle, solution = sudoku_logic.generate_puzzle(difficulty=diff)
        assert all(cell != sudoku_logic.EMPTY for row in solution for cell in row)
        cnt = sudoku_logic.count_solutions([row[:] for row in puzzle], max_solutions=2)
        assert cnt == 1
        results[diff] = _count_prefilled(puzzle)

    # Check ordering: easy > medium > hard
    assert results['easy'] > results['medium']
    assert results['medium'] > results['hard']


def test_app_new_route_respects_difficulty(client):
    # Ensure API accepts difficulty and returns puzzle of expected prefilled count
    resp = client.get('/new?difficulty=easy')
    assert resp.status_code == 200
    data = resp.get_json()
    puzzle = data['puzzle']
    prefilled = _count_prefilled(puzzle)
    assert prefilled == sudoku_logic.DIFFICULTY_PREFILLS['easy']