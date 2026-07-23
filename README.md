# snake-py-terminal

Minimal Snake game for the terminal. No extra packages on Windows.

## Run

```powershell
python snake.py
```

Or double-click `run.bat`.

**Controls:** WASD or arrow keys · `q` to quit

## Requirements

- Python 3.10+
- Windows: PowerShell, Windows Terminal, or VS Code terminal (uses built-in `msvcrt`)
- Linux/macOS: uses stdlib `curses`

## Notes

- Run from a real terminal tab — not the VS Code "Run Python File" output panel.
- Rendering uses an alternate screen and updates only changed cells, so the board should not flash each frame.
- On Windows, the text cursor is hidden during play to avoid a black block appearing on the side of the terminal.

## Repo

https://github.com/sbf-developer/snake-py-terminal
