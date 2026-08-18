#!/usr/bin/env python3
"""Script de build para Electricitron - Windows EXE."""
import subprocess
import sys
import os


def build_windows():
    """Build executable for Windows using PyInstaller."""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Electricitron",
        "--windowed",
        "--onefile",
        "--add-data=assets;assets",
        "--clean",
        "--noconfirm",
        "electricitron/main.py"
    ]
    if os.path.exists("assets/icon.ico"):
        cmd.insert(5, "--icon=assets/icon.ico")
    subprocess.run(cmd, check=True)
    print("Build Windows completado: dist/Electricitron.exe")


if __name__ == "__main__":
    build_windows()
