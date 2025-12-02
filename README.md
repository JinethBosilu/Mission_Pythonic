# Mission: Pythonic

A Pygame-based educational game that teaches Python programming through hacker-themed missions.

## Features

- 🎮 **Full GUI Game Experience** - Pygame window with hacker/Matrix theme
- 🐍 **10 Progressive Levels** - Learn Python from variables to modules
- 💻 **In-Game Code Editor** - Write and test code in real-time
- 💾 **Auto-Save Progress** - Never lose your progress
- 🎯 **Simplified Challenges** - Clear objectives, immediate feedback
- 🏆 **Scoring & Ranks** - Track your hacker rank progression

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Mission_Pythonic.git
cd Mission_Pythonic

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Game Controls

- **Mouse**: Click buttons and menus
- **Keyboard**: Type code in editor
- **F5**: Run code
- **ESC**: Pause/Menu

## Level Overview

1. **Variables & I/O** - Rename secret files
2. **Data Types** - Convert encrypted passwords
3. **Conditionals** - Security system logic
4. **Loops** - Deactivate multiple alarms
5. **Lists** - Extract encrypted messages
6. **Dictionaries** - Map usernames to hints
7. **Functions** - Automate repetitive tasks
8. **File Handling** - Read hidden logs
9. **Classes** - Simulate hacker bots
10. **Modules** - Generate random passwords

## Development

### Project Structure
```
Mission_Pythonic/
├── main.py              # Game entry point
├── requirements.txt     # Dependencies
├── src/
│   ├── game_engine.py   # Pygame game loop
│   ├── ui/              # GUI components
│   ├── core/            # Game logic
│   └── levels/          # Level system
├── levels/              # Level JSON files
├── assets/              # Images, fonts, sounds
└── tests/               # Test suite
```

### Building Executable

For developers who want to build a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Run the build script
python build_game.py

# The executable will be in the dist/ folder
# Don't forget to include the levels/ folder when distributing
```

### Download Pre-built Executable

Check the [Releases](https://github.com/YOUR_USERNAME/Mission_Pythonic/releases) page for pre-built executables.

## License

MIT License

## Contributing

See CONTRIBUTING.md for guidelines on creating new levels.
