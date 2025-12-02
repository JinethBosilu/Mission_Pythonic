@echo off
echo ================================
echo Mission: Pythonic - Build Script
echo ================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo.

echo Installing build dependencies...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo.

echo Building executable...
python build_game.py
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.

echo ================================
echo Build Complete!
echo ================================
echo.
echo Executable location: dist\MissionPythonic.exe
echo.
echo Next steps:
echo 1. Copy the 'levels' folder to the dist folder
echo 2. Copy DISTRIBUTION.md and LICENSE to the dist folder
echo 3. Create a ZIP file of the dist folder
echo 4. Upload to GitHub releases
echo.
pause
