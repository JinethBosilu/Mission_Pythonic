# Changelog

All notable changes to Mission: Pythonic will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-02

### Added
- Complete GUI game with Pygame and pygame-gui
- 10 progressive Python learning levels (variables to modules)
- Interactive code editor with real-time execution
- Timer system with time limits per level
- Time penalty system (5 points per 10 seconds overtime, max 50)
- Pause menu (ESC key) with Resume/Restart/Menu/Quit options
- Timeout overlay with automatic detection and action buttons
- Trolling/sassy AI feedback system with 40+ unique messages
- Matrix/hacker-themed visual effects:
  - Particle system with physics
  - Matrix rain animation (50 columns)
  - Glow text rendering
  - Scan line effects
  - Pulsing animations
  - Corner brackets UI elements
- Auto-save progress system (stored in user profile)
- Level select screen with progress tracking
- Victory screen on completion
- Name input for player customization
- Hint system (3 hints per level with progressive sass)
- Solution reveal option (with shame messages)
- Next Level and Restart buttons
- Back to Menu and Quit buttons throughout
- Window resize support with timer preservation
- F5 keyboard shortcut for running code

### Technical
- Scene-based architecture (7 scenes)
- Safe code execution with RestrictedPython
- JSON-based level definitions
- Proper error handling and validation
- Git version control with detailed commits
- Comprehensive documentation

### UI/UX
- Centered text alignment throughout
- Proper z-order for overlays
- Hover effects on buttons
- Red flash effect on timeout
- Green-on-black Matrix color scheme
- Progress bar visualization
- Timer color warnings (green → red)
- Consistent visual theme across all scenes

### Bug Fixes
- Fixed timer reset on window resize
- Fixed timer reset on pause/resume
- Fixed timeout overlay appearing behind UI elements
- Fixed timeout message flickering
- Fixed pause menu alignment
- Fixed button overlap with borders
- Fixed scan line visibility in pause menu
- Fixed timeout state persistence when changing scenes

## [Unreleased]

### Planned Features
- Sound effects and background music
- More levels (advanced Python concepts)
- Achievements system
- Leaderboard/time trials
- Custom level editor
- Multiplayer/competitive mode

---

[1.0.0]: https://github.com/YOUR_USERNAME/Mission_Pythonic/releases/tag/v1.0.0
