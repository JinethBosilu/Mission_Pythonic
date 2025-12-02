# Creating a Release

This guide explains how to build and release Mission: Pythonic.

## Build Process

### 1. Install Build Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-build.txt
```

### 2. Build the Executable

```bash
python build_game.py
```

This creates:
- `dist/MissionPythonic.exe` - The standalone executable

### 3. Prepare Distribution Package

Create a folder structure for distribution:

```
MissionPythonic-v1.0.0/
├── MissionPythonic.exe
├── levels/
│   ├── level_001.json
│   ├── level_002.json
│   └── ... (all level files)
├── DISTRIBUTION.md
└── LICENSE
```

### 4. Create ZIP Archive

```bash
# Windows PowerShell
Compress-Archive -Path MissionPythonic-v1.0.0 -DestinationPath MissionPythonic-v1.0.0-windows.zip

# Linux/macOS
zip -r MissionPythonic-v1.0.0-windows.zip MissionPythonic-v1.0.0/
```

## GitHub Release

### 1. Tag the Release

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 2. Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Select the tag you just created (v1.0.0)
4. Fill in the release information:

**Release Title**: `Mission: Pythonic v1.0.0`

**Description Template**:
```markdown
# Mission: Pythonic v1.0.0

A hacker-themed Python learning game with 10 progressive missions.

## 🎮 What's New

- Complete Python learning journey from variables to modules
- Interactive code editor with real-time feedback
- Timer system with penalties for extra challenge
- Sassy AI feedback to keep you motivated
- Beautiful Matrix-inspired UI with particle effects
- Auto-save progress system

## 📦 Download

**Windows**: Download `MissionPythonic-v1.0.0-windows.zip`

### System Requirements
- Windows 10 or later
- 512 MB RAM
- 50 MB disk space
- 1280x720 minimum resolution

## 🚀 Quick Start

1. Download and extract the ZIP file
2. Run `MissionPythonic.exe`
3. Enter your agent name
4. Start coding!

## 📝 Controls

- **F5** or **RUN** button: Execute code
- **ESC**: Pause menu
- **Mouse/Keyboard**: Navigate and code

## 🐛 Known Issues

None at this time. Report bugs in the Issues section.

## 🎓 Learning Path

The game includes 10 missions covering:
- Variables & I/O
- Data Types
- Conditionals
- Loops
- Lists
- Dictionaries
- Functions
- File Handling
- Classes & Objects
- Modules

## 💝 Support

Enjoy the game? Star the repository and share with friends learning Python!

---

**Full changelog**: https://github.com/YOUR_USERNAME/Mission_Pythonic/compare/v0.9.0...v1.0.0
```

### 3. Upload Assets

Drag and drop these files to the release:
- `MissionPythonic-v1.0.0-windows.zip` (main distribution)
- Source code will be automatically added by GitHub

### 4. Publish Release

Click "Publish release" when ready.

## Version Numbering

Use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes or complete overhauls
- **MINOR**: New features, new levels
- **PATCH**: Bug fixes, small improvements

Examples:
- `v1.0.0` - Initial release
- `v1.1.0` - Added 5 new levels
- `v1.0.1` - Fixed timer bug

## Testing Before Release

Before publishing, test the executable on a clean Windows machine:

1. Extract the ZIP to a new folder
2. Run the game
3. Complete at least 3 levels
4. Test pause/resume
5. Test window resize
6. Verify saves work correctly
7. Check all buttons and menus

## Checklist

- [ ] All tests passing
- [ ] Version number updated in game
- [ ] CHANGELOG.md updated
- [ ] Executable built and tested
- [ ] ZIP file created
- [ ] Git tag created
- [ ] GitHub release created
- [ ] Release notes written
- [ ] Assets uploaded
- [ ] Release published
- [ ] README links updated

## Post-Release

1. Update README.md with latest release link
2. Announce on social media
3. Monitor issues for bugs
4. Thank contributors

---

Happy releasing! 🚀
