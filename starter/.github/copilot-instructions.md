# GitHub Copilot Instructions

## Project Overview

This project is a Flask-based Sudoku web application.

The project contains:
- A Python Flask backend
- Sudoku generation and solving logic
- A browser-based Sudoku UI using HTML, CSS, and JavaScript
- Difficulty levels
- Hint functionality
- Solution checking
- Game timer
- Scoreboard / fastest-times display
- Light and dark themes
- Automated pytest tests

## General Coding Standards

- Keep code simple, readable, and maintainable.
- Prefer clear and descriptive variable and function names.
- Follow existing project structure and coding style.
- Avoid unnecessary refactoring.
- Do not rewrite working code unless the requested feature requires it.
- Make the smallest safe change needed to implement a requirement.
- Do not introduce unnecessary dependencies.
- Preserve existing functionality when adding new features.
- Add comments only when they clarify non-obvious logic.

## Python / Flask

- Use standard Python conventions and readable formatting.
- Keep Flask routes focused and easy to understand.
- Validate user input at API boundaries.
- Return appropriate HTTP status codes and JSON responses for API errors.
- Do not expose internal exceptions or sensitive information to users.
- Preserve the existing application state and route behavior unless explicitly asked to change it.
- Keep Sudoku logic separate from Flask route handling where practical.

## Sudoku Logic

- Sudoku boards must remain valid 9x9 Sudoku boards.
- Preserve Sudoku row, column, and 3x3 box constraints.
- Generated puzzles must have valid solutions.
- Do not weaken or bypass existing Sudoku validation.
- Preserve the uniqueness requirements of generated puzzles.
- Difficulty levels should continue to behave consistently.

## Frontend

- Use semantic and accessible HTML where practical.
- Keep JavaScript organized and avoid unnecessary global state.
- Preserve existing game behavior when modifying the UI.
- Buttons and controls should remain usable with both mouse and keyboard.
- Maintain readable visual hierarchy and clear feedback for users.
- Do not introduce unnecessary frontend frameworks.

## Themes

- The application must support both light mode and dark mode.
- Theme changes must apply consistently to the entire application.
- Ensure sufficient contrast between text, backgrounds, buttons, inputs, and Sudoku cells.
- Do not break the existing theme when adding UI components.
- Theme preference should continue to persist if the existing implementation supports persistence.

## Timer and Scoreboard

- Preserve timer accuracy and existing timer behavior.
- Do not reset or alter the timer unexpectedly.
- Scoreboard entries must remain consistent with the existing data format.
- Do not break difficulty information or recorded completion times.

## Testing

Before considering a change complete:

1. Run the full pytest suite:
   `python -m pytest`

2. Confirm that all existing tests pass.

3. If a test fails, investigate the actual failure before making additional changes.

4. Do not modify or delete tests simply to make them pass unless explicitly requested.

5. Add tests for new backend behavior when appropriate.

6. Do not claim a feature is complete until the tests pass.

## Change Management

- Work incrementally.
- Before making broad changes, understand the existing implementation.
- For each requested feature, identify the relevant files first.
- Make one logical change at a time.
- Run tests after meaningful changes.
- Avoid unrelated changes to files outside the requested feature.
- Do not overwrite working functionality without a clear reason.

## Copilot Behavior

When assisting with this project:

- Start by inspecting the relevant existing code.
- Explain what needs to change before making broad modifications.
- Prefer targeted edits over complete rewrites.
- Preserve existing working features.
- If requirements are ambiguous, ask for clarification instead of guessing.
- After making changes, run the relevant tests.
- Report exactly what changed and whether tests passed.
- If tests cannot be run, clearly state that instead of claiming they passed.