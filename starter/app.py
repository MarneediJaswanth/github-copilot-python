from flask import Flask, render_template, jsonify, request  # type: ignore[import]
import random
import uuid
import time
import sudoku_logic

app = Flask(__name__)

# Server-side puzzle store: puzzle_id -> {puzzle, solution, created_at}
PUZZLES = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    # Accept either an explicit `clues` parameter or a `difficulty` parameter.
    difficulty = request.args.get('difficulty')
    clues_arg = request.args.get('clues')
    if clues_arg is not None:
        clues = int(clues_arg)
        puzzle, solution = sudoku_logic.generate_puzzle(clues=clues)
    else:
        puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)
    # store server-side and return opaque puzzle_id to client
    puzzle_id = str(uuid.uuid4())
    PUZZLES[puzzle_id] = {
        'puzzle': puzzle,
        'solution': solution,
        'created_at': int(time.time())
    }
    return jsonify({'puzzle': puzzle, 'puzzle_id': puzzle_id})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    puzzle_id = data.get('puzzle_id')
    if not puzzle_id:
        return jsonify({'error': 'missing puzzle_id'}), 400
    entry = PUZZLES.get(puzzle_id)
    if entry is None:
        return jsonify({'error': 'invalid puzzle_id'}), 400
    solution = entry.get('solution')
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})


@app.route('/check_cell', methods=['POST'])
def check_cell():
    data = request.json
    row = data.get('row')
    col = data.get('col')
    value = data.get('value')
    puzzle_id = data.get('puzzle_id')
    if not puzzle_id:
        return jsonify({'error': 'missing puzzle_id'}), 400
    entry = PUZZLES.get(puzzle_id)
    if entry is None:
        return jsonify({'error': 'invalid puzzle_id'}), 400
    solution = entry.get('solution')
    try:
        r = int(row)
        c = int(col)
        v = int(value)
    except Exception:
        return jsonify({'error': 'invalid input'}), 400
    if r < 0 or r >= sudoku_logic.SIZE or c < 0 or c >= sudoku_logic.SIZE:
        return jsonify({'error': 'index out of range'}), 400
    correct = solution[r][c] == v
    return jsonify({'correct': correct})


@app.route('/hint', methods=['POST'])
def hint():
    data = request.json
    board = data.get('board')
    puzzle_id = data.get('puzzle_id')
    if not puzzle_id:
        return jsonify({'error': 'missing puzzle_id'}), 400
    entry = PUZZLES.get(puzzle_id)
    if entry is None:
        return jsonify({'error': 'invalid puzzle_id'}), 400
    solution = entry.get('solution')
    if board is None or not isinstance(board, list):
        return jsonify({'error': 'invalid board'}), 400
    empties = []
    for r in range(sudoku_logic.SIZE):
        for c in range(sudoku_logic.SIZE):
            try:
                val = board[r][c]
            except Exception:
                return jsonify({'error': 'invalid board shape'}), 400
            if val == 0:
                empties.append((r, c))
    if not empties:
        return jsonify({'error': 'no empty cells'}), 400
    # choose one empty cell at random
    r, c = random.choice(empties)
    v = solution[r][c]
    return jsonify({'row': r, 'col': c, 'value': v})

if __name__ == '__main__':
    app.run(debug=True)