#!/usr/bin/env python3
"""
Build script for Chat Analyzer executable
Run: python build.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_pyinstaller():
    try:
        import PyInstaller
        print("PyInstaller is installed.")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully.")

def build_executable():
    print("\n" + "="*50)
    print("Building Chat Analyzer Executable")
    print("="*50 + "\n")
    
    if os.path.exists("dist"):
        import shutil
        shutil.rmtree("dist")
        print("Cleaned previous build.")
    
    print("Building executable...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "chat_analyzer.spec", "--clean"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False
    
    print("Build completed successfully!")
    
    dist_path = Path("dist")
    exe_path = dist_path / "ChatAnalyzer.exe" if sys.platform == "win32" else dist_path / "ChatAnalyzer"
    
    if exe_path.exists():
        print(f"\nExecutable created: {exe_path}")
        print(f"Size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        return True
    else:
        print("Executable not found in dist folder.")
        return False

def main():
    check_pyinstaller()
    success = build_executable()
    
    if success:
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL")
        print("="*50)
        print("\nYou can find the executable in the 'dist' folder.")
        print("You can now distribute it to users without Python.")
    else:
        print("\nBuild failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
