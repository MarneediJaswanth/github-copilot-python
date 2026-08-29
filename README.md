# Sudoku — Flask Web Game

This repository contains a simple Sudoku web game built with Python and Flask. It provides a responsive, accessible UI and gameplay features suitable for desktop and mobile browsers.

## Main features
- Playable Sudoku board with client-side input
- Difficulty levels: Easy, Medium, Hard
- Unique-solution puzzle generation on the server
- Live invalid-entry feedback (per-cell validation)
- Check Solution button (server-side verification)
- Hint button that fills and locks one correct cell
- Timer to measure completion time
- Top 10 fastest-times scoreboard persisted in browser `localStorage`
- Dark / Light Mode with persisted preference
- Responsive and accessible UI (keyboard navigation, focus states)

## Technologies
- Python
- Flask
- HTML
- CSS
- JavaScript
- pytest (for unit / integration tests)

## Requirements / Prerequisites
- Python 3.8 or newer
- pip
- A modern web browser (Chrome, Firefox, Edge, Safari)

## Setup (Windows)
Open PowerShell and run:

```powershell
cd path\to\github-copilot-python\starter
python -m venv venv
# PowerShell (if execution policy prevents activation, run PowerShell as Administrator or use cmd)
.\venv\Scripts\Activate.ps1
# or cmd.exe
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Run the application
From the `starter` folder run:

```powershell
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Run tests
From the `starter` folder run:

```powershell
python -m pytest
```

Current test suite: 19 passing tests.

## Project structure
- `starter/` — application package and static assets
	- `app.py` — Flask application and JSON endpoints
	- `sudoku_logic.py` — generator and solver utilities
	- `templates/index.html` — main UI
	- `static/styles.css` — styles and themes
	- `static/main.js` — client behavior (board rendering, timer, scoreboard, theme)
	- `tests/` — pytest test suite
- `README.md` — this document

## Scoreboard and theme persistence
The Top 10 scoreboard and the user's theme preference are stored in the browser using `localStorage`. Scores include `name`, `time` (seconds), and `difficulty`. Theme preference is saved under `sudoku_theme` and restored on page load.

## How to use the game
1. Open the app in your browser.
2. Choose a `Difficulty` (Easy / Medium / Hard) and click `New Game`.
3. Fill cells with numbers 1–9. Invalid entries are highlighted immediately.
4. Use `Check Solution` to validate the full board.
5. Click `Hint` to fill one correct empty cell — the hinted cell becomes locked.
6. Timer starts on a new game and stops on solve; you can save your name to the Top 10 scoreboard when you finish.

## Screenshots and milestones
If present, a `Screenshots/` folder contains Copilot milestone screenshots demonstrating UI changes and accessibility improvements. These images illustrate responsive layouts, dark mode, keyboard navigation, and hint/incorrect cell visuals.

---
If you notice anything that doesn't match the running application (behavior or tests), please open an issue or share the failing test output and I will help diagnose and fix it.
