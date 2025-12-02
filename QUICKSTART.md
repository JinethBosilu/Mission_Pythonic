# Mission: Pythonic - Quick Start Guide

## Installation

1. **Clone or download** the repository
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

Simply run:
```bash
python main.py
```

Or from the src directory:
```bash
python -m src.game
```

## First Time Playing

1. **Title Screen**: Press the "PRESS START" button
2. **Enter Name**: Type your hacker codename
3. **Level Select**: Choose any level to start
4. **Gameplay**: 
   - Read the mission log and objective
   - Write Python code in the editor
   - Press F5 or click "RUN" to test your code
   - Use "HINT" for help if stuck
   - Use "SHOW SOLUTION" to see the answer

## Controls

- **F5**: Run code
- **ESC**: Not currently used (use BACK TO MENU button)
- **Mouse**: Click buttons and type in code editor

## Levels Overview

1. **Variables & I/O**: Learn about variables and printing
2. **Data Types**: Convert between strings and numbers
3. **Conditionals**: Use if/else statements
4. **Loops**: Iterate with for loops
5. **Lists**: Access list elements
6. **Dictionaries**: Work with key-value pairs
7. **Functions**: Define and call functions
8. **File Handling**: Read files
9. **Classes**: Create objects
10. **Modules**: Import and use libraries

## Tips

- Start with Level 1 and progress sequentially
- Each level builds on previous concepts
- Don't be afraid to use hints!
- Your progress is automatically saved
- Try to solve it yourself before viewing the solution

## Troubleshooting

**Game won't start?**
- Make sure pygame is installed: `pip install pygame pygame-gui`
- Check Python version (3.8+ required)

**Code won't run?**
- Check for syntax errors
- Make sure you're printing the output
- Read the objective carefully

**Level won't complete?**
- Your output must match exactly what's expected
- Check capitalization and spacing

## Save File Location

Progress is saved to: `~/.mission_pythonic/progress.json`

You can delete this file to start over.

## Have Fun!

Enjoy learning Python through hacking missions! 🐍💻🔓
