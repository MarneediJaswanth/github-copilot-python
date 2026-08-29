// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
// Timer state
let timerInterval = null;
let elapsedSeconds = 0;

function formatTime(s) {
  return `Time: ${s}s`;
}

function applyTheme(theme) {
  if (theme === 'dark') {
let currentPuzzleId = null;
    document.body.classList.add('dark');
  } else {
    document.body.classList.remove('dark');
  }
}

function updateTimerDisplay() {
  const el = document.getElementById('timer');
  if (el) el.innerText = formatTime(elapsedSeconds);
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function resetTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
}

function checkForSolved() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  let anyEmpty = false;
  for (let i = 0; i < inputs.length; i++) {
    const inp = inputs[i];
    if (inp.value === '') {
      anyEmpty = true;
      break;
    }
    if (inp.classList.contains('incorrect')) {
      return false;
    }
  }
  if (!anyEmpty) {
    // solved
    stopTimer();
    const msg = document.getElementById('message');
    if (msg) {
      msg.style.color = '#388e3c';
      msg.innerText = 'Congratulations! You solved it!';
      // show save score UI so player can record their time
      showSaveScoreUI();
    }
    return true;
  }
  return false;
}

// Scoreboard / localStorage helpers
function getStoredScores() {
  try {
    const raw = localStorage.getItem('sudoku_top_scores');
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

function saveScoresList(list) {
  localStorage.setItem('sudoku_top_scores', JSON.stringify(list));
}

function saveScoreLocal(name, time, difficulty) {
  const scores = getStoredScores();
  scores.push({name: name || 'Anonymous', time: time, difficulty: difficulty});
  scores.sort((a, b) => a.time - b.time);
  const trimmed = scores.slice(0, 10);
  saveScoresList(trimmed);
  renderScores();
}

function renderScores() {
  const scores = getStoredScores();
  const tbody = document.querySelector('#scoreboard tbody');
  const empty = document.getElementById('scoreboard-empty');
  tbody.innerHTML = '';
  if (!scores || scores.length === 0) {
    if (empty) empty.style.display = 'block';
    return;
  }
  if (empty) empty.style.display = 'none';
  scores.forEach((s, idx) => {
    const tr = document.createElement('tr');
    const rankTd = document.createElement('td'); rankTd.innerText = String(idx + 1);
    const nameTd = document.createElement('td'); nameTd.innerText = s.name;
    const timeTd = document.createElement('td'); timeTd.innerText = String(s.time);
    const diffTd = document.createElement('td'); diffTd.innerText = s.difficulty;
    tr.appendChild(rankTd); tr.appendChild(nameTd); tr.appendChild(timeTd); tr.appendChild(diffTd);
    tbody.appendChild(tr);
  });
}

function showSaveScoreUI() {
  const panel = document.getElementById('save-score');
  if (!panel) return;
  panel.classList.remove('hidden');
  const nameInput = document.getElementById('player-name');
  if (nameInput) nameInput.focus();
}

function hideSaveScoreUI() {
  const panel = document.getElementById('save-score');
  if (!panel) return;
  panel.classList.add('hidden');
  const nameInput = document.getElementById('player-name');
  if (nameInput) nameInput.value = '';
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.setAttribute('inputmode', 'numeric');
      input.setAttribute('pattern', '[1-9]*');
      input.setAttribute('aria-label', `Row ${i+1} Column ${j+1}`);
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        // Provide immediate feedback for the entered value by asking server
        // whether this single cell is correct. Do nothing for empty values.
        const row = parseInt(e.target.dataset.row, 10);
        const col = parseInt(e.target.dataset.col, 10);
        if (!val) {
          // clear any incorrect mark when user deletes
          e.target.classList.remove('incorrect');
          return;
        }
        fetch('/check_cell', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({row, col, value: parseInt(val, 10)})
        }).then(r => r.json()).then(data => {
          if (data && data.correct === true) {
            e.target.classList.remove('incorrect');
          } else if (data && data.correct === false) {
            e.target.classList.add('incorrect');
          }
          // After updating cell correctness, check for solved state.
          checkForSolved();
        }).catch(() => {
          // on error, be conservative and do not mark as correct
        });
      });
      // keyboard navigation for arrow keys and Enter/Backspace
      input.addEventListener('keydown', (e) => {
        const row = parseInt(input.dataset.row, 10);
        const col = parseInt(input.dataset.col, 10);
        function focusCell(r, c) {
          if (r < 0 || r >= SIZE || c < 0 || c >= SIZE) return false;
          const idx = r * SIZE + c;
          const boardInputs = boardDiv.getElementsByTagName('input');
          const target = boardInputs[idx];
          if (!target) return false;
          if (target.disabled) return false;
          target.focus();
          return true;
        }
        switch (e.key) {
          case 'ArrowLeft': e.preventDefault(); focusCell(row, col - 1); break;
          case 'ArrowRight': e.preventDefault(); focusCell(row, col + 1); break;
          case 'ArrowUp': e.preventDefault(); focusCell(row - 1, col); break;
          case 'ArrowDown': e.preventDefault(); focusCell(row + 1, col); break;
          case 'Enter': e.preventDefault(); focusCell(row + 1 < SIZE ? row + 1 : row, col); break;
          case 'Backspace':
            // allow deletion and move left
            if (input.value === '') { e.preventDefault(); input.classList.remove('incorrect'); focusCell(row, col - 1); }
            break;
          default:
            break;
        }
      });
      // apply alternating 3x3 block styling via class
      const blockRow = Math.floor(i / 3);
      const blockCol = Math.floor(j / 3);
      if (((blockRow + blockCol) % 2) === 0) {
        input.classList.add('block-alt');
      }
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  let currentPuzzleId = null;
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.setAttribute('aria-disabled', 'true');
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty')?.value || 'medium';
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  currentPuzzleId = data.puzzle_id;
  document.getElementById('message').innerText = '';
  // reset and start timer when a new game begins
  resetTimer();
  startTimer();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board, puzzle_id: currentPuzzleId})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
    // stop timer when server confirms puzzle solved
    stopTimer();
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  // Ensure Hint button exists in case the HTML template wasn't updated or cached.
  const controls = document.querySelector('.controls');
  if (controls && !document.getElementById('hint')) {
    const hintBtn = document.createElement('button');
    hintBtn.id = 'hint';
    hintBtn.innerText = 'Hint';
    // insert before the message span if present
    const msg = document.getElementById('message');
    if (msg) controls.insertBefore(hintBtn, msg);
    else controls.appendChild(hintBtn);
  }
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', async () => {
    const boardDiv = document.getElementById('sudoku-board');
    const inputs = boardDiv.getElementsByTagName('input');
    const board = [];
    for (let i = 0; i < SIZE; i++) {
      board[i] = [];
      for (let j = 0; j < SIZE; j++) {
        const idx = i * SIZE + j;
        const val = inputs[idx].value;
        board[i][j] = val ? parseInt(val, 10) : 0;
      }
    }
    const res = await fetch('/hint', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board, puzzle_id: currentPuzzleId})
    });
    const data = await res.json();
    const msg = document.getElementById('message');
    if (data.error) {
      msg.style.color = '#d32f2f';
      msg.innerText = data.error;
      return;
    }
    const r = data.row, c = data.col, v = data.value;
    const idx = r * SIZE + c;
    const inp = inputs[idx];
    if (!inp.disabled && inp.value === '') {
      inp.value = v;
      inp.disabled = true;
      inp.setAttribute('aria-disabled', 'true');
      inp.classList.remove('incorrect');
      inp.classList.add('hinted');
      inp.setAttribute('title', 'Hinted cell');
      msg.style.color = '#388e3c';
      msg.innerText = `Hint applied at row ${r+1}, col ${c+1}`;
      // After a hint is applied, check whether puzzle is solved.
      checkForSolved();
    } else {
      msg.style.color = '#d32f2f';
      msg.innerText = 'No valid empty cell to hint.';
    }
  });
  // Scoreboard save/cancel handlers
  const saveBtn = document.getElementById('save-score-btn');
  const cancelBtn = document.getElementById('cancel-save-btn');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      const name = document.getElementById('player-name')?.value || 'Anonymous';
      const difficulty = document.getElementById('difficulty')?.value || 'medium';
      // elapsedSeconds holds the completion time
      saveScoreLocal(name, elapsedSeconds, difficulty);
      hideSaveScoreUI();
      const msg = document.getElementById('message');
      if (msg) { msg.style.color = '#388e3c'; msg.innerText = 'Score saved.'; }
    });
  }
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => { hideSaveScoreUI(); });
  }
  // render existing scores on load
  renderScores();
  // Theme: restore from localStorage or use default
  const theme = localStorage.getItem('sudoku_theme') || 'light';
  applyTheme(theme);
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.body.classList.contains('dark') ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('sudoku_theme', next);
      themeToggle.setAttribute('aria-pressed', next === 'dark' ? 'true' : 'false');
      themeToggle.innerText = next === 'dark' ? 'Light Mode' : 'Dark Mode';
    });
    // set initial label
    themeToggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    themeToggle.innerText = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
  }
  // initialize
  newGame();
});