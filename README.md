# Lights Out

## Run
python game.py

## Files
- `game.py` - GUI.
- `logic.py` - Board state, moves, hints, undo, and generates the puzzle boards.
- `test.py` - Unit tests.
- `tkinter sample/sample.py` - Tkinter tutorial example.

The interface and game logic are decoupled: `game.py` handles display and passes actions to `logic.py`, which does not depend on Tkinter.