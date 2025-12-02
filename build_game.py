"""Build script to create executable for Mission: Pythonic game."""
import shutil
import os
from pathlib import Path
import sys

def build_executable():
    """Build the game executable using PyInstaller."""
    
    try:
        import PyInstaller.__main__
    except ImportError:
        print("ERROR: PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        sys.exit(1)
    
    print("=" * 50)
    print("Mission: Pythonic - Build Script")
    print("=" * 50)
    print()
    
    # Clean previous builds
    print("Cleaning previous builds...")
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # PyInstaller arguments
    args = [
        'main.py',
        '--name=MissionPythonic',
        '--onefile',
        '--windowed',
        '--add-data=levels;levels',
        '--icon=NONE',  # Add icon later if you have one
        '--clean',
        '--noconfirm',
    ]
    
    print("\nBuilding Mission: Pythonic executable...")
    print("This may take a few minutes...\n")
    
    PyInstaller.__main__.run(args)
    
    # Create distribution folder
    print("\nCreating distribution package...")
    dist_folder = Path("dist/MissionPythonic-Package")
    dist_folder.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path("dist/MissionPythonic.exe")
    if exe_source.exists():
        shutil.copy(exe_source, dist_folder / "MissionPythonic.exe")
        print(f"✓ Copied executable")
    else:
        print("✗ ERROR: Executable not found!")
        sys.exit(1)
    
    # Copy levels folder
    levels_source = Path("levels")
    levels_dest = dist_folder / "levels"
    if levels_source.exists():
        shutil.copytree(levels_source, levels_dest, dirs_exist_ok=True)
        print(f"✓ Copied levels folder")
    else:
        print("✗ WARNING: levels folder not found!")
    
    # Copy documentation
    docs = ["DISTRIBUTION.md", "LICENSE"]
    for doc in docs:
        doc_path = Path(doc)
        if doc_path.exists():
            shutil.copy(doc_path, dist_folder / doc)
            print(f"✓ Copied {doc}")
    
    print("\n" + "=" * 50)
    print("BUILD COMPLETE!")
    print("=" * 50)
    print(f"\nPackage location: {dist_folder.absolute()}")
    print("\nNext steps:")
    print("1. Test the executable in the package folder")
    print("2. Create a ZIP file of the package folder")
    print("3. Upload to GitHub releases")
    print("\nQuick command to create ZIP:")
    print(f"   Compress-Archive -Path '{dist_folder}' -DestinationPath MissionPythonic-v1.0.0-windows.zip")

if __name__ == "__main__":
    try:
        build_executable()
    except Exception as e:
        print(f"\n✗ BUILD FAILED: {e}")
        sys.exit(1)
