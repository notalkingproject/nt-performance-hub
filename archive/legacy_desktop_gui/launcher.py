"""Launcher for the archived NT Performance Hub desktop GUI."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path
from tkinter import messagebox


SCRIPT_DIR = Path(__file__).resolve().parent
GUI_FILE = SCRIPT_DIR / "desktop_gui.py"


def main() -> int:
    try:
        if not GUI_FILE.exists():
            raise FileNotFoundError(f"Desktop GUI not found: {GUI_FILE}")
        runpy.run_path(str(GUI_FILE), run_name="__main__")
    except Exception as exc:
        messagebox.showerror("Beatlink Watcher Launcher", str(exc))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
