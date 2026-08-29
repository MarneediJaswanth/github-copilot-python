import json
import copy
import app as sudoku_app_module


# Simple backtracking solver used only in tests to derive the solution from a
# returned puzzle without touching server internals.
def solve_puzzle(puzzle):
    size = sudoku_app_module.sudoku_logic.SIZE
    board = copy.deepcopy(puzzle)

    def find_empty():
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    return r, c
        return None

    def backtrack():
        loc = find_empty()
        if not loc:
            return True
        r, c = loc
        for n in range(1, size + 1):
            if sudoku_app_module.sudoku_logic.is_safe(board, r, c, n):
                board[r][c] = n
                if backtrack():
                    return True
                board[r][c] = 0
        return False

    ok = backtrack()
    if not ok:
        raise RuntimeError('test helper failed to solve puzzle')
    return board


def test_index_route_returns_html(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Sudoku Game' in resp.data


def test_new_route_returns_puzzle_and_puzzle_id(client):
    resp = client.get('/new?clues=30')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'puzzle' in data
    assert 'puzzle_id' in data
    puzzle = data['puzzle']
    assert len(puzzle) == sudoku_app_module.sudoku_logic.SIZE


def test_check_route_with_correct_solution_returns_no_incorrect(client):
    # Generate a normal puzzle and derive its solution using the test solver
    resp = client.get('/new')
    assert resp.status_code == 200
    data = resp.get_json()
    puzzle = data['puzzle']
    puzzle_id = data['puzzle_id']
    solution = solve_puzzle(puzzle)
    resp = client.post('/check', data=json.dumps({'board': solution, 'puzzle_id': puzzle_id}),
                       content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'incorrect' in data
    assert data['incorrect'] == []


def test_check_route_without_puzzle_id_returns_400(client):
    resp = client.post('/check', data=json.dumps({'board': []}),
                       content_type='application/json')
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_check_route_with_invalid_puzzle_id_returns_400(client):
    resp = client.post('/check', data=json.dumps({'board': [], 'puzzle_id': 'nope'}),
                       content_type='application/json')
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_check_cell_endpoint(client):
    # Generate a normal puzzle and pick a cell that's already filled
    resp = client.get('/new')
    assert resp.status_code == 200
    data = resp.get_json()
    puzzle = data['puzzle']
    puzzle_id = data['puzzle_id']
    # find a filled cell
    size = sudoku_app_module.sudoku_logic.SIZE
    filled = None
    for r in range(size):
        for c in range(size):
            if puzzle[r][c] != 0:
                filled = (r, c)
                break
        if filled:
            break
    assert filled is not None
    r, c = filled
    correct_val = puzzle[r][c]
    # correct
    resp = client.post('/check_cell', json={'row': r, 'col': c, 'value': correct_val, 'puzzle_id': puzzle_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get('correct') is True
    # incorrect (choose a different value)
    wrong = 1 if correct_val != 1 else 2
    resp = client.post('/check_cell', json={'row': r, 'col': c, 'value': wrong, 'puzzle_id': puzzle_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get('correct') is False


def test_hint_endpoint_returns_valid_hint(client):
    # Generate a normal puzzle and request a hint for it
    resp = client.get('/new')
    assert resp.status_code == 200
    data = resp.get_json()
    puzzle = data['puzzle']
    puzzle_id = data['puzzle_id']
    # find empties
    size = sudoku_app_module.sudoku_logic.SIZE
    empties = [(r, c) for r in range(size) for c in range(size) if puzzle[r][c] == 0]
    assert empties
    resp = client.post('/hint', json={'board': puzzle, 'puzzle_id': puzzle_id})
    assert resp.status_code == 200
    data = resp.get_json()
    hr, hc, hv = data['row'], data['col'], data['value']
    assert (hr, hc) in empties
    # compute solution locally and verify returned value is correct
    solution = solve_puzzle(puzzle)
    assert solution[hr][hc] == hv


def test_hint_endpoint_no_empty_returns_400(client):
    # Generate a normal puzzle and locally solve it; posting the solved board should return 400
    resp = client.get('/new')
    assert resp.status_code == 200
    data = resp.get_json()
    puzzle = data['puzzle']
    puzzle_id = data['puzzle_id']
    solution = solve_puzzle(puzzle)
    resp = client.post('/hint', json={'board': solution, 'puzzle_id': puzzle_id})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_missing_and_invalid_puzzle_id_endpoints(client):
    # missing puzzle_id
    resp = client.post('/check_cell', json={'row': 0, 'col': 0, 'value': 1})
    assert resp.status_code == 400
    resp = client.post('/hint', json={'board': []})
    assert resp.status_code == 400
    # invalid puzzle_id
    resp = client.post('/check_cell', json={'row': 0, 'col': 0, 'value': 1, 'puzzle_id': 'bad'})
    assert resp.status_code == 400
    resp = client.post('/hint', json={'board': [], 'puzzle_id': 'bad'})
    assert resp.status_code == 400


def test_multi_client_puzzle_ids_are_independent():
    # create two separate test clients and ensure they each get a puzzle_id
    c1 = sudoku_app_module.app.test_client()
    c2 = sudoku_app_module.app.test_client()
    r1 = c1.get('/new?clues=30').get_json()
    r2 = c2.get('/new?clues=30').get_json()
    assert 'puzzle_id' in r1 and 'puzzle_id' in r2
    assert r1['puzzle_id'] != r2['puzzle_id']
